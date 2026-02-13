# Platform Governance & Meta-Contribution

## The Sacrosanct Boundary

CrowdForge operates two completely separate governance tracks. Projects use free-flowing "Yes, and..." collaboration with peer review. The platform itself uses a stricter, multi-approval governance process. This separation exists because a compromised project affects one team; a compromised platform affects everyone.

| Dimension | Project Governance | Platform Governance |
|---|---|---|
| Proposal | Any contributor | Any contributor |
| Approval | Peer review + project founder | Core team quorum |
| Reward | Karma → revenue share | Privileges, cosmetics, hiring pipeline |
| Failure mode | One project diluted | Entire platform hijacked |
| Transparency | Project-level audit log | Public changelog + decision log |

---

## Platform Change Governance

### Core Team Structure

Borrowing from Wikipedia's graduated hierarchy rather than a flat democracy or top-down dictatorship:

| Role | Count | How Selected | Powers |
|---|---|---|---|
| **Maintainer** | Unlimited | Self-nominated, core team approved after sustained platform contributions | Submit platform PRs, triage issues |
| **Core Reviewer** | 5–15 | Nominated by existing core, 7-day community discussion, 75%+ consensus | Approve platform PRs, manage releases |
| **Steward** | 3–5 | Elected annually by core reviewers + maintainers, 2/3 majority | Security-critical approvals, emergency powers, governance parameter changes |

### Approval Requirements

Platform changes follow tiered approval based on blast radius:

| Change Category | Examples | Required Approvals |
|---|---|---|
| **Cosmetic / Docs** | UI copy, help text, non-functional CSS | 1 core reviewer |
| **Feature** | New contributor-facing functionality, API additions | 2 core reviewers |
| **System** | Karma formula changes, trust level thresholds, payout logic | 2 core reviewers + 1 steward |
| **Security-Critical** | Authentication, payment processing, fraud detection rules | 2 stewards + security audit |
| **Governance** | Changes to this governance process itself | All stewards + 7-day public comment period |

### The Self-Approval Prohibition

No contributor can approve their own platform PR at any tier. This is the primary defense against the "10 bots approve their own change" attack vector. Specifically:

- PR author is excluded from the approval count
- Approvers must have no relationship disclosure flags with the author (reuses the fraud prevention relationship graph)
- Approvals from accounts younger than 90 days on the core team carry 0 weight on system-tier or higher changes

### Public Changelog

Every merged platform change generates a public changelog entry containing:
- What changed (plain-language summary, not commit messages)
- Who proposed it and who approved it
- The approval tier that applied
- Link to the full discussion thread

Changelog is append-only and cryptographically signed. No entries can be deleted or modified after publication.

### Emergency Powers

Stewards can bypass normal approval for time-critical security incidents:
- Requires 2 stewards to agree independently (no single unilateral action)
- Emergency change must be retroactively reviewed within 72 hours
- If retroactive review fails, the change is reverted and goes through normal process
- All emergency actions are logged with elevated visibility in the public changelog

---

## Community Governance for Projects

### Dispute Resolution

Karma disagreements follow an escalation ladder modeled on Wikipedia's talk → mediation → arbitration pipeline (Ostrom's Principle 6: accessible, low-cost conflict resolution):

| Stage | Mechanism | Timeline | Resolution |
|---|---|---|---|
| **1. Direct** | Contributors discuss in project thread | 48 hours | Mutual agreement |
| **2. Mediation** | Neutral Level 4+ contributor from a different project mediates | 7 days | Mediator proposes resolution, both parties accept/reject |
| **3. Arbitration** | Panel of 3 independent reviewers (Level 4+, no karma in the disputed project) | 14 days | Binding decision with written rationale |
| **4. Platform Appeal** | Core reviewer reviews arbitration decision | 30 days | Can overturn only on procedural grounds, not on merit |

Dispute resolution is free at stages 1–2. Stage 3 requires a small karma escrow (returned to the prevailing party) to prevent frivolous arbitration.

### Project Sunset Voting

Projects can be archived (stopping new contributions and freezing karma) through community vote:
- Requires 2/3 majority of contributors who earned karma in the last 90 days
- Voting period: 14 days
- Founder gets a single veto that triggers a second vote; second vote is final
- Sunset freezes karma and revenue distribution at current ratios — no clawback

