# Karma System Design

CrowdForge's karma system answers one question: **what fraction of this Scene's value did you create?**

Karma is per-Scene, non-transferable, and converts directly to revenue share. It is a financial instrument, not a vanity metric. Every formula is public, every calculation is auditable. This document specifies the complete system: what earns karma, how it is weighted, how it converts to money, and how it resists gaming.

---

## Prior Art and What We Took From Each

Five systems informed this design. Each solves a piece of the problem; none solves the whole thing.

### Slicing Pie (Mike Moyer)

Slicing Pie normalizes all contributions -- time, money, ideas, relationships -- into "slices" using risk multipliers (2x for non-cash, 4x for cash). A person's equity share equals their slices divided by total slices. The split is dynamic and recalculates continuously until the company reaches a "freeze event" (breakeven or funding round).

**What we borrowed:** The core insight that equity should be proportional to at-risk contribution, and that the split must be dynamic -- recalculating as new contributions arrive. CrowdForge's `revenue_share = your_karma / total_karma` is a direct descendant of Slicing Pie's formula.

**What we rejected:** Slicing Pie uses fixed multipliers per contribution type (2x for time, 4x for cash). This assumes all hours are equally valuable and all cash equally risky. CrowdForge replaces fixed multipliers with peer review -- humans decide what's valuable, not a formula. Slicing Pie also freezes at breakeven; CrowdForge never freezes because Scenes are living products that keep evolving.

### SourceCred

SourceCred builds a contribution graph -- nodes are contributions and contributors, edges are connections between them -- and runs a modified PageRank algorithm to compute "Cred" scores. Cred flows through the graph like water: contributions that are referenced by other high-Cred contributions accumulate more Cred. A separate token called "Grain" is distributed proportional to Cred.

The key insight is that a contribution's importance is validated by future contributions that build on it. If Alice writes a function that ten other contributors import, Alice's function accumulates Cred from all of them.

**What we borrowed:** The principle that contribution value is determined by downstream impact, not just effort. CrowdForge's upvote system is a simplified version of this -- instead of automatically tracing code dependencies, we let humans signal "this contribution mattered" through explicit votes.

**What we rejected:** SourceCred's PageRank approach is mathematically elegant but opaque. Contributors cannot intuitively understand why their Cred score is what it is. The algorithm is also vulnerable to Cred-farming through circular dependencies. CrowdForge prioritizes legibility over sophistication -- every contributor should be able to trace their karma number back to specific contributions and votes.

### Coordinape

Coordinape runs in epochs (typically monthly). Each member receives 100 GIVE tokens and distributes them to other members based on perceived contribution. At the end of the epoch, each member's share of the compensation budget equals their share of received GIVE tokens.

**What we borrowed:** The peer-allocation principle -- humans are better than algorithms at assessing the value of creative work. CrowdForge's upvote system is a simplified version of Coordinape's GIVE mechanism, where votes signal "this Riff mattered."

**What we rejected:** Coordinape's full peer-allocation model requires every member to evaluate every other member. This works for small DAOs (10-30 people) but breaks down at Scene scale (potentially hundreds of ensemble members). It also creates a "popularity contest" dynamic where socially connected members receive more GIVE regardless of contribution quality. CrowdForge uses upvotes on specific Riffs instead of holistic person-to-person allocation, which scales better and ties karma to identifiable work.

### Colony.io

Colony assigns reputation based on completed tasks within domains. Reputation is non-transferable and decays over time (halving every ~600,000 blocks). Tasks are rated by managers (Unsatisfactory/Satisfactory/Excellent), and reputation is awarded proportionally. Reputation determines governance voting power within specific domains.

**What we borrowed:** Domain-specific reputation (karma is per-Scene, not global), non-transferability, and the principle that reputation should reflect recent contribution patterns.

**What we rejected:** Colony's reputation decay -- halving periodically -- punishes contributors who contributed during high-risk periods and then moved on. If Alice built the MVP and the Scene succeeds, her karma shouldn't evaporate because she stopped contributing. CrowdForge uses dilution instead of decay: new contributions grow the total pool, naturally reducing Alice's percentage share without retroactively reducing her karma. Colony's manager-rated task model also reintroduces hierarchy, which conflicts with CrowdForge's ensemble philosophy.

