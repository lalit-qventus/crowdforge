# Agent: Backend & API

## Mission
Build CrowdForge's core backend — the services that power projects, contributions, task management, user accounts, and the karma engine. The backend is the foundation everything else builds on. It must be correct, fast, and auditable. Every karma calculation, every contribution record, every vote is immutable history.

## Core Services
1. **Auth Service** — registration, login, OAuth (GitHub, Google), identity verification score tracking, graduated trust levels (Observer through Inner Circle)
2. **Project Service** — lifecycle management (Proposal → Incubation → Active Build → Shipped → Earning → Sunset), project settings, founder controls
3. **Contribution Service** — submit, review, accept/reject, revert. Git-backed. Every contribution is a PR. Deferred karma attribution (karma awarded on acceptance, not submission)
4. **Task Service** — create tasks, claim (48hr expiry, max 3 active), release, complete. Task categories (Code, Design, Content, Marketing, Research, Ops)
5. **Karma Service** — see dedicated agent `03-karma-engine.md`
6. **Voting Service** — Idea Ring voting (72hr window, 25-vote quorum, 60% threshold), contribution upvoting (human-only, logarithmic scaling)
7. **Feed/Activity Service** — event publishing for real-time consumption, activity history per project and globally

## Tech Stack
- Node.js + tRPC or GraphQL
- PostgreSQL via Supabase
- Redis (Upstash) for caching, pub/sub, rate limiting
- Meilisearch for full-text search
- Git (bare repos or GitHub API) for contribution version control

## Data Model Priorities
- Users (with identity score, trust level, AI agent flag)
- Projects (with lifecycle stage, settings, founder)
- Contributions (with status, karma awarded, reviewer, timestamps)
- Tasks (with assignee, claim expiry, status, category)
- Votes (with voter, target, weight, timestamp)
- Karma ledger (immutable log of every karma event per project)

## Reference Docs
- `../docs/architecture/design.md` — system architecture, service diagram, tech choices
- `../docs/karma-system/design.md` — karma formulas and rules
- `../docs/fraud-prevention/design.md` — trust levels, rate limits, behavioral signals
- `../docs/spawn-protection/design.md` — project lifecycle phases, contribution rules per phase

## Constraints
- All karma calculations must be deterministic and auditable
- Never delete data — soft delete only. Contribution history is immutable.
- API must support both human clients and AI agent clients
- Rate limiting by trust level (see fraud prevention doc)

## You Are Encouraged To
- Spawn sub-agents for individual services
- Build the data model and migrations first, then services on top
- Create an API spec/contract before implementing
