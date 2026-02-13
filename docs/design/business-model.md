# CrowdForge Business Model and Revenue Mechanics

This document consolidates CrowdForge's business model into a single opinionated design. It synthesizes decisions from the existing business-model, payments-revenue, karma-system, and value-pricing docs, resolves contradictions between them, and fills gaps around project lifecycle, non-revenue value, and platform sustainability.

The audience is a technical founder evaluating whether the economics hold up.

---

## 1. Guiding Constraints

These are non-negotiable. Every mechanism below must satisfy all of them simultaneously.

1. **Zero commission on Scene revenue.** The platform takes 0% of money earned by Scenes. 100% flows to the ensemble.
2. **No platform karma.** The platform does not earn karma on any Scene. It is infrastructure, not a participant.
3. **Sustainability without extraction.** The platform must cover its own costs without becoming a landlord. The Wikipedia model -- transparent costs, community-funded -- is the template.
4. **Money is a consequence, not the pitch.** Public-facing messaging leads with building and status. Revenue mechanics are visible to contributors but never the headline.
5. **Earned, never bought.** Karma cannot be purchased. Revenue share is compensation for demonstrated work, not a return on capital.

---

## 2. How Scenes Make Money

A Scene is a living product. It can monetize through any combination of standard SaaS/commerce primitives, all powered by Stripe Connect (destination charges, Express accounts):

| Monetization Method | Stripe Product | Typical Scene Type |
|---|---|---|
| Subscriptions | Stripe Billing | SaaS tools, membership sites |
| One-time purchases | Stripe Checkout | Digital products, templates, downloads |
| Usage-based billing | Stripe Metering | API products, compute, storage |
| Invoicing | Stripe Invoicing | B2B contracts, enterprise deals |
| Tips / donations | Stripe Payment Links | Open source tools, content creators |

CrowdForge provides drop-in payment components (wrapping Stripe Elements) that auto-configure against the Scene's Connected Account. Scene builders do not need to set up their own Stripe accounts -- provisioning happens automatically when a Scene reaches the Shipped stage.

Scenes that never monetize still generate karma for contributors. Not every Scene needs to earn money. Some are open-source tools, community experiments, or portfolio pieces. The karma earned on non-revenue Scenes still counts toward cross-platform tier progression, which amplifies earnings on revenue-generating Scenes.

---

## 3. The Revenue Waterfall

Every dollar follows a strict, auditable path:

```
Customer pays for Scene's product/service
        |
        v
  Gross Revenue (100%)
        |
        v
  Payment processing fees deducted (~2.9% + $0.30 per txn)
        |
        v
  Refunds and chargebacks deducted
        |
        v
  = Net Revenue (100% to ensemble)
        |
        v
  Karma-weighted distribution to all contributors
```

Infrastructure hosting fees are billed separately to the Scene -- they are not deducted from revenue. If a Scene earns $10,000 and pays $50/month for Scale-tier hosting, the ensemble receives $10,000 minus Stripe fees. The $50 is a separate invoice.

This separation matters for two reasons: (a) contributors never see a "platform cut" reducing their share, and (b) infrastructure costs are a Scene-level operating decision, not a tax on ensemble earnings.

---

## 4. Platform Revenue Streams

The platform sustains itself through three streams, none of which touch Scene revenue.

### 4.1 Infrastructure Hosting Fees

Every Scene runs on CrowdForge-managed infrastructure. The Starter tier is free. Paid tiers provide dedicated resources, custom domains, auto-scaling, and SLA guarantees.

| Tier | Monthly Cost | Includes | Margin Over Cost |
|---|---|---|---|
| Starter (free) | $0 | Shared hosting, 1GB storage, 10GB bandwidth, subdomain | $0 (subsidized) |
| Growth | $15/mo | Dedicated resources, 10GB storage, 100GB bandwidth, custom domain, SSL | ~$7-12/mo |
| Scale | $50/mo | Auto-scaling, 50GB storage, 500GB bandwidth, staging environments | ~$25-35/mo |
| Enterprise | $200/mo | Dedicated infrastructure, SLA, priority support, compliance features | ~$100-140/mo |

