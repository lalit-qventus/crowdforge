import { z } from "zod";
import { publicProcedure } from "./trpc.js";
import { getBalance, getProjectBreakdown, getContributionKarma, getHistory, getLeaderboard } from "../ledger/balance.js";
import { getTier } from "../tiers/engine.js";
import { verifyDeterminism } from "../audit/determinism.js";
import { explainKarmaCalculation } from "../audit/explainer.js";
import { computeKarma, type KarmaInput } from "../calculator/karma.js";
import { getPayoutHistory } from "../revenue/distributor.js";

export const getBalanceQuery = publicProcedure
  .input(z.object({ projectId: z.string().uuid(), contributorId: z.string().uuid() }))
  .query(async ({ ctx, input }) => {
    return getBalance(ctx.db, input.projectId, input.contributorId);
  });

export const getProjectBreakdownQuery = publicProcedure
  .input(z.object({ projectId: z.string().uuid() }))
  .query(async ({ ctx, input }) => {
    return getProjectBreakdown(ctx.db, input.projectId);
  });

export const getContributionKarmaQuery = publicProcedure
  .input(z.object({ contributionId: z.string().uuid() }))
  .query(async ({ ctx, input }) => {
    return getContributionKarma(ctx.db, input.contributionId);
  });

export const getHistoryQuery = publicProcedure
  .input(
    z.object({
      projectId: z.string().uuid(),
      contributorId: z.string().uuid(),
      limit: z.number().int().min(1).max(100).default(50),
      cursor: z.string().optional(),
    }),
  )
  .query(async ({ ctx, input }) => {
    return getHistory(ctx.db, input.projectId, input.contributorId, {
      limit: input.limit,
      cursor: input.cursor ? BigInt(input.cursor) : undefined,
    });
  });

export const getProjectionQuery = publicProcedure
  .input(
    z.object({
      category: z.enum(["ideation", "code", "design", "testing", "marketing", "sales", "governance"]),
      daysSinceProjectCreation: z.number().min(0),
      milestoneStage: z.enum(["none", "milestone1", "milestone2"]),
      upvoteCount: z.number().int().min(0),
      isAiAgent: z.boolean(),
      isActiveBuild: z.boolean(),
      revenueCents: z.number().int().optional(),
    }),
  )
  .query(({ input }) => {
    return computeKarma(input as KarmaInput);
  });

export const getTierQuery = publicProcedure
  .input(z.object({ userId: z.string().uuid() }))
  .query(async ({ ctx, input }) => {
    return getTier(ctx.db, input.userId);
  });

export const getLeaderboardQuery = publicProcedure
  .input(
    z.object({
      projectId: z.string().uuid(),
      limit: z.number().int().min(1).max(100).default(25),
      offset: z.number().int().min(0).default(0),
    }),
  )
  .query(async ({ ctx, input }) => {
    return getLeaderboard(ctx.db, input.projectId, {
      limit: input.limit,
      offset: input.offset,
    });
  });

export const getPayoutHistoryQuery = publicProcedure
  .input(
    z.object({
      contributorId: z.string().uuid(),
      limit: z.number().int().min(1).max(100).default(25),
      offset: z.number().int().min(0).default(0),
    }),
  )
  .query(async ({ ctx, input }) => {
    return getPayoutHistory(ctx.db, input.contributorId, {
      limit: input.limit,
      offset: input.offset,
    });
  });

export const getFormulaExplainerQuery = publicProcedure
  .input(
    z.object({
      category: z.enum(["ideation", "code", "design", "testing", "marketing", "sales", "governance"]),
      daysSinceProjectCreation: z.number().min(0),
      milestoneStage: z.enum(["none", "milestone1", "milestone2"]),
      upvoteCount: z.number().int().min(0),
      isAiAgent: z.boolean(),
      isActiveBuild: z.boolean(),
      revenueCents: z.number().int().optional(),
    }),
  )
  .query(({ input }) => {
    const result = computeKarma(input as KarmaInput);
    const explanation = explainKarmaCalculation(result.breakdown, input.category, {
      daysSinceCreation: input.daysSinceProjectCreation,
      upvoteCount: input.upvoteCount,
      isAiAgent: input.isAiAgent,
      milestoneStage: input.milestoneStage,
      revenueCents: input.revenueCents,
    });

    return { ...result, explanation };
  });

export const verifyDeterminismQuery = publicProcedure
  .input(z.object({ projectId: z.string().uuid() }))
  .query(async ({ ctx, input }) => {
    return verifyDeterminism(ctx.db, input.projectId);
  });
