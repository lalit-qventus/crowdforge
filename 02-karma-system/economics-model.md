# Karma Economics: Mathematical Model and Analysis

## Notation and Core Formulas

All models below use these shared definitions.

| Symbol | Definition | Default |
|--------|-----------|---------|
| B | Base karma per contribution | 4-10 (category-dependent) |
| B̄ | Expected base karma (contribution-mix weighted) | 7.3 |
| t | Days since project creation | — |
| M(t) | Pioneer multiplier | 1 + 2e^(-0.01t) |
| v | Upvote count | — |
| U(v) | Upvote score | ln(1+v) / ln(10) |
| K_c(t,v) | Karma per contribution | B * M(t) * (1 + U(v)) |
| n(t) | Active contributors at time t | — |
| f | Contributions per contributor per month | — |
| R(t) | Monthly project revenue at time t | — |
| S(t) | Cumulative project karma at time t | — |
| E(t) | Exchange rate ($/karma/month) | R(t) / S(t) |
| τ_i | Tier multiplier for tier i | [0, 0.5, 1.0, 1.5, 2.0, 2.5] |

**Revenue split:** 100% to contributors. The platform takes zero cut of project revenue. Platform sustainability is funded through separate channels (infrastructure fees, subscriptions, etc.) — not modeled here.

**Note:** The existing design docs reference 70/15/15 (karma-system) and 85/15 (business-model) splits. Both are superseded. All revenue flows directly to karma-weighted contributors.

---

## 1. Karma Supply Model

### 1.1 Per-Contribution Expected Karma

Assuming a contribution-mix-weighted average base karma of B̄ = 7.3 and average upvote count v̄ = 3 (giving U(3) = 0.602):

```
E[K_c(t)] = 7.3 * (1 + 2e^{-0.01t}) * 1.602
```

| Day | M(t) | E[K_c] |
|-----|-------|--------|
| 0 | 3.00 | 35.1 |
| 30 | 2.48 | 29.0 |
| 60 | 2.10 | 24.6 |
| 90 | 1.81 | 21.2 |
| 180 | 1.33 | 15.6 |
| 365 | 1.05 | 12.3 |
| 730 | 1.00 | 11.7 |

The pioneer multiplier produces a ~3x range between day-0 and steady-state contributions. After ~1 year, karma emission per contribution is effectively constant at ~12 karma.

### 1.2 Monthly Emission Rate Per Project

Monthly karma emission = n(t) * f * E[K_c(t)]

For a project with n=10 contributors, f=5 contributions each:

| Month | Avg Day | E[K_c] | Emission/mo |
|-------|---------|--------|-------------|
| 1 | 15 | 31.0 | 1,550 |
| 3 | 75 | 22.0 | 1,100 |
| 6 | 165 | 16.0 | 800 |
| 12 | 350 | 12.5 | 625 |
| 24 | 715 | 11.7 | 585 |

Emission converges to a steady rate of ~n*f*11.7 once the pioneer bonus decays.

### 1.3 Cumulative Supply Curve

For constant contributor count n and frequency f, cumulative karma is the integral:

```
S(T) = n * f * B̄ * (1 + Ū) * ∫₀ᵀ M(t) dt
     = n * f * 11.7 * [T + 200(1 - e^{-0.01T})]
```

where 11.7 = B̄ * (1 + Ū) is the steady-state per-contribution karma and 200 = 2/0.01 is the pioneer integral constant.

The pioneer bonus adds a fixed ~200 * n * f * 11.7 ≈ 2,340 * n * f karma lump over the project lifetime, regardless of how long the project runs. After year 1, supply growth is linear.

**Platform-wide supply** with P(t) projects, each at different ages:

```
S_platform(T) = Σ_{j=1}^{P(T)} S_j(T - t_j)
```

where t_j is the creation date of project j. If projects are created at rate p per month:

```
S_platform(T) ≈ p * n̄ * f̄ * 11.7 * [T²/2 + 200T]
```

This is quadratic in T (from new projects accumulating). Growth is polynomial, not exponential — bounded by human/AI labor capacity. Platform-wide karma cannot hyperinflate unless contribution frequency grows unboundedly.

### 1.4 Supply Curve Pathology Check

**Does supply grow faster than revenue?**

Revenue is bounded by market demand and product quality, growing at best linearly in the long run (after S-curve growth). Karma grows quadratically at the platform level (more projects over time). This creates a structural tendency for the platform-wide exchange rate to decline over time.

**Why this is acceptable:** Exchange rates are per-project, not platform-wide. Each project has its own S(t) and R(t). A project with stable revenue and stable contribution rate has linear karma growth and (ideally) stable revenue, giving E(t) ∝ 1/t — a declining exchange rate per project. This means per-karma value falls as the project matures, which is correct: early karma (earned at higher risk) should be "worth more" in retrospect than late karma.

**When this fails:** If a project's contribution rate spikes without corresponding revenue growth, per-karma value collapses. See Section 5 (Failure Modes).

---

## 2. Dilution Model

### 2.1 Single-Contributor Dilution

Contributor A earns K_A karma at time 0 and stops contributing. Total project karma S(t) grows as other contributors continue.

```
share_A(t) = K_A / S(t)
```

If the project has constant emission rate ε per month after A stops:

```
S(t) = K_A + ε * t
share_A(t) = K_A / (K_A + ε * t)
```

This is a hyperbolic decay. The half-life of A's share (time to go from initial share to half):

```
t_half = K_A / ε
```

