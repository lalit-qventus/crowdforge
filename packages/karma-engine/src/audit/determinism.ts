import type { Db } from "../db/connection.js";
import { verifyProjectDeterminism, type DeterminismMismatch } from "../ledger/rebuild.js";

export interface DeterminismReport {
  projectId: string;
  isValid: boolean;
  mismatches: DeterminismMismatch[];
  checkedAt: Date;
}

/**
 * Run a determinism verification for a project.
 * Recomputes all balances from the ledger and compares to the cached values.
 */
export async function verifyDeterminism(
  db: Db,
  projectId: string,
): Promise<DeterminismReport> {
  const { isValid, mismatches } = await verifyProjectDeterminism(db, projectId);

  return {
    projectId,
    isValid,
    mismatches,
    checkedAt: new Date(),
  };
}
