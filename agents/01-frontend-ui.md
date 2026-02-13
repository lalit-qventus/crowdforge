# Agent: Frontend & UI

## Mission
Build CrowdForge's entire frontend — from landing page to Forge editor to dashboards. The platform should feel like an improv stage that happens to produce real companies. Alive, pulsing, dynamic. Dark terminal aesthetic with bioluminescent accents. Never corporate, never static.

## Design Philosophy
- "Yes, and..." improv energy — the platform feels like collective creation in motion
- Dark theme, terminal-noir with green/cyan glows
- Every page has something moving, updating, or pulsing ("alive by default")
- The Forge Stream (cinema-mode spectator view) is the signature experience — like Twitch for building startups
- Git is the underlying metaphor: contributions are PRs, acceptances are merges

## Key Pages to Build
1. **Landing page** — exists at `index.html`, needs improv-themed redesign (current tagline "Watch strangers build startups together" is rejected — needs edgier positioning)
2. **Home/Feed** — Reddit-like live activity feed with global pulse
3. **Idea Ring** — pitch cards with 72hr voting, real-time vote animations
4. **Project Workspace** — GitHub-like task board, PR review, discussions
5. **Forge Editor** — Monaco + WebContainers, live preview, AI assistant, real-time co-editing
6. **Forge Stream** — full-screen cinema-mode spectator view
7. **Contributor Profile** — karma tiers, badges, earnings, contribution history
8. **Dashboards** — personal (my karma, earnings) + project (health, karma map, revenue)

## Tech Stack (from architecture doc)
- Next.js (App Router) for SSR + CSR
- Monaco Editor + WebContainers for Forge
- WebSockets (Socket.io or Liveblocks) for real-time
- Supabase Auth for authentication
- Tailwind or CSS modules for styling

## Reference Docs
- `06-architecture/design.md` — full UX flows, information architecture, page designs
- `10-value-pricing/analysis.md` — karma tier UI (6 tiers with visual hierarchy)
- `11-branding-competitors/analysis.md` — positioning, aesthetic direction
- `01-platform-vision/vision.md` — overall vision and principles

## Constraints
- No generic AI aesthetics (no purple gradients, no Inter font, no cookie-cutter layouts)
- Mobile-responsive but desktop-first (builders work on desktop)
- Accessibility matters — WCAG AA minimum
- Performance: first contentful paint < 1.5s

## You Are Encouraged To
- Spawn sub-agents for individual pages or components
- Create a design system/component library first, then build pages on top
- Research improv theater aesthetics for visual inspiration
