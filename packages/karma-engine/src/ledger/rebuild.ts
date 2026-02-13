import { eq, sql } from "drizzle-orm";
import type { Db } from "../db/connection.js";
import { karmaLedger, karmaBalances } from "../db/schema.js";

/**
 * Rebuild all balance caches for a project from the ledger.
 * Deletes existing balances and recomputes from scratch.
 */
export async function rebuildProjectBalances(db: Db, projectId: string): Promise<number> {
  return db.transaction(async (tx) => {
    // Delete existing balances for the project
    await tx.delete(karmaBalances).where(eq(karmaBalances.projectId, projectId));

    // Reaggregate from ledger
    const result = await tx.execute(sql`
      INSERT INTO karma_balances (project_id, contributor_id, total_karma, vested_karma, unvested_karma, last_ledger_id)
      SELECT
        project_id,
        contributor_id,
        COALESCE(SUM(karma_delta::numeric), 0),
        COALESCE(SUM(vested_karma_delta::numeric), 0),
        COALESCE(SUM(unvested_karma_delta::numeric), 0),
        MAX(id)
      FROM karma_ledger
      WHERE project_id = ${projectId}
      GROUP BY project_id, contributor_id
    `);

    return Number(result.count);
  });
}

/**
 * Verify that balance cache matches ledger aggregation.
 * Returns mismatches for auditing.
 */
export async function verifyProjectDeterminism(
  db: Db,
  projectId: string,
): Promise<{ isValid: boolean; mismatches: DeterminismMismatch[] }> {
  const mismatches = await db.execute(sql`
    WITH ledger_sums AS (
      SELECT
        project_id,
        contributor_id,
        COALESCE(SUM(karma_delta::numeric), 0) AS expected_total,
        COALESCE(SUM(vested_karma_delta::numeric), 0) AS expected_vested,
        COALESCE(SUM(unvested_karma_delta::numeric), 0) AS expected_unvested
      FROM karma_ledger
      WHERE project_id = ${projectId}
      GROUP BY project_id, contributor_id
    )
    SELECT
      ls.contributor_id,
      ls.expected_total,
      ls.expected_vested,
      ls.expected_unvested,
      kb.total_karma AS actual_total,
      kb.vested_karma AS actual_vested,
      kb.unvested_karma AS actual_unvested
    FROM ledger_sums ls
    LEFT JOIN karma_balances kb
      ON kb.project_id = ls.project_id
      AND kb.contributor_id = ls.contributor_id
    WHERE
      kb.total_karma IS NULL
      OR kb.total_karma::numeric != ls.expected_total
      OR kb.vested_karma::numeric != ls.expected_vested
      OR kb.unvested_karma::numeric != ls.expected_unvested
  `);

  const rows = [...mismatches] as unknown as DeterminismMismatch[];
  return { isValid: rows.length === 0, mismatches: rows };
}

export interface DeterminismMismatch {
  contributor_id: string;
  expected_total: string;
  expected_vested: string;
  expected_unvested: string;
  actual_total: string | null;
  actual_vested: string | null;
  actual_unvested: string | null;
}
