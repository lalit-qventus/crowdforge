# Startup Framework Templates & Structured Collaboration Model

How CrowdForge provides "order to the chaos" -- structured frameworks that guide collaborative startup building without killing creative freedom.

---

## 1. Design Philosophy: Constrain the Process, Not the Output

Every successful accelerator follows the same pattern: provide a container and let participants fill it. EF gives 8 weeks and a matching framework but founders choose their own co-founders and ideas. Antler provides design sprint templates but doesn't dictate what to build. YC gives weekly dinners, office hours, and Demo Day as fixed milestones but founders run their companies autonomously.

CrowdForge applies this same principle at the platform level. The platform tells you what questions to answer, not what answers to give.

Three constraints that work:

1. **Required artifacts, flexible format.** Every Scene must have a Lean Canvas, but the platform never dictates how to fill it in. Require the thinking, not the format.
2. **Prompts over prescriptions.** Instead of "Your MVP must be built in 4 weeks," the platform asks: "What's the smallest thing you can build to test your hypothesis? How long will that take?"
3. **Templates are starting points, not cages.** Every template includes "None of these fit? Describe your own approach." The framework is a scaffold you can climb off of.

What this means in practice: a Scene that skips the validation stage and goes straight to building gets a visible flag ("This Scene hasn't completed problem validation") but is never blocked. The flag is information for potential contributors, not a gate. Some of the best startups skip validation because the founder lived the problem for years. The platform surfaces the information and lets the ensemble decide.

---

## 2. Scene Lifecycle: Five Stages

Drawn from Lean Startup's Build-Measure-Learn, YC's "make something people want," and EF's Form-Ideate-Validate structure. Adapted for CrowdForge's ensemble model where there is no single founder running the show -- there is a champion who lit the campfire and an ensemble who tends it.

```
IDEATION --> VALIDATION --> BUILD --> LAUNCH --> GROWTH
```

### Stage 1: Ideation (The Pitch)

**Goal:** Articulate a problem worth solving and attract an ensemble.

**Required artifacts:**

| Artifact | What It Captures | Inspired By |
|---|---|---|
| Problem Statement | One sentence. "When [situation], [target user] wants to [motivation], so they can [expected outcome]." | Jobs To Be Done (Christensen) |
| Target User | Specific and narrow. "Young professionals in NYC who commute by subway" not "people who travel." | Antler's market specificity requirement |
| Why Now | What changed in the world that makes this possible or necessary today? Technology shift, regulation change, behavioral change. | YC application: "Why did you pick this idea?" |
| The Secret | What non-obvious insight does this rest on? What do you know that most people don't? | Thiel's Zero to One |
| Existing Alternatives | How do people solve this problem today? What do they spend time or money on? | YC application: "Who desperately needs this?" |

**Platform tools at this stage:**
- Guided pitch card builder (fill-in prompts, not blank fields)
- Idea Ring for 72-hour community voting (25-vote quorum, 60% threshold)
- Competitor research template
- "Similar Scenes" matching -- surface existing Scenes working on related problems

**Stage gate:** Idea Ring vote passes. This is the only hard gate in the system. Everything after this is progressive disclosure of tools and increasing governance, not permission to proceed.

**What YC would ask at this stage:**
- "Describe what your company does in one or two sentences." (Clarity test -- if you can't, you don't understand it yet.)
- "Who desperately needs this?" (Not "who might use this" -- desperation signals real demand.)
- "What's new about what you're making?" (The Secret in YC language.)

### Stage 2: Validation (Seed Phase)

**Goal:** Prove the problem is real and find the first believers.

**Required artifacts:**

| Artifact | What It Captures |
|---|---|
| Lean Canvas | All 9 boxes: Problem, Customer Segments, UVP, Solution, Channels, Revenue, Costs, Key Metrics, Unfair Advantage |
| User Interview Log | Minimum 10 conversations with potential users who are not friends or family. Direct quotes, not summaries. |
| Hypothesis Statement | "We believe [solution] will solve [problem] for [segment]. We'll know we're right when [measurable signal]." |
| MVP Scope | The smallest thing that tests the core hypothesis. Ruthlessly minimal. |

