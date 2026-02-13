export const PIONEER_BONUS = 2.0;
export const DECAY_RATE = 0.01;

export const VESTING_IMMEDIATE_FRACTION = 0.25;
export const VESTING_DURATION_DAYS = 90;

export const AI_ACTIVE_BUILD_RATE = 0.7;

export const REVERT_PENALTY_MULTIPLIER = 1.20;

// 100% of revenue goes to karma-weighted contributors.
// The platform earns its share through karma (for hosting, tooling,
// infrastructure) — same system as everyone else. Zero commission.
export const REVENUE_SPLIT = {
  contributors: 1.0,
  platform: 0,
  treasury: 0,
} as const;

export const HOLDBACK_FRACTION = 0.20;
export const HOLDBACK_RELEASE_DAYS = 30;

export const MIN_PAYOUT_SHARE = 0.001; // 0.1% of project karma
export const MIN_TRUST_LEVEL = 3;

export const CATEGORY_BASE_KARMA = {
  ideation: 5,
  code: 10,
  design: 8,
  testing: 7,
  marketing: 6,
  sales: 0, // computed from revenue
  governance: 4,
} as const;

export type ContributionCategory = keyof typeof CATEGORY_BASE_KARMA;

export const SALES_KARMA_RATE = 0.01; // 1 karma per $100 → 0.01 karma per dollar

// Milestone fractions applied to the pioneer bonus portion
export const MILESTONE_FRACTIONS = {
  none: 0,
  milestone1: 0.5,
  milestone2: 1.0,
} as const;

export type MilestoneStage = keyof typeof MILESTONE_FRACTIONS;

// Milestone 1: 10 accepted contributions from 5+ unique contributors
export const MILESTONE_1_ACCEPTED_COUNT = 10;
export const MILESTONE_1_UNIQUE_CONTRIBUTORS = 5;

// Milestone 2: first revenue OR 50 accepted contributions
export const MILESTONE_2_ACCEPTED_COUNT = 50;