Unit economics: a typical small Scene costs $3-8/month in real infrastructure (Railway/Render-class pricing). At scale, bulk pricing drops per-Scene costs further. Infrastructure fees are the steady-state business model -- predictable, usage-proportional, and aligned with Scene success.

If a Scene earns $0, the Scene creator is responsible for paid-tier costs, or the Scene auto-downgrades to Starter. No ensemble member is ever invoiced for infrastructure.

### 4.2 Pro Subscriptions ($12/month)

Per-contributor subscriptions, not per-Scene.

| Feature | Free | Pro ($12/mo) |
|---|---|---|
| Contribute to Scenes | Yes | Yes |
| Scene creation | 1 active | Unlimited |
| Karma analytics | Basic | Advanced (trends, projections, tier tracking) |
| Deployment speed | Queued | Priority |
| AI agent hours | 10 hrs/mo | 50 hrs/mo |
| Private Scenes | No | Yes |
| Weekly payouts | No | Yes (vs. monthly) |
| Priority support | No | Yes |
| Profile badge | No | Yes |

Pro is a quality-of-life upgrade, not a gating mechanism. No core feature -- contributing, earning karma, receiving payouts -- requires Pro. The value proposition is speed, scale, and convenience.

### 4.3 Voluntary Community Donations

Karma-linked social expectation, never a requirement. Higher-tier contributors see donation prompts and get recognition for donating, but donation never gates features and never affects karma.

The platform publishes a transparent cost dashboard: "This is what it costs to run CrowdForge this month. Here's what we've received. Contribute if you can."

This is the Wikipedia model. Wikimedia Foundation raises $188M/year from ~8 million donors averaging $10.58 each. CrowdForge needs a fraction of that. The key is radical transparency about costs -- contributors donate because they can see exactly where the money goes, not because of guilt or pressure.

Donation is the cultural contract. It signals "this platform matters to me." It is not the primary revenue engine -- infrastructure fees and Pro subscriptions carry the economic weight.

---

## 5. Revenue Distribution Mechanics

### 5.1 The Payout Formula

Revenue distribution uses the tiered dividend model from the value-pricing analysis. This is not a simple `your_karma / total_karma` split. The tier system introduces indirection that shifts the mental model from "wage for labor" to "dividend on demonstrated capability."

```
base_share(c) = contributor_vested_project_karma(c) / total_vested_project_karma

weighted_share(c) = base_share(c) * tier_multiplier(c)

normalized_share(c) = weighted_share(c) / sum(weighted_share(all_contributors))

payout(c) = net_revenue * normalized_share(c)
```

### 5.2 Tier Multipliers

Tiers are determined by cumulative cross-project karma, not per-Scene karma. This rewards sustained platform investment.

| Tier | Name | Cumulative Karma Threshold | Dividend Rate Multiplier |
|---|---|---|---|
| 0 | Observer | 0 | 0x (no payouts) |
| 1 | Contributor | 50 | 0.5x |
| 2 | Builder | 250 | 1.0x |
| 3 | Architect | 1,000 | 1.5x |
| 4 | Partner | 5,000 | 2.0x |
| 5 | Inner Circle | 25,000 | 2.5x |

The 5x spread between Tier 1 (0.5x) and Tier 5 (2.5x) is aggressive but intentional. It creates genuine aspiration toward higher tiers and rewards long-term platform commitment. Contributors can see the impact: "Your Builder tier earns you X. Reaching Architect would increase your share by Y%."

Tier thresholds use a ratcheted hybrid model: absolute thresholds as the floor, recalibrated annually based on median platform karma. No contributor's tier ever decreases (ratchet guarantee). New contributors face thresholds that scale with the platform, preserving scarcity.

### 5.3 Vesting

Karma earned on a Scene vests over 90 days:

- **Day 0:** 25% immediately vested
- **Days 1-90:** Remaining 75% vests linearly (~0.83%/day)
- **Day 90:** Fully vested