**Example:** Alice earns 500 karma in month 1. Project emits 800 karma/month thereafter.
- t_half = 500 / 800 = 0.625 months ≈ 19 days
- After 1 month: 500 / 1300 = 38.5%
- After 6 months: 500 / 5300 = 9.4%
- After 12 months: 500 / 10,100 = 5.0%
- After 24 months: 500 / 19,700 = 2.5%

### 2.2 Equilibrium Share for Day-1 Contributors

A contributor who provided X% of total contributions in month 1 and then stopped. If the project sustains n active contributors at f contributions/month:

```
steady_state_share ≈ K_initial / (K_initial + n * f * 11.7 * T)  → 0 as T → ∞
```

The share asymptotically approaches zero but never reaches it. The critical question: is the absolute payout still meaningful?

**MVP founder example:** Alice wrote the MVP, earning 500 karma (with pioneer bonuses). Project reaches $10K/month revenue at month 12 with 8,000 total karma.

Alice's share: 500/8000 = 6.25%
Alice's monthly payout (pre-tier): $10,000 * 0.0625 = **$625/month**

At month 24 with 15,000 total karma and $15K revenue:
Alice's share: 500/15000 = 3.33%
Payout: $15,000 * 0.0333 = **$500/month**

At month 36 with 22,000 karma and $20K revenue:
Payout: $20,000 * (500/22000) = **$455/month**

The revenue growth partially offsets the dilution. Alice retains a meaningful income stream for years, which validates the "no decay" design choice. However, the tier system amplifies this further — if Alice is Tier 4 (2.0x) while new contributors are Tier 1 (0.5x), her effective share is much larger than the raw karma ratio suggests.

### 2.3 Is Dilution Fair?

**Test case:** Pioneer who built the MVP vs. late contributor who provides ongoing maintenance.

Pioneer (month 1): 500 karma, 3.0x pioneer multiplier baked in.
Maintainer (months 6-24): 20 karma/contribution * 5 contributions/month * 18 months = 1,800 karma.

At month 24:
- Pioneer: 500/2,300 = 21.7% raw share
- Maintainer: 1,800/2,300 = 78.3% raw share

The maintainer dominates — as they should, having invested 18x more time. But the pioneer's 21.7% for one month of work (vs. 78.3% for 18 months) represents a 4:1 per-month return advantage, reflecting the risk premium. With tier multipliers, the pioneer likely holds a higher tier (accumulated karma from other projects too) amplifying their share further.

**Verdict:** Dilution is fair. Early contributors retain meaningful share, but only if the project succeeds (otherwise their karma has no revenue behind it). The pioneer multiplier provides adequate compensation for early risk.

---

## 3. Tier Threshold Analysis

### 3.1 Absolute Thresholds — Projected Tier Distributions

Thresholds: [0, 50, 250, 1,000, 5,000, 25,000]

**Assumptions for distribution modeling:**
- Contributors accumulate karma at varying rates: casual (~75/mo), regular (~200/mo), power (~500/mo), elite (~1,000/mo)
- Distribution: 40% casual, 35% regular, 15% power, 10% elite
- Contributors join at a uniform rate over the platform's lifetime
- Churn rate: 50% of casual drop off within 6 months, 20% of others

**At 1,000 contributors (platform age ~6 months):**