**Platform tools at this stage:**
- Lean Canvas builder with guided prompts per box
- User interview script template (what to ask, what not to ask, how to avoid leading questions)
- Landing page generator for demand testing
- Seed ensemble formation: champion hand-picks 3-7 members, human-only, 30+ day account age

**Stage gate:** No hard gate. The platform surfaces a validation health indicator based on artifacts completed. A Scene that starts building without validation gets flagged, not blocked.

**What Antler evaluates at this stage:**
- Problem-solution fit: Does the solution actually address the articulated problem?
- Market validation: Have you talked to real people? What did they say?
- Team composition: Do you have complementary skills to execute?

**What EF's "Edge" framework adds:**
EF asks every founder: "What's your unfair advantage?" This maps to CrowdForge's "Secret" field but extends to the ensemble -- what combination of skills and domain knowledge exists in this group that makes them uniquely suited to solve this?

### Stage 3: Build (Active Development)

**Goal:** Ship an MVP and get it in front of real users.

**Required artifacts:**

| Artifact | What It Captures |
|---|---|
| Architecture Decision | Technical approach, stack choices, deployment strategy |
| Success Metric | Defined before building. "We'll know the MVP works when [X users do Y within Z time]." |
| Weekly Update | What did we learn? What will we do next week? Where are we stuck? |

**Platform tools at this stage:**
- Forge editor with live preview
- One-click staging deployment to `scenename.crowdforge.app`
- Built-in observability: error tracking, basic analytics
- Riff claiming system (48-hour expiry, max 3 active claims per contributor)
- AI agent participation opens (with rate limits from fraud prevention)

**Stage gate:** None. Building can start whenever the ensemble is ready. The platform provides structure through the weekly update cadence, not through blocking.

**What Paul Graham would say at this stage:**
- "Talk to users, write code." The only two activities that matter.
- "Do things that don't scale." Recruit users manually, one by one. Create an insanely great experience for the first 10.
- "Launch fast." Ship something, anything, and get it in front of real humans.

### Stage 4: Launch (Going Live)

**Goal:** Product is live with real users. Revenue tracking begins.

**Required artifacts:**

| Artifact | What It Captures |
|---|---|
| Launch Checklist | Domain configured, SSL active, payment integration, analytics running |
| Growth Channel | Primary acquisition path identified and documented |
| Revenue Model | How money comes in. Pricing tested or at least hypothesized. |

**Platform tools at this stage:**
- One-click production deployment with custom domain
- SSL certificate provisioning
- Payment integration (Stripe connect) with automatic revenue tracking
- Ad performance monitoring with automated alerts
- User interest tracking: signup rates, activation, retention cohorts
- "Default Alive/Dead" calculator based on burn rate vs. revenue trajectory

**Stage gate:** None, but the platform starts surfacing health scores prominently once a Scene launches.

**Growth rate benchmarks (from YC):**

| Growth Rate | Assessment |
|---|---|
| 10%+ WoW | Exceptional -- sustain this |
| 5-7% WoW | Good -- the YC standard |
| 2-4% WoW | Mediocre -- run more experiments |
| 0-1% WoW | Stalled -- re-evaluate product-market fit |
| Negative | Declining -- immediate attention required |

### Stage 5: Growth (Scaling)

**Goal:** Post-product-market-fit. Repeatable acquisition, growing revenue, expanding the ensemble.

**Required artifacts:**

| Artifact | What It Captures |
|---|---|
| Unit Economics | CAC, LTV, LTV:CAC ratio, payback period |
| Go-to-Market Playbook | Documented acquisition channels that work and don't |
| Contributor Roles | Defined roles and needs -- what skills does the Scene need next? |

