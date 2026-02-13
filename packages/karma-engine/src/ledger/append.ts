import { eq, and, sql } from "drizzle-orm";
import type { Db } from "../db/connection.js";
import { karmaLedger, karmaBalances, type KarmaEventType } from "../db/schema.js";

export interface LedgerEntryInput {
  eventType: KarmaEventType;
  projectId: string;
  contributorId: string;
  contributionId: string | null;
  karmaDelta: string;
  vestedKarmaDelta: string;
  unvestedKarmaDelta: string;
  formulaInputs: Record<string, unknown>;
  idempotencyKey: string;
}

/**
 * Single write path for the karma ledger.
 * Appends a ledger entry and upserts the balance cache in one transaction.
 *
 * Returns the new ledger entry ID, or null if the idempotency key already exists.
 */
export async function appendLedgerEntry(
  db: Db,
  input: LedgerEntryInput,
): Promise<bigint | null> {
  return db.transaction(async (tx) => {
    // Append to immutable ledger
    const [entry] = await tx
      .insert(karmaLedger)
      .values({
        eventType: input.eventType,
        projectId: input.projectId,
        contributorId: input.contributorId,
        contributionId: input.contributionId,
        karmaDelta: input.karmaDelta,
        vestedKarmaDelta: input.vestedKarmaDelta,
        unvestedKarmaDelta: input.unvestedKarmaDelta,
        formulaInputs: input.formulaInputs,
        idempotencyKey: input.idempotencyKey,
      })
      .onConflictDoNothing({ target: karmaLedger.idempotencyKey })
      .returning({ id: karmaLedger.id });

    if (!entry) return null; // Idempotent duplicate

    // Upsert balance cache
    await tx
      .insert(karmaBalances)
      .values({
        projectId: input.projectId,
        contributorId: input.contributorId,
        totalKarma: input.karmaDelta,
        vestedKarma: input.vestedKarmaDelta,
        unvestedKarma: input.unvestedKarmaDelta,
        lastLedgerId: entry.id,
      })
      .onConflictDoUpdate({
        target: [karmaBalances.projectId, karmaBalances.contributorId],
        set: {
          totalKarma: sql`${karmaBalances.totalKarma} + ${input.karmaDelta}::numeric`,
          vestedKarma: sql`${karmaBalances.vestedKarma} + ${input.vestedKarmaDelta}::numeric`,
          unvestedKarma: sql`${karmaBalances.unvestedKarma} + ${input.unvestedKarmaDelta}::numeric`,
          lastLedgerId: entry.id,
        },
      });

    return entry.id;
  });
}

/**
 * Append multiple ledger entries in a single transaction.
 * Used for batch operations like milestone retroactive application.
 */
export async function appendLedgerBatch(
  db: Db,
  entries: LedgerEntryInput[],
): Promise<bigint[]> {
  return db.transaction(async (tx) => {
    const ids: bigint[] = [];

    for (const input of entries) {
      const [entry] = await tx
        .insert(karmaLedger)
        .values({
          eventType: input.eventType,
          projectId: input.projectId,
          contributorId: input.contributorId,
          contributionId: input.contributionId,
          karmaDelta: input.karmaDelta,
          vestedKarmaDelta: input.vestedKarmaDelta,
          unvestedKarmaDelta: input.unvestedKarmaDelta,
          formulaInputs: input.formulaInputs,
          idempotencyKey: input.idempotencyKey,
        })
        .onConflictDoNothing({ target: karmaLedger.idempotencyKey })
        .returning({ id: karmaLedger.id });

      if (!entry) continue;
      ids.push(entry.id);

      await tx
        .insert(karmaBalances)
        .values({
          projectId: input.projectId,
          contributorId: input.contributorId,
          totalKarma: input.karmaDelta,
          vestedKarma: input.vestedKarmaDelta,
          unvestedKarma: input.unvestedKarmaDelta,
          lastLedgerId: entry.id,
        })
        .onConflictDoUpdate({
          target: [karmaBalances.projectId, karmaBalances.contributorId],
          set: {
            totalKarma: sql`${karmaBalances.totalKarma} + ${input.karmaDelta}::numeric`,
            vestedKarma: sql`${karmaBalances.vestedKarma} + ${input.vestedKarmaDelta}::numeric`,
            unvestedKarma: sql`${karmaBalances.unvestedKarma} + ${input.unvestedKarmaDelta}::numeric`,
            lastLedgerId: entry.id,
          },
        });
    }

    return ids;
  });
}
