# Wikipedia & Wikia/Fandom: Collaboration at Scale

Platform strategy research for CrowdForge. What makes millions of humans build an encyclopedia for free, and what breaks when you commercialize it.

---

## 1. The Collaboration Miracle: How Wikipedia Happened

### Scale

- Founded January 15, 2001 by Jimmy Wales and Larry Sanger
- 20,000 articles by end of 2001, purely organic growth
- English Wikipedia: 7+ million articles as of 2024
- 66+ million articles across 300+ language editions
- 1.5 billion unique device visits per month
- 13 million edits per month (~5 edits per second)
- Hosted by Wikimedia Foundation, funded almost entirely by reader donations

### The Growth Engine

Wikipedia's growth followed an exponential curve from 2001-2007, when active editor count and editing volume peaked. The engine was a self-reinforcing loop:

1. **Low barrier to entry** -- anyone can edit, no account required for minor edits
2. **Immediate visibility** -- your contribution is live instantly, giving a dopamine hit of "I changed something millions will read"
3. **Cumulative value** -- each edit makes the whole more valuable, attracting more readers, which attracts more editors
4. **Network effects in knowledge** -- more articles create more internal links, which create more discovery, which creates more articles

The key insight: Wikipedia didn't ask people to "write an encyclopedia." It asked them to fix a typo, add a fact, expand a stub. The granularity of contribution was the innovation. You could contribute 30 seconds or 30 hours. Both mattered.

### What Benkler Calls "Commons-Based Peer Production"