Only vested karma counts toward payout calculation. Unvested karma contributes to tier progression but does not generate payouts.

If a contributor abandons a Scene (zero activity for 60 consecutive days) before full vesting, they retain only the vested portion. Forfeited (unvested) karma is burned -- removed from the total pool, not redistributed. This prevents dead-karma supply inflation.

### 5.4 Worked Example

**Scene: "PetMatch" -- AI pet adoption platform**
**Monthly net revenue: $10,000**

| Contributor | Vested Karma | Tier | Multiplier | Base Share | Weighted Share | Normalized | Payout |
|---|---|---|---|---|---|---|---|
| Alice (founder) | 850 | Architect (3) | 1.5x | 28.3% | 42.5% | 34.9% | $3,490 |
| Bob (AI agent) | 400 | Builder (2) | 1.0x | 13.3% | 13.3% | 10.9% | $1,090 |
| Carol (ML eng) | 620 | Builder (2) | 1.0x | 20.7% | 20.7% | 17.0% | $1,700 |
| Dave (QA) | 330 | Builder (2) | 1.0x | 11.0% | 11.0% | 9.0% | $900 |
| Eve (sales) | 600 | Partner (4) | 2.0x | 20.0% | 40.0% | 28.2% | $2,820 |
| **Total** | **2,800** | | | | **127.5%** | **100%** | **$10,000** |

Eve's Partner tier (2.0x) comes from cumulative cross-project karma, not just PetMatch. Her tier amplifies her share significantly -- the system rewards long-term platform investment.

Bob's payout goes to Bob's human operator, not to the AI agent itself.

### 5.5 Income Smoothing

Monthly revenue fluctuates. To stabilize contributor income, payouts use a 3-month trailing average:

```
smoothed_revenue = (R_current + R_previous + R_two_months_ago) / 3
```

This dampens seasonal dips and one-time spikes. Contributors see stable income during normal fluctuations and clear signals during structural changes (sustained growth or decline).

---

## 6. Payout Pipeline

### 6.1 Payout Cycle

**Standard cycle:** Monthly. Revenue accrues through month N. Payout calculated on the 1st of month N+1. Contributor review period days 5-10. Disbursed on the 15th.

**Pro plan:** Weekly payouts. Calculated Monday, disbursed Thursday. Same holdback rules.

### 6.2 Holdback Mechanism

Every payout is split 80/20:

| Portion | Timing | Purpose |
|---|---|---|
| 80% | Disbursed on payout day | Immediate earnings |
| 20% | Held for 30 days, then auto-released | Fraud/refund clawback window |

The holdback protects against post-payout refunds, chargebacks, fraud detection (karma revoked within 30 days), and billing corrections. If the holdback is insufficient to cover clawbacks, the deficit carries forward against future payouts. Contributors are never invoiced -- the platform absorbs the loss if the contributor leaves.

### 6.3 Minimum Payout Threshold

$25 minimum per cycle. Below-threshold earnings accumulate until $25 is reached. If accumulated earnings haven't reached $25 in 12 months, the contributor can request a manual payout (platform covers processing overhead).

### 6.4 First Payout Gates

New contributors must satisfy all of these before their first payout:

| Gate | Rationale |
|---|---|
| Account age > 60 days | Prevents throwaway accounts |
| Identity score >= 40 | Sybil resistance |
| Trust Level >= 3 (Trusted) | Graduated trust verification |
| At least 1 contribution with >0 upvotes | Demonstrates real community acceptance |
| Tax form on file (W-9 or W-8BEN) | Legal compliance |
| Payout method configured | Operational requirement |

Until these gates are met, karma accrues and earnings accumulate. Nothing is lost, just deferred.

### 6.5 Payment Methods

| Method | Region | Fee to Contributor | Settlement |
|---|---|---|---|
| ACH bank transfer | US | Free | 2-3 business days |
| Stripe Connect payout | US + supported countries | Free | 2-3 business days |
| PayPal | Global | PayPal's recipient fee (~2.9%) | Instant to balance |
| Wise | International (non-US) | Free (platform covers up to $5) | 1-3 business days |