### Revenue-Tier Governance Thresholds

As projects generate more revenue, governance requirements escalate (aligned with fraud prevention's existing tier system):

| Revenue Tier | Governance Requirements |
|---|---|
| **< $1K/month** | Standard peer review, founder + contributors govern |
| **$1K–$10K/month** | 3+ non-founder contributors must approve karma-affecting decisions; quarterly karma distribution report published to all contributors |
| **$10K–$50K/month** | Independent reviewer assigned from platform's reviewer pool; quarterly audits of karma distribution; contributor council (top 5 karma holders + 2 randomly selected contributors) votes on project-level policy |
| **$50K+/month** | Full independent audit annually; contributor council expanded to 9; any contributor can trigger a governance review by collecting 20% of active contributors' signatures |

### Independent Reviewer Program

Experienced contributors (Level 4+, 180+ days, karma across 3+ projects) can apply to become independent reviewers:
- Reviewers are assigned to projects they have no karma stake in
- Compensation: platform cosmetics + "Independent Reviewer" badge + priority in hiring pipeline
- Reviewers rotate every 6 months to prevent capture
- A reviewer who holds karma in an assigned project is immediately disqualified and replaced

---

## Moderation System

### Content Moderation

Applicable to project discussions, pitch descriptions, contribution comments, and profile content:

| Content Type | Moderation Approach |
|---|---|
| **Spam** | Automated detection + community flagging; auto-hidden at 3 flags from Level 2+ users |
| **Plagiarism** | Contribution similarity check (>0.85 cosine threshold from fraud prevention); flagged for human review |
| **Harmful content** | Zero-tolerance for hate speech, harassment, doxxing; immediate removal by any Level 3+ moderator, reviewed within 24 hours |
| **Off-topic** | Community flags; hidden at 5 flags; author can edit and request restoration |

### Contribution Flagging

Contributors can flag contributions (not just content) for:
- **Quality concerns** — contribution doesn't meet project standards
- **Attribution disputes** — contribution appears copied from another contributor
- **Scope violations** — contribution doesn't match the project's stated goals

Flagged contributions enter a review queue. The contributor's karma from that contribution is held in escrow until resolution. Reviewers are Level 3+ contributors with karma in the same project but no direct relationship with either party.

### Appeal Process

Every moderation decision generates an appeal ticket:
- **Auto-moderation decisions** (spam filter, similarity detection): Appeal reviewed by a human moderator within 48 hours
- **Human moderation decisions**: Appeal reviewed by a different moderator of equal or higher level within 7 days
- **Steward moderation decisions**: Appeal reviewed by the full steward panel within 14 days

Appeals are limited to 2 per incident. The second appeal decision is final.

### Graduated Sanctions

Following Ostrom's Principle 5 and Wikipedia's proven escalation model:

| Level | Sanction | Trigger | Duration | Reversibility |
|---|---|---|---|---|
| **1. Warning** | Visible notice on profile | First minor violation | Permanent record, no functional impact | Auto-clears after 6 months of clean behavior |
| **2. Restriction** | Limited to existing projects, cannot join new ones | Repeated minor violations or single moderate violation | 30 days | Appealable after 15 days |
| **3. Suspension** | Cannot contribute, vote, or earn karma; existing karma frozen | Serious violation or 3+ restrictions in 12 months | 90 days | Appealable after 45 days |
| **4. Ban** | Account permanently disabled; karma redistributed to project pools | Egregious violation (fraud, harassment, platform manipulation) or 2+ suspensions | Permanent | Appealable once after 12 months to steward panel |

Sanctions are always identity-attached (the moderator who imposed them is visible to the sanctioned user). Anonymous punishment is forbidden — this is the core lesson from Stack Overflow's failure.

---

## Anti-Aristocracy Mechanics

Stack Overflow collapsed because high-reputation users weaponized moderation to gatekeep newcomers. CrowdForge prevents this through structural design, not cultural appeals:

### Privileges Open Doors, Never Close Them

Every capability unlocked by karma enables the holder to do more — never to prevent others from participating:

| Karma Level | Unlocks | Explicitly Does NOT Unlock |
|---|---|---|
| Level 2 | Upvoting, joining more projects | Ability to reject newcomer contributions |
| Level 3 | Payouts, governance participation | Ability to close or delete others' contributions |
| Level 4 | Independent reviewer eligibility, mediation | Unilateral moderation power |
| Steward | Platform governance participation | Ability to override project-level contributor decisions |

### Mentorship Tracking

High-karma contributors are measured on mentorship activity:
- Review-with-feedback rate: percentage of reviews where the reviewer left constructive comments
- Newcomer success rate: percentage of newcomers whose first contribution was reviewed by this person and who went on to make 3+ more contributions
- These metrics are visible on profiles and factor into core team nominations

### Anti-Gatekeeping Detection

The platform monitors for aristocratic behavior patterns:

| Signal | Detection | Response |
|---|---|---|
| High rejection rate on newcomer contributions | Contributor rejects >40% of first-time contributions over 30-day window | Warning + review of recent rejections by independent moderator |
| Downvote concentration | >30% of a contributor's downvotes target accounts younger than 30 days | Downvote privilege suspended pending review |
| Clique formation | Cluster analysis detects closed approval rings (same 3–5 people approving only each other) | Flag to independent reviewer; approval weight reduced for the cluster |
| Mentorship avoidance | Level 4+ contributor with zero review-with-feedback interactions over 90 days | Gentle nudge; sustained avoidance factors into governance eligibility |

### The Responsibility Principle

Higher karma = more responsibility, not more authority. Concretely:
- Steward-tier contributors are expected to mentor at least 2 newcomers per quarter
- Core reviewers who don't participate in dispute mediation when requested lose their reviewer status after 2 consecutive refusals
- Governance participation is a duty, not a privilege — inactive governance members are rotated out after 6 months

---

## Governance Evolvability

The governance system itself must be evolvable (Ostrom's Principle 3: those affected can modify the rules). Hardcoded rules become attack surfaces and participation barriers as the platform grows.

### Parameter Registry

All governance thresholds are stored in a public parameter registry, not hardcoded:

```
governance.approval.cosmetic.required_reviewers = 1
governance.approval.feature.required_reviewers = 2
governance.approval.system.required_reviewers = 2
governance.approval.system.required_stewards = 1
governance.sunset.majority_threshold = 0.667
governance.dispute.arbitration_panel_size = 3
governance.sanctions.restriction_duration_days = 30
governance.anti_gatekeeping.rejection_threshold = 0.40
```

Changes to this registry are governance-tier changes (all stewards + 7-day public comment).

### Governance Proposals

Any Level 4+ contributor can submit a Governance Evolution Proposal (GEP):
- 7-day public discussion period
- Requires endorsement from 5+ Level 3+ contributors to proceed to vote
- Vote requires 2/3 majority of all stewards + core reviewers
- Approved GEPs have a 30-day implementation window
- Each GEP includes a revert plan in case of unintended consequences

### Sunset Clause

Every non-core governance rule includes an expiration date (default: 12 months). Before expiration, the rule must be actively renewed through a lightweight review (1 steward + community temperature check). Rules that nobody renews are automatically deprecated. This prevents governance cruft accumulation.

---

## Transparency Infrastructure

All governance operates in the open (Ostrom's Principle 4: accountable monitors):

| Data | Visibility | Retention |
|---|---|---|
| Platform PR approvals | Public | Permanent |
| Moderation actions | Public (identity-attached) | Permanent |
| Dispute resolutions | Public (anonymized parties) | Permanent |
| Governance votes | Public (named votes) | Permanent |
| Sanction history | Visible to sanctioned user + moderators | Per sanction duration rules |
| Parameter changes | Public changelog | Permanent |
| Emergency actions | Public with elevated visibility | Permanent |
| Anti-gatekeeping flags | Visible to flagged user + reviewing moderator | 12 months |

### Audit API

A public, read-only API exposes:
- All governance decisions with full context
- Aggregate moderation statistics (actions per month, appeal rates, overturn rates)
- Parameter change history with diffs
- Anti-gatekeeping detection aggregate metrics (no individual identification)

This API enables the community to build independent monitoring tools, preventing the platform from marking its own homework.
