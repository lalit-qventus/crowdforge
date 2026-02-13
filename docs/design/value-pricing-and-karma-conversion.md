# Value-Based Pricing and Karma-to-Revenue Conversion Design

This document proposes the concrete karma-to-revenue conversion mechanism for CrowdForge. It synthesizes value-based pricing theory, game economy design, behavioral economics, cooperative dividend models, and platform precedents into a single actionable system.

The core thesis: karma should behave like shares in a cooperative that pay dividends, not like poker chips that convert to cash. The conversion must be indirect enough that contributors focus on status, access, and craft mastery -- with financial returns arriving as a consequence of those things, not as the reason for them.

---

## 1. Why Direct Conversion Fails

### The Cost-Plus Trap

The naive karma system is cost-based pricing applied to human contribution:

```
payout = project_revenue * (my_karma / total_karma)
```

A contributor holding 38.8 karma out of 394.9 total can compute their share to the penny: 9.8% = $490/month on a $5K project. This creates three failure modes:

**Commodification.** Every contribution becomes a mental transaction. "This PR is worth ~$14 of karma." The contribution is a purchase order, not an investment in something you care about.

**Resentment transparency.** When the arithmetic is simple, people optimize the denominator. They lobby against accepting others' contributions (dilution), they submit volume over quality, and they resent anyone whose karma-per-hour is higher than theirs.

**Crowding out.** Gneezy and Rustichini's "A Fine Is a Price" (2000) demonstrated that small financial incentives destroy prosocial behavior without compensating for it. An Israeli daycare fined parents for late pickup -- late pickups increased. The fine converted a social obligation into a market transaction. Blood donation studies (Mellstrom and Johannesson, 2008) found that offering payment for donations cut supply by nearly half.

The CrowdForge karma system sits in the danger zone: enough money to destroy the social framing ("we're building something together") but not enough to be compelling as pure compensation. A contributor holding 10% karma on a $5K/month project earns $425/month -- not enough to live on, too much to ignore.

### The Value-Based Alternative

Value-based pricing sets price by the buyer's perceived benefit, not the producer's cost. A $10 product sold at cost-plus becomes $20. The same product sold on value -- because it prevents $1,000/month in downtime -- becomes $200. The customer pays for the outcome, not the input.

Applied to karma: if 1 karma = $1, people see through it. The abstraction layer is too thin. But if karma unlocks a tier that determines a dividend rate on project revenue streams you're connected to, the value chain has enough indirection that contributors focus on what karma signifies and enables, not what it converts to.

---

## 2. The Dividend Model

### Cooperative Patronage as Blueprint

Agricultural cooperatives distribute profits through patronage dividends: members receive a share of profits proportional to their use of the cooperative, not their equity ownership. The key insight is that members "earn their way into ownership" through participation, not capital investment. At least 20% of the dividend must be distributed in cash; the rest is retained as member equity.

CrowdForge adapts this model:

- **Karma = patronage.** Your karma represents your demonstrated contribution to the cooperative (the project), not a financial investment.
- **Tier = membership class.** Higher patronage history (cumulative karma) places you in a higher membership class with better dividend rates.
- **Dividend = revenue share.** Monthly payouts are dividends on your accumulated patronage, not wages for your labor.

The psychological difference between "you earned $5" and "your karma generated $5 in dividends this month" is not cosmetic. The first frames the contributor as a wage laborer. The second frames them as a stakeholder whose accumulated contribution is producing returns. Research on employee stock options (University of Pennsylvania) shows that equity framing creates a social exchange relationship that triggers reciprocity norms, while wage framing does not.

### The Conversion Chain

```
contribution --> project karma --> cumulative karma --> tier --> dividend rate
  --> weighted share of revenue pool --> monthly payout
```

Each step adds indirection. No contributor can run a simple mental calculation from "hours worked" to "dollars earned." This is intentional:

1. **Breaks the wage frame.** You cannot say "I earn $X/hour on CrowdForge." You earn karma, which builds your tier, which determines your dividend rate, which applies to your share of revenue across all projects you've touched.
2. **Creates multiple motivation loops.** Earning karma is satisfying (competence). Leveling up is satisfying (achievement). Seeing dividends grow is satisfying (investment). Each loop reinforces the others.
3. **Makes gaming harder.** In a direct system, the optimal strategy is "maximize karma/effort ratio." In the tiered system, the optimal strategy is "be a genuinely valuable contributor across multiple projects for a sustained period" -- which is exactly the behavior the platform wants.

---

## 3. The Tier-Dividend System

### Tier Thresholds and Dividend Rate Multipliers

| Tier | Name | Cumulative Karma Threshold | Dividend Rate Multiplier | Identity |
|---|---|---|---|---|
| 0 | Observer | 0 | 0x (no dividends) | Spectator |
| 1 | Contributor | 50 | 0.5x | Newcomer proving themselves |
| 2 | Builder | 250 | 1.0x (baseline) | Reliable, trusted |
| 3 | Architect | 1,000 | 1.5x | Experienced, sought-after |
| 4 | Partner | 5,000 | 2.0x | Platform veteran, multi-project |
| 5 | Inner Circle | 25,000 | 2.5x | Elite, platform-defining |

### The Payout Formula

```
base_share(c) = vested_project_karma(c) / total_vested_project_karma

weighted_share(c) = base_share(c) * tier_multiplier(c)

normalized_share(c) = weighted_share(c) / SUM(weighted_share(all contributors))

payout(c) = distributable_revenue * normalized_share(c)
```

Where `distributable_revenue = gross_revenue - payment_processing_fees - infrastructure_costs`.

The normalization step is critical: it ensures that 100% of the distributable revenue is paid out, regardless of the mix of tier multipliers in the contributor pool. The multipliers are relative, not absolute -- a room full of Tier 5 contributors each earning 2.5x doesn't pay out 250% of revenue; it normalizes so their relative shares remain proportional to their karma.

### Why Non-Linear Multipliers

The 5x spread between Tier 1 (0.5x) and Tier 5 (2.5x) is intentional. A compressed spread (say 2x) makes tier advancement feel insignificant. A steep spread (say 13x) makes the system feel unfair to newcomers.

The 5x spread means:

- A Tier 5 contributor with 200 project karma earns the same weighted share as a Tier 1 contributor with 1,000 project karma.
- This rewards sustained platform-wide contribution, not just grinding on one project.
- But project-level karma still dominates: a Tier 1 contributor with 5,000 project karma always out-earns a Tier 5 contributor with 100 project karma (weighted: 2,500 vs 250).

The multipliers create aspiration without creating tyranny. A new contributor can see the path: "I'm Tier 1 at 0.5x. If I reach Tier 2 (250 karma, maybe 2-3 months of active contribution), my effective share doubles."

---

## 4. Non-Financial Tier Benefits (The Status Stack)

Financial dividends alone are insufficient. If tiers only change a dividend multiplier, contributors mentally collapse the system back to "karma = money with extra steps." The non-financial benefits must be independently desirable.

### Access

| Tier | Access Unlocked |
|---|---|
| 0 (Observer) | Browse, comment, propose ideas |
| 1 (Contributor) | Submit riffs, earn base karma, join Scenes |
| 2 (Builder) | Priority Scene invitations, profile badge, governance voting |
| 3 (Architect) | Curated high-potential Scenes before public listing, mentorship matching, featured profile |
| 4 (Partner) | Advisory board eligibility, early access to platform features, hiring pipeline visibility |
| 5 (Inner Circle) | Strategic governance input, beta features, platform-level decision influence |

### Governance Power

Governance participation is gated by tier, not by karma alone. A Tier 2 Builder can vote on project-level decisions. A Tier 4 Partner can vote on platform-level decisions. A Tier 5 Inner Circle member has advisory board input on platform strategy.