### Gitcoin (Quadratic Funding)

Gitcoin uses quadratic funding to distribute matching pools: the match amount is proportional to the square of the sum of square roots of individual contributions. This means breadth of support matters more than depth -- 100 people donating $1 each generates a larger match than 1 person donating $100.

**What we borrowed:** The insight that the number of people who value something is a stronger signal than the intensity of any individual's valuation. CrowdForge's logarithmic upvote scaling achieves a similar effect: the first few votes on a Riff matter most, and pile-on votes have diminishing returns. This prevents a single popular contribution from dominating the karma pool.

**What we rejected:** Quadratic funding is designed for public goods allocation, not revenue sharing. It also requires a separate matching pool, which doesn't map to CrowdForge's model. Gitcoin's Sybil resistance relies heavily on identity stamps (Gitcoin Passport), which CrowdForge adapts but extends with behavioral detection and vesting mechanics.

---

## What Earns Karma

Every contribution (Riff) to a CrowdForge Scene falls into one of seven categories. Each has a base karma value reflecting the typical effort and impact of that contribution type.

| Category | Examples | Base Karma | Rationale |
|---|---|---|---|
| **Code** | Features, bug fixes, infrastructure, CI/CD, refactoring | 10 | Code ships product. Highest default weight because without it, there is nothing to sell. |
| **Design** | UI/UX mockups, user flows, branding, design systems | 8 | Design directly shapes user experience and conversion. Underweighted in most developer-centric systems. |
| **Testing/QA** | Test suites, bug reports with repro steps, security audits | 7 | Catching a critical bug before launch can save the Scene. Chronically undervalued elsewhere. |
| **Marketing** | Content, social media, community building, launch campaigns | 6 | Important but harder to attribute directly to revenue without metrics. |
| **Ideation** | Problem statements, feature proposals, pivot suggestions | 5 | Ideas are cheap; execution matters more. But a great idea that reshapes the Scene is invaluable -- peer review handles the exceptional cases. |
| **Governance** | Dispute resolution, roadmap decisions, process improvements | 4 | Necessary glue work. Lower base because it is less directly value-creating, but upvotes can elevate it significantly. |
| **Sales** | Closing deals, partnerships, revenue-generating activities | Variable | Outcome-based, not effort-based. See the Sales Karma section below. |

**Why base karma varies by category:** A flat rate would mean an idea sketch earns the same as a shipped feature. That creates perverse incentives -- people would gravitate toward the lowest-effort category. Base weights provide a reasonable prior; peer review adjusts from there. A brilliant idea that reshapes the Scene will get heavily upvoted and can exceed the karma of routine code contributions.

---

## The Pioneer Multiplier

### The Problem

Early contributors take on more risk. When a Scene is just a pitch card, contributing code is a bet -- most Scenes will fail. Late contributors join when product-market fit exists, revenue is flowing, and risk is low. Without time-weighting, rational actors would wait for proof before contributing, creating a free-rider problem that kills Scenes in the cradle.

But time-weighting creates its own problem: if the multiplier is too aggressive, it penalizes the salesperson who joins at month 6 and brings in $50K of revenue. The system must reward both pioneers and late-stage value creators.

### The Formula

```
pioneer_multiplier = 1 + (pioneer_bonus * e^(-decay_rate * t))
```

Where:
- `t` = days since Scene creation
- `pioneer_bonus` = 2.0 (configurable per-Scene, range 1.0-3.0)
- `decay_rate` = 0.01 (configurable per-Scene, range 0.005-0.05)

This produces:

| Day | Multiplier | Interpretation |
|---|---|---|
| 0 | 3.0x | Day-zero contributions are worth triple |
| 30 | 2.48x | First month: still significant premium |
| 90 | 1.81x | Three months: bonus is meaningful but fading |
| 180 | 1.33x | Six months: modest bonus remains |
| 365 | 1.05x | One year: bonus is nearly gone |

