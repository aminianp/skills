---
name: prototype-status
description: Report the current state of a prototype project — which artifacts exist in each stage (PRD, CUJs, theme, wireframes, prototypes, components), which are approved/selected via the manifest, and what the next step is. Trigger when the user says "where am I", "where are we", "project status", "/prototype-status", "what's done", "what's left", "summarize the project", or when picking up a project after a break and needing to orient. Also trigger proactively at the start of a fresh conversation on an existing prototype project.
---

# Prototype Status

## What This Does

Reads `prototype/APPROVED` + scans the artifact directories and prints a one-screen Markdown report: render target, per-stage status (with what's approved vs. what just exists), an inventory of every artifact (with approval markers), and a suggested next step. Designed for orienting at the start of a session, picking up after time away, or quick "where are we" check-ins.

This skill replaces the awkward dance of opening five files and the launcher to figure out project state.

## Pipeline

- **Reads from**: `prototype/APPROVED`, `prototype/{prd,cujs,styles,wireframes,hi-fi,components}/`, `prototype/tokens.css`
- **Writes nothing.** Read-only.
- **Suggests next**: depending on which gap is biggest, points the user at `prd-crit`, `map-cujs`, `design-themes`, `design-wireframes`, `design-prototypes`, `design-components`, or `implementation-brief`.

## How to Run

From the project root:

```bash
python3 ~/.claude/skills/prototype-status/scripts/status.py prototype/
```

Default argument is `./prototype`, so omitting it works when run from the project root.

The output is Markdown. Pipe it to a file or paste it into the conversation.

## What Gets Reported

1. **Render target** &mdash; from the manifest's `target:` line. Defaults to `web-spa` notation if unset.
2. **Pipeline table** &mdash; one row per stage. Each row shows:
   - `✓ <approved value>` if the stage's manifest key is set
   - `⚠ exists, not approved` if files are present but no approval line
   - `— not started` if the directory is empty and no manifest line
3. **Approval manifest** &mdash; the raw key:value pairs, in the order they appear in APPROVED.
4. **Inventory** &mdash; every artifact file across the six artifact directories, with the `<title>` extracted, and a marker pointing back to the manifest key when approved.
5. **Suggested next step** &mdash; the first gap detected (e.g., "approve CUJs", "start wireframes"). When everything is approved, suggests `implementation-brief`.

## Iteration

This skill is read-only. No iteration concerns.

## When NOT to Run

- The project hasn't been initialized yet (`prototype/` doesn't exist) &mdash; run `prototype-init` first.
- You already know the state and just want to do work &mdash; this is for orientation, not for everyone-runs-it-every-time.

## Why a Script and Not Inline Agent Work

Reading the manifest + scanning six directories + extracting titles is deterministic and benefits from being byte-identical across invocations. A script gives a one-line shell command for any other skill to call (e.g., `prototype-init` could run it after scaffolding to confirm). It's also faster and cheaper than parsing files in-conversation.