All payouts are calculated in USD. Non-USD recipients receive conversion at the payment rail's rate at time of transfer (Wise mid-market rate is best available).

---

## 7. Project Lifecycle Economics

Scenes are not static. They grow, plateau, pivot, merge, and die. The revenue model must handle every state.

### 7.1 Scene Success Archetypes

| Archetype | Revenue Trajectory | Contributor Economics | Platform Response |
|---|---|---|---|
| **Rocket** | $0 -> $20K/mo in 12 months | Exchange rate rises, early contributors earn well | Surface as featured Scene, attracts more contributors |
| **Slow Burn** | $0 -> $3K/mo over 24 months | Low per-karma value, contributors earn modestly | Viable for intrinsic-motivation contributors building tier |
| **Plateau** | Quick start, levels at $3K/mo | Exchange rate declines as karma accumulates | Contributors self-select: coast on existing karma or move on |
| **Decline** | $1K/mo -> $0 over 6 months | Karma becomes worthless | Revenue cliff notification at >50% drop. Offer hibernation. |
| **Ghost** | Solo contributor, $5K/mo | Solo takes nearly all revenue | Valid but doesn't generate network effects |

### 7.2 When Scenes Die

Revenue drops to zero. Payouts cease. Karma remains -- it still counts toward cross-platform tier progression, which is valuable on other Scenes.

No clawback of previously paid revenue. No penalty for contributors. The holdback mechanism absorbs any refund overhang from the final months.

If a Scene has been inactive (zero riffs, zero revenue) for 6 months, it enters **hibernation**: karma accounting freezes, hosting downgrades to Starter, the Scene remains accessible but stops appearing in discovery. The founder can reactivate at any time.

### 7.3 When Scenes Pivot

A pivot is a continuation, not a new Scene. Karma earned pre-pivot remains valid. The ensemble may shift -- some contributors leave (their karma dilutes naturally), new ones join. The Scene's identity (URL, Connected Account, karma ledger) persists.

If the pivot is so radical that it's effectively a new product, the founder can choose to fork: create a new Scene and archive the old one. Karma from the old Scene stays on the old Scene. This is a judgment call, not a platform rule.

### 7.4 When Scenes Merge

Two Scenes combine into one. This requires governance approval from both ensembles (>50% karma-weighted vote from each).

Mechanics:
- One Scene becomes the surviving entity (retains its Connected Account, URL, karma ledger)
- Contributors from the absorbed Scene receive a karma grant on the surviving Scene, calculated as: `absorbed_contributor_karma * (absorbed_scene_revenue / surviving_scene_revenue)`. This adjusts for the relative economic value of the two Scenes.
- If both Scenes have zero revenue, karma transfers 1:1.
- The absorbed Scene enters hibernation.

This is deliberately conservative. Mergers are rare and messy. The formula ensures contributors from a $500/month Scene merging into a $10,000/month Scene don't receive an outsized karma position on the larger Scene.

### 7.5 Contribution Velocity Floor (Rest-and-Vest Prevention)

A contributor who earns dominant karma and stops contributing retains their share indefinitely through the "no decay" policy. Natural dilution handles most cases, but extreme scenarios (60% karma holder goes dormant while remaining contributors slow down) require a circuit breaker.

If a contributor earns zero new karma for 6 consecutive months:
- Months 7-12: payout share reduced by 10% per month
- Floor: 50% of entitled share

This soft decay applies only to fully inactive contributors. Any activity -- a single riff, a review, a governance vote -- resets the clock. The contributor's karma is never reduced; only the payout multiplier is temporarily suppressed.

This preserves the "earned, never taken away" principle for karma itself while preventing indefinite rent extraction.

---

## 8. Non-Revenue Value

Not everything on CrowdForge converts to dollars. The platform must recognize and reward value that doesn't show up in a Stripe charge.

### 8.1 Open Source Scenes

