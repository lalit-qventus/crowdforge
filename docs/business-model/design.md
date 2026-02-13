# CrowdForge Business Model

## Core Revenue Architecture

CrowdForge operates on a zero-commission, donation-backed model. The platform takes zero commission from Scene revenue and earns zero karma on Scenes. 100% of every dollar a Scene earns goes to the ensemble that built it. Platform operations are funded by voluntary community donations, infrastructure hosting fees, and optional premium subscriptions.

This is the Wikipedia model applied to a creative platform: transparent about costs, sustained by the community it serves, with additional revenue from hosting infrastructure that Scenes need anyway.

### Zero Commission Means Zero

100% of Scene revenue flows to karma-weighted ensemble members. The platform does not participate in karma-based revenue sharing. The platform does not earn karma. There is no hidden take.

**How this compares:**

| Platform | Model | CrowdForge Difference |
|---|---|---|
| Apple App Store | 30% commission | CrowdForge takes 0% — ensemble keeps everything |
| Google Play | 15-30% commission | CrowdForge takes 0% — ensemble keeps everything |
| Substack | 10% commission | CrowdForge takes 0% — ensemble keeps everything |
| Patreon | 5-12% commission | CrowdForge takes 0% — ensemble keeps everything |
| YouTube (ads) | 45% commission | CrowdForge takes 0% — ensemble keeps everything |

### Revenue Streams

**PRIMARY: Voluntary Community Donations**
Karma-linked social expectation, not a requirement. Higher karma tiers have a social norm to contribute, but donation is never forced and never gates features. A transparent cost dashboard shows the community exactly what it costs to run CrowdForge each month: "This is what it costs to run CrowdForge this month. Contribute if you can."

**SECONDARY: Infrastructure Hosting Fees**
Scenes are hosted on CrowdForge's managed infrastructure. These are direct cost pass-throughs, not profit centers.

| Tier | Monthly Cost | Includes |
|---|---|---|
| Starter (free) | $0 | Shared hosting, 1GB storage, 10GB bandwidth, custom subdomain |
| Growth | $15/mo | Dedicated resources, 10GB storage, 100GB bandwidth, custom domain, SSL |
| Scale | $50/mo | Auto-scaling, 50GB storage, 500GB bandwidth, staging environments |
| Enterprise | $200/mo | Dedicated infrastructure, SLA, priority support, compliance features |

**Unit economics of hosting:** Using Railway/Render-class infrastructure, a typical small Scene costs CrowdForge ~$3-8/month to host. The Growth tier at $15/mo produces ~$7-12/mo margin per Scene. At scale, bulk infrastructure pricing drops per-Scene costs further.

Infrastructure fees are billed separately to the Scene, not deducted from revenue. If a Scene earns $0, the Scene creator is responsible for infrastructure costs above the Starter tier, or the Scene downgrades to Starter automatically.

**TERTIARY: Optional Pro Subscription (CrowdForge Pro)**

Individual ensemble member subscriptions, not per-Scene.

| Feature | Free | Pro ($12/mo) |
|---|---|---|
| Contribute to Scenes | Yes | Yes |
| Karma tracking | Basic | Advanced analytics, trends, projections |
| Scene creation | 1 active | Unlimited |
| Deployment speed | Queued | Priority |
| AI agent hours | 10 hrs/mo | 50 hrs/mo |
| Private Scenes | No | Yes |
| Priority support | No | Yes |
| Profile badge | No | Yes |

---

## Revenue Flow Mechanics

### The Money Pipeline

```
Customer pays for product/service
        |
        v
  Gross Revenue (100%)
        |
        v
  Payment processing fees deducted (~3%)
        |
        v
  100% to karma-weighted ensemble
```

Infrastructure fees are billed separately to the Scene, not deducted from revenue.

### Payout Rules

**Minimum payout threshold:** $25. Below this, earnings accumulate until the threshold is reached. This avoids micro-transaction processing costs eating into ensemble earnings.

**Payout frequency:** Monthly, on the 15th, for earnings accrued through the last day of the previous month. Ensemble members can request weekly payouts on the Pro plan.