**Platform tools at this stage:**
- Advanced analytics dashboard
- Competitive intelligence monitoring
- Automated pivot/persevere suggestions based on data patterns
- Revenue distribution tracking with contributor karma breakdown
- Ad management integration
- SEO and growth channel analytics

---

## 3. The "Yes, And..." Contribution Model

### How Contributions Flow

In improv, "Yes, and..." means accepting what your scene partner offers and building on it. The opposite -- "No, but..." -- kills scenes. CrowdForge structures this principle into the contribution mechanics.

**The structural mechanic:**

1. Anyone can propose a Riff (contribution) to any open Scene.
2. Riffs are accepted by default unless the Scene champion or peer reviewers reject them within 48 hours.
3. Rejection requires a reason. Not "I don't like it" but "This conflicts with [architecture decision / user feedback / existing Riff]."
4. A rejected Riff can be forked -- the contributor takes their work and builds it as an alternative approach. The ensemble can later merge it back if it proves better.
5. Riffs that build on existing Riffs earn a "building on" attribution that is visible in the contribution graph.

**Why accept-by-default matters:**

Traditional open source uses a submit-and-wait model where a maintainer reviews and decides. This creates a bottleneck that kills momentum. It also creates a power dynamic where gatekeepers determine what gets in. CrowdForge inverts this: contributions flow in, and the bar for rejection is higher than the bar for acceptance. The ensemble self-corrects through karma -- good Riffs get upvoted and earn more karma; ignored Riffs earn only base karma and fade through dilution.

This is the "Yes, and..." operating system. The default is "yes." The "and" is what the next contributor adds on top.

**What this does NOT mean:**
- It does not mean anything goes. Scene champions can define contribution guidelines (code style, design system, architecture constraints).
- It does not mean no review. Peer review still happens -- it determines karma multipliers, not access.
- It does not mean AI agents dump unlimited Riffs. Rate limits from the fraud prevention system apply.

### Structured Contribution Proposals

When someone wants to contribute to a Scene, the platform prompts them to specify:

| Field | Prompt |
|---|---|
| **What** | What specifically are you offering to do? |
| **Why** | How does this connect to the Scene's current stage and goals? |
| **Evidence** | What makes you think this will help? User feedback, data, domain expertise? |
| **Scope** | How long will this take? What does "done" look like? |
| **Builds On** | Which existing Riffs does this extend or complement? |

This gives the "Yes, and..." energy a productive channel. The contribution references what already exists (the "yes") and adds something new (the "and"). Random drive-by suggestions that don't connect to the Scene's artifacts naturally attract less karma because they're harder for peers to validate.

### Anti-Pattern Detection

The platform monitors for "No, but..." behavior -- patterns that indicate a contributor is blocking rather than building:

| Signal | Detection | Response |
|---|---|---|
| High rejection rate | Champion rejects >40% of Riffs over 30 days | Warning + independent review of recent rejections |
| Scope policing without contribution | Contributor flags scope violations but never submits Riffs | Flag surfaced to ensemble; opinion weight reduced in reviews |
| Duplicate gatekeeping | Multiple contributors coordinating rejections of the same contributor's work | Anti-gatekeeping detection from governance system triggers |

---

## 4. Idea Evaluation Scorecard

Every Idea Ring pitch is evaluated by community voters across four dimensions. Voters score each criterion 1-5. The composite score determines whether the Scene gets seeded.

### Market and Problem (Weight: 35%)

| Criterion | Score 1 (Weak) | Score 5 (Strong) |
|---|---|---|
| Problem Severity | Nice-to-have | Hair-on-fire problem |
| Market Size | Tiny niche, no expansion path | Large addressable market or expanding niche |
| Frequency | User encounters problem rarely | Daily or continuous pain point |
| Willingness to Pay | No evidence anyone would pay | Users already paying for inferior solutions |
| Timing (Why Now) | No reason this needs to exist now | Clear catalyst: tech shift, regulation change, behavioral change |

### Solution and Differentiation (Weight: 25%)

