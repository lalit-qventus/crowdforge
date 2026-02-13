# CrowdForge Karma System Design

## Core Philosophy

Karma in CrowdForge is **per-project reputation that converts directly to revenue share**. It answers one question: "What fraction of this project's value did you create?"

Karma is not a vanity metric. It is a financial instrument — the denominator in a revenue-split equation. Every design decision below flows from this constraint.

### Design Principles

1. **Earned, never granted** — Karma comes from contribution + peer validation, not from role or title
2. **Per-project scope** — Karma in Project A says nothing about Project B (though a profile aggregates history)
3. **Human-validated** — Only humans can upvote; AI agents earn karma through contribution but cannot vote
4. **Time-aware** — Early risk-taking is rewarded, but late measurable value is never penalized
5. **Non-transferable** — You cannot give, sell, or delegate karma

---

## 1. Contribution Types and Base Karma

Every contribution to a CrowdForge project falls into one of seven categories. Each has a **base karma value** that reflects the typical effort and impact of that contribution type.

| Category | Examples | Base Karma | Rationale |
|---|---|---|---|
| **Ideation** | Problem statement, feature proposals, pivot suggestions | 5 | Ideas are cheap; execution matters more. But a great idea that redirects the project is invaluable — peer review handles that. |
| **Code** | Features, bug fixes, infrastructure, CI/CD, refactoring | 10 | Highest default weight. Code is the backbone of shipped product. |
| **Design** | UI/UX mockups, user flows, branding, design systems | 8 | Design directly shapes user experience and conversion. |
| **Testing/QA** | Test suites, bug reports with repro steps, security audits | 7 | Under-valued in most systems. Catching a critical bug before launch can save the project. |
| **Marketing** | Content, social media, community building, launch campaigns | 6 | Important but harder to attribute directly to revenue without metrics. |
| **Sales** | Closing deals, partnerships, revenue-generating activities | Variable (see Section 6) | Sales karma is outcome-based, not effort-based. |
| **Governance** | Dispute resolution, roadmap decisions, process improvements | 4 | Necessary glue work. Lower base because it's less directly value-creating, but peer multipliers can elevate it. |

**Why base karma varies by category:** A flat rate across categories would mean an idea sketch earns the same as a shipped feature. That creates perverse incentives. However, base karma is just the starting point — the peer review multiplier (Section 3) is where the real differentiation happens. A brilliant idea that reshapes the project will get heavily upvoted and can exceed the karma of routine code contributions.

**Tradeoff acknowledged:** Category weighting is inherently subjective. The alternative (flat base, pure peer review) was considered but rejected because it places too much burden on voters to assess cross-category value. Base weights provide a reasonable prior; votes adjust from there.

---

## 2. Time-Weighting: The Pioneer Multiplier

### The Problem

Early contributors take on more risk. When a project is just an idea, contributing code or design is a bet — most projects fail. Late contributors join when product-market fit exists, revenue is flowing, and risk is low. Without time-weighting, rational actors would wait for proof before contributing, creating a free-rider problem.

But time-weighting creates its own problem: if the multiplier is too aggressive, it penalizes a salesperson who joins at month 6 and brings in $50K of revenue. The system must reward both pioneers and late-stage value creators.

### The Formula

```
pioneer_multiplier = 1 + (pioneer_bonus * e^(-decay_rate * t))
```

Where:
- `t` = time elapsed since project creation (in days)
- `pioneer_bonus` = 2.0 (maximum bonus for day-zero contributions)
- `decay_rate` = 0.01 (controls how fast the bonus fades)

This gives:
- **Day 0:** multiplier = 3.0x (contribution worth triple)
- **Day 30:** multiplier = 2.48x
- **Day 90:** multiplier = 1.81x
- **Day 180:** multiplier = 1.33x
- **Day 365:** multiplier = 1.05x (bonus nearly gone)

### Why Exponential Decay, Not Linear

Linear decay (e.g., lose 0.5% per day) creates a cliff where the bonus abruptly hits zero. Exponential decay is asymptotic — the bonus gracefully approaches 1.0x but never creates a sudden discontinuity. This matters because contributors shouldn't feel a binary "I missed the window" moment.

