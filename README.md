# crowdforge

Collaborative platform where contributors earn karma through accepted work and share in project revenue.

## Folder Structure

```
crowdforge/
├── docs/                    # Design documents
│   ├── vision.md            # Platform vision and principles
│   ├── karma-system/        # Karma formulas, economics model
│   ├── architecture/        # System architecture, tech stack, UX flows
│   ├── spawn-protection/    # Project lifecycle phases, milestone gating
│   ├── fraud-prevention/    # Trust levels, rate limiting
│   ├── business-model/      # Revenue model (COGS-based)
│   ├── value-pricing/       # Tier system, dividend multipliers, vesting
│   ├── payments-revenue/    # Stripe Connect, payout design
│   ├── deploy-pipeline/     # CI/CD, hosting infrastructure
│   ├── platform-governance/ # Community governance, moderation
│   ├── growth-community/    # Growth mechanics, community building
│   ├── go-to-market/        # Launch strategy
│   ├── brand/               # Brand guidelines, copy kit
│   ├── moat-defensibility/  # Competitive analysis
│   └── research/            # Stack Overflow, Wikipedia research
├── agents/                  # Agent team briefs (12 teams)
│   ├── 01-frontend-ui.md
│   ├── 02-backend-api.md
│   ├── 03-karma-engine.md
│   └── ...
├── frontend/                # Static frontend prototype
│   ├── index.html           # Landing page
│   ├── intelligence.html    # Analytics page
│   ├── pages/               # Dashboard, Forge, Idea Ring, Profile, Project, Stream
│   └── styles/              # Design system CSS
├── backend/                 # Django API (Python)
│   ├── apps/
│   │   ├── accounts/        # User registration, profiles, identity verification
│   │   ├── projects/        # Project CRUD, lifecycle, settings
│   │   ├── contributions/   # Submit, review, accept/reject contributions
│   │   ├── tasks/           # Task creation, claiming, expiry management
│   │   ├── karma/           # Karma ledger, formulas, balance queries
│   │   ├── voting/          # Idea Ring voting (72h window, quorum)
│   │   ├── activity/        # Activity feed events
│   │   └── search/          # Full-text search via Meilisearch
│   ├── core/                # Constants, events, exceptions, middleware, permissions
│   ├── crowdforge/          # Django settings, URL routing, ASGI/WSGI
│   └── pyproject.toml       # Python dependencies (uv)
└── packages/
    └── karma-engine/        # Karma computation system
        ├── src/
        │   ├── calculator/  # Pure functions — karma formula, pioneer multiplier, upvote score
        │   ├── ledger/      # Append-only ledger, balance cache, milestone retroactive
        │   ├── tiers/       # Cross-project tier aggregation with ratchet guarantee
        │   ├── vesting/     # 25% immediate + 90-day linear vesting
        │   ├── revenue/     # Monthly payout calculation (70/15/15 split)
        │   ├── audit/       # Determinism verification, formula explainer
        │   ├── api/         # tRPC router (10 queries, 8 mutations)
        │   └── db/          # Drizzle schema, migrations, seed data
        └── tests/           # 64 tests — calculator, tiers, vesting, revenue, PetMatch example
```
