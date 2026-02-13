# CrowdForge Payments & Revenue Infrastructure

## Overview

This document specifies CrowdForge's payment infrastructure end-to-end: how money enters the system from project customers, how it flows through the revenue split engine, and how it exits as payouts to contributors. Every payout is traceable to specific karma calculations. Contributors see the exact breakdown of how their payout was computed.

---

## 1. Revenue Collection

### Stripe Connect Architecture

Every CrowdForge project operates as a sub-merchant via **Stripe Connect** in **platform (destination charges)** mode. CrowdForge is the platform account; each project gets a Connected Account.

```
Customer (pays for product/service)
       |
       v
  Stripe Charge (platform account)
       |
       v
  Destination charge to Project Connected Account
       |
       v
  Platform takes its cut via application_fee_amount
```

**Why destination charges over direct charges:** The platform controls the charge lifecycle — refunds, disputes, and fee calculations stay under CrowdForge's control rather than delegating to individual project owners. This is critical for the holdback and fraud clawback mechanisms.

**Why not separate charges + transfers:** Destination charges create a direct paper trail between customer payment and project account, simplifying reconciliation and tax reporting.

### Connected Account Setup

When a project transitions to the **Shipped** stage (has a live production URL), CrowdForge auto-provisions a Stripe Connected Account:

| Field | Value |
|---|---|
| Account type | `express` (initially), upgradable to `custom` at Scale tier |
| Country | Determined by project Founder's location |
| Business type | `company` (the project entity on CrowdForge) |
| Capabilities | `card_payments`, `transfers` |
| Payout schedule | Manual (CrowdForge controls disbursement timing) |

Express accounts let Stripe handle identity verification of the project Founder — CrowdForge doesn't need to build KYC flows for project-level banking.

### Monetization Primitives

Projects can monetize through any combination of:

| Method | Stripe Product | Use Case |
|---|---|---|
| Subscriptions | Stripe Billing | SaaS products, membership sites |
| One-time payments | Stripe Checkout | Digital products, downloads, one-off purchases |
| Usage-based billing | Stripe Metering | API products, compute, storage |
| Invoicing | Stripe Invoicing | B2B contracts, enterprise deals |
| Donations/tips | Stripe Payment Links | Open source, content creators |

CrowdForge provides pre-built payment components (React components wrapping Stripe Elements) that project builders drop into their apps. These components auto-configure against the project's Connected Account.

### Revenue Event Pipeline

Every successful charge generates a revenue event:

```
Stripe webhook (charge.succeeded)
       |
       v
  Revenue Service ingests event
       |
       v
  Records: project_id, amount_gross, currency, stripe_fee, net_amount, timestamp
       |
       v
  Deduplication check (idempotency_key from Stripe)
       |
       v
  Updates project revenue ledger (append-only)
       |
       v
  Publishes event to real-time feed ("ProjectX earned $49!")
```

**Refund handling:** `charge.refunded` events create negative revenue entries in the ledger. Refunds reduce the revenue pool for the current payout cycle. If a refund occurs after payout, it's deducted from the next cycle (or clawed back from holdback — see Section 3).

**Dispute handling:** `charge.dispute.created` events freeze the disputed amount. If the dispute is lost, it becomes a negative revenue entry. CrowdForge auto-submits dispute evidence using transaction metadata.

### Revenue Tracking Dashboard

Each project's dashboard displays:

- **Gross revenue** — Total charges collected
- **Stripe processing fees** — ~2.9% + $0.30 per transaction (absorbed by platform from its 15% cut)
- **Refunds & chargebacks** — Deductions
- **Infrastructure costs** — Hosting tier fees deducted
- **Net project revenue** — The number that feeds into the split engine
- **Cumulative charts** — Daily, weekly, monthly revenue with trend lines
- **Revenue by source** — Breakdown by subscription/one-time/usage/invoice

All figures update in real-time via WebSocket push from the Revenue Service.

---

## 2. Revenue Split Engine

### The Split

Net project revenue is divided three ways:

| Allocation | Default % | Purpose |
|---|---|---|
| Contributor Pool | 70% | Distributed to contributors proportional to weighted karma |
| Platform Fee | 15% | CrowdForge operations (absorbs Stripe fees, hosting, compliance) |
| Project Treasury | 15% | Reinvestment fund governed by project contributors |

The contributor pool percentage is configurable per-project within **60–80%** bounds. When adjusted, the platform fee stays fixed at 15% and the treasury absorbs the difference:

| Contributor Pool | Platform Fee | Project Treasury |
|---|---|---|
| 60% | 15% | 25% |
| 70% (default) | 15% | 15% |
| 80% | 15% | 5% |

