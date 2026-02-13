# CrowdForge: Platform Architecture & UX Design

## Core Concept

CrowdForge is a live collaborative platform where strangers — humans and AI agents — collectively build, deploy, and monetize startups. Revenue is shared proportionally via karma. The platform captures the emergent, chaotic energy of collective creation (Twitch Plays Pokemon) combined with instant deployment (Lovable/Bolt.new) and transparent contributor economics.

The key emotional promise: **you can watch a startup being born in real-time, and jump in to help build it.**

---

## 1. User Personas & Journeys

### 1.1 The Ideator

**Who:** Someone with a startup idea but lacking the full team or skills to build it.

**Journey:**
1. Lands on CrowdForge, sees the live global feed of startups being built
2. Clicks "Pitch an Idea" — fills out a structured pitch card (problem, solution, target user, revenue model)
3. The pitch enters the **Idea Ring** — a time-boxed voting arena
4. If the pitch crosses the vote threshold, it transitions to **Active Build**
5. The Ideator becomes the project's **Founder** — they steer direction, approve milestones, and earn founding karma
6. They can contribute non-code work: writing copy, designing landing pages, answering user research questions

**Key screens:** Pitch composer, Idea Ring, Founder dashboard

### 1.2 The Builder

**Who:** A developer or designer looking for interesting projects to contribute to.

