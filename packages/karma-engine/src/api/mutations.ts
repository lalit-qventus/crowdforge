import { z } from "zod";
import { publicProcedure } from "./trpc.js";
import { computeKarma, computeUpvoteDelta, computeRevertPenalty, type KarmaInput } from "../calculator/karma.js";
import { appendLedgerEntry, type LedgerEntryInput } from "../ledger/append.js";
import { getContributionKarma } from "../ledger/balance.js";
import { createVestingSchedule, cancelVestingForLedgerEntry } from "../vesting/schedule.js";
import { processVestingReleases } from "../vesting/release.js";
import { recalculateTier } from "../tiers/engine.js";
import { updateMilestoneProgress, applyMilestoneRetroactive, getMilestoneStage } from "../ledger/milestones.js";
import { calculatePayouts, releaseHoldback, type PayoutCalculationInput } from "../revenue/distributor.js";
import { rebuildProjectBalances } from "../ledger/rebuild.js";
import { VESTING_IMMEDIATE_FRACTION } from "../calculator/constants.js";

export const onContributionAccepted = publicProcedure
  .input(
    z.object({
      projectId: z.string().uuid(),
      contributorId: z.string().uuid(),
      contributionId: z.string().uuid(),
      category: z.enum(["ideation", "code", "design", "testing", "marketing", "sales", "governance"]),
      daysSinceProjectCreation: z.number().min(0),
      upvoteCount: z.number().int().min(0),
      isAiAgent: z.boolean(),
      isActiveBuild: z.boolean(),
      revenueCents: z.number().int().optional(),
      submittedAt: z.date(),
    }),
  )
  .mutation(async ({ ctx, input }) => {
    const milestoneStage = await getMilestoneStage(ctx.db, input.projectId);

    const karmaInput: KarmaInput = {
      category: input.category,
      daysSinceProjectCreation: input.daysSinceProjectCreation,
      milestoneStage,
      upvoteCount: input.upvoteCount,
      isAiAgent: input.isAiAgent,
      isActiveBuild: input.isActiveBuild,
      revenueCents: input.revenueCents,
    };

    const result = computeKarma(karmaInput);

    // Append to ledger + update balance
    const ledgerEntryId = await appendLedgerEntry(ctx.db, {
      eventType: "contribution_accepted",
      projectId: input.projectId,
      contributorId: input.contributorId,
      contributionId: input.contributionId,
      karmaDelta: result.totalKarma.toFixed(4),
      vestedKarmaDelta: result.vestedKarma.toFixed(4),
      unvestedKarmaDelta: result.unvestedKarma.toFixed(4),
      formulaInputs: {
        ...result.breakdown,
        category: input.category,
        daysSinceProjectCreation: input.daysSinceProjectCreation,
        milestoneStage,
        upvoteCount: input.upvoteCount,
        isAiAgent: input.isAiAgent,
        isActiveBuild: input.isActiveBuild,
        revenueCents: input.revenueCents,
      },
      idempotencyKey: `contribution_accepted:${input.contributionId}`,
    });

    if (!ledgerEntryId) return { idempotent: true, karma: result };

    // Create vesting schedule for unvested portion
    if (result.unvestedKarma > 0) {
      await createVestingSchedule(ctx.db, {
        ledgerEntryId,
        projectId: input.projectId,
        contributorId: input.contributorId,
        totalUnvested: result.unvestedKarma.toFixed(4),
        vestingStartAt: input.submittedAt,
      });
    }

    // Update milestone counters, check for milestone achievement
    const milestoneEvent = await updateMilestoneProgress(
      ctx.db,
      input.projectId,
      input.contributorId,
      input.category === "sales",
    );

    // If a milestone was just hit, apply retroactive bonuses
    let retroactiveCount = 0;
    if (milestoneEvent) {
      retroactiveCount = await applyMilestoneRetroactive(
        ctx.db,
        input.projectId,
        milestoneEvent,
      );
    }

    // Recalculate contributor tier
    const tierResult = await recalculateTier(ctx.db, input.contributorId);

    return {
      idempotent: false,
      karma: result,
      ledgerEntryId: ledgerEntryId.toString(),
      milestoneEvent,
      retroactiveCount,
      tierChanged: tierResult.changed,
      newTier: tierResult.newTier,
    };
  });

