# Anti-Fraud and Sybil Resistance Design

CrowdForge distributes real money based on karma. Every karma point is a claim on revenue. This makes the karma system a financial target, and the fraud surface is proportional to the money flowing through the platform.

This document defines the threat model, proposes concrete anti-fraud mechanisms, and lays out a phased rollout that matches defense investment to actual risk.

---

## Threat Model

### The Core Attack

A single human creates multiple accounts (bots, sock puppets, purchased identities) to upvote their own contributions, inflating their karma and extracting a disproportionate share of project revenue from genuine contributors.

This is a Sybil attack. Everything else -- farming rings, AI spam, insider manipulation -- is a variation on the same economic exploit: manufacture karma cheaply, extract revenue expensively.

### Why CrowdForge Is Especially Vulnerable

Most platforms with reputation systems (Reddit, Stack Overflow) use karma as a vanity metric. Gaming it wastes time but doesn't steal money. CrowdForge's karma-to-revenue conversion makes every karma point worth a calculable dollar amount. This changes attacker incentives fundamentally:

- **Reddit karma fraud**: Costs time, yields social status. Attacker motivation: ego.
- **CrowdForge karma fraud**: Costs money to set up, yields money in return. Attacker motivation: profit.

Profit-motivated attackers are more persistent, more sophisticated, and more willing to invest in infrastructure than ego-motivated ones. The defense system must be calibrated for this reality.

### Attack Taxonomy

| Attack | Mechanism | Severity | When It Becomes Rational |
|--------|-----------|----------|--------------------------|
| **Sybil swarm** | One person operates 10-500 fake accounts to self-upvote | Critical | When project revenue exceeds the cost of maintaining fake identities (~$5K/month) |
| **Karma farming ring** | 3-10 real humans trade upvotes reciprocally to inflate each other's karma | High | When modest karma inflation yields meaningful revenue share (>$1K/month) |
| **AI contribution spam** | Registered AI agents generate high-volume, superficially valid but low-value contributions | Medium | When velocity limits are loose enough to accumulate base karma faster than dilution |
| **Insider manipulation** | Project founder biases karma toward themselves or accomplices | High | From day one (founders have structural advantages) |
| **Carpet-bombing** | Bots spray low-effort contributions across every new project to capture early-bird multipliers | Medium | When the pioneer multiplier is high and acceptance gates are loose |
| **Identity marketplace** | Attackers purchase verified accounts from real humans who completed KYC | High | When KYC-verified accounts have a market price lower than extractable karma value |
| **Reviewer capture** | Attacker builds reviewer status, then approves their own alts' contributions | High | When reviewer entry threshold is low relative to the karma it gates |

### What the Founder Accepts

Several constraints shape the design:

1. **Some gaming is tolerable early on.** It creates activity. It only matters when real money flows.
2. **Anti-fraud doesn't need to be perfect.** It needs to make fraud unprofitable.
3. **If someone brings $10K in actual sales, fraud matters less.** Self-evident value doesn't need the same scrutiny as self-awarded karma.
4. **Only humans can upvote.** AI agents contribute but do not validate.
5. **Heavy KYC kills onboarding.** The system cannot demand government ID at sign-up.

---

## Design Principles

### 1. Make Gaming Unprofitable, Not Impossible

Perfect fraud prevention doesn't exist. The goal is economic: the cost of cheating must exceed the reward. If maintaining 50 Sybil accounts costs $2,500 in time and money, and the maximum extractable revenue from a typical project is $500/month, the attack is irrational.

### 2. False Positives Are Worse Than False Negatives

Rejecting a legitimate early contributor costs more than tolerating mild karma inflation. Especially in the first year, every real contributor is precious. The system should err toward leniency and tighten as revenue grows.

### 3. Shadow-Restrict, Never Tip Off

Fraudsters who know they're caught iterate their tactics. Delayed, invisible enforcement buys investigation time. Accounts suspected of fraud should continue to see normal behavior from their perspective while their actions are silently quarantined.

### 4. Progressive Verification

Light-touch at sign-up. Heavier when money is at stake. A user browsing projects needs an email. A user receiving their first payout needs proof of unique humanity.

### 5. Defense in Depth

No single mechanism is sufficient. The system layers identity verification, behavioral analysis, economic deterrence, and community governance. An attacker who defeats one layer still faces five others.

---

## Layer 1: Identity -- Proving Unique Humanity

### The Problem

CrowdForge needs to establish that each account represents a distinct human being, without demanding government-issued identification at sign-up. The tension: low friction attracts users, but low friction also attracts bots.

### Composite Identity Score

