/**
 * Upvote score: `ln(1 + upvote_count) / ln(10)`
 *
 * 0 upvotes → 0, 1 → 0.30, 9 → 1.0, 99 → 2.0
 */
export function upvoteScore(upvoteCount: number): number {
  return Math.log(1 + upvoteCount) / Math.LN10;
}