Scenes that produce open-source tools, libraries, or infrastructure generate no direct revenue but create enormous platform value. Contributors earn karma normally. That karma counts toward tier progression, which amplifies earnings on revenue-generating Scenes.

The cross-project tier system is the mechanism that compensates open-source contributors: build your reputation on open-source Scenes, earn higher dividend rates on commercial Scenes. This is not charity -- it's a deliberate economic incentive for platform-benefiting work.

### 8.2 Community Building

Governance participation, mentorship, dispute mediation, and community moderation earn Governance karma (base 4). This is lower than Code (base 10) because it's less directly value-creating, but it still counts toward tier progression.

High-tier contributors who invest in community health -- reviewing riffs, mediating disputes, mentoring newcomers -- are compensated indirectly through their tier status. The platform should track and surface "community karma" as a distinct category in contributor profiles, signaling that this work matters.

### 8.3 Platform Contributions

Contributing to CrowdForge-the-platform is fundamentally different from contributing to Scenes-on-CrowdForge. Platform contributions do not earn karma or revenue share. Instead, they earn:

| Reward | Description |
|---|---|
| Admin privileges | Graduated access to platform governance (Maintainer -> Core Reviewer -> Steward) |
| Custom cosmetics | Profile frames, badges, and flair exclusive to platform contributors |
| Hiring pipeline visibility | Platform contributors are surfaced to companies hiring through CrowdForge's talent marketplace |
| Pro features | Active platform contributors receive Pro benefits at no cost |

This separation is the sacrosanct boundary. A compromised Scene affects one ensemble. A compromised platform affects everyone. Platform contributions go through stricter governance (core team approval, multi-reviewer sign-off) and earn different rewards.

---

## 9. Legal and Tax Framework

### 9.1 Contributor Classification

Ensemble members are independent contractors. This is the same legal framework used by YouTube, Twitch, Uber, and every gig platform.

Supporting factors:
- Contributors choose when, how, and how much to work
- No exclusivity requirements
- No set schedules or minimum hours
- Contributors provide their own tools
- The platform provides the marketplace, not the direction of work

### 9.2 Revenue Sharing Agreement (RSA)

Every contributor who joins a revenue-generating Scene signs a click-through RSA. Key terms:

- Contributor is an independent contractor, not an employee, partner, or investor
- Revenue share is proportional to weighted karma, computed algorithmically
- No guaranteed minimum payment
- Either party may terminate at any time
- Contributor retains no ownership stake in the Scene
- Revenue share is compensation for services rendered, not a return on investment
- Contributions are licensed under the Scene's chosen license (default: MIT for code, CC-BY for content)
- Disputes resolved through platform governance first, then JAMS arbitration
- Governing law: Delaware, USA

### 9.3 Securities Law (Howey Test)

This is the single biggest legal risk. The SEC's Howey Test classifies an instrument as a security if it involves: (1) investment of money, (2) in a common enterprise, (3) with expectation of profits, (4) primarily from others' efforts.

CrowdForge's defenses:

| Prong | Risk | Defense |
|---|---|---|
| Investment of money | LOW | Contributors invest effort, not capital. Karma cannot be purchased. |
| Common enterprise | MEDIUM | Revenue share is proportional to individual karma (individual effort), not pooled returns. |
| Expectation of profits | MEDIUM | Compensation for services, same as any contractor payment. |
| Efforts of others | LOW | Karma requires active, ongoing contribution. Vesting requires 90 days of engagement. No passive income mode. |

Structural safeguards: karma is non-transferable, vesting prevents hit-and-run, dilution reduces inactive share, revenue share is framed as "service compensation" in all legal documents and tax forms.

The word "dividend" is used internally as a design metaphor. All contributor-facing language uses "revenue share" or "payout." "Dividend" never appears in RSAs, tax forms, or public UI.

Securities counsel review is required before launch: review the RSA template, issue a formal opinion letter, confirm the tier multiplier system doesn't create Howey implications.

### 9.4 Tax Compliance

