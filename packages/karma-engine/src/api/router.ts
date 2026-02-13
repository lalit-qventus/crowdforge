import { router } from "./trpc.js";
import {
  getBalanceQuery,
  getProjectBreakdownQuery,
  getContributionKarmaQuery,
  getHistoryQuery,
  getProjectionQuery,
  getTierQuery,
  getLeaderboardQuery,
  getPayoutHistoryQuery,
  getFormulaExplainerQuery,
  verifyDeterminismQuery,
} from "./queries.js";
import {
  onContributionAccepted,
  onUpvoteChanged,
  onContributionReverted,
  onMilestoneAchieved,
  runPayoutCycle,
  runVestingRelease,
  releaseHoldbackMutation,
  rebuildProjectBalancesMutation,
} from "./mutations.js";

export const karmaRouter = router({
  // Queries
  getBalance: getBalanceQuery,
  getProjectBreakdown: getProjectBreakdownQuery,
  getContributionKarma: getContributionKarmaQuery,
  getHistory: getHistoryQuery,
  getProjection: getProjectionQuery,
  getTier: getTierQuery,
  getLeaderboard: getLeaderboardQuery,
  getPayoutHistory: getPayoutHistoryQuery,
  getFormulaExplainer: getFormulaExplainerQuery,
  verifyDeterminism: verifyDeterminismQuery,

  // Mutations
  onContributionAccepted,
  onUpvoteChanged,
  onContributionReverted,
  onMilestoneAchieved,
  runPayoutCycle,
  runVestingRelease,
  releaseHoldback: releaseHoldbackMutation,
  rebuildProjectBalances: rebuildProjectBalancesMutation,
});

export type KarmaRouter = typeof karmaRouter;
