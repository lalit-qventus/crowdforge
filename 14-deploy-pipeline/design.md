# CrowdForge: Deployment Pipeline Design

The deployment pipeline is CrowdForge's "write code → instant preview → one-click deploy" infrastructure. Projects deployed on CrowdForge create natural switching costs — contributors don't want to set up their own infra, and accumulated analytics/domains/monitoring make migration painful. The deployment experience must be so frictionless that self-hosting feels like punishment.

---

## 1. Architecture Overview

```
                    ┌─────────────────────────────┐
                    │     crowdforge.app           │
                    │     (Cloudflare DNS + CDN)   │
                    └──────────┬──────────────────┘
                               │
                    ┌──────────▼──────────────────┐
                    │     Deploy Gateway           │
                    │  (routing, SSL termination,  │
                    │   tier enforcement, WAF)     │
                    └──────────┬──────────────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                     │
┌─────────▼────────┐ ┌────────▼─────────┐ ┌────────▼─────────┐
│  Static Sites    │ │  Container Apps  │ │  Serverless Fns  │
│  (Cloudflare R2  │ │  (Fly.io         │ │  (Fly.io         │
│   + Pages)       │ │   Machines)      │ │   Machines,      │
│                  │ │                  │ │   scale-to-zero) │
└──────────────────┘ └────────┬─────────┘ └────────┬─────────┘
                              │                     │
                    ┌─────────▼─────────────────────▼────────┐
                    │           Data Layer (per project)      │
                    │  ┌───────────┐  ┌───────────┐          │
                    │  │ Supabase  │  │ R2 Object │          │
                    │  │ Postgres  │  │ Storage   │          │
                    │  └───────────┘  └───────────┘          │
                    │  ┌───────────┐  ┌───────────┐          │
                    │  │ Upstash   │  │ Supabase  │          │
                    │  │ Redis     │  │ Auth      │          │
                    │  └───────────┘  └───────────┘          │
                    └────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Role | Why This Choice |
|---|---|---|
| **Cloudflare** | DNS, CDN, DDoS protection, SSL termination for custom domains, static asset serving | Zero-egress-fee CDN, global edge network, free SSL, R2 for static hosting |
| **Fly.io Machines** | Container runtime for dynamic apps (Node, Python, Next.js SSR) | Per-request billing (scale-to-zero), multi-region, sub-second cold starts, Firecracker VMs for isolation |
| **Supabase** | Managed Postgres, auth, real-time subscriptions per project | One-click provisioning, row-level security, built-in auth eliminates a whole service for project creators |
| **Upstash Redis** | Session cache, rate limiting, queue for build jobs | Serverless pricing (pay per request), no idle cost for inactive projects |
| **Cloudflare R2** | File uploads, build artifacts, static asset hosting | S3-compatible, zero egress fees, integrates with Cloudflare CDN |

---

## 2. Build Pipeline

### 2.1 Framework Detection

When a project's code is committed (via the Forge or GitHub push), the build system auto-detects the framework by inspecting the repo:

```
Detection Order:
1. crowdforge.toml (explicit config — always wins)
2. next.config.{js,ts,mjs}  →  Next.js
3. vite.config.{js,ts}      →  Vite (React/Vue/Svelte)
4. package.json "scripts.build" exists + no framework markers  →  Generic Node
5. requirements.txt or pyproject.toml  →  Python
6. Dockerfile  →  Custom container
7. Only index.html  →  Static site
```

Each detected framework maps to a **build preset** — a pre-configured build recipe.

### 2.2 Build Presets

| Framework | Install | Build Command | Output | Runtime |
|---|---|---|---|---|
| **Next.js** | `npm ci` | `npm run build` | `.next/` | Fly.io Machine (Node) |
| **Vite (React)** | `npm ci` | `npm run build` | `dist/` | Cloudflare R2 (static) |
| **Vite (SSR)** | `npm ci` | `npm run build` | `dist/` | Fly.io Machine (Node) |
| **Generic Node** | `npm ci` | `npm run build` | varies | Fly.io Machine (Node) |
| **Python (FastAPI/Flask)** | `pip install -r requirements.txt` | — | — | Fly.io Machine (Python) |
| **Static HTML** | — | — | `./` | Cloudflare R2 |
| **Dockerfile** | — | `docker build` | image | Fly.io Machine |

### 2.3 Build Execution

```
Trigger (merge to main or "Ship" click)
    │
    ▼
