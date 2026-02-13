# CrowdForge Vocabulary

Internal document. Defines the platform's terminology, what each term replaces, and why the replacement matters.

---

## Core Vocabulary

| Term | Replaces | Why | Visibility |
|------|----------|-----|------------|
| **Scene** | Project | Improv scenes are collaborative, temporary, alive. "Projects" sound like corporate PMO — milestones, deliverables, Gantt charts. A Scene is something you step into, contribute to, and watch evolve. | User-facing |
| **Riff** | Contribution / Task | Musical — you riff ON something. Inherently creative and collaborative. Format-agnostic: a Riff can be code, design, copy, strategy, naming, architecture, a joke. "Task" implies assignment. "Contribution" implies charity. A Riff implies play. | User-facing |
| **Ensemble** | Team / Contributors | Theater — a group creating together with no fixed hierarchy. No lead. No manager. Just people who showed up and started creating. "Team" implies structure and roles. An Ensemble implies collective creation. | User-facing |
| **Audience** | Viewers / Spectators | An improv audience that participates. They suggest, react, vote, and can step on stage at any moment. "Viewer" implies passivity. "Audience" implies energy flowing both directions. | User-facing |
| **Stage** | Platform feed / Dashboard | Where Scenes play out live. The Stage is what you see when you open the platform — active Scenes, trending Riffs, Ensemble activity. "Dashboard" implies metrics. "Feed" implies scrolling. A Stage implies performance and presence. | User-facing |
| **Canvas** | Project page | A Canvas fills up, gets richer, accumulates layers. A project page is a checklist getting checked off. The Canvas is the living artifact of a Scene — code, designs, discussions, prototypes, all layered together. | Internal-only (for now) |
| **Karma** | Points / Credits / Tokens | Stays as-is. Karma is earned on Stage through contribution, never bought, never traded. It's reputation made tangible. "Points" sound like a game. "Credits" sound like currency. "Tokens" sound like crypto. Karma sounds like something you earn by doing right. | User-facing |
| **Pioneer** | Early contributor | Someone who joined a Scene in its earliest epochs, before it had momentum or certainty. Pioneers took the risk. The karma multiplier for Pioneers reflects that risk. | User-facing |

## Karma Tiers

Six tiers, in order:

1. Observer
2. Contributor
3. Builder
4. Architect
5. Partner
6. **Inner Circle**

CSS class for tier 6: `.tier--inner-circle`

"Founder's Circle" is permanently retired. Never use it.

## Forbidden Vocabulary

### Internal-only (never user-facing)

These terms are used in internal docs and code comments but must never appear in UI copy, marketing, or user-facing text:

- **cinema-mode** — internal name for the immersive Scene viewing experience
- **spectator view** — use "Audience view" in user-facing contexts
- **alive by default** — internal design principle, not a feature name
- **signature experience** — product strategy jargon, not user language
- **bioluminescent** — internal visual design language reference

### Retired Terms

- **Founder's Circle** — permanently retired. The tier is called **Inner Circle**.

## Where Vocabulary Applies

### Inside the platform (use vocabulary)
Once someone is logged in and using CrowdForge, use the vocabulary naturally. "Start a Scene" not "Create a project." "Drop a Riff" not "Submit a contribution." "Join the Ensemble" not "Join the team."

The vocabulary should feel like slang that a community invented, not terminology that a product team imposed. If it sounds like a glossary entry, rewrite it until it sounds like something someone would actually say.

### Landing page and marketing (use plain English)
First-time visitors have zero context. "Riff," "Scene," "Ensemble," "Stage" mean nothing to them. The landing page SHOWS what happens (through the demo/chain) and EXPLAINS it in everyday language. Visitors earn the vocabulary by using the product — the landing page doesn't teach it.

**Landing page rules:**
- Never use "Riff" — say "contribution," "idea," or just show it happening
- Never use "Scene" — say "project" or "idea" or describe what's being built
- Never use "Ensemble" — say "strangers," "builders," "people"
- Never use "Stage" — just show the platform
- "Karma" is OK — it's widely understood from Reddit/gaming culture
- "Yes, and..." is OK — it's the core concept and is self-explanatory in context

### Internal docs and code (use vocabulary freely)
All internal documents, code comments, variable names, and team communication use the full vocabulary without restriction.
