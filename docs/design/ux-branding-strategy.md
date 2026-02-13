# CrowdForge UX & Branding Strategy

---

## Part 1: Landing Page Design

### The Job of the Landing Page

The landing page has exactly one job: make a visitor think "I need to see what's happening in there." It does not explain how karma works, how revenue splits, or what a contribution looks like mechanically. Those live deeper in the funnel. The landing page sells a feeling -- the feeling that something alive is happening right now and you're missing it.

Every reference point confirms this. Lovable's landing page says "Build something" with an input field -- not "AI-assisted React component generation with Supabase backend." Discord says "Group chat that's all fun & games" -- not "WebRTC-based voice channels with role-based permissions." The abstraction layer between what the product IS and what the landing page SAYS is vast, deliberate, and correct.

### Hero Section

**Headline:** "Finish each other's startups."

This works because it is specific enough to understand (startups get built), weird enough to stop scrolling (finish EACH OTHER'S?), and warm enough to feel inviting (not "leverage collaborative synergies"). The current implementation gets this right.

**Sub-headline:** One sentence that unpacks the headline into a concrete image. The current version -- "Someone shares an idea. Others add to it -- design, code, marketing. It gets built, deployed, and when it earns money, everyone shares the revenue." -- is strong but slightly long. A tighter version:

> Someone shares an idea. Strangers add to it. It gets built and shipped -- and when it makes money, everyone who helped shares the revenue.

**CTA pair:**
- Primary: "Join the waitlist" (pre-launch) / "Start building" (post-launch)
- Secondary: "Watch it happen" -- scrolls to the live activity section

**Presence indicator:** The blinking dot with "247 people creating right now" is the single most important element below the CTA. It answers the unspoken question: "Is anyone actually using this?" The number should feel real (not round hundreds), should fluctuate slightly, and should use the word "creating" not "online" or "active." Creating implies output. Active implies idle browser tabs.

### What Best-in-Class Landing Pages Teach Us

**Lovable** -- The input field as hero. Lovable's landing page puts a text input ("Describe your app idea...") front and center. The lesson: reduce the distance between landing and doing. For CrowdForge post-launch, consider replacing the waitlist form with a "Browse live projects" or "Watch someone build right now" action that puts the visitor INTO the experience immediately.

**Linear** -- Density as credibility. Linear's page is information-dense in a way that signals competence. Lots of small, precise typography. Grid-based layouts. The lesson: monospace labels, tight spacing, and data-rich cards signal "this is real and serious" without saying it. CrowdForge's current mono-label style (scene stats, presence counts) borrows this well.

**Vercel** -- Trust through specificity. Vercel names real customers (Runway, Zapier) and uses precise technical language. The lesson for CrowdForge: once real projects exist, name them. "NomadDesk shipped last Tuesday" is more credible than "projects ship fast." The current Scene cards (NomadDesk, Yokai Drift, Mise en Place) do this with fictional examples -- replace with real ones as soon as possible.

**Notion** -- Emotional headline, structural proof. "One workspace. Zero busywork." is emotional. Then the page proves it with specific feature cards. The lesson: the hero sells the feeling; the body proves the mechanism. CrowdForge's "Yes, And..." chain section does this perfectly -- it SHOWS the mechanism through narrative rather than explaining it through bullet points.

**Figma** -- Community as product. Figma's landing page features a carousel of community-created work. The designers ARE the marketing. The lesson for CrowdForge: the projects built on the platform are the best possible social proof. Post-launch, the Scene cards section should pull from real, live data -- not static examples.

**Arc Browser** -- User-centric framing. "The browser that puts you first." No features. No specs. Just a relationship statement. The lesson: CrowdForge's landing page should feel like it's talking TO the visitor, not ABOUT the platform.

**Discord** -- Plain language at every level. "Group chat that's all fun & games." "Stream like you're in the same room." "Hop in when you're free, no need to call." Discord never once mentions WebRTC, codecs, or server architecture on the homepage. The lesson is the most important one for CrowdForge: the internal vocabulary is powerful, but the landing page speaks human.

### Recommended Landing Page Structure

**Section 1 -- Hero.** Headline, sub-headline, dual CTA, presence indicator. Dark background, centered layout, breathing room. The hero should feel like a theater lobby -- you can hear the show happening on the other side of the doors.

**Section 2 -- The Chain.** The "Yes, And..." narrative. An idea evolves through stranger contributions into a shipped product. This is the single best storytelling device on the page. It shows the mechanism without explaining it. The current implementation (sara -> jin -> mira -> alex -> eve -> "None of them knew each other this morning") is the strongest section on the page and should not be significantly altered.

**Section 3 -- Live Activity Window.** A glimpse of projects being built right now (or recently). Not a dashboard. Not a feature list. A window into something alive. The current Scene cards section serves this role. Post-launch, this should pull real data: actual project names, actual contributor counts, actual status. The Live Pulse widget in the corner reinforces the "alive" feeling.

**Section 4 -- The Promise.** One statement about the economic model. "100% of revenue goes to the people who built it. We just keep the lights on." Three stats: 0% platform take, 100% to creators, community-funded server costs. This section should be brief and definitive -- not a sales pitch, a fact.

**Section 5 -- Waitlist / CTA.** "This is just getting started." Email capture. The current implementation is clean. Post-launch, replace with "Start building" or "Watch a project" -- an action that puts them in the product, not on a list.

### What the Landing Page Must NOT Do

- Explain the karma system or any scoring mechanics
- Show pricing tiers or subscription plans
- Use the words "Riff," "Scene," "Ensemble," "Stage," or "Forge Stream"
- Lead with revenue or earnings
- Show project management UI (Gantt charts, sprint boards, ticket lists)
- Say "AI-powered," "AI-driven," or feature AI as the hero
- Use stock photography or generic SaaS illustration
- List features in a grid

### Mobile Considerations

The hero must work on a 375px screen. The Chain section should stack vertically with stagger animations preserved. The Scene cards should collapse to a 2-column grid on tablet and 1-column on small phones. The Live Pulse widget should remain but be collapsible. The waitlist form should stack vertically. The presence indicator should remain visible -- it is more important on mobile where the user cannot see the full page context.

---

## Part 2: Brand Identity

### Visual Direction

CrowdForge should look and feel like the backstage of a theater company at 11pm -- lights are on, people are making things, there is energy and warmth but no corporate polish. The visual system should communicate: this is a place where real creative work happens, done by real people, and you can see it happening.

**What CrowdForge looks like:**
- A jazz club at midnight (dark, warm, alive with activity)
- The backstage of a theater (creative chaos, camaraderie, work-in-progress)
- A campfire (people gathered around something they are building together)
- A recording studio control room (technical capability in service of creative output)

**What CrowdForge does NOT look like:**
- A SaaS dashboard (clean, clinical, productivity-optimized)
- A startup pitch deck (aspirational photography, gradient backgrounds, white space)
- A hackathon platform (neon colors, countdown timers, leaderboards)
- A freelance marketplace (profiles, ratings, hourly rates)
- A DAO governance interface (proposal cards, voting mechanisms, treasury dashboards)
- A code repository (file trees, diff views, branch diagrams)

### Color Palette

The current palette is anchored in deep, warm blacks with vivid accent colors. This is correct. The dark palette creates the "theater" feeling -- dark backgrounds make accent colors feel like stage lights.

**Backgrounds:**
- Deep Black (#0d0907) -- primary background, the darkness of the theater
- Surface (#161110) -- card and panel backgrounds, slightly lifted
- Elevated (#1e1816) -- secondary surfaces, inputs, nested elements

**Accent Colors (the "stage lights"):**
- Cyan (#00ffd5) -- primary accent, live states, human contributor identity
- Green (#39ff14) -- success, shipped states, growth
- Coral (#ff6b6b) -- secondary accent, urgency, creative energy
- Violet (#a78bfa) -- AI agent identity, ideas, inception
- Amber (#f5a623) -- warnings, karma, highlights, brand warmth

**Text:**
- Primary (#f0e6d3) -- warm white, headlines and body
- Secondary (#9a8e80) -- descriptions, supporting text
- Muted (#4d4239) -- timestamps, labels, disabled states

**Usage principles:**
- Backgrounds are always dark. No white backgrounds, no light mode (at least not at launch -- the theater metaphor breaks under fluorescent lighting).
- Accent colors are used sparingly, like spotlights. When everything glows, nothing does.
- Each accent color has a semantic role. Cyan = live/human. Violet = AI. Coral = energy/urgency. Green = shipped/success. Amber = karma/warmth. Mixing these semantics dilutes their meaning.
- Glow effects (box-shadow with accent colors at low opacity) create the "stage light" ambiance. Use on hover states, live indicators, and interactive elements. Never on static text or decorative elements.

### Typography

Three font families, each with a clear role:

**Bricolage Grotesque (Display):** Headlines, hero text, section titles. Weight 700-800. Tight letter-spacing (-0.03em to -0.04em). This font has personality -- it is not a neutral sans-serif. It has quirks and character that signal "this is not another SaaS product."

**JetBrains Mono (Monospace):** Code, labels, timestamps, terminal-style UI, stat counters, presence indicators. Weight 300-600. Wide letter-spacing (0.04em-0.15em) for labels. This font signals technical credibility and connects to the builder audience.

**Instrument Sans (Body):** Paragraphs, descriptions, UI text, longer-form content. Weight 400-700. Standard spacing, comfortable line-height (1.6-1.8). Readable and unobtrusive.

**Typography rules:**
- Never use Inter, Helvetica, or system fonts in marketing materials. These are the fonts of "every other SaaS product."
- Monospace labels in uppercase with wide letter-spacing are a signature element. They create the terminal/backstage aesthetic.
- Display type should be large and high-contrast. Tight letter-spacing at large sizes creates density and confidence.

### Illustration & Imagery Style

CrowdForge should avoid illustration almost entirely. The product IS the visual. Live activity feeds, code snippets, project cards, contributor avatars, karma bars -- these are more compelling than any illustration could be.

When imagery is needed:

- **Data as art.** Contribution timelines, karma distribution charts, activity heatmaps -- present real data beautifully. The data itself is the illustration.
- **Terminal aesthetics.** Monospace text, blinking cursors, streaming log lines. The "watching code being written" visual is inherently compelling to the target audience.
- **Avatar mosaics.** Grids of contributor initials/avatars on a project, showing the ensemble. People + diversity of contributors is the visual proof.
- **No stock photography.** No photos of people at laptops, whiteboards, or standing in front of screens.
- **No flat corporate illustration.** No Notion-style minimal line drawings. No abstract geometric shapes. No "diverse team of illustrated characters."
- **No AI-generated art.** The brand is human-first. Using AI imagery on a platform about human creativity is contradictory.

### Motion & Animation Philosophy

Everything on stage is alive. Static equals dead. But animation serves meaning, not decoration.

**Ambient animations (slow, subtle, organic):**
- Background grid drift: slow parallax movement, 8-10s cycle
- Glow pulse on live indicators: 2-2.5s cycle, breathing rhythm
- Presence counter fluctuation: gentle number changes every 5s
- Background atmospheric effects: subtle grain, scanlines at very low opacity

**Interaction animations (quick, responsive, meaningful):**
- Card hover: translate up 4px + shadow deepen, 0.3s ease
- Scroll reveal: translate up 20px + fade in, 0.7-0.8s ease with stagger
- Feed item entry: slide in from right/left + fade, 0.4s ease
- Button hover: subtle scale or glow increase, 0.2s ease

**Forbidden animations:**
- Bounce, shake, or spin effects
- Attention-hijacking motion (flashing, pulsing CTAs)
- Parallax scrolling on content sections (backgrounds only)
- Loading spinners longer than 2 seconds without progress indication
- Any animation that does not respect `prefers-reduced-motion`

### Reference Brands and What to Borrow

**Figma -- Community as identity.** Figma's brand communicates that the product is its users. The community page, the plugin ecosystem, the "made with Figma" pride. CrowdForge should borrow this: the projects and people on the platform ARE the brand. Contributor avatars, project names, and activity feeds should appear everywhere.

**Discord -- Playfulness without childishness.** Discord uses character mascots (Wumpus), conversational copy, and bright colors, but never feels like a children's product. The tone is "your friend group's group chat," not "enterprise communication platform." CrowdForge should borrow the warmth and informality, but replace Discord's cartoon energy with CrowdForge's theater/jazz energy.

**Are.na -- Creative minimalism and anti-algorithm positioning.** Are.na's visual identity is restrained, intellectual, and intentional. "Playlists, but for ideas." The brand communicates that this is a place for people who think deeply. CrowdForge should borrow the sense of intentionality -- this is not a feed to mindlessly scroll. It is a place to DO something.

**Bandcamp -- Creator-first economics as brand identity.** Bandcamp leads with "Fans have paid artists $1.67 billion." The economic model IS the brand differentiator. CrowdForge should borrow this: "100% to creators" is not a feature -- it is the brand identity. The 0% commission is as central to CrowdForge's visual identity as the color palette.

---

## Part 3: Internal vs. External Voice

This is the most important section of this document. Every other branding decision is downstream of getting this right.

### The Problem

CrowdForge has a rich, evocative internal vocabulary: Riffs, Scenes, Ensembles, Stages, Sidecoaches, Forge Streams, Karma Tiers, Pioneer Multipliers. This vocabulary is powerful inside the community. It creates belonging, shared identity, and a sense of being part of something with its own culture.

But this vocabulary is lethal on a landing page. "Drop a Riff on a Scene and the Ensemble will validate your contribution" is meaningless to someone who has never heard of CrowdForge. It is worse than meaningless -- it signals "this is not for you" to the exact people the platform needs to attract.

### How Other Platforms Handle This

**Slack:** The homepage says "Where work happens" and "Slack is the productivity platform." It does not say "Create a channel in a workspace and use threaded replies to maintain topicality." The word "channel" does not appear prominently on the landing page. Users learn what channels, threads, huddles, and workflows are AFTER they sign up, through progressive disclosure during onboarding.

**Discord:** The homepage says "Group chat that's all fun & games." It does not say "Join a server, browse text and voice channels, and assign yourself roles." The words "server," "guild," and "role" are absent from the homepage. Users encounter these concepts in-product, after they have already decided to try Discord.

**Figma:** The homepage says "The collaborative interface design tool." It does not say "Create frames in a canvas, use auto-layout with constraints, and share prototypes via inspect mode." Users learn Figma's vocabulary (frames, components, auto-layout, variants) through the product experience and tutorial overlays.

**GitHub:** The homepage says "Where the world builds software." It does not say "Clone a repository, create a branch, stage changes, and submit a pull request." The entire Git vocabulary -- commits, branches, merges, rebases, DAGs -- is absent from the homepage. Users learn it through documentation, the product, and the community.

**The pattern is universal:** Landing pages speak plain human language. Internal vocabulary is introduced inside the product, after the user has committed to trying it.

### The Translation Guide

This table maps every significant internal term to its plain-language equivalent for external contexts (landing page, marketing, social media, ads) and defines when the internal term is introduced.

| Internal Term | Landing Page / Marketing | When to Introduce Internal Term |
|---|---|---|
| Riff | "contribution," "idea," or just show the action | First contribution (onboarding) |
| Scene | "project," "idea," "startup," or name the actual project | First project page visit (onboarding) |
| Ensemble | "people," "builders," "the people who built it," "team" | First week, when user joins a project |
| Stage | (never name it -- just show the platform) | Organic discovery; never formally introduced |
| Forge Stream | "live activity," "watch it happen," "live feed" | First visit to the activity feed |
| Sidecoach | "AI assistant," "helper," or (ideally) invisible | Never explicitly named to users |
| Karma | "karma" -- this term can appear on the landing page; Reddit and gaming culture normalized it | Sign-up / first contribution |
| Karma Tiers (Observer through Inner Circle) | "levels" or "reputation" if mentioned at all | First karma earned (onboarding) |
| Pioneer | "early contributor" or "first builders" | When a user joins a new project early |
| Pioneer Multiplier | "early builders earn more" | First week, in karma detail view |
| Contribution Velocity Floor | Never externalize this term | Never; internal system mechanic |
| Karma Dividend | "your share of the revenue" or "what you've earned" | First payout or revenue milestone |
| Tier Multiplier | Never externalize this term | Never; internal system mechanic |
| Canvas | "project page" or "workspace" | Internal-only for now |
| Audience | "spectators," "people watching" | Organic discovery |
| Yes, And... | "Yes, And..." -- this phrase is self-explanatory in context and can appear on the landing page | Landing page (in the Chain narrative) |
| Cinema-mode | Never externalize | Never; internal design concept |
| Spectator View | "watch mode" or just "watch" | Never formally named |
| Alive by Default | Never externalize | Never; internal design principle |
| Signature Experience | Never externalize | Never; internal product strategy |
| Bioluminescent | Never externalize | Never; internal visual language |
| Campfire Model | Never externalize | Never; internal philosophy |
| Hive Mind | Never externalize | Never; internal philosophy |

### Translation Examples

**Bad (jargon-heavy):**
> Drop a Riff on a Scene and the Ensemble will validate it. Earn karma and climb from Observer to Inner Circle. Watch the Forge Stream to find active Stages.

**Good (plain language, landing page):**
> Add your idea to a project. The people building it decide what stays. Earn reputation for everything you contribute. Watch live to see what's happening now.

**Bad (marketing email):**
> Your Pioneer Multiplier on Scene #12 is decaying. Drop a Riff before the contribution velocity floor resets.

**Good (marketing email):**
> The project you joined early is growing. Your early-contributor bonus is highest right now -- add something before it decreases.

**Bad (social media):**
> Just watched an Ensemble Riff a Scene from idea to shipped product in 6 hours on the Stage.

**Good (social media):**
> Just watched 7 people turn a coffee shop wifi tracker into a live product in 6 hours. None of them knew each other this morning.

### The Principle

Plain language gets them in the door. The vocabulary is the secret handshake they learn once they are inside.

Jargon should feel like something you EARN access to -- like learning the names of moves in a martial art, or the positions in an orchestra, or the slang of a neighborhood you just moved into. It is a marker of belonging, not a barrier to entry.

The moment a new user first hears "Riff" used naturally by another contributor, and understands what it means from context, that user has crossed a threshold. They are no longer a visitor. They are part of the culture. That moment cannot happen if the landing page already threw the vocabulary at them before they had any context to anchor it.

### Where Each Voice Applies

| Context | Voice | Vocabulary Level |
|---|---|---|
| Landing page | Plain English, zero jargon, show-don't-tell | External only |
| Marketing emails (cold) | Plain English, minimal jargon, curiosity-driven | External only |
| Sign-up flow | Plain English with gentle introductions | 1-2 terms max (karma) |
| Onboarding (first session) | Introduce core terms with plain-English anchors | Riff, Scene, karma |
| In-product UI (logged in) | Full internal vocabulary, used naturally | All terms |
| Community (Discord, forums) | Full internal vocabulary, peer-to-peer | All terms |
| Marketing emails (to users) | Internal vocabulary OK, they know the terms | All terms |
| Documentation / guides | Internal vocabulary with definitions on first use | All terms, defined |

---

## Part 4: Onboarding Vocabulary Ramp

### Design Principle

Each internal term is introduced at the moment it becomes useful -- not before. A term introduced before the user has context for it is noise. A term introduced at the exact moment the user needs it becomes instantly intuitive.

### The Journey Map

**Stage 0: Landing Page (pre-signup)**

Vocabulary exposed: NONE (except "karma" if used, and "Yes, And..." in narrative context).

The landing page uses only plain English. The visitor sees:
- "Finish each other's startups" (not "Riff on each other's Scenes")
- "Someone shares an idea" (not "Someone drops a Riff")
- "Others add to it" (not "The Ensemble riffs on it")
- "5 people" (not "An Ensemble of 5")
- "247 people creating right now" (not "247 contributors on Stage")

The visitor should leave the landing page understanding WHAT happens (people build things together) without knowing any of the vocabulary for HOW the platform describes it.

**Stage 1: Sign-Up Flow**

Vocabulary introduced: karma (passively).

The sign-up flow is fast and frictionless. The only internal term that appears is "karma," and only in passing context ("You'll earn karma for everything you contribute"). Karma needs no explanation -- Reddit, gaming, and Buddhism have done the work. The sign-up flow does NOT explain tiers, multipliers, or scoring mechanics.

What the user sees:
- "What do you like to build?" (skill selection, plain language)
- "Here are projects that need your skills" (not "Here are Scenes that need Riffs")

**Stage 2: First Project Page Visit**

Vocabulary introduced: Scene, Riff.

The first time a user visits a project page, they encounter the internal vocabulary in context. The page heading says "Scene" where a generic platform would say "Project." The contribution input says "Add a Riff" where a generic platform would say "Contribute."

The terms are contextually obvious. The page shows other people's Riffs (contributions), labeled as Riffs, with creator avatars and timestamps. The user understands by seeing, not by reading a glossary.

An optional tooltip or first-time overlay can provide a one-line anchor:
- "On CrowdForge, projects are called Scenes -- because they're collaborative, alive, and always evolving."
- "Your contributions are called Riffs -- because every idea builds on what came before."

These tooltips appear once, on first visit, and are dismissable. They are not modals, not blocking, and not mandatory.

**Stage 3: First Contribution**

Vocabulary reinforced: Riff, Scene. New exposure: Ensemble (passively).

When the user submits their first contribution, the confirmation message says something like: "Your Riff is live. The ensemble can see it now." This is the first time "ensemble" appears, and its meaning is clear from context -- the other people on the project.

The user also sees their first karma earned. No explanation of the formula. Just a number going up. "You earned 12 karma for this Riff." The dopamine hit teaches the concept faster than any documentation.

**Stage 4: First Week**

Vocabulary introduced: Ensemble (formally), karma tiers, Pioneer.

After a few contributions, the user has enough context to understand the community layer:
- Their profile shows their karma tier (Observer, Contributor, etc.) with a progress indicator to the next tier. The tiers are self-explanatory in order.
- If they joined a project early, they see a "Pioneer" badge. An in-context note explains: "You joined this project early. Pioneers earn more karma because they took the risk."
- The word "Ensemble" now appears naturally in project descriptions, contributor lists, and notifications.

**Stage 5: Power User (Weeks 2+)**

Vocabulary unlocked: Full platform vocabulary.

By this point, the user speaks the language. They say "Riff" and "Scene" naturally. They understand karma tiers, Pioneer bonuses, and Ensemble dynamics from experience. The platform's full vocabulary is available in settings, documentation, and advanced features.

Terms that remain internal-only even for power users:
- Sidecoach (the AI helper is just "the AI" or invisible)
- Cinema-mode (the immersive view is just "full screen" or "focus mode")
- Contribution velocity floor (the mechanic is invisible)
- Tier multiplier (the mechanic is invisible)
- Bioluminescent, alive by default, signature experience (design principles, not features)

### Vocabulary Introduction Summary

| User Stage | Terms Introduced | Method |
|---|---|---|
| Landing page | None | Show, don't name |
| Sign-up | Karma (passive) | In-context mention |
| First project page | Scene, Riff | Contextual exposure + optional tooltip |
| First contribution | Ensemble (passive) | Confirmation message |
| First week | Ensemble (formal), tiers, Pioneer | Profile UI, badges, notifications |
| Power user | Full vocabulary | Organic, through documentation and community |

### Anti-Patterns in Vocabulary Onboarding

- **The glossary dump.** Never show a "Learn CrowdForge terminology" page during onboarding. Glossaries are for reference, not for learning.
- **The forced tutorial.** Never make a user complete a "learn what a Riff is" step before they can contribute. Let them DO the thing, then name it.
- **The tooltip avalanche.** Never show more than one new term per screen. Cognitive overload kills retention.
- **The "we're different" manifesto.** Never dedicate a page to explaining why CrowdForge uses different words. The vocabulary should feel natural, not ideological.

---

## Part 5: Copy Voice Guidelines

### The Voice

CrowdForge sounds like a friend showing you something cool they found. Not pitching you. Not selling you. Showing you. The friend is excited but not desperate. Knowledgeable but not pedantic. Confident but not arrogant.

**Benchmark voices:**
- A friend texting "come look at this, you won't believe what these people just built"
- Paul Graham writing about something he finds genuinely interesting
- The MC at a jazz club introducing the next set
- A theater director giving a pre-show pep talk

**Not these voices:**
- A SaaS marketing page ("Streamline your workflow with our AI-powered platform")
- A startup pitch deck ("We're disrupting the $4.7T freelance economy")
- A hackathon MC ("Who's ready to SHIP?!?!")
- A DAO governance proposal ("This proposal seeks to allocate treasury funds")
- A corporate press release ("We are excited to announce")

### Tone Rules

**Lead with building, creating, and belonging.** Financial outcomes are a consequence, not the pitch. The person who comes to CrowdForge because they want to make money will be disappointed. The person who comes because they want to make something with people will find the money is a bonus.

Bad: "Earn money building startups with people."
Good: "Build something with people. When it makes money, everyone shares."

Bad: "Unlock higher revenue shares by climbing karma tiers."
Good: "The more you build, the more the community trusts you."

**Be specific, not aspirational.** Real names, real numbers, real outcomes.

Bad: "Join thousands of creators building the future."
Good: "7 people turned a wifi tracker into a live product in 6 hours."

Bad: "Powerful collaboration tools for modern teams."
Good: "Sara had an idea at 2pm. By 6pm, four people had shipped it."

**Be brief.** If a sentence can lose a word, lose it. If a paragraph can lose a sentence, lose it. The audience is builders -- they respect economy.

Bad: "CrowdForge is a collaborative platform that enables people to come together and build innovative products while sharing in the revenue generated by their collective creative contributions."
Good: "Strangers build things together. Everyone who helped gets paid."

**Active voice, always.** The subject does the thing. No passive constructions.

Bad: "Karma is awarded based on contribution quality."
Good: "You earn karma for everything you build."

Bad: "Revenue is distributed proportionally among contributors."
Good: "Everyone who helped gets their share."

**Provocative over safe.** Take a position. Make a claim. Be interesting.

Safe: "A new way to collaborate on projects."
Provocative: "Finish each other's startups."

Safe: "Fair compensation for all contributors."
Provocative: "100% to creators. The platform keeps nothing."

### Forbidden Words and Phrases

| Never Use | Why |
|---|---|
| leverage | Corporate jargon |
| synergy | Corporate jargon |
| ecosystem | Overused in tech, means nothing |
| disrupt / revolutionize | Startup cliche, grandiose |
| empower | Patronizing |
| unlock | Gaming/SaaS cliche |
| supercharge | Hyperbole |
| seamless | Meaningless superlative |
| robust | Meaningless superlative |
| cutting-edge | Dated cliche |
| game-changing | Startup cliche |
| AI-powered | The brand is human-first |
| blockchain / web3 / DAO / token | Instant credibility damage |
| simple / easy / just | Diminishes complexity the audience respects |
| startup (as primary framing) | Too Silicon Valley; use "project" or name the actual thing |

### Allowed Exceptions

| Term | Why It Works |
|---|---|
| karma | Widely understood from Reddit and gaming culture |
| Yes, And... | Self-explanatory in context, core to identity |
| builders | Active, identity-affirming, not jargon |
| ship / shipped | Developer culture, universally understood |
| people | Specific, evocative, slightly provocative |

### Copy Examples by Context

**Landing page headline options:**
- "Finish each other's startups."
- "You bring the spark. Strangers bring the fire."
- "What gets built when nobody's in charge."

**Landing page sub-headline:**
- "Someone shares an idea. Strangers add to it. It gets built -- and when it makes money, everyone who helped shares the revenue."

**CTA buttons:**
- Pre-launch: "Join the waitlist" / "Watch it happen"
- Post-launch: "Start building" / "Watch live" / "Browse projects"
- Never: "Sign up free" (SaaS cliche), "Get started" (generic), "Try it now" (desperate)

**Error states:**
- Bad: "Oops! Something went wrong. Please try again."
- Good: "That didn't work. Here's what happened: [specific error]. Try [specific action]."

**Empty states:**
- Bad: "Nothing to see here yet!"
- Good: "No projects match your skills yet. New ones appear every few hours."

**Notification copy:**
- Bad: "You've received 15 karma points!"
- Good: "You earned 15 karma. @jin built on your idea."

---

## Appendix: Research Sources

This document draws on analysis of the following landing pages and brands, accessed February 2026:

- Lovable (lovable.dev) -- AI app builder, input-field-as-hero pattern, community showcase
- Linear (linear.app) -- Product development tool, dense information design, monospace aesthetic
- Vercel (vercel.com) -- Developer platform, trust through specificity, customer logos
- Notion (notion.com) -- Workspace tool, emotional headline + structural proof, mascot integration
- Figma (figma.com) -- Design tool, community-as-product, collaborative identity
- Arc Browser (arc.net) -- Browser, user-centric framing, deep blue palette
- Discord (discord.com) -- Communication platform, plain-language mastery, progressive vocabulary
- Bandcamp (bandcamp.com) -- Music platform, creator-first economics as brand identity
- Are.na (are.na) -- Knowledge curation, creative minimalism, anti-algorithm ethos