┌─────────────────────────────────────────────────┐
│  Build Orchestrator (CrowdForge Deploy Service) │
│                                                 │
│  1. Clone repo at commit SHA                    │
│  2. Detect framework (§2.1)                     │
│  3. Pull build preset                           │
│  4. Resolve environment variables               │
│  5. Execute build in isolated container          │
│  6. Upload artifacts                            │
│  7. Route to deployment target                  │
│  8. Health check                                │
│  9. Swap traffic                                │
│  10. Notify project (WebSocket event)           │
└─────────────────────────────────────────────────┘
```

**Build environment:** Builds run in ephemeral Fly.io Machines — a fresh VM spun up per build, destroyed after. This guarantees isolation (Project A's build cannot read Project B's secrets) and reproducibility.

**Build cache:** `node_modules` and pip caches are stored per-project in R2. On subsequent builds, the cache is restored before install, cutting build times by 60-80%.

**Build timeout:** 5 minutes hard limit. If a build exceeds this, it fails. Standard framework builds complete in 15-45 seconds.

### 2.4 `crowdforge.toml` (Optional Override)

Projects that need non-standard configuration can place a `crowdforge.toml` in the repo root:

```toml
[build]
framework = "nextjs"          # override auto-detection
command = "npm run build"     # override build command
output = ".next"              # override output directory
node_version = "20"           # pin runtime version

[env]
NODE_ENV = "production"
NEXT_PUBLIC_API_URL = "$CROWDFORGE_PROJECT_URL/api"

[routes]
# Custom routing rules
"/api/*" = { type = "function" }
"/*"     = { type = "static" }

[resources]
# Request specific tier resources
tier = "growth"
regions = ["iad", "lhr"]      # multi-region (Scale+ only)
```

Projects without this file deploy with zero configuration.

---

## 3. Environments

### 3.1 Staging

Every project in Active Build gets an auto-deploying staging environment.

| Property | Value |
|---|---|
| **URL** | `{project-slug}-staging.crowdforge.app` |
| **Deploy trigger** | Every merged change (automatic) |
| **Database** | Dedicated Supabase instance (seeded with test data) |
| **Isolation** | Separate Fly.io Machine from production |
| **Access** | Public by default; Founder can restrict to contributors-only |
| **Lifecycle** | Created when project enters Active Build, destroyed on project archive |

Staging deploys happen on the **same pipeline as production** — same build presets, same container images, same environment variable resolution. The only difference is the target machine and URL.

**Preview deploys:** For projects on Scale tier and above, every submitted-for-review change also gets a preview URL: `{project-slug}-pr-{number}.crowdforge.app`. Preview environments are destroyed 24 hours after the review is resolved.

### 3.2 Production

| Property | Value |
|---|---|
| **URL** | `{project-slug}.crowdforge.app` + optional custom domain |
| **Deploy trigger** | One-click "Ship" button (Founder or delegated contributor) |
| **Database** | Dedicated Supabase instance (production data) |
| **Isolation** | Dedicated Fly.io Machine with tier-appropriate resources |
| **Health check** | HTTP health check before traffic swap |
| **Rollback** | One-click rollback to any previous deploy (§7) |

**The "Ship" button:** Located on the project dashboard. Shows a diff summary of what changed since the last production deploy. Founder clicks "Ship" → build starts → progress bar streams in real-time → health check passes → traffic swaps → confetti animation + Pulse notification.

**Deploy permissions:** By default, only the Founder can ship to production. The Founder can delegate this to specific contributors via the project settings. Delegation requires the contributor to have >100 karma on the project.

### 3.3 Environment Variables

Projects configure env vars through the CrowdForge dashboard (never committed to the repo).

```
Platform-injected variables (always available):
  CROWDFORGE_PROJECT_ID    → unique project identifier
  CROWDFORGE_PROJECT_URL   → full URL of the current environment
  CROWDFORGE_ENV           → "staging" | "production" | "preview"
  CROWDFORGE_COMMIT_SHA    → the deployed commit
  DATABASE_URL             → connection string for the project's Postgres
  REDIS_URL                → connection string for the project's Redis (if provisioned)
  SUPABASE_URL             → Supabase project URL
  SUPABASE_ANON_KEY        → Supabase public anon key
  SUPABASE_SERVICE_KEY     → Supabase service role key (server-side only)
