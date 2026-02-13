// Database
export { createDb, type Db } from "./db/connection.js";
export * from "./db/schema.js";
export { seedTierThresholds, TIER_SEEDS } from "./db/seed.js";

// Calculator (pure functions)
export { computeKarma, computeUpvoteDelta, computeRevertPenalty } from "./calculator/karma.js";
export type { KarmaInput, KarmaResult, KarmaBreakdown } from "./calculator/karma.js";
export { rawPioneerMultiplier, effectivePioneerMultiplier } from "./calculator/pioneer.js";
export { upvoteScore } from "./calculator/upvote.js";
export * from "./calculator/constants.js";

// Ledger
export { appendLedgerEntry, appendLedgerBatch } from "./ledger/append.js";
export type { LedgerEntryInput } from "./ledger/append.js";
export { getBalance, getProjectBreakdown, getContributionKarma, getHistory, getLeaderboard } from "./ledger/balance.js";
export { rebuildProjectBalances, verifyProjectDeterminism } from "./ledger/rebuild.js";
export { updateMilestoneProgress, applyMilestoneRetroactive, getMilestoneStage } from "./ledger/milestones.js";

// Tiers
export { recalculateTier, getTier } from "./tiers/engine.js";
export { getTierThresholds, computeTierFromKarma, invalidateThresholdCache } from "./tiers/thresholds.js";

// Vesting
export { createVestingSchedule, cancelVestingForLedgerEntry, getActiveVestingSchedules } from "./vesting/schedule.js";
export { processVestingReleases } from "./vesting/release.js";

// Revenue
export { calculatePayouts, releaseHoldback, getPayoutHistory } from "./revenue/distributor.js";
export type { PayoutCalculationInput, PayoutResult, PayoutLineItemResult } from "./revenue/distributor.js";

// Audit
export { verifyDeterminism } from "./audit/determinism.js";
export { explainKarmaCalculation } from "./audit/explainer.js";

// API
export { karmaRouter, type KarmaRouter } from "./api/router.js";
export type { KarmaContext } from "./api/trpc.js";
