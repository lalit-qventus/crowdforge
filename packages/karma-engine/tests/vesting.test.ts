import { describe, it, expect } from "vitest";
import { VESTING_IMMEDIATE_FRACTION, VESTING_DURATION_DAYS } from "../src/calculator/constants.js";

describe("vesting math", () => {
  // The vesting logic runs in the DB-backed release cron,
  // but the math is verified here against design spec expectations.

  function vestingPercent(day: number): number {
    const immediate = VESTING_IMMEDIATE_FRACTION; // 0.25
    const remaining = 1 - immediate; // 0.75
    const fraction = Math.min(day / VESTING_DURATION_DAYS, 1);
    return immediate + remaining * fraction;
  }

  it("25% vested at day 0", () => {
    expect(vestingPercent(0)).toBeCloseTo(0.25, 4);
  });

  it("50% vested at day 30", () => {
    // 0.25 + 0.75 * (30/90) = 0.25 + 0.25 = 0.50
    expect(vestingPercent(30)).toBeCloseTo(0.50, 4);
  });

  it("62.5% vested at day 45", () => {
    // 0.25 + 0.75 * (45/90) = 0.25 + 0.375 = 0.625
    expect(vestingPercent(45)).toBeCloseTo(0.625, 4);
  });

  it("75% vested at day 60", () => {
    expect(vestingPercent(60)).toBeCloseTo(0.75, 4);
  });

  it("100% vested at day 90", () => {
    expect(vestingPercent(90)).toBeCloseTo(1.0, 4);
  });

  it("still 100% after day 90", () => {
    expect(vestingPercent(120)).toBeCloseTo(1.0, 4);
    expect(vestingPercent(365)).toBeCloseTo(1.0, 4);
  });

  it("daily vesting rate is ~0.83% of total", () => {
    // 75% over 90 days = 0.8333...% per day
    const dailyRate = (1 - VESTING_IMMEDIATE_FRACTION) / VESTING_DURATION_DAYS;
    expect(dailyRate).toBeCloseTo(0.00833, 4);
  });
});
