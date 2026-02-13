import { PIONEER_BONUS, DECAY_RATE, MILESTONE_FRACTIONS, type MilestoneStage } from "./constants.js";

/**
 * Raw pioneer multiplier: `1 + pioneer_bonus * e^(-decay_rate * days)`
 *
 * Day 0 → 3.0x, Day 90 → 1.81x, Day 365 → 1.05x
 */
export function rawPioneerMultiplier(daysSinceCreation: number): number {
  return 1 + PIONEER_BONUS * Math.exp(-DECAY_RATE * daysSinceCreation);
}

/**
 * Effective pioneer multiplier gated by milestone progress.
 *
 * The milestone fraction scales only the bonus portion (raw - 1),
 * so milestone_none gives exactly 1.0x (no bonus).
 */
export function effectivePioneerMultiplier(
  daysSinceCreation: number,
  milestoneStage: MilestoneStage,
): number {
  const raw = rawPioneerMultiplier(daysSinceCreation);
  const fraction = MILESTONE_FRACTIONS[milestoneStage];
  return 1 + (raw - 1) * fraction;
}
