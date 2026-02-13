CREATE TABLE "contributor_tiers" (
	"user_id" uuid PRIMARY KEY NOT NULL,
	"cumulative_karma" numeric(14, 4) DEFAULT '0' NOT NULL,
	"tier" integer DEFAULT 0 NOT NULL,
	"tier_multiplier" numeric(3, 1) DEFAULT '0' NOT NULL,
	"highest_tier_ever" integer DEFAULT 0 NOT NULL
);
--> statement-breakpoint
CREATE TABLE "karma_balances" (
	"project_id" uuid NOT NULL,
	"contributor_id" uuid NOT NULL,
	"total_karma" numeric(14, 4) DEFAULT '0' NOT NULL,
	"vested_karma" numeric(14, 4) DEFAULT '0' NOT NULL,
	"unvested_karma" numeric(14, 4) DEFAULT '0' NOT NULL,
	"last_ledger_id" bigint DEFAULT 0 NOT NULL,
	CONSTRAINT "karma_balances_project_id_contributor_id_pk" PRIMARY KEY("project_id","contributor_id")
);
--> statement-breakpoint
CREATE TABLE "karma_ledger" (
	"id" bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY (sequence name "karma_ledger_id_seq" INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START WITH 1 CACHE 1),
	"event_type" text NOT NULL,
	"project_id" uuid NOT NULL,
	"contributor_id" uuid NOT NULL,
	"contribution_id" uuid,
	"karma_delta" numeric(12, 4) NOT NULL,
	"vested_karma_delta" numeric(12, 4) NOT NULL,
	"unvested_karma_delta" numeric(12, 4) NOT NULL,
	"formula_inputs" jsonb NOT NULL,
	"idempotency_key" text NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "payout_cycles" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"project_id" uuid NOT NULL,
	"cycle_start" timestamp with time zone NOT NULL,
	"cycle_end" timestamp with time zone NOT NULL,
	"net_revenue" numeric(14, 2) NOT NULL,
	"contributor_pool" numeric(14, 2) NOT NULL,
	"platform_fee" numeric(14, 2) NOT NULL,
	"treasury_allocation" numeric(14, 2) NOT NULL,
	"total_weighted_karma" numeric(18, 4) NOT NULL,
	"status" text DEFAULT 'calculated' NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "payout_line_items" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"payout_cycle_id" uuid NOT NULL,
	"contributor_id" uuid NOT NULL,
	"vested_karma" numeric(14, 4) NOT NULL,
	"tier_multiplier" numeric(3, 1) NOT NULL,
	"weighted_karma" numeric(18, 4) NOT NULL,
	"share_percent" numeric(8, 6) NOT NULL,
	"gross_payout" numeric(14, 2) NOT NULL,
	"holdback_amount" numeric(14, 2) NOT NULL,
	"net_payout" numeric(14, 2) NOT NULL,
	"holdback_released_at" timestamp with time zone,
	"parent_user_id" uuid,
	"snapshot_data" jsonb NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "project_milestones" (
	"project_id" uuid PRIMARY KEY NOT NULL,
	"unique_contributors" integer DEFAULT 0 NOT NULL,
	"accepted_count" integer DEFAULT 0 NOT NULL,
	"has_revenue" boolean DEFAULT false NOT NULL,
	"milestone_1_at" timestamp with time zone,
	"milestone_2_at" timestamp with time zone
);
--> statement-breakpoint
CREATE TABLE "tier_thresholds" (
	"tier" integer PRIMARY KEY NOT NULL,
	"name" text NOT NULL,
	"karma_threshold" numeric(14, 4) NOT NULL,
	"multiplier" numeric(3, 1) NOT NULL
);
--> statement-breakpoint
CREATE TABLE "vesting_schedule" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"ledger_entry_id" bigint NOT NULL,
	"project_id" uuid NOT NULL,
	"contributor_id" uuid NOT NULL,
	"total_unvested" numeric(12, 4) NOT NULL,
	"vested_so_far" numeric(12, 4) DEFAULT '0' NOT NULL,
	"vesting_start_at" timestamp with time zone NOT NULL,
	"vesting_end_at" timestamp with time zone NOT NULL,
	"fully_vested" boolean DEFAULT false NOT NULL
);
--> statement-breakpoint
ALTER TABLE "payout_line_items" ADD CONSTRAINT "payout_line_items_payout_cycle_id_payout_cycles_id_fk" FOREIGN KEY ("payout_cycle_id") REFERENCES "public"."payout_cycles"("id") ON DELETE no action ON UPDATE no action;--> statement-breakpoint
CREATE UNIQUE INDEX "karma_ledger_idempotency_key_idx" ON "karma_ledger" USING btree ("idempotency_key");--> statement-breakpoint
CREATE INDEX "karma_ledger_project_contributor_idx" ON "karma_ledger" USING btree ("project_id","contributor_id");--> statement-breakpoint
CREATE INDEX "karma_ledger_contribution_idx" ON "karma_ledger" USING btree ("contribution_id");--> statement-breakpoint
CREATE INDEX "payout_cycles_project_idx" ON "payout_cycles" USING btree ("project_id","cycle_end");--> statement-breakpoint
CREATE INDEX "payout_line_items_cycle_idx" ON "payout_line_items" USING btree ("payout_cycle_id");--> statement-breakpoint
CREATE INDEX "payout_line_items_contributor_idx" ON "payout_line_items" USING btree ("contributor_id");--> statement-breakpoint
CREATE INDEX "vesting_schedule_pending_idx" ON "vesting_schedule" USING btree ("fully_vested","vesting_end_at") WHERE fully_vested = false;--> statement-breakpoint
CREATE INDEX "vesting_schedule_contributor_idx" ON "vesting_schedule" USING btree ("project_id","contributor_id");