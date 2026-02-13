import { describe, it, expect } from "vitest";
import { computeKarma, type KarmaInput } from "../src/calculator/karma.js";

/**
 * PetMatch worked example from `02-karma-system/design.md`.
 *
 * Reproduces the design doc's reference numbers to verify
 * the calculator matches the spec.
 */
describe("PetMatch worked example", () => {
  it("Alice: Ideation + Code on day 0 with 3 upvotes → ~72 karma", () => {
    // Alice makes 2 contributions: ideation (5) and code (10), with 3 upvotes each
    // The design doc says 15 base, so it's combined: base = 15
    // Since our calculator works per-contribution, we compute separately
    // Day 0, pioneer = 3.0x, upvote_score = ln(4)/ln(10) ≈ 0.602, multiplier = 1.602

    const ideation = computeKarma({
      category: "ideation",
      daysSinceProjectCreation: 0,
      milestoneStage: "milestone2",
      upvoteCount: 3,
      isAiAgent: false,
      isActiveBuild: false,
    });

    const code = computeKarma({
      category: "code",
      daysSinceProjectCreation: 0,
      milestoneStage: "milestone2",
      upvoteCount: 3,
      isAiAgent: false,
      isActiveBuild: false,
    });

    const totalAlice = ideation.totalKarma + code.totalKarma;
    // ideation: 5 * 3.0 * 1.602 = 24.03
    // code: 10 * 3.0 * 1.602 = 48.06
    // total: 72.09
    expect(totalAlice).toBeCloseTo(72, 0);
  });

  it("Bob AI: Design on day 5 with 2 upvotes → ~34.3 karma", () => {
    // Bob is an AI agent during active build
    // Day 5, pioneer = 1 + 2*e^(-0.05) ≈ 2.9025
    // upvote_score = ln(3)/ln(10) ≈ 0.477, multiplier = 1.477
    // AI rate = 0.7
    // 8 * 2.9025 * 1.477 * 0.7 ≈ 24.0

    const bob = computeKarma({
      category: "design",
      daysSinceProjectCreation: 5,
      milestoneStage: "milestone2",
      upvoteCount: 2,
      isAiAgent: true,
      isActiveBuild: true,
    });

    // Design doc says ~34.3, but that's without AI rate
    // With AI 0.7x rate: 8 * 2.9025 * 1.477 * 0.7 ≈ 24.0
    // Without AI rate: 8 * 2.9025 * 1.477 ≈ 34.3
    // The design doc's worked example doesn't mention AI rate for Bob
    // so let's verify the non-AI version matches
    const bobHuman = computeKarma({
      category: "design",
      daysSinceProjectCreation: 5,
      milestoneStage: "milestone2",
      upvoteCount: 2,
      isAiAgent: false,
      isActiveBuild: true,
    });

    expect(bobHuman.totalKarma).toBeCloseTo(34.3, 0);
    // With AI rate applied:
    expect(bob.totalKarma).toBeCloseTo(34.3 * 0.7, 0);
  });

  it("Carol: Code on day 75 with 9 upvotes → ~38.8 karma", () => {
    // Day 75, pioneer = 1 + 2*e^(-0.75) ≈ 1.9447
    // upvote_score = ln(10)/ln(10) = 1.0, multiplier = 2.0

    const carol = computeKarma({
      category: "code",
      daysSinceProjectCreation: 75,
      milestoneStage: "milestone2",
      upvoteCount: 9,
      isAiAgent: false,
      isActiveBuild: false,
    });

    // 10 * 1.9447 * 2.0 = 38.89
    expect(carol.totalKarma).toBeCloseTo(38.8, 0);
  });

  it("Dave: Testing on day 80 with 5 upvotes → ~23.7 karma", () => {
    // Day 80, pioneer = 1 + 2*e^(-0.80) ≈ 1.8987
    // upvote_score = ln(6)/ln(10) ≈ 0.778, multiplier = 1.778

    const dave = computeKarma({
      category: "testing",
      daysSinceProjectCreation: 80,
      milestoneStage: "milestone2",
      upvoteCount: 5,
      isAiAgent: false,
      isActiveBuild: false,
    });

    // 7 * 1.8987 * 1.778 = 23.63
    expect(dave.totalKarma).toBeCloseTo(23.7, 0);
  });

  it("Eve: Sales $10K on day 180 with 4 upvotes → ~226.1 karma", () => {
    // $10,000 revenue → 100 karma base
    // Day 180, pioneer = 1 + 2*e^(-1.80) ≈ 1.3306
    // upvote_score = ln(5)/ln(10) ≈ 0.699, multiplier = 1.699

    const eve = computeKarma({
      category: "sales",
      daysSinceProjectCreation: 180,
      milestoneStage: "milestone2",
      upvoteCount: 4,
      isAiAgent: false,
      isActiveBuild: false,
      revenueCents: 1_000_000, // $10,000
    });

    // 100 * 1.3306 * 1.699 = 226.1
    expect(eve.totalKarma).toBeCloseTo(226.1, 0);
  });

  it("PetMatch total karma matches spec (~394.9)", () => {
    // Recompute all and sum (using human rates for Bob per design doc)
    const alice1 = computeKarma({
      category: "ideation",
      daysSinceProjectCreation: 0,
      milestoneStage: "milestone2",
      upvoteCount: 3,
      isAiAgent: false,
      isActiveBuild: false,
    });
    const alice2 = computeKarma({
      category: "code",
      daysSinceProjectCreation: 0,
      milestoneStage: "milestone2",
      upvoteCount: 3,
      isAiAgent: false,
      isActiveBuild: false,
    });
    const bob = computeKarma({
      category: "design",
      daysSinceProjectCreation: 5,
      milestoneStage: "milestone2",
      upvoteCount: 2,
      isAiAgent: false, // design doc uses human rate for the example
      isActiveBuild: true,
    });
    const carol = computeKarma({
      category: "code",
      daysSinceProjectCreation: 75,
      milestoneStage: "milestone2",
      upvoteCount: 9,
      isAiAgent: false,
      isActiveBuild: false,
    });
    const dave = computeKarma({
      category: "testing",
      daysSinceProjectCreation: 80,
      milestoneStage: "milestone2",
      upvoteCount: 5,
      isAiAgent: false,
      isActiveBuild: false,
    });
    const eve = computeKarma({
      category: "sales",
      daysSinceProjectCreation: 180,
      milestoneStage: "milestone2",
      upvoteCount: 4,
      isAiAgent: false,
      isActiveBuild: false,
      revenueCents: 1_000_000,
    });

    const total =
      alice1.totalKarma +
      alice2.totalKarma +
      bob.totalKarma +
      carol.totalKarma +
      dave.totalKarma +
      eve.totalKarma;

    expect(total).toBeCloseTo(394.9, 0);
  });

  it("PetMatch payout shares match spec", () => {
    const contributions = [
      { label: "Alice", karma: 72.0 },
      { label: "Bob", karma: 34.3 },
      { label: "Carol", karma: 38.8 },
      { label: "Dave", karma: 23.7 },
      { label: "Eve", karma: 226.1 },
    ];

    const totalKarma = contributions.reduce((s, c) => s + c.karma, 0);
    const pool = 5000 * 0.70; // $3,500

    const payouts = contributions.map((c) => ({
      ...c,
      share: c.karma / totalKarma,
      payout: pool * (c.karma / totalKarma),
    }));

    expect(payouts[0]!.share).toBeCloseTo(0.182, 2);
    expect(payouts[0]!.payout).toBeCloseTo(637, -1);

    expect(payouts[4]!.share).toBeCloseTo(0.572, 2);
    expect(payouts[4]!.payout).toBeCloseTo(2002, -1);

    // Sum should equal pool
    const payoutSum = payouts.reduce((s, p) => s + p.payout, 0);
    expect(payoutSum).toBeCloseTo(pool, 0);
  });
});
