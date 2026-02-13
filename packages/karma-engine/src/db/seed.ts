import { createDb } from "./connection.js";
import { tierThresholds } from "./schema.js";

const TIER_SEEDS = [
  { tier: 0, name: "Observer", karmaThreshold: "0", multiplier: "0.0" },
  { tier: 1, name: "Contributor", karmaThreshold: "50", multiplier: "0.5" },
  { tier: 2, name: "Builder", karmaThreshold: "250", multiplier: "1.0" },
  { tier: 3, name: "Architect", karmaThreshold: "1000", multiplier: "1.5" },
  { tier: 4, name: "Partner", karmaThreshold: "5000", multiplier: "2.0" },
  { tier: 5, name: "Founder's Circle", karmaThreshold: "25000", multiplier: "2.5" },
] as const;

export { TIER_SEEDS };

export async function seedTierThresholds(db: ReturnType<typeof createDb>) {
  await db
    .insert(tierThresholds)
    .values([...TIER_SEEDS])
    .onConflictDoNothing();
}

// CLI entrypoint
if (process.argv[1]?.endsWith("seed.ts")) {
  const db = createDb(process.env.DATABASE_URL!);
  await seedTierThresholds(db);
  console.log("Seeded tier thresholds");
  process.exit(0);
}
