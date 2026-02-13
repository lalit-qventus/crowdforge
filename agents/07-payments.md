# Agent: Payments & Revenue

## Mission
Build CrowdForge's payment infrastructure — the system that collects revenue from projects and distributes it to contributors based on karma. This is the part that makes CrowdForge real: people get paid for building startups with strangers. It must be legally sound, tax-compliant, and transparent.

## What to Build

### Revenue Collection
- Stripe integration for project monetization (subscriptions, one-time payments, invoicing)
- Each project gets its own Stripe Connected Account (or sub-merchant)
- Revenue tracking dashboard per project (real-time GMV, net revenue, karma-weighted distribution)

### Payout Distribution
- Monthly payout cycle (15th of each month for previous month's earnings)
- Calculation: `payout = project_net_revenue * contributor_pool_pct * (contributor_weighted_karma / total_weighted_karma)`
- Weighted karma = `karma * tier_multiplier` (see karma engine doc)
- Minimum payout threshold: $25 (accumulates until reached)
- 20% holdback for 30 days (fraud clawback window)
- Weekly payouts available on Pro plan

### Payment Methods
- ACH / bank transfer (US) — free
- PayPal — free (recipient pays PayPal fees)
- Wise (international) — platform covers fees up to $5
- Stripe Connect payouts

### Tax Compliance
- US contributors: W-9 collection, 1099-NEC for earnings > $600/year
- Non-US contributors: W-8BEN collection
- Use Tipalti or Trolley for automated tax form collection and filing
- VAT/GST on platform fees (subscriptions, infrastructure) based on contributor country

### Revenue Split
- 100% of project revenue flows to karma-weighted contributors
- Zero platform commission — the platform earns its share through karma (it's a contributor too, earning karma for hosting, tooling, and infrastructure)
- No separate treasury allocation

### Legal
- Revenue Sharing Agreement (RSA) template — signed by every contributor joining a project
- Contributors = independent contractors (not employees, not investors)
- Defeats Howey Test: karma is non-transferable, requires active participation, cannot be purchased
- Get securities counsel review before launch

## Reference Docs
- `../docs/business-model/design.md` — revenue flow, legal structure, unit economics, tax details
- `../docs/karma-system/design.md` — karma-to-revenue conversion, worked example
- `../docs/value-pricing/analysis.md` — tier multiplier system

## Constraints
- Every payout must be traceable to specific karma calculations
- Transparent: contributors see exact breakdown of how their payout was computed
- Multi-currency support from day one (USD primary, convert at payout time)
- Compliance with supported country list initially: US, EU, UK, Canada, Australia, India, Brazil