| Criterion | Score 1 (Weak) | Score 5 (Strong) |
|---|---|---|
| 10x Factor | Marginal improvement | Dramatically better in a clear dimension |
| Secret / Insight | Obvious idea anyone could have | Non-obvious insight from domain expertise |
| Defensibility | No moat; anyone can copy this | Network effects, data advantages, or switching costs |
| Simplicity | Requires explaining a complex concept | Instantly understood value proposition |

### Execution Feasibility (Weight: 20%)

| Criterion | Score 1 (Weak) | Score 5 (Strong) |
|---|---|---|
| MVP Speed | Needs months to build anything testable | Can test core hypothesis in days or weeks |
| Skills Available | No one in the community has the required skills | Contributors with relevant expertise already interested |
| Regulatory Risk | Heavy regulation, unclear legal landscape | No significant regulatory barriers |

### Team and Traction (Weight: 20%)

| Criterion | Score 1 (Weak) | Score 5 (Strong) |
|---|---|---|
| Champion Commitment | Part-time curiosity | Full-time obsession with this problem |
| Domain Expertise | No relevant experience | Deep domain knowledge or lived experience |
| Early Signals | No validation attempted | Landing page signups, letters of intent, or waitlist |
| Community Energy | No one else engaged | Multiple contributors actively interested |

### Composite Score Interpretation

- **4.0-5.0:** High-conviction Scene. Fast-track to active development.
- **3.0-3.9:** Promising but has gaps. Platform surfaces specific weaknesses for the champion to address.
- **2.0-2.9:** Needs significant work. Recommend returning to problem validation.
- **Below 2.0:** Does not meet threshold. Archive with documented feedback so the champion can iterate.

---

## 5. Scene Health Dashboard

### Automated Health Score (0-100)

Computed weekly, visible to the ensemble and to potential contributors browsing Scenes:

```
HEALTH SCORE (0-100)

  Growth Health (0-25)
    WoW growth rate vs. benchmarks
    Growth trend: accelerating, steady, or decelerating
    Growth channel diversity

  Engagement Health (0-25)
    DAU/MAU ratio
    Session frequency and depth
    Feature adoption breadth
    Retention curve shape

  Team Health (0-25)
    Contributor activity: Riffs, discussions, reviews
    Response time to user feedback
    Milestone completion rate
    Decision velocity

  Validation Health (0-25)
    User interviews conducted this period
    Experiments run and documented
    Hypothesis log updated
    Revenue or payment validation progress
```

### Automated Suggestions

The platform surfaces recommendations based on data patterns, not opinions:

**Suggest Pivot When:**
- Growth flat for 3+ consecutive weeks despite active experimentation
- Sean Ellis score below 40% after multiple iterations
- Retention curve declines to near-zero within 30 days
- Multiple growth channels tested with no sustainable CAC

**Suggest Persevere When:**
- Activation and retention trending positively, even if slowly
- User feedback enthusiastic about core value proposition
- Retention curve flattening (some users stick permanently)
- Each experiment producing validated learning

**Suggest Archive When:**
- No growth, no engagement, no validation after a full milestone cycle
- Champion has disengaged for 30+ days
- Problem hypothesis invalidated with no viable pivot
- Zero revenue signal despite multiple monetization attempts

These are surfaced as data-driven nudges, not mandates. The ensemble decides.

---

## 6. The Two-Track System: Scene Contributions vs. Platform Contributions

This is the "sacrosanct boundary" described in the platform governance design. Scene contributions and platform contributions operate under fundamentally different rules because they carry fundamentally different risks.

### Track 1: Scene Contributions (Karma-Based, Open)

| Property | How It Works |
|---|---|
| Who can contribute | Anyone with a CrowdForge account |
| Approval model | Accept-by-default; rejection requires reason |
| Reward | Karma that converts to revenue share |
| AI participation | Yes, with rate limits |
| Risk if gamed | One Scene gets diluted karma |
| Governance | Peer review + Scene champion |
| Philosophy | "Yes, and..." -- build on what exists |

