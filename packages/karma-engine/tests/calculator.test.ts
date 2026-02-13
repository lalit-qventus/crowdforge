import { describe, it, expect } from "vitest";
import { computeKarma, computeUpvoteDelta, computeRevertPenalty, type KarmaInput } from "../src/calculator/karma.js";
import { rawPioneerMultiplier, effectivePioneerMultiplier } from "../src/calculator/pioneer.js";
import { upvoteScore } from "../src/calculator/upvote.js";
import { REVERT_PENALTY_MULTIPLIER } from "../src/calculator/constants.js";

// --- Pioneer Multiplier ---

describe("rawPioneerMultiplier", () => {
  it("returns 3.0x on day 0", () => {
    expect(rawPioneerMultiplier(0)).toBeCloseTo(3.0, 4);
  });

  it("returns ~2.48x on day 30", () => {
    expect(rawPioneerMultiplier(30)).toBeCloseTo(2.4824, 2);
  });

  it("returns ~1.81x on day 90", () => {
    expect(rawPioneerMultiplier(90)).toBeCloseTo(1.8131, 2);
  });

  it("returns ~1.33x on day 180", () => {
    expect(rawPioneerMultiplier(180)).toBeCloseTo(1.3306, 2);
  });

  it("returns ~1.05x on day 365", () => {
    expect(rawPioneerMultiplier(365)).toBeCloseTo(1.0506, 2);
  });

  it("converges toward 1.0 for very large t", () => {
    expect(rawPioneerMultiplier(730)).toBeCloseTo(1.0, 1);
  });
});

describe("effectivePioneerMultiplier", () => {
  it("returns 1.0x when milestone stage is none (bonus fraction = 0)", () => {
    expect(effectivePioneerMultiplier(0, "none")).toBe(1);
    expect(effectivePioneerMultiplier(30, "none")).toBe(1);
  });

  it("applies 50% of bonus at milestone1", () => {
    // Day 0: raw = 3.0, bonus = 2.0, 50% of bonus = 1.0, effective = 2.0
    expect(effectivePioneerMultiplier(0, "milestone1")).toBeCloseTo(2.0, 4);
  });

  it("applies 100% of bonus at milestone2", () => {
    // Day 0: raw = 3.0, effective = 3.0
    expect(effectivePioneerMultiplier(0, "milestone2")).toBeCloseTo(3.0, 4);
  });
});

// --- Upvote Score ---

describe("upvoteScore", () => {
  it("returns 0 for 0 upvotes", () => {
    expect(upvoteScore(0)).toBe(0);
  });

  it("returns ~0.30 for 1 upvote", () => {
    expect(upvoteScore(1)).toBeCloseTo(0.3010, 2);
  });

  it("returns ~0.60 for 3 upvotes", () => {
    expect(upvoteScore(3)).toBeCloseTo(0.6021, 2);
  });

  it("returns ~1.0 for 9 upvotes", () => {
    expect(upvoteScore(9)).toBeCloseTo(1.0, 2);
  });

  it("returns ~1.49 for 30 upvotes", () => {
    expect(upvoteScore(30)).toBeCloseTo(1.4914, 2);
  });

  it("returns ~2.0 for 99 upvotes", () => {
    expect(upvoteScore(99)).toBeCloseTo(2.0, 2);
  });
});

// --- Karma Computation ---

