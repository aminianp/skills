---
name: journey-writer
description: Generate step-by-step user journeys from approved JTBDs. Use when finalized JTBDs need to be translated into concrete user flows before design or engineering handoff. Trigger when the user mentions user journeys, user flows, or wants to map out how a user accomplishes a goal. Also trigger proactively when a PRD is approved and the next logical step is translating JTBDs into flows.
---

# Journey Writer

## Step 1: Interview
Before generating anything, ask for any of the following that hasn't already been provided:

1. Which JTBD(s) should be expanded into journeys?
2. Which persona is each journey for?
3. What product context is needed to make steps realistic? (what's already built, what's new, relevant constraints)

Skip questions already answered in the conversation or an accompanying PRD. If JTBDs are present but not yet approved, flag it — journeys built on draft JTBDs will change as the JTBDs change, which creates rework downstream. Ask the user to confirm they want to proceed anyway.

## Journey Structure
Produce one section per JTBD:

```
## [JTBD statement]
**Persona:** [name]
**Entry point:** [how they realistically arrive at this task]

### Happy Path
1. [step]
2. [step]
...

### Failure States
- **[Failure name]:** [what triggers it] → [what the user experiences] → [recovery path]

### Open Questions
- [decision the journey exposes that isn't answered by the JTBD or PRD]
```

## Happy Path Guidelines
- Start with a realistic entry point — not "user opens the app" but how they actually arrive at this specific task in practice
- Each step should describe a user action and what happens as a result
- Keep granularity useful: specific enough for design and engineering, not so detailed it describes visual layout
- End with what success looks like for the user, not just system completion

## Failure States Guidelines
Identify 2-3 failure states worth designing for per journey — not every possible error. Prioritize:
- Failures most likely to occur at scale
- Failures most damaging to the user if unhandled
- Failures that require a product decision (not just an error message)

The goal is to surface decisions that need to be made before design starts, not to enumerate every edge case — that's an engineering concern.

## Open Questions Guidelines
Flag decisions the journey exposes that aren't resolved by the existing PRD:
- Edge cases requiring a product decision before design can proceed
- Places where the journey assumes something not yet defined
- Conflicts between this journey and another JTBD's journey

## Quality Check Before Returning
- Does every step connect to the JTBD? Remove steps that don't.
- Is the entry point how users actually arrive — or how the team wishes they'd arrive?
- Does the happy path resolve the JTBD, not just complete a task flow?
- Do failure states have real recovery paths, not just error screens?