**Payment methods:**
- ACH / bank transfer (US) — free
- PayPal — free (PayPal charges the recipient their own fees)
- Wise (international) — platform covers transfer fees up to $5
- Stripe Connect payouts — free

**Holdback period:** New ensemble members have a 30-day holdback on their first payout. This prevents fraud schemes where someone riffs spam, claims karma, cashes out, and disappears.

**Revenue from multiple Scenes:** A single ensemble member can earn from many Scenes. All earnings aggregate into one monthly payout, regardless of how many Scenes they contributed to.

### Example Revenue Flow

A SaaS product on CrowdForge earns $10,000/month in subscription revenue:

| Line Item | Amount |
|---|---|
| Gross revenue | $10,000 |
| Payment processing (~3%) | -$300 |
| Distributed to ensemble | $9,700 (100%) |

Infrastructure fees (e.g., Scale tier at $50/mo) are billed separately to the Scene and do not reduce the ensemble's revenue share.

If ensemble member Alice holds 12% of the Scene's weighted karma:
- Alice's share: $9,700 x 0.12 = **$1,164/month**

The platform receives $0 from this Scene's revenue. The platform's costs are covered by donations, Alice's optional Pro subscription, and the Scene's infrastructure tier fee.

---

## Legal Structure

### Contributor Classification: Independent Contractors

Ensemble members are **independent contractors**, not employees. This is the same legal framework used by Twitch, YouTube, Uber, and every gig platform.

**Why this works for CrowdForge:**
- Ensemble members choose when, how, and how much to work
- Ensemble members can work on multiple Scenes simultaneously
- No exclusivity requirements
- No set schedules or minimum hours
- Ensemble members provide their own tools (their computers, internet)
- The platform provides the marketplace, not the direction of work