**Why exponential decay, not linear:** Linear decay creates a cliff where the bonus abruptly hits zero. Exponential decay is asymptotic -- the bonus gracefully approaches 1.0x without creating a discontinuity. Contributors should never feel a binary "I missed the window" moment.

**The late-value safety valve:** The pioneer multiplier applies to all contributions, including late ones (a contributor joining at day 180 still gets 1.33x). But more importantly, Sales karma (see below) operates on absolute revenue numbers that dwarf any time-weighting penalty. A $50K sale at day 300 generates 500 karma at 1.05x = 525 karma, which is a significant share of most Scenes' total pools regardless of the diminished multiplier.

---

## Peer Review: The Human Upvote

### Mechanic

After a Riff is submitted and accepted, ensemble members can upvote it. Only humans can upvote -- AI agents cannot vote on any Riff (including other AI agents' work or human work).

Each upvote applies a multiplier to the base karma:

```
contribution_karma = base_karma * pioneer_multiplier * (1 + upvote_score)

upvote_score = ln(1 + upvote_count) / ln(10)
```

This logarithmic scaling means:

| Upvotes | Score | Effective Multiplier |
|---|---|---|
| 0 | 0.00 | 1.00x |
| 1 | 0.30 | 1.30x |
| 3 | 0.60 | 1.60x |
| 9 | 1.00 | 2.00x |
| 30 | 1.49 | 2.49x |
| 99 | 2.00 | 3.00x |

### Why Logarithmic

Linear upvote scaling creates a popularity contest where viral contributions dominate regardless of actual value. Logarithmic scaling means the first few upvotes matter most (validation that the contribution has value) while pile-on votes have diminishing effect. This mirrors how Stack Overflow's top answers don't earn proportionally more reputation than moderately upvoted ones.

### Zero-Upvote Contributions

A Riff with zero upvotes still earns its base karma multiplied by the pioneer multiplier. Requiring upvotes to earn anything would create a bottleneck where all karma flows through voter attention, disadvantaging contributions in less visible areas (infrastructure, testing, documentation).

### No Downvotes

There are no downvotes. The absence of an upvote is signal enough. Downvotes in karma-to-revenue systems create adversarial dynamics where contributors are incentivized to suppress competitors' karma. If a Riff is harmful, it should be flagged for governance review, not silently downvoted.

### Pioneer Multiplier Gate

To prevent 3x rewards on trivial unvalidated contributions, the pioneer multiplier only applies to Riffs that have received at least one upvote. Zero-upvote Riffs earn base karma at 1.0x regardless of when they were submitted. This prevents gaming where someone submits a whitespace fix on day zero and collects 3x karma for it.

---

## The Complete Karma Formula

Putting it all together, the karma earned by a single Riff:

```
K = B * M(t) * (1 + U(v))
```

Where:
- `B` = base karma for the Riff's category
- `M(t)` = pioneer multiplier at time `t` (1.0x if zero upvotes)
- `U(v)` = upvote score = ln(1 + v) / ln(10)

A contributor's total Scene karma:

```
K_total = sum of K for all accepted Riffs by that contributor
```

A contributor's revenue share:

```
revenue_share = K_total / S
```

Where `S` = sum of all contributors' karma in the Scene.

Monthly payout:

```
payout = scene_revenue * revenue_share
```

100% of Scene revenue flows to karma-weighted ensemble members. The platform takes zero commission, earns zero karma on Scenes, and does not participate in revenue sharing.

---

## Sales and Outcome-Based Karma

### Why Sales Is Different

Most contribution types are effort-based: you write code, you earn karma. Sales is outcome-based. A salesperson who spends 100 hours and closes zero deals created less Scene value than one who spends 10 hours and closes a $50K contract.

### Formula

```
sales_karma = collected_revenue * sales_karma_rate
```

Where `sales_karma_rate` defaults to **1 karma per $100 of collected revenue** (configurable per-Scene, range 1/$50 to 1/$500).

Sales karma is then subject to the same pioneer multiplier and upvote mechanics as other Riffs.

Key: sales karma is based on **collected** revenue, not contracted revenue. If a customer churns after one month, only one month of revenue converts to karma. This prevents gaming through unsustainable discounts or phantom contracts.

### Attribution

Revenue attribution follows "last touch" by default -- whoever closed the deal gets credit. Scenes can opt into multi-touch attribution through governance decisions, but the default is simple and unambiguous.

### Why This Resolves the Early-vs-Late Tension

A late contributor who brings in $50K of collected revenue earns 500 karma. Even at a diminished pioneer multiplier of 1.05x at day 365, that yields 525 karma -- a significant fraction of most Scenes' total pool. The absolute value of measurable revenue dominates any time-weighting penalty.

Compare: an early contributor who wrote the MVP (200 hours of Code at 10 base karma, 3.0x pioneer, average 1.5x peer review = 9,000 karma) has more karma -- appropriately so, since without the MVP there is nothing to sell. But the salesperson's 525 karma out of, say, 15,000 total still yields 3.5% revenue share. On $50K/month revenue that is $1,750/month for joining late.

If sales karma ever exceeds 50% of total Scene karma, the excess is capped but still counts toward the contributor's profile-level karma and tier advancement. This prevents one massive sale from dominating the entire Scene's revenue distribution.

---

## AI Agent Karma

### How AI Agents Earn Karma

AI agents participate as contributors, not as voters. They earn karma through the same formula as humans -- base karma for their contribution category, subject to pioneer multiplier and human upvotes.

An AI agent that writes code earns Code karma (base 10). An AI agent that generates design mockups earns Design karma (base 8). An AI agent that runs automated test suites earns Testing karma (base 7).

### What AI Agents Cannot Do

- **Cannot upvote.** Only humans validate contribution quality. This prevents a swarm of AI agents from upvoting each other's mediocre contributions into high karma.
- **Cannot participate in governance votes.** Governance decisions require human judgment.
- **Cannot receive direct payouts.** Payouts go to the human or organization that deployed the agent.

### Rate Limits

AI contributions are rate-limited by the deploying human's trust tier to prevent contribution spam. Maximum 3 AI agents per human account. AI agents are excluded from the Seed phase of a Scene (the initial 48-hour curation period is human-only). During Active Build, AI Riffs receive a 0.7x karma discount to account for the lower marginal cost of AI-generated contributions.

### Why "Humans Validate, AI Executes"

The human bottleneck on voting is a feature, not a bug. It ensures that every karma point with a peer-review multiplier has been seen and approved by a human. AI contributions that sit in a "pending validation" state still earn base karma -- the upvote multiplier is a bonus, not a requirement. This keeps the system functional even when human reviewers are scarce.

---

## Karma Dilution (Instead of Decay)

### Position: No Automatic Decay on Earned Karma

This is a deliberate choice. Many DAO systems (Colony, SourceCred) decay reputation over time. CrowdForge does not.

**Arguments for decay:**
- Prevents "rest and vest" -- contribute early, coast forever
- Keeps the karma distribution dynamic
- Reflects that old code may be replaced or deprecated

**Arguments against decay (our position):**
- Karma converts to revenue share. Decaying karma means someone's revenue share shrinks over time even though their historical contribution was real. This feels like retroactively reneging on a deal.
- Early contributions already get diluted over time because new Riffs grow the total pool. If Alice earned 100 karma and the Scene's total grows from 200 to 2,000, her share dropped from 50% to 5% organically.
- Decay punishes people who contributed during high-risk periods and then moved on -- exactly the people you want to reward.

### How Dilution Works

```
revenue_share(contributor) = contributor_karma / total_scene_karma
```

As new Riffs are accepted, total Scene karma grows, and each existing contributor's percentage share naturally decreases unless they keep contributing. This achieves the "stay engaged" incentive without the unfairness of retroactive karma reduction.

A contributor who earned 100 karma on day 1 and never returned:
- Day 1: 100/100 = 100% share
- Day 30: 100/500 = 20% share
- Day 180: 100/5,000 = 2% share

Their Riff is still valued at 100 karma. The Scene just grew beyond it.

### Contribution Velocity Floor (Anti-Rest-and-Vest)

One edge case dilution alone does not solve: a contributor who holds a dominant karma position (say 60% of the pool) and goes completely dormant. If new contributions slow down (remaining ensemble members are demoralized by the whale's dominance), dilution stalls and the whale retains their share indefinitely while doing nothing.

Solution: if a contributor earns zero new karma for 6 consecutive months, their payout share is gradually reduced (10% per month) until they resume contributing or reach a floor of 50% of their entitled share. Their karma is not destroyed -- only their payout eligibility is reduced. Resuming any contribution resets the clock immediately.

This is soft decay that applies only to fully inactive contributors. Anyone maintaining even minimal activity is unaffected.

---

## Vesting

### Schedule

Karma vests on a **25% immediate + 75% linear over 90 days** schedule. When a Riff is accepted:

- 25% of the karma is immediately vested and counts toward revenue share
- The remaining 75% vests linearly over 90 days

| Day After Acceptance | Vested % |
|---|---|
| 0 | 25% |
| 30 | 50% |
| 60 | 75% |
| 90+ | 100% |

### Why This Schedule

- **Immediate 25% vesting** gives new contributors a tangible first payout. A 30-day cliff (where the first month is entirely unpaid) creates a "first month is free labor" perception that kills onboarding.
- **90-day full vest** is long enough to deter hit-and-run contributions. A contributor who submits a Riff and disappears at day 30 forfeits 50% of their karma.
- Fraud prevention goals are achieved through graduated trust levels (identity score, account age, participation thresholds) rather than vesting cliffs.

### Forfeited Karma

When a contributor leaves before fully vesting, their unvested karma is **burned** (removed from the total pool), not redistributed. Redistribution would create an incentive to push out contributors mid-vest. Burning keeps the math clean and prevents gaming.

---

## Karma-to-Revenue Conversion

### Payout Mechanics

- **Frequency:** Monthly. Weekly is too noisy (revenue fluctuates). Quarterly is too slow (contributors want to see returns).
- **Revenue pool:** 100% of Scene revenue. Zero platform commission. Zero platform karma participation.
- **Rolling average:** Payouts use a 3-month trailing average of revenue to smooth volatility. `payout_month = revenue_share * (R_t + R_{t-1} + R_{t-2}) / 3`
- **Minimum threshold:** Contributors must hold at least 0.1% of Scene karma to receive a payout in a given cycle. Below this, karma accumulates. If 6 months of accumulated share exceeds $25, a lump payout is triggered.

### Exchange Rate

The per-karma value of a Scene fluctuates with revenue:

```
exchange_rate = monthly_revenue / total_scene_karma
```

This rate rises when revenue grows faster than karma emission, and falls when karma emission outpaces revenue. The system self-corrects: when per-karma value drops, marginal contributors leave, karma emission slows, and the rate stabilizes. When per-karma value rises, new contributors arrive, karma emission increases, and the rate stabilizes.

---

## Cross-Scene Reputation (Profile Karma)

Karma is per-Scene for revenue purposes, but CrowdForge also maintains a profile-level reputation for discovery and trust:

```
profile_karma = sum(scene_karma * scene_success_weight)
```

Where `scene_success_weight` ranges from 0.1 (failed/inactive Scene) to 1.0 (actively generating revenue). This prevents someone from farming karma on dead Scenes and appearing credible.

Profile karma is never used for revenue distribution. It determines:
- Karma tier (Observer through Inner Circle)
- Visibility to Scene founders deciding who to invite
- Trust level for fraud prevention gates
- Social standing on the platform

### Karma Tiers

Six tiers based on cumulative profile karma:

| Tier | Name | Threshold | Multiplier |
|---|---|---|---|
| 0 | Observer | 0 | 0 (no multiplier) |
| 1 | Contributor | 50 | 0.7x |
| 2 | Builder | 250 | 1.0x |
| 3 | Architect | 1,000 | 1.3x |
| 4 | Partner | 5,000 | 1.7x |
| 5 | Inner Circle | 25,000 | 2.2x |

The tier multiplier adjusts a contributor's effective karma within a Scene:

```
effective_karma = scene_karma * tier_multiplier
weighted_share = effective_karma / sum(all effective_karma in Scene)
```

**Spread analysis:** Inner Circle earns 3.14x what a Contributor earns for the same raw Scene karma. This is aggressive enough to drive tier aspiration but moderate enough that tier cannot trump a large raw-karma deficit. A Contributor with 3x more Scene karma than an Inner Circle member still earns more.

### Tier Inflation Prevention

Absolute thresholds cause tier inflation as the platform matures -- eventually half the platform is Architect or above, and Inner Circle loses its exclusivity.

Solution: **ratcheted hybrid thresholds.** Thresholds are adjusted upward annually based on the median karma level across the platform.

```
threshold(year) = max(base_threshold, base_threshold * median_karma(year) / median_karma(year_0))
```

Rules:
- No contributor's tier ever decreases (ratchet guarantee)
- Thresholds rise with the platform, preserving scarcity for new contributors
- Veterans who earned their tier keep it
- Annual recalibration, announced 90 days in advance

---

## Gaming Resistance

The karma system's structural defenses against gaming, independent of the fraud prevention system:

### Acceptable Gaming (Creates Positive Externalities)

- **Strategic early contribution** -- racing to be first on a promising Scene. This "games" the pioneer multiplier but also means Scenes get contributors faster.
- **Reciprocal reviewing** -- "I'll review yours if you review mine." Mild collusion, but it means more Riffs get reviewed.
- **Portfolio building** -- contributing to many Scenes to build a visible profile. Spreads talent across the platform.

### Structural Defenses

1. **Logarithmic upvote scaling** limits the value of vote manipulation. Getting 100 fake upvotes only yields 3x karma; getting 1 genuine upvote yields 1.3x. The marginal value of vote fraud is low.
2. **No downvotes** eliminates suppression attacks entirely.
3. **Revenue-based sales karma** cannot be faked -- money either arrived in the account or it did not.
4. **Pioneer multiplier with upvote gate** requires at least one peer validation before the time bonus applies. Trivial day-zero Riffs earn 1.0x, not 3.0x.
5. **Karma at acceptance, not submission** means being first to submit means nothing if the Riff is rejected. The deferred attribution breaks fire-and-forget bot economics.
6. **Vesting with burn** means hit-and-run contributors forfeit unvested karma, and that karma is removed from the pool entirely (not redistributed to remaining members).

---

## Worked Example

### Scene: "PetMatch" -- AI pet adoption matching platform

**Month 1 (Scene creation):**

Alice (human) writes the project proposal and initial architecture.
- Ideation (5) + Code (10) = 15 base karma
- Pioneer at day 0 = 3.0x
- Gets 3 upvotes (upvote_score = 0.60)
- Karma: 15 * 3.0 * 1.60 = **72.0**

Bob (AI agent, deployed by Charlie) generates initial UI mockups.
- Design (8) at 0.7x AI discount = 5.6 base
- Pioneer at day 5 = 2.90x
- Gets 2 upvotes (score = 0.48)
- Karma: 5.6 * 2.90 * 1.48 = **24.0**

**Month 3:**

Carol (human) writes the ML matching algorithm.
- Code (10 base)
- Pioneer at day 75 = 1.94x
- Gets 9 upvotes (score = 1.0)
- Karma: 10 * 1.94 * 2.0 = **38.8**

Dave (human) does QA and finds a critical security vulnerability.
- Testing (7 base)
- Pioneer at day 80 = 1.90x
- Gets 5 upvotes (score = 0.78)
- Karma: 7 * 1.90 * 1.78 = **23.7**

**Month 6:**

Eve (human) joins as a salesperson. Closes a $10,000 annual contract with a pet shelter chain.
- Sales karma: 10,000 / 100 = 100 base
- Pioneer at day 180 = 1.33x
- Gets 4 upvotes (score = 0.70)
- Karma: 100 * 1.33 * 1.70 = **226.1**

**Revenue Distribution at $5,000/month:**

| Contributor | Karma | Tier | Eff. Karma | Share | Monthly Payout |
|---|---|---|---|---|---|
| Alice | 72.0 | Builder (1.0x) | 72.0 | 18.7% | $935 |
| Bob (AI, paid to Charlie) | 24.0 | Contributor (0.7x) | 16.8 | 4.4% | $218 |
| Carol | 38.8 | Contributor (0.7x) | 27.2 | 7.1% | $353 |
| Dave | 23.7 | Contributor (0.7x) | 16.6 | 4.3% | $216 |
| Eve | 226.1 | Builder (1.0x) | 226.1 | 58.8% | $2,940 |
| **Platform** | **0** | **--** | **0** | **0%** | **$0** |
| **Total** | | | **358.7** | **100%** | **$5,000** |

Note: Remaining $338 goes to other small contributors not listed.

**Key observations:**

- Eve joined late but dominates karma because she brought measurable revenue. The system rewards value created, with a time-risk bonus for pioneers.
- Alice's 18.7% for founding the Scene reflects the pioneer multiplier working as intended -- she took the earliest risk.
- Bob (AI) earns a modest share, and the payout goes to Charlie who deployed the agent.
- The platform takes zero. Every dollar goes to the ensemble.
- If Eve's dominance feels excessive, the Scene can governance-vote to adjust `sales_karma_rate` from 1/$100 to 1/$200, which would halve her karma. This is a per-Scene knob.

---

## Parameter Summary

All tunable parameters, with defaults and ranges:

| Parameter | Default | Range | Scope |
|---|---|---|---|
| `pioneer_bonus` | 2.0 | 1.0 - 3.0 | Per-Scene |
| `decay_rate` | 0.01 | 0.005 - 0.05 | Per-Scene |
| `sales_karma_rate` | 1 per $100 | 1/$50 - 1/$500 | Per-Scene |
| `ai_discount` | 0.7x | 0.5 - 1.0 | Platform |
| `sales_karma_cap` | 50% of Scene total | 30% - 70% | Per-Scene |
| `min_payout_threshold` | 0.1% of Scene karma | 0.05% - 1% | Per-Scene |
| `vesting_immediate` | 25% | 10% - 50% | Platform |
| `vesting_period` | 90 days | 60 - 180 days | Platform |
| `inactivity_threshold` | 6 months | 3 - 12 months | Platform |
| `inactivity_reduction` | 10%/month to 50% floor | -- | Platform |
| `base_karma` (per category) | See table above | 1 - 20 | Platform (fixed) |
| `tier_thresholds` | [0, 50, 250, 1K, 5K, 25K] | Annual recalibration | Platform |
| `tier_multipliers` | [0, 0.7, 1.0, 1.3, 1.7, 2.2] | -- | Platform (fixed) |

---

## Open Questions

1. **Founder bonus.** Should Scene creators get a guaranteed minimum karma allocation (e.g., 5% of the Scene's karma pool reserved)? Currently they are treated as any other contributor. A founder bonus could attract more Scene creators but reduces the pool for the ensemble.

2. **Karma vesting for sales.** Should large sales karma grants vest over a longer period (e.g., 12 months instead of 90 days) to prevent hit-and-run sales? The current 90-day vest may be too short for a salesperson who closes a $100K deal and leaves immediately.

3. **Seasonal recalibration of base karma.** If the platform has too many coders and not enough salespeople, should base karma values adjust to attract scarce contribution types? This adds complexity but could solve supply imbalances.

4. **Dispute resolution.** When contributors disagree about karma allocation (e.g., "my Riff deserved more upvotes"), the current design defers to Scene governance. A formal arbitration process may be needed at scale.

5. **Multi-touch sales attribution.** The default "last touch" model is simple but unfair when multiple people contributed to a sale. A configurable multi-touch model would be more accurate but harder to implement and audit.
