import { describe, it, expect } from "vitest";
import { computeKarma } from "../src/calculator/karma.js";
import { explainKarmaCalculation } from "../src/audit/explainer.js";

describe("explainKarmaCalculation", () => {
  it("produces readable breakdown for code contribution", () => {
    const result = computeKarma({
      category: "code",
      daysSinceProjectCreation: 30,
      milestoneStage: "milestone2",
      upvoteCount: 5,
      isAiAgent: false,
      isActiveBuild: false,
    });

    const lines = explainKarmaCalculation(result.breakdown, "code", {
      daysSinceCreation: 30,
      upvoteCount: 5,
      isAiAgent: false,
      milestoneStage: "milestone2",
    });

    expect(lines.length).toBeGreaterThanOrEqual(3);
    expect(lines[0]).toContain("Base karma: 10");
    expect(lines[1]).toContain("Pioneer multiplier");
    expect(lines[2]).toContain("Upvote bonus");
    expect(lines.at(-1)).toContain("Total");
  });

  it("includes AI rate line for AI agents", () => {
    const result = computeKarma({
      category: "code",
      daysSinceProjectCreation: 10,
      milestoneStage: "milestone1",
      upvoteCount: 0,
      isAiAgent: true,
      isActiveBuild: true,
    });

    const lines = explainKarmaCalculation(result.breakdown, "code", {
      daysSinceCreation: 10,
      upvoteCount: 0,
      isAiAgent: true,
      milestoneStage: "milestone1",
    });

    expect(lines.some((l) => l.includes("AI agent rate"))).toBe(true);
  });

  it("explains sales karma with revenue", () => {
    const result = computeKarma({
      category: "sales",
      daysSinceProjectCreation: 100,
      milestoneStage: "milestone2",
      upvoteCount: 0,
      isAiAgent: false,
      isActiveBuild: false,
      revenueCents: 50000,
    });

    const lines = explainKarmaCalculation(result.breakdown, "sales", {
      daysSinceCreation: 100,
      upvoteCount: 0,
      isAiAgent: false,
      milestoneStage: "milestone2",
      revenueCents: 50000,
    });

    expect(lines[0]).toContain("$500.00 revenue");
  });
});