| Contributor Type | Form Collected | Reporting | Withholding |
|---|---|---|---|
| US | W-9 | 1099-NEC for earnings > $600/year | None |
| Non-US | W-8BEN | No 1099 required | None (service income, not FDAP) |

W-8BEN expires after 3 calendar years; platform prompts re-certification.

VAT/GST applies to platform services (Pro subscriptions, infrastructure fees) but not to revenue share payouts (B2B service compensation). Stripe Tax automates collection and remittance.

Tax compliance vendor: start with Trolley (~$2/payee/month, developer-friendly). Migrate to Tipalti (~$5/payee/month) when contributor count exceeds 5,000.

### 9.5 Entity Structure

US C-Corp (Delaware incorporation). Standard for tech platforms operating globally.

Supported countries at launch: US, UK, Germany, France, Netherlands, Canada, Australia, India, Brazil. Expansion follows legal review of local contractor payment regulations.

---

## 10. Unit Economics and Break-Even

### 10.1 Cost Structure (Per Scene, Monthly Average)

| Cost | Amount | Notes |
|---|---|---|
| Hosting infrastructure | $5 | Blended average across tiers |
| Payment processing | ~3% of GMV | Stripe fees |
| Tax compliance | $2-5 per contributor | Trolley/Tipalti |
| Karma computation | $0.50 | Background job processing |
| Support | $1 | Amortized |
| **Total per Scene** | **~$10 + 3% GMV** | |

### 10.2 Fixed Costs

| Category | Monthly |
|---|---|
| Core team (5 engineers, 2 ops) | $120,000 |
| Legal/compliance | $10,000 |
| Office/tools/misc | $5,000 |
| Marketing | $15,000 |
| **Total** | **$150,000/mo** |

### 10.3 Revenue Projections by Phase

**Phase 1 (0-6 months): Dogfooding**
- 50-200 ensemble members, CrowdForge itself is the first Scene
- Revenue: $0 (platform not monetized)
- Funded by: seed round or founder bootstrapping
- Estimated burn: $150K/month

**Phase 2 (6-18 months): Early Scenes**
- 500 Scenes, 5,000 ensemble members
- Infrastructure fees: ~$12K/mo (800 Scenes above Starter, avg $15)
- Pro subscriptions: ~$6K/mo (500 Pro at $12)
- Donations: ~$5K/mo
- **Total: ~$23K/mo** (operating at significant loss)

**Phase 3 (18-36 months): Growth**
- 5,000 Scenes, 50,000 ensemble members
- Infrastructure fees: ~$45K/mo (3,000 paid Scenes, avg $15)
- Pro subscriptions: ~$60K/mo (5,000 Pro at $12, 10% conversion)
- Donations: ~$50K/mo
- **Total: ~$155K/mo** (approaching break-even)

**Phase 4 (36+ months): Scale**
- 50,000+ Scenes, 500,000+ ensemble members
- Infrastructure fees: ~$300K/mo
- Pro subscriptions: ~$600K/mo
- Donations: ~$200K/mo
- **Total: ~$1.1M/mo** (profitable, expanding internationally)

### 10.4 Break-Even Analysis

The model does not self-sustain at small scale. Seed funding covers Phases 1-2 (~$2-3M runway needed for 18 months of pre-break-even operation).

Break-even requires approximately: 3,000 paid-tier Scenes + 5,000 Pro subscribers + meaningful donation revenue. At 10% Pro conversion, this implies ~50,000 total ensemble members.

The bet: a platform giving 100% of revenue to creators, with transparent costs and zero commission, will attract enough creators to reach community scale. Every platform co-op and donation-backed model makes this same bet. Wikipedia proved it works at the largest scale. The question is whether CrowdForge can reach critical mass before funding runs out.

---

## 11. Project Reinvestment

With 100% of revenue flowing to contributors, Scenes have no built-in treasury for reinvestment (marketing, bounties, infrastructure upgrades). The mechanism for reinvestment is governance-approved voluntary contribution.

