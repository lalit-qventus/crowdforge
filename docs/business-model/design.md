# CrowdForge Business Model

## Core Revenue Architecture

CrowdForge earns money three ways: a cut of every project's revenue, infrastructure fees for hosting, and premium subscriptions.

### Platform Take Rate: 15%

The platform takes 15% of gross project revenue before distributing the remaining 85% to the contributor pool.

**Rationale for 15%:**

| Platform | Take Rate | What They Provide |
|---|---|---|
| Apple App Store | 30% | Distribution, payments, review |
| Google Play | 15-30% | Distribution, payments, review |
| Substack | 10% | Hosting, payments, newsletter delivery |
| Patreon | 5-12% (legacy), 10% (new) | Payments, membership tools |
| Gumroad | 10% + processing | Storefront, payments |
| YouTube (ads) | 45% | Distribution, ads infrastructure, audience |

CrowdForge provides more than Substack/Patreon (hosting, deployment, CI/CD, team coordination, karma tracking, fraud prevention, analytics) but less than Apple (no captive audience of billions). 15% sits in the fair middle ground. It's low enough that contributors don't feel gouged, high enough to fund platform operations and growth.

**What the 15% covers:**
- Payment processing (Stripe fees ~2.9% + $0.30 absorbed by the platform)
- Karma computation infrastructure
- Fraud prevention systems
- Project analytics dashboards
- Legal/tax compliance infrastructure

### Infrastructure Fees

Projects are hosted on CrowdForge's managed infrastructure. This is not optional — part of the platform's value proposition is that deployment and hosting are handled automatically.

| Tier | Monthly Cost | Includes |
|---|---|---|
| Starter (free) | $0 | Shared hosting, 1GB storage, 10GB bandwidth, custom subdomain |
| Growth | $15/mo | Dedicated resources, 10GB storage, 100GB bandwidth, custom domain, SSL |
| Scale | $50/mo | Auto-scaling, 50GB storage, 500GB bandwidth, staging environments |
| Enterprise | $200/mo | Dedicated infrastructure, SLA, priority support, compliance features |

**Unit economics of hosting:** Using Railway/Render-class infrastructure, a typical small project costs CrowdForge ~$3-8/month to host. The Growth tier at $15/mo produces ~$7-12/mo margin per project. At scale, bulk infrastructure pricing drops per-project costs further.

Infrastructure fees are paid from project revenue before the contributor split. If a project earns $0, the project creator is responsible for infrastructure costs above the Starter tier, or the project downgrades to Starter automatically.

### Premium Subscriptions (CrowdForge Pro)

Individual contributor subscriptions, not per-project.

| Feature | Free | Pro ($12/mo) |
|---|---|---|
| Contribute to projects | Yes | Yes |
| Karma tracking | Basic | Advanced analytics, trends, projections |
| Project creation | 1 active | Unlimited |
| Deployment speed | Queued | Priority |
| AI agent hours | 10 hrs/mo | 50 hrs/mo |
| Private projects | No | Yes |
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
  Payment processor fees (absorbed by platform from its cut)
        |
        v
  Infrastructure costs deducted (hosting tier)
        |
        v
  Net Project Revenue
        |
   +----+----+
   |         |
   v         v
Platform   Contributor
  15%       Pool 85%
             |
             v
   Distributed by karma
   proportional to each
   contributor's share
