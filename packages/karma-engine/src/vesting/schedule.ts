import { eq, and, sql } from "drizzle-orm";
import type { Db } from "../db/connection.js";
import { vestingSchedule } from "../db/schema.js";
import { VESTING_DURATION_DAYS } from "../calculator/constants.js";

/**
 * Create a vesting schedule entry for the unvested portion of a karma award.
 * Vesting is linear over 90 days from the start date.
 */
export async function createVestingSchedule(
  db: Db,
  params: {
    ledgerEntryId: bigint;
    projectId: string;
    contributorId: string;
    totalUnvested: string;
    vestingStartAt: Date;
  },
): Promise<string> {
  const vestingEndAt = new Date(params.vestingStartAt);
  vestingEndAt.setDate(vestingEndAt.getDate() + VESTING_DURATION_DAYS);

  const [row] = await db
    .insert(vestingSchedule)
    .values({
      ledgerEntryId: params.ledgerEntryId,
      projectId: params.projectId,
      contributorId: params.contributorId,
      totalUnvested: params.totalUnvested,
      vestedSoFar: "0",
      vestingStartAt: params.vestingStartAt,
      vestingEndAt,
      fullyVested: false,
    })
    .returning({ id: vestingSchedule.id });

  return row!.id;
}

/**
 * Cancel all unvested vesting entries for a contribution.
 * Used during revert: marks entries as fully vested (nothing left to vest).
 */
export async function cancelVestingForLedgerEntry(
  db: Db,
  ledgerEntryId: bigint,
): Promise<number> {
  const result = await db
    .update(vestingSchedule)
    .set({ fullyVested: true })
    .where(
      and(
        eq(vestingSchedule.ledgerEntryId, ledgerEntryId),
        eq(vestingSchedule.fullyVested, false),
      ),
    );

  return result.count;
}

export async function getActiveVestingSchedules(
  db: Db,
  projectId: string,
  contributorId: string,
) {
  return db
    .select()
    .from(vestingSchedule)
    .where(
      and(
        eq(vestingSchedule.projectId, projectId),
        eq(vestingSchedule.contributorId, contributorId),
        eq(vestingSchedule.fullyVested, false),
      ),
    );
}
