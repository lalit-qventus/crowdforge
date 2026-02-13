import {
  pgTable,
  bigint,
  text,
  uuid,
  numeric,
  timestamp,
  jsonb,
  boolean,
  integer,
  uniqueIndex,
  index,
  primaryKey,
} from "drizzle-orm/pg-core";
import { sql } from "drizzle-orm";

const timestamptz = (name: string) => timestamp(name, { withTimezone: true });

// ---------------------------------------------------------------------------
// karma_ledger — immutable append-only log (source of truth)
// ---------------------------------------------------------------------------
export const karmaLedger = pgTable(
  "karma_ledger",
  {
    id: bigint("id", { mode: "bigint" }).generatedAlwaysAsIdentity().primaryKey(),
    eventType: text("event_type").notNull(),
    projectId: uuid("project_id").notNull(),
    contributorId: uuid("contributor_id").notNull(),
    contributionId: uuid("contribution_id"),
    karmaDelta: numeric("karma_delta", { precision: 12, scale: 4 }).notNull(),
    vestedKarmaDelta: numeric("vested_karma_delta", { precision: 12, scale: 4 }).notNull(),
    unvestedKarmaDelta: numeric("unvested_karma_delta", { precision: 12, scale: 4 }).notNull(),
    formulaInputs: jsonb("formula_inputs").notNull(),
    idempotencyKey: text("idempotency_key").notNull(),
    createdAt: timestamptz("created_at").defaultNow().notNull(),
  },
  (table) => [
    uniqueIndex("karma_ledger_idempotency_key_idx").on(table.idempotencyKey),
    index("karma_ledger_project_contributor_idx").on(table.projectId, table.contributorId),
    index("karma_ledger_contribution_idx").on(table.contributionId),
  ],
);

export type KarmaLedgerEntry = typeof karmaLedger.$inferSelect;
export type NewKarmaLedgerEntry = typeof karmaLedger.$inferInsert;

export const KARMA_EVENT_TYPES = [
  "contribution_accepted",
  "upvote_added",
  "upvote_removed",
  "milestone_1_retroactive",
  "milestone_2_retroactive",
  "revert_penalty",
  "vesting_release",
  "formula_recalc",
] as const;

export type KarmaEventType = (typeof KARMA_EVENT_TYPES)[number];

// ---------------------------------------------------------------------------
// karma_balances — materialized cache, rebuildable from ledger
// ---------------------------------------------------------------------------
export const karmaBalances = pgTable(
  "karma_balances",
  {
    projectId: uuid("project_id").notNull(),
    contributorId: uuid("contributor_id").notNull(),
    totalKarma: numeric("total_karma", { precision: 14, scale: 4 }).notNull().default("0"),
    vestedKarma: numeric("vested_karma", { precision: 14, scale: 4 }).notNull().default("0"),
    unvestedKarma: numeric("unvested_karma", { precision: 14, scale: 4 }).notNull().default("0"),
    lastLedgerId: bigint("last_ledger_id", { mode: "bigint" }).notNull().default(sql`0`),
  },
  (table) => [primaryKey({ columns: [table.projectId, table.contributorId] })],
);

export type KarmaBalance = typeof karmaBalances.$inferSelect;

// ---------------------------------------------------------------------------
// vesting_schedule — tracks unvested karma chunks over 90-day linear vest
// ---------------------------------------------------------------------------
export const vestingSchedule = pgTable(
  "vesting_schedule",
  {
    id: uuid("id").defaultRandom().primaryKey(),
    ledgerEntryId: bigint("ledger_entry_id", { mode: "bigint" }).notNull(),
    projectId: uuid("project_id").notNull(),
    contributorId: uuid("contributor_id").notNull(),
    totalUnvested: numeric("total_unvested", { precision: 12, scale: 4 }).notNull(),
    vestedSoFar: numeric("vested_so_far", { precision: 12, scale: 4 }).notNull().default("0"),
    vestingStartAt: timestamptz("vesting_start_at").notNull(),
    vestingEndAt: timestamptz("vesting_end_at").notNull(),
    fullyVested: boolean("fully_vested").notNull().default(false),
  },
  (table) => [
    index("vesting_schedule_pending_idx")
      .on(table.fullyVested, table.vestingEndAt)
      .where(sql`fully_vested = false`),
    index("vesting_schedule_contributor_idx").on(table.projectId, table.contributorId),
  ],
);

export type VestingScheduleRow = typeof vestingSchedule.$inferSelect;

