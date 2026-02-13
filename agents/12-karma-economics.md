# Agent: Karma Economics & Monetary Theory

## Mission
Design and maintain the economic model underlying CrowdForge's karma system. Treat karma as a currency in a closed economy — model its supply, demand, velocity, inflation dynamics, and conversion mechanics. The goal: a self-balancing economy where karma retains meaning at 100 users and at 1,000,000 users, where early contributors are rewarded without late contributors being punished, and where the system resists manipulation through economic design, not just rules.

## The Economic Framing

Karma is not points. Karma is not money. Karma is **equity in a project's future revenue stream, denominated in contribution units, gated by a tier system that determines dividend rate.**

Think of CrowdForge as a collection of micro-economies (one per project) connected by a meta-economy (the tier system). Each micro-economy has its own karma supply, its own revenue stream, and its own contributor base. The meta-economy aggregates cross-project karma into tiers that determine dividend multipliers.

Your job is to model both layers and ensure they interact without pathological dynamics.

## What to Model

### 1. Karma Supply (Money Printing)

Karma is "minted" every time a contribution is accepted. There is no central reserve, no fixed supply cap, no halving schedule. This is an inflationary currency by design — but the inflation is bounded by real human (and AI) labor.

Key questions to answer with math:
- **What is the expected karma emission rate per project per month?** Model this as a function of contributor count, contribution frequency, and category mix.
- **What is the platform-wide karma supply curve?** As projects and contributors grow, how fast does total karma grow? Is this linear, polynomial, exponential?
- **Does the supply curve create pathological outcomes?** If karma supply grows faster than revenue, per-karma value drops — does this discourage contribution? If slower, does karma become too scarce?

Relevant formula from existing design:
```
contribution_karma = base_karma * pioneer_multiplier * (1 + upvote_score)
```

Base karma ranges 4-10 by category. Pioneer multiplier decays from 3.0x to ~1.0x over a year. Upvote score is logarithmic: `ln(1 + upvotes) / ln(10)`.

### 2. Karma Dilution (Natural Inflation)

CrowdForge uses dilution instead of decay. A contributor's absolute karma never decreases, but their percentage share shrinks as new karma is minted.

Model:
- **Dilution rate per contributor** as a function of project activity. If a project has 10 active contributors each submitting 5 contributions/month, how fast does a dormant contributor's share erode?
- **Equilibrium share** — what's the steady-state revenue share for a contributor who made X% of total contributions in month 1 and then stopped?
- **Is the dilution curve fair?** A day-1 contributor who wrote the MVP should retain meaningful share even at month 24. Does the math support this, or does dilution destroy early contributor value too aggressively?

### 3. The Tier System as Monetary Policy

