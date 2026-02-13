# CrowdForge Trust & Fraud Prevention System

The integrated defense infrastructure for CrowdForge. This document synthesizes the fraud prevention layers, spawn-kill protection mechanisms, and governance principles from Wikipedia/Ostrom research into a single operational system.

Companion documents: [`design.md`](./design.md) (fraud layer details), [`../spawn-protection/design.md`](../spawn-protection/design.md) (spawn mechanics), [`../research/wikipedia.md`](../research/wikipedia.md) (governance research).

---

## System Philosophy

Three constraints govern every decision:

1. **False positives are worse than false negatives** — Rejecting a real contributor costs more than tolerating mild gaming. Especially in early days when every contributor is precious.
2. **Shadow-restrict, never tip off** — Fraudsters who know they're caught iterate faster. Delayed, invisible enforcement buys investigation time.
3. **Make gaming unprofitable, not impossible** — Perfect fraud prevention doesn't exist. The goal is economic: the cost of cheating exceeds the reward.

The system follows Ostrom's commons governance: graduated sanctions, community monitoring, conflict resolution pipelines, and rules that emerge from participants rather than being imposed top-down.

---

## Trust State Machine

Every account on CrowdForge exists in exactly one trust state at any time. Transitions are triggered by verifiable conditions — never by subjective judgment alone.

### States

```
                    ┌──────────────────────────────────────────────────┐
                    │                                                  │
                    ▼                                                  │
UNVERIFIED ──► OBSERVER ──► PARTICIPANT ──► CONTRIBUTOR ──► TRUSTED ──► STEWARD
   (L-1)        (L0)          (L1)            (L2)          (L3)        (L4)
                    │             │               │             │          │
                    └─────────────┴───────────────┴─────────────┴──────────┘
                                          │
                                          ▼
                              SHADOW-RESTRICTED ──► SUSPENDED
```

### Transition Requirements

| From → To | Trigger | Conditions |
|-----------|---------|------------|
| Unverified → Observer | Email verification | Valid email confirmed |
| Observer → Participant | Identity threshold | Identity score ≥ 20, account age > 7 days |
| Participant → Contributor | First acceptance | Identity score ≥ 40, account age > 30 days, 1+ accepted contribution |
| Contributor → Trusted | Cross-project proof | Identity score ≥ 60, account age > 90 days, 5+ accepted contributions across 2+ projects, upvotes from 5+ distinct verified users |
| Trusted → Steward | Community nomination | 180+ days, consistent contribution history, nominated by 3+ Trusted/Steward users, approved by governance vote |
| Any → Shadow-Restricted | Fraud score ≥ 31 | Behavioral detection triggers (Layer 2). Account holder is NOT notified. |
| Shadow-Restricted → Suspended | Fraud score ≥ 86 OR manual review confirms fraud | Account holder IS notified with appeal path. Associated accounts investigated. |
| Shadow-Restricted → Previous State | Manual review clears account | Fraud score drops below 31 after investigation. |

### Demotion Rules