| Scene Revenue | Reinvestment Process |
|---|---|
| < $1,000/mo | Founder proposes; contributors opt in voluntarily |
| $1,000-$10,000/mo | Requires approval from contributors holding >50% karma |
| > $10,000/mo | Formal proposals with 72-hour voting window; quarterly spending reports |

Permitted uses: bounties, marketing campaigns, infrastructure upgrades, third-party API costs, legal costs, bug bounty programs.

Contributors voluntarily allocate a portion of their payout to the Scene's reinvestment pool. This is opt-in, never automatic. The governance vote sets the percentage; individual contributors choose whether to participate.

---

## 12. Competitive Positioning

| Platform | Model | CrowdForge Difference |
|---|---|---|
| YouTube Partner | 55% to creator, 45% to platform | CrowdForge: 100% to ensemble, $0 to platform |
| Patreon | 5-12% commission | CrowdForge: 0% commission |
| Apple App Store | 30% commission | CrowdForge: 0% commission |
| Upwork/Fiverr | Transactional (one client, one freelancer) | CrowdForge: collaborative (many contributors, one Scene, shared revenue) |
| Gitcoin | Crypto-based bounties | CrowdForge: traditional payments, no crypto, non-technical contributors welcome |
| Colony.io | DAO with token incentives | CrowdForge: no tokens, no blockchain, simpler legal structure |
| Open Collective | Fiscal hosting + transparency tools | CrowdForge: full product lifecycle (build, deploy, earn), not just financial infrastructure |
| Stocksy | Co-op, 50% to creator + dividends | CrowdForge: 100% to ensemble, no platform cut at all |

The zero-commission model is the headline differentiator. But the deeper moat is the combination: zero commission + karma-weighted distribution + tiered dividends + managed deployment + real-time collaboration. No existing platform offers this full stack.

---

## 13. Key Metrics

| Metric | What It Measures | Target |
|---|---|---|
| **GMV** | Total revenue generated by all Scenes | Growth indicator |
| **Platform Revenue** | Infra fees + Pro + donations (not Scene revenue) | Must cover operating costs |
| **Active Scenes** | Scenes with >= 1 riff in last 30 days | Engagement health |
| **Revenue-Generating Scenes** | Scenes earning > $0/month | Product-market fit signal |
| **Scene Success Rate** | % of Scenes generating > $100/mo within 6 months | Quality indicator |
| **Payout Ratio** | Total paid to ensemble / total GMV | Target ~97% (100% minus Stripe fees) |
| **Ensemble Member LTV** | Lifetime karma + revenue received + Scenes contributed to | Retention signal |
| **Pro Conversion Rate** | Pro subscribers / total ensemble members | Revenue sustainability |
| **Donation Rate** | Monthly donations / monthly operating costs | Cultural health |
| **Infrastructure Attach Rate** | % of Scenes on paid hosting tiers | Revenue predictability |

---

## 14. Risks and Mitigations

### "What if nobody's Scene makes money?"

The biggest risk. If Scenes don't generate revenue, karma is a game with no prize. Mitigation: curate early Scenes for revenue viability, provide monetization playbooks, surface revenue-generating Scenes prominently, and ensure that the non-financial value of karma (tier status, hiring pipeline, governance power) provides independent motivation.

### "How do you survive the 0-to-break-even period?"

Seed funding. The model requires ~$2-3M to reach Phase 3. This is a standard startup funding requirement. The pitch to investors: zero-commission platforms attract disproportionate creator supply (as YouTube and Substack demonstrated by taking smaller cuts than incumbents), and the infrastructure/subscription revenue model has proven unit economics.

### "What stops someone from forking a Scene off-platform?"

Nothing, fully. But: karma history stays on CrowdForge, the ensemble doesn't follow, revenue-sharing infrastructure is non-trivial to replicate, and license terms can require attribution. The deeper defense is switching cost -- moving means losing deployment, analytics, ensemble management, payment infrastructure, and contributor karma history.

### "What about the Howey Test?"

