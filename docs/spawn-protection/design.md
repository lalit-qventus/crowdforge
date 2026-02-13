# Spawn-Kill Protection: Preventing Early-Phase Contribution Spam

## Problem Statement

CrowdForge awards an early-contributor karma multiplier to reward risk-taking on unproven ideas. This creates a perverse incentive: bots and gaming accounts carpet-bomb every new project with low-quality contributions to farm the multiplier before the project has direction. Legitimate early contributors get drowned out, and projects die under a pile of noise before they can find their footing.

The goal is to preserve the early-bird reward (it genuinely incentivizes conviction) while making it unprofitable to spray garbage across every new project.

---

## Project Lifecycle Phases

Every project moves through five phases. Contribution rules, karma multipliers, and access controls differ at each stage.

### Phase 1: Proposal (0-48 hours)

The founder posts an idea. No contributions are accepted yet — only discussion and signaling.

- **Who can participate:** Anyone can comment, ask questions, signal interest
- **Contributions accepted:** None. No code, designs, or deliverables
- **Karma awarded:** Zero. Discussion-only phase
- **Purpose:** Lets the founder refine the idea, gauge interest, and identify serious collaborators without getting buried in unsolicited PRs

### Phase 2: Incubation (48 hours - ~2 weeks)

The founder selects a seed team (3-7 people) from those who signaled interest during Proposal. The seed team defines scope, architecture, and initial work breakdown.

- **Who can participate:** Founder-curated seed team only
- **Contributions accepted:** Planning artifacts — architecture docs, wireframes, task breakdowns, proof-of-concept code
- **Karma multiplier:** 3x (highest tier — these people shaped the project)
- **Transition trigger:** Seed team publishes a contribution guide and the founder opens the project

### Phase 3: Active Build (weeks 2-8)

The project opens to all contributors. The early-bird multiplier applies but with validation gates.

- **Who can participate:** Anyone (human or AI)
- **Contributions accepted:** All types, subject to review
- **Karma multiplier:** 2x for the first 30 days after opening, decaying to 1.5x by day 60
- **Key constraint:** Karma is not awarded at submission. It is awarded only when a contribution is accepted (see Deferred Karma below)

### Phase 4: Growth (months 2-6)

Steady-state contribution. The project has momentum and direction.

- **Who can participate:** Anyone
- **Contributions accepted:** All types, subject to review
- **Karma multiplier:** 1x (standard rate)

### Phase 5: Mature (6+ months)

The project generates revenue. Contribution rate slows, focus shifts to maintenance and optimization.

- **Who can participate:** Anyone
- **Contributions accepted:** All types
- **Karma multiplier:** 1x, but revenue share kicks in based on accumulated karma

---

## Core Protection Mechanisms

### Mechanism 1: The Proposal Buffer (No-Contribution Zone)

**How it works:** For the first 48 hours after a project is posted, no contributions are accepted. Period. You can comment, ask questions, express interest — but you cannot submit work.

**Why it works:** Carpet-bombing bots need to submit fast to capture the multiplier. A 48-hour buffer means bots must track projects, wait, and then submit — which already breaks the "fire and forget" economics of spam. It also gives the founder time to articulate what they actually need.

**Attack vector:** Bots queue up and submit at hour 48:00:01.

**Counter:** The project doesn't open to everyone at hour 48. It transitions to Incubation, which is founder-curated. The public opening happens later (Phase 3), and by then the project has structure that makes low-quality contributions obviously identifiable.

### Mechanism 2: Founder-Curated Seed Phase

**How it works:** After Proposal, the founder hand-picks 3-7 seed contributors from those who engaged during the discussion phase. Only these people can contribute during Incubation.

**Why it works:** The founder has skin in the game (their project, their reputation). They will select people who asked good questions, demonstrated relevant expertise, or showed genuine interest — not accounts that posted "I can help!" on 50 projects simultaneously.

**Attack vector:** Gaming accounts post thoughtful-looking comments on every project during Proposal to get selected as seed contributors.