describe("computeKarma", () => {
  it("produces deterministic output for identical inputs", () => {
    const input: KarmaInput = {
      category: "code",
      daysSinceProjectCreation: 30,
      milestoneStage: "milestone2",
      upvoteCount: 5,
      isAiAgent: false,
      isActiveBuild: false,
    };

    const r1 = computeKarma(input);
    const r2 = computeKarma(input);
    expect(r1.totalKarma).toBe(r2.totalKarma);
    expect(r1.vestedKarma).toBe(r2.vestedKarma);
    expect(r1.unvestedKarma).toBe(r2.unvestedKarma);
    expect(r1.breakdown).toEqual(r2.breakdown);
  });

  it("computes code contribution with pioneer and upvotes", () => {
    const result = computeKarma({
      category: "code",
      daysSinceProjectCreation: 0,
      milestoneStage: "milestone2",
      upvoteCount: 9,
      isAiAgent: false,
      isActiveBuild: false,
    });

    // base=10, pioneer=3.0, upvote_score=1.0, multiplier=2.0
    // total = 10 * 3.0 * 2.0 = 60
    expect(result.totalKarma).toBeCloseTo(60, 1);
    expect(result.vestedKarma).toBeCloseTo(15, 1); // 25%
    expect(result.unvestedKarma).toBeCloseTo(45, 1); // 75%
  });

  it("applies AI agent rate during active build", () => {
    const human = computeKarma({
      category: "code",
      daysSinceProjectCreation: 30,
      milestoneStage: "milestone2",
      upvoteCount: 0,
      isAiAgent: false,
      isActiveBuild: true,
    });
    const ai = computeKarma({
      category: "code",
      daysSinceProjectCreation: 30,
      milestoneStage: "milestone2",
      upvoteCount: 0,
      isAiAgent: true,
      isActiveBuild: true,
    });

    expect(ai.totalKarma).toBeCloseTo(human.totalKarma * 0.7, 2);
  });

  it("AI agents get 1.0x rate outside active build", () => {
    const human = computeKarma({
      category: "code",
      daysSinceProjectCreation: 180,
      milestoneStage: "milestone2",
      upvoteCount: 0,
      isAiAgent: false,
      isActiveBuild: false,
    });
    const ai = computeKarma({
      category: "code",
      daysSinceProjectCreation: 180,
      milestoneStage: "milestone2",
      upvoteCount: 0,
      isAiAgent: true,
      isActiveBuild: false,
    });

    expect(ai.totalKarma).toBeCloseTo(human.totalKarma, 4);
  });

  it("handles zero upvotes (multiplier = 1.0)", () => {
    const result = computeKarma({
      category: "code",
      daysSinceProjectCreation: 365,
      milestoneStage: "milestone2",
      upvoteCount: 0,
      isAiAgent: false,
      isActiveBuild: false,
    });

    // base=10, pioneer≈1.05, upvote multiplier=1.0
    expect(result.breakdown.upvoteMultiplier).toBeCloseTo(1.0, 4);
    expect(result.totalKarma).toBeCloseTo(10 * 1.0506 * 1.0, 1);
  });

  it("computes sales karma from revenue", () => {
    const result = computeKarma({
      category: "sales",
      daysSinceProjectCreation: 0,
      milestoneStage: "milestone2",
      upvoteCount: 0,
      isAiAgent: false,
      isActiveBuild: false,
      revenueCents: 1000000, // $10,000
    });

    // base = $10,000 * 0.01 = 100, pioneer=3.0, upvote=1.0
    expect(result.breakdown.baseKarma).toBe(100);
    expect(result.totalKarma).toBeCloseTo(300, 1);
  });

  it("returns 0 for sales with no revenue", () => {
    const result = computeKarma({
      category: "sales",
      daysSinceProjectCreation: 0,
      milestoneStage: "milestone2",
      upvoteCount: 5,
      isAiAgent: false,
      isActiveBuild: false,
    });
    expect(result.totalKarma).toBe(0);
  });

  it("handles each category base value", () => {
    const categories = [
      { cat: "ideation" as const, base: 5 },
      { cat: "code" as const, base: 10 },
      { cat: "design" as const, base: 8 },
      { cat: "testing" as const, base: 7 },
      { cat: "marketing" as const, base: 6 },
      { cat: "governance" as const, base: 4 },
    ];

    for (const { cat, base } of categories) {
      const result = computeKarma({
        category: cat,
        daysSinceProjectCreation: 365,
        milestoneStage: "milestone2",
        upvoteCount: 0,
        isAiAgent: false,
        isActiveBuild: false,
      });
      expect(result.breakdown.baseKarma).toBe(base);
    }
  });

  it("vesting split is 25/75", () => {
    const result = computeKarma({
      category: "code",
      daysSinceProjectCreation: 100,
      milestoneStage: "milestone2",
      upvoteCount: 3,
      isAiAgent: false,
      isActiveBuild: false,
    });

    expect(result.vestedKarma).toBeCloseTo(result.totalKarma * 0.25, 8);
    expect(result.unvestedKarma).toBeCloseTo(result.totalKarma * 0.75, 8);
    expect(result.vestedKarma + result.unvestedKarma).toBeCloseTo(result.totalKarma, 8);
  });
});

// --- Upvote Delta ---

describe("computeUpvoteDelta", () => {
  it("returns positive delta when upvotes increase", () => {
    const input: KarmaInput = {
      category: "code",
      daysSinceProjectCreation: 30,
      milestoneStage: "milestone2",
      upvoteCount: 5,
      isAiAgent: false,
      isActiveBuild: false,
    };

    const previousTotal = computeKarma({ ...input, upvoteCount: 3 }).totalKarma;
    const result = computeUpvoteDelta(input, previousTotal);

    expect(result.delta).toBeGreaterThan(0);
  });

  it("returns negative delta when upvotes decrease", () => {
    const input: KarmaInput = {
      category: "code",
      daysSinceProjectCreation: 30,
      milestoneStage: "milestone2",
      upvoteCount: 3,
      isAiAgent: false,
      isActiveBuild: false,
    };

    const previousTotal = computeKarma({ ...input, upvoteCount: 5 }).totalKarma;
    const result = computeUpvoteDelta(input, previousTotal);

    expect(result.delta).toBeLessThan(0);
  });
});

// --- Revert Penalty ---

describe("computeRevertPenalty", () => {
  it("applies 120% penalty", () => {
    const result = computeRevertPenalty(100);
    expect(result.penaltyKarma).toBe(-120);
    expect(result.breakdown.penaltyMultiplier).toBe(REVERT_PENALTY_MULTIPLIER);
  });

  it("returns negative karma value", () => {
    const result = computeRevertPenalty(50);
    expect(result.penaltyKarma).toBeLessThan(0);
    expect(Math.abs(result.penaltyKarma)).toBe(60);
  });

  it("handles zero total gracefully", () => {
    const result = computeRevertPenalty(0);
    expect(result.penaltyKarma).toBe(0);
  });
});
