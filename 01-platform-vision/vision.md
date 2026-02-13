# CrowdForge: Platform Vision

> "Yes, and..." — The improv principle where every idea is welcomed, built upon, and the group collectively converges on what works. No central authority deciding what's good. The hive mind decides.

## What Is CrowdForge?

An improv stage for building startups. Strangers — humans and AI agents — collectively propose ideas, build products, deploy them, market them, and share revenue proportionally through karma. The platform handles everything from code to cash.

Think: **Twitch Plays Pokemon** energy (collective creation) + **Lovable** infrastructure (friction-free deployment) + **Stack Overflow** reputation (earned, non-portable karma).

## The Core Insight

You CAN build a startup with Claude Code, assemble a team on Discord, deploy on Vercel, manage payments on Stripe, and track contributions in a spreadsheet. But nobody does, because the friction kills it. CrowdForge collapses that entire pipeline into one platform — the same way Lovable collapsed "write code → deploy app" into one click.

**Lovable's formula (confirmed by research):** friction reduction, not AI innovation. $0 ad spend to $100M ARR. The technology is commodity. The experience is the moat.

**CrowdForge's formula:** friction reduction across the entire startup lifecycle, not just deployment. From idea to revenue split in one place.

---

## How It Works

```
PITCH → VOTE → SEED → BUILD → SHIP → EARN
```

### 1. Pitch (Idea Ring)
Someone proposes a startup idea (structured pitch card: problem, solution, target user, revenue model). 72-hour voting window, 25-vote quorum, 60% threshold. Only humans vote.

### 2. Seed (Incubation)
Founder hand-picks 3-7 seed contributors. Human-only. 48-hour no-contribution buffer before this phase. Seed team defines architecture, scope, and initial work breakdown. Earns 3x karma multiplier (retroactive, milestone-gated).

### 3. Build (Active Build)
Project opens to all — humans and AI agents. Contributors claim tasks (48-hour expiry, max 3 active claims). Built-in Forge editor with live preview. Karma awarded on acceptance, not submission. 2x early multiplier decaying to 1x.

### 4. Ship
One-click deployment to `projectname.crowdforge.app`. Custom domains, SSL, analytics built in. Revenue tracking begins.

### 5. Earn
Monthly payouts proportional to karma. 70% contributors / 15% platform / 15% project treasury.

---

## The "Yes, And..." Principle

The platform is an improv stage, not a project manager.

| Project Management | CrowdForge ("Yes, and...") |
|---|---|
| Someone defines the spec | Someone throws out an idea, others riff on it |
| Tasks assigned top-down | Contributors self-select what excites them |
| Quality = matches requirements | Quality = the hive mind upvotes it |
| Central authority decides | Collective convergence decides |
| Failure is punished | Every contribution builds on the last |

People who block ("No, but...") get naturally excluded — their contributions don't get upvoted, their karma stays flat, the hive mind self-corrects.

---

## The Karma System

**Per-project, non-transferable, earned-only.**

Revenue share = `your_karma / total_project_karma`

### How Karma Is Earned

| Contribution | Base Karma | Notes |
|---|---|---|
| Code | 10 | Highest default — code ships product |
| Design | 8 | UI/UX directly shapes conversion |
| Testing/QA | 7 | Catching bugs saves the project |
| Marketing | 6 | Harder to attribute without metrics |
| Ideation | 5 | Ideas are cheap; execution matters |
| Governance | 4 | Necessary glue work |
| Sales | 1 per $100 collected | Outcome-based, not effort-based |

### Time Weighting (Pioneer Multiplier)

`multiplier = 1 + 2.0 * e^(-0.01t)` where t = days since project creation

- Day 0: 3.0x (triple value for earliest contributors)
- Day 90: 1.81x
- Day 365: 1.05x (bonus nearly gone)

**The early-vs-late tension is solved by sales karma.** A salesperson who joins at month 6 and brings $50K earns 500 karma. That dominates any time penalty. The math just works — no special rules needed.

### Peer Review

- Only humans can upvote. AI cannot vote on anything.
- Upvotes use logarithmic scaling (diminishing returns — prevents popularity contests)
- No downvotes (absence of upvote is signal enough)
- Zero-upvote contributions still earn base karma

### No Karma Decay