The structural defenses are strong (no money invested, active participation required, service compensation framing). But this requires securities counsel review before launch. The tier system's "dividend rate multiplier" language is internal-only; contributor-facing materials say "revenue share."

### "Is the donation model realistic?"

Wikipedia raises $188M/year from donations. Mozilla generates $500M+ (mostly search deals, but significant donations). The donation model works when: (a) the platform is genuinely valuable to its users, (b) costs are transparently published, and (c) there's a social norm around contribution. CrowdForge's karma-linked donation prompts create that social norm. But donations are the third revenue stream, not the first -- infrastructure fees and Pro subscriptions carry the economic weight.

---

## 15. Implementation Phases

### Phase 1: Foundation (Launch)

- Stripe Connect integration (Express accounts, destination charges)
- Revenue event ingestion (webhooks to append-only ledger)
- Basic payout calculation (monthly, direct karma share, no tier multipliers yet)
- ACH payouts via Stripe
- W-9 collection via Trolley
- Revenue dashboard (per-Scene)
- Payout breakdown display (contributor dashboard)
- Audit log

### Phase 2: Full Payout Engine (Month 3-6)

- Tier multiplier integration (weighted karma formula)
- Vesting schedule enforcement
- Holdback mechanism (80/20 split, 30-day escrow)
- PayPal and Wise payouts
- W-8BEN collection + non-US support
- Weekly payouts (Pro plan)
- 3-month revenue smoothing
- Scene reinvestment governance

### Phase 3: Scale and Compliance (Month 6-12)

- 1099-NEC auto-generation and e-filing
- VAT/GST collection on platform fees (Stripe Tax)
- Revenue reconciliation automation
- Contribution velocity floor
- Scene merge governance
- Scene hibernation mechanics
- Contributor earnings projections

### Phase 4: Maturity (Month 12+)

- Custom Stripe accounts for high-revenue Scenes
- Advanced revenue analytics (cohort analysis, churn impact)
- Tipalti migration for enterprise compliance
- Additional country support
- API for third-party integrations (accounting, tax prep)
- Transparent cost dashboard for donations

---

## 16. Open Decisions

These require input before implementation:

1. **Platform-as-contributor vs. separate billing.** The existing docs contain two conflicting models: (a) the platform earns karma for infrastructure contributions and receives revenue share through the same mechanism as contributors, and (b) infrastructure costs are billed separately and the platform takes zero karma. This document adopts model (b) -- separate billing, zero platform karma -- because it is cleaner, more transparent, and aligns with the founder's explicit constraint that the platform does not participate in revenue sharing. Model (a) was explored in the karma-economics doc but introduces complexity (how much karma does "hosting" earn?) and opacity (contributors can't easily verify the platform's karma is fair). The separate-billing model makes costs visible and avoidable.

2. **Tier multiplier spread.** The current [0, 0.5, 1.0, 1.5, 2.0, 2.5] spread creates a 5x differential between Tier 1 and Tier 5. The karma-economics doc recommends compressing to [0, 0.7, 1.0, 1.3, 1.7, 2.2] (3.1x spread). The wider spread drives tier-grinding behavior (good for retention) but increases resentment from lower-tier contributors (bad for newcomer experience). This is a judgment call that should be tested with the first ensemble cohort.

3. **Donation mechanics.** Should donations be structured as monthly recurring (GitHub Sponsors model) or one-time campaign-style (Wikipedia model)? Recurring provides predictability; campaigns create urgency. A hybrid -- recurring with annual transparency campaigns -- may be optimal.

4. **AI agent payout routing.** AI agents earn karma, but payouts go to the human operator. Should there be a per-agent reporting view, or should all agent earnings aggregate into the operator's dashboard? Per-agent reporting is useful for operators running multiple agents but adds UI complexity.

5. **Scene revenue attribution for sales.** The default is last-touch attribution (whoever closed the deal gets sales karma). Multi-touch attribution is more accurate but harder to implement and verify. Start with last-touch; revisit when Scenes reach $50K+/month where attribution disputes become material.
