-- Immutability enforcement: REVOKE UPDATE/DELETE on karma_ledger from application role.
-- Replace 'app_role' with the actual Supabase/application role name.
-- REVOKE UPDATE, DELETE ON karma_ledger FROM app_role;

-- Seed tier thresholds
INSERT INTO tier_thresholds (tier, name, karma_threshold, multiplier) VALUES
  (0, 'Observer', 0, 0.0),
  (1, 'Contributor', 50, 0.5),
  (2, 'Builder', 250, 1.0),
  (3, 'Architect', 1000, 1.5),
  (4, 'Partner', 5000, 2.0),
  (5, 'Founder''s Circle', 25000, 2.5)
ON CONFLICT (tier) DO NOTHING;