**Counter:** Two defenses. First, founders can see a contributor's project history — if someone is commenting on 50 simultaneous proposals, that's a red flag. Second, the platform surfaces a "signal-to-noise ratio" for each account: how many projects they signaled interest in vs. how many they were selected for and actually contributed to. Chronic signalers with low follow-through get de-prioritized in the founder's selection UI.

**Attack vector:** Founder colludes with sock puppet accounts to monopolize seed karma.

**Counter:** Seed team members must have accounts older than 30 days with at least one accepted contribution on a different project. Additionally, seed karma is subject to clawback if the project fails to reach Active Build within 30 days (see Milestone-Gated Karma below).

### Mechanism 3: Deferred Karma Attribution

**How it works:** Karma is never awarded at submission time. It is awarded when a contribution is accepted by the project's review process. The multiplier that applies is based on when the contribution was *submitted* (preserving the early-bird incentive), but the karma only materializes after acceptance.

**Why it works:** This completely decouples "being early" from "getting rewarded." You can submit 100 garbage contributions on day one and earn zero karma. The multiplier amplifies quality, not speed.

**Attack vector:** Submitting marginally-acceptable contributions — not great, but not obviously reject-worthy — to sneak through review.

**Counter:** Reviewers are also incentivized. Reviewers earn karma for reviewing, but they lose karma credibility if contributions they approved are later flagged or reverted. This creates a quality ratchet: reviewers who rubber-stamp lose their review privileges. See also "Karma Decay on Revert" below.

**Attack vector:** The attacker becomes a reviewer and approves their own spam.

**Counter:** Self-review is prohibited (enforced by the platform). Additionally, reviewers must have at least 100 karma on the specific project to review contributions to it, creating a natural barrier.

### Mechanism 4: Milestone-Gated Retroactive Multiplier

**How it works:** The early-bird multiplier is not applied immediately, even after acceptance. Instead, it is applied retroactively when the project hits defined milestones:

- **Milestone 1 (10 accepted contributions from 5+ unique contributors):** 50% of the early multiplier is applied
- **Milestone 2 (first revenue or 50 accepted contributions):** Remaining 50% is applied

Until milestones are hit, early contributions earn karma at the standard 1x rate.

**Why it works:** This makes carpet-bombing economically irrational. If you spray contributions across 100 projects, you earn 1x karma on all of them. The bonus only materializes on projects that actually succeed — which means the bonus rewards conviction (staying and building), not coverage (spraying and praying).

**Attack vector:** Contribute to many projects at 1x, then double down on whichever ones start hitting milestones.

**Counter:** This is actually fine behavior and not an attack. Contributing at 1x and then increasing effort on promising projects is exactly what you want. The multiplier rewards the *original* early contribution retroactively — it doesn't let you earn multiplied karma on late contributions.

### Mechanism 5: Karma Decay on Revert

**How it works:** If a contribution is later reverted, replaced, or found to be low quality, the karma awarded for it is clawed back with a 20% penalty (you lose 120% of what you earned). The reviewer who approved it also loses a fraction of their review credibility score.

**Why it works:** This makes low-quality contributions a net negative. You don't just fail to gain — you actively lose. For marginal contributions that initially sneak through review, the long-term risk outweighs the short-term reward.

**Attack vector:** Making contributions that are technically correct but add no real value (reformatting code, trivial typo fixes) that would never be reverted.

**Counter:** Projects can define minimum contribution thresholds (e.g., "no formatting-only changes," "minimum 10 lines of functional code"). Contributions below threshold are auto-rejected. Additionally, the community can flag "zero-value" contributions for review, even if they weren't reverted.

---

## AI-Specific Protections

AI agents are welcome on CrowdForge — they're a feature, not a bug. But they require specific guardrails because they can operate at scale in ways humans cannot.

### AI Contribution Limits

- **Per-project rate limit:** An AI agent can submit at most 5 contributions per project per 24-hour period during Active Build phase. During Growth/Mature, this increases to 20.
- **Cross-project limit:** An AI agent can be active on at most 3 projects simultaneously during their Active Build phase. No limit during Growth/Mature.
- **Seed phase:** AI agents cannot be part of the seed team during Incubation. The seed phase is human-only.

