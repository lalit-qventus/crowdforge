import { eq, and, sql } from "drizzle-orm";
import type { Db } from "../db/connection.js";
import { projectMilestones, karmaLedger, karmaBalances } from "../db/schema.js";
import {
  MILESTONE_1_ACCEPTED_COUNT,
  MILESTONE_1_UNIQUE_CONTRIBUTORS,
  MILESTONE_2_ACCEPTED_COUNT,
  VESTING_IMMEDIATE_FRACTION,
} from "../calculator/constants.js";
import { effectivePioneerMultiplier } from "../calculator/pioneer.js";
import { appendLedgerBatch, type LedgerEntryInput } from "./append.js";

export type MilestoneEvent = "milestone_1" | "milestone_2" | null;

/**
 * Update milestone counters and check if a milestone was just achieved.
 */
export async function updateMilestoneProgress(
  db: Db,
  projectId: string,
  contributorId: string,
  hasRevenue: boolean,
): Promise<MilestoneEvent> {
  // Upsert milestone record
  await db
    .insert(projectMilestones)
    .values({
      projectId,
      uniqueContributors: 1,
      acceptedCount: 1,
      hasRevenue,
    })
    .onConflictDoUpdate({
      target: projectMilestones.projectId,
      set: {
        acceptedCount: sql`${projectMilestones.acceptedCount} + 1`,
        hasRevenue: hasRevenue ? true : sql`${projectMilestones.hasRevenue}`,
        // unique_contributors needs special handling
      },
    });

  // Count unique contributors (do this separately for accuracy)
  const [uniqueCount] = await db.execute(sql`
    SELECT COUNT(DISTINCT contributor_id) AS cnt
    FROM karma_ledger
    WHERE project_id = ${projectId}
      AND event_type = 'contribution_accepted'
  `);
  const uniqueContributors = Number((uniqueCount as any).cnt);

  await db
    .update(projectMilestones)
    .set({ uniqueContributors })
    .where(eq(projectMilestones.projectId, projectId));

  // Fetch current milestone state
  const [milestone] = await db
    .select()
    .from(projectMilestones)
    .where(eq(projectMilestones.projectId, projectId));

  if (!milestone) return null;

  // Check milestone 1: 10 accepted from 5+ unique contributors
  if (
    !milestone.milestone1At &&
    milestone.acceptedCount >= MILESTONE_1_ACCEPTED_COUNT &&
    milestone.uniqueContributors >= MILESTONE_1_UNIQUE_CONTRIBUTORS
  ) {
    await db
      .update(projectMilestones)
      .set({ milestone1At: new Date() })
      .where(eq(projectMilestones.projectId, projectId));
    return "milestone_1";
  }

  // Check milestone 2: first revenue OR 50 accepted contributions
  if (
    milestone.milestone1At &&
    !milestone.milestone2At &&
    (milestone.hasRevenue || milestone.acceptedCount >= MILESTONE_2_ACCEPTED_COUNT)
  ) {
    await db
      .update(projectMilestones)
      .set({ milestone2At: new Date() })
      .where(eq(projectMilestones.projectId, projectId));
    return "milestone_2";
  }

  return null;
}

/**
 * Apply retroactive pioneer bonus for all prior contributions when a milestone is reached.
 *
 * When milestone_1 is hit: contributions go from fraction=0 → fraction=0.5
 * When milestone_2 is hit: contributions go from fraction=0.5 → fraction=1.0
 *
 * The delta is the difference in karma that each prior contribution should have earned.
 */
export async function applyMilestoneRetroactive(
  db: Db,
  projectId: string,
  milestoneEvent: "milestone_1" | "milestone_2",
): Promise<number> {
  // Fetch all contribution_accepted entries for the project
  const priorEntries = await db
    .select()
    .from(karmaLedger)
    .where(
      and(
        eq(karmaLedger.projectId, projectId),
        eq(karmaLedger.eventType, "contribution_accepted"),
      ),
    );

  const batchEntries: LedgerEntryInput[] = [];

  for (const entry of priorEntries) {
    const inputs = entry.formulaInputs as Record<string, any>;
    const daysSinceCreation = inputs.daysSinceProjectCreation as number;
    const previousStage = milestoneEvent === "milestone_1" ? "none" : "milestone1";
    const newStage = milestoneEvent === "milestone_1" ? "milestone1" : "milestone2";

    const oldPioneer = effectivePioneerMultiplier(daysSinceCreation, previousStage as any);
    const newPioneer = effectivePioneerMultiplier(daysSinceCreation, newStage as any);

    if (Math.abs(newPioneer - oldPioneer) < 0.0001) continue;

    // Recalculate with new pioneer, compute delta
    const baseKarma = inputs.baseKarma as number;
    const upvoteMultiplier = inputs.upvoteMultiplier as number;
    const aiRate = inputs.aiRate as number;

    const oldTotal = baseKarma * oldPioneer * upvoteMultiplier * aiRate;
    const newTotal = baseKarma * newPioneer * upvoteMultiplier * aiRate;
    const delta = newTotal - oldTotal;

    if (Math.abs(delta) < 0.0001) continue;

    const vestedDelta = delta * VESTING_IMMEDIATE_FRACTION;
    const unvestedDelta = delta - vestedDelta;

    const eventType = milestoneEvent === "milestone_1"
      ? "milestone_1_retroactive"
      : "milestone_2_retroactive";

    batchEntries.push({
      eventType: eventType as any,
      projectId,
      contributorId: entry.contributorId,
      contributionId: entry.contributionId,
      karmaDelta: delta.toFixed(4),
      vestedKarmaDelta: vestedDelta.toFixed(4),
      unvestedKarmaDelta: unvestedDelta.toFixed(4),
      formulaInputs: {
        milestoneEvent,
        originalLedgerEntryId: Number(entry.id),
        oldPioneerMultiplier: oldPioneer,
        newPioneerMultiplier: newPioneer,
        delta,
      },
      idempotencyKey: `${eventType}:${entry.id}`,
    });
  }

  if (batchEntries.length === 0) return 0;

  const ids = await appendLedgerBatch(db, batchEntries);
  return ids.length;
}

/**
 * Get the current milestone stage for a project.
 */
export async function getMilestoneStage(
  db: Db,
  projectId: string,
): Promise<"none" | "milestone1" | "milestone2"> {
  const [row] = await db
    .select()
    .from(projectMilestones)
    .where(eq(projectMilestones.projectId, projectId));

  if (!row) return "none";
  if (row.milestone2At) return "milestone2";
  if (row.milestone1At) return "milestone1";
  return "none";
}