Scene contributions are the creative heart of the platform. The bar for participation is low. The quality signal comes from karma mechanics: good Riffs get upvoted and compound; mediocre Riffs earn base karma and dilute. The system self-corrects through economic incentives, not access control.

### Track 2: Platform Contributions (Security-Reviewed, Different Rewards)

| Property | How It Works |
|---|---|
| Who can contribute | Anyone with a CrowdForge account |
| Approval model | Multi-reviewer approval; self-approval prohibited |
| Reward | Admin privileges, cosmetics, custom skins, hiring pipeline visibility |
| AI participation | Restricted -- human review required for all platform changes |
| Risk if gamed | Entire platform gets hijacked |
| Governance | Core team quorum; tiered by blast radius |
| Philosophy | Defense in depth -- multiple independent approvals |

Platform contributions change the infrastructure that every Scene runs on. A compromised Scene affects one ensemble; a compromised platform affects everyone. The approval requirements scale with blast radius:

| Change Category | Required Approvals |
|---|---|
| Cosmetic / Docs | 1 core reviewer |
| Feature | 2 core reviewers |
| System (karma formulas, trust thresholds, payout logic) | 2 core reviewers + 1 steward |
| Security-Critical (auth, payments, fraud rules) | 2 stewards + security audit |
| Governance (changes to the governance process itself) | All stewards + 7-day public comment period |

### Why Different Rewards

Platform contributors don't earn karma. This is deliberate. If platform contributions earned karma, the same karma-gaming attacks that fraud prevention handles for Scenes would now threaten the platform itself. Instead, platform contributors earn:

- **Admin privileges:** Elevated platform capabilities (moderator tools, reviewer status, steward eligibility)
- **Cosmetics:** Custom profile themes, badges, special UI treatments
- **Hiring pipeline:** Platform contributors are visible to companies hiring through CrowdForge's network. Sustained platform contribution is a signal of engineering depth, security awareness, and systems thinking.

These rewards create a different incentive structure: platform contributors are motivated by status, responsibility, and career advancement rather than direct revenue. This attracts a different (and complementary) contributor profile -- the infrastructure-minded builder who cares about the platform's integrity.

---

## 7. Revenue Model Templates

Every Scene should identify its revenue model early. The platform provides guided templates for common models:

### SaaS (Software-as-a-Service)

| Element | Guidance |
|---|---|
| Pricing model | Tiered (Free/Pro/Enterprise) or usage-based |
| Key metrics | MRR, ARR, churn rate, LTV, CAC, LTV:CAC ratio |
| Benchmark targets | Monthly churn < 5%, LTV:CAC > 3:1, payback < 12 months |
| Revenue milestones | $1K MRR, $10K MRR, $100K ARR, $1M ARR |
| Critical question | Is this a painkiller (must-have) or vitamin (nice-to-have)? |

### Marketplace

| Element | Guidance |
|---|---|
| Pricing model | Transaction fee (%), listing fee, or subscription for sellers |
| Key metrics | GMV, take rate, liquidity (matches per listing), supply/demand balance |
| Benchmark targets | Take rate 10-30% depending on category |
| Revenue milestones | First transaction, $10K GMV, $100K GMV |
| Critical question | Which side do you acquire first? How do you solve chicken-and-egg? |

### API / Developer Tools

| Element | Guidance |
|---|---|
| Pricing model | Usage-based (per API call), tiered plans, enterprise contracts |
| Key metrics | API calls/month, developer signups, time-to-first-call |
| Benchmark targets | Time to first API call < 15 minutes |
| Revenue milestones | First paying developer, 100 active developers, $10K MRR |
| Critical question | Is this a "build vs. buy" decision developers will choose to buy? |

### Freemium

| Element | Guidance |
|---|---|
| Pricing model | Free core product + premium features or capacity |
| Key metrics | Free-to-paid conversion rate, time to conversion, feature adoption by tier |
| Benchmark targets | Free-to-paid conversion 2-5%, with 15-20% within first year |
| Revenue milestones | First paid conversion, 100 paying users, $10K MRR |
| Critical question | Is the free tier valuable enough to hook users but limited enough to drive upgrades? |

