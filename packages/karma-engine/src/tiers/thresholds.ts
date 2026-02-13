import { asc } from "drizzle-orm";
import type { Db } from "../db/connection.js";
import { tierThresholds, type TierThreshold } from "../db/schema.js";

let cachedThresholds: TierThreshold[] | null = null;

export async function getTierThresholds(db: Db): Promise<TierThreshold[]> {
  if (cachedThresholds) return cachedThresholds;

  cachedThresholds = await db
    .select()
    .from(tierThresholds)
    .orderBy(asc(tierThresholds.tier));

  return cachedThresholds;
}

export function invalidateThresholdCache() {
  cachedThresholds = null;
}

/**
 * Determine tier from cumulative karma using loaded thresholds.
 * Returns the highest tier whose threshold is met.
 */
export function computeTierFromKarma(
  cumulativeKarma: number,
  thresholds: TierThreshold[],
): { tier: number; multiplier: number } {
  let result = { tier: 0, multiplier: 0 };

  for (const t of thresholds) {
    if (cumulativeKarma >= Number(t.karmaThreshold)) {
      result = { tier: t.tier, multiplier: Number(t.multiplier) };
    }
  }

  return result;
}