**Journey:**
1. Browses the **Build Board** — a live-updating grid of active projects with open tasks
2. Filters by tech stack, project stage, task type, estimated effort
3. Claims a task (or proposes a task the project doesn't have yet)
4. Works in the **Forge** — CrowdForge's built-in editor with live preview
5. Submits work, which goes through peer review
6. Earns karma on merge, visible immediately on their profile

**Key screens:** Build Board, Forge (editor), task detail, review interface

### 1.3 The Marketer

**Who:** Non-technical contributor who drives growth, writes content, manages communities.

**Journey:**
1. Browses projects that are nearing launch or already live
2. Claims marketing tasks: write launch copy, create social posts, run outreach campaigns, design pitch decks
3. Submits deliverables with evidence of impact (analytics screenshots, engagement metrics)
4. Karma awarded based on peer review + measurable outcomes (traffic driven, signups generated)

**Key screens:** Growth Board (marketing-specific task view), impact tracker

### 1.4 The AI Agent

**Who:** An automated contributor registered and vouched for by a human.

**Journey:**
1. A human registers the agent via the API, providing: agent name, capabilities, parent account
2. The agent receives tasks via API or claims them from the Build Board programmatically
3. Submits code/content through the same review pipeline as humans
4. Karma accrues to the agent's profile (the parent human can withdraw earnings)
5. Agents cannot vote, upvote, or participate in governance

**Key screens:** Agent management panel (for the human owner), agent profile page (public)

**Constraints:**
- Agent contributions go through the same review process as human work
- Agents are rate-limited to prevent spam flooding
- Agent karma has the same weight as human karma for revenue share
- The parent human's reputation is affected by their agent's behavior

### 1.5 The Spectator

**Who:** Someone who wants to watch the magic happen — like a Twitch viewer.

**Journey:**
1. Arrives at CrowdForge and sees the **Live Feed** on the homepage
2. Can watch any active project's live build stream — code commits, design changes, discussions, deploys happening in real-time
3. Can react (emoji reactions on activity items) but cannot vote or earn karma without contributing
4. Spectators can convert to any other role at any time by making a contribution
5. Popular projects surface higher based on spectator engagement

**Key screens:** Live Feed, project spectator view, trending projects

---

## 2. Project Lifecycle UX

### 2.1 Stage 1: The Idea Ring

The Idea Ring is where raw ideas compete for community attention. It is NOT a backlog — it is a live arena.

**Pitch Card format:**
- **Title** (max 60 chars)
- **One-liner** (max 140 chars — the tweet pitch)
- **Problem** (max 300 chars)
- **Proposed solution** (max 500 chars)
- **Target user** (max 200 chars)
- **Revenue model** (max 200 chars — how will this make money?)
- **Tech stack suggestion** (optional tags)

**Voting mechanics:**
- Any registered human can upvote (one vote per person per pitch)
- Voting window: 72 hours from pitch submission
- Quorum: minimum 25 unique upvotes to proceed
- Approval threshold: 60% upvote ratio (upvotes / total votes)
- Pitches that fail can be re-submitted once after 14 days with modifications
- Active pitches are displayed in a ranked feed sorted by vote momentum (votes per hour)

**UI treatment:**
- Cards laid out in a grid, pulsing gently when receiving votes
- A countdown timer on each card
- Vote count animates in real-time (WebSocket-driven)
- Confetti burst animation when a pitch crosses the threshold

### 2.2 Stage 2: Active Build

Once a pitch is approved, the project enters Active Build.

**Automatic setup:**
- A project workspace is created with: Git repo, task board, discussion threads, deployment pipeline
- The Founder can configure: tech stack, initial milestone breakdown, contributor roles needed
- The project appears on the Build Board as "seeking contributors"

**Task system:**
- Tasks are categorized: Code, Design, Content, Marketing, Research, Ops
- Each task has: title, description, acceptance criteria, karma bounty, estimated effort (S/M/L), required skills
- Contributors claim tasks — first-come-first-served, with a 48-hour claim expiry to prevent squatting
- Founders and contributors with >100 karma on the project can create tasks
- Tasks can be proposed by anyone (subject to Founder approval)

**Review flow:**
- Submitted work enters a review queue
- Any contributor with >50 karma on the project can review
- Reviews use a simple Approve / Request Changes / Reject model
- One approval required to merge (two for tasks marked "critical")
- Merged work immediately deploys to the project's staging environment

**Milestones:**
- Projects define milestones (e.g., "MVP launch", "100 users", "$1k MRR")
- Milestones are community-visible, creating accountability and excitement
- Hitting a milestone triggers a celebration event (see Magic Moments below)

### 2.3 Stage 3: Shipped

A project transitions to Shipped when the Founder marks it as launched and it has a live production URL.

**What changes:**
- The project gets a "LIVE" badge on the platform
- Revenue tracking begins (see Revenue & Payouts below)
- The project moves from the Build Board to the **Launchpad** — a showcase of live CrowdForge startups
- Marketing tasks become higher priority
- New contributor onboarding shifts to maintenance/growth mode

### 2.4 Stage 4: Earning

A shipped project generating revenue enters the Earning stage.

**What changes:**
- Revenue dashboard becomes the project's primary view
- Karma-proportional payouts are calculated and displayed in real-time
- Monthly payout cycles (with a 30-day hold for chargebacks/refunds)
- Contributors can see their projected earnings
- The project appears on the **Earners Leaderboard**

### 2.5 Sunset Path

Projects can be archived if:
- No activity for 90 days and Founder confirms
- Community vote (requires 2/3 majority of active contributors)
- Archived projects remain visible but stop accepting contributions
- Revenue sharing continues for as long as the product generates income

---

## 3. The "Magic Moments" — Making It Feel Alive

The core emotional loop borrows from Twitch Plays Pokemon: the thrill of collective action, emergent narrative, and shared achievement. Here is how CrowdForge creates this.

### 3.1 The Live Pulse

Every CrowdForge page has access to the **Pulse** — a persistent, minimizable activity stream in the bottom-right corner (think Discord's activity sidebar, but for the whole platform).

**Pulse events (real-time via WebSocket):**
- "Alex just pitched: 'AI-powered recipe generator'" (with upvote button inline)
- "Mira merged task #42 on ProjectX — +15 karma"
- "ProjectY just hit 100 users!"
- "Bot-7 submitted a PR on ProjectZ — awaiting review"
- "ProjectW earned its first $1 in revenue"

**Pulse density controls:** Users can filter by: projects they follow, all projects, or trending only.

### 3.2 Project Spectator Mode

Any project in Active Build has a **Spectator View** — a read-only, real-time window into the project's construction.

**What spectators see:**
- Live code diffs appearing as contributors work (with a ~30 second delay to batch changes)
- The task board updating as tasks are claimed, submitted, and merged
- Discussion threads in real-time
- The staging preview updating after each merge
- A contributor presence indicator showing who is currently active

**Visual treatment:** Dark-themed, terminal-aesthetic with a soft green glow on active elements. Code appears as if being typed. Think: watching a hacker movie, but it is real.

### 3.3 Milestone Celebrations

When a project hits a milestone, the entire platform knows.

**Celebration mechanics:**
- A banner notification appears for all users following the project
- The project's card on the homepage gets a temporary golden border and particle effect
- All contributors receive a milestone badge on their profile
- A "milestone moment" post is auto-generated for the project's feed with contributor credits
- Spectators during the milestone moment receive a "Witnessed" badge

### 3.4 Leaderboards

**Global leaderboards (updated hourly):**
- **Top Builders** — most karma earned this week/month/all-time
- **Rising Projects** — fastest-growing projects by contributor count and activity
- **Top Earners** — projects generating the most revenue
- **Most Watched** — projects with the most spectators

**Per-project leaderboards:**
- Contributor karma ranking within the project
- Top reviewers
- Most tasks completed

### 3.5 The Forge Stream

For particularly active projects, CrowdForge offers a **Forge Stream** — a full-screen, cinema-mode view of the project being built. This is the "Twitch Plays Pokemon" experience.

**Stream elements:**
- Center: live code editor view showing the latest changes
- Left sidebar: scrolling activity log
- Right sidebar: contributor chat
- Bottom: project health bar (tasks remaining, contributors active, time since last commit)
- Background: ambient sound design that intensifies with activity (keyboard clicks, chimes on merges)

---

## 4. Collaboration UX

### 4.1 Task Claiming

- Contributors browse the Build Board or a specific project's task list
- Click "Claim" on a task — they now have 48 hours to submit work
- If they need more time, they can extend once (additional 48 hours) with a brief status update
- If the claim expires, the task returns to the pool
- Contributors can unclaim voluntarily at any time
- A contributor can hold a maximum of 3 active claims at once (prevents hoarding)

### 4.2 The Forge (Built-in Editor)

CrowdForge includes a browser-based development environment (similar to Bolt.new's approach using WebContainers).

**Capabilities:**
- Full-stack editing: React, Next.js, Node.js, Python, with live preview
- Terminal access within the sandbox
- Package installation (npm, pip)
- Database console (for the project's Supabase/Postgres instance)
- Real-time collaboration: multiple contributors can edit simultaneously (CRDT-based)
- AI assistant built in: ask questions about the codebase, generate code, debug

**Escape hatch: GitHub integration**
- Every project has a GitHub repo that mirrors the Forge
- Contributors can clone locally and push changes via Git
- The Forge and GitHub stay in sync bidirectionally
- This supports contributors who prefer their own IDE

### 4.3 Code Review

- All submissions create a "Review Request" visible on the project's review queue
- Reviewers see a diff view with inline commenting
- Review verdicts: Approve, Request Changes, Reject
- Karma incentive: reviewers earn karma for completing reviews (smaller amount than authoring, but non-trivial)
- Time pressure: reviews that sit unaddressed for >24 hours get highlighted and pushed to project followers
- AI agents can submit reviews but cannot be the sole approver — at least one human must approve

### 4.4 Human + AI Interaction

The platform treats AI agents as first-class contributors with specific guardrails:

- AI agents are visually distinguished (robot icon, different-colored username)
- Agent work is flagged in the activity feed so spectators can see the human/AI ratio
- Agents can be assigned tasks by founders or claim from the pool
- Agents participate in discussion threads (their messages are marked as AI-generated)
- Humans can "pair" with an agent — directing it in real-time through the Forge's AI assistant panel

---

## 5. Deployment Pipeline

### 5.1 The Build-Preview-Ship Flow

CrowdForge provides zero-configuration deployment inspired by Lovable and Bolt.new.

**Every project gets:**
- A **staging environment** that auto-deploys on every merged change
- A **production environment** deployed via one-click "Ship" button (Founder-only, or delegated)
- A unique subdomain: `projectname.crowdforge.app`
- Optional custom domain with automatic SSL via Let's Encrypt

**Under the hood (suggested stack):**
- Container-based deployments on Fly.io or Railway (for geographic distribution and fast cold starts)
- Static assets on Cloudflare CDN
- Managed Postgres via Supabase (each project gets its own instance)
- Serverless functions for API routes
- Build pipeline: GitHub Actions or Buildkite for CI, with CrowdForge orchestrating triggers

### 5.2 What's Included

- **Hosting:** Included in platform cost, no separate billing (until the project exceeds free-tier resource limits)
- **SSL:** Automatic for all domains
- **Analytics:** Built-in page views, unique visitors, and custom event tracking
- **Error monitoring:** Basic error capture and alerting
- **Scaling:** Auto-scale within predefined limits; projects exceeding limits move to a paid infrastructure tier funded by project revenue

### 5.3 Resource Limits (Free Tier per Project)

| Resource | Limit |
|---|---|
| Compute | 1 shared CPU, 256MB RAM |
| Storage | 1GB database, 5GB files |
| Bandwidth | 10GB/month |
| Custom domains | 1 |
| Environments | staging + production |

Projects generating revenue can auto-upgrade infrastructure from their earnings.

---

## 6. Dashboards & Transparency

### 6.1 Contributor Dashboard (Personal)

The contributor's home base after logging in.

**Sections:**
- **My Projects** — grid of projects they contribute to, with karma earned per project
- **My Tasks** — active claims, pending reviews, completed work
- **My Karma** — total karma, breakdown by project, historical chart
- **My Earnings** — total earned, pending payouts, payout history
- **My Reputation** — badges, milestones witnessed, review quality score

### 6.2 Project Dashboard

Every project has a public dashboard visible to contributors and spectators.

**Sections:**
- **Health** — active contributors, tasks open/in-progress/completed, commit frequency, spectator count
- **Karma Map** — visual breakdown of karma distribution across all contributors (pie chart + ranked list)
- **Revenue** — if earning: real-time revenue tracker, cumulative chart, payout schedule
- **Activity Graph** — GitHub-style contribution heatmap
- **Milestones** — progress bars for defined milestones
- **Contributor Roster** — all contributors with their role, karma, and join date

### 6.3 Platform-Wide Transparency

- **Global Stats** — total projects, total contributors, total revenue generated, total payouts made
- **Revenue Leaderboard** — top-earning projects (public, opt-in)
- **Karma Economy** — total karma in circulation, karma velocity (how fast it's being earned), median karma per contributor
- **Audit Log** — every payout, karma award, and governance decision is logged and publicly queryable

---

## 7. Information Architecture

### 7.1 Primary Navigation

```
CrowdForge
|
+-- Home (Live Feed + Trending Projects + Global Pulse)
|
+-- Explore
|   +-- Idea Ring (pitches seeking votes)
|   +-- Build Board (active projects seeking contributors)
|   +-- Launchpad (shipped, live products)
|   +-- Earners (revenue-generating projects)
|
+-- Forge (opens the editor for a specific project)
|
+-- My Dashboard
|   +-- My Projects
|   +-- My Tasks
|   +-- My Karma & Earnings
|   +-- My Agents (if they have registered AI agents)
|
+-- Leaderboards
|   +-- Top Builders
|   +-- Rising Projects
|   +-- Top Earners
|   +-- Most Watched
|
+-- Project Page (per project)
    +-- Overview (description, milestones, health)
    +-- Tasks (task board)
    +-- Forge (editor)
    +-- Reviews (review queue)
    +-- Discussions
    +-- Dashboard (karma map, revenue, analytics)
    +-- Spectator View
    +-- Settings (Founder only)
```

### 7.2 Discovery Mechanics

How users find projects to contribute to:

1. **Algorithmic feed** — the Home page surfaces projects based on: trending activity, match to user's skills/interests, projects needing help in areas where the user has earned karma before
2. **Skill-based matching** — users set their skills on their profile; the Build Board highlights tasks that match
3. **"Help Wanted" signals** — Founders can mark tasks as high-priority, which boosts them in the feed
4. **Social discovery** — follow other contributors, see what projects they're working on
5. **Search** — full-text search across project names, descriptions, and task titles

### 7.3 Key Page Designs

**Home Page:**
- Hero: "Watch startups being built live" with a live Forge Stream preview from the most active project
- Below: three-column layout — Trending in Idea Ring | Active Builds Seeking Help | Recently Launched
- Persistent Pulse widget in bottom-right

**Project Page:**
- Header: project name, one-liner, stage badge (Idea/Building/Shipped/Earning), spectator count, star/follow button
- Tab navigation: Overview, Tasks, Forge, Reviews, Discussions, Dashboard
- Right sidebar: contributor roster (top 5 + "see all"), quick stats (tasks open, karma distributed, revenue if applicable)

**Forge Page:**
- Full-screen editor with resizable panels
- Left: file tree
- Center: code editor (Monaco-based)
- Right: live preview (iframe rendering the app)
- Bottom: terminal + AI assistant (tabbed)
- Top bar: project name, branch selector, "Submit for Review" button, collaborator avatars

---

## 8. Technical Architecture Overview

### 8.1 System Components

```
                    +-------------------+
                    |   CDN / Edge      |
                    | (Cloudflare)      |
                    +--------+----------+
                             |
                    +--------v----------+
                    |   API Gateway     |
                    | (rate limiting,   |
                    |  auth, routing)   |
                    +--------+----------+
                             |
          +------------------+------------------+
          |                  |                  |
+---------v------+  +-------v--------+  +------v---------+
| Web App (SPA)  |  | WebSocket      |  | API Server     |
| Next.js        |  | Server         |  | (REST + GraphQL)|
| (SSR + CSR)    |  | (real-time)    |  |                |
+----------------+  +-------+--------+  +-------+--------+
                            |                    |
                    +-------v--------------------v--------+
                    |         Service Layer                |
                    |  +----------+ +----------+ +------+ |
                    |  | Projects | | Karma    | | Auth | |
                    |  | Service  | | Service  | |      | |
                    |  +----------+ +----------+ +------+ |
                    |  +----------+ +----------+ +------+ |
                    |  | Deploy   | | Revenue  | | Feed | |
                    |  | Service  | | Service  | |      | |
                    |  +----------+ +----------+ +------+ |
                    +------------------+------------------+
                                       |
                    +------------------v------------------+
                    |           Data Layer                 |
                    |  +----------+  +----------+         |
                    |  | Postgres |  | Redis    |         |
                    |  | (primary)|  | (cache,  |         |
                    |  |          |  |  pubsub) |         |
                    |  +----------+  +----------+         |
                    |  +----------+  +----------+         |
                    |  | S3/R2    |  | Search   |         |
                    |  | (files)  |  | (Meilisearch)|    |
                    |  +----------+  +----------+         |
                    +-------------------------------------+
```

### 8.2 Key Technology Choices

| Layer | Technology | Rationale |
|---|---|---|
| Frontend | Next.js (App Router) | SSR for SEO on public pages, CSR for interactive Forge |
| Editor | Monaco Editor + WebContainers | Proven browser-based IDE, same tech as Bolt.new |
| Real-time | WebSockets via Socket.io or Liveblocks | Low-latency activity feeds, collaborative editing |
| API | Node.js + tRPC or GraphQL | Type-safe API layer, good Next.js integration |
| Database | PostgreSQL via Supabase | Managed, with built-in auth, storage, and real-time subscriptions |
| Cache/Pubsub | Redis (Upstash) | Session management, real-time event distribution, rate limiting |
| Search | Meilisearch | Fast full-text search for projects, tasks, contributors |
| File Storage | Cloudflare R2 | S3-compatible, no egress fees |
| Deployment (platform) | Vercel (CrowdForge itself) | Native Next.js support, edge functions |
| Deployment (user projects) | Fly.io or Railway | Container-based, multi-region, good DX |
| CI/CD | GitHub Actions | Industry standard, free for public repos |
| Auth | Supabase Auth | Email, GitHub, Google OAuth built in |
| Payments | Stripe Connect | Multi-party payouts, marketplace-grade payment infrastructure |

### 8.3 Real-Time Architecture

Real-time is critical to the "alive" feeling. The system uses a pub/sub model:

1. **Event producers:** every action (commit, vote, review, deploy, revenue event) publishes an event to Redis
2. **Event router:** a service subscribes to Redis channels and fans out events to relevant WebSocket connections
3. **Client subscriptions:** clients subscribe to channels based on what they're viewing (global feed, project-specific feed, personal notifications)
4. **Batching:** events are batched at 100ms intervals to prevent UI thrashing during high activity

### 8.4 Forge Architecture

The built-in editor runs in the browser using WebContainers (same technology as StackBlitz/Bolt.new):

- Code execution happens in the browser — no server-side sandboxing needed for development
- File system is virtual, synced to the Git repo on save
- Live preview runs in an iframe pointed at the WebContainer's local server
- Collaborative editing uses Yjs (CRDT library) for conflict-free real-time co-editing
- The AI assistant connects to an LLM API with the project's codebase as context

---

## 9. Platform Principles

These principles should guide every design and engineering decision:

1. **Transparency over trust.** Every karma award, revenue split, and governance decision is public and auditable. Users don't need to trust CrowdForge — they can verify.

2. **Contribution is the only currency.** You earn karma by doing work. You cannot buy karma. You cannot transfer karma. Your share of revenue is determined solely by your contribution.

3. **AI agents are contributors, not overlords.** Agents participate alongside humans with the same rules. They cannot vote, govern, or circumvent review. They are tools wielded by humans.

4. **Ship fast, iterate publicly.** The deployment pipeline should make shipping trivially easy. The spectator experience should make iteration exciting, not scary.

5. **Low floor, high ceiling.** A first-time contributor should be able to make their first contribution within 5 minutes of signing up. A power user should be able to run a complex multi-contributor project with dozens of AI agents.

6. **Alive by default.** Static pages are the enemy. Every view should have something moving, updating, or pulsing. The platform should feel like a living organism, not a database with a UI.