```

### Payout Rules

**Minimum payout threshold:** $25. Below this, earnings accumulate until the threshold is reached. This avoids micro-transaction processing costs eating into contributor earnings.

**Payout frequency:** Monthly, on the 15th, for earnings accrued through the last day of the previous month. Contributors can request weekly payouts on the Pro plan.

**Payment methods:**
- ACH / bank transfer (US) — free
- PayPal — free (PayPal charges the recipient their own fees)
- Wise (international) — platform covers transfer fees up to $5
- Stripe Connect payouts — free

**Holdback period:** New contributors have a 30-day holdback on their first payout. This prevents fraud schemes where someone contributes spam, claims karma, cashes out, and disappears.

**Revenue from multiple projects:** A single contributor can earn from many projects. All earnings aggregate into one monthly payout, regardless of how many projects they contributed to.

### Example Revenue Flow

A SaaS product on CrowdForge earns $10,000/month in subscription revenue:

| Line Item | Amount |
|---|---|
| Gross revenue | $10,000 |
| Infrastructure (Scale tier) | -$50 |
| Net project revenue | $9,950 |
| Platform cut (15%) | -$1,492.50 |
| Contributor pool | $8,457.50 |

If contributor Alice holds 12% of the project's karma:
- Alice's share: $8,457.50 x 0.12 = **$1,014.90/month**

---

## Legal Structure

### Contributor Classification: Independent Contractors

Contributors are **independent contractors**, not employees. This is the same legal framework used by Twitch, YouTube, Uber, and every gig platform.

**Why this works for CrowdForge:**
- Contributors choose when, how, and how much to work
- Contributors can work on multiple projects simultaneously
- No exclusivity requirements
- No set schedules or minimum hours
- Contributors provide their own tools (their computers, internet)
- The platform provides the marketplace, not the direction of work

**Tax documentation:**
- US contributors: W-9 on signup, 1099-NEC issued for earnings > $600/year
- Non-US contributors: W-8BEN on signup, no 1099 required (income is sourced to the contributor's country)
- Platform uses a tax compliance vendor (e.g., Trolley/Tipalti) to automate form collection and filing

### Revenue Sharing Agreement (RSA)

Every contributor who joins a project signs a Revenue Sharing Agreement. This is a standard contract — not an equity grant, not a security, not an investment.

**Key terms of the RSA:**
- Contributor earns a share of project net revenue proportional to their karma percentage
- Karma is computed by the platform's algorithm, not by subjective human judgment
- No guaranteed minimum payment
- Agreement can be terminated by either party at any time
- Contributor retains no ownership stake in the project
- Revenue share is compensation for services rendered, not a return on investment

### Avoiding Securities Classification (The Howey Test)

This is the single biggest legal risk. The SEC's Howey Test classifies something as a security if it involves: (1) investment of money, (2) in a common enterprise, (3) with expectation of profits, (4) primarily from the efforts of others.

**CrowdForge's position on each prong:**

| Prong | Risk | Mitigation |
|---|---|---|
| Investment of money | LOW | Contributors invest time/effort, not money. No one buys karma. No financial investment required. |
| Common enterprise | MEDIUM | Projects are collaborative, which could be seen as a common enterprise. Mitigated by: each contributor's return is tied to their own karma (their own effort), not pooled investment returns. |
| Expectation of profits | MEDIUM | Contributors do expect to earn money. But this is compensation for work, like a freelancer expecting payment — not investment returns. |
| Efforts of others | LOW | This is the strongest defense. Contributors earn karma through their OWN active participation. Karma decays without continued contribution. You cannot passively hold karma and collect revenue — you must actively work. This is fundamentally different from passive investing. |

**Structural safeguards:**
- Karma is non-transferable (cannot be sold, traded, or gifted)
- Karma decays over time, requiring ongoing contribution
- No one can "buy in" to a project's revenue stream
- Revenue share is explicitly framed as service compensation, not investment returns
- Contributors must actively participate — there is no passive income mode

**Legal precedent:** This structure closely mirrors the YouTube Partner Program and Twitch Affiliate Program, both of which operate at massive scale without securities classification. The key differentiator is active participation: contributors earn through work, not through capital deployment.

**Recommendation:** Engage securities counsel before launch to review the RSA template. The structure is sound, but a formal legal opinion letter provides protection.

### International Operations

**Entity structure:** US C-Corp (Delaware incorporation) as the platform operator. This is standard for tech platforms operating globally.

**International payments:**
- Wise Business or Stripe Connect for cross-border payouts
- Each country has its own tax rules for contractor income — the contributor is responsible for their local tax obligations
- Platform collects W-8BEN from non-US contributors and does not withhold US taxes on income sourced outside the US (per IRS rules, the work location determines income source)
- VAT/GST: The platform charges applicable taxes on subscription fees and infrastructure fees based on the contributor's country. Revenue share payouts are not subject to VAT (they are B2B service compensation).

**Countries with restrictions:** Some countries have foreign income restrictions or require local entity registration. The platform should start with a supported country list (US, EU, UK, Canada, Australia, India, Brazil) and expand as legal review permits.

---

## Unit Economics

### Cost Structure (Monthly, at Scale)

| Cost Category | Per Project (avg) | Notes |
|---|---|---|
| Hosting infrastructure | $5 | Blended average across tiers |
| Payment processing | ~3% of GMV | Stripe fees |
| Tax compliance (Tipalti/Trolley) | $2-5/contributor/mo | Scales with contributor count |
| Karma computation | $0.50 | Background job processing |
| Support | $1 | Amortized across projects |
| **Total per project** | **~$10 + 3% GMV** | |

### Break-Even Analysis

**Assumptions:**
- Average project revenue: $500/month (many earn $0, a few earn $10K+, power law distribution)
- Average infrastructure tier: Growth ($15/mo)
- Average contributors per project: 8
- Platform take: 15%

**Per-project economics:**
- Platform revenue: $500 x 15% = $75
- Infrastructure revenue: $15
- Total platform revenue per project: $90
- Platform costs per project: ~$25 (hosting + processing + overhead)
- **Gross margin per project: ~$65/month**

**Break-even (covering fixed costs):**

| Fixed Cost | Monthly |
|---|---|
| Core team (5 engineers, 2 ops) | $120,000 |
| Legal/compliance | $10,000 |
| Office/tools/misc | $5,000 |
| Marketing | $15,000 |
| **Total fixed** | **$150,000/mo** |

Break-even at: **$150,000 / $65 = ~2,300 revenue-generating projects**

If only 20% of projects generate revenue (the rest are hobby/experimental), the platform needs ~11,500 total projects to break even.

### Growth Model

**Phase 1 (0-6 months): Dogfooding**
- The platform itself is the first project
- Target: 50-200 contributors building CrowdForge on CrowdForge
- Revenue: $0 (platform not monetized yet)
- Funded by: Seed round or founder bootstrapping

**Phase 2 (6-18 months): Early Projects**
- Open to public, curated project list
- Target: 500 projects, 5,000 contributors
- Revenue: ~$30K/month (assuming 100 revenue-generating projects at $300 avg)
- Operating at a loss, subsidized by funding

**Phase 3 (18-36 months): Growth**
- Self-serve project creation, marketplace dynamics
- Target: 5,000 projects, 50,000 contributors
- Revenue: ~$300K/month
- Approaching profitability

**Phase 4 (36+ months): Scale**
- 50,000+ projects, 500,000+ contributors
- Revenue: $3M+/month
- Profitable, expanding internationally and into enterprise

---

## Competitive Analysis

### Direct Competitors

| Platform | Model | CrowdForge Differentiator |
|---|---|---|
| **Replit Bounties** | One-off task bounties paid in Cycles | CrowdForge offers ongoing revenue sharing, not one-time payments. Contributors build equity-like stakes through karma. |
| **Gitcoin** | Crypto-based bounties for open source | CrowdForge uses traditional payments (no crypto). Lower barrier to entry. Works for non-technical contributors too. |
| **Colony.io** | DAO infrastructure with token incentives | CrowdForge avoids crypto/tokens entirely. Simpler legal structure. Accessible to mainstream users. |
| **Algora** | Bounties for open source with GitHub integration | CrowdForge goes beyond bounties — full project lifecycle from idea to deployment to revenue. |
| **Upwork/Fiverr** | Traditional freelance marketplace | CrowdForge is collaborative (many people build one thing together), not transactional (one client hires one freelancer). Revenue sharing vs. fixed payment. |

### The Moat

CrowdForge's defensibility comes from three compounding effects:

**1. Karma Network Effects**
A contributor's karma history across projects becomes their reputation. The more projects someone contributes to successfully, the more valuable their profile becomes — and the harder it is to replicate on another platform. This is the same lock-in that makes LinkedIn profiles valuable: years of accumulated professional history.

**2. Deployment Lock-In**
Projects are deployed on CrowdForge infrastructure. Moving a project off-platform means losing the deployment pipeline, the analytics, the contributor management, and the revenue-sharing automation. This is similar to Shopify's lock-in: you *can* leave, but the switching cost is high.

**3. Revenue Gravity**
Once a project is earning revenue and distributing it to contributors, there is enormous inertia against moving. Every contributor has a financial interest in the project staying on CrowdForge. Moving platforms means re-negotiating revenue splits, re-implementing payment infrastructure, and risking contributor attrition.

---

## Bootstrapping Strategy

### The Dogfooding Play

The founder's instinct is correct: CrowdForge should be the first project built on CrowdForge.

**How this works:**
1. The platform starts as a minimal viable product — project creation, basic karma tracking, manual deployment
2. All platform development is tracked as contributions to the "CrowdForge" project
3. Early contributors earn karma on the CrowdForge project itself
4. When the platform starts generating revenue (from other projects using it), CrowdForge-the-project pays out to its own contributors

This creates a powerful narrative: "The people who built this platform earn revenue from it, just like you'll earn revenue from your projects."

### Attracting the First 100 Contributors

**Strategy 1: Seeded Projects (most important)**
Launch with 3-5 pre-selected project ideas that have clear revenue potential. Examples:
- A SaaS tool (landing page builder, form tool, analytics dashboard)
- A content site (niche newsletter, directory, resource hub)
- A developer tool (API, SDK, CLI utility)

These seeded projects give contributors something concrete to work on immediately, rather than staring at an empty platform.

**Strategy 2: Indie Hacker / Open Source Community**
Target communities that already think about building products collaboratively:
- Hacker News "Show HN" crowd
- r/SideProject, r/indiehackers
- Dev.to, Hashnode
- Open source contributors on GitHub who want to monetize their work

**Strategy 3: Content-Driven Launch**
Document the building of CrowdForge publicly. "Building a startup where strangers build startups together" is inherently interesting content. Post build logs, revenue transparency reports, and contributor spotlights.

**Strategy 4: Micro-bounties for First Contributions**
Offer small guaranteed payouts ($10-50) for first-time contributors on seeded projects, funded by the platform. This reduces the risk of contributing to an unproven platform. These are marketing costs, not ongoing subsidies.

### The Viral Loop

```
Contributor joins project
        |
        v
  Contributes work, earns karma
        |
        v
  Project launches, earns revenue
        |
        v
  Contributor receives payout (real money!)
        |
        v
  Contributor shares on social media
  ("I earned $X from a project I helped build with strangers")
        |
        v
  New contributors join
        |
        v
  More projects get built
        |
        v
  More revenue generated
        |
        v
  Repeat