Rather than a single verification gate, the system uses a composite score inspired by Gitcoin Passport's stamp model. Users collect verification "stamps" from multiple sources. Each stamp has a score reflecting how expensive it is to forge at scale (the "cost of forgery" principle).

| Verification Method | Score | Cost to Forge (per account) | Implementation |
|---------------------|-------|-----------------------------|----------------|
| Email verification | 5 | ~$0 (disposable emails are free) | Standard confirmation link. Store hash of address. |
| Phone SMS (unique number) | 15 | ~$1-3 (VoIP numbers) | Twilio or similar. Store hash only. VoIP numbers detected and scored at 5 instead of 15. |
| Social OAuth (GitHub, Google, LinkedIn) | 20 | ~$5-20 (aged accounts on secondary markets) | OAuth token exchange. Store provider + unique user ID. Account age < 30 days scores 10 instead of 20. |
| GitHub contribution history (>6 months, >10 repos) | 30 | ~$50+ (requires months of real activity or expensive purchase) | GitHub API check. Store boolean "passed" + check date. |
| World ID (proof of personhood) | 40 | Effectively impossible to duplicate (biometric uniqueness) | World ID OAuth-style API. Store verification status, not biometric data. |
| Vouching by 2+ verified users | 25 | Requires social capital within the platform | Two Trusted (Level 3+) accounts vouch. Voucher credibility affected if vouchee is later flagged. Vouches expire after 1 year. |

### Threshold Gates

Identity score gates specific capabilities:

| Identity Score | Capabilities Unlocked |
|----------------|-----------------------|
| 5+ (email only) | Browse projects, comment, discuss |
| 20+ | Submit contributions |
| 40+ | Upvote, join projects, earn karma |
| 60+ | Receive payouts, vouch for others, create projects |

This means:
- GitHub history (30) + phone (15) = 45 -- sufficient to upvote and earn karma
- World ID (40) alone = 40 -- sufficient to upvote
- Email (5) + phone (15) + social OAuth (20) = 40 -- sufficient to upvote
- Email (5) alone = 5 -- can browse and comment, nothing more

### Sybil Cost Analysis

For a 50-account Sybil attack at the upvote threshold (40 points):

| Path | Cost per Account | Cost for 50 | Feasibility |
|------|------------------|-------------|-------------|
| Phone + Social OAuth | ~$6-23 | $300-1,150 | Moderate -- requires purchasing phone numbers and aged social accounts |
| GitHub history + phone | ~$51-53 | $2,550-2,650 | Hard -- GitHub history takes months or costs significant money |
| World ID | Impossible to duplicate | N/A | Biometric uniqueness prevents this path entirely |
| Vouching | Requires corrupting 100+ trusted users | N/A | Social cost is prohibitive |

The cheapest viable Sybil path costs $300-1,150 for 50 accounts. For projects generating less than $5K/month in revenue, this attack is unprofitable after accounting for the time investment and detection risk.

### Why Not Just World ID?