```

User-defined env vars are scoped per environment (staging vs. production) and encrypted at rest.

---

## 4. Custom Domains

### 4.1 Setup Flow

```
User enters domain in project settings
    │
    ▼
CrowdForge displays DNS instructions:
  "Add a CNAME record pointing to proxy.crowdforge.app"
    │
    ▼
CrowdForge polls DNS (every 30s for 48 hours)
    │
    ▼
DNS verified → Issue SSL cert via Cloudflare for SaaS
    │
    ▼
Certificate provisioned (< 60 seconds via Cloudflare)
    │
    ▼
Domain active — traffic routes to project's Fly.io Machine
```

### 4.2 Implementation

Custom domains use **Cloudflare for SaaS** (not Let's Encrypt directly). Advantages:

- SSL certificates provisioned in seconds, not minutes
- Automatic renewal with zero downtime
- DDoS protection and WAF included
- No certificate storage or rotation logic needed on CrowdForge's side

**DNS verification:** CrowdForge checks for CNAME to `proxy.crowdforge.app`. For apex domains (no CNAME support), users add a Cloudflare-provided TXT record and CrowdForge configures an A record pointing to the edge proxy.

**Domain limits by tier:**

| Tier | Custom Domains |
|---|---|
| Starter | 0 (subdomain only) |
| Growth | 1 |
| Scale | 5 |
| Enterprise | Unlimited |

---

## 5. Resource Management & Tier Enforcement

### 5.1 Tier Definitions

| Resource | Starter ($0) | Growth ($15/mo) | Scale ($50/mo) | Enterprise ($200/mo) |
|---|---|---|---|---|
| **CPU** | 1 shared vCPU | 1 dedicated vCPU | 2 dedicated vCPU, auto-scale to 4 | 4+ dedicated, auto-scale |
| **RAM** | 256 MB | 512 MB | 1 GB, auto-scale to 2 GB | 4 GB+, auto-scale |
| **Storage (DB)** | 500 MB | 5 GB | 25 GB | 100 GB+ |
| **Storage (files)** | 500 MB | 5 GB | 25 GB | 100 GB+ |
| **Bandwidth** | 10 GB/mo | 100 GB/mo | 500 GB/mo | 2 TB/mo |
| **Custom domains** | 0 | 1 | 5 | Unlimited |
| **Preview deploys** | No | No | Yes | Yes |
| **Regions** | 1 (auto-selected) | 1 (chooseable) | Up to 3 | Up to 6 |
| **Uptime SLA** | Best-effort | 99.5% | 99.9% | 99.95% |
| **Build concurrency** | 1 | 2 | 5 | 10 |
| **Deploy history** | 10 deploys | 50 deploys | 200 deploys | Unlimited |
| **Monitoring** | Error capture | + alerting | + APM traces | + dedicated Grafana |
| **Analytics** | Page views | + uniques, referrers | + custom events, funnels | + raw data export |
| **Support** | Community | Email (48h) | Email (24h) + chat | Dedicated + Slack |

### 5.2 Enforcement Mechanisms

**Compute:** Fly.io Machines are configured with hard CPU and memory limits matching the tier. Exceeding memory triggers OOM kill — the machine restarts automatically. Sustained CPU saturation triggers a dashboard warning suggesting tier upgrade.

**Bandwidth:** Cloudflare tracks bytes served per project subdomain. At 80% of monthly limit, the Founder receives a warning. At 100%, traffic continues but the project enters a 72-hour grace period with a banner prompting upgrade. After grace period: traffic is throttled (not killed — killing a live product is hostile).

**Storage:** Database size is checked daily. At 90% of limit, writes are still allowed but the Founder is warned. At 100%, INSERT/UPDATE operations return a 507 error until the project upgrades or frees space.

**Build concurrency:** Builds exceeding the tier's concurrency limit are queued, not rejected. Queue position is visible in the deploy dashboard.

### 5.3 Auto-Upgrade from Revenue

Projects generating revenue can opt into **auto-upgrade**: when a project's monthly revenue exceeds a threshold, the infrastructure tier upgrades automatically, paid from project earnings (deducted before the platform cut).

```
Revenue thresholds for auto-upgrade:
  $0/mo     → Starter (free)
  $50/mo    → Growth ($15/mo auto-deducted)
  $200/mo   → Scale ($50/mo auto-deducted)
  $1,000/mo → Enterprise ($200/mo auto-deducted)