Changes to the split require a governance vote from contributors holding >50% of project karma.

### The Revenue Waterfall

Revenue flows through a strict waterfall before reaching the split:

```
Gross Revenue (100%)
       |
       v
  - Stripe processing fees (~2.9% + $0.30)         [absorbed by platform]
       |
       v
  - Refunds & chargebacks
       |
       v
  - Infrastructure costs (hosting tier)
       |
       v
  = Net Project Revenue
       |
  +----+----+----+
  |         |         |
  v         v         v
Platform  Contributor  Project
  15%     Pool 70%    Treasury 15%
```

Infrastructure costs are deducted before the split — they're a cost of running the project, not a contributor expense. If a project earns $0, the Founder is responsible for infrastructure costs above Starter tier, or the project auto-downgrades.

### Weighted Karma Payout Formula

The payout formula integrates the tier multiplier system from the value-pricing design:

```
base_share(c) = contributor_project_karma(c) / total_project_karma

weighted_share(c) = base_share(c) * tier_multiplier(c)

normalized_share(c) = weighted_share(c) / sum(weighted_share(all contributors))

payout(c) = contributor_pool * normalized_share(c)
```

Where `tier_multiplier` is determined by the contributor's cumulative cross-project karma tier:

| Tier | Name | Cumulative Karma Threshold | Dividend Rate Multiplier |
|---|---|---|---|
| 0 | Observer | 0 | 0x (no payouts) |
| 1 | Contributor | 50 | 0.5x |
| 2 | Builder | 250 | 1.0x |
| 3 | Architect | 1,000 | 1.5x |
| 4 | Partner | 5,000 | 2.0x |
| 5 | Inner Circle | 25,000 | 2.5x |

Only **vested karma** counts toward payout calculation. Unvested karma contributes to tier progression but does not generate dividends.

### Vesting Schedule

Karma earned on a project vests over 90 days:

- **Day 0:** 25% immediately vested
- **Days 1–90:** Remaining 75% vests linearly (~0.83%/day)
- **Day 90:** Fully vested

If a contributor abandons a project before full vesting, they retain only the vested portion. "Abandonment" is defined as zero contributions and zero activity (reviews, comments, governance votes) for 60 consecutive days.

### Worked Example

**Project: "PetMatch" — AI pet adoption platform**
**Monthly net revenue: $10,000**
**Contributor pool (70%): $7,000**

| Contributor | Project Karma | Vested Karma | Tier | Multiplier | Base Share | Weighted Share | Normalized | Payout |
|---|---|---|---|---|---|---|---|---|
| Alice (founder) | 850 | 850 | Architect (1.5x) | 1.5 | 28.3% | 42.5% | 34.9% | $2,443 |
| Bob (AI agent) | 400 | 400 | Builder (1.0x) | 1.0 | 13.3% | 13.3% | 10.9% | $763 |
| Carol (ML eng) | 620 | 620 | Builder (1.0x) | 1.0 | 20.7% | 20.7% | 17.0% | $1,190 |
| Dave (QA) | 330 | 330 | Builder (1.0x) | 1.0 | 11.0% | 11.0% | 9.0% | $630 |
| Eve (sales) | 800 | 600 | Partner (2.0x) | 2.0 | 20.0% | 40.0% | 28.2% | $1,974 |
| **Total** | **3,000** | **2,800** | | | | **121.8%** | **100%** | **$7,000** |

Note: Eve has 800 total karma but only 600 vested (she joined recently). Her Partner tier comes from cumulative cross-project karma, not just this project. Her 2.0x multiplier amplifies her share significantly — the system rewards long-term platform investment.

Bob's payout ($763) goes to Bob's human operator, not to the AI agent itself.

---

## 3. Payout Pipeline

### Payout Cycle

**Standard cycle:** Monthly, calculated on the 1st, disbursed on the 15th.

```
Month N (revenue accrual period)
       |
       v
  Day 1 of Month N+1: Payout calculation snapshot
       |
       v
  Days 1-5: Calculation + fraud review window
       |
       v
  Days 5-10: Contributor review period (contributors can flag errors)
       |
       v
  Day 15: Payout disbursement
```

**Pro plan:** Weekly payouts available. Calculated every Monday for the prior week, disbursed Thursday. Same holdback rules apply.

### Payout Calculation Steps

On calculation day, for each project:

