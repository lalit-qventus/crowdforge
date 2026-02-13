# CrowdForge: Platform Vision

> "Yes, and..." — The improv principle where every idea is welcomed, built upon, and the group collectively converges on what works. No central authority deciding what's good. The hive mind decides.

## The One-Sentence Pitch

**CrowdForge is the backstage of a theater where anyone can walk in, watch rehearsal, and step on stage — a creative platform where people riff on each other's ideas, build together in real time, and share in what they create.**

---

## The Creative Experience

CrowdForge is structured around three layers:

- **Stage** — the platform itself. The theater, the lights, the infrastructure.
- **Scene** — a living creative project. Not a task list — a thing being built by an ensemble.
- **Riff** — the atomic creative unit. Everything that happens on CrowdForge is a riff.

### The Riff

A Riff is the smallest unit of creative contribution. It is:

- **Small** — a single meaningful addition, not a multi-day epic
- **Creative** — it adds something that didn't exist before
- **Composable** — it builds on existing riffs, and future riffs build on it
- **Format-aware** — code, design, copy, testing, marketing, governance — all are riffs
- **Visible** — every riff is seen, attributed, and tracked in real time

The Riff replaces the "task" and the "ticket." You don't complete a task. You riff on a Scene.

### The Five Emotional Moments

These are the feelings that make CrowdForge addictive:

1. **Someone riffed on my riff.** Your code got extended. Your design got implemented. Your idea became real. The feeling that your work matters to people.
2. **I watched it get built.** You were in the audience when the ensemble shipped a feature live. You saw the code appear, the preview update, the staging deploy. You were there.
3. **The Scene shipped.** The thing you helped build is live on the internet. Real people are using it. You can send the link to your friends.
4. **My first karma.** The platform acknowledged your contribution. You have a score. You exist in the system. You matter.
5. **My first payout.** Real money, deposited in your bank account, from a Scene you helped build with people. This is the moment people screenshot and share.

### The Spectator-to-Creator Pipeline

Not everyone walks in ready to contribute. The pipeline:

```
Watch → React → Micro-riff → Skill-riff → Lead
```

- **Watch** — Spectator mode. Full-screen cinema view of a Scene being built in real time. Live code, moving tasks, staging deploys.
- **React** — Audience members react with emoji, comment, cheer on the ensemble.
- **Micro-riff** — First contribution. Fix a typo, suggest a color, write one line of copy. Barrier is near zero.
- **Skill-riff** — Real contribution. Ship a component, design a page, write a marketing email. Earns meaningful karma.
- **Lead** — Pitch your own Scene. Curate your own ensemble. You've gone from watching to running the show.

### The "Yes, And..." Principle

The Stage is an improv theater, not a project manager.

| Project Management | CrowdForge ("Yes, and...") |
|---|---|
| Someone defines the spec | Someone throws out an idea, others riff on it |
| Tasks assigned top-down | Ensemble members self-select what excites them |
| Quality = matches requirements | Quality = the ensemble upvotes it |
| Central authority decides | Collective convergence decides |
| Failure is punished | Every riff builds on the last |

People who block ("No, but...") get naturally excluded — their riffs don't get upvoted, their karma stays flat, the hive mind self-corrects.

### The Campfire Model

A Scene is a campfire. The founder lights it. The ensemble gathers around it. Some people sit close and tend the fire. Some sit further back and watch. Some wander between campfires. The fire doesn't have an org chart. People contribute because the fire is interesting and warm.

### The Magic Moments

What makes this feel alive:

**Live Pulse** — Persistent real-time activity stream on every page. "Alex just pitched a new Scene..." "Mira's riff was accepted..." "SceneW earned its first $1."

**Forge Stream** — Cinema-mode full-screen view of a Scene being built. Live code, moving tasks, staging deploys. The Twitch Plays Pokemon experience for building software.