```

The Founder can disable auto-upgrade and manage tier manually.

---

## 6. Monitoring & Analytics

### 6.1 Error Capture

Every deployed project gets built-in error monitoring at zero configuration cost.

**Client-side:** A lightweight error boundary script (< 2 KB gzipped) is auto-injected into HTML responses. It captures:
- Unhandled exceptions with stack traces
- Unhandled promise rejections
- Console errors
- Network request failures (4xx/5xx)

**Server-side:** Structured logging from the container runtime captures:
- Uncaught exceptions
- Process crashes and restarts
- OOM events
- Slow responses (> 5 seconds)

Errors are stored for 30 days (Starter/Growth) or 90 days (Scale/Enterprise).

**Error dashboard:** Project contributors see errors grouped by type, with occurrence count, first/last seen timestamps, and affected deploy version. Errors auto-resolve when the deploy that introduced them is superseded.

### 6.2 Uptime Monitoring

CrowdForge runs health checks against every production deployment.

| Check | Frequency | Behavior on Failure |
|---|---|---|
| HTTP GET `/` | 30 seconds | 3 consecutive failures → machine restart |
| TCP connect | 10 seconds | 5 consecutive failures → machine restart + alert |
| Process alive | 5 seconds | Immediate restart on crash |

**Status page:** Each project gets a public status endpoint at `{project-slug}.crowdforge.app/status` returning uptime percentage and incident history (past 90 days). Projects on Scale+ can customize the status page with their branding.

### 6.3 Performance Metrics

Available on Growth tier and above:

- **Response time** — p50, p95, p99 per endpoint
- **Throughput** — requests per second
- **Error rate** — percentage of 4xx and 5xx responses
- **Cold start latency** — time from scale-to-zero wake to first response
- **Build duration** — trend over last 50 builds

Enterprise tier adds full APM traces (distributed tracing via OpenTelemetry, visualized in a dedicated Grafana instance).

### 6.4 Built-in Analytics

Every deployed project includes analytics with zero setup — no tracking scripts to add, no third-party accounts to create.

**Starter tier (page views):**
- Total page views per day/week/month
- Top pages by view count

**Growth tier (+ uniques, referrers):**
- Unique visitors (fingerprint-based, no cookies — privacy-respecting)
- Referrer breakdown (where traffic comes from)
- Geographic distribution (country-level)
- Device and browser breakdown

**Scale tier (+ custom events, funnels):**
- Custom event tracking via `crowdforge.track("event_name", { properties })`
- Funnel analysis (define multi-step funnels, see conversion rates)
- Retention cohorts (weekly/monthly)
- Real-time visitor count

**Enterprise tier (+ raw data export):**
- All of the above
- CSV/JSON export of raw analytics data
- Webhook on analytics events (for custom pipelines)
- Data retention: unlimited (lower tiers retain 12 months)

**Implementation:** Analytics data is collected at the Cloudflare edge (using Cloudflare Analytics Engine). Page views are captured from HTTP request logs — no client-side JavaScript needed for basic metrics. Custom events use a lightweight client SDK (`crowdforge.track()`) that posts to an edge function.

**Privacy:** No cookies. No cross-site tracking. No PII stored. Unique visitors are identified by a daily-rotating hash of IP + User-Agent (cannot be reversed to identify individuals). GDPR-compliant by design.

---

## 7. Rollback

### 7.1 Deploy History

Every successful deploy is recorded as an immutable **deploy snapshot**:

```
Deploy Snapshot:
  id:           deploy_abc123
  project:      petmatch
  environment:  production
  commit_sha:   a1b2c3d
  commit_msg:   "Add matching algorithm v2"
  built_at:     2025-03-15T10:30:00Z
  deployed_at:  2025-03-15T10:30:45Z
  deployed_by:  @sarah (Founder)
  build_duration: 32s
  artifact_ref: r2://crowdforge-builds/petmatch/deploy_abc123.tar.gz
  status:       active | superseded | rolled_back
  machine_id:   fly_machine_xyz
```

Deploy history is kept per tier (10 for Starter through unlimited for Enterprise). Artifacts are stored in R2 and are immutable — a rollback re-deploys the stored artifact, it does not rebuild.

### 7.2 Rollback Flow

```
Founder opens Deploy History in project dashboard
    │
    ▼