1. **Sum net revenue** for the accrual period from the revenue ledger
2. **Deduct infrastructure costs** for the period
3. **Apply the revenue split** (70/15/15 or project-custom)
4. **Snapshot karma state:** for each contributor, capture vested project karma and current tier
5. **Compute weighted shares** using the formula in Section 2
6. **Apply holdback:** withhold 20% of each contributor's payout
7. **Check minimum threshold:** if payout (after holdback) < $25, roll over to next cycle
8. **Generate payout records** with full breakdown (see Section 8)

### Holdback Mechanism

Every payout is split 80/20:

| Portion | Timing | Purpose |
|---|---|---|
| 80% | Disbursed on payout day (the 15th) | Immediate earnings |
| 20% | Held for 30 days, then auto-released | Fraud clawback window |

The holdback protects against:
- **Refunds** that arrive after payout (deducted from holdback)
- **Chargebacks** (deducted from holdback)
- **Fraud detection** (if the contributor's karma is revoked within 30 days, holdback is forfeited)
- **Revenue corrections** (billing errors, duplicate charges)

If the holdback is insufficient to cover clawbacks, the deficit carries forward as a negative balance against future payouts. Contributors are never invoiced for deficits — the platform absorbs the loss if the contributor leaves.

### Minimum Payout Threshold

- **$25** minimum per payout cycle
- Below-threshold earnings accumulate across cycles until $25 is reached
- Accumulated earnings are displayed on the contributor dashboard as "pending balance"
- If a contributor's pending balance hasn't reached $25 in 12 months, they can request a manual payout (platform covers the processing overhead)

### First Payout Gate

New contributors face additional gates before their first payout:

| Requirement | Rationale |
|---|---|
| Account age > 60 days | Prevents throwaway accounts |
| Identity score >= 40 (fraud prevention Layer 1) | Sybil resistance |
| Trust Level >= 3 (Trusted) | Graduated trust verification |
| At least 1 contribution with >0 upvotes | Demonstrates real community acceptance |
| Tax form on file (W-9 or W-8BEN) | Legal compliance |
| Payout method configured | Operational requirement |

Until these gates are met, karma accrues and earnings accumulate — nothing is lost, just deferred.

---

## 4. Payment Methods

### Supported Methods

| Method | Region | Fee to Contributor | Fee to Platform | Settlement Time |
|---|---|---|---|---|
| ACH bank transfer | US | Free | ~$0.25/transfer | 2-3 business days |
| Stripe Connect payout | US + supported countries | Free | Included in Stripe fees | 2-3 business days |
| PayPal | Global | PayPal's recipient fee (~2.9%) | Free | Instant to PayPal balance |
| Wise | International (non-US) | Free (platform covers up to $5) | $1-5/transfer | 1-3 business days |

### Implementation

**ACH / Stripe Connect:** Use Stripe's built-in payout rails. Contributors link their bank account through Stripe's Connect onboarding (Express account for each contributor who opts for direct payouts, or platform-managed payouts via Stripe Transfers).

**PayPal:** Stripe doesn't natively pay out to PayPal. Use PayPal Payouts API (batch payouts) as a secondary rail. Contributors provide their PayPal email. Platform sends batch payouts on disbursement day.

**Wise:** Use Wise Business API for international transfers. Particularly valuable for contributors in countries where Stripe's payout coverage is limited. Platform absorbs transfer fees up to $5 per payout; excess is deducted from the contributor's payout.

### Contributor Payout Setup

During onboarding (or when first eligible for payouts), contributors complete:

1. **Select payout method** — one primary method required
2. **Provide details** — bank account (ACH), PayPal email, or Wise recipient info
3. **Verify identity** — tied to fraud prevention identity score (already required)
4. **Submit tax form** — W-9 (US) or W-8BEN (non-US)
5. **Confirm payout currency** — USD is primary; Wise handles conversion at payout time

Contributors can change their payout method at any time. Changes take effect on the next payout cycle.

### Multi-Currency

**Revenue collection:** Projects can charge in any Stripe-supported currency. All revenue is normalized to USD in the revenue ledger using Stripe's exchange rate at the time of charge.

**Payout disbursement:** Payouts are calculated in USD. For non-USD recipients:
- ACH/Stripe: USD only (recipient's bank handles conversion)
- PayPal: Sent in USD (PayPal converts at their rate)
- Wise: Converted at Wise's mid-market rate at time of transfer (this is the best rate available)

CrowdForge does not hold foreign currency balances or perform speculative FX. All conversion happens at the payment rail level at the moment of transfer.

---

## 5. Tax Compliance

### US Contributors

| Item | Detail |
|---|---|
| Form collected | W-9 (Request for Taxpayer Identification Number) |
| When collected | Before first payout eligibility |
| Reporting | 1099-NEC issued for earnings > $600/calendar year |
| Filing deadline | January 31 (to contributor), March 31 (to IRS, electronic) |
| Withholding | None (contributors are independent contractors responsible for self-employment tax) |

### Non-US Contributors

| Item | Detail |
|---|---|
| Form collected | W-8BEN (Certificate of Foreign Status) |
| When collected | Before first payout eligibility |
| Reporting | No 1099 required; income is foreign-sourced |
| Withholding | None for service income (not FDAP income); the work is performed outside the US |
| Validity | W-8BEN expires after 3 calendar years; platform prompts re-certification |

### VAT/GST on Platform Fees

CrowdForge charges VAT/GST on **platform services** (Pro subscriptions, infrastructure fees) — not on contributor revenue share payouts, which are B2B service compensation.

| Region | Tax | Rate | Applies To |
|---|---|---|---|
| EU | VAT | Country-specific (17-27%) | Pro subscription, infrastructure fees |
| UK | VAT | 20% | Pro subscription, infrastructure fees |
| Australia | GST | 10% | Pro subscription, infrastructure fees |
| India | GST | 18% | Pro subscription, infrastructure fees |
| Canada | GST/HST | 5-15% | Pro subscription, infrastructure fees |
| Brazil | ISS + PIS/COFINS | ~9.25% | Pro subscription, infrastructure fees |
| US | Sales tax | State-specific | Pro subscription, infrastructure fees (where applicable) |

CrowdForge registers for VAT/GST in each supported jurisdiction (or uses Stripe Tax to automate collection and remittance).

### Tax Compliance Vendor

Use **Trolley** (formerly Payment Rails) or **Tipalti** for automated:

- Tax form collection (W-9, W-8BEN) via embedded UI widgets
- TIN validation (IRS TIN matching for US, format validation for non-US)
- 1099-NEC generation and e-filing
- W-8BEN expiration tracking and re-certification prompts
- Audit-ready document storage

**Vendor selection criteria:**

| Vendor | Strength | Cost |
|---|---|---|
| Trolley | Developer-friendly API, good for startups, lower minimum | ~$2/payee/month |
| Tipalti | Enterprise-grade, broader international coverage, AP automation | ~$5/payee/month + setup |

**Recommendation:** Start with Trolley at launch (lower cost, simpler integration). Migrate to Tipalti when contributor count exceeds 5,000 or when enterprise features (AP automation, ERP integration) are needed.

---

## 6. Legal Framework

### Revenue Sharing Agreement (RSA)

Every contributor signs an RSA when joining a revenue-generating project. The RSA is a click-through agreement, not a negotiated contract.

**Key terms:**

| Clause | Content |
|---|---|
| Nature of relationship | Contributor is an independent contractor, not an employee, partner, or investor |
| Compensation | Revenue share proportional to weighted karma, as calculated by the platform's algorithm |
| No guaranteed minimum | Payouts depend on project revenue and karma standing; zero revenue = zero payout |
| Algorithm governance | Karma is computed algorithmically; no individual manual adjustments; algorithm changes require governance vote |
| Termination | Either party may terminate at any time; contributor retains vested karma and associated future payouts |
| IP assignment | Contributions are licensed to the project under the project's chosen license (default: MIT for code, CC-BY for content) |
| No ownership stake | Revenue share is compensation for services, not equity, dividends (in the legal sense), or investment returns |
| Dispute resolution | Binding arbitration via platform governance first, then JAMS arbitration for unresolved disputes |
| Governing law | Delaware, USA |

### Independent Contractor Classification

The RSA explicitly establishes the independent contractor relationship. Supporting factors:

| IRS Factor | CrowdForge Position |
|---|---|
| Behavioral control | Contributors choose what to work on, when, and how. No schedules, no mandated hours. |
| Financial control | Contributors provide their own tools. They can work on multiple projects and other platforms simultaneously. No exclusivity. |
| Relationship type | No benefits, no training provided, no indefinite relationship. The RSA is terminable at will. |

### Howey Test Defense

The karma/revenue system is structured to avoid securities classification:

| Howey Prong | Defense |
|---|---|
| Investment of money | Contributors invest effort, not capital. Karma cannot be purchased. |
| Common enterprise | Revenue share is proportional to individual karma (individual effort), not pooled returns. |
| Expectation of profits | Compensation for services rendered, same as any contractor payment. |
| Efforts of others | Karma requires active, ongoing contribution. Unvested karma = no payout. Abandoned projects = diluted share. No passive income mode. |

**Structural safeguards built into the payment system:**
- Karma is non-transferable — cannot be sold, traded, or gifted
- Vesting requires 90 days of engagement — no hit-and-run
- Dilution naturally reduces share of inactive contributors
- Revenue share is framed as service compensation in all legal documents, tax forms, and user-facing language

**Critical:** The term "dividend" is used internally as a design metaphor for the tier multiplier system. **All user-facing language, legal documents, and tax forms use "revenue share" or "service compensation."** The word "dividend" never appears in contributor-facing materials.

### Securities Counsel Review

Before launch, engage securities counsel to:
1. Review the RSA template
2. Issue a formal legal opinion letter on non-security classification
3. Review the tier multiplier system for any Howey implications
4. Confirm the "service compensation" framing holds under the weighted karma model

---

## 7. Project Treasury

### Purpose

The 15% project treasury allocation creates a project-owned fund for reinvestment. This prevents the tragedy of the commons where no one funds marketing, bounties, or infrastructure improvements because it would come out of their personal share.

### Governance

| Revenue Level | Treasury Control |
|---|---|
| < $1,000/month | Founder-controlled spending |
| $1,000–$10,000/month | Spending proposals require approval from contributors holding >50% karma |
| > $10,000/month | Formal treasury proposals with 72-hour voting window; quarterly treasury reports |

### Permitted Uses

- Bounties for specific tasks (karma + cash hybrid incentive)
- Marketing campaigns and paid acquisition
- Infrastructure upgrades beyond the current hosting tier
- Third-party service costs (APIs, SaaS tools the project uses)
- Legal costs (if the project needs its own legal structure)
- Bug bounty program for security

### Prohibited Uses

- Direct payouts to specific contributors outside the karma system
- Personal expenses of any contributor
- Investment in other projects or financial instruments
- Payments to entities owned by the Founder without governance approval

---

## 8. Transparency & Auditability

### Payout Breakdown

Every payout includes a detailed breakdown visible to the recipient:

```json
{
  "payout_id": "pay_abc123",
  "contributor_id": "usr_xyz",
  "period": "2026-01",
  "projects": [
    {
      "project_id": "proj_petmatch",
      "project_name": "PetMatch",
      "gross_revenue": 12500.00,
      "infrastructure_deduction": 50.00,
      "net_revenue": 12450.00,
      "contributor_pool_pct": 0.70,
      "contributor_pool": 8715.00,
      "your_vested_karma": 850,
      "total_project_karma": 3000,
      "your_base_share": 0.2833,
      "your_tier": "Architect",
      "your_tier_multiplier": 1.5,
      "your_weighted_share": 0.425,
      "sum_all_weighted_shares": 1.218,
      "your_normalized_share": 0.349,
      "your_gross_payout": 3041.62,
      "holdback_20pct": 608.32,
      "your_net_payout": 2433.29
    }
  ],
  "total_gross": 3041.62,
  "total_holdback": 608.32,
  "total_net": 2433.29,
  "pending_holdback_releases": [
    {
      "from_period": "2025-12",
      "amount": 487.50,
      "release_date": "2026-02-15"
    }
  ],
  "payout_method": "ach",
  "currency": "USD",
  "status": "disbursed",
  "disbursed_at": "2026-02-15T00:00:00Z"
}
```

### Audit Trail

Every financial event is recorded in an append-only audit log:

| Event Type | Data Captured |
|---|---|
| `revenue.collected` | project_id, amount, currency, source (subscription/one-time/etc), stripe_charge_id |
| `revenue.refunded` | project_id, amount, original_charge_id, reason |
| `revenue.disputed` | project_id, amount, charge_id, dispute_id, status |
| `payout.calculated` | contributor_id, project_id, period, all formula inputs and outputs |
| `payout.disbursed` | contributor_id, amount, method, transfer_id |
| `holdback.released` | contributor_id, amount, original_payout_id |
| `holdback.clawed_back` | contributor_id, amount, reason, original_payout_id |
| `treasury.spent` | project_id, amount, purpose, approved_by (governance vote ID) |
| `split.changed` | project_id, old_split, new_split, governance_vote_id |

The audit log is publicly queryable (read-only) by any project contributor. Platform-wide aggregate data (total payouts, total revenue) is public on the transparency dashboard.

### Contributor Earnings Dashboard

Each contributor sees:

- **Lifetime earnings** — total across all projects, all time
- **This month's projected earnings** — based on current revenue run rate and karma standing
- **Pending balance** — accumulated earnings below the $25 threshold
- **Holdback balance** — amounts in the 30-day escrow window, with release dates
- **Payout history** — every past payout with full breakdown (expandable)
- **Earnings by project** — per-project revenue share over time (chart)
- **Tier impact** — "Your Architect tier earned you X% more than Builder rate would have"

---

## 9. Database Schema

### Core Tables

```sql
-- Immutable revenue ledger
CREATE TABLE revenue_events (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id      UUID NOT NULL REFERENCES projects(id),
    event_type      TEXT NOT NULL,  -- 'charge', 'refund', 'dispute_lost', 'dispute_won'
    amount_cents    BIGINT NOT NULL, -- signed: positive for charges, negative for refunds
    currency        TEXT NOT NULL DEFAULT 'usd',
    amount_usd_cents BIGINT NOT NULL, -- normalized to USD
    stripe_event_id TEXT UNIQUE NOT NULL, -- idempotency
    metadata        JSONB,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Payout cycle snapshots
CREATE TABLE payout_cycles (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    period_start    DATE NOT NULL,
    period_end      DATE NOT NULL,
    status          TEXT NOT NULL DEFAULT 'calculating',
        -- 'calculating' -> 'review' -> 'approved' -> 'disbursing' -> 'complete'
    calculated_at   TIMESTAMPTZ,
    disbursed_at    TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Per-contributor payout line items
CREATE TABLE payout_items (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cycle_id            UUID NOT NULL REFERENCES payout_cycles(id),
    contributor_id      UUID NOT NULL REFERENCES users(id),
    project_id          UUID NOT NULL REFERENCES projects(id),
    net_revenue_cents   BIGINT NOT NULL,
    pool_pct            NUMERIC(5,4) NOT NULL,
    pool_amount_cents   BIGINT NOT NULL,
    vested_karma        NUMERIC(12,2) NOT NULL,
    total_project_karma NUMERIC(12,2) NOT NULL,
    base_share          NUMERIC(10,8) NOT NULL,
    tier                SMALLINT NOT NULL,
    tier_multiplier     NUMERIC(4,2) NOT NULL,
    weighted_share      NUMERIC(10,8) NOT NULL,
    normalized_share    NUMERIC(10,8) NOT NULL,
    gross_amount_cents  BIGINT NOT NULL,
    holdback_cents      BIGINT NOT NULL,
    net_amount_cents    BIGINT NOT NULL,
    status              TEXT NOT NULL DEFAULT 'pending',
        -- 'pending' -> 'disbursed' | 'rolled_over' (below threshold)
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Holdback escrow tracking
CREATE TABLE holdbacks (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    payout_item_id  UUID NOT NULL REFERENCES payout_items(id),
    contributor_id  UUID NOT NULL REFERENCES users(id),
    amount_cents    BIGINT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'held',
        -- 'held' -> 'released' | 'clawed_back'
    release_date    DATE NOT NULL, -- 30 days after disbursement
    released_at     TIMESTAMPTZ,
    clawback_reason TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Contributor payout preferences
CREATE TABLE payout_methods (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contributor_id  UUID NOT NULL REFERENCES users(id),
    method_type     TEXT NOT NULL, -- 'ach', 'paypal', 'wise', 'stripe_connect'
    is_primary      BOOLEAN NOT NULL DEFAULT true,
    details_encrypted BYTEA NOT NULL, -- encrypted payout details (bank account, email, etc.)
    verified        BOOLEAN NOT NULL DEFAULT false,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Tax form tracking
CREATE TABLE tax_forms (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contributor_id  UUID NOT NULL REFERENCES users(id),
    form_type       TEXT NOT NULL, -- 'w9', 'w8ben'
    vendor_form_id  TEXT NOT NULL, -- reference ID from Trolley/Tipalti
    status          TEXT NOT NULL, -- 'pending', 'submitted', 'validated', 'expired'
    expires_at      DATE, -- W-8BEN: 3 calendar years
    submitted_at    TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Project revenue split configuration
CREATE TABLE project_splits (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id          UUID NOT NULL REFERENCES projects(id),
    contributor_pool_pct NUMERIC(5,4) NOT NULL DEFAULT 0.7000,
    platform_fee_pct    NUMERIC(5,4) NOT NULL DEFAULT 0.1500,
    treasury_pct        NUMERIC(5,4) NOT NULL DEFAULT 0.1500,
    governance_vote_id  UUID, -- null for default, references governance vote that changed it
    effective_from      TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT valid_split CHECK (
        contributor_pool_pct + platform_fee_pct + treasury_pct = 1.0000
        AND contributor_pool_pct BETWEEN 0.6000 AND 0.8000
        AND platform_fee_pct = 0.1500
    )
);

-- Append-only audit log
CREATE TABLE payment_audit_log (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type  TEXT NOT NULL,
    actor_id    UUID, -- null for system events
    entity_type TEXT NOT NULL, -- 'project', 'contributor', 'payout', 'holdback', 'treasury'
    entity_id   UUID NOT NULL,
    payload     JSONB NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### Indexes

```sql
CREATE INDEX idx_revenue_events_project ON revenue_events(project_id, created_at);
CREATE INDEX idx_payout_items_cycle ON payout_items(cycle_id);
CREATE INDEX idx_payout_items_contributor ON payout_items(contributor_id, created_at);
CREATE INDEX idx_holdbacks_release ON holdbacks(status, release_date) WHERE status = 'held';
CREATE INDEX idx_tax_forms_expiry ON tax_forms(status, expires_at) WHERE status = 'validated';
CREATE INDEX idx_audit_log_entity ON payment_audit_log(entity_type, entity_id, created_at);
```

---

## 10. Service Architecture

### Payment Service Boundaries

The Payment Service sits within CrowdForge's service layer and owns:

```
Revenue Service (ingest + ledger)
       |
       v
Split Engine (calculate payouts)
       |
       v
Disbursement Service (execute transfers)
       |
       v
Tax Compliance Service (forms + reporting)
```

### Integration Points

| Service | Dependency | Direction |
|---|---|---|
| Stripe | Revenue collection + ACH payouts | Bidirectional (webhooks in, API out) |
| PayPal Payouts API | PayPal disbursements | Outbound |
| Wise Business API | International transfers | Outbound |
| Trolley/Tipalti | Tax form collection + filing | Bidirectional |
| Karma Service | Vested karma snapshots, tier lookups | Inbound (read) |
| Fraud Service | Contributor trust level, clawback triggers | Inbound (read + events) |
| Notification Service | Payout notifications, tax form reminders | Outbound |
| Real-time Feed | Revenue events for live dashboard | Outbound (publish) |

### Key API Endpoints

```
POST   /api/projects/:id/stripe/connect     -- Provision Connected Account
GET    /api/projects/:id/revenue             -- Revenue dashboard data
GET    /api/projects/:id/revenue/ledger      -- Raw revenue events (paginated)
GET    /api/projects/:id/split               -- Current revenue split config
PUT    /api/projects/:id/split               -- Update split (requires governance vote)

GET    /api/contributors/me/earnings         -- Personal earnings dashboard
GET    /api/contributors/me/payouts          -- Payout history with breakdowns
GET    /api/contributors/me/holdbacks        -- Active holdbacks with release dates
GET    /api/contributors/me/payout-method    -- Current payout configuration
PUT    /api/contributors/me/payout-method    -- Update payout method
GET    /api/contributors/me/tax-status       -- Tax form status
POST   /api/contributors/me/tax-form         -- Initiate tax form collection flow

GET    /api/payouts/cycles/:id               -- Payout cycle details
GET    /api/payouts/cycles/:id/items         -- All line items for a cycle
POST   /api/payouts/cycles/:id/approve       -- Approve cycle for disbursement (admin)

GET    /api/audit/payments                   -- Query audit log (contributor-scoped or admin)
```

---

## 11. Scheduled Jobs

| Job | Schedule | Description |
|---|---|---|
| `payout_calculator` | 1st of each month, 00:00 UTC | Snapshots karma, computes all payout items for the period |
| `payout_disburser` | 15th of each month, 06:00 UTC | Executes transfers for approved payout cycles |
| `holdback_releaser` | Daily, 00:00 UTC | Releases holdbacks past their 30-day window |
| `holdback_clawback` | On fraud/refund event | Deducts from held amounts when clawback triggered |
| `tax_form_reminder` | Weekly, Monday 09:00 UTC | Emails contributors with missing or expiring tax forms |
| `w8ben_expiry_check` | Monthly, 1st | Flags W-8BEN forms expiring within 90 days |
| `revenue_reconciler` | Daily, 02:00 UTC | Reconciles revenue ledger against Stripe balance reports |
| `weekly_payout_calculator` | Monday 00:00 UTC | Computes weekly payouts for Pro plan contributors |
| `treasury_report` | Quarterly | Generates treasury spending reports for projects >$10K/month |
| `stripe_fee_reconciler` | Monthly | Verifies platform's Stripe fee absorption against actual fees |

---

## 12. Edge Cases & Failure Modes

### Revenue Disputes Between Projects

If two projects dispute revenue attribution (e.g., shared customer base), the revenue stays in the originating project's Connected Account. Cross-project revenue disputes are resolved through platform governance arbitration.

### Contributor Leaves Mid-Cycle

Vested karma continues to generate payouts as long as the project earns revenue. The contributor's share naturally dilutes as new contributions grow the total karma pool. There is no "exit penalty" — earned and vested karma is permanent.

### Project Revenue Drops to Zero

Payouts cease. Accumulated karma remains. If revenue resumes, payouts resume using the same karma distribution. The treasury balance (if any) remains available under governance control.

### Stripe Account Suspension

If a project's Connected Account is suspended by Stripe (fraud, policy violation), all revenue collection halts. Pending payouts are frozen. The platform notifies all contributors and initiates a review. If the suspension is permanent, remaining funds in the Connected Account are disbursed according to the last valid payout calculation, minus any Stripe-imposed penalties.

### Currency Conversion Losses

Exchange rate fluctuations between revenue collection and payout disbursement can create minor discrepancies. The revenue ledger records USD-equivalent at time of charge (Stripe's rate). Payouts are in USD. Any FX slippage is absorbed by the platform from its 15% cut, not passed to contributors.

### Payout Failure

If a transfer fails (invalid bank details, PayPal account closed, Wise rejection):
1. The payout item is marked `failed`
2. Contributor is notified with the failure reason
3. Amount rolls back to pending balance
4. Contributor updates their payout method
5. A retry is attempted in the next cycle (or manually triggered by the contributor)

Failed payouts are retried for 3 consecutive cycles. After 3 failures, the balance is held indefinitely until the contributor updates their payout method and manually requests disbursement.

### Negative Revenue Period

If refunds + chargebacks exceed new revenue in a period, the project has negative net revenue. No payouts are made. The deficit carries forward and must be recovered before the next payout cycle can disburse. Contributors are not asked to return previous payouts — the holdback mechanism and future revenue absorb the loss.

### AI Agent Operator Payout

AI agent earnings are attributed to the agent's human operator. The operator's payout aggregates their personal contributions across projects and their agents' contributions. A single payout is issued per human, regardless of how many agents they operate.

---

## 13. Supported Countries (Launch)

| Country | Payout Methods | Tax Form | VAT/GST on Platform Fees |
|---|---|---|---|
| United States | ACH, Stripe, PayPal | W-9 | State sales tax (where applicable) |
| United Kingdom | Stripe, Wise, PayPal | W-8BEN | 20% VAT |
| Germany | Stripe, Wise, PayPal | W-8BEN | 19% VAT |
| France | Stripe, Wise, PayPal | W-8BEN | 20% VAT |
| Netherlands | Stripe, Wise, PayPal | W-8BEN | 21% VAT |
| Canada | Stripe, Wise, PayPal | W-8BEN | 5-15% GST/HST |
| Australia | Stripe, Wise, PayPal | W-8BEN | 10% GST |
| India | Wise, PayPal | W-8BEN | 18% GST |
| Brazil | Wise, PayPal | W-8BEN | ~9.25% ISS+PIS/COFINS |

Expansion to additional countries follows legal review of local contractor payment regulations, tax withholding requirements, and payment rail availability.

---

## 14. Implementation Phases

### Phase 1: Foundation (Launch)

- Stripe Connect integration (Express accounts, destination charges)
- Revenue event ingestion pipeline (webhooks → ledger)
- Basic payout calculation (monthly cycle, direct karma share — no tier multipliers yet)
- ACH payouts via Stripe
- W-9 collection via Trolley
- Revenue dashboard (per-project)
- Payout breakdown display (contributor dashboard)
- Audit log

### Phase 2: Full Payout Engine (Month 3-6)

- Tier multiplier integration (weighted karma formula)
- Vesting schedule enforcement
- Holdback mechanism (80/20 split, 30-day escrow)
- PayPal payouts
- Wise international transfers
- W-8BEN collection + non-US contributor support
- Weekly payout option (Pro plan)
- Project treasury management
- Tax form expiry tracking

### Phase 3: Scale & Compliance (Month 6-12)

- 1099-NEC auto-generation and e-filing
- VAT/GST collection on platform fees (Stripe Tax integration)
- Revenue reconciliation automation
- Configurable project splits with governance voting
- Multi-currency revenue normalization improvements
- Payout retry automation
- Treasury governance for high-revenue projects
- Contributor earnings projections ("at current rate, you'll earn $X this month")

### Phase 4: Maturity (Month 12+)

- Custom account migration (high-revenue projects get full Stripe Custom accounts)
- Advanced revenue analytics (cohort analysis, revenue attribution, churn impact)
- Tipalti migration for enterprise-grade compliance
- Additional country support based on demand
- API for third-party integrations (accounting software, tax prep tools)
- Contributor tax summaries (annual earnings report for personal tax filing)
