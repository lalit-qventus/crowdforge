import type { KarmaBreakdown } from "../calculator/karma.js";
import type { ContributionCategory } from "../calculator/constants.js";
import { CATEGORY_BASE_KARMA, SALES_KARMA_RATE } from "../calculator/constants.js";

/**
 * Produce a human-readable explanation of a karma calculation.
 */
export function explainKarmaCalculation(
  breakdown: KarmaBreakdown,
  category: ContributionCategory,
  context: {
    daysSinceCreation: number;
    upvoteCount: number;
    isAiAgent: boolean;
    milestoneStage: string;
    revenueCents?: number;
  },
): string[] {
  const lines: string[] = [];

  // Base karma
  if (category === "sales") {
    const revenue = (context.revenueCents ?? 0) / 100;
    lines.push(
      `Base karma: $${revenue.toFixed(2)} revenue × ${SALES_KARMA_RATE}/$ = ${breakdown.baseKarma.toFixed(2)} karma`,
    );
  } else {
    lines.push(
      `Base karma: ${CATEGORY_BASE_KARMA[category]} (${category} contribution)`,
    );
  }

  // Pioneer multiplier
  lines.push(
    `Pioneer multiplier: ${breakdown.pioneerMultiplier.toFixed(4)}x ` +
      `(day ${context.daysSinceCreation}, milestone: ${context.milestoneStage})`,
  );

  // Upvote score
  if (context.upvoteCount > 0) {
    lines.push(
      `Upvote bonus: ln(1 + ${context.upvoteCount}) / ln(10) = ${breakdown.upvoteScore.toFixed(4)} → ${breakdown.upvoteMultiplier.toFixed(4)}x`,
    );
  } else {
    lines.push(`Upvote bonus: none (0 upvotes) → 1.0x`);
  }

  // AI rate
  if (context.isAiAgent) {
    lines.push(`AI agent rate: ${breakdown.aiRate}x`);
  }

  // Total
  lines.push(
    `Total: ${breakdown.baseKarma.toFixed(2)} × ${breakdown.pioneerMultiplier.toFixed(4)} × ${breakdown.upvoteMultiplier.toFixed(4)}` +
      (context.isAiAgent ? ` × ${breakdown.aiRate}` : "") +
      ` = ${breakdown.totalKarma.toFixed(4)} karma`,
  );

  return lines;
}
