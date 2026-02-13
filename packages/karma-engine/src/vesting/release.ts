import { eq, and, sql, lte } from "drizzle-orm";
import type { Db } from "../db/connection.js";
import { vestingSchedule, karmaLedger, karmaBalances } from "../db/schema.js";
import { VESTING_DURATION_DAYS } from "../calculator/constants.js";

export interface VestingReleaseResult {
  processed: number;
  fullyVested: number;
  totalVestedKarma: number;
}

/**
 * Daily vesting cron: process all pending vesting schedules.
 * Linear vesting: `vested = total_unvested * min(days_elapsed / 90, 1)`
 *
 * Writes `vesting_release` ledger entries that shift karma from unvested → vested.
 * The karma_delta is 0 (total doesn't change), but vested/unvested shift.
 */
export async function processVestingReleases(
  db: Db,
  asOf: Date = new Date(),
): Promise<VestingReleaseResult> {
  const result: VestingReleaseResult = { processed: 0, fullyVested: 0, totalVestedKarma: 0 };

  // Fetch all non-fully-vested schedules
  const pending = await db
    .select()
    .from(vestingSchedule)
    .where(eq(vestingSchedule.fullyVested, false));

  for (const schedule of pending) {
    const startMs = new Date(schedule.vestingStartAt).getTime();
    const endMs = new Date(schedule.vestingEndAt).getTime();
    const nowMs = asOf.getTime();
    const totalUnvested = Number(schedule.totalUnvested);
    const previouslyVested = Number(schedule.vestedSoFar);

    // Linear vesting calculation
    const elapsedDays = (nowMs - startMs) / (1000 * 60 * 60 * 24);
    const fraction = Math.min(elapsedDays / VESTING_DURATION_DAYS, 1);
    const shouldBeVested = totalUnvested * fraction;
    const newlyVested = shouldBeVested - previouslyVested;

    if (newlyVested <= 0.0001) continue; // Skip negligible amounts

    const isFullyVested = fraction >= 1;

    await db.transaction(async (tx) => {
      // Write a vesting_release ledger entry
      // karma_delta = 0 (total unchanged), shift from unvested to vested
      await tx.insert(karmaLedger).values({
        eventType: "vesting_release",
        projectId: schedule.projectId,
        contributorId: schedule.contributorId,
        contributionId: null,
        karmaDelta: "0",
        vestedKarmaDelta: newlyVested.toFixed(4),
        unvestedKarmaDelta: (-newlyVested).toFixed(4),
        formulaInputs: {
          vestingScheduleId: schedule.id,
          elapsedDays: Math.round(elapsedDays * 100) / 100,
          fraction: Math.round(fraction * 10000) / 10000,
          totalUnvested,
          previouslyVested,
          newlyVested: Math.round(newlyVested * 10000) / 10000,
        },
        idempotencyKey: `vesting:${schedule.id}:${asOf.toISOString().slice(0, 10)}`,
      }).onConflictDoNothing({ target: karmaLedger.idempotencyKey });

      // Update balance: shift unvested → vested
      await tx
        .update(karmaBalances)
        .set({
          vestedKarma: sql`${karmaBalances.vestedKarma}::numeric + ${newlyVested.toFixed(4)}::numeric`,
          unvestedKarma: sql`${karmaBalances.unvestedKarma}::numeric - ${newlyVested.toFixed(4)}::numeric`,
        })
        .where(
          and(
            eq(karmaBalances.projectId, schedule.projectId),
            eq(karmaBalances.contributorId, schedule.contributorId),
          ),
        );

      // Update vesting schedule
      await tx
        .update(vestingSchedule)
        .set({
          vestedSoFar: shouldBeVested.toFixed(4),
          fullyVested: isFullyVested,
        })
        .where(eq(vestingSchedule.id, schedule.id));
    });

    result.processed++;
    result.totalVestedKarma += newlyVested;
    if (isFullyVested) result.fullyVested++;
  }

  return result;
}
