import { describe, it, expect } from "vitest";
import { REVENUE_SPLIT, HOLDBACK_FRACTION, MIN_PAYOUT_SHARE } from "../src/calculator/constants.js";

describe("revenue distribution math", () => {
  it("revenue split sums to 100%", () => {
    const total = REVENUE_SPLIT.contributors + REVENUE_SPLIT.platform + REVENUE_SPLIT.treasury;
    expect(total).toBe(1.0);
  });

  it("100% of revenue goes to karma-weighted contributors", () => {
    const revenue = 10000;
    expect(revenue * REVENUE_SPLIT.contributors).toBe(10000);
  });

  it("platform takes zero commission", () => {
    expect(REVENUE_SPLIT.platform).toBe(0);
  });

  it("no separate treasury allocation", () => {
    expect(REVENUE_SPLIT.treasury).toBe(0);
  });

  it("holdback is 20%", () => {
    expect(HOLDBACK_FRACTION).toBe(0.20);
  });

  it("weighted payout calculation", () => {
    // Simulate: 3 contributors with different karma and tiers
    // Platform is also a contributor with earned karma
    const contributors = [
      { vested: 100, multiplier: 1.0 }, // Builder
      { vested: 200, multiplier: 1.5 }, // Architect
      { vested: 50, multiplier: 0.5 },  // Contributor
      { vested: 30, multiplier: 1.0 },  // Platform (earned via infra karma)
    ];

    const weighted = contributors.map((c) => c.vested * c.multiplier);
    // 100, 300, 25, 30
    const totalWeighted = weighted.reduce((s, w) => s + w, 0); // 455

    const pool = 10000; // 100% to contributors
    const payouts = weighted.map((w) => pool * (w / totalWeighted));

    // Verify sum equals pool
    const payoutSum = payouts.reduce((s, p) => s + p, 0);
    expect(payoutSum).toBeCloseTo(pool, 2);

    // Verify proportions
    expect(payouts[0]!).toBeCloseTo(pool * (100 / 455), 2);
    expect(payouts[1]!).toBeCloseTo(pool * (300 / 455), 2);
    expect(payouts[2]!).toBeCloseTo(pool * (25 / 455), 2);
    expect(payouts[3]!).toBeCloseTo(pool * (30 / 455), 2);
  });

  it("holdback calculation", () => {
    const grossPayout = 1000;
    const holdback = grossPayout * HOLDBACK_FRACTION;
    const net = grossPayout - holdback;
    expect(holdback).toBe(200);
    expect(net).toBe(800);
  });

  it("minimum payout share threshold", () => {
    expect(MIN_PAYOUT_SHARE).toBe(0.001); // 0.1%
  });
});