**Spectator Mode** — Read-only real-time view. Watch people build together. React as audience. Convert to ensemble member any time.

**Milestone Celebrations** — Stage-wide banners, golden borders, badges. When a Scene hits first revenue, everyone knows.

---

## What CrowdForge Is NOT

- **Not a project management tool.** No Gantt charts, no sprint planning, no ticket queues. Riffs, not tasks.
- **Not a freelance marketplace.** No clients hiring freelancers. An ensemble building together and sharing revenue.
- **Not a hackathon.** No deadlines, no judges, no prizes. Scenes live as long as the ensemble keeps riffing.
- **Not a DAO.** No tokens, no governance votes, no blockchain. Karma and payouts, simple as that.
- **Not a code repository.** Code is one type of riff. Design, copy, marketing, testing, sales — all first-class riffs.

**It's the backstage of a theater where anyone can walk in, watch rehearsal, and step on stage.**

---

## How It Works

```
PITCH → VOTE → SEED → BUILD → SHIP → EARN
```

### 1. Pitch (Idea Ring)
Someone proposes a Scene (structured pitch card: problem, solution, target user, revenue model). 72-hour voting window, 25-vote quorum, 60% threshold. Only humans vote.

### 2. Seed (Incubation)
Founder hand-picks 3-7 seed ensemble members. Human-only. 48-hour no-riff buffer before this phase. Seed team defines architecture, scope, and initial work breakdown. Earns 3x karma multiplier (retroactive, milestone-gated).

### 3. Build (Active Build)
Scene opens to all — humans and AI agents. Ensemble members claim tasks (48-hour expiry, max 3 active claims). Built-in Forge editor with live preview. Karma awarded on acceptance, not submission. 2x early multiplier decaying to 1x.

### 4. Ship
One-click deployment to `scenename.crowdforge.app`. Custom domains, SSL, analytics built in. Revenue tracking begins.

### 5. Earn
Monthly payouts proportional to karma. 100% of Scene revenue goes to the ensemble. The platform takes zero commission.

---

## The Karma System

**Per-Scene, non-transferable, earned-only.**

Revenue share = `your_karma / total_scene_karma`

### How Karma Is Earned

| Riff Type | Base Karma | Notes |
|---|---|---|
| Code | 10 | Highest default — code ships product |
| Design | 8 | UI/UX directly shapes conversion |
| Testing/QA | 7 | Catching bugs saves the Scene |
| Marketing | 6 | Harder to attribute without metrics |
| Ideation | 5 | Ideas are cheap; execution matters |
| Governance | 4 | Necessary glue work |
| Sales | 1 per $100 collected | Outcome-based, not effort-based |

### Time Weighting (Pioneer Multiplier)

`multiplier = 1 + 2.0 * e^(-0.01t)` where t = days since Scene creation

- Day 0: 3.0x (triple value for earliest ensemble members)
- Day 90: 1.81x
- Day 365: 1.05x (bonus nearly gone)

**The early-vs-late tension is solved by sales karma.** A salesperson who joins at month 6 and brings $50K earns 500 karma. That dominates any time penalty. The math just works — no special rules needed.

### Peer Review

- Only humans can upvote. AI cannot vote on anything.
- Upvotes use logarithmic scaling (diminishing returns — prevents popularity contests)
- No downvotes (absence of upvote is signal enough)
- Zero-upvote riffs still earn base karma

### No Karma Decay

Instead of artificially shrinking old riffs, new riffs naturally dilute the pool. If Alice earned 100 karma and the total grows from 200 to 5,000, her share dropped from 50% to 2% organically. Her riff is still valued — the Scene just grew beyond it.

---

## Business Model

### Zero Commission, Donation-Backed

100% of Scene revenue goes to the ensemble. The platform takes zero commission and earns zero karma on Scenes. CrowdForge does not participate in revenue sharing.

Platform costs are covered by:

| Stream | Model |
|---|---|
| Community donations | Voluntary, karma-linked social expectation (not requirement). Like Wikipedia's model — transparent cost dashboard showing what it costs to run CrowdForge. |
| Infrastructure fees | Direct cost pass-through for hosting tiers ($0-200/mo per Scene) |
| Pro subscriptions | Optional $12/mo for advanced analytics, priority deployment, private Scenes |

### Legal Structure
- Ensemble members = independent contractors (1099-NEC). Same framework as Twitch/YouTube.
- Revenue Sharing Agreement (not equity, not security). Defeats all four prongs of the Howey Test.
- Karma is non-transferable, cannot be purchased, requires active participation.

---

## Fraud Prevention (6-Layer Defense)

Pragmatic and iterative. Some gaming is tolerable initially for buzz. Real money requires protection.

### Layer 1: Identity (Sybil Resistance)
Composite verification score: phone (15pts) + GitHub history (30pts) + World ID (40pts) + social OAuth (20pts) + vouching (25pts). Need 40+ points to upvote or receive payouts. Makes a 50-account Sybil attack cost $150-2,500+.

### Layer 2: Behavioral Detection
Reciprocal karma trading, burst activity, riff similarity, graph clustering, session fingerprinting. Shadow-restrict suspicious accounts (don't tip off attackers).

### Layer 3: Stake-Based Deterrence
30-day cliff + 90-day linear vesting. 60-day account age minimum for payouts. 20% holdback for 30 days (clawback window). Gaming is unprofitable below ~$5-10K Scene revenue.

### Layer 4: AI Quality Gate
Rate limits by trust tier. Max 3 AI agents per human. AI excluded from seed phase. 0.7x karma discount during Active Build.

### Layer 5: Insider Defense
Founder upvotes on own Scene carry 50% weight. Self-votes = zero weight. Independent reviewer assigned at $10K+/month revenue.

### Layer 6: Graduated Trust
5 levels from Observer → Steward. Upvoting requires Level 2 (30-day age + identity score 40+). Payouts require Level 3 (90-day age + cross-Scene contributions).

---

## Spawn-Kill Protection

The early-bird multiplier creates an incentive to carpet-bomb every new Scene. Five mechanisms prevent this:

1. **Proposal Buffer** — 48-hour no-riff zone. Breaks fire-and-forget bot economics.
2. **Founder-Curated Seed Phase** — Founder picks 3-7 seed ensemble members. Human-only. Accounts must be 30+ days old.
3. **Deferred Karma Attribution** — Karma awarded on acceptance, not submission. Being early means nothing if your riff is rejected.
4. **Milestone-Gated Retroactive Multiplier** — The 3x/2x bonus only kicks in when the Scene hits real milestones (10 riffs from 5+ unique ensemble members, or first revenue). Carpet-bombing 100 Scenes earns 1x on all of them.
5. **Karma Decay on Revert** — Reverted riffs lose 120% of earned karma. Low-quality work is a net negative, not just zero.

---

## Platform vs. Scene Governance (The Sacrosanct Boundary)

The platform itself is sacred. Contributing to CrowdForge-the-platform is fundamentally different from contributing to Scenes on CrowdForge.

| | Scene Riffs | Platform Contributions |
|---|---|---|
| Who can propose | Anyone | Anyone |
| Who approves | Peer review + Scene founder | Core team / elevated governance |
| Reward | Karma → revenue share | Admin privileges, cosmetics, hiring pipeline |
| Risk if gamed | One Scene gets diluted | Entire platform gets hijacked |
| AI participation | Yes (with rate limits) | Restricted — human review required |

Platform changes go through a separate, stricter approval process. This prevents the attack vector of bots proposing and self-approving platform changes.

---

## The Core Insight

You CAN build a startup with Claude Code, assemble a team on Discord, deploy on Vercel, manage payments on Stripe, and track contributions in a spreadsheet. But nobody does, because the friction kills it. CrowdForge collapses that entire pipeline into one platform — the same way Lovable collapsed "write code → deploy app" into one click.

**Lovable's formula (confirmed by research):** friction reduction, not AI innovation. $0 ad spend to $100M ARR. The technology is commodity. The experience is the moat.

**CrowdForge's formula:** friction reduction across the entire startup lifecycle, not just deployment. From idea to revenue split in one place.

Think: **Twitch Plays Pokemon** energy (collective creation) + **Lovable** infrastructure (friction-free deployment) + **Stack Overflow** reputation (earned, non-portable karma).

---

## The Moat (Ranked by Strength)

### Tier 1: Deep Moats (Years to Replicate)

**1. Contribution Intelligence Data Flywheel**
Every Scene generates data about what makes collaborative startups succeed. This trains matching algorithms, task decomposition AI, fraud detection, and success prediction. A clone starts with zero signal. This compounds — the gap widens, not narrows.

**2. Non-Portable Karma + Network Effects**
Ensemble members accumulate karma across Scenes over months. Leaving means abandoning: revenue streams, trust level, peer relationships, visibility to founders. Cross-side network effects (more ensemble members → better products → more revenue → more ensemble members) become self-reinforcing at scale.

**3. Deployed Product Ecosystem**
Scenes are hosted on CrowdForge. Migrating means: new hosting, rebuild payment infrastructure, redirect domains, convince ensemble to follow, lose analytics history. This is Shopify-level lock-in.

### Tier 2: Strong Moats (Months to Replicate)

**4. KYC / Identity Infrastructure**
Verified identity required to earn money. A clone must rebuild this from scratch. Every verified user has invested effort they won't repeat elsewhere.

**5. Community Culture**
The first 1,000 ensemble members become legends. Origin stories, rituals, shared language ("karma," "seed team," "pioneer multiplier," "riff"). Culture can't be cloned.

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
Ensemble member joins → Riffs on a Scene → Scene launches → Revenue flows →
Ensemble member receives first payout → Shares on social media →
("I earned $347 this month from a Scene I built with people") →
New ensemble members join → More Scenes → More revenue → Repeat
```

**The viral moment is the first payout.** Shareable payout cards with Scene names, karma rank, and earnings.

### Phase 1 (0-6 months): Dogfooding
- 50-200 ensemble members building seeded Scenes
- Hand-curate first 50 Scenes for revenue viability
- Target indie hacker / open source communities
- First 1,000 ensemble members get special status (legends)
- Micro-bounties ($10-50) to reduce first-riff risk

### Phase 2 (6-18 months): Early Scenes
- 500 Scenes, 5,000 ensemble members
- Revenue: ~$30K/month
- Launch ensemble-Scene matching from data
- Full karma/trust/fraud stack deployed

### Phase 3 (18-36 months): Growth
- 5,000 Scenes, 50,000 ensemble members
- Revenue: ~$300K/month
- Approaching profitability
- API/marketplace for third-party integrations

### Phase 4 (36+ months): Scale
- 50,000+ Scenes, 500,000+ ensemble members
- Revenue: $3M+/month
- Enterprise tier, investor integration
- CrowdForge IS the category

---

## Detailed Design Documents

- [Karma System](karma-system/design.md) — formulas, worked examples, parameter tables
- [Fraud Prevention](fraud-prevention/design.md) — 6-layer defense with attack scenarios
- [Business Model](business-model/design.md) — revenue flow, legal structure, unit economics, investor Q&A
- [Spawn Protection](spawn-protection/design.md) — lifecycle phases, gating mechanisms, adversarial analysis
- [Platform Architecture](architecture/design.md) — UX flows, tech stack, system diagram
- [Moat & Defensibility](moat-defensibility/design.md) — moat stack, attacker playbook, phased strategy
- [Lovable Analysis](moat-defensibility/lovable-analysis.md) — friction reduction lessons, growth mechanics