Sees chronological list of deploys with:
  - Commit message + SHA
  - Who deployed, when
  - Duration it was active
  - Error rate during that deploy
    │
    ▼
Clicks "Rollback" on a previous deploy
    │
    ▼
Confirmation modal:
  "Roll back production to deploy_xyz789 (commit a1b2c3d)?
   This will replace the current version immediately."
    │
    ▼
CrowdForge pulls the stored artifact from R2
    │
    ▼
Deploys artifact to a new Fly.io Machine
    │
    ▼
Health check passes → traffic swaps
    │
    ▼
Old machine is drained (30s) then destroyed
    │
    ▼
Pulse notification: "PetMatch rolled back to deploy_xyz789"
```

**Rollback speed:** Because rollbacks deploy pre-built artifacts (no rebuild), they complete in under 10 seconds.

**Database rollbacks are NOT included.** Rolling back application code does not roll back database state. If a deploy included a destructive migration, the Founder must handle data recovery separately. The deploy confirmation modal warns if the deploy being rolled back includes migrations.

### 7.3 Automatic Rollback

Projects on Scale+ can enable **auto-rollback**: if the error rate exceeds a configurable threshold (default: 10x the previous deploy's error rate) within the first 5 minutes after deploy, the system automatically rolls back and alerts the Founder.

---

## 8. Deploy Speed Budget

Target: standard project deploys complete in under 60 seconds from trigger to live traffic.

| Phase | Budget | How |
|---|---|---|
| Clone repo | 2s | Shallow clone at commit SHA from CrowdForge's Git mirror |
| Restore cache | 3s | R2 cache pull (node_modules, pip cache) — same region |
| Install deps | 10s | Cached: incremental install. Cold: full install (may exceed) |
| Build | 15s | Framework-optimized presets, parallelized where possible |
| Upload artifact | 3s | Compressed tar to R2 (same region as build machine) |
| Deploy to Fly.io | 5s | Fly.io Machine start from pre-built image |
| Health check | 5s | HTTP GET with 3 retries at 1s intervals |
| Traffic swap | 2s | Cloudflare DNS/routing update |
| **Total** | **45s** | 15s buffer to stay under 60s |

**Cold builds** (first deploy, no cache) may take 90-120 seconds. Subsequent deploys benefit from aggressive caching and complete well within the 60s target.

---

## 9. Project Isolation

Every project runs in complete isolation from every other project. A traffic spike on Project A cannot affect Project B.

### 9.1 Isolation Boundaries

| Layer | Isolation Method |
|---|---|
| **Compute** | Each project runs in its own Fly.io Machine (Firecracker microVM) — hardware-level isolation |
| **Network** | Projects cannot communicate with each other. Each Machine gets a unique private IP. No shared network namespace |
| **Database** | Each project gets a dedicated Supabase project (separate Postgres instance, separate connection pool) |
| **Storage** | R2 objects are namespaced per project with IAM policies preventing cross-project access |
| **Secrets** | Env vars are encrypted per-project with unique keys. Build environments have no access to other projects' secrets |
| **DNS** | Each subdomain resolves to the project's specific Machine. No shared origin server |
| **Build** | Builds run in ephemeral, single-use VMs. No shared filesystem between builds |

### 9.2 Noisy Neighbor Prevention

- **CPU:** Starter tier uses shared CPU with cgroup limits. Growth+ gets dedicated cores — no contention possible.
- **Bandwidth:** Cloudflare rate-limits per subdomain. A viral project on Starter hits its 10GB cap; Cloudflare throttles that subdomain only.
- **Database:** Supabase projects are fully separate. Connection pool exhaustion on one project has zero effect on others.

---

## 10. Code Export & Portability

CrowdForge must never trap projects. Natural switching costs (analytics history, contributor network, payment infrastructure, domain config) are the moat — not code captivity.

### 10.1 What's Exportable

| Asset | Export Method |
|---|---|
| **Source code** | Git clone (always available — the repo is the source of truth) |
| **Database** | `pg_dump` via Supabase dashboard, or CrowdForge "Export Data" button (produces SQL dump) |
| **File storage** | Bulk download via dashboard or S3-compatible API |
| **Environment variables** | Export as `.env` file from project settings |
| **Analytics data** | CSV export (Enterprise), API export (Scale+) |
| **Deploy history** | Not exported (build artifacts are platform-specific) |

### 10.2 What's NOT Portable (Natural Moat)

- Contributor network and karma history
- Revenue sharing infrastructure and payout history
- Governance structure and permissions
- Project activity feed and spectator engagement
- Accumulated reputation and trust relationships
- Integrated monitoring/alerting configuration

This is the Shopify moat — the code is yours, but the business infrastructure around it is deeply integrated. Migration is possible but painful enough that it's rarely worth it for a project that's working.

---

## 11. Internal Service Design

### 11.1 Deploy Service API

The Deploy Service is the orchestrator. It exposes an internal API consumed by the CrowdForge web app and the Forge editor.

```
POST   /deploys                    → trigger a new deploy
GET    /deploys/:id                → get deploy status + logs
GET    /deploys/:id/logs/stream    → SSE stream of build logs
POST   /deploys/:id/rollback       → rollback to this deploy
GET    /projects/:id/deploys       → list deploy history
GET    /projects/:id/environments  → list environments (staging, production, previews)
POST   /projects/:id/domains       → add custom domain
DELETE /projects/:id/domains/:domain → remove custom domain
GET    /projects/:id/domains/:domain/status → DNS verification status
GET    /projects/:id/resources     → current resource usage vs. tier limits
POST   /projects/:id/tier          → upgrade/downgrade tier
```

### 11.2 Event Flow

Deploys emit events consumed by the rest of the CrowdForge platform:

```
deploy.started     → Pulse feed, project dashboard (progress bar appears)
deploy.building    → Build log streaming, Forge editor status
deploy.succeeded   → Pulse feed, confetti, project dashboard update
deploy.failed      → Error notification to Founder + deployer, error log link
deploy.rolledback  → Pulse feed, project dashboard, alert to contributors
domain.verified    → Project settings update, Pulse notification
domain.ssl_issued  → Domain marked as active
resources.warning  → Founder notification (approaching tier limit)
resources.exceeded → Grace period initiated, upgrade prompt
```

### 11.3 Data Model

```
projects
  id              UUID
  slug            VARCHAR UNIQUE     -- used in subdomain
  tier            ENUM (starter, growth, scale, enterprise)
  auto_upgrade    BOOLEAN DEFAULT true