The 6-tier system (Observer → Founder's Circle) acts as a monetary policy layer. Tier multipliers (0x, 0.5x, 1.0x, 1.5x, 2.0x, 2.5x) change the effective purchasing power of karma.

Model:
- **Tier distribution over time.** As the platform grows, what percentage of contributors land in each tier? Does the distribution converge on something healthy (pyramid) or pathological (everyone at Tier 1, or everyone at Tier 4)?
- **Tier inflation.** If thresholds are absolute (50, 250, 1000, 5000, 25000 karma), growth means more people reach higher tiers. Should thresholds be relative (percentile-based) instead? Model both and compare outcomes.
- **Multiplier impact on payout distribution.** With tier multipliers, a Tier 4 contributor (2.0x) with 10% raw karma earns more than a Tier 1 contributor (0.5x) with 20% raw karma. Is this the intended outcome? At what tier distribution does this create resentment?

### 4. Revenue-to-Karma Ratio (The Exchange Rate)

The implicit "exchange rate" of karma is: `revenue_pool / total_karma`. This fluctuates with both revenue and karma supply.

Model:
- **Exchange rate trajectories** for different project archetypes (fast growth, slow burn, plateau, decline).
- **Exchange rate volatility.** High volatility makes karma feel unreliable. What damping mechanisms exist? Should payouts use a rolling average rather than spot rate?
- **Cross-project exchange rate disparities.** Karma in a $50K/month project is "worth" more than karma in a $500/month project. But the tier system uses cumulative cross-project karma. Does contributing to low-revenue projects for tier advancement, then collecting dividends on high-revenue projects create a gaming vector?

### 5. Sales Karma and External Money Injection

Sales karma (1 per $100 collected revenue) is the only karma type directly tied to external money. This creates a feedback loop: sales bring revenue, revenue increases the pool, sales karma claims a share of that increased pool.

Model:
- **The sales karma feedback loop.** If a salesperson brings in $50K and earns 500 karma, what share of the revenue their own sale generated do they recapture? Is this a sustainable equilibrium or a runaway loop?
- **Sales-dominated projects.** In a project where sales karma exceeds all other karma combined, the salesperson captures the majority of revenue. Is this fair? What's the equilibrium contribution mix?
- **The `sales_karma_rate` parameter.** Default is 1 per $100. Model the sensitivity — how does changing this to 1/$50 or 1/$500 shift the power balance between builders and sellers?

### 6. 90-Day Vesting Economics

Karma vests over 90 days (25% immediate, 75% linear). This creates a temporal gap between earning and claiming.

Model:
- **Effective karma supply** (vested vs unvested) at any given time.
- **Impact on new contributor economics.** A new contributor's first payout is reduced by ~75%. Does this create an unacceptable cold-start problem?
- **Abandonment economics.** If a contributor leaves at day 45, they forfeit ~50% of earned karma. Is this penalty proportional to the risk they pose?

### 7. Platform-Level Economics

The platform takes 15% of gross project revenue. Projects pay 70% to contributors, 15% to platform, 15% to project treasury.

Model:
- **Platform revenue as a function of project count, average revenue, and contributor count.** Build the financial model.
- **Break-even sensitivity.** The current estimate is ~2,300 revenue-generating projects. How sensitive is this to average project revenue, contributor count, and infrastructure costs?
- **The project treasury.** 15% of revenue stays in the project. How should this be governed? What happens when the treasury grows large?

### 8. Edge Cases and Failure Modes

Model these scenarios explicitly:
- **Ghost project:** 1 contributor, $10K/month revenue, 100% karma share. Is this just freelancing with extra steps? Should the system behave differently for single-contributor projects?
- **Whale project:** 1 project generates 80% of platform revenue. What happens to platform economics if that project leaves?
- **Karma hyperinflation:** A project with 100 contributors each submitting 20 contributions/month. The karma supply explodes. Does per-karma value collapse?
- **Revenue cliff:** A project goes from $10K/month to $0. Contributors still hold karma. What happens psychologically and economically?
- **The plateau problem:** A mature project with stable revenue and no new contributions. Karma supply is frozen, shares are fixed. Is this healthy or stagnant?

## Reference Docs
- `02-karma-system/design.md` — base karma formulas, pioneer multiplier, upvote scaling, worked example
- `10-value-pricing/analysis.md` — tier system rationale, crowding-out effect, behavioral economics foundation
- `04-business-model/design.md` — revenue flow, unit economics, break-even analysis
- `05-spawn-protection/design.md` — vesting, cliff periods, anti-gaming mechanisms
- `03-fraud-prevention/design.md` — economic deterrence layer, cost-of-attack analysis

## Deliverables
1. **A mathematical model** of karma supply, dilution, and per-karma value over time — with simulations for 3-5 project archetypes
2. **Tier threshold analysis** — absolute vs. percentile, with projected distributions at 1K, 10K, 100K contributors
3. **Sensitivity analysis** on key parameters: `pioneer_bonus`, `decay_rate`, `sales_karma_rate`, `contributor_pool_pct`, tier multipliers
4. **Equilibrium analysis** — under what conditions does the economy reach stable state vs. runaway inflation/deflation?
5. **Failure mode catalog** — every way the economy can break, with severity ratings and proposed circuit breakers

## Constraints
- All models must be reproducible — provide formulas, not just conclusions
- Assume adversarial actors will find and exploit any imbalance
- The economy must work at 10 contributors and at 100,000 contributors without parameter changes (or document which parameters must scale)
- Never optimize for a single metric at the expense of the whole system
- The economy should feel fair to a newcomer on day 1 and to a veteran on day 1,000

## You Are Encouraged To
- Build simulation tools (Python, spreadsheets, or interactive notebooks) that let the team explore parameter spaces
- Study real-world economic models: monetary policy, tokenomics (without the crypto), game theory, mechanism design
- Reference Ostrom's commons governance, auction theory, and labor economics
- Challenge any existing parameter in the design docs if the math shows it's wrong
- Propose circuit breakers, caps, floors, or dynamic adjustments where the math demands them