### The Late-Value Safety Valve

The pioneer multiplier applies to **all** contributions, including late ones. A contributor joining at day 180 still gets 1.33x. But more importantly, the **Sales/Outcome** karma track (Section 6) operates independently of timing — if you bring in $50K of measurable revenue at day 300, the absolute value of that contribution dominates any time multiplier.

**Tradeoff:** A 3.0x day-zero multiplier means the first contributor who writes a README gets 3x karma for it. This is intentional — that README contributor also validated the project idea, recruited others by making the project tangible, and took the highest risk. If this feels too generous, the `pioneer_bonus` parameter can be tuned per-project by the project creator (within bounds of 1.0-3.0).

---

## 3. Peer Review and the Human Upvote

### Core Mechanic

After a contribution is submitted, project members can **upvote** it. Only humans can upvote. AI agents cannot vote on any contribution (including other AI agents' work or human work).

Each upvote applies a multiplier to the base karma:

```
contribution_karma = base_karma * pioneer_multiplier * (1 + upvote_score)
```

Where `upvote_score` is calculated from upvotes using diminishing returns:

```
upvote_score = ln(1 + upvote_count) / ln(10)
```

This logarithmic scaling means:
- **1 upvote:** score = 0.30 (1.30x multiplier on base)
- **3 upvotes:** score = 0.60 (1.60x)
- **9 upvotes:** score = 1.0 (2.0x)
- **30 upvotes:** score = 1.49 (2.49x)
- **99 upvotes:** score = 2.0 (3.0x)

### Why Logarithmic, Not Linear

Linear upvote scaling creates a "popularity contest" dynamic where viral contributions dominate regardless of actual value. Logarithmic scaling ensures that the first few upvotes matter most (validation that the contribution has value), while pile-on votes have diminishing effect. This mirrors how Stack Overflow's top answers don't earn proportionally more reputation than moderately upvoted ones.

### Zero-Upvote Contributions

A contribution with zero upvotes still earns its base karma (multiplied by pioneer). This is intentional — requiring upvotes to earn anything would create a bottleneck where all karma flows through voter attention, disadvantaging contributions in less visible areas (infrastructure, testing, documentation).

### Downvotes

There are no downvotes. The absence of an upvote is signal enough. Downvotes in karma-to-revenue systems create adversarial dynamics where contributors are incentivized to suppress competitors' karma. This is a lesson from Reddit, where downvote brigading is a persistent problem. If a contribution is harmful, it should be flagged for governance review, not silently downvoted.

**Tradeoff:** No downvotes means low-quality contributions accumulate base karma. This is mitigated by: (a) the governance review process can revoke karma from spam/harmful contributions, and (b) the logarithmic upvote curve means high-quality work pulls far ahead of unremarkable work over time.

---

## 4. Karma Decay: Should Old Contributions Fade?

### Position: No Automatic Decay on Earned Karma

This is a deliberate and somewhat contrarian choice. Many reputation systems (Reddit, Stack Overflow) don't decay karma either, but some DAO systems do. Here's the reasoning:

**Arguments for decay:**
- Prevents "rest and vest" — contribute early, coast forever
- Keeps the karma distribution dynamic
- Reflects that old code may be replaced or deprecated

**Arguments against decay (our position):**
- Karma converts to revenue share. Decaying karma means someone's revenue share shrinks over time even though their historical contribution was real. This feels like retroactively reneging on a deal.
- Early contributions already get less karma over time because new contributions dilute the total pool. If Alice earned 100 karma and the project total grows from 200 to 2000, her share dropped from 50% to 5% organically.
- Decay punishes people who contributed during high-risk periods and then moved on — exactly the people you want to reward.

### The Dilution Mechanism (Natural Decay)

Instead of explicit decay, CrowdForge uses **dilution**. As new contributions are made, the total karma pool grows, and each contributor's percentage share naturally decreases unless they keep contributing. This achieves the "stay engaged" incentive without the unfairness of retroactive karma reduction.

```
revenue_share(contributor) = contributor_karma / total_project_karma
```

A contributor who earned 100 karma on day 1 and never returned:
- Day 1: 100/100 = 100% share
- Day 30: 100/500 = 20% share
- Day 180: 100/5000 = 2% share

This is fair: their contribution is still valued at 100 karma, but the project grew beyond their contribution.

### Exception: Revoked Contributions

If a contribution is later found to be plagiarized, harmful, or fraudulent, governance can revoke the karma entirely. This is not decay — it's correction.

**Tradeoff:** No decay means a contributor who made a single massive contribution early on retains that karma forever, even if the codebase they wrote is entirely rewritten. The counter-argument: they took the risk, they validated the approach, and the rewrite builds on what they proved. The pioneer multiplier already rewards this appropriately, and dilution handles the rest.

---

## 5. Karma-to-Revenue Conversion

### Per-Project Revenue Pool

Each CrowdForge project has a **revenue pool** — 100% of the money generated by the product (subscriptions, sales, licensing, etc.). This pool is distributed proportionally based on karma. The platform participates as a contributor (earning karma for hosting, tooling, and infrastructure), so its share comes through the same karma system as everyone else — not through a fee or commission.

```
payout(contributor) = project_revenue * (contributor_karma / total_project_karma)
```

### Payout Frequency

Monthly. This is a pragmatic choice:
- Weekly is too noisy (revenue fluctuates)
- Quarterly is too slow (contributors want to see returns from their work)
- Monthly strikes a balance and aligns with standard billing cycles

### Minimum Payout Threshold

Contributors must hold at least **0.1% of project karma** to receive a payout in a given cycle. Below this threshold, karma accumulates but doesn't trigger payment. This prevents micro-transactions and gas-like overhead from thousands of tiny payments.

### Revenue Distribution

100% of project revenue flows to karma-weighted contributors. There is no platform fee, no commission, and no separate treasury allocation.

The platform earns its share by participating in the karma system as a contributor. CrowdForge earns karma for the infrastructure contributions it makes to every project — hosting, deployment, tooling, CI/CD, payment processing, and karma computation. This karma is weighted and distributed alongside every other contributor's karma.

This means the platform's incentives are fully aligned with contributors: the better the infrastructure, the more karma it earns, and the more it receives from the shared revenue pool — through the same mechanism as everyone else.

---

## 6. Sales and Outcome-Based Karma

### The Problem with Effort-Based Karma for Sales

Most contribution types are effort-based: you write code, you earn karma. Sales is different. A salesperson who spends 100 hours and closes zero deals created less project value than one who spends 10 hours and closes a $50K contract. Sales karma must be outcome-based.

### Sales Karma Formula

```
sales_karma = revenue_brought * sales_karma_rate
```

Where `sales_karma_rate` is set per-project (default: **1 karma per $100 of attributed revenue**).

Examples:
- Bring in a $10,000 contract → 100 sales karma
- Close a $50,000 partnership → 500 sales karma

This karma is then subject to the same pioneer multiplier and peer review as other contributions.

### Attribution Rules

Revenue attribution follows "last touch" by default — whoever closed the deal gets credit. Projects can opt into more complex attribution (first touch, multi-touch) through governance decisions, but the default is simple and unambiguous.

### Why This Solves the Early-vs-Late Tension

A late contributor who brings in $50K of revenue earns 500 karma. Even without a pioneer multiplier (say, 1.05x at day 365), that 525 karma likely represents a significant share of total project karma. The absolute value of measurable revenue dominates any time-weighting penalty.

Compare: an early contributor who wrote the MVP (say, 200 hours of code at 10 base karma each, with 3.0x pioneer and average 1.5x peer review = 9,000 karma) still has more karma — and that's appropriate, because without the MVP there's nothing to sell. But the salesperson's 525 karma out of, say, 15,000 total still yields a meaningful 3.5% revenue share, which on $50K/month revenue is $1,225/month. Not bad for joining late.

**Tradeoff:** Tying sales karma directly to revenue creates incentive to close deals at any cost (e.g., offering unsustainable discounts). Mitigation: sales karma is based on *collected* revenue, not contracted revenue. If a customer churns after one month, only one month of revenue converts to karma.

---

## 7. AI Agent Karma

### How AI Agents Earn Karma

AI agents participate as contributors, not as voters. They earn karma the same way humans do — through contributions that are peer-reviewed by humans.

- An AI agent that writes code earns Code karma (base 10), subject to pioneer multiplier and human upvotes
- An AI agent that generates design mockups earns Design karma (base 8)
- An AI agent that runs automated test suites earns Testing karma (base 7)

### What AI Agents Cannot Do

- **Cannot upvote** — Only humans validate contribution quality
- **Cannot participate in governance votes** — Governance decisions require human judgment
- **Cannot receive direct payouts** — Payouts go to the human or organization that deployed the agent

### Why This Works

The "humans validate, AI executes" model prevents a scenario where a swarm of AI agents upvote each other's mediocre contributions into high karma. The human bottleneck on voting is a feature, not a bug — it ensures that every karma point has been seen and approved by a human.

**Tradeoff:** This means AI contributions can sit in a "pending validation" state if human reviewers are scarce. The mitigation is that unreviewed contributions still earn base karma — the upvote multiplier is a bonus, not a requirement.

---

## 8. Gaming Considerations

### Acceptable Gaming (Creates Buzz)

The founder explicitly stated that some gaming is acceptable initially. These behaviors are gaming but create positive externalities:

- **Strategic early contribution** — Racing to be first on a promising project. This is "gaming" the pioneer multiplier, but it also means projects get contributors faster.
- **Reciprocal upvoting** — "I'll review yours if you review mine." This is mild collusion, but it also means more contributions get reviewed.
- **Portfolio building** — Contributing to many projects to build a visible profile. This spreads talent across the platform.

### Unacceptable Gaming (Requires Prevention)

- **Sybil attacks** — Creating fake human accounts to upvote your own contributions. Mitigation: identity verification (phone, government ID) for upvote-eligible accounts.
- **Karma farming with low-effort contributions** — Submitting trivial changes (whitespace, typo fixes) en masse. Mitigation: minimum contribution size thresholds per category; governance can flag patterns.
- **Collusion rings** — Organized groups systematically upvoting each other. Mitigation: graph analysis on voting patterns; flag accounts whose upvotes are statistically non-independent.
- **AI masquerading as human** — Deploying AI agents as "human" accounts to gain voting rights. Mitigation: periodic human verification challenges (not CAPTCHAs — those are solved by AI — but video calls, proof-of-work tasks, or vouching systems).

The fraud prevention system is designed separately, but the karma system's structural defenses are:
1. Logarithmic upvote scaling limits the value of vote manipulation
2. No downvotes eliminates suppression attacks
3. Revenue-based sales karma can't be faked (money either arrived or it didn't)
4. Pioneer multiplier rewards genuine early risk, not gaming