deploys
  id              UUID
  project_id      FK → projects
  environment     ENUM (staging, production, preview)
  commit_sha      VARCHAR(40)
  commit_message  TEXT
  deployed_by     FK → users
  artifact_url    VARCHAR            -- R2 URL
  status          ENUM (building, succeeded, failed, active, superseded, rolled_back)
  build_duration  INTERVAL
  started_at      TIMESTAMPTZ
  completed_at    TIMESTAMPTZ
  error_log       TEXT               -- populated on failure

domains
  id              UUID
  project_id      FK → projects
  domain          VARCHAR UNIQUE
  dns_verified    BOOLEAN DEFAULT false
  ssl_provisioned BOOLEAN DEFAULT false
  cloudflare_id   VARCHAR            -- Cloudflare for SaaS custom hostname ID
  created_at      TIMESTAMPTZ
  verified_at     TIMESTAMPTZ

resource_usage
  id              UUID
  project_id      FK → projects
  period          DATE               -- monthly bucket
  bandwidth_bytes BIGINT
  storage_bytes   BIGINT
  build_minutes   INTEGER
  updated_at      TIMESTAMPTZ
```

---

## 12. Failure Modes

| Failure | Detection | Response |
|---|---|---|
| Build fails | Non-zero exit code | Deploy marked `failed`, error log stored, Founder notified, staging/production unchanged |
| Health check fails post-deploy | 3 consecutive failed checks | Traffic NOT swapped, old Machine kept running, deploy marked `failed` |
| Machine crashes in production | Fly.io health monitoring (5s interval) | Automatic restart from same image. If 3 crashes in 5 minutes → auto-rollback (Scale+) or alert (lower tiers) |
| Supabase outage | Connection pool exhaustion / timeout | Circuit breaker returns 503 with "Database temporarily unavailable". Retries with exponential backoff |
| Cloudflare outage | External uptime monitor (Checkly) | CrowdForge status page updated. Fly.io direct IPs available as emergency bypass (Enterprise only) |
| Build queue backup | Queue depth > 50 | Alert to CrowdForge ops. Spin up additional build machines. Priority queue for paid tiers |
| R2 storage failure | Artifact upload failure | Retry 3x with backoff. On persistent failure, fall back to streaming artifact directly to Fly.io Machine |
| DNS verification stuck | 48 hours without successful verification | Notify user, suggest DNS troubleshooting guide. Do not auto-delete the domain config |

---

## 13. Security

### 13.1 Build Security

- Builds run in ephemeral VMs with no network access to CrowdForge internals
- Build containers have no access to other projects' data or secrets
- Dependencies are installed from public registries only (npm, PyPI) — no private registry support in Starter/Growth
- Build output is scanned for accidentally committed secrets (env vars, API keys) using a pattern-matching pass
- `crowdforge.toml` is validated before execution — no arbitrary command injection via config

### 13.2 Runtime Security

- Fly.io Machines run in Firecracker microVMs — hardware-level isolation
- Outbound network access from Machines is unrestricted (projects may call external APIs)
- Inbound traffic passes through Cloudflare WAF (OWASP Core Rule Set)
- DDoS protection included via Cloudflare (all tiers)
- Rate limiting at the edge: 1000 req/s per subdomain (Starter), scaling with tier

### 13.3 Secrets Management

- Environment variables encrypted at rest with per-project AES-256 keys
- Keys stored in a separate secrets manager (not in the application database)
- Secrets injected into build/runtime environments via secure environment variable passing (never written to disk)
- Audit log of all secret access (who read/wrote which secret, when)

---

## 14. Implementation Sequence

### Phase 1: Static Site Deploys (Week 1-2)

Ship the simplest possible deploy path: static HTML/CSS/JS sites deployed to Cloudflare R2.

- Framework detection for static sites
- Build pipeline (clone → detect → upload to R2)
- Subdomain routing (`{slug}.crowdforge.app`)
- Auto-deploy on merge to staging
- "Ship" button for production
- Deploy history (last 10)

**Why start here:** Validates the full deploy flow end-to-end with the lowest infrastructure complexity. Many early CrowdForge projects will be landing pages and simple SPAs.

### Phase 2: Container Deploys (Week 3-4)

Add dynamic application support via Fly.io Machines.

- Build presets for Next.js, Vite SSR, Node, Python
- Fly.io Machine provisioning per project
- Build caching in R2
- Environment variable management
- Health checks and traffic swapping
- Rollback (artifact-based)

### Phase 3: Data Layer (Week 5-6)

Provision per-project databases and integrate storage.

- Supabase project auto-provisioning on project creation
- `DATABASE_URL` injection into builds/runtime
- R2 file storage per project with SDK
- Redis provisioning (Upstash) for caching-heavy projects

### Phase 4: Custom Domains & SSL (Week 7)

- Cloudflare for SaaS integration
- DNS verification flow
- SSL auto-provisioning
- Apex domain support

### Phase 5: Resource Management (Week 8)

- Tier enforcement (CPU, RAM, storage, bandwidth)
- Usage tracking and warnings
- Grace periods for limit exceedance
- Auto-upgrade from revenue

### Phase 6: Monitoring & Analytics (Week 9-10)

- Error capture (client + server)
- Uptime monitoring and auto-restart
- Built-in analytics (Cloudflare Analytics Engine)
- Performance metrics dashboard
- Custom event tracking SDK

### Phase 7: Advanced Features (Week 11-12)

- Preview deploys per PR
- Auto-rollback on error spike
- Multi-region deployment
- Private registry support (Enterprise)
- APM traces (Enterprise)

---

## 15. Unit Economics

| Tier | Revenue | Infra Cost (est.) | Gross Margin |
|---|---|---|---|
| Starter | $0 | $2-4/mo (shared resources, scale-to-zero) | -$2-4 (subsidized) |
| Growth | $15/mo | $5-8/mo | 47-67% |
| Scale | $50/mo | $15-25/mo | 50-70% |
| Enterprise | $200/mo | $50-80/mo | 60-75% |

**Break-even:** Platform needs ~30% of projects on Growth+ to cover Starter tier subsidies. At 1,000 total projects with 300 on Growth ($15) and 50 on Scale ($50), monthly infra revenue = $7,000 against estimated infra cost of ~$4,500.

**Scale-to-zero is critical for economics:** Inactive Starter projects (no traffic) cost near-zero because Fly.io Machines stop when idle and Supabase pauses unused databases. The $2-4/mo estimate is for projects with light but active traffic.
