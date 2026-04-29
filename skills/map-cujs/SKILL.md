---
name: map-cujs
description: Convert high-level CUJs provided in chat or in a PRD to detailed flow maps. Work with the user to expand the generated flows into ones with happy paths and failure branches, then analyze them for optimization opportunities. Trigger when the user mentions CUJs, user flows, journey maps, Mermaid diagrams for flows, or is preparing to hand off to design. Also trigger proactively when a PRD containing CUJs is approved and the next step is design handoff, or when the user is mapping out failure modes for a flow they've already sketched.
metadata:
  tags:
    - "product skills"
    - "CUJs"
    - "user flows"
    - "journey mapping"
    - "flow optimization"
---

# Map CUJs

This skill runs in three stages with a required human review gate between them. The first stage expands CUJs into detailed flows and produces Mermaid diagrams. The second stage reviews the flows with the user and expands them into happy paths and failure branches. The third stage analyzes the expanded flows for optimization opportunities. Each stage requires explicit user approval to proceed to the next, as the expansions and optimizations involve judgment calls about product behavior that the user must confirm reflect reality.

## What a CUJ Actually Is

A CUJ describes how a specific persona accomplishes a specific Job To Be Done. It is **not** a forward pass through your product's UI. The most common failure of agent-generated CUJs is producing a click trail that looks like a journey but tells you nothing about whether the user got value.

### Bad CUJ — a click trail
> 1. User clicks Work in nav
> 2. Lands on work page
> 3. Scrolls through experience
> 4. Clicks LinkedIn

This is a UI walkthrough disguised as a journey. The user could complete every step and still not have accomplished anything meaningful.

### Good CUJ — job-anchored
> **JTBD:** Recruiter wants to assess if the candidate is a fit for the role they're hiring for, in under two minutes (PRD §2 P0).
> **Persona:** Recruiter / hiring manager
> **Trigger:** Recruiter is sourcing candidates for [role]; finds the candidate's name through LinkedIn / referral / search.
>
> **Steps:**
> 1. Recruiter arrives at the site (direct or referral)
> 2. Tries to identify quickly: who is this person, what's their domain
> 3. Looks for evidence of fit — does experience match the role's requirements (years, scope, domain)?
> 4. Forms a verdict: yes / no / maybe
> 5. If yes/maybe: captures evidence (LinkedIn, resume) for further screening
>
> **Outcome:** Recruiter has a verdict and the evidence to act on it. Time elapsed: under 2 minutes.

The Good version describes what the user is trying to figure out, decide, and walk away with. UI clicks are inferred from those goals — not the other way around.

### Required for every CUJ

- **Cite the JTBD by reference.** Quote or paraphrase the JTBD text, name the persona, and link to the PRD section/line where it's defined. If the PRD lists JTBDs without explicit links to CUJs, surface that mapping gap to the user (see "When the PRD lacks anchors" below).
- **Trigger.** What made the user start this job? Without a trigger, you can't reason about realistic entry conditions or referrer/UTM context.
- **Steps describe user intent**, not UI mechanics. "Looks for evidence of fit" is a step. "Clicks LinkedIn" is an action that may or may not happen depending on what the user finds.
- **Outcome.** Did the JTBD get satisfied? An outcome statement closes the loop and gives Stage 2 (failure branches) something concrete to negate.

### When the PRD lacks anchors

Two common gaps:

1. **A JTBD has no corresponding CUJ.** The PRD signals intent to serve a job but never describes how. Don't invent a CUJ to fill the hole — flag the coverage gap to the user. The fix is updating the PRD, not papering over it.
2. **CUJs exist but don't reference JTBDs.** The mapping is implicit. Surface this as a critique: ask the user which JTBD each CUJ serves, and recommend they update the PRD to make the link explicit.

Don't proceed to mapping until each CUJ you're going to draw has a JTBD anchor. CUJs without anchors drift away from user value within a single iteration.

## Step 1: Journey Mapping
Read high-level CUJs from a PRD (either linked in chat or provided as a file in the project directory). For each CUJ in the PRD, confirm its JTBD anchor (per "What a CUJ Actually Is" above) before drawing the flow. If the PRD's CUJ section is missing JTBD references, pause and surface the gap before continuing.

Convert each anchored CUJ to a flow map with the happy path only. If no PRD is available, ask the user to describe the CUJ they want to map — but still require a JTBD and persona before drawing anything. Work through one flow at a time. The output of this stage is a set of flow descriptions and Mermaid diagrams that represent the happy path for each CUJ, with the JTBD/persona/trigger/outcome captured alongside the diagram.

## Step 2: Flow Expansion
Present the generated flows to the user for review. Work with them to expand each flow with plausible failure branches:

- Prompt the user to identify potential failure points in the flow
- Ask for possible context switches between tools and/or windows that could cause drop-off
- For each failure point, ask the user to describe how the system should respond to recover from this failure state.

Use this information to update the flow descriptions and Mermaid diagrams to include these branches. The goal is to create a comprehensive map of the user journey that accounts for both ideal and non-ideal scenarios.

## Step 3: Analysis and Optimization
Once the user has approved the expanded flows, analyze them for optimization opportunities. Analyze the flows through the following lenses:

**Context switches** — steps where the user must leave the product and return (e.g., check email, open another tool, copy from another system). Flag each one and note whether it's avoidable.

**Redundant steps** — actions that don't materially advance the user toward completing the JTBD. A step is redundant if removing it wouldn't break the flow or reduce quality of outcome.

**Memory burden** — steps where the user must recall something from an earlier step without system support (e.g., copy a value, remember a setting, re-enter information already provided).

**Dead ends** — branches with no recovery path. The user is stuck with no clear next action.

**Step count vs. JTBD complexity** — if the flow has significantly more steps than the JTBD warrants, flag it. Simple JTBDs with long flows usually signal UX debt or missing abstractions.

Work with the user to reduce friction, eliminate redundant steps, and improve the overall user experience. Once optimizations are identified, update the flow descriptions and Mermaid diagrams to reflect the proposed changes. The final output should be a set of optimized user journey maps that can be shared with design and engineering for implementation.

## Mermaid Diagram Guidelines
Produce one Mermaid flowchart per CUJ using `graph TD` (top-down). Apply consistent styling using `classDef` so the diagrams are readable and visually calm.

**Color palette — use only these four node types:**

```
classDef default fill:#f0f0f0,stroke:#999999,color:#1a1a1a
classDef happy fill:#d6e4f0,stroke:#7aafcf,color:#1a1a1a
classDef branch fill:#f0e0d6,stroke:#cf9a7a,color:#1a1a1a
classDef decision fill:#f5f5dc,stroke:#b8b870,color:#1a1a1a
```

- `default` — start/end nodes and neutral steps
- `happy` — steps on the primary success path (muted blue)
- `branch` — failure or alternative path steps (muted amber)
- `decision` — decision points / forks (muted yellow)

**Styling rules:**
- All text dark (`#1a1a1a`) on light backgrounds — never use bright or saturated fills
- Edge lines use the default Mermaid gray; don't override line color unless a branch needs a label
- Label decision edges with brief conditions (`yes/no`, `found/not found`, etc.)
- Keep node labels to one short phrase — detail belongs in the written flow description, not the diagram

## Optimization Output Format
For each CUJ:
1. **Flow summary** — one sentence on what the flow does and how complex it is
2. **Findings** — bulleted list of issues found, organized by lens, each with the specific step(s) involved
3. **Recommendations** — specific, actionable suggestions (not redesigns — flag the problem and suggest a direction)
4. **Optimization score** — `Clean` / `Minor issues` / `Needs rework`