---

## 9. Cross-Project Reputation (Profile Karma)

While karma is per-project for revenue purposes, CrowdForge also maintains a **profile-level reputation** for discovery and trust:

```
profile_reputation = sum(project_karma * project_success_weight)
```

Where `project_success_weight` ranges from 0.1 (failed/inactive project) to 1.0 (actively generating revenue).

This prevents someone from farming karma on dead projects and appearing credible. Profile reputation is never used for revenue distribution — it's purely a signal for project creators deciding who to invite or accept.

---

## 10. Comparison with Existing Systems

| System | What CrowdForge Borrows | What CrowdForge Rejects |
|---|---|---|
| **Reddit** | Upvote-based karma, logarithmic scaling | Downvotes, global karma (not project-scoped), karma as vanity metric |
| **Stack Overflow** | Category-specific reputation (questions vs. answers), daily caps concept | Rigid point values, accepted-answer bonus (creates perverse incentive to accept fast, not best) |
| **Gitcoin** | Sybil resistance through identity verification, "cost of forgery" framing | Blockchain dependency, stamp-based scoring (too identity-focused, not contribution-focused) |
| **DAO Reputation** | Non-transferability, governance participation gating | Token-based systems, on-chain complexity |
| **OSS Contributor Index** | Measuring diverse contribution types beyond code | Employer-centric scoring, commit-count metrics |

