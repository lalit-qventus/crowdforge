import { describe, it, expect } from "vitest";
import { computeTierFromKarma } from "../src/tiers/thresholds.js";
import { TIER_SEEDS } from "../src/db/seed.js";

const thresholds = TIER_SEEDS.map((s) => ({
  tier: s.tier,
  name: s.name,
  karmaThreshold: s.karmaThreshold,
  multiplier: s.multiplier,
}));

describe("computeTierFromKarma", () => {
  it("returns Observer (tier 0) for 0 karma", () => {
    const result = computeTierFromKarma(0, thresholds);
    expect(result.tier).toBe(0);
    expect(result.multiplier).toBe(0);
  });

  it("returns Observer for 49 karma (below Contributor threshold)", () => {
    const result = computeTierFromKarma(49, thresholds);
    expect(result.tier).toBe(0);
  });

  it("returns Contributor (tier 1) at exactly 50 karma", () => {
    const result = computeTierFromKarma(50, thresholds);
    expect(result.tier).toBe(1);
    expect(result.multiplier).toBe(0.5);
  });

  it("returns Builder (tier 2) at 250 karma", () => {
    const result = computeTierFromKarma(250, thresholds);
    expect(result.tier).toBe(2);
    expect(result.multiplier).toBe(1.0);
  });

  it("returns Architect (tier 3) at 1000 karma", () => {
    const result = computeTierFromKarma(1000, thresholds);
    expect(result.tier).toBe(3);
    expect(result.multiplier).toBe(1.5);
  });

  it("returns Partner (tier 4) at 5000 karma", () => {
    const result = computeTierFromKarma(5000, thresholds);
    expect(result.tier).toBe(4);
    expect(result.multiplier).toBe(2.0);
  });

  it("returns Founder's Circle (tier 5) at 25000 karma", () => {
    const result = computeTierFromKarma(25000, thresholds);
    expect(result.tier).toBe(5);
    expect(result.multiplier).toBe(2.5);
  });

  it("handles values between tiers", () => {
    const result = computeTierFromKarma(500, thresholds);
    expect(result.tier).toBe(2); // Builder (250+), not Architect (1000+)
  });

  it("handles very large values", () => {
    const result = computeTierFromKarma(1_000_000, thresholds);
    expect(result.tier).toBe(5);
    expect(result.multiplier).toBe(2.5);
  });
});