```

The viral moment is the **first payout**. When someone receives real money for contributing to a project they didn't start and don't own, that's a story worth sharing. The platform should make payout moments shareable (e.g., "I earned $347 this month from 3 CrowdForge projects" — shareable card with project names and karma rank).

---

## Skeptical Investor Q&A

### "What if nobody's project makes money?"

This is the biggest risk. If projects don't generate revenue, the karma system is a game with no prize, and contributors leave.

**Mitigation:**
- Curate early projects for revenue viability (not just cool ideas)
- Provide templates/playbooks for monetization (how to add payments, how to price, how to market)
- Platform provides deployment and a basic storefront — reducing the gap between "built" and "earning"
- Highlight revenue-generating projects prominently to set expectations

### "How do you prevent someone from forking a project off-platform?"

You can't, fully. But:
- The karma history stays on CrowdForge — the contributor network doesn't follow
- Revenue-sharing infrastructure is non-trivial to replicate
- If a project forks off, it loses all its contributors and their ongoing work
- License terms can require attribution and revenue-sharing for derivatives

### "Isn't this just Upwork with extra steps?"

No. Upwork is transactional: one client, one freelancer, one job, one payment. CrowdForge is collaborative: many contributors, one project, ongoing revenue, proportional sharing. The unit of work on Upwork is a "gig." The unit of work on CrowdForge is a "contribution to a living project."

### "What about contributor disputes over karma allocation?"

The karma algorithm is deterministic and transparent (see Karma System design doc). Contributors can see exactly why they have the karma they have. Disputes are about the algorithm's fairness, not about subjective human judgment. The platform can adjust the algorithm based on community governance, but individual karma scores are not manually adjustable.

### "Does 15% leave enough for contributors to care?"

At 15%, for every $100 a project earns, $85 goes to contributors. Compare:
- YouTube keeps 45% of ad revenue
- App Store keeps 30%
- Even Substack keeps 10% and provides far less infrastructure

A contributor holding 10% karma on a project earning $5,000/month takes home: $5,000 x 85% x 10% = **$425/month**. For side-project-level effort, that's compelling. For a full-time contributor holding 25% karma on a project earning $20,000/month: $20,000 x 85% x 25% = **$4,250/month**. That's a livable income in many countries.

### "What about AI agents as contributors? Do they get paid?"

AI agents earn karma like any other contributor. The revenue share for AI agent contributions goes to the agent's owner (the person or organization that deployed the agent). This is no different from a company deploying a contractor — the entity deploying the resource receives the compensation.

The platform charges for AI agent compute time (see Premium Subscriptions), which is a separate revenue stream from the karma-based revenue share.

---

## Summary of Revenue Streams

| Stream | Type | Expected Contribution |
|---|---|---|
| Platform take (15% of GMV) | Variable | 60% of platform revenue |
| Infrastructure fees | Recurring | 20% of platform revenue |
| Pro subscriptions ($12/mo) | Recurring | 15% of platform revenue |
| Enterprise/white-label | Recurring | 5% of platform revenue (long-term) |

## Key Metrics to Track

- **GMV (Gross Merchandise Value):** Total revenue generated by all projects
- **Platform Revenue:** GMV x 15% + infrastructure + subscriptions
- **Active Projects:** Projects with at least 1 contribution in the last 30 days
- **Revenue-Generating Projects:** Projects earning > $0/month
- **Contributor LTV:** Lifetime value of a contributor (karma earned, projects contributed to, revenue received)
- **Payout Ratio:** Total paid to contributors / total GMV — should stay above 80%
- **Project Success Rate:** % of projects that generate > $100/month within 6 months of creation