---

## 11. Worked Example

**Project: "PetMatch" — an AI pet adoption matching platform**

**Month 1 (project creation):**
- Alice (human) writes the project proposal and initial architecture. Ideation (5 base) + Code (10 base) = 15 base karma. Pioneer multiplier at day 0 = 3.0x. Gets 3 upvotes (upvote_score = 0.60). Total: 15 * 3.0 * 1.60 = **72 karma**.
- Bob (AI agent) generates the initial UI mockups. Design (8 base). Pioneer at day 5 = 2.90x. Gets 2 upvotes (score = 0.48). Total: 8 * 2.90 * 1.48 = **34.3 karma**.

**Month 3:**
- Carol (human) writes the ML matching algorithm. Code (10 base). Pioneer at day 75 = 1.94x. Gets 9 upvotes (score = 1.0). Total: 10 * 1.94 * 2.0 = **38.8 karma**.
- Dave (human) does QA and finds a critical security bug. Testing (7 base). Pioneer at day 80 = 1.90x. Gets 5 upvotes (score = 0.78). Total: 7 * 1.90 * 1.78 = **23.7 karma**.

**Month 6:**
- Eve (human) joins as a salesperson. Closes a $10,000 annual contract with a pet shelter chain. Sales karma = 10,000 / 100 = 100 karma. Pioneer at day 180 = 1.33x. Gets 4 upvotes (score = 0.70). Total: 100 * 1.33 * 1.70 = **226.1 karma**.

