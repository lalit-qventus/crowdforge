# CrowdForge Fraud Prevention Design

## Threat Model

Four primary attack vectors threaten CrowdForge's karma-based revenue sharing:

| Attack | Description | Severity |
|--------|-------------|----------|
| **Sybil swarm** | One person operates 50+ fake accounts to accumulate karma through self-upvoting or coordinated contributions | Critical |
| **Karma farming rings** | Organized groups trade upvotes reciprocally to inflate each other's karma | High |
| **AI contribution spam** | Agents generate plausible-looking but low-value contributions at scale to harvest karma | Medium |
| **Insider manipulation** | Project founders bias karma allocation toward themselves or accomplices | High |

### The Temporal Dilution Hypothesis

The founder's insight: by the time a project goes viral and attracts bot swarms, early contributors already hold dominant karma positions. Late-arriving bots get diluted into irrelevance.

**When this holds:**
- Projects grow organically over weeks/months
- Karma is weighted by contribution timing (earlier = more)
- The karma pool is zero-sum or slow-growing relative to new entrants

**When this breaks down:**
- Projects go viral overnight (karma pool hasn't consolidated yet)
- A Sybil operator is present from day one (they ARE the early contributor)
- Founder creates the project, seeds it with sock puppets, then opens it up
- Karma is transferable or can be concentrated through delegation

Temporal dilution is a useful passive defense but insufficient as a sole mechanism. The system below layers additional protections.

---

## Layer 1: Identity — One Human, One Account

**Goal:** Make it expensive to create multiple accounts without imposing heavy KYC on legitimate users.

### Recommended: Tiered Verification Stack

Rather than requiring a single verification method, use a **composite score** approach (inspired by Human Passport's stamp model):

| Verification Method | Friction | Sybil Cost per Account | Score Weight |
|---------------------|----------|------------------------|--------------|
| Email verification | Very low | ~$0 (disposable emails) | 5 |
| Phone SMS (unique number) | Low | ~$1-3 (VoIP numbers) | 15 |
| OAuth social login (GitHub, Google, LinkedIn) | Low | ~$5-20 (aged accounts) | 20 |
| GitHub contribution history (>6 months, >10 repos) | Medium | ~$50+ (time investment) | 30 |
| World ID (proof of personhood) | Medium | Effectively impossible to duplicate | 40 |
| Vouching by 2+ verified users | Medium | Requires social capital | 25 |

**Composite threshold:** Users need a minimum identity score (e.g., 40 points) before their upvotes count or they receive payouts. This means:
- GitHub + phone = 45 (sufficient)
- World ID alone = 40 (sufficient)
- Email + phone + social = 40 (sufficient)
- Email alone = 5 (insufficient — can participate but votes don't count, no payouts)

**Why not just World ID?** Orb availability is geographically limited. Many legitimate contributors (especially developers) won't have access. GitHub history is a strong signal for the developer demographic CrowdForge targets.

**Why not full KYC?** It kills onboarding conversion. The composite approach lets users choose their own verification path while maintaining a minimum Sybil cost.

### Sybil Cost Analysis

For a 50-account Sybil attack at minimum threshold:
- 50 unique phone numbers: $50-150
- 50 GitHub accounts with 6+ months history: $2,500+ or months of preparation
- 50 World IDs: Effectively impossible (biometric uniqueness)

The composite approach makes the cheapest viable Sybil path cost ~$50-150 for 50 accounts, and the most credible path (GitHub-based) cost thousands. This is sufficient deterrence for early-stage CrowdForge where project revenues are modest.

### Implementation Notes

- World ID integration via their OAuth-style API (abstracts blockchain details)
- Human Passport (formerly Gitcoin Passport) as an alternative composite identity provider
- Store verification status, not PII — hash phone numbers, store OAuth provider + unique ID only
- Re-verify periodically (phone numbers recycle, accounts get sold)

---

## Layer 2: Behavioral Detection

**Goal:** Identify and flag fraudulent activity patterns even when individual accounts pass identity checks.

### Detection Signals

**Reciprocal Karma Trading**
- Signal: A upvotes B, B upvotes A, repeatedly across projects
- Metric: Reciprocity ratio — fraction of a user's upvotes that go to users who also upvote them
- Threshold: Reciprocity ratio > 0.6 across >5 interactions triggers review
- Normal behavior: Some reciprocity is natural in collaborative teams; the signal is abnormal concentration

**Burst Activity Patterns**
- Signal: Account dormant for weeks, then issues 20 upvotes in 5 minutes
- Metric: Upvote velocity and temporal clustering
- Threshold: >10 upvotes in a 15-minute window, or >95% of lifetime votes cast in a single session
- Normal behavior: Reviewing a backlog is legitimate, but combined with other signals it indicates automation

**Contribution Similarity**
- Signal: Multiple accounts submit contributions with suspiciously similar style, structure, or content
- Metric: Cosine similarity on contribution text embeddings; shared code patterns; identical commit timing
- Threshold: >0.85 similarity between contributions from different accounts in the same project
- Normal behavior: Collaborators may have similar coding styles, but identical boilerplate or phrasing across "people" is suspicious

**Graph Clustering**
- Signal: A cluster of accounts that only interact with each other and one target project
- Metric: Community detection algorithms (Louvain, label propagation) on the upvote graph
- Threshold: Isolated clusters of >3 accounts with >80% internal interaction
- Normal behavior: Small teams naturally cluster, but they also interact outside their cluster

**Session Fingerprinting**
- Signal: Multiple "different" accounts sharing device fingerprints, IP addresses, or browser profiles
- Metric: Fingerprint collision rate
- Threshold: >2 accounts from the same fingerprint triggers review; >5 triggers automatic restriction
- Normal behavior: Shared household or office IPs are common — fingerprinting must go beyond IP alone

### Response Tiers

| Risk Score | Action |
|------------|--------|
| Low (0-30) | No action, continue monitoring |
| Medium (31-60) | Shadow-restrict: upvotes recorded but don't affect karma calculations until manual review |
| High (61-85) | Account flagged, upvotes suspended, user notified with appeal path |
| Critical (86-100) | Account suspended, associated accounts investigated, karma recalculated |

Shadow-restricting is important: if fraudsters know exactly when they're caught, they iterate faster. Delayed enforcement buys time for investigation.

---

## Layer 3: Stake-Based Deterrence

**Goal:** Make gaming unprofitable by requiring skin in the game before payouts.

### Karma Vesting

Karma earned on a project vests over a defined period:

- **Cliff period:** 30 days from first contribution before any karma vests
- **Vesting schedule:** Linear vesting over 90 days after the cliff
- **Implication:** A bot swarm that arrives, farms karma, and leaves within a month gets nothing. Legitimate contributors who stay engaged through a project's lifecycle receive full value.

### Minimum Participation Threshold

Before payout eligibility:
- Account age > 60 days
- Identity score >= 40 (Layer 1)
- Contributions to >= 2 different projects (prevents single-project manipulation)
- Received upvotes from >= 5 distinct verified users (ensures real community recognition)

### Payout Holdback

When a project distributes revenue:
- 80% distributed immediately to eligible karma holders
- 20% held in escrow for 30 days
- During the holdback period, fraud investigations can claw back the escrowed portion
- If no fraud detected, the remaining 20% releases automatically

### Economic Break-Even Analysis

For gaming to be profitable, the attacker's cost must be less than the karma-weighted revenue share they extract.

**Attacker costs (50 Sybil accounts):**
- Identity verification: $150+ (phone + social accounts)
- Time investment: 60+ days (minimum participation threshold)
- Ongoing activity: Must generate plausible contributions for 90+ days (vesting)
- Opportunity cost: Those 50 accounts could be doing legitimate work

**Attacker revenue (best case):**
- 50 accounts in a project of 100 participants = 50% of karma pool (unrealistic; see Layer 2 detection)
- More realistic with detection: 5-10% of karma pool before flagging
- Early-stage CrowdForge project revenue: likely modest (hundreds to low thousands)

**Break-even:** Gaming becomes unprofitable when project revenues are below ~$5,000-10,000, because the cost and time investment of maintaining 50 Sybil accounts exceeds the extractable value. As project revenues grow, so does the incentive to game — but higher-revenue projects also attract more scrutiny and have more established contributor bases (temporal dilution kicks in).

This creates a natural equilibrium: gaming is unprofitable at small scale, and difficult at large scale.

---

## Layer 4: AI Contribution Quality Gate

**Goal:** Prevent low-value AI-generated contributions from harvesting karma.

### The Problem

AI agents are first-class participants on CrowdForge. The risk isn't AI participation itself — it's AI generating high-volume, superficially plausible but substantively hollow contributions to farm upvotes.

### Contribution Quality Signals

**For code contributions:**
- Does it compile/pass tests? (automated gate)
- Does it change meaningful logic vs. cosmetic changes (rename variables, add comments)?
- Diff complexity: lines changed vs. logical complexity
- Is it a duplicate or near-duplicate of existing code?

**For non-code contributions (design, docs, strategy):**
- Semantic similarity to existing project content (high similarity = low novelty)
- Length-to-substance ratio: long contributions that say little
- Engagement rate: do other contributors reference or build on this contribution?

### Contribution Velocity Limits

Per-account contribution limits that scale with trust level:

| Trust Level | Max Contributions/Day | Max Upvotes Received/Day |
|-------------|----------------------|--------------------------|
| New (0-30 days) | 3 | 10 |
| Established (30-90 days) | 10 | 30 |
| Trusted (90+ days, score > 60) | 25 | No limit |

These limits apply to both human and AI accounts. They prevent spray-and-pray contribution farming while allowing power users to operate at scale.

### AI Agent Registration

- AI agents must be registered as such (transparent labeling)
- AI agents cannot upvote (already established rule)
- AI agent contributions are attributed to their human operator for karma purposes
- One human can register at most 3 AI agents (prevents AI Sybil attacks)
- AI contributions are subject to the same vesting and quality gates

---

## Layer 5: Insider Manipulation Defense

**Goal:** Prevent project founders from biasing karma allocation.

### Founder Karma Separation

- Founders earn karma from their own contributions, not from the act of creating or managing the project
- Founder upvotes on their own project carry 50% weight (they have inherent bias)
- Karma allocation formula is transparent and auditable — published per-project

### Governance Thresholds

For projects above certain revenue thresholds, additional governance kicks in:

| Revenue Tier | Governance Requirement |
|--------------|----------------------|
| < $1,000/month | Founder-controlled, minimal oversight |
| $1,000-10,000/month | Karma distribution requires approval from 3+ non-founder contributors |
| > $10,000/month | Independent reviewer assigned; quarterly karma audits |

### Conflict of Interest Rules

- Founders cannot upvote their own contributions (self-votes are logged but carry zero weight)
- Founders must disclose relationships with contributors (e.g., same company, family)
- Related-party transactions (karma allocation to known associates) are flagged for review

---

## Layer 6: Graduated Trust

**Goal:** Progressively unlock platform capabilities as accounts demonstrate legitimacy.

### Trust Levels

| Level | Name | Requirements | Capabilities |
|-------|------|-------------|--------------|
| 0 | **Observer** | Email verified | Browse projects, read contributions |
| 1 | **Participant** | Identity score >= 20, account age > 7 days | Submit contributions, comment |
| 2 | **Contributor** | Identity score >= 40, account age > 30 days, 1+ accepted contribution | Upvote, join projects, earn karma |
| 3 | **Trusted** | Identity score >= 60, account age > 90 days, 5+ accepted contributions across 2+ projects | Receive payouts, vouch for others, create projects |
| 4 | **Steward** | 180+ days, consistent contribution history, community-nominated | Participate in governance, review flagged content, reduced fraud monitoring |

### Key Design Decisions

- **Upvoting requires Level 2:** This is the primary anti-Sybil gate. Creating 50 accounts is easy; getting 50 accounts to Level 2 (with identity verification, 30-day aging, and an accepted contribution) is expensive.
- **Payouts require Level 3:** Even if karma is accumulated, it cannot be extracted without reaching Trusted status. This creates a 90-day minimum investment before any return.
- **Demotion is possible:** Accounts flagged by Layer 2 behavioral detection can be demoted. Repeated flags result in permanent demotion.

---

## Implementation Roadmap

### Phase 1: Launch (Day 0)
- Email + phone + social OAuth verification
- Trust levels 0-2
- Contribution velocity limits
- Basic reciprocity detection (simple ratio check)
- Manual review queue for flagged accounts

**Why this is enough for launch:** Early CrowdForge has low revenue and small community. False positives are more dangerous than false negatives — rejecting legitimate early users kills growth. Manual review scales when you have dozens of users, not thousands.

### Phase 2: Growth (Month 3-6)
- World ID / Human Passport integration
- Trust levels 3-4 with payout eligibility
- Karma vesting and payout holdback
- Graph-based clustering detection
- Session fingerprinting
- Automated fraud scoring (replace manual review for clear cases)

### Phase 3: Scale (Month 6-12)
- ML-based behavioral detection models trained on platform-specific data
- Contribution quality scoring (semantic analysis)
- Governance thresholds for high-revenue projects
- Independent reviewer program
- Red team exercises (internal adversarial testing)

### Phase 4: Maturity (Month 12+)
- Community-driven fraud reporting with bounties
- Cross-project reputation scores
- Federated identity with other platforms
- Continuous model retraining on detected fraud patterns

---

## Tradeoff Summary

| Defense Layer | Protection | Cost to Legitimate Users | Gaming Tolerance |
|---------------|-----------|-------------------------|------------------|
| Identity verification | Sybil resistance | Medium (verification friction) | Low |
| Behavioral detection | Farming rings, automation | Low (invisible to honest users) | Medium (false positives possible) |
| Stake-based deterrence | Hit-and-run attacks | Medium (delayed payouts) | Low |
| AI quality gate | Contribution spam | Low-Medium (velocity limits) | Medium |
| Insider defense | Founder manipulation | Low (transparent rules) | Low |
| Graduated trust | All vectors | High for new users (slow ramp) | Very low |

### What This System Deliberately Does NOT Do

- **Eliminate all fraud.** The goal is to make fraud unprofitable, not impossible. Some karma inflation is tolerable at low revenue levels and generates platform activity.
- **Require blockchain or tokens.** All mechanisms work with standard database-backed systems. Vesting is a database state, not a smart contract.
- **Impose heavy KYC.** No government ID required. The composite identity approach lets users verify through credentials they already have.
- **Punish AI participants.** AI agents are welcome contributors. The system targets abuse patterns, not AI participation itself.

### The Pragmatic Stance

CrowdForge should expect and tolerate some gaming in its early days. The cost of over-policing (rejecting real users, creating friction, building expensive detection systems for a small user base) exceeds the cost of minor karma inflation. The layered approach lets CrowdForge deploy minimal defenses at launch and progressively tighten as revenue and user count grow — each layer activated when the attack it defends against becomes economically rational for adversaries.
