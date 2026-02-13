# Agent: Platform Governance & Meta-Contribution

## Mission
Design and implement the governance layer for CrowdForge itself — the platform, not the projects on it. The platform is sacrosanct. While projects use "Yes, and..." free-flowing collaboration, changes to the platform itself go through a fundamentally different, more secure approval process. This agent also designs how contributors to the platform (as opposed to projects) are rewarded.

## The Sacrosanct Boundary

| | Project Contributions | Platform Contributions |
|---|---|---|
| Who proposes | Anyone | Anyone |
| Who approves | Peer review + project founder | Core team / elevated governance |
| Reward | Karma → dividends | Admin privileges, cosmetics, hiring pipeline |
| Risk if gamed | One project gets diluted | Entire platform gets hijacked |

## Platform Contribution Rewards
Contributors who improve CrowdForge itself do NOT earn karma-to-revenue. Instead:
- **Admin privileges** — elevated trust, moderation powers
- **Custom cosmetics** — profile skins, badges, visual flair
- **Hiring pipeline** — platform contributors are first in line for full-time roles
- **Recognition** — "Platform Builder" designation on profile
- **Governance participation** — vote on platform-level decisions

## What to Build

### Platform Change Governance
- All platform PRs require core team approval (not just peer review)
- Security-critical changes require multiple core team members
- Public changelog for all platform changes
- Community can propose changes but cannot self-approve (prevents the "10 bots approve their own change" attack)

### Community Governance for Projects
- Dispute resolution process for karma disagreements
- Project sunset voting (2/3 majority of active contributors)
- Governance thresholds that activate at revenue tiers ($1K, $10K/month)
- Independent reviewer program for high-revenue projects

### Moderation System
- Content moderation for discussions and pitches
- Contribution flagging (spam, plagiarism, harmful content)
- Appeal process for moderation decisions
- Graduated sanctions (warning → restriction → suspension → ban)

## Reference Docs
- `../docs/research/wikipedia.md` — governance hierarchy, admin elections, Ostrom's 8 principles for governing commons
- `../docs/fraud-prevention/design.md` — graduated trust, insider defense
- `../docs/research/stackoverflow.md` — how reputation aristocracy killed the community

## The Anti-Aristocracy Principle
Stack Overflow died because high-rep users weaponized moderation to gatekeep newcomers. CrowdForge must prevent this:
- High-karma contributors gain responsibilities, not power over others
- Steward tier means you help more, not that you control more
- Mentoring activity should be tracked and rewarded
- Red flags: high-karma users with high rejection rates on newcomer contributions

## Constraints
- Platform changes and project contributions are completely separate governance tracks
- No single person should be able to unilaterally change the platform
- Governance should be transparent — all decisions logged and publicly queryable
- The governance system itself should be evolvable (not hardcoded rules)
