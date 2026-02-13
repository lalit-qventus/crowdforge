import {
  CATEGORY_BASE_KARMA,
  SALES_KARMA_RATE,
  AI_ACTIVE_BUILD_RATE,
  VESTING_IMMEDIATE_FRACTION,
  REVERT_PENALTY_MULTIPLIER,
  type ContributionCategory,
  type MilestoneStage,
} from "./constants.js";
import { effectivePioneerMultiplier } from "./pioneer.js";
import { upvoteScore } from "./upvote.js";

export interface KarmaInput {
  category: ContributionCategory;
  daysSinceProjectCreation: number;
  milestoneStage: MilestoneStage;
  upvoteCount: number;
  isAiAgent: boolean;
  isActiveBuild: boolean;
  /** Only for sales category: attributed revenue in cents */
  revenueCents?: number;
}

export interface KarmaResult {
  totalKarma: number;
  vestedKarma: number;
  unvestedKarma: number;
  breakdown: KarmaBreakdown;
}

export interface KarmaBreakdown {
  baseKarma: number;
  pioneerMultiplier: number;
  upvoteScore: number;
  upvoteMultiplier: number;
  aiRate: number;
  totalKarma: number;
}

function baseKarma(category: ContributionCategory, revenueCents?: number): number {
  if (category === "sales") {
    return ((revenueCents ?? 0) / 100) * SALES_KARMA_RATE;
  }
  return CATEGORY_BASE_KARMA[category];
}

export function computeKarma(input: KarmaInput): KarmaResult {
  const base = baseKarma(input.category, input.revenueCents);
  const pioneer = effectivePioneerMultiplier(input.daysSinceProjectCreation, input.milestoneStage);
  const uScore = upvoteScore(input.upvoteCount);
  const upvoteMultiplier = 1 + uScore;
  const aiRate = input.isAiAgent && input.isActiveBuild ? AI_ACTIVE_BUILD_RATE : 1.0;

  const totalKarma = base * pioneer * upvoteMultiplier * aiRate;
  const vestedKarma = totalKarma * VESTING_IMMEDIATE_FRACTION;
  const unvestedKarma = totalKarma - vestedKarma;

  return {
    totalKarma,
    vestedKarma,
    unvestedKarma,
    breakdown: {
      baseKarma: base,
      pioneerMultiplier: pioneer,
      upvoteScore: uScore,
      upvoteMultiplier,
      aiRate,
      totalKarma,
    },
  };
}

/**
 * Recompute karma for a contribution with a changed upvote count.
 * Returns the delta from the previous total.
 */
export function computeUpvoteDelta(
  input: KarmaInput,
  previousTotalKarma: number,
): KarmaResult & { delta: number } {
  const result = computeKarma(input);
  const delta = result.totalKarma - previousTotalKarma;
  const vestedDelta = delta * VESTING_IMMEDIATE_FRACTION;
  const unvestedDelta = delta - vestedDelta;

  return {
    ...result,
    totalKarma: delta,
    vestedKarma: vestedDelta,
    unvestedKarma: unvestedDelta,
    delta,
  };
}

/**
 * Revert penalty: 120% clawback of all karma ever granted for a contribution.
 */
export function computeRevertPenalty(totalKarmaGranted: number): {
  penaltyKarma: number;
  breakdown: { totalGranted: number; penaltyMultiplier: number };
} {
  const penaltyKarma = totalKarmaGranted === 0 ? 0 : -(totalKarmaGranted * REVERT_PENALTY_MULTIPLIER);

  return {
    penaltyKarma,
    breakdown: {
      totalGranted: totalKarmaGranted,
      penaltyMultiplier: REVERT_PENALTY_MULTIPLIER,
    },
  };
}