**Tax documentation:**
- US ensemble members: W-9 on signup, 1099-NEC issued for earnings > $600/year
- Non-US ensemble members: W-8BEN on signup, no 1099 required (income is sourced to the ensemble member's country)
- Platform uses a tax compliance vendor (e.g., Trolley/Tipalti) to automate form collection and filing

### Revenue Sharing Agreement (RSA)

Every ensemble member who joins a Scene signs a Revenue Sharing Agreement. This is a standard contract — not an equity grant, not a security, not an investment.

**Key terms of the RSA:**
- Ensemble member earns a share of Scene net revenue proportional to their karma percentage
- Karma is computed by the platform's algorithm, not by subjective human judgment
- No guaranteed minimum payment
- Agreement can be terminated by either party at any time
- Ensemble member retains no ownership stake in the Scene
- Revenue share is compensation for services rendered, not a return on investment

### Avoiding Securities Classification (The Howey Test)

This is the single biggest legal risk. The SEC's Howey Test classifies something as a security if it involves: (1) investment of money, (2) in a common enterprise, (3) with expectation of profits, (4) primarily from the efforts of others.

**CrowdForge's position on each prong:**

| Prong | Risk | Mitigation |
|---|---|---|
| Investment of money | LOW | Ensemble members invest time/effort, not money. No one buys karma. No financial investment required. |
| Common enterprise | MEDIUM | Scenes are collaborative, which could be seen as a common enterprise. Mitigated by: each ensemble member's return is tied to their own karma (their own effort), not pooled investment returns. |
| Expectation of profits | MEDIUM | Ensemble members do expect to earn money. But this is compensation for work, like a freelancer expecting payment — not investment returns. |
| Efforts of others | LOW | This is the strongest defense. Ensemble members earn karma through their OWN active participation. Karma decays without continued contribution. You cannot passively hold karma and collect revenue — you must actively work. This is fundamentally different from passive investing. |

**Structural safeguards:**
- Karma is non-transferable (cannot be sold, traded, or gifted)
- Karma decays over time, requiring ongoing contribution
- No one can "buy in" to a Scene's revenue stream
- Revenue share is explicitly framed as service compensation, not investment returns
- Ensemble members must actively participate — there is no passive income mode

**Legal precedent:** This structure closely mirrors the YouTube Partner Program and Twitch Affiliate Program, both of which operate at massive scale without securities classification. The key differentiator is active participation: ensemble members earn through work, not through capital deployment.

**Recommendation:** Engage securities counsel before launch to review the RSA template. The structure is sound, but a formal legal opinion letter provides protection.

### International Operations

**Entity structure:** US C-Corp (Delaware incorporation) as the platform operator. This is standard for tech platforms operating globally.

**International payments:**
- Wise Business or Stripe Connect for cross-border payouts
- Each country has its own tax rules for contractor income — the ensemble member is responsible for their local tax obligations
- Platform collects W-8BEN from non-US ensemble members and does not withhold US taxes on income sourced outside the US (per IRS rules, the work location determines income source)
- VAT/GST: The platform charges applicable taxes on subscription fees and infrastructure fees based on the ensemble member's country. Revenue share payouts are not subject to VAT (they are B2B service compensation).

**Countries with restrictions:** Some countries have foreign income restrictions or require local entity registration. The platform should start with a supported country list (US, EU, UK, Canada, Australia, India, Brazil) and expand as legal review permits.

---

## Unit Economics

### Cost Structure (Monthly, at Scale)

| Cost Category | Per Scene (avg) | Notes |
|---|---|---|
| Hosting infrastructure | $5 | Blended average across tiers |
| Payment processing | ~3% of GMV | Stripe fees |
| Tax compliance (Tipalti/Trolley) | $2-5/ensemble member/mo | Scales with ensemble size |
| Karma computation | $0.50 | Background job processing |
| Support | $1 | Amortized across Scenes |
| **Total per Scene** | **~$10 + 3% GMV** | |

### Break-Even Analysis

The donation-backed model requires honest accounting. At small scale, donations alone will not cover platform costs. Seed funding or bootstrapping is necessary in the early phases. The model becomes viable as the community grows large enough that donations, infrastructure fees, and Pro subscriptions collectively cover operating costs.

**Fixed costs:**

| Fixed Cost | Monthly |
|---|---|
| Core team (5 engineers, 2 ops) | $120,000 |
| Legal/compliance | $10,000 |
| Office/tools/misc | $5,000 |
| Marketing | $15,000 |
| **Total fixed** | **$150,000/mo** |

**Revenue sources at scale (5,000 Scenes, 50,000 ensemble members):**

| Source | Estimate | Assumptions |
|---|---|---|
| Infrastructure fees | $45,000/mo | ~3,000 Scenes above Starter tier, avg $15/mo |
| Pro subscriptions | $60,000/mo | ~5,000 Pro subscribers at $12/mo (10% conversion) |
| Community donations | $50,000+/mo | Social norm among 50,000 ensemble members |
| **Total** | **$155,000+/mo** | |

At scale, infrastructure fees alone may approach break-even. Donations are the cultural contract — the community's way of saying "this platform matters." Pro subscriptions cover the gap. This is not a model that works at 500 users. It requires reaching community scale, which means seed funding covers the early phases.

### Growth Model

**Phase 1 (0-6 months): Dogfooding**
- The platform itself is the first Scene
- Target: 50-200 ensemble members building CrowdForge on CrowdForge
- Revenue: $0 (platform not monetized yet)
- Funded by: Seed round or founder bootstrapping

**Phase 2 (6-18 months): Early Scenes**
- Open to public, curated Scene list
- Target: 500 Scenes, 5,000 ensemble members
- Revenue: ~$15K/month (infrastructure fees + early Pro subscriptions)
- Operating at a loss, subsidized by funding

**Phase 3 (18-36 months): Growth**
- Self-serve Scene creation, marketplace dynamics
- Target: 5,000 Scenes, 50,000 ensemble members
- Revenue: ~$155K/month (infrastructure + Pro + donations)
- Approaching profitability

**Phase 4 (36+ months): Scale**
- 50,000+ Scenes, 500,000+ ensemble members
- Revenue: $1M+/month
- Profitable, expanding internationally and into enterprise

---

## Competitive Analysis

### Direct Competitors

| Platform | Model | CrowdForge Differentiator |
|---|---|---|
| **Replit Bounties** | One-off task bounties paid in Cycles | CrowdForge offers ongoing revenue sharing, not one-time payments. Ensemble members build equity-like stakes through karma. |
| **Gitcoin** | Crypto-based bounties for open source | CrowdForge uses traditional payments (no crypto). Lower barrier to entry. Works for non-technical ensemble members too. |
| **Colony.io** | DAO infrastructure with token incentives | CrowdForge avoids crypto/tokens entirely. Simpler legal structure. Accessible to mainstream users. |
| **Algora** | Bounties for open source with GitHub integration | CrowdForge goes beyond bounties — full Scene lifecycle from idea to deployment to revenue. |
| **Upwork/Fiverr** | Traditional freelance marketplace | CrowdForge is collaborative (many people build one thing together), not transactional (one client hires one freelancer). Revenue sharing vs. fixed payment. |

### The Moat

CrowdForge's defensibility comes from three compounding effects:

**1. Karma Network Effects**
An ensemble member's karma history across Scenes becomes their reputation. The more Scenes someone contributes to successfully, the more valuable their profile becomes — and the harder it is to replicate on another platform. This is the same lock-in that makes LinkedIn profiles valuable: years of accumulated professional history.

**2. Deployment Lock-In**
Scenes are deployed on CrowdForge infrastructure. Moving a Scene off-platform means losing the deployment pipeline, the analytics, the ensemble management, and the revenue-sharing automation. This is similar to Shopify's lock-in: you *can* leave, but the switching cost is high.

**3. Revenue Gravity**
Once a Scene is earning revenue and distributing it to the ensemble, there is enormous inertia against moving. Every ensemble member has a financial interest in the Scene staying on CrowdForge. Moving platforms means re-negotiating revenue splits, re-implementing payment infrastructure, and risking ensemble attrition.

---

## Bootstrapping Strategy

### The Dogfooding Play

The founder's instinct is correct: CrowdForge should be the first Scene built on CrowdForge.

**How this works:**
1. The platform starts as a minimal viable product — Scene creation, basic karma tracking, manual deployment
2. All platform development is tracked as riffs on the "CrowdForge" Scene
3. Early ensemble members earn karma on the CrowdForge Scene itself
4. When the platform starts generating revenue (from donations and infrastructure fees), CrowdForge-the-Scene pays out to its own ensemble

This creates a powerful narrative: "The people who built this platform earn revenue from it, just like you'll earn revenue from your Scenes."

### Attracting the First 100 Ensemble Members

**Strategy 1: Seeded Scenes (most important)**
Launch with 3-5 pre-selected Scene ideas that have clear revenue potential. Examples:
- A SaaS tool (landing page builder, form tool, analytics dashboard)
- A content site (niche newsletter, directory, resource hub)
- A developer tool (API, SDK, CLI utility)

These seeded Scenes give ensemble members something concrete to riff on immediately, rather than staring at an empty platform.

**Strategy 2: Indie Hacker / Open Source Community**
Target communities that already think about building products collaboratively:
- Hacker News "Show HN" crowd
- r/SideProject, r/indiehackers
- Dev.to, Hashnode
- Open source contributors on GitHub who want to monetize their work

**Strategy 3: Content-Driven Launch**
Document the building of CrowdForge publicly. "Building a startup where people build startups together" is inherently interesting content. Post build logs, revenue transparency reports, and ensemble member spotlights.

**Strategy 4: Micro-bounties for First Riffs**
Offer small guaranteed payouts ($10-50) for first-time ensemble members on seeded Scenes, funded by the platform. This reduces the risk of contributing to an unproven platform. These are marketing costs, not ongoing subsidies.

### The Viral Loop

```
Ensemble member joins Scene
        |
        v
  Riffs on the Scene, earns karma
        |
        v
  Scene launches, earns revenue
        |
        v
  Ensemble member receives payout (real money!)
        |
        v
  Ensemble member shares on social media
  ("I earned $X from a Scene I helped build with people")
        |
        v
  New ensemble members join
        |
        v
  More Scenes get built
        |
        v
  More revenue generated
        |
        v
  Repeat
```

The viral moment is the **first payout**. When someone receives real money for riffing on a Scene they didn't start and don't own, that's a story worth sharing. The platform should make payout moments shareable (e.g., "I earned $347 this month from 3 CrowdForge Scenes" — shareable card with Scene names and karma rank).

---

## Skeptical Investor Q&A

### "What if nobody's Scene makes money?"

This is the biggest risk. If Scenes don't generate revenue, the karma system is a game with no prize, and ensemble members leave.

**Mitigation:**
- Curate early Scenes for revenue viability (not just cool ideas)
- Provide templates/playbooks for monetization (how to add payments, how to price, how to market)
- Platform provides deployment and a basic storefront — reducing the gap between "built" and "earning"
- Highlight revenue-generating Scenes prominently to set expectations

### "How do you prevent someone from forking a Scene off-platform?"

You can't, fully. But:
- The karma history stays on CrowdForge — the ensemble doesn't follow
- Revenue-sharing infrastructure is non-trivial to replicate
- If a Scene forks off, it loses all its ensemble members and their ongoing riffs
- License terms can require attribution and revenue-sharing for derivatives

### "Isn't this just Upwork with extra steps?"

No. Upwork is transactional: one client, one freelancer, one job, one payment. CrowdForge is collaborative: many ensemble members, one Scene, ongoing revenue, proportional sharing. The unit of work on Upwork is a "gig." The unit of work on CrowdForge is a "riff on a living Scene."

### "What about ensemble disputes over karma allocation?"

The karma algorithm is deterministic and transparent (see Karma System design doc). Ensemble members can see exactly why they have the karma they have. Disputes are about the algorithm's fairness, not about subjective human judgment. The platform can adjust the algorithm based on community governance, but individual karma scores are not manually adjustable.

### "With zero commission AND no karma earning, how does the platform survive?"

Three revenue streams: voluntary community donations, infrastructure hosting fees, and optional Pro subscriptions.

**Donations** are the cultural contract. Like Wikipedia, CrowdForge publishes a transparent cost dashboard: "This is what it costs to run CrowdForge. Here's what we've received. Contribute if you can." Higher karma tiers carry a social expectation to donate, but it's never forced and never gates features. Wikipedia raises $150M+/year from donations. CrowdForge needs a fraction of that.

**Infrastructure fees** are the steady-state business model. Every Scene above the free tier pays $15-200/month for hosting. At 5,000 Scenes, this alone generates $45K+/month. At 50,000 Scenes, infrastructure fees could cover all operating costs without a single donation.

**Pro subscriptions** ($12/mo) provide advanced analytics, priority deployment, private Scenes, and more AI agent hours. At 10% conversion of ensemble members, this is a meaningful revenue stream.

At small scale, this model does not self-sustain — seed funding is necessary. At community scale, it works. The bet is that a platform giving 100% of revenue to creators will attract enough creators to reach that scale.

### "What about AI agents as contributors? Do they get paid?"

AI agents earn karma like any other ensemble member. The revenue share for AI agent riffs goes to the agent's owner (the person or organization that deployed the agent). This is no different from a company deploying a contractor — the entity deploying the resource receives the compensation.

The platform charges for AI agent compute time (see Premium Subscriptions), which is a separate revenue stream.

---

## Summary of Revenue Streams

| Stream | Type | Notes |
|---|---|---|
| Community donations | Voluntary | Karma-linked social norm, transparent cost dashboard |
| Infrastructure fees | Recurring | Hosting tiers ($0-200/mo per Scene) |
| Pro subscriptions ($12/mo) | Recurring | Per-ensemble-member premium features |
| Enterprise/white-label | Recurring | Long-term expansion |

## Key Metrics to Track

- **GMV (Gross Merchandise Value):** Total revenue generated by all Scenes
- **Platform Revenue:** Donations + infrastructure fees + subscriptions (NOT from Scene revenue)
- **Active Scenes:** Scenes with at least 1 riff in the last 30 days
- **Revenue-Generating Scenes:** Scenes earning > $0/month
- **Ensemble Member LTV:** Lifetime value of an ensemble member (karma earned, Scenes contributed to, revenue received)
- **Payout Ratio:** Total paid to ensemble / total GMV — should be ~97% (100% minus payment processing fees)
- **Scene Success Rate:** % of Scenes that generate > $100/month within 6 months of creation
- **Donation Rate:** Monthly donations / monthly operating costs — target > 1.0 at scale
- **Infrastructure Attach Rate:** % of Scenes on paid hosting tiers