export const onUpvoteChanged = publicProcedure
  .input(
    z.object({
      projectId: z.string().uuid(),
      contributorId: z.string().uuid(),
      contributionId: z.string().uuid(),
      category: z.enum(["ideation", "code", "design", "testing", "marketing", "sales", "governance"]),
      daysSinceProjectCreation: z.number().min(0),
      newUpvoteCount: z.number().int().min(0),
      isAiAgent: z.boolean(),
      isActiveBuild: z.boolean(),
      revenueCents: z.number().int().optional(),
      eventType: z.enum(["upvote_added", "upvote_removed"]),
    }),
  )
  .mutation(async ({ ctx, input }) => {
    const milestoneStage = await getMilestoneStage(ctx.db, input.projectId);

    // Get previous total karma for this contribution
    const priorEntries = await getContributionKarma(ctx.db, input.contributionId);
    const previousTotalKarma = priorEntries.reduce(
      (sum, e) => sum + Number(e.karmaDelta),
      0,
    );

    const karmaInput: KarmaInput = {
      category: input.category,
      daysSinceProjectCreation: input.daysSinceProjectCreation,
      milestoneStage,
      upvoteCount: input.newUpvoteCount,
      isAiAgent: input.isAiAgent,
      isActiveBuild: input.isActiveBuild,
      revenueCents: input.revenueCents,
    };

    const result = computeUpvoteDelta(karmaInput, previousTotalKarma);

    if (Math.abs(result.delta) < 0.0001) return { delta: 0 };

    const vestedDelta = result.delta * VESTING_IMMEDIATE_FRACTION;
    const unvestedDelta = result.delta - vestedDelta;

    await appendLedgerEntry(ctx.db, {
      eventType: input.eventType,
      projectId: input.projectId,
      contributorId: input.contributorId,
      contributionId: input.contributionId,
      karmaDelta: result.delta.toFixed(4),
      vestedKarmaDelta: vestedDelta.toFixed(4),
      unvestedKarmaDelta: unvestedDelta.toFixed(4),
      formulaInputs: {
        ...result.breakdown,
        previousTotalKarma,
        newUpvoteCount: input.newUpvoteCount,
        delta: result.delta,
      },
      idempotencyKey: `${input.eventType}:${input.contributionId}:${input.newUpvoteCount}`,
    });

    // Recalculate tier
    await recalculateTier(ctx.db, input.contributorId);

    return { delta: result.delta };
  });

export const onContributionReverted = publicProcedure
  .input(
    z.object({
      projectId: z.string().uuid(),
      contributorId: z.string().uuid(),
      contributionId: z.string().uuid(),
    }),
  )
  .mutation(async ({ ctx, input }) => {
    // Sum all karma ever granted for this contribution
    const entries = await getContributionKarma(ctx.db, input.contributionId);
    const totalGranted = entries.reduce(
      (sum, e) => sum + Math.max(Number(e.karmaDelta), 0),
      0,
    );

    const penalty = computeRevertPenalty(totalGranted);

    // Cancel all unvested vesting entries for this contribution's ledger entries
    for (const entry of entries) {
      await cancelVestingForLedgerEntry(ctx.db, entry.id);
    }

    // Write penalty entry — all penalty goes to vested (immediate impact)
    await appendLedgerEntry(ctx.db, {
      eventType: "revert_penalty",
      projectId: input.projectId,
      contributorId: input.contributorId,
      contributionId: input.contributionId,
      karmaDelta: penalty.penaltyKarma.toFixed(4),
      vestedKarmaDelta: penalty.penaltyKarma.toFixed(4),
      unvestedKarmaDelta: "0",
      formulaInputs: penalty.breakdown,
      idempotencyKey: `revert_penalty:${input.contributionId}`,
    });

    // Recalculate tier
    await recalculateTier(ctx.db, input.contributorId);

    return { penaltyKarma: penalty.penaltyKarma, totalReverted: totalGranted };
  });

export const onMilestoneAchieved = publicProcedure
  .input(
    z.object({
      projectId: z.string().uuid(),
      milestoneEvent: z.enum(["milestone_1", "milestone_2"]),
    }),
  )
  .mutation(async ({ ctx, input }) => {
    const count = await applyMilestoneRetroactive(
      ctx.db,
      input.projectId,
      input.milestoneEvent,
    );
    return { retroactiveEntriesCreated: count };
  });

export const runPayoutCycle = publicProcedure
  .input(
    z.object({
      projectId: z.string().uuid(),
      cycleStart: z.date(),
      cycleEnd: z.date(),
      netRevenue: z.number().min(0),
      isSingleContributor: z.boolean(),
      contributorTrustLevels: z.record(z.string(), z.number()),
      aiAgentParents: z.record(z.string(), z.string()),
    }),
  )
  .mutation(async ({ ctx, input }) => {
    const payoutInput: PayoutCalculationInput = {
      projectId: input.projectId,
      cycleStart: input.cycleStart,
      cycleEnd: input.cycleEnd,
      netRevenue: input.netRevenue,
      isSingleContributor: input.isSingleContributor,
      contributorTrustLevels: new Map(Object.entries(input.contributorTrustLevels)),
      aiAgentParents: new Map(Object.entries(input.aiAgentParents)),
    };

    return calculatePayouts(ctx.db, payoutInput);
  });

export const runVestingRelease = publicProcedure
  .input(z.object({ asOf: z.date().optional() }))
  .mutation(async ({ ctx, input }) => {
    return processVestingReleases(ctx.db, input.asOf);
  });

export const releaseHoldbackMutation = publicProcedure
  .input(z.object({ payoutCycleId: z.string().uuid() }))
  .mutation(async ({ ctx, input }) => {
    const count = await releaseHoldback(ctx.db, input.payoutCycleId);
    return { released: count };
  });

export const rebuildProjectBalancesMutation = publicProcedure
  .input(z.object({ projectId: z.string().uuid() }))
  .mutation(async ({ ctx, input }) => {
    const count = await rebuildProjectBalances(ctx.db, input.projectId);
    return { rebuiltCount: count };
  });
