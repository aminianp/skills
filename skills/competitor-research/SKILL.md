---
name: competitor-research
description: Research competitors through a structured interview and synthesize findings into a competitive landscape. Use whenever mapping a market, evaluating differentiation, or understanding how competitors address a specific JTBD — even if the user only mentions "competitors", "what else is out there", or wants market context before writing a PRD. Trigger proactively if the user is starting a PRD and hasn't done competitive research yet.
---

# Competitor Research

## Step 1: Product Interview
Before researching anything, ask the user for any of the following that hasn't already been provided:

1. Are there specific companies or products you already want researched?
2. What is the JTBD your product serves?
- Skip this step if user has provided a PRD with JTBDs either in the conversation or in the project directory. If the user has provided a PRD but it's unclear which JTBDs are most relevant to the research, ask: "Which JTBDs are most important to focus on for this research?"
3. Which product lines or features are most relevant to compare?
4. Any competitors, products, markets, geographies, or segments to exclude?
5. What is your company's stage and approximate size? (This is needed to tier competitors relative to your position)
6. What dimensions should be researched and to what end? Here are some examples for reference:
- Analyze how the aforementioned JTBDs are served by competitors to identify underserved customer needs
- Comparing product lines and features to find opportunities for differentiation
- Analyze how each competitor positions their product to find opportunities for differentiated messaging/positioning
- Understand how each competitor prices their product to establish a baseline for our own pricing
- Identify and size market segments, and where each competitor plays to find a market for our own products

This is not an exhaustive list and the user may choose more than one research objective!

Skip questions already answered in the conversation or an accompanying PRD. Wait for responses before proceeding.

**The interview answers directly shape what gets researched and how the output is structured.** A pricing-focused goal means the competitor table leads with pricing detail and tiers; a differentiation goal means strengths, weaknesses, and the differentiation map take priority. Adapt accordingly rather than producing the same output regardless of goal.

## Step 2: Expand the Competitor List
Don't limit research to only the competitors the user named — they may not know who else is in the space. Identify additional candidates:

- **Direct competitors** — Companies with similar products targeting the same JTBD and customer segment (e.g., Pepsi is a direct competitor to Coca-Cola)
- **Indirect competitors** — Companies with alternative solutions to the same JTBD, even if they look different on the surface (e.g., bottled water is an indirect competitor to soda for quenching thirst)

Tell the user which additional competitors you're adding and why before researching them. If the list would grow large (more than 5 companies or alternatives), ask the user to prioritize rather than researching everything. Do not start researching competitors until you have a short-list or a prioritized list from the user.

## Step 3: Research Each Competitor
For each competitor, find the fields most relevant to the stated research goal. Here are the default values, but adapt based on research goals stated in the user interview:

- **Product**: core offering, key features, what JTBD it addresses
- **Positioning**: how they describe themselves, who they target
- **Pricing**: model and tiers if public
- **Strengths**: what they do demonstrably well
- **Weaknesses**: documented gaps, user complaints, known limitations
- **Recent moves**: launches, pivots, funding, partnerships

Also note each competitor's **stage and size** (established/large, similar to user, emerging) — this feeds the Competitive Landscape Map in the output.

Use web search where available. Attach a confidence level to every claim based on source type — since you retrieved the information, you know exactly where it came from:

- `High` — from official sources (product page, press release, SEC/regulatory filing)
- `Medium` — from reputable third-party coverage (press, analyst reports)
- `Low` — inferred or from user-generated sources (reviews, forums, social)

## Output Format
Produce a structured landscape adapted to the research goal from the interview. Default structure:

1. **Competitive Landscape Map** — a matrix showing each competitor tiered by stage/size (established, peer, emerging) and mapped to the market segment they primarily serve. Gaps in the matrix are as informative as the filled cells — they show where no one is playing.
2. **Competitor table** — one row per competitor, columns weighted toward the research goal
3. **Differentiation map** — where the user's product has an advantage, parity, or gap relative to the field
4. **Strategic observations** — patterns across the landscape relevant to the stated research goal
5. **Research gaps** — what couldn't be found and why it might matter

Include these caveats inline where relevant, not as a footnote:
- Internal roadmaps, true retention rates, and real margins are almost never public — flag when a conclusion requires this kind of inside knowledge
- Competitive landscapes shift fast; date-stamp findings and flag anything that may be stale
- This research is best for landscape mapping and differentiation angles, not a substitute for primary customer research or analyst intelligence
