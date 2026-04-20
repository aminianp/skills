---
name: map-cujs
description: Convert high-level CUJs provided in chat or in a PRD to detailed flow maps. Work with the user to expand the generated flows into ones with happy paths and failure branches, then analyze them for optimization opportunities. Trigger when the user mentions CUJs, user flows, journey maps, or is preparing to hand off to design.
metadata:
  tags:
    - "product skills"
    - "CUJs"
    - "user flows"
    - "journey mapping"
    - "flow optimization"
---

# Map CUJs

This skill runs in three stages with a required human review gate between them. The first stage expands CUJs into detailed flows and produces Mermaid diagrams. The second stage reviews the flows with the user and expand them into happy paths and failure branches. The third stage analyzes the expanded flows for optimization opportunities. Each stage requires explicit user approval to proceed to the next, as the expansions and optimizations involve judgment calls about product behavior that the user must confirm reflect reality.

## Step 1: Journey Mapping
Read high-level CUJs from a PRD (either linked in chat or provided as a file in the project directory) and convert to flow maps with the happy path only. If no PRD is available, ask the user to describe the CUJ they want to map — in this case, work through one flow at a time. For example, a CUJ like "User wants to onboard to the product" is too high-level to map directly — it needs to be broken down into specific steps the user takes and how the system responds. The output of this stage is a set of flow descriptions and Mermaid diagrams that represent the happy path for each CUJ.

## Step 2: Flow Expansion
Present the generated flows to the user for review. Work with them to expand each flow with plausible failure branches:

- Prompt the user to identify potential failure points in the flow
- Ask for possible context switches between tools and/or window that could cause drop-off
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
