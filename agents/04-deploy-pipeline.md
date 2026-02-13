# Agent: Deployment Pipeline

## Mission
Build CrowdForge's zero-config deployment infrastructure — the Lovable-style "write code → instant preview → one-click deploy" pipeline. This is a core moat: projects deployed on CrowdForge create switching costs. The deployment experience must be frictionless enough that nobody wants to set up their own infra.

## What to Build
1. **Staging environments** — auto-deploy on every merged contribution. Every project gets a staging URL (`projectname-staging.crowdforge.app`)
2. **Production deploy** — one-click "Ship" button (founder-only or delegated). Deploys to `projectname.crowdforge.app`
3. **Custom domains** — point any domain at CrowdForge with automatic SSL via Let's Encrypt
4. **Build pipeline** — detect framework (React, Next.js, Node, Python), install deps, build, deploy
5. **Resource management** — enforce per-project limits (CPU, RAM, storage, bandwidth by tier)
6. **Monitoring** — basic error capture, uptime monitoring, performance metrics
7. **Analytics** — built-in page views, unique visitors, custom events (no external analytics needed)
8. **Rollback** — one-click rollback to any previous deploy

## Infra Tiers
| Tier | Resources | Cost |
|---|---|---|
| Starter (free) | Shared CPU, 256MB RAM, 1GB storage, 10GB bandwidth | $0 |
| Growth | Dedicated, 10GB storage, 100GB bandwidth, custom domain | $15/mo |
| Scale | Auto-scaling, 50GB storage, 500GB bandwidth, staging envs | $50/mo |
| Enterprise | Dedicated infra, SLA, priority support | $200/mo |

## Suggested Tech Stack
- Fly.io or Railway for container-based deployments
- Cloudflare CDN for static assets
- Supabase for managed Postgres per project
- GitHub Actions or Buildkite for CI
- Let's Encrypt for SSL

## Reference Docs
- `../docs/architecture/design.md` — deployment pipeline section, tech stack choices
- `../docs/business-model/design.md` — infrastructure pricing and unit economics
- `../docs/moat-defensibility/design.md` — deployment lock-in as moat
- `../docs/moat-defensibility/lovable-analysis.md` — Lovable's deployment model

## Constraints
- Zero-config for standard frameworks (React, Next.js, Node, Python)
- Deploy must complete in under 60 seconds for standard projects
- Projects must be isolated — one project's traffic spike cannot affect another
- Code export must always be possible (no artificial lock-in — the natural switching costs are enough)
