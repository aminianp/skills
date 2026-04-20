---
name: implementation-brief
description: Convert an approved PRD into a developer-ready implementation brief. Use when a PRD is marked Ready and needs to be handed off to engineering. Trigger when the user mentions "implementation brief", "dev brief", "hand off to engineering", or when a PRD is approved and the next step is building.
---

# Implementation Brief

## What This Does
Translates an approved PRD into a structured brief that engineering can act on without reading the full PRD — with explicit scope, testable acceptance criteria, and open questions that would block implementation surfaced upfront.

## Input Requirements
- An approved PRD (marked `Ready` or equivalent signoff)
- Optionally: tech stack, team structure, known constraints, target timeline

If the PRD isn't marked as approved, flag it and ask whether to proceed anyway.

## Ask Before Writing
Ask only for what's genuinely missing from the PRD:
1. Are there technical constraints not covered? (e.g., must use the existing auth system, can't modify the payments service)
2. Who is the intended engineering audience — one engineer, a squad, a specific team?
3. Is there a target timeline or milestone this needs to fit?

Don't ask for information the PRD already contains.

## Brief Structure

### Header
- PRD title, version, and approval date
- Date brief was written and last synced with PRD

### Problem Summary
2-3 sentences synthesizing what's being solved and why it's being built now. Reference the PRD problem statement but don't copy-paste — a brief that just restates the PRD adds no value.

### Scope
**In scope** — concrete list of what's being built

**Out of scope** — explicit non-goals from the PRD, plus anything the user journeys might imply but shouldn't be built. Unstated non-goals are a primary source of scope creep; make them explicit.

**Critical user journeys** — reference by name from the PRD, don't rewrite them here

### Acceptance Criteria
Testable conditions that define done. One per deliverable. Format:
> Given [context], when [action], then [observable outcome]

Only write acceptance criteria for things in scope. Writing criteria for out-of-scope items is a common way scope creep enters through the back door.

### Architecture & Integration Notes
Only include what's known from the PRD or explicitly provided by the user:
- External systems touched
- Data flows or storage requirements stated in the PRD
- Hard constraints the user mentioned

Leave this section sparse if the PRD doesn't address architecture. Don't invent it.

### Open Questions
Questions the brief exposes that would block implementation if left unresolved:
- PRD ambiguities engineering will hit in sprint planning
- Decisions the PRD deferred that now need answers
- Dependencies on other teams or systems

Prioritize by urgency: what must be resolved before work starts vs. what can be decided during implementation.

### Success Metrics (reference)
Pull the north star metric and primary tracking metrics from the PRD verbatim. Engineering needs to know what they're instrumenting for before they write the first line of code.