- Accounts flagged by behavioral detection can be demoted one level
- Repeated flags (3+ within 90 days) result in permanent demotion to Observer
- Suspended accounts can appeal once. Second suspension is permanent.
- Steward demotion requires governance vote (prevents admin overreach — Ostrom principle #7)

### Capabilities by Trust Level

| Capability | Observer | Participant | Contributor | Trusted | Steward |
|-----------|----------|-------------|-------------|---------|---------|
| Browse projects | ✓ | ✓ | ✓ | ✓ | ✓ |
| Comment/discuss | ✓ | ✓ | ✓ | ✓ | ✓ |
| Submit contributions | | ✓ | ✓ | ✓ | ✓ |
| Upvote | | | ✓ | ✓ | ✓ |
| Join projects | | | ✓ | ✓ | ✓ |
| Earn karma | | | ✓ | ✓ | ✓ |
| Receive payouts | | | | ✓ | ✓ |
| Vouch for others | | | | ✓ | ✓ |
| Create projects | | | | ✓ | ✓ |
| Review flagged content | | | | | ✓ |
| Participate in governance | | | | | ✓ |
| Reduced fraud monitoring | | | | | ✓ |

---

## Unified Defense Matrix

The system layers 6 fraud prevention layers with 5 spawn protection mechanisms. Each defense targets specific attack vectors. No single layer is sufficient alone; the compound effect is what makes gaming unprofitable.

### How Layers Interact

```
IDENTITY (L1) ──────────────────────────────────────────────────► Sybil cost barrier
     │
     ├──► GRADUATED TRUST (L6) ──────────────────────────────────► Capability gating
     │         │
     │         ├──► SPAWN PROTECTION ────────────────────────────► Early-phase defense
     │         │     ├── Proposal buffer (48h no-contribution zone)
     │         │     ├── Founder-curated seed (3-7 humans only)
     │         │     ├── Deferred karma (award on acceptance)
     │         │     ├── Milestone-gated multiplier (retroactive)
     │         │     └── Karma decay on revert (120% clawback)
     │         │
     │         └──► AI QUALITY GATE (L4) ────────────────────────► Volume throttling
     │               ├── Velocity limits by trust level
     │               ├── AI registration (max 3 per human)
     │               └── AI excluded from seed phase
     │
     ├──► BEHAVIORAL DETECTION (L2) ─────────────────────────────► Pattern recognition
     │     ├── Reciprocal karma trading
     │     ├── Burst activity
     │     ├── Contribution similarity
     │     ├── Graph clustering
     │     └── Session fingerprinting
     │
     ├──► STAKE-BASED DETERRENCE (L3) ───────────────────────────► Economic barriers
     │     ├── 30-day cliff + 90-day linear vesting
     │     ├── 60-day account age for payouts
     │     └── 20% holdback for 30 days
     │
     └──► INSIDER DEFENSE (L5) ──────────────────────────────────► Governance checks
           ├── Founder upvotes at 50% weight
           ├── Self-votes at zero weight
           └── Independent reviewer at $10K+/month
```

### Attack Vector Coverage

| Attack | Primary Defense | Secondary Defense | Tertiary Defense |
|--------|----------------|-------------------|-----------------|
| 50-account Sybil swarm | Identity (L1): $150-2,500 cost | Graduated Trust (L6): 30-day age + accepted contribution per account | Behavioral (L2): graph clustering detects coordinated accounts |
| Karma farming ring | Behavioral (L2): reciprocity ratio > 0.6 | Stake (L3): vesting delays reward extraction | Graph clustering: isolated clusters with >80% internal interaction |
| AI contribution spam | AI Gate (L4): velocity limits + registration | Spawn: deferred karma + milestone gating | Behavioral (L2): contribution similarity detection |
| Carpet-bomb new projects | Spawn: proposal buffer + seed curation | Spawn: milestone-gated multiplier | Spawn: karma decay on revert |
| Founder sock-puppet seeding | Spawn: seed accounts need 30-day age + prior contributions | Insider (L5): self-votes zero weight | Behavioral (L2): session fingerprinting |
| Insider manipulation | Insider (L5): founder upvotes at 50% | Governance thresholds at revenue tiers | Independent reviewer at $10K+/month |
| Review manipulation | Self-review prohibition (platform-enforced) | Reviewer credibility decay on reverted approvals | Cross-account behavioral analysis |
| Undisclosed AI accounts | Behavioral (L2): cadence/style analysis | Identity (L1): periodic re-verification | Community flagging |

---

## Detection Pipeline

All behavioral signals feed into a unified fraud scoring engine. The engine produces a single fraud score (0-100) per account, updated on every relevant event.

### Signal Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        EVENT STREAM                              │
│  (upvotes, contributions, logins, sessions, reviews)            │
└──────────────┬──────────────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────────────┐
│                    SIGNAL EXTRACTORS                              │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────┐      │
│  │ Reciprocity  │  │ Burst        │  │ Similarity        │      │
│  │ Analyzer     │  │ Detector     │  │ Engine            │      │
│  │              │  │              │  │ (embeddings)      │      │
│  │ ratio > 0.6  │  │ >10 votes/   │  │ cosine > 0.85     │      │
│  │ across >5    │  │  15 min      │  │ between accounts  │      │
│  │ interactions │  │              │  │                   │      │
│  └──────┬───────┘  └──────┬───────┘  └────────┬──────────┘      │
│         │                 │                    │                  │
│  ┌──────┴───────┐  ┌──────┴───────┐                              │
│  │ Graph        │  │ Fingerprint  │                              │
│  │ Clusterer    │  │ Matcher      │                              │
│  │              │  │              │                              │
│  │ >3 accounts  │  │ >2 accounts  │                              │
│  │ >80% internal│  │ same print   │                              │
│  └──────┬───────┘  └──────┬───────┘                              │
│         │                 │                                      │
└─────────┴─────────────────┴──────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────────────┐
│                    FRAUD SCORING ENGINE                           │
│                                                                  │
│  Weighted combination of all signals:                            │
│                                                                  │
│  fraud_score = Σ(signal_weight * signal_value)                   │
│                                                                  │
│  Signal weights (Phase 1 — hand-tuned):                          │
│  ┌────────────────────────────┬────────┐                         │
│  │ Reciprocity ratio          │  20    │                         │
│  │ Burst activity             │  15    │                         │
│  │ Contribution similarity    │  25    │                         │
│  │ Graph cluster membership   │  25    │                         │
│  │ Fingerprint collision      │  30    │                         │
│  └────────────────────────────┴────────┘                         │
│                                                                  │
│  Capped at 100. Signals are normalized to [0, 1] before         │
│  weighting. Multiple signals compound — a single anomaly         │
│  rarely triggers high scores alone.                              │
└──────────────┬───────────────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────────────┐
│                    RESPONSE ROUTER                                │
│                                                                  │
│  Score 0-30:   MONITOR (log, no action)                          │
│  Score 31-60:  SHADOW-RESTRICT (upvotes don't count,            │
│                contributions queued, user not notified)           │
│  Score 61-85:  FLAG (upvotes suspended, user notified,          │
│                appeal path provided)                             │
│  Score 86-100: SUSPEND (account frozen, associated accounts     │
│                investigated, karma recalculated)                 │
└──────────────────────────────────────────────────────────────────┘
```

### Shadow-Restriction Mechanics

Shadow-restriction is the system's most important response tier. The restricted account continues to operate normally from the user's perspective, but:

- **Upvotes are recorded but excluded** from karma calculations
- **Contributions enter a silent review queue** — they appear submitted to the user but are held for manual review before acceptance
- **Payout eligibility is paused** — accrued karma is frozen (not revoked) pending investigation
- **Duration**: 30 days by default, or until manual review resolves the case
- **The user sees no indication** of restriction. Their dashboard, karma display, and activity all appear normal.

This is critical: if attackers can detect when they're caught, they iterate their tactics. Shadow-restriction creates an information asymmetry that favors the platform.

### When Shadow-Restriction Ends

- **Cleared**: manual review finds no fraud → restriction lifted, frozen karma restored, queued contributions processed normally
- **Escalated**: evidence confirms fraud → transition to Flag or Suspend
- **Expired**: 30 days pass without manual review → auto-lift (fail-open; false positives are more dangerous than false negatives)

---

## Spawn Protection Integration

Spawn protection mechanisms operate specifically during the early project lifecycle. They complement the 6-layer fraud system by hardening the phase when gaming incentives are highest (the early-bird karma multiplier).

### Project Lifecycle × Trust System Interaction

| Project Phase | Duration | Who Can Participate | Trust Level Required | Karma Multiplier | Fraud Layers Active |
|--------------|----------|--------------------|--------------------|-----------------|-------------------|
| **Proposal** | 0-48h | Anyone (discussion only) | Observer (L0) | None (0x) | L1 (identity for voting) |
| **Incubation** | 48h-~2wk | Founder-curated seed (3-7) | Contributor (L2), 30+ day age, prior accepted contribution | 3x (retroactive, milestone-gated) | L1, L2, L5 |
| **Active Build** | Weeks 2-8 | Anyone | Participant (L1) to contribute, Contributor (L2) to upvote | 2x → 1.5x (decaying) | All 6 layers |
| **Growth** | Months 2-6 | Anyone | Participant (L1)+ | 1x | All 6 layers |
| **Mature** | 6+ months | Anyone | Participant (L1)+ | 1x (revenue share active) | All 6 layers + governance thresholds |

### Deferred Karma × Vesting Interaction

Karma goes through a two-stage delay pipeline:

```
Contribution submitted
        │
        ▼
[Pending Review] ──── no karma earned yet
        │
        ▼ (accepted by reviewer)
[Karma Attributed] ── base_karma * pioneer_multiplier * (1 + upvote_score)
        │              BUT: multiplier is 1x until milestone gates are met
        │
        ▼ (project hits milestone 1: 10 contributions from 5+ unique contributors)
[50% Multiplier Applied] ── half the early-bird bonus materializes
        │
        ▼ (project hits milestone 2: first revenue or 50 accepted contributions)
[Full Multiplier Applied] ── remaining bonus materializes
        │
        ▼ (30-day cliff from first contribution)
[Vesting Begins] ── karma starts vesting linearly over 90 days
        │
        ▼ (vesting complete)
[Fully Vested Karma] ── counts toward revenue share and payouts
```

For a day-zero contributor on a project that hits milestones at month 2:
- Months 0-1: Earns 1x karma (multiplier not yet applied)
- Month 2: Retroactive 3x multiplier applied, but karma enters 30-day cliff
- Month 3: Vesting begins (25% immediately available)
- Month 5: Fully vested, full revenue share participation

For a carpet-bombing bot submitting to 100 projects:
- Earns 1x karma on all 100 (multipliers never trigger on projects it doesn't nurture)
- Karma from most projects stays unvested (bot moves on before cliff period)
- Net result: near-zero extractable value

### Reviewer Credibility System

Reviewers are the critical control point — they gate which contributions earn karma. The system must prevent reviewer capture.

- **Earning review rights**: 100+ project-specific karma
- **Self-review**: Prohibited (platform-enforced, not honor system)
- **Credibility score**: Starts at 100, adjustable range 0-200
  - Each approved contribution that survives 90 days without revert: +1
  - Each approved contribution later reverted: -10
  - Each approved contribution later flagged as fraud: -25
- **Credibility consequences**:
  - Score < 50: Review rights suspended, must rebuild through contributions
  - Score > 150: Reviews carry priority in the queue (fast-track acceptance)
- **Credibility is per-project**: Being a great reviewer on Project A gives no review rights on Project B

---

## Economic Deterrence Model

The system's economic defense creates a cost-benefit equation where gaming is unprofitable at every scale.

### Cost of Attack by Scale

| Attack Scale | Identity Cost | Time Investment | Detection Risk | Expected Revenue | Profitable? |
|-------------|--------------|-----------------|----------------|-----------------|-------------|
| 5 Sybil accounts (casual) | $15-50 | 60+ days (min age) | Low (small cluster) | ~1-2% of modest project revenue | No — time cost alone exceeds return |
| 50 Sybil accounts (serious) | $150-2,500 | 90+ days (vesting) | High (graph clustering, fingerprinting) | 5-10% before detection | No — identity cost + detection risk |
| 500 Sybil accounts (industrial) | $1,500-25,000 | 90+ days | Very high | Accounts suspended before payout | No — catastrophic cost |
| Karma farming ring (5 real people) | $0 (real accounts) | Ongoing | Medium (reciprocity analysis) | Modest share inflation | Marginal — social cost + shadow-restriction risk |
| AI contribution spam (3 agents) | $0 (registered) | N/A | Low (within rate limits) | Bounded by velocity limits + 0.7x discount | No — rate limits cap the ceiling |
| Insider manipulation (founder) | $0 | N/A | High above $10K/mo | 50% weight on self-project votes | Modest at low revenue, caught at high revenue |

### The Equilibrium

- **Below $5K/month project revenue**: Gaming costs exceed extractable value. The 6-layer system is overkill but operates passively.
- **$5K-$10K/month**: Marginal incentive to game. Behavioral detection and vesting provide sufficient deterrence.
- **Above $10K/month**: Governance thresholds activate. Independent reviewer assigned. The attack surface shrinks as scrutiny increases.
- **Above $50K/month**: Projects have established contributor bases with dominant karma positions. Temporal dilution makes late-arriving fraud economically irrelevant.

Gaming incentive scales with revenue, but so do defenses. This is the self-balancing property the system is designed for.

---

## Identity Verification Implementation

### Composite Score Computation

```
identity_score = Σ(verification_method_score)
```

| Verification | Score | Implementation | Re-verification |
|-------------|-------|---------------|-----------------|
| Email | 5 | Standard confirmation link. Store hash of address. | Annual |
| Phone SMS | 15 | Unique number via Twilio/similar. Store hash only. VoIP numbers flagged (reduced score: 5). | Every 6 months (numbers recycle) |
| Social OAuth (GitHub, Google, LinkedIn) | 20 | OAuth token exchange. Store provider + unique user ID. Account age < 30 days gets reduced score (10). | Continuous (token refresh) |
| GitHub contribution history | 30 | GitHub API: check account age > 6 months, contributions to > 10 repos. Store boolean "passed" + check date. | Quarterly |
| World ID | 40 | World ID OAuth-style API. Store verification status, not biometric data. | One-time (biometric uniqueness is permanent) |
| Vouching (2+ verified users) | 25 | Two Trusted (L3+) accounts vouch. Voucher's credibility is affected if vouchee is later flagged. | Vouches expire after 1 year (must be re-vouched) |

### Sufficient Combinations (≥ 40 points)

- GitHub history + phone = 45 ✓
- World ID alone = 40 ✓
- Email + phone + social = 40 ✓
- Social + GitHub history = 50 ✓
- Phone + social + vouching = 60 ✓

### Data Storage Principles

- **Store verification status, not PII**: Hash phone numbers, store OAuth provider + user ID, boolean flags for GitHub/World ID checks
- **No government ID, ever**: Kills onboarding conversion and creates a surveillance dynamic
- **Verification is additive**: Users can always add more verification methods to increase their score
- **Verification can be withdrawn**: Users can remove a verification method (score decreases accordingly)

---

## AI-Specific Trust Rules

AI agents are first-class contributors with specific guardrails that prevent scale-based gaming while preserving legitimate AI productivity.

### Registration and Limits

- AI agents must be registered as AI (transparent labeling, robot icon, distinct username color)
- One human can register at most 3 AI agents
- AI agent karma accrues to the agent's profile; payouts go to the parent human
- Parent human's trust level is affected by their agents' behavior (bad agent = trust hit for human)

### Phase-Specific Restrictions

| Project Phase | AI Participation | Rate Limit | Karma Rate |
|--------------|-----------------|------------|------------|
| Proposal | Can comment (flagged as AI) | N/A | 0x |
| Incubation (Seed) | **Excluded** | N/A | N/A |
| Active Build | Full participation | 5 contributions/project/day, max 3 Active Build projects simultaneously | 0.7x human rate |
| Growth | Full participation | 20 contributions/project/day, no cross-project limit | 1.0x (parity) |
| Mature | Full participation | 20 contributions/project/day | 1.0x |

### Undisclosed AI Detection

Accounts suspected of being AI-operated but registered as human:

**Behavioral signals:**
- Contribution cadence (consistent timing patterns, no natural variation)
- Response time (sub-second reactions to events)
- Style consistency (no variation in code patterns, comment style, writing voice)
- Activity hours (24/7 activity without breaks)

**Response:** Flag for review. If confirmed, the account is re-classified as AI (retroactive rate limits apply, karma recalculated at 0.7x for Active Build contributions). No suspension unless the human operator refuses to acknowledge the agent.

---

## Governance Integration

Drawing from Wikipedia's governance model and Ostrom's commons design principles, the trust system incorporates community self-governance at scale.

### Ostrom's Principles Applied

| Ostrom Principle | CrowdForge Implementation |
|-----------------|--------------------------|
| Clearly defined boundaries | Trust levels define who can do what. Identity verification defines who is real. |
| Rules match local conditions | Projects can customize parameters within platform bounds (pioneer_bonus, sales_karma_rate, etc.) |
| Collective-choice arrangements | Steward-level governance votes on platform policy changes. Per-project governance for revenue > $1K/month. |
| Community monitoring | Reviewer credibility system. Community fraud flagging. Contributor signal-to-noise ratios visible to founders. |
| Graduated sanctions | Monitor → shadow-restrict → flag → suspend. Demotions before bans. Appeals at every stage. |
| Conflict resolution | Project discussions → founder mediation → platform arbitration (for high-revenue projects). |
| Right to self-organize | Projects govern themselves within platform rules. Stewards participate in platform governance. |
| Nested governance | Account-level trust → project-level governance → platform-level policy. Each layer has its own rules and participants. |

### Revenue-Triggered Governance Thresholds

| Revenue Tier | Governance Requirement |
|-------------|----------------------|
| < $1,000/month | Founder-controlled. Minimal oversight. Platform fraud layers active passively. |
| $1,000-$10,000/month | Karma distribution requires approval from 3+ non-founder contributors. Quarterly karma audit published to contributors. |
| > $10,000/month | Independent reviewer assigned by platform. Quarterly audits. Governance votes on parameter changes. Conflict-of-interest disclosures required. |

### Wikipedia Lessons Embedded

**From Wikipedia's editor decline:**
- New contributors are most vulnerable in the first 15 days. The graduated trust system gives Observers immediate value (browse, comment, discuss) while protecting them from hostile gatekeeping.
- Contributor retention > contributor recruitment. The system rewards sustained engagement (vesting, dilution-based retention) over one-time contributions.

**From Wikipedia's barnstar system:**
- Non-monetary peer recognition drives motivation more than formal rewards. CrowdForge's upvote system serves this role — upvotes are peer recognition first, karma multipliers second.
- The framing matters: karma as "the community recognizing your value" (crowds in motivation) vs. "payment for work" (crowds out motivation).

**From Fandom's failure:**
- Value extraction without value sharing destroys communities. CrowdForge's 70% contributor pool is the antidote.
- Platform decisions must involve the community. Steward governance and per-project autonomy prevent the "Fandom exodus" dynamic.

**From the crowding-out research:**
- Never make base participation transactional. Contributors earn karma through work, not for work.
- Rewards should be retrospective and peer-originated. Revenue share follows contribution; it doesn't incentivize specific tasks.

---

## Monitoring and Metrics

### Health Dashboard (Operational)

| Metric | Healthy Range | Alert Threshold | What It Means |
|--------|---------------|-----------------|---------------|
| Shadow-restriction rate | 0.5-2% of active accounts | > 5% | Either fraud is spiking or detection is too aggressive (false positives) |
| Fraud score distribution | 90%+ accounts below 30 | < 80% below 30 | Widespread suspicious activity OR detection calibration drift |
| Appeal success rate | 30-50% of appeals upheld | > 70% (too many false positives) or < 10% (appeals broken) | Detection accuracy |
| Time to manual review | < 72 hours | > 7 days | Review queue is backing up; need more reviewers or automated triage |
| Identity score distribution | Bimodal (low for new users, high for active) | Uniform distribution | Verification isn't differentiating |
| Sybil cluster detections/month | Proportional to growth | 3x spike | Coordinated attack in progress |
| Karma vesting completion rate | > 60% of attributed karma fully vests | < 40% | Contributors are churning before vesting (too aggressive?) or bots are being caught (working as intended) |
| Reviewer credibility mean | 90-110 | < 70 or > 140 | Reviewer quality is degrading or credibility system is too lenient |

### Anti-Gaming KPIs (Strategic)

| KPI | Target | Measurement |
|-----|--------|-------------|
| Cost of 50-account Sybil attack | > $150 | Periodic red team exercises |
| Time-to-detection for karma farming rings | < 14 days | Simulated attacks + real incident tracking |
| Payout clawback rate | < 2% of total payouts | Monthly reconciliation |
| False positive rate (shadow-restrictions on legitimate accounts) | < 1% | Appeal outcomes + manual audit |
| Contributor onboarding friction score | < 3 minutes to first contribution | UX timing metrics |

---

## Implementation Roadmap

### Phase 1: Launch (Day 0)

**Goal: Minimal friction, basic protection, manual review.**

Build:
- Email + phone + social OAuth verification (identity score computation)
- Trust levels 0-2 (Observer, Participant, Contributor)
- Contribution velocity limits (3/day for new, 10/day for established)
- Basic reciprocity detection (simple ratio check on upvote patterns)
- Manual review queue for flagged accounts (admin dashboard)
- Proposal buffer (48-hour no-contribution zone)
- Deferred karma attribution (award on acceptance, not submission)
- AI rate limits (5/day/project, 3 simultaneous Active Build projects)

Skip for now:
- World ID, vouching (insufficient user base)
- Graph clustering (need data volume)
- Session fingerprinting (need baseline)
- Karma vesting (add friction later, not at launch)

**Rationale:** Early CrowdForge has low revenue and small community. False positives kill growth. Manual review scales at dozens of users. The proposal buffer + deferred karma are cheap to implement and block the most egregious attacks.

### Phase 2: Growth (Month 3-6)

**Goal: Automated detection, payout infrastructure, tighter gates.**

Build:
- World ID / Human Passport integration
- Trust levels 3-4 (Trusted, Steward) with payout eligibility
- Karma vesting (30-day cliff + 90-day linear)
- 20% payout holdback with 30-day clawback window
- Founder-curated seed phase
- Milestone-gated retroactive multiplier
- AI karma discount (0.7x during Active Build)
- Graph-based clustering detection (Louvain algorithm on upvote graph)
- Session fingerprinting (browser + device + IP correlation)
- Automated fraud scoring engine (weighted signal combination)
- Shadow-restriction system

**Dependency:** Phase 2 requires sufficient data from Phase 1 to calibrate detection thresholds. At least 500 accounts and 50 projects needed before graph clustering produces meaningful results.

### Phase 3: Scale (Month 6-12)

**Goal: ML-powered detection, quality scoring, governance.**

Build:
- ML-based behavioral detection models (trained on platform-specific fraud patterns from Phase 1-2)
- Contribution quality scoring (embedding-based semantic analysis for similarity detection)
- Reviewer credibility system (track approval → revert correlation)
- Karma decay on revert (120% clawback)
- Governance thresholds for high-revenue projects ($1K+ and $10K+ tiers)
- Independent reviewer program (for $10K+/month projects)
- Community fraud flagging with review queue
- Red team exercises (quarterly internal adversarial testing)

### Phase 4: Maturity (Month 12+)

**Goal: Community-driven enforcement, continuous improvement.**

Build:
- Community fraud reporting with bounties (Trusted+ users earn karma for confirmed fraud reports)
- Cross-project reputation scores for discovery (not revenue)
- Federated identity with external platforms (GitHub reputation import, with fraud-import protections)
- Continuous model retraining on detected fraud patterns
- Automated parameter tuning (adjust signal weights based on detection outcomes)
- Steward governance council for platform-level policy changes

---

## Attack Scenario Playbook

Concrete response procedures for each known attack pattern.

### Scenario 1: Sybil Swarm at Project Opening

**Detection:** Graph clustering identifies 20+ accounts created within 48 hours, all submitting to the same project within minutes of Phase 3 opening. Session fingerprinting shows shared device characteristics.

**Response:**
1. Automated: All 20+ accounts shadow-restricted (fraud score > 60 from fingerprint collision + burst activity)
2. Automated: Their contributions enter silent review queue (visible to submitter, held from project)
3. Manual: Fraud team investigates within 72 hours
4. If confirmed: Suspend all accounts. Recalculate project karma excluding their contributions. Flag the IP/fingerprint pattern for future detection.
5. If false positive (e.g., hackathon team on shared WiFi): Lift restrictions, add exemption note to account cluster.

### Scenario 2: Sophisticated Quality Gaming

**Detection:** Single operator runs 3 registered AI agents across multiple Active Build projects. Contributions are technically valid but shallow (reformatting, trivial documentation, cosmetic changes). Rate limits are respected.

**Response:**
1. Automated: AI rate limits cap output at 5/project/day during Active Build
2. Automated: 0.7x karma discount applies during Active Build
3. Project-level: Reviewers reject low-value contributions (minimum contribution thresholds)
4. If pattern persists: Contribution similarity engine detects template-based submissions across agents
5. Escalation: Parent human notified that agents are producing low-value work. If no improvement, AI registration privileges reduced to 1 agent.

### Scenario 3: Karma Farming Ring

**Detection:** 5 accounts with reciprocity ratio > 0.6 across > 5 interactions. Graph clustering shows isolated cluster with > 80% internal interaction.

**Response:**
1. Automated: All 5 accounts shadow-restricted
2. Their upvotes stop affecting karma calculations (invisible to them)
3. Manual: Review within 72 hours. Examine contribution quality independently.
4. If farming confirmed: Karma earned from ring interactions recalculated (ring member upvotes set to zero weight retroactively). Accounts demoted one trust level.
5. If legitimate collaborators: Restriction lifted. Note: some reciprocity is natural in teams — the threshold exists to catch abnormal concentration.

### Scenario 4: Founder-Attacker Collusion

**Detection:** Founder creates project, selects seed team. Seed team members have suspiciously correlated account creation dates, similar verification patterns, or shared session fingerprints with founder.

**Response:**
1. Automated: Seed accounts flagged for review (correlation detected)
2. Check: Do seed accounts have 30+ day age? Have prior accepted contributions on other projects? (Required by seed eligibility rules)
3. If accounts fail eligibility: Block seed team formation. Founder notified to select eligible contributors.
4. If accounts pass eligibility but correlation remains: Shadow-restrict the project's karma calculations. Milestone gates still apply — the project needs 10 contributions from 5+ unique non-correlated contributors to unlock multipliers.
5. If project never achieves organic milestone: Seed karma stays at 1x permanently. Founder's strategy fails economically.

---

## Open Questions

1. **Proposal buffer duration: 24 vs 48 hours?** 48 hours gives more room but may feel slow for time-sensitive ideas. Recommendation: founder-configurable with 24-hour minimum, 48-hour default.

2. **Cross-platform reputation import:** Should CrowdForge accept GitHub contribution history, Stack Overflow reputation, etc. to bootstrap new accounts past new-user restrictions? Pro: reduces friction for legitimate newcomers. Con: creates an import-fraud vector. Recommendation: accept as identity score boost only (GitHub history = 30 points), not as karma or trust level bypass.

3. **AI parity timeline:** The 0.7x AI discount during Active Build reflects AI's lower opportunity cost. As AI agents become more sophisticated, should parity come sooner? Recommendation: revisit at Phase 3 based on data about AI contribution quality vs. human contribution quality.

4. **Shadow-restriction transparency:** Current design: user is never told they're restricted. Alternative: tell users after restriction is lifted ("your account was under review for X days, no issues found"). Pro: builds trust. Con: reveals detection capability. Recommendation: notify after clearance only, not during restriction.

5. **Steward governance power:** Stewards can participate in platform governance. What prevents Steward capture (a small group of long-tenured users blocking change)? Recommendation: term limits on governance participation (2-year active terms, with re-nomination required) + minimum diversity requirements for governance quorum.