| Tier | Threshold | Projected % | Count |
|------|-----------|-------------|-------|
| 0 (Observer) | 0 | 25% | 250 |
| 1 (Contributor) | 50 | 35% | 350 |
| 2 (Builder) | 250 | 25% | 250 |
| 3 (Architect) | 1,000 | 12% | 120 |
| 4 (Partner) | 5,000 | 3% | 30 |
| 5 (Founder's Circle) | 25,000 | 0% | 0 |

Healthy pyramid. Tier 5 is unreachable this early.

**At 10,000 contributors (platform age ~18 months):**

| Tier | Projected % | Count |
|------|-------------|-------|
| 0 | 20% | 2,000 |
| 1 | 25% | 2,500 |
| 2 | 25% | 2,500 |
| 3 | 18% | 1,800 |
| 4 | 10% | 1,000 |
| 5 | 2% | 200 |

Still roughly pyramid-shaped but Tier 3+ is growing (30% combined). Veteran cohorts accumulate through the thresholds.

**At 100,000 contributors (platform age ~36+ months):**

| Tier | Projected % | Count |
|------|-------------|-------|
| 0 | 15% | 15,000 |
| 1 | 15% | 15,000 |
| 2 | 20% | 20,000 |
| 3 | 22% | 22,000 |
| 4 | 18% | 18,000 |
| 5 | 10% | 10,000 |

**Tier inflation is visible.** Half the platform is at Tier 3+. The pyramid has become a diamond, then approaches a top-heavy trapezoid. Tier 5 at 10% means 10,000 Founder's Circle members — the "founder" label loses exclusivity.

### 3.2 Percentile-Based Thresholds

| Tier | Percentile | Guarantee |
|------|-----------|-----------|
| 5 | Top 1% | Always ~1% |
| 4 | Top 5% | Always ~4% |
| 3 | Top 15% | Always ~10% |
| 2 | Top 40% | Always ~25% |
| 1 | Top 75% | Always ~35% |
| 0 | Bottom 25% | Always ~25% |

**Advantages:**
- Pyramid is preserved forever regardless of scale
- Status scarcity is maintained
- Reaching Tier 5 remains prestigious

**Disadvantages:**
- A contributor's tier can DROP as better contributors join — violating the "earned, never taken away" principle
- Creates zero-sum competition between contributors
- Psychologically demotivating: "I lost my Tier 4 status because someone better showed up"
- Tier recalculation introduces volatility in dividend rates, making income unpredictable

### 3.3 Recommendation: Ratcheted Hybrid

Use absolute thresholds as the **floor** and adjust thresholds upward annually based on the 50th-percentile karma level.

```
threshold_i(year) = max(base_threshold_i, base_threshold_i * median_karma(year) / median_karma(year_0))
```

Rules:
- No contributor's tier ever decreases (ratchet)
- Thresholds rise with the platform, preserving scarcity for NEW contributors
- Veterans who earned their tier keep it, even if they'd fall below the new threshold
- Annual recalibration, announced 90 days in advance

**Projected thresholds over time:**

| Tier | Year 0 | Year 1 | Year 2 | Year 3 |
|------|--------|--------|--------|--------|
| 1 | 50 | 75 | 120 | 180 |
| 2 | 250 | 375 | 600 | 900 |
| 3 | 1,000 | 1,500 | 2,400 | 3,600 |
| 4 | 5,000 | 7,500 | 12,000 | 18,000 |
| 5 | 25,000 | 37,500 | 60,000 | 90,000 |

This keeps Tier 5 exclusive (~1-3% of contributors) while honoring the ratchet guarantee.

---

## 4. Tier Multiplier Impact on Payouts

### 4.1 Weighted Share Formula

```
weighted_share_i = (project_karma_i * τ_tier) / Σ_j(project_karma_j * τ_tier_j)
payout_i = R * weighted_share_i
```

### 4.2 Distortion Analysis

**Scenario:** A project with 5 contributors.

| Contributor | Project Karma | Raw Share | Tier | τ | Weighted Karma | Weighted Share |
|-------------|--------------|-----------|------|---|----------------|---------------|
| A (founder) | 2,000 | 40.0% | 4 | 2.0 | 4,000 | 45.5% |
| B (builder) | 1,500 | 30.0% | 2 | 1.0 | 1,500 | 17.0% |
| C (new dev) | 800 | 16.0% | 1 | 0.5 | 400 | 4.5% |
| D (sales) | 500 | 10.0% | 3 | 1.5 | 750 | 8.5% |
| E (new) | 200 | 4.0% | 1 | 0.5 | 100 | 1.1% |
| **Total** | **5,000** | **100%** | | | **6,750** | **100%** |

**Key distortions:**
- A's share increases from 40% → 45.5% (+14% relative gain from tier)
- C's share drops from 16% → 4.5% (-72% relative loss)
- E's share drops from 4% → 1.1% (-72% relative loss)

The tier system creates a 4x effective multiplier between Tier 4 (2.0x) and Tier 1 (0.5x). A Tier 4 contributor with HALF the raw karma of a Tier 1 contributor earns the SAME weighted share.

### 4.3 Resentment Threshold

The tier system becomes psychologically problematic when a contributor can observe that someone with demonstrably LESS project contribution earns MORE revenue.

**Critical case:** Contributor with 200 project karma at Tier 5 (2.5x) → weighted 500. Contributor with 400 project karma at Tier 1 (0.5x) → weighted 200. The Tier 5 contributor earns 2.5x more revenue despite having half the project karma.

This is by design — the tier system rewards platform-wide track record, not just project-local contribution. But the contributor earning less will experience it as unfair unless the tier system's rationale is visibly communicated.

**Mitigation:** Display both raw karma share AND tier-adjusted share in contributor dashboards. Frame it as: "Your base share is 8%. Your Tier 1 status adjusts this to 4.5%. Reaching Tier 2 (250 more karma) would bring your share to 9%." This converts resentment into aspiration.

---

## 5. Project Archetype Simulations

### 5.1 Archetype: "Rocket" (Fast Growth)

**Profile:** SaaS tool that finds product-market fit fast.

| Month | Contributors | Contrib/mo | Revenue | Cum. Karma | E ($/karma) |
|-------|-------------|------------|---------|------------|-------------|
| 1 | 5 | 25 | $0 | 878 | $0 |
| 3 | 15 | 75 | $500 | 4,350 | $0.08 |
| 6 | 30 | 150 | $5,000 | 12,800 | $0.27 |
| 9 | 40 | 200 | $12,000 | 22,400 | $0.38 |
| 12 | 50 | 250 | $20,000 | 33,300 | $0.42 |
| 18 | 50 | 250 | $30,000 | 55,500 | $0.38 |
| 24 | 40 | 200 | $35,000 | 72,500 | $0.34 |

Exchange rate rises during growth, peaks when revenue growth outpaces karma emission, then stabilizes or declines as contributor pool matures. Healthy trajectory — no pathologies.

### 5.2 Archetype: "Slow Burn" (Gradual Build)

| Month | Contributors | Contrib/mo | Revenue | Cum. Karma | E ($/karma) |
|-------|-------------|------------|---------|------------|-------------|
| 1 | 3 | 15 | $0 | 527 | $0 |
| 6 | 8 | 40 | $200 | 3,500 | $0.04 |
| 12 | 12 | 60 | $1,000 | 8,700 | $0.08 |
| 18 | 15 | 75 | $2,000 | 15,500 | $0.09 |
| 24 | 15 | 75 | $3,000 | 22,300 | $0.09 |

Low per-karma value throughout. Contributors earn modest amounts ($5-50/month at 5% share). Sustainable but not exciting. These projects survive on intrinsic motivation + tier-building incentive.

### 5.3 Archetype: "Plateau" (Quick Start, Levels Off)

| Month | Contributors | Contrib/mo | Revenue | Cum. Karma | E ($/karma) |
|-------|-------------|------------|---------|------------|-------------|
| 1 | 20 | 100 | $0 | 3,510 | $0 |
| 3 | 8 | 40 | $3,000 | 6,900 | $0.30 |
| 6 | 8 | 40 | $3,000 | 10,500 | $0.20 |
| 12 | 8 | 40 | $3,000 | 16,300 | $0.13 |
| 24 | 5 | 25 | $3,000 | 24,300 | $0.09 |

**Pathology detected:** Exchange rate halves from month 3 to month 12. Contributors watch their per-karma value erode with every contribution while revenue stays flat. Rational response: stop contributing and coast on existing karma — which is exactly what happens (contributor count drops). The system self-corrects toward stasis, which is acceptable for a mature product.

### 5.4 Archetype: "Decline" (Promising Start, Fades)

| Month | Contributors | Contrib/mo | Revenue | Cum. Karma | E ($/karma) |
|-------|-------------|------------|---------|------------|-------------|
| 1 | 10 | 50 | $500 | 1,755 | $0.20 |
| 3 | 8 | 40 | $1,000 | 4,700 | $0.15 |
| 6 | 3 | 15 | $200 | 6,200 | $0.02 |
| 9 | 1 | 5 | $0 | 6,500 | $0 |

**Failure mode:** Revenue cliff. Karma earned in months 1-3 becomes worthless. Contributors who vested feel cheated. But their absolute karma was never "taken away" — it's still there, the revenue behind it dried up. This is equivalent to holding stock in a failing company. The system is honest about this: karma is equity, and equity in a failed project is worth zero.

No circuit breaker is appropriate here — projects fail, and that's reality.

### 5.5 Archetype: "Ghost" (Solo Project)

| Month | Contributors | Contrib/mo | Revenue | Cum. Karma | E ($/karma) |
|-------|-------------|------------|---------|------------|-------------|
| 1 | 1 | 10 | $5,000 | 351 | $9.97 |
| 6 | 1 | 5 | $8,000 | 1,100 | $5.09 |
| 12 | 1 | 3 | $10,000 | 1,500 | $4.67 |

**Observation:** With 100% revenue flowing to contributors, the solo contributor keeps everything. This is economically equivalent to freelancing with CrowdForge providing infrastructure and payment processing for free (funded by the platform's separate revenue streams). Ghost projects are not a pathology under this split — they're a valid use case.

The risk is behavioral: solo projects don't generate the collaborative dynamics CrowdForge is designed around. They consume platform resources without contributing to network effects. Consider gating certain platform benefits (priority hosting, analytics) behind multi-contributor thresholds to nudge toward collaboration without penalizing solos.

---

## 6. Sales Karma Feedback Loop

### 6.1 Self-Recapture Rate

A salesperson brings in revenue R_s and earns R_s / 100 sales karma. Assuming no pioneer bonus and no upvotes (conservative):

```
sales_karma = R_s / 100
salesperson_share = sales_karma / S_total
salesperson_payout = R_total * salesperson_share
```

If the salesperson's sales are the entire revenue (R_s = R_total):

```
self_recapture = R_s * (R_s/100) / S_total
recapture_rate = R_s / (100 * S_total)
```

**Example:** Salesperson brings $50K, total karma pool is 10,000.
- Sales karma: 500
- Share: 500/10,000 = 5%
- Payout: $50,000 * 0.05 = $2,500
- Recapture rate: $2,500 / $50,000 = **5.0%**

This is at the low end of standard sales commission rates (5-20%). The feedback loop is NOT self-reinforcing — the salesperson captures a small fraction of the revenue they generate.

### 6.2 Sales-Dominated Projects

**Scenario:** Project has $500K annual revenue, mostly from one salesperson.

| Contributor | Category | Karma | Share |
|-------------|----------|-------|-------|
| Builders (5) | Code/Design | 4,000 | 44.4% |
| Salesperson | Sales | 5,000 | 55.6% |
| **Total** | | **9,000** | |

Salesperson captures: $41,667/mo * 0.556 = **$23,167/month**
Builders split: $41,667/mo * 0.444 = **$18,500/month** (across 5 = $3,700 each)

The salesperson earns 6.3x each individual builder. Is this fair? They brought in 100% of the revenue. Without them, all builders earn $0. The ratio is aggressive but defensible.

### 6.3 Sensitivity to sales_karma_rate

| Rate | Sales Karma (on $50K) | Sales Share (in 10K pool) | Self-Recapture |
|------|----------------------|--------------------------|----------------|
| 1/$50 | 1,000 | 9.1% | 9.1% |
| **1/$100 (default)** | **500** | **4.8%** | **4.8%** |
| 1/$200 | 250 | 2.4% | 2.4% |
| 1/$500 | 100 | 1.0% | 1.0% |

At 1/$50, a $500K salesperson accumulates 10,000 karma — enough for Tier 4 from sales alone. This creates a power imbalance.

At 1/$500, a $500K salesperson earns only 1,000 karma — barely Tier 3. Sales becomes under-rewarded relative to the value created.

**The default (1/$100) sits in a reasonable middle.** A salesperson who generates $500K earns 5,000 karma (Tier 4 boundary), which feels proportional — they're a "Partner" level contributor through measurable value creation.

---

## 7. Vesting Economics

### 7.1 Model Comparison

The docs contain two conflicting vesting schedules:

**Model A** (value-pricing doc): 25% immediate, 75% linear over 90 days.
**Model B** (fraud-prevention doc): 30-day cliff, then linear over 90 days (120 total).

| Day | Model A (vested %) | Model B (vested %) |
|-----|-------------------|-------------------|
| 0 | 25.0% | 0% |
| 15 | 37.5% | 0% |
| 30 | 50.0% | 0% |
| 45 | 62.5% | 16.7% |
| 60 | 75.0% | 33.3% |
| 90 | 100% | 66.7% |
| 120 | 100% | 100% |

### 7.2 Effective Karma Supply Impact

At any point, total effective karma = Σ(vested karma for each contribution).

For a project with constant karma emission ε/month:
- **Model A:** Effective supply lags raw supply by ~1.5 months
- **Model B:** Effective supply lags raw supply by ~2.5 months

The lag creates a "karma overhang" — unvested karma that will vest in the future, diluting existing holders' effective shares predictably.

### 7.3 New Contributor Cold-Start

A new contributor's first payout under each model (assuming monthly payouts):

**Model A:** First contribution at day 0, first payout at day 30. Vested fraction: 50%. They receive half the karma-implied payout.

**Model B:** First contribution at day 0, first payout at day 30. Vested fraction: 0%. They receive nothing in their first month.

Model B is punishing for new contributors. The 30-day cliff means a contributor's first month is entirely unpaid, which conflicts with the "should feel fair to a newcomer on day 1" constraint.

### 7.4 Recommendation

**Use Model A (25% immediate + 90-day linear).** Rationale:
- Immediate 25% vesting gives new contributors a tangible first payout
- 90-day full vest is long enough to deter hit-and-run (contributors who leave at day 30 forfeit 50%)
- No cliff avoids the "first month is free labor" perception
- Fraud prevention goals are achieved through graduated trust levels (identity score, account age, participation thresholds) rather than vesting cliffs

### 7.5 Abandonment Economics

A contributor who leaves at day D forfeits (100% - vested_D%) of earned karma.

| Departure Day | Forfeited % (Model A) | Effective Penalty |
|---------------|----------------------|-------------------|
| 7 | 69.2% | Severe — almost no return |
| 30 | 50.0% | Significant — half the karma |
| 60 | 25.0% | Moderate — 3/4 retained |
| 90+ | 0% | None — fully vested |

The penalty curve is proportional to abandonment speed, which is the right shape. Quick exits are heavily penalized; committed contributors who leave after the project's direction is set retain most value.

---

## 8. Revenue-to-Karma Exchange Rate

### 8.1 Exchange Rate Trajectories by Archetype

Exchange rate E(t) = R(t) / S(t)

| Archetype | Month 6 | Month 12 | Month 24 | Trend |
|-----------|---------|----------|----------|-------|
| Rocket | $0.27 | $0.42 | $0.34 | Rises then stabilizes |
| Slow Burn | $0.04 | $0.08 | $0.09 | Slowly rising |
| Plateau | $0.20 | $0.13 | $0.09 | Declining (fixed revenue, growing karma) |
| Decline | $0.02 | $0 | $0 | Collapse |
| Ghost | $5.09 | $4.67 | — | High but declining |

### 8.2 Volatility and Damping

Exchange rate volatility comes from two sources:
1. **Revenue volatility:** Monthly revenue fluctuations (seasonal, churn, one-time deals)
2. **Karma supply shocks:** Large contributions or sales events that spike karma

**Proposal — Rolling Average Payouts:**

Instead of spot-rate payouts (R_this_month / S_this_month), use a 3-month trailing average:

```
payout_month = (1 / S_current) * (R_{t} + R_{t-1} + R_{t-2}) / 3
```

This smooths income by 3x while maintaining responsiveness to real trends. Contributors see stable income during normal fluctuations and clear signals during structural changes.

### 8.3 Cross-Project Exchange Rate Disparity

Karma in a $50K/month project: E ≈ $0.50/karma
Karma in a $500/month project: E ≈ $0.05/karma

The tier system uses cumulative cross-project karma. Can someone game this by farming karma on cheap projects for tier advancement, then collecting dividends on expensive projects?

**Analysis:** Contributor X farms 5,000 karma across 10 low-revenue projects → Tier 4 (2.0x multiplier). X has 100 karma on a high-value project.

X's weighted share on the high-value project: (100 * 2.0) / Σ(weighted karma)

Compare to Y with 3,000 project karma at Tier 3 (1.5x): (3,000 * 1.5) / Σ = 4,500

X's weighted karma: 200. Y's weighted karma: 4,500. Y dominates 22.5:1.

**The gaming vector is weak** because per-project karma dwarfs the tier multiplier effect. The only scenario where this flips is extreme tier differential (Tier 5 vs. Tier 1) combined with similar project karma — which would mean the Tier 5 person invested comparable effort on that specific project, just at different times. That's not gaming; that's reward for platform loyalty.

---

## 9. Platform Cost Economics (COGS Model)

The platform takes zero direct cut of project revenue. Instead, platform operational costs are deducted from gross revenue before karma-weighted distribution — the same way a business pays cost of goods sold before distributing profit.

### 9.1 The Distribution Formula

```
distributable_revenue = gross_revenue - platform_costs(project)
payout_i = distributable_revenue * weighted_share_i
```

Where `platform_costs(project)` is the actual cost of servicing that project:

| Cost Component | Scales With | Typical Range |
|---------------|-------------|---------------|
| Hosting/compute | Traffic, storage, uptime tier | $3-200/mo |
| Payment processing | Gross revenue (Stripe ~2.9% + $0.30) | ~3% of gross |
| Karma computation | Contributors, contribution volume | $0.50-5/mo |
| Fraud prevention | Contributor count, flag volume | $1-10/mo |
| Support | Ticket volume | $0-5/mo |

### 9.2 Exchange Rate With Platform Costs

The effective exchange rate becomes:

```
E(t) = (R(t) - C(t)) / S(t)
```

Where C(t) = platform costs for the project at time t.

**Key property:** Higher platform costs correlate with healthier economics. A project incurring $500/mo in platform costs is one with heavy traffic (high hosting), lots of transactions (high payment processing), many contributors (high karma computation), and enough value to attract bad actors (high fraud prevention). These are all signs of a thriving project where R(t) >> C(t).

### 9.3 Cost Impact by Project Scale

| Project Revenue | Platform Costs | Cost % | Distributable | Contributors Get |
|----------------|---------------|--------|---------------|-----------------|
| $100/mo | ~$8 | 8.0% | $92 | 92% of gross |
| $500/mo | ~$20 | 4.0% | $480 | 96% of gross |
| $5,000/mo | ~$165 | 3.3% | $4,835 | 97% of gross |
| $20,000/mo | ~$625 | 3.1% | $19,375 | 97% of gross |
| $100,000/mo | ~$3,050 | 3.1% | $96,950 | 97% of gross |

Platform costs converge toward ~3% at scale (dominated by payment processing fees, which are proportional). Small projects bear a higher percentage burden from fixed costs (base hosting, minimum compute). This is the natural economics of infrastructure — fixed costs spread across revenue.

### 9.4 Why This Is Better Than a Percentage Cut

| Direct Cut (15%) | COGS Model |
|------------------|------------|
| $500 project pays $75 to platform regardless of costs | $500 project pays ~$20 (actual costs) |
| $100K project pays $15K to platform (windfall profit) | $100K project pays ~$3K (actual costs) |
| Platform incentivized to maximize GMV cut | Platform incentivized to minimize operational costs |
| Contributors see arbitrary tax | Contributors see transparent, auditable cost line |
| Feels extractive | Feels like shared infrastructure |

The COGS model aligns platform incentives with contributor interests: the platform earns by providing efficient infrastructure (lower costs = happier contributors = more projects = more scale economies), not by extracting rent from successful projects.

### 9.5 Platform Sustainability Under COGS

Without a percentage cut, platform sustainability depends on:
1. **Scale economies:** Per-project costs drop as infrastructure is amortized across more projects
2. **Infrastructure tier revenue:** Projects choose paid hosting tiers ($15-200/mo) that include margin above cost
3. **Premium subscriptions:** Pro features ($12/mo per contributor) are pure margin
4. **Cost efficiency:** Platform profits when operational cost < what projects pay for infrastructure tiers

At scale (10,000+ projects), the margin on infrastructure tiers + subscriptions exceeds fixed costs. The platform is an infrastructure provider, not a tax collector.

### 9.6 Karma Impact of Platform Costs

Platform costs reduce the exchange rate E(t) but don't change karma mechanics. The impact on karma holders:

```
karma_value_reduction = C(t) / S(t)
```

For a project with 10,000 karma and $165/mo costs: each karma point loses $0.0165/month in value from platform costs. This is negligible at any meaningful project scale.

**Circuit breaker:** If platform costs exceed 20% of gross revenue for 3 consecutive months, the project is flagged for infrastructure tier optimization. Projects should never operate where costs consume a significant fraction of revenue.

---

## 10. Sensitivity Analysis on Key Parameters

### 10.1 Pioneer Bonus

```
M(t) = 1 + pioneer_bonus * e^{-decay_rate * t}
```

| pioneer_bonus | Day-0 Mult | Day-90 Mult | Pioneer Premium (year 1 avg) |
|---------------|-----------|-------------|------------------------------|
| 1.0 | 2.0x | 1.41x | +42% over steady state |
| **2.0 (default)** | **3.0x** | **1.81x** | **+84%** |
| 3.0 | 4.0x | 2.22x | +126% |

At pioneer_bonus = 3.0, day-0 contributions earn 4x steady-state. A single founder who writes the project proposal on day 0 earns as much karma as 4 equivalent contributions later. This is likely too generous for non-code contributions (an Ideation contribution at 4x = 60 karma, comparable to 6 code contributions at steady-state).

**Recommendation:** Keep default at 2.0. The 3.0x day-0 multiplier is aggressive but within reason. Projects that want less early-contributor bias can lower to 1.0-1.5.

### 10.2 Decay Rate

| decay_rate | Half-life (days) | Day-180 Mult | Day-365 Mult |
|-----------|-----------------|-------------|-------------|
| 0.005 | 139 | 1.81x | 1.33x |
| **0.01 (default)** | **69** | **1.33x** | **1.05x** |
| 0.02 | 35 | 1.05x | 1.00x |
| 0.05 | 14 | 1.00x | 1.00x |

At decay_rate = 0.005, the pioneer bonus persists for nearly a year. At 0.05, it vanishes within a month.

**The default (0.01) creates a ~3-month meaningful window and a ~12-month residual tail.** This matches the typical lifecycle where early months are highest-risk.

### 10.3 Contributor Pool Percentage

| contributor_pool_pct | Payout on $10K revenue | Impact on contributor behavior |
|---------------------|----------------------|-------------------------------|
| 60% | $6,000 | Contributors feel shortchanged; retention drops |
| **70% (default)** | **$7,000** | **Balanced** |
| 80% | $8,000 | Better for contributors; less for treasury/platform |

At 60%, the 15% platform fee + 15% treasury + 10% "missing" money creates perception that the platform takes too much. At 80%, the project treasury (now 5%) has almost no reinvestment capacity.

**The default (70%) is the sweet spot.** The 85/15 split in the business model doc (eliminating treasury) is simpler but removes reinvestment capacity. Recommendation: reconcile the docs around 70/15/15.

### 10.4 Tier Multipliers

Current: [0, 0.5, 1.0, 1.5, 2.0, 2.5]

**Spread analysis:** Tier 5 earns 5x what Tier 1 earns for the same raw karma. Is this too steep?

| Multiplier Set | Tier 1→5 Spread | Effect |
|---------------|----------------|--------|
| [0, 0.5, 1.0, 1.5, 2.0, 2.5] (current) | 5x | Strong tier incentive, significant distortion |
| [0, 0.7, 1.0, 1.3, 1.6, 2.0] (compressed) | 2.9x | Moderate incentive, less distortion |
| [0, 0.8, 1.0, 1.2, 1.5, 2.0] (flat) | 2.5x | Weak incentive, minimal distortion |
| [0, 0.3, 1.0, 2.0, 3.0, 4.0] (steep) | 13.3x | Extreme incentive, heavy distortion |

**Recommendation:** The current 5x spread is on the aggressive end. A compressed set like [0, 0.7, 1.0, 1.3, 1.7, 2.2] (3.1x spread) preserves meaningful tier incentive while reducing the cases where tier trumps raw contribution. This is a judgment call — steeper spreads drive tier-grinding behavior (good for retention) but increase resentment from lower-tier contributors (bad for newcomer experience).

---

## 11. Equilibrium Analysis

### 11.1 Stable Equilibrium Conditions

The per-project economy reaches equilibrium when:

```
dE/dt = 0  →  (dR/dt)/R = (dS/dt)/S
```

Revenue growth rate equals karma supply growth rate. In practice, this occurs when:
- Contributor count stabilizes (churn = recruitment)
- Revenue stabilizes (growth = churn)
- Contribution frequency stabilizes

At equilibrium, E = R / S is constant, and contributors earn predictable income.

### 11.2 Self-Correcting Dynamics

**Inflation scenario (karma grows faster than revenue):**
1. Per-karma value E drops
2. Marginal contributors (low karma holders) find payouts insufficient → leave
3. Contributor count drops → karma emission drops
4. E stabilizes or recovers

**Deflation scenario (revenue grows faster than karma):**
1. Per-karma value E rises
2. High per-karma value attracts new contributors
3. Karma emission increases
4. E stabilizes

Both scenarios have **negative feedback loops** that push toward equilibrium. The system is self-correcting.

### 11.3 When Self-Correction Fails

**Case 1: Revenue cliff with no contributor exit.**
Revenue drops to $0, but contributors keep contributing (perhaps hoping for recovery). Karma accumulates against zero revenue. E = 0 indefinitely. Contributors eventually leave, but the psychological damage (months of unpaid work) may cause permanent reputation harm to the platform.

**Circuit breaker:** If a project's revenue drops >80% month-over-month, send explicit notifications to all contributors with their current E trajectory. Transparency prevents silent value destruction.

**Case 2: Whale contributor exit.**
One contributor holds 60% of project karma and leaves. Remaining contributors' shares jump from splitting 40% to splitting 100% of ongoing revenue. This is a windfall. But the departing contributor's karma remains — their share doesn't redistribute, it's just dormant (no payouts if they're below 0.1% threshold... wait, they have 60%, they're definitely above). They continue receiving 60% of revenue indefinitely despite contributing nothing.

**This is the "rest and vest" problem the dilution model was supposed to solve.** But dilution only works if new contributions keep flowing. If the remaining contributors also slow down (demoralized by the whale's dominance), karma emission slows, dilution slows, and the whale retains dominant share.

**Circuit breaker:** Consider a "contribution velocity floor" — if a contributor earns zero new karma for 6 consecutive months, their payout share is gradually reduced (10% per month) until they resume contributing or reach a floor of 50% of their vested share. This is a form of soft decay that applies only to fully inactive contributors, preserving the "no karma decay" principle for anyone maintaining even minimal activity.

**Case 3: Platform-level whale project.**
One project generates 80% of platform revenue. If it leaves, platform revenue drops 80%.

**This is a concentration risk, not a karma economics problem.** Mitigation is business strategy (diversification, retention incentives for high-GMV projects), not parameter tuning.

---

## 12. Failure Mode Catalog

| # | Failure Mode | Trigger | Severity | Self-Corrects? | Circuit Breaker |
|---|-------------|---------|----------|----------------|-----------------|
| 1 | **Karma hyperinflation** | 100+ contributors, 20 contributions each/month | Medium | Yes (dilution makes marginal contributions worthless, people leave) | Cap per-project monthly emissions at 20x the rolling 3-month average. Excess contributions queue for next month. |
| 2 | **Revenue cliff** | Product loses customers | High | No (karma holders trapped) | Explicit notification at >50% revenue drop. Provide "project hibernation" option that freezes karma accounting. |
| 3 | **Ghost project (solo freelancer)** | 1 contributor, all revenue | Low | N/A (stable) | Waive treasury split for single-contributor projects. Display warning that CrowdForge adds 15% overhead vs. direct freelancing. |
| 4 | **Whale contributor rest-and-vest** | Dominant contributor goes dormant | High | Slowly (dilution over months/years) | Contribution velocity floor: 6 months inactivity → gradual payout reduction to 50% of entitled share. |
| 5 | **Tier inflation** | Absolute thresholds become easy to reach | Medium | No | Ratcheted hybrid thresholds (see Section 3.3). Annual recalibration. |
| 6 | **Sales karma dominance** | Salesperson captures >50% of karma | Medium | Partially (more builders join if payouts are high) | Per-project governance can adjust sales_karma_rate. Platform sets maximum sales karma at 50% of total project karma — excess sales karma is capped but still counts toward tier. |
| 7 | **Pioneer exploit (README farming)** | Trivial day-0 contributions at 3.0x | Low | Yes (dilution rapidly erodes trivial contributions) | Minimum karma threshold for pioneer multiplier: contribution must receive at least 1 upvote before multiplier applies. |
| 8 | **Plateau stagnation** | Stable project, no new contributions, frozen shares | Low | N/A (stable state) | Not a failure — this is a healthy mature project. No intervention needed. |
| 9 | **Vesting abandonment** | Contributors leave mid-vest, forfeiting karma | Low | N/A | Forfeited karma is burned (removed from total), not redistributed. This prevents gaming via temporary contributors who inflate then deflate the pool. |
| 10 | **Cross-project tier gaming** | Farm small projects for tier, collect on big projects | Low | N/A (vector is weak per Section 8.3) | No circuit breaker needed. The 2.5x maximum tier multiplier cannot overcome significant project-karma deficits. |
| 11 | **Payout threshold exclusion** | Small contributors stuck below 0.1% threshold forever | Medium | No (dilution pushes them further below) | Allow karma below threshold to accumulate across payout periods. If 6 months of accumulated share exceeds $25, trigger a lump payout. |
| 12 | **Split discrepancy confusion** | Docs say 85/15 in one place and 70/15/15 in another | High | No | Reconcile documentation. Adopt 70/15/15 as canonical. |

---

## 13. Parameters That Must Scale

Most parameters can remain fixed across 10 to 100,000 contributors. These cannot:

| Parameter | Why It Must Scale | Scaling Rule |
|-----------|------------------|-------------|
| Tier thresholds | Absolute thresholds cause tier inflation | Annual recalibration based on median karma (Section 3.3) |
| Contribution velocity limits | Trusted contributors need higher limits | Graduated by trust level (already designed in fraud-prevention doc) |
| Payout minimum ($25) | At high contributor counts, many fall below threshold | Consider lowering to $10 when payment processing costs drop; or batch micro-payouts quarterly |
| Review capacity | At scale, peer review becomes bottleneck for karma attribution | Introduce automated pre-screening (lint, test pass) that auto-accepts routine contributions at reduced karma (0.5x for auto-accepted vs. 1.0x for peer-reviewed) |

---

## 14. Discrepancies Between Design Documents

| Issue | Doc A | Doc B | Impact | Recommendation |
|-------|-------|-------|--------|----------------|
| Revenue split | karma-system: 70/15/15 | business-model: 85/15 | Contributors see different numbers depending on which doc they read | Adopt 70/15/15. Update business model doc. |
| Vesting schedule | value-pricing: 25% immediate + 90d | fraud-prevention: 30d cliff + 90d | New contributors experience different economics | Adopt Model A (25% immediate + 90d). Provides immediate value. |
| Pioneer multiplier | karma-system: continuous decay (3.0x→1.0x) | spawn-protection: phase-based (3x/2x/1.5x/1x) | Two competing time-bonus mechanics | Choose one. The phase-based model from spawn-protection is simpler and integrates with project lifecycle. The continuous model from karma-system is mathematically cleaner. Recommend continuous for underlying math, phase gates for UX presentation. |
| Karma at submission vs. acceptance | karma-system: implied at submission | spawn-protection: explicitly at acceptance only | Determines when karma enters the supply | Adopt "at acceptance" universally. Prevents supply inflation from unreviewed contributions. |

---

## 15. Recommendations Summary

1. **Reconcile the revenue split** to 70/15/15 across all docs.
2. **Adopt Model A vesting** (25% immediate + 90-day linear) — balances fraud prevention with newcomer experience.
3. **Implement ratcheted hybrid tier thresholds** — annual recalibration preserving existing tiers.
4. **Compress tier multipliers** to [0, 0.7, 1.0, 1.3, 1.7, 2.2] — reduces distortion while preserving aspiration.
5. **Add rolling 3-month payout averaging** — smooths exchange rate volatility.
6. **Cap sales karma** at 50% of total project karma — prevents sales-dominated distortions.
7. **Implement contribution velocity floor** — 6 months inactivity triggers gradual payout reduction to 50%.
8. **Waive project treasury** for single-contributor projects — prevents penalizing solo work.
9. **Burn forfeited (unvested) karma** rather than leaving it in the pool — prevents dead-karma supply inflation.
10. **Add 1-upvote gate** on pioneer multiplier — prevents 3x rewards on trivial unvalidated contributions.