This creates a meritocratic power structure that mirrors cooperative governance: you earn influence through demonstrated contribution, not through capital.

### Professional Credentialing

"Tier 4 Partner on CrowdForge" becomes a credible professional signal -- analogous to "50K reputation on Stack Overflow" but with the added weight of financial outcomes. Tier 3+ profiles are surfaced in a talent marketplace visible to companies hiring.

### Status Markers

Tier-specific profile frames, badges, and leaderboard positions are visible on all contributions and in the live activity stream. The platform celebrates tier advancement publicly ("Alex just reached Architect!") and keeps payout amounts private (visible only in personal dashboards).

The ordering matters: **status first, access second, credentialing third, money fourth.** Cash comes last -- not because it's unimportant, but because leading with cash triggers crowding-out. Leading with status, access, and credentialing activates autonomy ("I choose to be part of this elite group"), competence ("my tier reflects my skill"), and relatedness ("I belong to this community of builders").

---

## 5. Lessons from Game Economy Design

### The Premium Currency Pattern

Fortnite V-Bucks, Roblox Robux, and COD Points all use the same psychological architecture: convert real money into a platform-specific token, then price items in that token. The conversion rate is deliberately non-round (1,000 V-Bucks = $8.99, approximately $0.009 per V-Buck) so that mental arithmetic is difficult.

The V-Bucks model teaches three design principles:

**Psychological distance.** You're not spending $12 on a skin; you're spending 1,200 V-Bucks you already have. The intermediate token absorbs the emotional weight of spending. For CrowdForge, karma is the intermediate token -- but in reverse. Contributors aren't spending; they're earning. The same psychological distance applies: "I earned 150 karma" feels different from "I earned $15."

**Leftover currency.** V-Bucks bundles are sized so that you always have some left over after a purchase, creating an incentive to buy more. CrowdForge's equivalent: karma accumulates across projects and persists indefinitely. You always have "some left over" from past projects, creating an ongoing connection to the platform even when you're between active contributions.

**Non-round conversion.** V-Bucks don't convert at $0.01 each. The irregular rate defeats mental arithmetic. CrowdForge's conversion is even more opaque: karma -> tier -> multiplier -> weighted share -> payout. No one can compute their hourly rate, which is exactly the point.

### The Stack Overflow Pattern

Stack Overflow reputation has zero monetary value, yet users obsess over it. The mechanism: progressive privilege unlocking.

- 15 rep: upvote
- 125 rep: downvote
- 2,000 rep: edit others' posts
- 10,000 rep: moderator tools

Each threshold creates a goal that drives behavior. The reputation itself is the reward -- the capability it unlocks is the reinforcement. Joel Spolsky described this as "a dusting of gamification" -- enough game mechanics to channel behavior, not enough to make it feel like a game.

CrowdForge's tier system replicates this pattern with financial consequences layered on top. The tier is the Stack Overflow-style status marker (visible, aspirational, capability-gating). The dividend is the financial consequence (invisible to others, privately satisfying, compounding with tenure).

### The YouTube Partner Program Pattern

YouTube requires 1,000 subscribers and 4,000 watch hours before a creator can monetize. Only ~3% of channels meet these thresholds. This gate makes monetization feel like an achievement, not an entitlement.

CrowdForge's Tier 0 (Observer) and Tier 1 (Contributor at 0.5x) serve the same function. You don't earn full dividend rates from day one. You earn your way to Builder (1.0x baseline) through 250 cumulative karma -- demonstrating sustained contribution across one or more projects. The gate transforms the dividend from a commodity into a milestone.

### Anti-Gaming Through Indirection

In token economics and game design, the primary anti-gaming mechanism is making the optimal strategy identical to the desired behavior. Bonding curves in token economics slow price increases after milestones, discouraging speculation. CrowdForge's tier system achieves the same effect: the optimal path to maximizing your dividend is sustained, high-quality, multi-project contribution -- which is exactly the behavior the platform wants.

Specific anti-gaming properties of the tier system:

- **Logarithmic upvote scaling** limits the value of vote manipulation. Getting 99 upvotes (3.0x) is only 2.3x better than getting 3 upvotes (1.6x).
- **Non-linear tier thresholds** (50, 250, 1,000, 5,000, 25,000) mean that each successive tier requires exponentially more karma. Farming Tier 2 is easy; farming Tier 5 requires years of genuine contribution.
- **Cross-project accumulation** means you can't game one project; you need sustained contribution across the platform.
- **Tier multipliers apply to per-project karma** -- so even at Tier 5, you need real project-level contribution to earn meaningful dividends.

---

## 6. The Conversion Mechanism in Detail

### Worked Example

**Scene: "PetMatch" -- AI pet adoption platform**
**Monthly distributable revenue: $10,000**

| Contributor | Project Karma (Vested) | Cumulative Karma (Cross-Project) | Tier | Multiplier | Base Share | Weighted Share | Normalized | Monthly Dividend |
|---|---|---|---|---|---|---|---|---|
| Alice (founder) | 850 | 3,200 | Architect (3) | 1.5x | 30.4% | 45.5% | 35.5% | $3,550 |
| Bob (AI agent) | 400 | 400 | Contributor (1) | 0.5x | 14.3% | 7.1% | 5.6% | $560 |
| Carol (ML eng) | 620 | 1,800 | Architect (3) | 1.5x | 22.1% | 33.2% | 25.9% | $2,590 |
| Dave (QA) | 330 | 600 | Builder (2) | 1.0x | 11.8% | 11.8% | 9.2% | $920 |
| Eve (sales) | 600 | 8,500 | Partner (4) | 2.0x | 21.4% | 42.9% | 23.8% | $2,380 |
| **Total** | **2,800** | | | | **100%** | **128.1%** | **100%** | **$10,000** |

Key observations:

- **Alice's tier matters.** Her Architect status (from contributing to other Scenes) boosts her share from 30.4% to 35.5%. The tier system rewards platform-wide track record.
- **Bob is penalized by Tier 1.** His raw share is 14.3% but his effective share is 5.6% -- the 0.5x multiplier halves his dividend. As Bob's operator accumulates karma across projects, this penalty lifts.
- **Eve's cross-project history amplifies her.** She has 600 project karma but is a Partner (2.0x) from extensive platform contribution elsewhere. Her weighted share is 23.8% vs a raw share of 21.4%.
- **Nobody can compute an hourly rate.** The path from "I submitted a riff" to "$X in my bank account" requires knowing: base karma for the contribution type, pioneer multiplier at the time of submission, upvote count, vesting schedule, total project karma, every other contributor's tier, total revenue, and infrastructure costs. This is by design.

### What the Contributor Dashboard Shows

The dashboard presents a narrative, not a spreadsheet:

```
Your Tier: Architect (Level 3)
  Next tier: Partner (5,000 karma) -- 1,800 to go

Active Scenes: 3
  PetMatch: 850 karma (30.4% of Scene)
  CodeReview.ai: 420 karma (12.1% of Scene)
  DesignKit: 280 karma (8.7% of Scene)

This Month's Dividends: $4,180
  PetMatch: $3,550
  CodeReview.ai: $480
  DesignKit: $150

Your Architect tier earned you 22% more than Builder rate would have.
Reaching Partner would increase your dividends by an estimated 18%.
```

The framing is always: "your tier earned you more" and "reaching the next tier would earn you X more." This converts the financial information into an aspiration signal, not a wage statement.

### What the Public Profile Shows

```
Alice -- Architect
  Scenes: 7 (3 active, 2 shipped, 2 archived)
  Karma: 3,200
  Top riffs: [list of highest-upvoted contributions]
  Badges: Pioneer (3 Scenes), First Revenue, 100-Day Streak
```

No financial information. No payout amounts. No dividend rates. The public profile is pure status. Financial details are private.

---

## 7. Tier Threshold Maintenance

### The Inflation Problem