// ---------------------------------------------------------------------------
// contributor_tiers — cross-project karma aggregation
// ---------------------------------------------------------------------------
export const contributorTiers = pgTable("contributor_tiers", {
  userId: uuid("user_id").primaryKey(),
  cumulativeKarma: numeric("cumulative_karma", { precision: 14, scale: 4 }).notNull().default("0"),
  tier: integer("tier").notNull().default(0),
  tierMultiplier: numeric("tier_multiplier", { precision: 3, scale: 1 }).notNull().default("0"),
  highestTierEver: integer("highest_tier_ever").notNull().default(0),
});

export type ContributorTier = typeof contributorTiers.$inferSelect;

// ---------------------------------------------------------------------------
// tier_thresholds — adjustable thresholds (for annual recalibration)
// ---------------------------------------------------------------------------
export const tierThresholds = pgTable("tier_thresholds", {
  tier: integer("tier").primaryKey(),
  name: text("name").notNull(),
  karmaThreshold: numeric("karma_threshold", { precision: 14, scale: 4 }).notNull(),
  multiplier: numeric("multiplier", { precision: 3, scale: 1 }).notNull(),
});

export type TierThreshold = typeof tierThresholds.$inferSelect;

// ---------------------------------------------------------------------------
// payout_cycles — monthly payout records
// ---------------------------------------------------------------------------
export const payoutCycles = pgTable(
  "payout_cycles",
  {
    id: uuid("id").defaultRandom().primaryKey(),
    projectId: uuid("project_id").notNull(),
    cycleStart: timestamptz("cycle_start").notNull(),
    cycleEnd: timestamptz("cycle_end").notNull(),
    netRevenue: numeric("net_revenue", { precision: 14, scale: 2 }).notNull(),
    contributorPool: numeric("contributor_pool", { precision: 14, scale: 2 }).notNull(),
    platformFee: numeric("platform_fee", { precision: 14, scale: 2 }).notNull(),
    treasuryAllocation: numeric("treasury_allocation", { precision: 14, scale: 2 }).notNull(),
    totalWeightedKarma: numeric("total_weighted_karma", { precision: 18, scale: 4 }).notNull(),
    status: text("status").notNull().default("calculated"),
    createdAt: timestamptz("created_at").defaultNow().notNull(),
  },
  (table) => [index("payout_cycles_project_idx").on(table.projectId, table.cycleEnd)],
);

export type PayoutCycle = typeof payoutCycles.$inferSelect;

// ---------------------------------------------------------------------------
// payout_line_items — per-contributor payout within a cycle
// ---------------------------------------------------------------------------
export const payoutLineItems = pgTable(
  "payout_line_items",
  {
    id: uuid("id").defaultRandom().primaryKey(),
    payoutCycleId: uuid("payout_cycle_id")
      .notNull()
      .references(() => payoutCycles.id),
    contributorId: uuid("contributor_id").notNull(),
    vestedKarma: numeric("vested_karma", { precision: 14, scale: 4 }).notNull(),
    tierMultiplier: numeric("tier_multiplier", { precision: 3, scale: 1 }).notNull(),
    weightedKarma: numeric("weighted_karma", { precision: 18, scale: 4 }).notNull(),
    sharePercent: numeric("share_percent", { precision: 8, scale: 6 }).notNull(),
    grossPayout: numeric("gross_payout", { precision: 14, scale: 2 }).notNull(),
    holdbackAmount: numeric("holdback_amount", { precision: 14, scale: 2 }).notNull(),
    netPayout: numeric("net_payout", { precision: 14, scale: 2 }).notNull(),
    holdbackReleasedAt: timestamptz("holdback_released_at"),
    parentUserId: uuid("parent_user_id"),
    snapshotData: jsonb("snapshot_data").notNull(),
    createdAt: timestamptz("created_at").defaultNow().notNull(),
  },
  (table) => [
    index("payout_line_items_cycle_idx").on(table.payoutCycleId),
    index("payout_line_items_contributor_idx").on(table.contributorId),
  ],
);

export type PayoutLineItem = typeof payoutLineItems.$inferSelect;

// ---------------------------------------------------------------------------
// project_milestones — tracks milestone gate progress
// ---------------------------------------------------------------------------
export const projectMilestones = pgTable("project_milestones", {
  projectId: uuid("project_id").primaryKey(),
  uniqueContributors: integer("unique_contributors").notNull().default(0),
  acceptedCount: integer("accepted_count").notNull().default(0),
  hasRevenue: boolean("has_revenue").notNull().default(false),
  milestone1At: timestamptz("milestone_1_at"),
  milestone2At: timestamptz("milestone_2_at"),
});

export type ProjectMilestone = typeof projectMilestones.$inferSelect;