### Content / Media

| Element | Guidance |
|---|---|
| Pricing model | Advertising, sponsorships, premium subscriptions, events |
| Key metrics | Subscribers, engagement rate, ad RPM, subscriber growth |
| Benchmark targets | Email open rate > 40%, paid conversion > 5% of free |
| Revenue milestones | First sponsor, $1K/month revenue, $10K/month |
| Critical question | Can you build a loyal audience before monetizing? |

---

## 8. The Pitch Canvas

The standard "problem/solution" pitch is incomplete. CrowdForge Scenes present themselves using an expanded structure:

1. **The Hook (5 seconds):** One sentence that makes someone lean in. A provocative insight or surprising fact, not a problem statement.

2. **The "Why Now":** What has changed in the world that makes this possible or necessary today?

3. **The Secret:** What non-obvious insight does this ensemble have that others don't?

4. **The Problem:** Who hurts and how badly? Quantify the pain. Show that people are already spending time or money on inferior solutions.

5. **The Solution:** What does this product do, in concrete terms? Demo or walkthrough, not abstract descriptions.

6. **The Evidence:** What validation exists? User quotes, signup numbers, revenue, engagement data.

7. **The Market:** How big can this get? Start with the narrow beachhead, then show the expansion path.

8. **The Model:** How does money come in? What are unit economics, even projected?

9. **The Moat:** Why can't someone else copy this? Network effects, data advantages, brand, switching costs.

10. **The Ensemble:** Why is this the right group to build this? Relevant experience, complementary skills, commitment level.

11. **The Ask:** What does this Scene need right now? Contributors, specific skills, users, feedback.

This canvas is both the Scene's pitch to attract contributors and its self-assessment tool. Each field maps to an Idea Evaluation Scorecard criterion, so filling out the Pitch Canvas directly improves the Scene's composite score.

---

## 9. Weekly Rituals

Structure through cadence, not surveillance. Borrowed from YC's weekly dinners and EF's weekly check-ins.

### The Weekly Update (Required)

Every active Scene publishes a weekly update answering three questions:

1. **What did we learn this week?** Not "what did we build" -- what validated learning came from what we built or tested?
2. **What will we do next week?** Concrete experiments and Riffs, not vague aspirations.
3. **Where are we stuck?** Blockers, skill gaps, unanswered questions. This is an invitation for the community to help.

Updates are visible to the entire platform. This creates peer accountability without top-down enforcement. A Scene that hasn't posted a weekly update in 3 weeks gets a visible "inactive" flag.

### The Health Check (Automated)

The platform computes and displays the Health Score (Section 5) every Monday. Scenes with declining health get surfaced to the community as "needs help" -- an invitation for experienced contributors to offer guidance, not a punishment.

### Milestone Celebrations (Automatic)

When a Scene hits a milestone, the platform celebrates it visibly:
- First Riff accepted
- First 10 contributors
- First user signup
- First revenue dollar
- $1K MRR
- $10K MRR

These create the emotional moments described in the vision doc. They're also social proof signals that attract new contributors.

---

## 10. Matching Contributors to Scenes

Drawing from EF's co-founder matching and Antler's 50-question survey, but adapted for an open ensemble model where contributors join multiple Scenes.

### Skill Matching

Contributors self-declare skills during onboarding:
- Technical: languages, frameworks, infrastructure, data, ML
- Design: UI/UX, branding, motion, illustration
- Business: marketing, sales, growth, operations, finance
- Domain: industry expertise (fintech, healthtech, edtech, etc.)

Scenes declare what they need through the "Team Need" tags (needs-technical, needs-design, needs-marketing, needs-domain-expert, needs-data).

The platform matches available contributors to Scenes that need their skills, weighted by:
- Skill match quality
- Contributor's karma history (higher karma = more reliable signal)
- Scene health score (struggling Scenes get priority matching)
- Contributor's declared availability

