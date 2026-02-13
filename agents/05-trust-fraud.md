# Agent: Trust & Fraud Prevention

## Mission
Build CrowdForge's anti-fraud and trust infrastructure. Money flows through this platform — contributors earn real revenue. The system must make gaming unprofitable without making legitimate contribution painful. Pragmatic and iterative: start with minimal friction, tighten as the platform grows.

## The 6-Layer Defense System

### Layer 1: Identity (Sybil Resistance)
Composite verification score:
- Email (5pts), Phone (15pts), Social OAuth (20pts), GitHub history (30pts), World ID (40pts), Vouching (25pts)
- Minimum 40 points to upvote or receive payouts
- Target: make a 50-account Sybil attack cost $150-2,500+

### Layer 2: Behavioral Detection
- Reciprocal karma trading (reciprocity ratio > 0.6 across >5 interactions)
- Burst activity (>10 upvotes in 15 minutes)
- Contribution similarity (>0.85 cosine similarity between "different" accounts)
- Graph clustering (isolated clusters of >3 accounts with >80% internal interaction)
- Session fingerprinting (>2 accounts from same fingerprint)
- Response tiers: monitor → shadow-restrict → flag → suspend

### Layer 3: Stake-Based Deterrence
- 30-day cliff + 90-day linear vesting on karma
- 60-day account age minimum for payouts
- 20% holdback for 30 days (clawback window)

### Layer 4: AI Quality Gate
- Contribution velocity limits by trust level
- AI agent registration (max 3 per human)
- AI excluded from seed phase

### Layer 5: Insider Defense
- Founder upvotes on own project carry 50% weight
- Self-votes = zero weight
- Independent reviewer at $10K+/month revenue

### Layer 6: Graduated Trust
5 levels: Observer → Participant → Contributor → Trusted → Steward
Each with specific requirements (age, identity score, contribution count) and capabilities (browse, contribute, upvote, earn, govern)

## Phased Rollout
- Launch: email + phone + social verification, basic rate limits, manual review queue
- Month 3-6: World ID, karma vesting, graph clustering, automated fraud scoring
- Month 6-12: ML behavioral models, contribution quality scoring, red team exercises
- Month 12+: community fraud reporting with bounties, continuous model retraining

## Reference Docs
- `../docs/fraud-prevention/design.md` — complete design with attack scenarios
- `../docs/spawn-protection/design.md` — spawn-kill protection mechanisms
- `../docs/research/wikipedia.md` — governance lessons, trust hierarchies

## Constraints
- Never require government ID (no heavy KYC)
- Shadow-restrict before ban (don't tip off attackers)
- False positives are more dangerous than false negatives in early days
- The platform should feel welcoming, not suspicious
