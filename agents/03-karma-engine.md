# Agent: Karma Engine

## Mission
Implement CrowdForge's karma computation system — the financial backbone of the platform. Karma determines revenue share. Every calculation must be deterministic, auditable, and transparent. Contributors must be able to see exactly why they have the karma they have.

## The Karma Model

### Per-Project Scope
Karma is scoped to each project. Revenue share = `contributor_karma / total_project_karma`. Cross-project reputation exists for profiles but is never used for payouts.

### Contribution Categories and Base Karma
| Category | Base | Notes |
|---|---|---|
| Code | 10 | |
| Design | 8 | |
| Testing/QA | 7 | |
| Marketing | 6 | |
| Ideation | 5 | |
| Governance | 4 | |
| Sales | 1 per $100 collected | Outcome-based |

### Pioneer Multiplier
`multiplier = 1 + 2.0 * e^(-0.01 * days_since_project_creation)`
- Day 0: 3.0x, Day 90: 1.81x, Day 365: 1.05x
- Applied at contribution submission time, but karma only awarded on acceptance (deferred attribution)
- Milestone-gated: full multiplier only applies when project hits milestones (10 accepted contributions from 5+ unique contributors, or first revenue)

### Upvote Score
`upvote_score = ln(1 + upvote_count) / ln(10)`
- Human-only upvotes. AI cannot vote.
- No downvotes.

### Full Formula
`contribution_karma = base_karma * pioneer_multiplier * (1 + upvote_score)`

### Karma-to-Revenue: The Tier System
Karma is NOT a direct cash conversion. It determines your dividend tier:
| Tier | Dividend Multiplier |
|---|---|
| Observer (0 karma) | 0x |
| Contributor | 0.5x |
| Builder | 1.0x |
| Architect | 1.5x |
| Master | 2.0x |
| Inner Circle | 2.5x |

Effective revenue share = `(contributor_karma * tier_multiplier) / sum(all_contributor_karma * their_tier_multipliers)`

### No Decay
Karma does not decay. Natural dilution handles "rest and vest" — new contributions grow the total pool.

### Revert Penalty
Reverted contributions lose 120% of earned karma. Net negative.

### AI Agent Karma
- AI agents earn at 0.7x during Active Build, 1.0x during Growth/Mature
- Cannot vote. Payouts go to deploying human/org.
- Max 3 agents per human.

## What to Build
1. Karma ledger — immutable append-only log of every karma event
2. Karma calculator — recomputes project karma distribution on demand
3. Tier engine — determines contributor tier based on cross-project karma
4. Revenue distributor — calculates payout per contributor per project per cycle
5. Karma API — endpoints for querying karma breakdown, projections, history
6. Audit trail — every karma event traceable to its source contribution and formula inputs

## Reference Docs
- `../docs/karma-system/design.md` — complete design with worked examples
- `../docs/value-pricing/analysis.md` — tier system rationale, behavioral economics
- `../docs/spawn-protection/design.md` — milestone-gated multiplier details

## Constraints
- Deterministic: same inputs must produce same outputs, always
- Auditable: contributors can query exactly how their karma was calculated
- Parameters are tunable per-project within platform bounds (see parameter table in karma doc)
- Payout minimum: 0.1% of project karma to receive payout in a cycle
