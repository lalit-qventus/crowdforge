import { eq, sql, gt } from "drizzle-orm";
import type { Db } from "../db/connection.js";
import { contributorTiers, karmaBalances, type ContributorTier } from "../db/schema.js";
import { getTierThresholds, computeTierFromKarma } from "./thresholds.js";

export interface TierUpdateResult {
  previousTier: number;
  newTier: number;
  cumulativeKarma: number;
  changed: boolean;
}

/**
 * Recalculate a contributor's cross-project tier.
 * Aggregates karma across all projects, applies ratchet guarantee.
 */
export async function recalculateTier(
  db: Db,
  userId: string,
): Promise<TierUpdateResult> {
  const thresholds = await getTierThresholds(db);

  // Sum karma across all projects (only positive balances)
  const [cumulativeRow] = await db
    .select({
      total: sql<string>`COALESCE(SUM(GREATEST(${karmaBalances.totalKarma}::numeric, 0)), 0)`,
    })
    .from(karmaBalances)
    .where(eq(karmaBalances.contributorId, userId));

  const cumulativeKarma = Number(cumulativeRow!.total);
  const computed = computeTierFromKarma(cumulativeKarma, thresholds);

  // Get current tier record (or create)
  const [existing] = await db
    .select()
    .from(contributorTiers)
    .where(eq(contributorTiers.userId, userId));

  const previousTier = existing?.tier ?? 0;
  const highestEver = Math.max(computed.tier, existing?.highestTierEver ?? 0);

  // Ratchet: tier never decreases
  const finalTier = Math.max(computed.tier, highestEver);
  const finalMultiplier = finalTier === computed.tier
    ? computed.multiplier
    : Number(thresholds.find((t) => t.tier === finalTier)?.multiplier ?? 0);

  // Upsert tier record
  await db
    .insert(contributorTiers)
    .values({
      userId,
      cumulativeKarma: cumulativeKarma.toFixed(4),
      tier: finalTier,
      tierMultiplier: finalMultiplier.toFixed(1),
      highestTierEver: highestEver,
    })
    .onConflictDoUpdate({
      target: contributorTiers.userId,
      set: {
        cumulativeKarma: cumulativeKarma.toFixed(4),
        tier: finalTier,
        tierMultiplier: finalMultiplier.toFixed(1),
        highestTierEver: highestEver,
      },
    });

  return {
    previousTier,
    newTier: finalTier,
    cumulativeKarma,
    changed: previousTier !== finalTier,
  };
}

export async function getTier(db: Db, userId: string): Promise<ContributorTier | null> {
  const [row] = await db
    .select()
    .from(contributorTiers)
    .where(eq(contributorTiers.userId, userId));
  return row ?? null;
}