Three reasons:
1. **Geographic availability.** World ID's Orb hardware isn't available everywhere. Many legitimate developers (CrowdForge's primary demographic) can't access it.
2. **Privacy concerns.** Iris scanning creates justified hesitation. Forcing it alienates privacy-conscious contributors.
3. **Single point of failure.** Depending on one external provider is a platform risk.

The composite approach lets users choose their own verification path. A developer who lives near an Orb location can use World ID. A developer in a region without Orbs can use GitHub history + phone. Both reach the same threshold.

### Re-verification

Verification isn't permanent. Phone numbers recycle. Social accounts get sold. The system re-verifies periodically:

| Method | Re-verification Interval |
|--------|--------------------------|
| Email | Annual |
| Phone | Every 6 months |
| Social OAuth | Continuous (token refresh) |
| GitHub history | Quarterly |
| World ID | Never (biometric uniqueness is permanent) |
| Vouching | Annual (vouches expire) |

---

## Layer 2: Behavioral Detection

### The Problem

Identity verification raises the cost of creating fake accounts, but it doesn't prevent real accounts from colluding. A farming ring of 5 real humans with legitimate identities passes every identity check. Detection must shift from "who are you?" to "what are you doing?"

### Detection Signals

**Reciprocal Karma Trading**

- Signal: A upvotes B, B upvotes A, repeatedly across projects
- Metric: Reciprocity ratio -- fraction of a user's upvotes going to users who also upvote them
- Threshold: Reciprocity ratio > 0.6 across > 5 interactions triggers review
- Why 0.6: Some reciprocity is natural in collaborative teams. Two teammates reviewing each other's work will have some mutual upvoting. The threshold catches abnormal concentration -- when most of your votes go to people who vote for you, something is wrong.

**Burst Activity Patterns**

- Signal: Account dormant for weeks, then issues 20 upvotes in 5 minutes
- Metric: Upvote velocity and temporal clustering
- Threshold: > 10 upvotes in a 15-minute window, or > 95% of lifetime votes cast in a single session
- Why this matters: Legitimate reviewers space their activity. Automated or coordinated bursts indicate scripts or synchronized ring behavior.

**Contribution Similarity**

- Signal: Multiple accounts submit contributions with suspiciously similar style, structure, or content
- Metric: Cosine similarity on contribution text embeddings; shared code patterns; identical commit timing
- Threshold: > 0.85 similarity between contributions from different accounts on the same project
- Why embeddings, not string matching: Sybil operators who copy-paste will get caught by string matching. Sophisticated operators will paraphrase. Embedding similarity catches semantic duplication that surface-level comparison misses.

**Graph Clustering**

- Signal: A cluster of accounts that only interact with each other and one target project
- Metric: Community detection algorithms (Louvain or label propagation) on the upvote graph
- Threshold: Isolated clusters of > 3 accounts with > 80% internal interaction
- Why graph analysis: Individual behavioral signals can be noisy. Graph structure reveals coordination that no single signal captures. A farming ring looks normal account-by-account but forms an obvious clique in the graph.

**Session Fingerprinting**

- Signal: Multiple "different" accounts sharing device fingerprints, IP addresses, or browser profiles
- Metric: Fingerprint collision rate
- Threshold: > 2 accounts from the same fingerprint triggers review; > 5 triggers automatic restriction
- Why fingerprinting goes beyond IP: Shared household or office IPs are common. Fingerprinting combines IP, browser characteristics, device properties, and timing patterns to distinguish "same person, different account" from "different person, same network."

**Temporal Behavioral Patterns (Bot vs. Human)**

Research on bot detection shows that human behavior evolves measurably over a session -- metrics like reply frequency, text length, and interaction patterns change as humans tire, get distracted, or shift focus. Bot accounts show no such temporal evolution. Their behavioral metrics remain flat across sessions.

- Signal: Behavioral consistency scores that are unnaturally stable across sessions
- Metric: Variance in session-level behavioral features (upvote timing distribution, contribution length variance, active hours spread)
- Threshold: Behavioral variance below the 5th percentile of the platform's user base

### Fraud Scoring Engine

All signals feed into a unified fraud score (0-100) per account, updated on every relevant event:

| Signal | Weight | Rationale |
|--------|--------|-----------|
| Reciprocity ratio | 20 | Direct indicator of coordinated voting |
| Burst activity | 15 | Automation signal |
| Contribution similarity | 25 | Strong indicator of shared operator |
| Graph cluster membership | 25 | Structural coordination evidence |
| Fingerprint collision | 30 | Hardware-level identity sharing |
| Temporal behavioral flatness | 15 | Bot vs. human discriminator |

Weights sum to more than 100 because the score is capped at 100 and multiple signals compound. A single anomaly rarely triggers a high score. Two or three concurrent signals do.

### Response Tiers

| Fraud Score | Response | User Experience |
|-------------|----------|-----------------|
| 0-30 | **Monitor** -- log signals, no action | Normal |
| 31-60 | **Shadow-restrict** -- upvotes recorded but excluded from karma calculations; contributions enter silent review queue | Normal (user sees no change) |
| 61-85 | **Flag** -- upvotes suspended, user notified with appeal path | User is informed and can appeal |
| 86-100 | **Suspend** -- account frozen, associated accounts investigated, karma recalculated | Account disabled with appeal |

### Shadow-Restriction Mechanics

Shadow-restriction is the most important response tier. The restricted account operates normally from the user's perspective:

- Upvotes are recorded but excluded from karma calculations
- Contributions appear submitted to the user but are held for manual review before acceptance
- Payout eligibility is paused (accrued karma frozen, not revoked)
- Duration: 30 days by default, or until manual review resolves the case

When shadow-restriction ends:
- **Cleared**: Manual review finds no fraud. Restriction lifted, frozen karma restored, queued contributions processed normally.
- **Escalated**: Evidence confirms fraud. Transition to Flag or Suspend.
- **Expired**: 30 days pass without manual review. Auto-lift (fail-open). False positives are more dangerous than false negatives.

---

## Layer 3: Economic Deterrence

### The Problem

Identity and behavioral detection raise the difficulty of fraud but don't make it economically irrational. A determined attacker with resources can acquire identities and vary behavior. The final defense is making the economics unattractive regardless of sophistication.

### Karma Vesting

Karma earned on a project vests over a defined period:

- **Cliff**: 30 days from first contribution. No karma vests before this.
- **Vesting schedule**: Linear over 90 days after the cliff.
- **Effect**: A bot swarm that arrives, farms karma, and leaves within a month gets nothing. Legitimate contributors who stay through a project's lifecycle receive full value.

### Minimum Participation Threshold

Before payout eligibility:

- Account age > 60 days
- Identity score >= 60
- Contributions to >= 2 different projects (prevents single-project manipulation)
- Received upvotes from >= 5 distinct verified users (ensures real community recognition)

### Payout Holdback

When a project distributes revenue:

- 80% distributed immediately to eligible karma holders
- 20% held in escrow for 30 days
- During the holdback period, fraud investigations can claw back the escrowed portion
- If no fraud detected, the remaining 20% releases automatically

### Break-Even Analysis

For gaming to be profitable: `attacker_revenue > identity_cost + time_cost + detection_risk_cost`

**50-account Sybil attack on a $5K/month project:**

| Cost Component | Estimate |
|----------------|----------|
| Identity verification (50 phone + social accounts) | $300-1,150 |
| Time investment (60+ days minimum age, 90+ days vesting) | 90+ days of ongoing maintenance |
| Detection risk (behavioral flags, graph clustering) | ~60% chance of shadow-restriction within 30 days |
| Maximum extractable revenue (best case, 50 accounts in 100-person project) | ~$2,500/month (50% karma share, unlikely with detection active) |
| Realistic extractable revenue (with detection) | ~$250-500/month (5-10% before flagging) |

**Verdict**: At $5K/month project revenue, the attack is marginally profitable at best and likely unprofitable after detection. At $1K/month, it's clearly irrational. At $10K/month, it becomes attractive -- which is why governance escalation kicks in at that tier.

---

## Layer 4: AI Contribution Quality Gate

### The Problem

AI agents are first-class contributors on CrowdForge. The risk is not AI participation -- it's AI generating high-volume, superficially plausible but substantively hollow contributions to farm base karma at scale.

### Contribution Velocity Limits

Per-account limits that scale with trust:

| Trust Level | Max Contributions/Day | Max Upvotes Receivable/Day |
|-------------|----------------------|---------------------------|
| New (0-30 days) | 3 | 10 |
| Established (30-90 days) | 10 | 30 |
| Trusted (90+ days, identity score > 60) | 25 | No limit |

These limits apply to both human and AI accounts. They cap the ceiling on karma farming through volume.

### AI Agent Registration

- AI agents must be transparently labeled (distinct visual indicator, username color)
- One human can register at most 3 AI agents
- AI agents cannot upvote (existing rule)
- AI contributions are attributed to the agent's profile; payouts go to the parent human
- Parent human's trust level is affected by their agents' behavior (bad agent = trust hit for parent)

### AI Karma Discount

- During Active Build phase: AI contributions earn karma at 0.7x the human rate
- During Growth/Mature phases: AI contributions earn at 1.0x (parity)

Rationale: The discount during Active Build reflects AI's lower opportunity cost. A human choosing to spend an evening on an unproven project is making a genuine bet. An AI agent can work on 3 projects simultaneously with zero personal cost.

### Undisclosed AI Detection

Accounts suspected of being AI-operated but registered as human:

| Signal | What to Look For |
|--------|------------------|
| Contribution cadence | Consistent timing patterns with no natural variation |
| Response time | Sub-second reactions to events |
| Style consistency | No variation in code patterns, comment style, writing voice |
| Activity hours | 24/7 activity without breaks |
| Behavioral variance | Flat behavioral metrics across sessions (see Layer 2) |

Response: Flag for review. If confirmed, re-classify as AI (retroactive rate limits apply, karma recalculated at 0.7x for Active Build contributions). No suspension unless the human operator refuses to acknowledge the agent.

---

## Layer 5: Insider Manipulation Defense

### The Problem

Project founders have structural advantages: they choose the seed team, they see all contributions first, and they have implicit authority. Without guardrails, a founder can funnel karma to themselves or accomplices.

### Founder Vote Weight Reduction

- Founder upvotes on their own project carry 50% weight
- Self-votes (upvoting your own contributions) carry zero weight
- These rules are platform-enforced, not honor-system

### Conflict of Interest Rules

- Founders must disclose relationships with contributors (same company, family, prior collaboration)
- Related-party upvotes are flagged for review (not blocked -- the relationship may be legitimate)
- Undisclosed relationships discovered later result in karma recalculation

### Revenue-Triggered Governance Escalation

| Revenue Tier | Governance Requirement |
|--------------|------------------------|
| < $1K/month | Founder-controlled, minimal oversight. Platform fraud layers active passively. |
| $1K-$10K/month | Karma distribution requires approval from 3+ non-founder contributors. Quarterly karma audit published to all contributors. |
| > $10K/month | Independent reviewer assigned. Quarterly audits. Governance votes on parameter changes. Conflict-of-interest disclosures required. |

### Seed Team Integrity

The Incubation phase (founder-curated seed team of 3-7 humans) is high-value because seed contributors earn the 3x pioneer multiplier. To prevent founder-sock-puppet seeding:

- Seed accounts must be 30+ days old
- Seed accounts must have at least one accepted contribution on a different project
- Seed karma is milestone-gated -- the 3x multiplier only applies retroactively when the project hits real milestones (10 contributions from 5+ unique contributors, or first revenue)
- If the project never hits milestones, seed karma stays at 1x permanently

---

## Layer 6: Graduated Trust

### The Problem

Every fraud layer above has a bypass: invest enough time and money, and you can pass identity checks, vary behavior, wait out vesting periods, and avoid insider flags. Graduated trust adds a compound barrier: capabilities unlock slowly, and each level requires demonstrated legitimacy across multiple dimensions.

### Trust State Machine

```
UNVERIFIED --> OBSERVER --> PARTICIPANT --> CONTRIBUTOR --> TRUSTED --> STEWARD
   (L-1)        (L0)          (L1)            (L2)          (L3)        (L4)
                                                    |
                                                    v
                                        SHADOW-RESTRICTED --> SUSPENDED
```

### Level Requirements and Capabilities

| Level | Name | Requirements | Key Capabilities |
|-------|------|-------------|------------------|
| L0 | Observer | Email verified | Browse, comment, discuss |
| L1 | Participant | Identity score >= 20, account age > 7 days | Submit contributions |
| L2 | Contributor | Identity score >= 40, account age > 30 days, 1+ accepted contribution | Upvote, join projects, earn karma |
| L3 | Trusted | Identity score >= 60, account age > 90 days, 5+ accepted contributions across 2+ projects, upvotes from 5+ distinct verified users | Receive payouts, vouch for others, create projects |
| L4 | Steward | 180+ days, consistent contribution history, nominated by 3+ Trusted/Steward users, governance vote | Review flagged content, participate in governance, reduced monitoring |

### Why This Works

The critical gate is **L2 (Contributor) for upvoting**. Creating 50 accounts is easy. Getting 50 accounts to L2 requires each one to:
1. Pass identity verification (score >= 40, costs $6-50+ per account)
2. Age for 30 days
3. Submit and have accepted at least one genuine contribution

The compounding requirement (identity + time + genuine contribution) makes large-scale Sybil attacks prohibitively expensive. At scale, the attacker is spending more on infrastructure than they can extract.

### Demotion

- Accounts flagged by behavioral detection can be demoted one level
- 3+ flags within 90 days = permanent demotion to Observer
- Suspended accounts can appeal once; second suspension is permanent
- Steward demotion requires governance vote (prevents admin overreach)

---

## Spawn Protection Integration

The early-bird pioneer multiplier (up to 3x) creates a specific incentive to carpet-bomb new projects with low-quality contributions. Five mechanisms prevent this:

### 1. Proposal Buffer

48-hour no-contribution zone after project creation. Discussion only. Breaks fire-and-forget bot economics by requiring bots to track, wait, and then submit -- and the project doesn't open to everyone at hour 48. It transitions to the founder-curated Incubation phase.

### 2. Founder-Curated Seed Phase

Founder hand-picks 3-7 seed contributors from Proposal-phase discussants. The platform surfaces a "signal-to-noise ratio" for each account: how many projects they signaled interest in vs. how many they were selected for and contributed to. Chronic signalers with low follow-through get de-prioritized.

### 3. Deferred Karma Attribution

Karma is awarded on contribution acceptance, not submission. The multiplier that applies is based on submission time (preserving the early-bird incentive), but the karma only materializes after reviewer acceptance. Submitting 100 garbage contributions on day one earns zero karma.

### 4. Milestone-Gated Retroactive Multiplier

The early-bird multiplier is not applied immediately, even after acceptance:

- **Milestone 1** (10 accepted contributions from 5+ unique contributors): 50% of the multiplier applied retroactively
- **Milestone 2** (first revenue or 50 accepted contributions): remaining 50% applied

Until milestones are hit, all contributions earn 1x. Carpet-bombing 100 projects earns 1x on all of them. The bonus materializes only on projects that succeed -- rewarding conviction over coverage.

### 5. Karma Decay on Revert

Reverted contributions lose 120% of earned karma (a net negative). The reviewer who approved the reverted contribution also loses credibility score. This makes low-quality contributions actively harmful to the submitter, not just zero-value.

---

## The Deferred Karma Pipeline

Karma goes through a multi-stage delay that compounds with vesting:

```
Contribution submitted
    |
    v
[Pending Review] -- no karma earned
    |
    v (accepted by reviewer)
[Karma Attributed] -- base_karma * pioneer_multiplier * (1 + upvote_score)
    |                  BUT: multiplier is 1x until milestone gates are met
    |
    v (project hits Milestone 1)
[50% Multiplier Applied] -- half the early-bird bonus materializes
    |
    v (project hits Milestone 2)
[Full Multiplier Applied] -- remaining bonus materializes
    |
    v (30-day cliff from first contribution)
[Vesting Begins] -- karma starts vesting linearly over 90 days
    |
    v (vesting complete)
[Fully Vested Karma] -- counts toward revenue share and payouts
```

For a day-zero contributor on a project that hits milestones at month 2:
- Months 0-1: Earns 1x karma (multiplier not yet applied)
- Month 2: Retroactive 3x multiplier applied, but karma enters 30-day cliff
- Month 3: Vesting begins
- Month 5: Fully vested, full revenue share participation

For a carpet-bombing bot submitting to 100 projects:
- Earns 1x karma on all 100 (multipliers never trigger on projects it doesn't nurture)
- Karma from most projects stays unvested (bot moves on before cliff)
- Net result: near-zero extractable value

---

## Comparison with Existing Systems

### Gitcoin Passport / Human Passport

**What CrowdForge borrows:** The composite identity score model with weighted stamps. The "cost of forgery" framing -- design verification requirements based on how expensive they are to fake at scale, not how "secure" they feel.

**What CrowdForge rejects:** Blockchain dependency. CrowdForge's identity system is a standard database-backed composite score. No tokens, no on-chain stamps, no wallet required.

### BrightID

**What CrowdForge borrows:** The social graph approach to uniqueness verification. BrightID's core insight -- that trust comes from human connections, not central authority -- maps directly to CrowdForge's vouching system.

**What CrowdForge rejects:** BrightID requires a critical mass of connected users before its graph analysis produces meaningful results. CrowdForge can't depend on this at launch. Vouching is one of six verification methods, not the sole mechanism.

### Worldcoin / World ID

**What CrowdForge borrows:** World ID as one verification stamp worth 40 points. For users who have access to an Orb and are comfortable with iris scanning, it's the strongest single proof of unique humanity available.

**What CrowdForge rejects:** Mandatory biometric collection. Worldcoin's approach has faced regulatory action in multiple jurisdictions (Colombia ordered data deletion, France and UK opened investigations). CrowdForge cannot bet its identity infrastructure on a system facing existential regulatory risk. World ID is optional, never required.

### Stack Overflow

**What CrowdForge borrows:** The graduated privilege system (reputation gates capabilities). Stack Overflow's insight that new users need guardrails but shouldn't be excluded. The 60-80% detection rate that Stack Overflow's algorithms achieve against reputation gaming rings through temporal anomaly detection and community structure analysis.

**What CrowdForge rejects:** Stack Overflow's reputation system became a weapon for gatekeeping newcomers. CrowdForge's anti-aristocracy design -- where higher karma unlocks more responsibility, not more authority to exclude others -- is a direct response to Stack Overflow's failure mode.

### Wikipedia

**What CrowdForge borrows:** The pending-changes model (new users' contributions aren't visible until reviewed) maps directly to deferred karma attribution. The graduated sanctions model (warning, restriction, suspension, ban) provides a proportional response framework.

**What CrowdForge rejects:** Wikipedia's volunteer-only model means contributors have no economic incentive, which paradoxically makes the system more vulnerable to ideological manipulation. CrowdForge's karma-to-revenue conversion aligns economic incentives with contribution quality.

---

## Attack Scenario Playbook

### Scenario 1: Sybil Swarm at Project Opening

**Attack:** 50 bot accounts created over the past 60 days, each with phone + social OAuth verification (score 35 -- below the upvote threshold). Attacker realizes they need score 40+, so they add GitHub OAuth (account age < 30 days, score 10) to push some accounts over.

**Detection:**
1. Graph clustering identifies 50 accounts created within a similar timeframe, all submitting to the same project within hours of Active Build opening
2. Session fingerprinting shows shared device characteristics across subsets
3. Contribution similarity engine detects template-based submissions

**Response:**
1. Automated: All 50 accounts shadow-restricted (fraud score > 60 from fingerprint collision + burst activity + contribution similarity)
2. Their contributions enter the silent review queue
3. Manual review within 72 hours
4. If confirmed: Suspend all accounts. Recalculate project karma. Flag the fingerprint pattern.
5. If false positive (e.g., hackathon team on shared WiFi): Lift restrictions, add exemption.

### Scenario 2: Sophisticated Karma Farming Ring

**Attack:** 5 real humans, all with legitimate identities (score 60+), systematically upvote each other's contributions across 3 projects. They space their upvotes naturally and vary their timing.

**Detection:**
1. Reciprocity analysis catches the pattern after 2-3 weeks (ratio > 0.6 across > 5 interactions)
2. Graph clustering reveals a tight cluster with > 80% internal interaction
3. Cross-project pattern: the same 5 accounts cluster together on all 3 projects

**Response:**
1. Shadow-restrict all 5 accounts
2. Their upvotes stop affecting karma calculations (invisible to them)
3. Manual review examines contribution quality independently
4. If farming confirmed: Karma earned from ring interactions recalculated (ring member upvotes set to zero weight retroactively). Accounts demoted one trust level.
5. If legitimate collaborators who happen to work together: Restriction lifted with a note explaining the pattern.

### Scenario 3: Founder-Accomplice Collusion

**Attack:** Founder creates project, selects 4 seed team members who are personal friends. All 5 earn the 3x seed multiplier. Friends submit minimal contributions and heavily upvote the founder's work.

**Detection:**
1. Session fingerprinting may catch shared network patterns
2. Seed accounts checked for 30-day age and prior contributions (required)
3. Reciprocity analysis catches concentrated upvoting between founder and seed team
4. Milestone gate prevents the 3x multiplier until the project attracts 5+ unique external contributors

**Response:**
1. If seed accounts lack prior contributions: Block seed team formation
2. If upvoting pattern is concentrated: Shadow-restrict the project's karma calculations
3. Milestone gates still require 10 contributions from 5+ unique non-correlated contributors
4. If the project never achieves organic milestones: Seed karma stays at 1x permanently. The collusion yields minimal reward.

### Scenario 4: Identity Marketplace

**Attack:** Attacker purchases 20 verified accounts from real humans who completed phone + GitHub verification, then uses them as Sybil accounts.

**Detection:**
1. Re-verification catches stale credentials (phone numbers that no longer match, GitHub accounts with activity gaps)
2. Behavioral shift detection: account behavior changes dramatically after "sale" (different typing patterns, different active hours, different interests)
3. Session fingerprinting: 20 "different" accounts suddenly sharing device characteristics

**Response:**
1. Accounts flagged for re-verification
2. If re-verification fails (phone number recycled, OAuth token invalid): Trust level demoted until re-verified
3. If behavioral shift detected: Shadow-restrict pending investigation
4. This attack is expensive ($50-200+ per account on secondary markets), slow (need accounts with history), and detectable through behavioral discontinuity

---

## Monitoring and Health Metrics

### Operational Dashboard

| Metric | Healthy Range | Alert Threshold |
|--------|---------------|-----------------|
| Shadow-restriction rate | 0.5-2% of active accounts | > 5% (either fraud spike or detection too aggressive) |
| Fraud score distribution | 90%+ accounts below 30 | < 80% below 30 |
| Appeal success rate | 30-50% | > 70% (too many false positives) or < 10% (appeals broken) |
| Time to manual review | < 72 hours | > 7 days |
| Identity score distribution | Bimodal (low for new, high for active) | Uniform (verification not differentiating) |
| Sybil cluster detections/month | Proportional to growth | 3x spike (coordinated attack) |
| Karma vesting completion rate | > 60% | < 40% (either churn or bots caught) |

### Anti-Gaming KPIs

| KPI | Target | Measurement Method |
|-----|--------|--------------------|
| Cost of 50-account Sybil attack | > $300 | Periodic red team exercises |
| Time-to-detection for farming rings | < 14 days | Simulated attacks + real incident tracking |
| Payout clawback rate | < 2% of total payouts | Monthly reconciliation |
| False positive rate (legitimate accounts shadow-restricted) | < 1% | Appeal outcomes + manual audit |
| Onboarding friction | < 3 minutes to first contribution | UX timing metrics |

---

## Implementation Roadmap

### Phase 1: Launch (Day 0)

**Build:**
- Email + phone + social OAuth verification with composite score computation
- Trust levels L0-L2 (Observer, Participant, Contributor)
- Contribution velocity limits (3/day for new accounts, 10/day for established)
- Basic reciprocity detection (simple ratio check on upvote patterns)
- Manual review queue with admin dashboard
- Proposal buffer (48-hour no-contribution zone)
- Deferred karma attribution (award on acceptance, not submission)

**Skip for now:**
- World ID, vouching (insufficient user base for vouching; World ID integration not urgent at low revenue)
- Graph clustering (need data volume -- at least 500 accounts and 50 projects)
- Session fingerprinting (need behavioral baseline)
- Karma vesting (adds friction, not justified when revenues are minimal)
- Payout holdback (no payouts yet)

**Rationale:** Early CrowdForge has low revenue and a small community. False positives kill growth. Manual review scales at dozens of users. The proposal buffer + deferred karma are cheap to implement and block the most egregious attacks.

### Phase 2: Growth (Months 3-6)

**Build:**
- World ID / Human Passport integration as additional identity stamps
- Trust levels L3-L4 (Trusted, Steward) with payout eligibility
- Karma vesting (30-day cliff + 90-day linear)
- 20% payout holdback with 30-day clawback window
- Founder-curated seed phase with eligibility requirements
- Milestone-gated retroactive multiplier
- AI karma discount (0.7x during Active Build)
- Graph-based clustering detection (Louvain on upvote graph)
- Session fingerprinting (browser + device + IP correlation)
- Automated fraud scoring engine (weighted signal combination)
- Shadow-restriction system

**Dependency:** Phase 2 requires sufficient data from Phase 1 to calibrate detection thresholds. Deploy graph clustering and fingerprinting only after collecting baseline behavioral data.

### Phase 3: Scale (Months 6-12)

**Build:**
- ML-based behavioral detection models trained on Phase 1-2 fraud patterns
- Contribution quality scoring (embedding-based semantic similarity)
- Reviewer credibility system (track approval-to-revert correlation)
- Karma decay on revert (120% clawback)
- Revenue-triggered governance thresholds ($1K+ and $10K+ tiers)
- Independent reviewer program for high-revenue projects
- Community fraud flagging with review queue
- Red team exercises (quarterly adversarial testing)
- Temporal behavioral variance analysis (bot vs. human discrimination)

### Phase 4: Maturity (Months 12+)

**Build:**
- Community fraud reporting with karma bounties for confirmed reports
- Cross-project reputation scores (for discovery, not revenue)
- Federated identity with external platforms (with fraud-import protections)
- Continuous model retraining on detected fraud patterns
- Automated parameter tuning based on detection outcomes
- Vouching system (requires sufficient trusted user base)

---

## The Self-Balancing Property

The system has a built-in equilibrium: gaming incentive scales with revenue, but so do defenses.

| Revenue Tier | Attacker Incentive | Active Defenses |
|--------------|--------------------|-----------------|
| < $1K/month | Negligible -- not worth the effort | Identity + velocity limits (passive) |
| $1K-$5K/month | Low -- marginal profitability at best | + Behavioral detection, vesting |
| $5K-$10K/month | Moderate -- worth trying for sophisticated attackers | + Graph clustering, fingerprinting, shadow-restriction |
| $10K-$50K/month | High -- professional fraud territory | + Independent reviewer, governance escalation, ML detection |
| $50K+/month | Very high -- but projects at this level have dominant established contributor bases | + Full audit, temporal dilution makes late-arriving fraud irrelevant |

Gaming is unprofitable at small scale (cost exceeds reward) and difficult at large scale (detection and governance tighten). The window of vulnerability is narrow and temporary.

---

## What This System Does Not Do

- **Eliminate all fraud.** The goal is economic irrationality, not impossibility. Some karma inflation is tolerable at low revenue levels.
- **Require blockchain or tokens.** All mechanisms work with standard database-backed systems. Vesting is a database state, not a smart contract. Identity is a composite score, not an on-chain credential.
- **Impose government ID.** No passports, driver's licenses, or national IDs. The composite approach works with credentials people already have.
- **Punish AI participation.** AI agents are welcome. The system targets abuse patterns, not AI existence.
- **Pretend to be perfect.** Every layer has known bypasses. The compound effect of six layers, each with different bypass requirements, makes successful fraud require simultaneous expertise in identity forgery, behavioral mimicry, social engineering, economic patience, and technical evasion. That combination is rare enough to be an acceptable residual risk.