**Total project karma: 394.9**

| Contributor | Karma | Revenue Share | Monthly Payout (at $5K/mo revenue) |
|---|---|---|---|
| Alice (founder) | 72.0 | 18.2% | $910 |
| Bob (AI agent) | 34.3 | 8.7% | $435 |
| Carol (ML engineer) | 38.8 | 9.8% | $490 |
| Dave (QA) | 23.7 | 6.0% | $300 |
| Eve (sales) | 226.1 | 57.2% | $2,860 |

**Key observation:** Eve joined late but dominates karma because she brought measurable revenue. The pioneer multiplier for Alice ensures she's rewarded for taking the initial risk, but the system doesn't pretend that writing a proposal is worth more than generating $10K in sales. This is the intended behavior — the system rewards *value created*, with a time-risk bonus for pioneers.

If Eve's sales karma feels disproportionate, the project can governance-vote to adjust the `sales_karma_rate` (e.g., 1 karma per $200 instead of $100). This is a per-project knob, not a platform-wide setting.

---

## 12. Parameter Summary

All tunable parameters in one place, with defaults and allowed ranges:

| Parameter | Default | Range | Scope |
|---|---|---|---|
| `pioneer_bonus` | 2.0 | 1.0 - 3.0 | Per-project |
| `decay_rate` | 0.01 | 0.005 - 0.05 | Per-project |
| `sales_karma_rate` | 1 per $100 | 1 per $50 - 1 per $500 | Per-project |
| `contributor_pool_pct` | 100% | Fixed | Platform |
| `min_payout_threshold` | 0.1% of project karma | 0.05% - 1% | Per-project |
| `base_karma` (per category) | See Section 1 | 1 - 20 | Platform (fixed) |

---

## 13. Open Questions and Future Considerations

1. **Should project creators get a founder bonus?** Currently they're treated as contributors. A fixed founder allocation (e.g., 10% of karma pool reserved) could attract more project creators but reduces the pool for other contributors.

2. **Multi-project contributors:** If someone contributes to 5 projects, they're spreading thin. Should there be a focus bonus for deep contributors vs. shallow ones? Current design says no — let the market decide.

3. **Karma vesting:** Should large karma grants (especially sales) vest over time (e.g., 25% immediate, 75% over 12 months)? This prevents hit-and-run sales contributions but adds complexity.

4. **Dispute resolution for karma:** When contributors disagree about karma allocation, how is this resolved? Currently deferred to governance, but a formal arbitration process may be needed.

5. **Seasonal recalibration:** Should base karma values be adjusted periodically based on platform-wide data about contribution supply/demand? E.g., if the platform has too many coders and not enough salespeople, adjust base karma to attract sales contributors.