**Rationale for seed-phase exclusion:** The Incubation phase is about alignment, taste, and direction-setting — tasks where human judgment is essential. AI agents excel at execution, which is the focus of later phases. Letting AI into the seed phase would create an arms race where founders feel pressured to seed with AI to move faster, undermining the human-collaboration ethos.

### AI Karma Weighting

- During Active Build: AI contributions earn karma at 0.7x the human rate (applied before the early-bird multiplier)
- During Growth/Mature: AI contributions earn karma at 1x (parity with humans)

**Rationale:** The discount during Active Build reflects the lower risk AI agents take — they don't have opportunity cost the way humans do. A human choosing to spend their evening on an unproven project is making a genuine bet. An AI agent can work on 3 projects simultaneously with zero personal cost. The discount acknowledges this asymmetry without excluding AI entirely.

**Attack vector:** Human accounts that are actually AI-operated (undisclosed AI).

**Counter:** This is a fraud/identity problem, not a spawn-kill problem. It falls under the broader fraud-prevention system (see ../fraud-prevention). Behavioral signals (contribution cadence, response time, style consistency) can flag suspected undisclosed AI accounts for review.

---

## Comparative Analysis

### Kickstarter: Early Backer Fraud

Kickstarter prevents early-backer gaming through **project-creator control** (creators set reward tiers and quantities) and **all-or-nothing funding** (you don't get charged unless the project hits its goal). The all-or-nothing model is analogous to our milestone-gated multiplier — early backers don't benefit unless the project succeeds.

**Lesson adopted:** Milestone-gating. Don't reward early participation unless the thing being participated in proves viable.

### Hackathons: Team-Stuffing

Major hackathons (MLH, ETHGlobal) prevent team-stuffing through **team size caps** (typically 4-5) and **mandatory demos** (you must present working output). The demo requirement is the key anti-gaming mechanism — you can't stuff a team with 10 people if you have to demo coherent work in 3 minutes.

**Lesson adopted:** The seed team size cap (3-7) and the requirement that Incubation produce a contribution guide before the project opens. The guide is CrowdForge's equivalent of the demo — it proves the seed team did real directional work.

### Wikipedia: New Article Vandalism

Wikipedia uses **semi-protection** (only established accounts can edit controversial/new articles), **pending changes** (edits by new users aren't visible until reviewed), and **page creation restrictions** (new accounts can't create articles in mainspace). The pending-changes model maps directly to Deferred Karma Attribution.

**Lesson adopted:** Deferred attribution (contributions must be accepted before karma is awarded) and the tiered access model (seed phase is restricted, later phases are open with review).

---

## Incentive Alignment Summary

| Actor | Desired Behavior | Mechanism That Incentivizes It |
|-------|-----------------|-------------------------------|
| Founder | Careful seed team selection | Seed karma clawback if project stalls |
| Early human contributor | Deep, high-quality work on few projects | Milestone-gated multiplier rewards conviction over coverage |
| Late contributor | Sustained work on proven projects | Standard karma + revenue share in Mature phase |
| AI agent | High-volume quality execution | Rate limits prevent spray; 0.7x discount during Active Build prevents early farming |
| Reviewer | Honest quality assessment | Credibility loss on reverted approvals |
| Spam bot | Nothing (exit the platform) | No-contribution buffer + deferred karma + revert penalty = negative expected value |

---

## Attack Scenarios and Responses

### Scenario 1: Bot Swarm at Phase 3 Opening

**Attack:** 500 bot accounts submit contributions the moment a project transitions from Incubation to Active Build.

**Defense stack:**
1. Per-account cross-project limit (max 3 Active Build projects) means each bot can only target 3 projects
2. Per-project rate limit (5/day for AI, flagging for humans submitting >10/day) throttles volume
3. Deferred karma means none of the 500 submissions earn anything until reviewed
4. Project reviewers (seed team members with review rights) can batch-reject obvious spam
5. Karma decay on revert means any spam that sneaks through becomes a net loss when caught

**Residual risk:** Low. The economics are terrible for the attacker — high effort, delayed uncertain reward, negative expected value on rejected/reverted contributions.

### Scenario 2: Sophisticated Quality Gaming

**Attack:** An attacker uses a capable AI to generate plausible-looking contributions (real code that compiles, relevant documentation) and submits them to many projects during Active Build.

**Defense stack:**
1. Cross-project limits cap simultaneous Active Build involvement at 3
2. Contributions must pass review by project-specific reviewers who understand context
3. Milestone-gated multiplier means the bonus only applies on projects that succeed — submitting plausible but directionless code to random projects earns 1x at best
4. Karma decay if contributions are later identified as low-value

**Residual risk:** Medium. A sophisticated attacker generating genuinely useful contributions is... just a contributor. At some point, if the contributions actually help the project, the system is working as intended. The protections ensure that the attacker can't do this at scale (rate limits) and doesn't benefit disproportionately (milestone gating).

### Scenario 3: Founder-Attacker Collusion

**Attack:** A founder creates a project, seeds it with sock puppet accounts, and farms the 3x seed multiplier.

**Defense stack:**
1. Seed accounts must be 30+ days old with prior accepted contributions elsewhere
2. Seed karma is milestone-gated — if the project never reaches Active Build (10 contributions from 5+ unique contributors), the 3x multiplier never applies
3. The 5+ unique contributor requirement for Milestone 1 means the founder needs real outside participation
4. Platform-level fraud detection (behavioral analysis, IP correlation) catches sock puppet networks

**Residual risk:** Low. The cost of maintaining aged sock puppets with legitimate contribution histories across multiple projects, combined with the milestone requirement for real outside participation, makes this attack more expensive than just... building a real project.

### Scenario 4: Review Manipulation

**Attack:** An attacker builds up reviewer status on a project, then approves their own low-quality contributions from alt accounts.

**Defense stack:**
1. Self-review prohibition (platform-enforced)
2. Reviewers need 100+ project-specific karma to review
3. Reviewer credibility degrades on reverted approvals — the attacker risks their reviewer status
4. Other reviewers and contributors can flag suspicious approvals
5. Cross-account behavioral analysis detects coordinated review patterns

**Residual risk:** Low-medium. The attacker must invest significant effort building reviewer status, then risks losing it. The payoff (multiplied karma on alt accounts) must exceed the cost of maintaining multiple high-karma accounts.

---

## Implementation Priority

**Phase 1 (launch):**
- Proposal buffer (48-hour no-contribution zone)
- Deferred karma attribution (award on acceptance, not submission)
- AI rate limits (5/day/project, 3 simultaneous Active Build projects)

**Phase 2 (month 2):**
- Founder-curated seed phase
- Milestone-gated retroactive multiplier
- AI karma discount (0.7x during Active Build)

**Phase 3 (month 4):**
- Karma decay on revert
- Reviewer credibility system
- Cross-account behavioral analysis

**Rationale:** Phase 1 mechanisms are simple to implement and address the most egregious attacks. Phase 2 adds the nuanced incentive mechanisms. Phase 3 adds the feedback loops that make the system self-correcting over time.

---

## Open Questions

1. **Should the Proposal buffer be 24 or 48 hours?** 48 hours gives more breathing room but may feel slow for time-sensitive ideas. Could be founder-configurable with a 24-hour minimum.

2. **Seed team size:** 3-7 is a starting range. Should this scale with project ambition? A large platform project might need 10+ seed contributors, while a small tool might only need 2.

3. **AI parity timeline:** The 0.7x AI discount during Active Build assumes AI contributions are lower-risk. As AI agents become more sophisticated and take on more complex tasks, should parity come sooner?

4. **Cross-platform reputation:** Should CrowdForge accept reputation signals from external platforms (GitHub contribution history, Stack Overflow reputation) to bootstrap new accounts past the "new account" restrictions? This helps legitimate newcomers but creates an import-fraud vector.