### Working Style Compatibility

Beyond skills, EF and Antler both emphasize working style fit. CrowdForge captures this through lightweight profile questions:

- **Pace:** Do you prefer shipping fast and iterating, or planning thoroughly first?
- **Communication:** Do you prefer async (written) or sync (calls/chat)?
- **Ambiguity tolerance:** Are you comfortable starting work without a clear spec?
- **Feedback style:** Do you prefer direct critique or diplomatic suggestions?

These aren't used as hard filters -- they're surfaced to Scene champions when reviewing contributor requests, giving context about potential fit.

---

## 11. Platform-Provided Tooling by Stage

Each stage unlocks additional platform tooling. Tools are always available, but the platform highlights what's most relevant at each stage.

| Stage | Primary Tools | Monitoring |
|---|---|---|
| Ideation | Pitch Card builder, Idea Ring voting, competitor research template | Community engagement with pitch |
| Validation | Lean Canvas builder, interview script template, landing page generator | Landing page conversion, interview count |
| Build | Forge editor, staging deployment, CI/CD, error tracking | Riff velocity, contributor activity, code quality signals |
| Launch | Production deployment, custom domain, SSL, payment integration | Growth rate, signup/activation/retention, revenue |
| Growth | Advanced analytics, ad management, competitive intelligence, A/B testing | Unit economics, channel performance, health score |

### Observability Stack

Available from the Build stage onward:
- Error tracking with automatic Riff attribution (which Riff introduced this error?)
- Basic analytics: page views, unique visitors, session duration
- Uptime monitoring with automatic incident alerts
- Performance monitoring: response times, throughput

### Ad Management

Available from the Launch stage onward:
- Integration with major ad platforms
- Automated alerts: CPA rising above LTV, CTR dropping below benchmarks, winning creative identified
- ROAS tracking with channel-level breakdown
- Budget recommendations based on unit economics

### Competitive Intelligence

Available from the Launch stage onward:
- Monitoring for similar products on Product Hunt, HN, and social media
- Competitor pricing change alerts
- Competitor funding announcements
- SEO ranking changes for key terms

---

## 12. What Makes This Feel Authoritative

CrowdForge's framework should feel like it was built by someone who has deployed a lot of startups. That authority comes from three design choices:

**1. Frameworks drawn from proven sources, clearly attributed.**

Every template traces back to YC, EF, Antler, Lean Startup, or another established methodology. The platform doesn't invent novel frameworks -- it curates and adapts the best ones for ensemble collaboration. Attribution is explicit: "This evaluation scorecard is adapted from YC's application criteria and Antler's investment committee dimensions."

**2. Opinionated defaults with escape hatches.**

The platform has opinions: weekly updates are required, Lean Canvas is the default planning tool, the Idea Evaluation Scorecard weights Market & Problem at 35%. But every opinion has an override. A Scene champion who has a better framework can use it. The defaults exist so that Scenes that don't know what framework to use get a good one automatically.

**3. Real data, not motivational platitudes.**

The platform surfaces growth benchmarks ("5-7% WoW is good, 10%+ is exceptional"), failure pattern data ("42% of startups fail because they build something nobody wants"), and health scores based on quantitative signals. The voice is direct and practical -- not "you can do it!" but "here's what the data says about Scenes like yours."

### Content Voice

Sound like a seasoned founder advising a friend. Direct, practical, specific. "Here's what actually works."

Do not sound like a business school textbook, a motivational speaker, or a corporate blog. No jargon without explanation. No aspirational fluff.

Benchmark voices:
- Paul Graham's essays: clear thinking, strong opinions, simple language
- First Round Review: operational depth, specific numbers and tactics
- Hacker News community norm: direct, practical, from-the-trenches

---

## 13. Comparison with Accelerator Frameworks