Harvard professor [Yochai Benkler](https://en.wikipedia.org/wiki/The_Wealth_of_Networks) coined the term "commons-based peer production" (CBPP) to describe Wikipedia's model. Key characteristics:

- **No single person controls the resource** -- it's open to the public or a defined group
- **Self-selected, decentralized individual action** -- no one assigns tasks
- **Less rigid hierarchy** than traditional organizations
- **Non-profit scope** with no financial compensation for contributors
- Individuals act "out of social and psychological motivations to do something interesting"

Benkler's examples of CBPP: free/open-source software, Wikipedia, NASA Clickworkers. The pattern is the same: modular tasks + intrinsic motivation + shared commons = massive output.

---

## 2. Governance: Emergent Bureaucracy

### The Hierarchy (Bottom to Top)

| Role | Count (English Wikipedia) | Powers |
|------|--------------------------|--------|
| **Anonymous editors** | Unlimited | Edit unprotected pages |
| **Registered editors** | ~11.9M total, ~39K active monthly | Edit semi-protected pages, vote, upload files |
| **Autoconfirmed users** | Auto-granted after 4 days + 10 edits | Edit semi-protected pages |
| **Rollbackers** | Granted by admins | Revert vandalism with one click |
| **Administrators** | ~1,100 | Delete pages, protect pages, block users |
| **Bureaucrats** | 16 | Grant admin rights, rename users |
| **Stewards** | ~30 (cross-wiki) | All technical permissions across all Wikimedia projects |

### How Admins Are Elected: Requests for Adminship (RfA)

The RfA process is Wikipedia's most sophisticated governance mechanism:

1. Any editor can nominate themselves or be nominated
2. Community discussion runs for 7 days
3. Editors evaluate: contributions, past history, commitment, trust, temperament
4. **Not a vote** -- officially a consensus discussion, though practically ~75-80% support is needed to pass
5. Bureaucrats make the final call on whether consensus exists
6. The standard ensures "a high level of experience, trust and familiarity across a broad front of projects"

This is meritocratic selection without formal credentials. Your track record IS your resume.

### Quality Control Mechanisms

Wikipedia doesn't rely on one control mechanism but layers many:

- **Recent Changes patrol** -- volunteers watch the firehose of edits in real-time
- **Anti-vandalism bots** (ClueBot NG and others) -- revert obvious vandalism within seconds. IBM found most vandalism on English Wikipedia is reverted within 5 minutes
- **Page protection levels** -- unprotected, semi-protected (no new/anon editors), fully protected (admins only)
- **Article quality ratings** -- Stub, Start, C, B, Good Article, Featured Article
- **Featured Article process** -- rigorous peer review for the highest quality tier; having an article selected as Featured boosts editor motivation (76% of editors report this)
- **Dispute resolution pipeline** -- talk page discussion -> third opinion -> mediation -> arbitration committee

### Edit Wars and Conflict

Edit wars are rare relative to total editing volume, but they're disproportionately visible and damaging to editor morale. The governance response:

- **3-revert rule (3RR)** -- reverting more than 3 times in 24 hours on the same page can get you blocked
- **Page protection** -- admins can lock disputed pages
- **Arbitration Committee (ArbCom)** -- elected body that handles the most intractable disputes, can impose topic bans and editor sanctions

### Deletionism vs. Inclusionism

The longest-running philosophical conflict in Wikipedia. Two camps:

**Deletionists** argue for strict notability standards -- if a topic doesn't have significant coverage in reliable secondary sources, the article should go. Motivated by quality, focus, and preventing promotional content.

**Inclusionists** argue for broad coverage with lower entry barriers -- content starts poor and improves; there's no incremental cost to hosting; you can't predict what knowledge will be useful.

The deletionists have largely won in practice: ~25% of all articles have been deleted, with 28% of deletions attributed to lack of notability. This has real consequences -- deletionism's notability criteria correlate with systemic biases (underrepresentation of topics important to non-Western, non-English-speaking populations).

**CrowdForge lesson:** Every collaborative platform will develop its own version of this debate. The question is whether the gatekeeping mechanism serves quality or just incumbent power.

### The Self-Organizing Bureaucracy Paradox

Research describes Wikipedia as a ["self-organizing bureaucracy"](https://www.tandfonline.com/doi/full/10.1080/1369118X.2021.1994633). The community developed increasingly rigid procedures to handle complexity, and although Wikipedia's fifth pillar says editors can "ignore all rules," in practice editors willingly crafted and enforced elaborate rule systems. Developing and enforcing rules became its own form of contribution -- a kind of meta-work.

---

## 3. Why People Contribute: The Motivation Stack

### Academic Research Findings

[Research on Wikipedia contributor motivations](https://www.sciencedirect.com/science/article/abs/pii/S0747563210000877) identifies **internal self-concept motivation** as the primary driver -- not altruism, not external reward, but the need to see yourself as competent and knowledgeable.

The motivation stack, roughly ordered by prevalence:

1. **Learning and teaching** -- the most ubiquitous motivation. Editors learn by researching topics to write about, and teach by making knowledge accessible. The process of editing IS the reward.

2. **Competence signaling** -- editing Wikipedia demonstrates expertise. The edits are public, attributable, and permanent. It's a portfolio of knowledge work.

3. **Community belonging** -- Wikipedia has a rich social layer: talk pages, WikiProjects, meetups, barnstars. Editors form genuine relationships. The community satisfies the psychological need for [relatedness](https://pmc.ncbi.nlm.nih.gov/articles/PMC5364176/) (Self-Determination Theory).

4. **Autonomy** -- editors choose what to work on, when, and how much. No one assigns tasks. This satisfies the need for autonomy, a core driver in SDT.

5. **Impact visibility** -- seeing your words on a page read by millions. This is the "cathedral builder" effect: contributing to something larger than yourself.

6. **Ideological commitment** -- belief in free knowledge as a public good. Many editors are motivated by the mission itself.

7. **Fun** -- the puzzle-solving pleasure of improving an article, tracking down sources, winning a "did you know" nomination.

### What Self-Determination Theory (Deci & Ryan) Says

SDT identifies three fundamental psychological needs:

- **Autonomy** -- sense of initiative and ownership in one's actions
- **Competence** -- feeling effective and capable
- **Relatedness** -- meaningful connection with others

Wikipedia satisfies all three. This is not an accident -- it's the structural reason Wikipedia works. Platforms that violate any of these three needs will struggle with contributor retention.

### The Barnstar System: Non-Monetary Recognition

[Barnstars](https://en.wikipedia.org/wiki/Wikipedia:Barnstars) are virtual awards editors give each other. Introduced in 2003, they have become central to Wikipedia's motivational infrastructure:

- Anyone can award one to anyone -- no permission or status required
- Placed on the recipient's user talk page with a personalized message
- Types include: Original Barnstar (general excellence), Copyeditor's, Anti-Vandalism, Technical, Mediation
- Accumulation of barnstars informally signals trustworthiness and expertise
- Research shows barnstars influence admin election outcomes and collaboration invitations
- 76% of editors report that having an article selected as Featured boosted their editing activity

The insight: **non-monetary, peer-to-peer recognition is more motivating than any formal reward system could be**, because it satisfies competence and relatedness needs simultaneously.

---

## 4. The Editor Decline Problem

### The Numbers

Wikipedia's editor count peaked around 2007 and has been in gradual decline since:

- December 2024: ~39,000 active editors (English Wikipedia), down 0.15% year-over-year
- 12-month average: ~38,000 active editors
- In 2024: 775,435 registered editors made at least one edit, but about half were one-time edits
- The most active 1,000 editors (~0.003% of users) contribute about two-thirds of all edits

### Why Editors Leave

[Research on editor retention](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_Editor_Retention/Reasons_editors_leave) identifies these factors:

1. **Hostile reception of new editors** -- new editors are most likely to leave within 15 days. It takes ~200 days to integrate into the core community. The gap between those two numbers is where most attrition happens.
2. **Bureaucratic overhead** -- the rule system that emerged to manage quality also creates barriers to participation
3. **Edit warring and incivility** -- experienced editors leaving triggers cascading departures; discourse quality deteriorates, repelling serious newcomers
4. **Admin overreach** -- frustration from blocks, threats of blocks, or administrative actions against long-term editors
5. **"Lone wolf" culture** -- the absence of a supportive, collaborative environment repels many contributors, particularly women
6. **Gender gap** -- women editors have shorter lifecycle than men; women editor drop-off is a determinant factor in the community's gender gap
7. **Core burnout** -- long-term editors get tired of answering the same questions, become brusque, and eventually disengage entirely. Administrator activity has been noticeably falling.

**CrowdForge lesson:** The biggest threat to a collaborative platform is not insufficient contributors but the loss of experienced ones. Retention > recruitment.

---

## 5. Wikia/Fandom: Commercializing the Wiki Model

### Business Model

[Fandom](https://en.wikipedia.org/wiki/Fandom_(website)) (originally Wikia, co-founded by Jimmy Wales in 2004) applied the wiki collaboration model to entertainment fandoms -- games, movies, TV, anime.

- Revenue model: **advertising** -- display ads, auto-playing video ads, pop-ups
- Raised $191M across 10 funding rounds
- Acquired GameSpot, Metacritic, TV Guide, GameFAQs, Giant Bomb, Comic Vine from Red Ventures in October 2022
- Sold D&D Beyond to Hasbro for $146.3M
- In February 2025, launched "FanDNA Helix" -- an AI model trained on wiki content + user social media to serve targeted ads

### The Value Extraction Problem

Fandom's model creates a fundamental tension:

- **Contributors** do all the work: researching, writing, formatting, moderating, maintaining thousands of wiki pages
- **Contributors get nothing** -- no payment, no revenue share, no equity
- **Fandom captures all the value** -- selling ads against contributor-generated content
- Fandom provides hosting, infrastructure, and "support" in exchange for 100% of ad revenue

This has been [described as a model for labor exploitation](https://www.jsr.org/hs/index.php/path/article/download/1237/500/4663). Fans invest thousands of unpaid hours while Fandom generates substantial revenue from their work.

### The Backlash and Migration (2024-2025)

The chickens came home to roost. [Major wiki communities are leaving Fandom](https://thegameofnerds.com/2025/11/15/the-monetization-backlash-how-fandom-wiki-sites-are-losing-community-trust/):

**2024 migrations:** South Park Wiki, Dead by Daylight Wiki, League of Legends Wiki
**2025 migrations:** Warframe, Vampire Survivors, Undertale/Deltarune, Nichijou, Balatro

Reasons cited:
- Aggressive monetization degrading user experience
- Auto-playing video ads, intrusive pop-ups, cluttered layouts
- Malvertising -- ads redirecting to suspicious sites
- Lack of communication -- Fandom running experiments without consulting wiki communities
- No regard for editor feedback
- November 2025: Fandom started showing ads to logged-in users who aren't actively editing

**Where they're going:** [Wiki.gg](https://wiki.gg) (founded by ex-Fandom president), [Miraheze](https://miraheze.org) (non-profit), self-hosted MediaWiki instances. These alternatives offer community control over layouts and ad policies.

### The Lesson

Fandom demonstrates that **you can build a billion-dollar business on volunteer labor, but the volunteers will eventually revolt if they receive zero value back while the platform extracts maximum value from their work.** The wiki content is portable (Creative Commons licensed), so when contributors leave, they take the content with them.

---

## 6. The Crowding Out Problem: Money vs. Motivation

### Core Research

The central question for CrowdForge: does adding financial reward help or hurt intrinsic motivation?

[Deci & Ryan's meta-analysis of 128 studies](https://pubmed.ncbi.nlm.nih.gov/10589297/) found:

- **Engagement-contingent, completion-contingent, and performance-contingent rewards significantly undermined intrinsic motivation**
- **Positive feedback enhanced both behavior and self-reported interest**
- The mechanism: rewards have two components -- a **controlling** component (do X to get Y) and a **competence-signaling** component (this reward means you're good)
- If the controlling component dominates, intrinsic motivation is crowded out
- If the competence-signaling component dominates, motivation is crowded in

### The Two Types of Reward

[Bruno Frey's motivation crowding theory](https://en.wikipedia.org/wiki/Motivation_crowding_theory) and [open source research](https://www.sciencedirect.com/science/article/abs/pii/S0048733313001868) clarify the distinction:

**Rewards that CROWD OUT motivation:**
- Corporate-assigned, controlling rewards ("we'll pay you $X to do Y")
- Rewards contingent on specific task completion
- Rewards that feel like surveillance or control
- The Debian/dunc-tank example: paying two release managers to finish a release on time caused resentment and crowded out volunteer motivation

**Rewards that CROWD IN motivation:**
- Voluntary, peer-originated rewards ("users tipped you because they valued your work")
- Merit-based recognition that signals status and competence
- Rewards that enhance autonomy rather than restrict it
- Google Summer of Code: framed as opportunity and recognition, attracted new contributors without displacing existing ones

### Open Source Evidence

[Research comparing paid vs. volunteer open source contributors](https://arxiv.org/html/2401.13940v1) found:

- Paid developers contribute more frequently and are more likely to become long-term contributors
- But paid developers work on employer-assigned priorities, not community priorities
- Volunteer developers contribute out of interest and passion, choosing their own tasks
- **Community-motivated developers are LESS willing to accept monetary rewards** -- money feels like it cheapens what they're doing
- The key factor is **who provides the reward and how it's framed**: voluntary user rewards feel supportive; corporate rewards feel controlling

### Implications for CrowdForge

The research points to a narrow path:

1. **Never make base participation transactional** -- the moment "contribute to get paid" becomes the frame, intrinsic motivation dies
2. **Reward as recognition, not payment** -- frame financial rewards as the community recognizing value, not as wages for work
3. **Peer-to-peer, not platform-to-contributor** -- rewards that come from other community members crowd in; rewards that come from the platform crowd out
4. **Preserve autonomy** -- contributors must choose what to work on. Assigned, paid tasks produce corporate employees, not community members
5. **Make rewards surprising and retrospective** -- reward work already done, don't promise payment for work to be done

---

## 7. The 1% Rule and Participation Inequality

### The Classic 90-9-1 Distribution

[Jakob Nielsen's 2006 formulation](https://www.nngroup.com/articles/participation-inequality/):

- **90%** of users are lurkers (read, never contribute)
- **9%** contribute occasionally (edit, comment)
- **1%** create most of the content

Wikipedia's numbers are even more extreme:
- 0.2% of unique visitors are active contributors
- The most active 1,000 editors (0.003% of users) produce two-thirds of all edits

### Is the Rule Changing?

Post-2020 data suggests the ratio is improving in some contexts:

- Small communities (under 5,000 members): up to 33% actively create or contribute
- Medium communities (10K-50K): ~20% participate, split between content creation (~10%) and reactions (~10%)
- The key variable is **community size** -- smaller communities have higher participation rates

### Strategies to Increase the Contributor Ratio

Based on research across Wikipedia and other platforms:

1. **Lower the contribution floor** -- Wikipedia's genius was making "fix a typo" a valid contribution. The smaller the minimum contribution, the more people cross the threshold from lurker to contributor.

2. **Immediate feedback loops** -- seeing your contribution live instantly converts lurkers to contributors. Delayed gratification kills participation.

3. **Progressive engagement** -- don't ask for essays, ask for reactions first, then comments, then edits, then original content. Build the habit incrementally.

4. **Social proof** -- showing that others like the contributor are participating. "Editors like you improved 50 articles this week."

5. **Remove friction, not standards** -- the barrier should be in the approval process, not the submission process. Let anyone submit; filter after.

6. **Small communities first** -- start with tight, high-trust groups where participation rates are naturally higher. Scale after culture is established.

---

## 8. Wikipedia's Reputation and Trust System

### How Trust Is Built

Wikipedia has no formal reputation score, points system, or leaderboard. Trust emerges from:

1. **Edit history** -- every edit is permanently attributed. Your contribution history IS your reputation. Anyone can review it.

2. **Barnstars** -- peer-awarded recognition tokens. Informal but socially significant. Barnstar accumulation correlates with admin election success.

3. **User page** -- editors curate a profile showing their interests, contributions, and awards. Functions as a portfolio.

4. **WikiProject membership** -- joining topic-specific working groups signals expertise and commitment.

5. **Article quality milestones** -- being the primary author of a Good Article or Featured Article is high-status.

6. **Tenure and edit count** -- raw numbers matter. Autoconfirmed status requires 4 days + 10 edits. Admin candidates typically have thousands of edits over years.

### Why This Works

The system works because:

- **Trust is earned through observable behavior**, not claimed through credentials
- **Reputation is contextual** -- being trusted on biology articles doesn't make you trusted on political ones
- **The community decides** -- admin elections, article reviews, dispute resolution all involve community judgment
- **No buying your way in** -- money cannot purchase status (contrast with Fandom's approach)
- **Graduated authority** -- you earn more power as you demonstrate more trustworthiness, but the power can be revoked

### What Breaks It

- **Credential inflation** -- as the bar for adminship rises (currently ~75-80% approval needed), fewer people try, creating a shrinking admin pool
- **Old guard dynamics** -- long-tenured editors accumulate informal power that can be exclusionary
- **Opacity** -- not all community norms are written down; newcomers face hidden rules

---

## 9. The Evolutionary Basis: Why Humans Collaborate

### Tomasello's Shared Intentionality

[Michael Tomasello's research](https://onlinelibrary.wiley.com/doi/full/10.1002/ejsp.2015) identifies humans as "ultra-social primates" with a unique cognitive capacity: **shared intentionality** -- the ability to participate with others in activities with shared goals and intentions.

Key findings:

- Great apes understand intentional action but do NOT participate in joint activities with shared intentions
- Human children develop shared intentionality in the first 14 months of life through two converging pathways: (1) understanding others as intentional agents, and (2) a species-unique motivation to share emotions and activities
- This capacity enabled cumulative culture: collaborative innovations built on previous generations' work

### The Interdependence Hypothesis

[Tomasello's two-step model](https://www.journals.uchicago.edu/doi/10.1086/668207) of how human cooperation evolved:

**Step 1: Collaborative foraging.** Humans became obligate collaborative foragers -- individuals were interdependent and had direct interest in partners' well-being. This produced:
- Joint attention and communication
- Shared goals and plans
- Norms of fairness in dividing spoils

**Step 2: Cultural group identity.** As groups competed, humans developed:
- Group norms and social institutions
- In-group loyalty and conformity
- Teaching and pedagogy
- Cumulative cultural evolution

### What This Means for Platform Design

Humans don't need to be convinced to collaborate. **Collaboration is the default mode.** What platforms need to do is remove the barriers that prevent natural collaborative behavior:

1. **Shared intentionality requires shared goals** -- the platform must articulate a goal people can jointly pursue
2. **Interdependence creates investment** -- when your success depends on others' success, you care about their well-being
3. **Fairness norms are instinctive** -- humans have deep intuitions about fair distribution of collaborative spoils. Violating these norms (Fandom's model) triggers revolt
4. **Group identity amplifies effort** -- people work harder for "their" community than for an abstract platform
5. **Teaching is a natural human behavior** -- platforms that enable knowledge transfer tap into a deep-rooted motivation

---

## 10. Ostrom's Design Principles for Governing the Commons

[Elinor Ostrom](https://en.wikipedia.org/wiki/Elinor_Ostrom) won the Nobel Prize for demonstrating that communities can self-govern shared resources without centralized authority or privatization. Her eight design principles for successful commons governance:

1. **Clearly defined boundaries** -- who has rights to participate must be clear (Wikipedia: anyone can edit, but privileges are earned)

2. **Congruence between rules and local conditions** -- rules must match the actual situation, not be imposed from above (Wikipedia: each WikiProject develops its own norms)

3. **Collective-choice arrangements** -- those affected by rules can participate in modifying them (Wikipedia: policy changes require community consensus)

4. **Monitoring** -- monitors are accountable to the community or are community members themselves (Wikipedia: Recent Changes patrol, anti-vandalism bots, peer review)

5. **Graduated sanctions** -- violations receive proportional responses, not nuclear options (Wikipedia: warning -> temporary block -> extended block -> ban)

6. **Conflict resolution mechanisms** -- accessible, low-cost dispute resolution (Wikipedia: talk pages -> mediation -> arbitration)

7. **Minimal recognition of rights to organize** -- external authorities don't undermine community self-governance (Wikipedia: Wikimedia Foundation deliberately avoids interfering in editorial decisions)

8. **Nested enterprises** -- governance organized in multiple layers (Wikipedia: individual articles -> WikiProjects -> community-wide policies -> Wikimedia Foundation)

Wikipedia satisfies all eight principles. Fandom violates principles 3, 4, and 7 (the corporation makes unilateral decisions, monitors serve corporate interests, and the platform undermines community self-governance).

---

## 11. Synthesis: Lessons for CrowdForge

### What Wikipedia Proves

1. **Humans will collaborate at massive scale without financial reward** -- given the right conditions (shared purpose, autonomy, community, visible impact)

2. **Governance must emerge from the community, not be imposed** -- Wikipedia's rules were crafted by the people who follow them

3. **Granularity of contribution is critical** -- the smaller the minimum useful contribution, the more people participate

4. **Reputation systems based on observable behavior work** -- no need for formal credentials or centralized scoring

5. **Peer recognition (barnstars) is more motivating than any formal reward system**

### What Wikipedia's Problems Warn Against

1. **Bureaucratic ossification** -- rules that emerged to solve problems become barriers to participation. CrowdForge must keep governance lightweight and adaptive.

2. **The deletionism trap** -- quality gatekeeping can become exclusionary power. CrowdForge needs clear, transparent standards that don't become tools of incumbent control.

3. **New contributor hostility** -- the 15-day cliff where most Wikipedia editors quit. CrowdForge needs active onboarding, mentorship, and protected early experiences (relates to CrowdForge's existing "spawn protection" concept).

4. **Core contributor burnout** -- the most active contributors carry disproportionate load and burn out. CrowdForge must distribute work and recognize sustained effort.

5. **Gender and diversity gaps** -- Wikipedia's hostile culture repels women and underrepresented groups. CrowdForge must design for inclusion from day one.

### What Fandom's Failure Teaches

1. **Value extraction without value sharing destroys communities** -- Fandom's 100% ad revenue capture + 0% contributor compensation is unstable. Contributors will migrate when alternatives exist.

2. **Content portability is a double-edged sword** -- Creative Commons licensing means contributors can take their work elsewhere. For CrowdForge: if contributors own their work, they stay because they want to, not because they're locked in. This builds genuine loyalty.

3. **Platform decisions must involve the community** -- Fandom's unilateral experiments and policy changes triggered the exodus. CrowdForge governance must give contributors real voice.

### The Financial Reward Design Space

Based on crowding out research, the viable approaches for CrowdForge:

| Approach | Crowding Effect | Why |
|----------|----------------|-----|
| Platform pays contributors per task | CROWDS OUT | Feels controlling, converts intrinsic motivation to transactional |
| Users tip/reward contributors voluntarily | CROWDS IN | Peer-originated, signals value and competence |
| Revenue sharing based on contribution | DEPENDS | If transparent and fair, crowds in. If opaque or unfair, crowds out |
| Equity/ownership stake | CROWDS IN | Aligns incentives, creates interdependence, satisfies fairness norms |
| Bounties for specific tasks | MIXED | Attracts mercenaries, repels community-motivated contributors |
| Recognition + optional financial component | CROWDS IN | Recognition is primary, money is secondary signal of value |

The optimal design: **make the primary reward social (reputation, recognition, community status) and the financial reward a consequence of social standing, not a substitute for it.** Money should follow reputation, not replace it.

### The Participation Ratio Challenge

Wikipedia's 0.003% super-contributor ratio is extreme. CrowdForge can improve on it by:

1. **Starting small** -- small communities naturally have higher participation rates (up to 33%)
2. **Making contribution the default** -- lower the floor to reactions, votes, feedback before asking for original creation
3. **Creating interdependence** -- when your project needs others' input, more people engage
4. **Visible impact** -- show contributors the downstream effect of their work in real-time
5. **Progressive skill building** -- create clear paths from "commented on a project" to "led a startup build"

### The Governance Blueprint

Drawing from Ostrom + Wikipedia:

1. **Community-created rules** -- let early contributors shape the norms, then codify
2. **Graduated authority** -- earn privileges through demonstrated behavior, not credentials
3. **Graduated sanctions** -- proportional responses to violations, not bans
4. **Transparent monitoring** -- community members monitor each other, not a corporate team
5. **Nested governance** -- project-level autonomy within platform-wide principles
6. **Conflict resolution pipeline** -- discussion -> mediation -> arbitration, with each step more formal
7. **Protect the right to fork** -- if a sub-community disagrees with platform direction, they can take their work and go. This keeps the platform honest.

---

## Sources

- [How Did They Build the Free Encyclopedia? -- ACM Transactions on CHI](https://dl.acm.org/doi/10.1145/3617369)
- [History of Wikipedia](https://en.wikipedia.org/wiki/History_of_Wikipedia)
- [Wikipedia: A Self-Organizing Bureaucracy -- Taylor & Francis](https://www.tandfonline.com/doi/full/10.1080/1369118X.2021.1994633)
- [Wikipedia Governance -- P2P Foundation](https://wiki.p2pfoundation.net/Wikipedia_-_Governance)
- [Wikipedia: Quality Control](https://en.wikipedia.org/wiki/Wikipedia:Quality_control)
- [Wikipedia: Administration](https://en.wikipedia.org/wiki/Wikipedia:Administration)
- [Deletionism and Inclusionism in Wikipedia](https://en.wikipedia.org/wiki/Deletionism_and_inclusionism_in_Wikipedia)
- [Motivations of Wikipedia Content Contributors -- ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0747563210000877)
- [The Emerging Neuroscience of Intrinsic Motivation -- PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC5364176/)
- [Intrinsic and Extrinsic Motivation from SDT Perspective -- ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0361476X20300254)
- [Wikipedia Barnstars](https://en.wikipedia.org/wiki/Wikipedia:Barnstars)
- [Uncovering Valued Work in Wikipedia through Barnstars -- UBC](https://www.cs.ubc.ca/~bestchai/papers/cscw2008.pdf)
- [Wikipedia Editor Retention](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_Editor_Retention)
- [Why Wikipedia Is Losing Contributors](https://en.wikipedia.org/wiki/Wikipedia:Why_is_Wikipedia_losing_contributors_-_Thinking_about_remedies)
- [Fandom (website) -- Wikipedia](https://en.wikipedia.org/wiki/Fandom_(website))
- [Fandom and the Multimillion Dollar Business of Monetizing Volunteer Work](https://frisk.space/posts/fandom-and-the-multimillion-business-of-monetizing-volunteer-work/)
- [To What Extent Does Fandom Act as a Model for Labor Exploitation?](https://www.jsr.org/hs/index.php/path/article/download/1237/500/4663)
- [The Monetization Backlash: How Fandom Sites Are Losing Community Trust](https://thegameofnerds.com/2025/11/15/the-monetization-backlash-how-fandom-wiki-sites-are-losing-community-trust/)
- [You Don't Understand Why Wikis Are Leaving Fandom](https://medium.com/@lindenclayton/you-dont-understand-why-wikis-are-leaving-fandom-6378372ad06e)
- [Meta-Analytic Review: Effects of Extrinsic Rewards on Intrinsic Motivation -- Deci et al.](https://pubmed.ncbi.nlm.nih.gov/10589297/)
- [Motivation Crowding Theory -- Wikipedia](https://en.wikipedia.org/wiki/Motivation_crowding_theory)
- [Acceptance of Monetary Rewards in Open Source -- ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0048733313001868)
- [Paid vs Volunteer Open Source: Study of the Rust Project](https://arxiv.org/html/2401.13940v1)
- [Participation Inequality: The 90-9-1 Rule -- Nielsen Norman Group](https://www.nngroup.com/articles/participation-inequality/)
- [1% Rule -- Wikipedia](https://en.wikipedia.org/wiki/1%25_rule)
- [The Wealth of Networks -- Yochai Benkler](https://en.wikipedia.org/wiki/The_Wealth_of_Networks)
- [Commons-Based Peer Production -- Wikipedia](https://en.wikipedia.org/wiki/Commons-based_peer_production)
- [Two Key Steps in the Evolution of Human Cooperation -- Tomasello](https://www.journals.uchicago.edu/doi/10.1086/668207)
- [The Ultra-Social Animal -- Tomasello 2014](https://onlinelibrary.wiley.com/doi/full/10.1002/ejsp.2015)
- [Origins and Psychology of Human Cooperation -- Harvard](https://projects.iq.harvard.edu/sites/projects.iq.harvard.edu/files/culture_cognition_coevol_lab/files/annurev-psych-081920-042106.pdf)
- [Elinor Ostrom -- Wikipedia](https://en.wikipedia.org/wiki/Elinor_Ostrom)
- [Ostrom's Eight Design Principles -- Agrarian Trust](https://www.agrariantrust.org/ostroms-eight-design-principles-for-a-successfully-managed-commons/)
- [Governing the Commons -- Cambridge University Press](https://www.cambridge.org/core/books/governing-the-commons/7AB7AE11BADA84409C34815CC288CD79)
- [Wikipedia Statistics 2025 -- StatsUp](https://analyzify.com/statsup/wikipedia)
- [Guide to Requests for Adminship](https://en.wikipedia.org/wiki/Wikipedia:Guide_to_requests_for_adminship)