With absolute thresholds (50, 250, 1,000, 5,000, 25,000), the tier distribution shifts over time:

| Platform Age | Tier 5 % | Problem |
|---|---|---|
| 6 months | 0% | Healthy -- nobody has reached it yet |
| 18 months | 2% | Healthy -- small, exclusive group |
| 36 months | 10% | Inflating -- 10,000 Inner Circle members dilutes exclusivity |

### The Ratcheted Hybrid Solution

Use absolute thresholds as the floor, and adjust upward annually based on the 50th-percentile karma level:

```
threshold_i(year) = max(base_threshold_i, base_threshold_i * median_karma(year) / median_karma(year_0))
```

Rules:
- No contributor's tier ever decreases (ratchet guarantee).
- Thresholds rise with the platform, preserving scarcity for new contributors.
- Veterans who earned their tier keep it, even if they'd fall below the new threshold.
- Annual recalibration, announced 90 days in advance.

Projected thresholds:

| Tier | Year 0 | Year 1 | Year 2 | Year 3 |
|---|---|---|---|---|
| 1 (Contributor) | 50 | 75 | 120 | 180 |
| 2 (Builder) | 250 | 375 | 600 | 900 |
| 3 (Architect) | 1,000 | 1,500 | 2,400 | 3,600 |
| 4 (Partner) | 5,000 | 7,500 | 12,000 | 18,000 |
| 5 (Inner Circle) | 25,000 | 37,500 | 60,000 | 90,000 |

This keeps Inner Circle at ~1-3% of contributors while honoring the ratchet guarantee.

---

## 8. Behavioral Economics Foundation

### Self-Determination Theory (Deci and Ryan)

Human motivation rests on three needs: autonomy (I choose to do this), competence (I'm getting better at this), and relatedness (I'm part of something meaningful). External rewards that feel controlling ("do X, get Y") undermine autonomy. External rewards that feel informational ("your skill level qualifies you for this tier") enhance competence.

The tier system is informational: "your Architect status reflects your demonstrated capability across multiple Scenes." The dividend is a consequence of that status, not a per-action payment.

### The Endowment Effect and IKEA Effect

Kahneman, Knetsch, and Thaler demonstrated that people value things they own 2-3x more than identical things they don't own. Norton, Mochon, and Ariely's IKEA effect research extends this: people value things they built even more than things they merely own.

For karma: contributors who earned their karma through labor will value it more than any equivalent cash payment. A direct cash conversion anchors the value downward to the cash amount. An indirect system lets the endowment and IKEA effects inflate the perceived value upward -- karma feels worth more than its cash equivalent because you built it.

### Loss Aversion and Tier Retention

Research on employee stock options shows that unvested equity reduces employee mobility -- the prospect of forfeiting accumulated value is more painful than the pleasure of a new cash bonus elsewhere. CrowdForge's tier system creates the same lock-in:

- Leaving the platform means abandoning your tier, your dividend rate, your accumulated karma across all Scenes, and your governance power.
- The ratchet guarantee (tiers never decrease) amplifies this: your tier is a permanent asset as long as you stay.
- Contributors at Tier 3+ have invested months of sustained contribution. Walking away from that investment triggers loss aversion.

### Gneezy-Rustichini Compliance

The system avoids the "fine is a price" failure mode by never framing karma as payment for contribution. Karma is recognition of contribution. The dividend is a consequence of recognition level. This two-step indirection preserves the social framing ("we're building together") while still delivering financial returns.

The dividend amounts must be large enough to be meaningful (avoiding the "small reward that destroys motivation without compensating for it" trap). The tier multiplier system ensures that high-tier contributors earn substantially more than low-tier ones, making the financial reward feel like genuine acknowledgment of demonstrated value.

---

## 9. Comparison to Direct Payout

