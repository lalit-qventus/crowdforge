import { eq, and, sql, gt } from "drizzle-orm";
import type { Db } from "../db/connection.js";
import {
  karmaBalances,
  contributorTiers,
  payoutCycles,
  payoutLineItems,
} from "../db/schema.js";
import {
  REVENUE_SPLIT,
  HOLDBACK_FRACTION,
  MIN_PAYOUT_SHARE,
  MIN_TRUST_LEVEL,
} from "../calculator/constants.js";

export interface PayoutCalculationInput {
  projectId: string;
  cycleStart: Date;
  cycleEnd: Date;
  netRevenue: number;
  isSingleContributor: boolean;
  /** Map of contributorId → trust level (for eligibility filtering) */
  contributorTrustLevels: Map<string, number>;
  /** Map of contributorId → parent user id (for AI agents) */
  aiAgentParents: Map<string, string>;
}

export interface PayoutResult {
  cycleId: string;
  contributorPool: number;
  platformFee: number;
  treasuryAllocation: number;
  lineItems: PayoutLineItemResult[];
}

export interface PayoutLineItemResult {
  contributorId: string;
  vestedKarma: number;
  tierMultiplier: number;
  weightedKarma: number;
  sharePercent: number;
  grossPayout: number;
  holdbackAmount: number;
  netPayout: number;
  parentUserId: string | null;
}

/**
 * Calculate and record a monthly payout cycle.
 * Treasury fee is waived for single-contributor projects.
 */
export async function calculatePayouts(
  db: Db,
  input: PayoutCalculationInput,
): Promise<PayoutResult> {
  // Revenue split — treasury waived for single-contributor
  const treasuryRate = input.isSingleContributor ? 0 : REVENUE_SPLIT.treasury;
  const contributorRate = input.isSingleContributor
    ? REVENUE_SPLIT.contributors + REVENUE_SPLIT.treasury
    : REVENUE_SPLIT.contributors;

  const contributorPool = input.netRevenue * contributorRate;
  const platformFee = input.netRevenue * REVENUE_SPLIT.platform;
  const treasuryAllocation = input.netRevenue * treasuryRate;

  // Fetch all balances for the project
  const balances = await db
    .select()
    .from(karmaBalances)
    .where(eq(karmaBalances.projectId, input.projectId));

  // Get total vested karma for share threshold calculation
  const totalVestedKarma = balances.reduce(
    (sum, b) => sum + Math.max(Number(b.vestedKarma), 0),
    0,
  );

  // Filter eligible contributors
  const eligible = balances.filter((b) => {
    const vested = Math.max(Number(b.vestedKarma), 0);
    if (vested <= 0) return false;

    // Minimum share threshold
    if (totalVestedKarma > 0 && vested / totalVestedKarma < MIN_PAYOUT_SHARE) return false;

    // Trust level check
    const trust = input.contributorTrustLevels.get(b.contributorId) ?? 0;
    if (trust < MIN_TRUST_LEVEL) return false;

    return true;
  });

  // Fetch tier multipliers for eligible contributors
  const tierMap = new Map<string, number>();
  for (const b of eligible) {
    const [tier] = await db
      .select()
      .from(contributorTiers)
      .where(eq(contributorTiers.userId, b.contributorId));
    tierMap.set(b.contributorId, tier ? Number(tier.tierMultiplier) : 0);
  }

  // Calculate weighted karma
  const weighted = eligible.map((b) => {
    const vested = Math.max(Number(b.vestedKarma), 0);
    const multiplier = tierMap.get(b.contributorId) ?? 0;
    return {
      contributorId: b.contributorId,
      vestedKarma: vested,
      tierMultiplier: multiplier,
      weightedKarma: vested * multiplier,
    };
  });

  const totalWeightedKarma = weighted.reduce((sum, w) => sum + w.weightedKarma, 0);

  // Calculate individual payouts
  const lineItems: PayoutLineItemResult[] = weighted
    .filter((w) => w.weightedKarma > 0)
    .map((w) => {
      const sharePercent = totalWeightedKarma > 0 ? w.weightedKarma / totalWeightedKarma : 0;
      const grossPayout = contributorPool * sharePercent;
      const holdbackAmount = grossPayout * HOLDBACK_FRACTION;
      const netPayout = grossPayout - holdbackAmount;

      return {
        contributorId: w.contributorId,
        vestedKarma: w.vestedKarma,
        tierMultiplier: w.tierMultiplier,
        weightedKarma: w.weightedKarma,
        sharePercent,
        grossPayout,
        holdbackAmount,
        netPayout,
        parentUserId: input.aiAgentParents.get(w.contributorId) ?? null,
      };
    });

  // Verify invariant: sum of gross payouts <= contributor pool
  const totalGross = lineItems.reduce((sum, li) => sum + li.grossPayout, 0);
  if (totalGross > contributorPool + 0.01) {
    throw new Error(
      `Payout invariant violated: totalGross (${totalGross}) > contributorPool (${contributorPool})`,
    );
  }

  // Persist cycle and line items in a single transaction
  const cycleId = await db.transaction(async (tx) => {
    const [cycle] = await tx
      .insert(payoutCycles)
      .values({
        projectId: input.projectId,
        cycleStart: input.cycleStart,
        cycleEnd: input.cycleEnd,
        netRevenue: input.netRevenue.toFixed(2),
        contributorPool: contributorPool.toFixed(2),
        platformFee: platformFee.toFixed(2),
        treasuryAllocation: treasuryAllocation.toFixed(2),
        totalWeightedKarma: totalWeightedKarma.toFixed(4),
        status: "calculated",
      })
      .returning({ id: payoutCycles.id });

    for (const li of lineItems) {
      await tx.insert(payoutLineItems).values({
        payoutCycleId: cycle!.id,
        contributorId: li.contributorId,
        vestedKarma: li.vestedKarma.toFixed(4),
        tierMultiplier: li.tierMultiplier.toFixed(1),
        weightedKarma: li.weightedKarma.toFixed(4),
        sharePercent: li.sharePercent.toFixed(6),
        grossPayout: li.grossPayout.toFixed(2),
        holdbackAmount: li.holdbackAmount.toFixed(2),
        netPayout: li.netPayout.toFixed(2),
        parentUserId: li.parentUserId,
        snapshotData: {
          totalWeightedKarma,
          contributorPool,
          eligibleCount: lineItems.length,
        },
      });
    }

    return cycle!.id;
  });

  return {
    cycleId,
    contributorPool,
    platformFee,
    treasuryAllocation,
    lineItems,
  };
}

/**
 * Release holdback for a payout cycle after 30 days.
 */
export async function releaseHoldback(
  db: Db,
  payoutCycleId: string,
): Promise<number> {
  const result = await db
    .update(payoutLineItems)
    .set({ holdbackReleasedAt: new Date() })
    .where(
      and(
        eq(payoutLineItems.payoutCycleId, payoutCycleId),
        sql`${payoutLineItems.holdbackReleasedAt} IS NULL`,
      ),
    );

  return result.count;
}

export async function getPayoutHistory(
  db: Db,
  contributorId: string,
  opts: { limit: number; offset: number },
) {
  return db
    .select()
    .from(payoutLineItems)
    .where(eq(payoutLineItems.contributorId, contributorId))
    .orderBy(sql`${payoutLineItems.createdAt} DESC`)
    .limit(opts.limit)
    .offset(opts.offset);
}
