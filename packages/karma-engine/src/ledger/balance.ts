import { eq, and, sql, desc } from "drizzle-orm";
import type { Db } from "../db/connection.js";
import { karmaBalances, karmaLedger, type KarmaBalance } from "../db/schema.js";

export async function getBalance(
  db: Db,
  projectId: string,
  contributorId: string,
): Promise<KarmaBalance | null> {
  const [row] = await db
    .select()
    .from(karmaBalances)
    .where(
      and(eq(karmaBalances.projectId, projectId), eq(karmaBalances.contributorId, contributorId)),
    );
  return row ?? null;
}

export async function getProjectBreakdown(
  db: Db,
  projectId: string,
): Promise<KarmaBalance[]> {
  return db
    .select()
    .from(karmaBalances)
    .where(eq(karmaBalances.projectId, projectId))
    .orderBy(desc(karmaBalances.totalKarma));
}

export async function getContributionKarma(
  db: Db,
  contributionId: string,
) {
  return db
    .select()
    .from(karmaLedger)
    .where(eq(karmaLedger.contributionId, contributionId))
    .orderBy(karmaLedger.id);
}

export async function getHistory(
  db: Db,
  projectId: string,
  contributorId: string,
  opts: { limit: number; cursor?: bigint },
) {
  const conditions = [
    eq(karmaLedger.projectId, projectId),
    eq(karmaLedger.contributorId, contributorId),
  ];

  if (opts.cursor) {
    conditions.push(sql`${karmaLedger.id} < ${opts.cursor}`);
  }

  const entries = await db
    .select()
    .from(karmaLedger)
    .where(and(...conditions))
    .orderBy(desc(karmaLedger.id))
    .limit(opts.limit + 1);

  const hasMore = entries.length > opts.limit;
  if (hasMore) entries.pop();

  return {
    entries,
    nextCursor: hasMore ? entries[entries.length - 1]!.id : null,
  };
}

export async function getLeaderboard(
  db: Db,
  projectId: string,
  opts: { limit: number; offset: number },
) {
  return db
    .select()
    .from(karmaBalances)
    .where(eq(karmaBalances.projectId, projectId))
    .orderBy(desc(karmaBalances.totalKarma))
    .limit(opts.limit)
    .offset(opts.offset);
}