| Dimension | Direct Payout (Current) | Dividend Model (Proposed) |
|---|---|---|
| **Mental model** | "I earned $490 this month" | "My Architect status generated $3,550 in dividends across 3 Scenes" |
| **Frame** | Wage / piece-rate | Equity / ownership stake |
| **Time horizon** | This month's payout | Lifetime earnings potential across all Scenes |
| **Retention mechanism** | Must keep earning to keep getting paid | Tier status creates loss aversion; dividend rate compounds with tenure |
| **Identity** | "I'm a contractor on this project" | "I'm an Architect on CrowdForge" |
| **Response to platform growth** | Indifferent (my payout is my payout) | Invested (platform growth means more Scenes, more revenue pools, higher dividends) |
| **Gaming strategy** | Maximize karma/effort ratio on one project | Be genuinely valuable across multiple projects for years |
| **Resentment trigger** | "That person earns more $/hour than me" | "That person is a higher tier -- I want to get there too" |

---

## 10. Vesting as Commitment Device

### The 90-Day Vest

Karma earned on a project vests over 90 days:

- **Day 0:** 25% immediately vested
- **Days 1-90:** Remaining 75% vests linearly (~0.83%/day)
- **Day 90:** Fully vested

Unvested karma counts toward tier progression but does not generate dividend payouts. This creates two incentives:

1. **Stay engaged.** A contributor who leaves at day 30 forfeits 50% of earned karma. At day 7, they forfeit 69%.
2. **No hit-and-run.** Submitting a riff, claiming karma, and disappearing is penalized proportionally to how quickly you leave.

### Why 25% Immediate

A 30-day cliff (Model B in the economics analysis) means new contributors earn nothing in their first month. This violates the "should feel fair to a newcomer on day 1" constraint. The 25% immediate vest gives new contributors a tangible first dividend while still penalizing quick exits.

### Abandoned Karma

If a contributor abandons a project (zero activity for 60 consecutive days) before full vesting, they retain only the vested portion. The unvested portion is burned (removed from the total karma pool), not redistributed. Burning prevents gaming via temporary contributors who inflate then deflate the pool.

---

## 11. Revenue Smoothing

### The Volatility Problem

Monthly revenue fluctuates. A project with $12K in January, $8K in February, and $14K in March creates payout swings that feel chaotic. Contributors prefer predictability.

### Rolling 3-Month Average

Instead of spot-rate payouts, use a trailing 3-month average:

```
smoothed_revenue(t) = (R(t) + R(t-1) + R(t-2)) / 3
payout(c, t) = smoothed_revenue(t) * normalized_share(c, t)
```

This dampens revenue spikes and dips by 3x while maintaining responsiveness to real trends. A sustained revenue increase shows up within 2 months; a one-month anomaly is absorbed.

For new projects (less than 3 months of revenue history), use whatever history is available: month 1 uses only month 1 revenue; month 2 uses the 2-month average.

---

## 12. The Contribution Velocity Floor

### The Rest-and-Vest Problem