| Dimension | YC | EF | Antler | CrowdForge |
|---|---|---|---|---|
| Starting point | Existing team + idea | Individual talent, no team or idea | Individual or team, idea optional | Anyone with an idea; ensemble forms around it |
| Team formation | Pre-formed | 8-week structured matching | Speed dating + 50-question survey | Self-selection around Scenes, skill-matched |
| Idea validation | "Make something people want" | Edge framework: find your unfair advantage | 6-step hypothesis testing | Idea Ring community vote + scorecard |
| Stage structure | Batch-based (3 months) | Form (14 weeks) + Launch (3 months) | Phase One (10 weeks) + Phase Two (4 months) | Continuous, milestone-driven |
| Approval gate | Demo Day investor pitch | Investment Committee | Investment Committee | Community vote at Ideation; progressive health signals after |
| Revenue model | Equity (7%) | Equity (~10%) | Equity (varies) | Zero commission; karma-based revenue share |
| Scale | ~500 companies per batch | ~50-100 per cohort | ~50-100 per cohort | Unlimited concurrent Scenes |
| AI participation | N/A | N/A | N/A | First-class contributor with rate limits |
| Post-program | Alumni network | Portfolio support | Platform access | Permanent -- Scenes live as long as the ensemble tends them |

### What CrowdForge borrows:
- From YC: "Make something people want" as the north star; growth benchmarks; emphasis on talking to users
- From EF: Structured team formation; the "Edge" concept adapted as "The Secret" field; complementary skill matching
- From Antler: Multi-phase validation; structured co-founder compatibility assessment; design sprint templates
- From Lean Startup: Build-Measure-Learn loop; hypothesis-driven development; pivot/persevere decision framework

### What CrowdForge rejects:
- Equity-based models (zero commission, karma-based revenue share instead)
- Batch constraints (Scenes are continuous, not time-boxed)
- Centralized approval committees (community vote replaces investment committee)
- Fixed team structures (fluid ensembles, not co-founder pairs)

---

## Appendix A: User Validation Checklist

Before a Scene moves from Validation to Build, the platform recommends (but does not require) completing these tiers:

### Tier 1: Minimum Validation

- Talked to at least 10 potential users who are not friends or family
- Can articulate the problem in the user's words (direct quotes)
- Users are currently spending time or money solving this problem some other way
- At least 3 users said they would use or pay for a solution

### Tier 2: Strong Validation

- Landing page with clear value proposition
- At least 100 page visitors
- Email signup or waitlist conversion rate > 10%
- Competitive analysis completed
- One-paragraph "why now" explanation

### Tier 3: High-Conviction Validation

- Pre-orders or letters of intent received
- Users have paid money before the product exists
- Pilot customer identified and committed
- Champion has deep personal experience with the problem

## Appendix B: Go-to-Market Playbook Templates

### Direct Sales (B2B)
1. Define ICP: industry, size, role, budget
2. Build target list of 100 companies
3. Reach out manually: email, LinkedIn, warm intros
4. Offer free pilots or consultations
5. Track: meetings booked, demos given, conversion rate, deal size
6. Milestone: first 10 paying customers through direct outreach

### Product-Led Growth (B2C / SMB SaaS)
1. Build a product that's self-serve (signup to value in < 5 minutes)
2. Create viral loops or referral mechanics
3. Content marketing: SEO, social, community presence
4. Track: signups, activation rate, time-to-value, viral coefficient
5. Milestone: 1,000 organic signups without paid acquisition

### Community-Led Growth
1. Identify where target users already gather (Reddit, Discord, HN, Twitter)
2. Become a genuine contributor in those communities
3. Share the product naturally, not as a launch announcement
4. Build your own community around the problem space
5. Track: community size, engagement, conversion from community to product
6. Milestone: 500 active community members, measurable product adoption

### Paid Acquisition
1. Start with small budgets ($5-10/day) to test channels
2. Test 3-5 different ad creatives and audiences
3. Measure CAC against projected LTV
4. Only scale channels where CAC < 1/3 of LTV
5. Track: CPA, ROAS, conversion rate, payback period
6. Milestone: at least one channel producing users at sustainable CAC