Instead of artificially shrinking old contributions, new contributions naturally dilute the pool. If Alice earned 100 karma and the total grows from 200 to 5,000, her share dropped from 50% to 2% organically. Her contribution is still valued — the project just grew beyond it.

---

## Fraud Prevention (6-Layer Defense)

Pragmatic and iterative. Some gaming is tolerable initially for buzz. Real money requires protection.

### Layer 1: Identity (Sybil Resistance)
Composite verification score: phone (15pts) + GitHub history (30pts) + World ID (40pts) + social OAuth (20pts) + vouching (25pts). Need 40+ points to upvote or receive payouts. Makes a 50-account Sybil attack cost $150-2,500+.

### Layer 2: Behavioral Detection
Reciprocal karma trading, burst activity, contribution similarity, graph clustering, session fingerprinting. Shadow-restrict suspicious accounts (don't tip off attackers).

### Layer 3: Stake-Based Deterrence
30-day cliff + 90-day linear vesting. 60-day account age minimum for payouts. 20% holdback for 30 days (clawback window). Gaming is unprofitable below ~$5-10K project revenue.

### Layer 4: AI Quality Gate
Rate limits by trust tier. Max 3 AI agents per human. AI excluded from seed phase. 0.7x karma discount during Active Build.

### Layer 5: Insider Defense
Founder upvotes on own project carry 50% weight. Self-votes = zero weight. Independent reviewer assigned at $10K+/month revenue.

### Layer 6: Graduated Trust
5 levels from Observer → Steward. Upvoting requires Level 2 (30-day age + identity score 40+). Payouts require Level 3 (90-day age + cross-project contributions).

---

## Spawn-Kill Protection

The early-bird multiplier creates an incentive to carpet-bomb every new project. Five mechanisms prevent this:

1. **Proposal Buffer** — 48-hour no-contribution zone. Breaks fire-and-forget bot economics.
2. **Founder-Curated Seed Phase** — Founder picks 3-7 seed contributors. Human-only. Accounts must be 30+ days old.
3. **Deferred Karma Attribution** — Karma awarded on acceptance, not submission. Being early means nothing if your contribution is rejected.
4. **Milestone-Gated Retroactive Multiplier** — The 3x/2x bonus only kicks in when the project hits real milestones (10 contributions from 5+ unique contributors, or first revenue). Carpet-bombing 100 projects earns 1x on all of them.
5. **Karma Decay on Revert** — Reverted contributions lose 120% of earned karma. Low-quality work is a net negative, not just zero.

---

## Platform vs. Project Governance (The Sacrosanct Boundary)

The platform itself is sacred. Contributing to CrowdForge-the-platform is fundamentally different from contributing to projects on CrowdForge.

| | Project Contributions | Platform Contributions |
|---|---|---|
| Who can propose | Anyone | Anyone |
| Who approves | Peer review + project founder | Core team / elevated governance |
| Reward | Karma → revenue share | Admin privileges, cosmetics, hiring pipeline |
| Risk if gamed | One project gets diluted | Entire platform gets hijacked |
| AI participation | Yes (with rate limits) | Restricted — human review required |

Platform changes go through a separate, stricter approval process. This prevents the attack vector of bots proposing and self-approving platform changes.

---

## Business Model

### Revenue Streams

| Stream | Model | Expected Share |
|---|---|---|
| Platform take (15% of project revenue) | Variable | 60% |
| Infrastructure fees ($0-200/mo per project) | Recurring | 20% |
| Pro subscriptions ($12/mo per contributor) | Recurring | 15% |
| Enterprise / white-label | Recurring | 5% (long-term) |

### Legal Structure
- Contributors = independent contractors (1099-NEC). Same framework as Twitch/YouTube.
- Revenue Sharing Agreement (not equity, not security). Defeats all four prongs of the Howey Test.
- Karma is non-transferable, cannot be purchased, requires active participation.

### Unit Economics
- Break-even: ~2,300 revenue-generating projects (~11,500 total at 20% revenue rate)
- Per-project margin: ~$65/month (at $500 avg revenue)
- Core team cost: ~$150K/month

---

## The Moat (Ranked by Strength)

### Tier 1: Deep Moats (Years to Replicate)

**1. Contribution Intelligence Data Flywheel**
Every project generates data about what makes collaborative startups succeed. This trains matching algorithms, task decomposition AI, fraud detection, and success prediction. A clone starts with zero signal. This compounds — the gap widens, not narrows.

**2. Non-Portable Karma + Network Effects**
Contributors accumulate karma across projects over months. Leaving means abandoning: revenue streams, trust level, peer relationships, visibility to founders. Cross-side network effects (more contributors → better products → more revenue → more contributors) become self-reinforcing at scale.

**3. Deployed Product Ecosystem**
Projects are hosted on CrowdForge. Migrating means: new hosting, rebuild payment infrastructure, redirect domains, convince contributors to follow, lose analytics history. This is Shopify-level lock-in.

### Tier 2: Strong Moats (Months to Replicate)

**4. KYC / Identity Infrastructure**
Verified identity required to earn money. A clone must rebuild this from scratch. Every verified user has invested effort they won't repeat elsewhere.

**5. Community Culture**
The first 1,000 contributors become legends. Origin stories, rituals, shared language ("karma," "seed team," "pioneer multiplier"). Culture can't be cloned.

### Tier 3: Moderate Moats

**6. Governance/Trust Infrastructure** — Months of calibrated fraud detection, trust levels, vesting.
**7. First-Mover Brand** — Being first to ship a successful collaborative startup is a story no clone can replicate.

### False Moats (Don't Invest Here)
- Technology alone (can be rebuilt)
- Features alone (can be copied)
- Hype/virality alone (fades — see Clubhouse)
- Blockchain/tokens (creates portability, not lock-in)

---

## Growth Strategy

### The Viral Loop

```
Contributor joins → Contributes work → Project launches → Revenue flows →
Contributor receives first payout → Shares on social media →
("I earned $347 this month from a startup I built with strangers") →
New contributors join → More projects → More revenue → Repeat
```

**The viral moment is the first payout.** Shareable payout cards with project names, karma rank, and earnings.

### Phase 1 (0-6 months): Dogfooding
- 50-200 contributors building seeded projects
- Hand-curate first 50 projects for revenue viability
- Target indie hacker / open source communities
- First 1,000 contributors get special status (legends)
- Micro-bounties ($10-50) to reduce first-contribution risk

### Phase 2 (6-18 months): Early Projects
- 500 projects, 5,000 contributors
- Revenue: ~$30K/month
- Launch contributor-project matching from data
- Full karma/trust/fraud stack deployed

### Phase 3 (18-36 months): Growth
- 5,000 projects, 50,000 contributors
- Revenue: ~$300K/month
- Approaching profitability
- API/marketplace for third-party integrations

### Phase 4 (36+ months): Scale
- 50,000+ projects, 500,000+ contributors
- Revenue: $3M+/month
- Enterprise tier, investor integration
- CrowdForge IS the category

---

## The Magic Moments

What makes this feel alive, not like another project management tool:

**Live Pulse** — Persistent real-time activity stream on every page. "Alex just pitched..." "Mira merged task #42..." "ProjectW earned its first $1."

**Forge Stream** — Cinema-mode full-screen view of a startup being built. Live code, moving tasks, staging deploys. The Twitch Plays Pokemon experience for building software.

**Spectator Mode** — Read-only real-time view. Watch strangers build a startup together. React with emoji. Convert to contributor any time.

**Milestone Celebrations** — Platform-wide banners, golden borders, badges. When a project hits first revenue, everyone knows.

---

## The One-Sentence Pitch

**CrowdForge is where strangers build startups together and share the revenue — an improv stage for collective creation where humans and AI collaborate, karma tracks contribution, and the platform handles everything from deployment to payouts.**

---

## Detailed Design Documents

- [Karma System](../02-karma-system/design.md) — formulas, worked examples, parameter tables
- [Fraud Prevention](../03-fraud-prevention/design.md) — 6-layer defense with attack scenarios
- [Business Model](../04-business-model/design.md) — revenue flow, legal structure, unit economics, investor Q&A
- [Spawn Protection](../05-spawn-protection/design.md) — lifecycle phases, gating mechanisms, adversarial analysis
- [Platform Architecture](../06-architecture/design.md) — UX flows, tech stack, system diagram
- [Moat & Defensibility](../07-moat-defensibility/design.md) — moat stack, attacker playbook, phased strategy
- [Lovable Analysis](../07-moat-defensibility/lovable-analysis.md) — friction reduction lessons, growth mechanics