A contributor who holds 60% of project karma and stops contributing continues receiving 60% of revenue indefinitely. Dilution works slowly -- if remaining contributors also slow down (demoralized by the whale's dominance), the whale retains dominant share for years.

### Graduated Inactivity Reduction

If a contributor earns zero new karma for 6 consecutive months, their payout share is gradually reduced:

- **Months 1-6 of inactivity:** Full dividend rate (no penalty)
- **Month 7:** 90% of entitled dividend
- **Month 8:** 80%
- **Month 9:** 70%
- **Month 10:** 60%
- **Month 11+:** 50% floor (never drops below half)

Any new contribution (even minimal) resets the clock. This is soft decay applied to completely inactive contributors -- it does not violate the "no karma decay" principle because karma itself is untouched. Only the payout multiplier is affected.

The 50% floor ensures that early contributors retain a meaningful stake even in complete inactivity, honoring the "earned, never taken away" principle while preventing eternal rest-and-vest.

---

## 13. Cross-Project Tier Gaming Analysis

### The Attack Vector

Can someone farm karma on cheap projects for tier advancement, then collect dividends on expensive projects?

**Scenario:** Contributor X farms 5,000 karma across 10 low-revenue projects, reaching Tier 4 (2.0x). X has only 100 karma on a high-value project.

Compare to Contributor Y with 3,000 project karma at Tier 3 (1.5x) on the same high-value project.

```
X weighted: 100 * 2.0 = 200
Y weighted: 3,000 * 1.5 = 4,500
```

Y dominates 22.5:1. The gaming vector is weak because per-project karma dwarfs the tier multiplier effect. The only scenario where tier gaming succeeds is extreme tier differential combined with similar project karma -- which would mean the higher-tier person invested comparable effort on that specific project, just at different times. That is not gaming; it is reward for platform loyalty.

### Tier 5 Gaming Cost

Reaching Tier 5 (25,000 karma) through farming requires approximately:

- At ~12 karma per contribution (steady-state): 2,083 accepted contributions
- At 5 contributions/month: 34.7 months (nearly 3 years)
- Across multiple projects with peer review validation

This is not a viable attack vector. Three years of sustained, peer-validated contribution across multiple projects is the definition of a legitimate platform veteran.

---

## 14. Howey Test Implications

The dividend framing introduces a naming risk. "Dividend" implies a return on investment, which is one prong of the Howey test for securities classification.

### Structural Defenses

| Howey Prong | Defense |
|---|---|
| Investment of money | Contributors invest effort, not capital. Karma cannot be purchased, traded, or gifted. |
| Common enterprise | Revenue share is proportional to individual karma (individual effort), not pooled investment returns. |
| Expectation of profits | Compensation for services rendered. Same legal framework as YouTube Partner Program and Twitch Affiliate Program. |
| Efforts of others | Karma requires active, ongoing contribution. Unvested karma generates no payout. The contribution velocity floor reduces payouts for inactive contributors. No passive income mode. |

### Language Discipline

The term "dividend" is an internal design metaphor. All user-facing language, legal documents, RSAs, tax forms, and marketing materials use "revenue share" or "service compensation." The word "dividend" never appears in contributor-facing materials.

This is not deception -- it is appropriate legal framing. The mechanism functions like a dividend (accumulated contribution generates ongoing returns), but it is legally structured as performance-based service compensation (same as Twitch, YouTube, and every gig platform).

---

## 15. Migration Path

The existing karma system already has the right primitives. The migration reframes, it does not rebuild.

### What Stays

- Per-project karma accounting
- Base karma by contribution type (Code: 10, Design: 8, Testing: 7, Marketing: 6, Ideation: 5, Governance: 4)
- Pioneer multiplier (1 + 2e^(-0.01t))
- Logarithmic upvote scaling (ln(1+v) / ln(10))
- Non-transferability
- Dilution as natural decay
- Sales karma (1 per $100 collected revenue)
- 100% of distributable revenue to karma-weighted contributors

### What Changes

| Current | Proposed |
|---|---|
| `payout = revenue * (karma / total_karma)` | `payout = revenue * normalized_share` where normalized_share includes tier multiplier |
| Karma is the complete story | Karma feeds into a tier system that determines dividend rate |
| Revenue share is the sole reward | Revenue share is one of several tier-gated rewards (status, access, governance, credentialing) |
| All karma is immediately "active" | 90-day vesting schedule (25% immediate + 75% linear) |
| Cross-project reputation is informational only | Cumulative cross-project karma determines tier and dividend rate |
| No inactivity penalty | Contribution velocity floor: gradual payout reduction after 6 months of zero contribution |

### What's Added

- Tier thresholds and tier-specific non-financial benefits
- Dividend rate multiplier per tier
- Revenue smoothing (3-month trailing average)
- Ratcheted hybrid threshold recalibration (annual)
- Public status markers with private-only financial dashboards
- Contribution velocity floor (50% minimum after 11+ months inactive)

---

## 16. Implementation Sequence

### Phase 1: Tier System (Launch)

Deploy the tier system with multipliers. Contributors see their tier, the benefits each tier unlocks, and their progress toward the next tier. Payouts use the weighted formula from day one.

This is the minimum viable conversion mechanism. Everything else layers on top.

### Phase 2: Non-Financial Benefits (Month 2-4)

Roll out tier-gated access: priority Scene invitations for Builder+, curated Scene access for Architect+, advisory board for Partner+. These benefits must feel valuable independent of the dividend rate.

### Phase 3: Status Infrastructure (Month 3-6)

Profile frames, badges, tier advancement celebrations in the live activity stream, leaderboards. Public profiles show tier and contribution history. Financial dashboards remain private.

### Phase 4: Threshold Recalibration (Year 1 Anniversary)

First annual threshold adjustment based on median karma. Announce 90 days before the anniversary. Apply the ratchet guarantee. Communicate transparently: "Tier thresholds are rising because the community is growing. If you've already earned your tier, you keep it."

---

## 17. Risk Analysis

### Risk: Contributors See Through the Indirection

Someone publishes a blog post reverse-engineering the tier system into a $/hour estimate.

**Mitigation:** This is inevitable and acceptable. People know that stock options have a calculable value, but they still behave differently with options than with cash. The psychological frame matters more than the mathematical reducibility. The indirection does not need to be opaque -- it needs to be complex enough that the default mental model shifts from "wage" to "investment."

### Risk: Over-Complexity Deters Newcomers

A new contributor looks at tiers, vesting, multipliers, and weighted shares and thinks "this is too complicated."

**Mitigation:** Progressive disclosure. The onboarding experience presents: "Contribute. Earn karma. Level up. Get paid." Tier 0 and Tier 1 are simple: submit riffs, earn karma, accumulate toward Builder. Full complexity is revealed only to retained contributors who advance. Complexity is a feature for veterans, not a barrier for newcomers.

### Risk: Tier Resentment

A Tier 5 contributor with 200 project karma earns more than a Tier 1 contributor with 400 project karma on the same Scene.

**Mitigation:** Display both raw karma share and tier-adjusted share in contributor dashboards. Frame it as aspiration: "Your base share is 8%. Your Contributor status adjusts this to 4.5%. Reaching Builder (250 karma -- 190 to go) would bring your share to 9%." This converts resentment into motivation.

### Risk: Mercenary Tier Farming

Contributors farm low-effort contributions across many Scenes purely to advance their tier.

**Mitigation:** Karma is earned through peer-reviewed contributions. Low-effort riffs receive zero upvotes, earning only base karma. At 5 karma per trivial contribution, farming to Tier 5 (25,000 karma) requires 5,000 trivial accepted riffs -- an absurd volume that peer reviewers will flag long before it reaches that scale. The behavioral detection layer (fraud prevention Layer 2) flags burst activity and riff similarity patterns.

---

## 18. Summary

The karma-to-revenue conversion mechanism for CrowdForge rests on six principles:

1. **Indirection over transparency.** The conversion chain (contribution -> karma -> tier -> multiplier -> weighted share -> payout) prevents mental piece-rate calculation and preserves intrinsic motivation.

2. **Status over cash.** Tiers, badges, access, governance power, and professional credentialing are the primary rewards. Financial dividends are a consequence of status, not the purpose of contribution.

3. **Cooperative dividends over wages.** The framing is "your accumulated contribution generates ongoing returns" not "you earned $X for that riff."

4. **Non-linear thresholds.** Each successive tier requires exponentially more karma (50, 250, 1,000, 5,000, 25,000), making the system naturally resistant to gaming while creating clear aspiration milestones.

5. **Ratcheted scarcity.** Annual threshold recalibration preserves tier exclusivity as the platform grows, while the ratchet guarantee ensures no contributor ever loses a tier they earned.

6. **Aligned incentives.** The optimal strategy for maximizing personal dividends is identical to the optimal strategy for making the platform succeed: sustained, high-quality, multi-project contribution over years. When the game theory and the platform's goals point in the same direction, the system works.
