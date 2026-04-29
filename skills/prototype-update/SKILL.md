---
name: prototype-update
description: Rescan the prototype directory and regenerate the launcher page (index.html) so it lists whatever artifacts currently exist. Trigger when the user says "prototype-update", "refresh the prototype", "rescan prototypes", "the launcher is stale", after wireframes/styles/hi-fi pages have been added or renamed, or when a prototyping skill has just written new files. Trigger proactively at the end of any skill invocation that adds or removes files under `prototype/wireframes/`, `prototype/cujs/`, `prototype/styles/`, `prototype/hi-fi/`, or `prototype/prd/`.
---

# Prototype Update

## What This Does
Scans the artifact subdirectories under `prototype/` and rewrites `prototype/index.html` so the launcher page reflects what's actually there. Each `.html` file in `prd/`, `cujs/`, `wireframes/`, `styles/`, and `hi-fi/` becomes a link, displayed using the file's `<title>` (with a fallback to the filename stem).

The work is done by `scripts/regenerate.py` — a small standalone Python script with no dependencies beyond stdlib. The script is the source of truth for launcher format; this skill's job is to know when to invoke it and how to handle the edges.

## When to Run
- After `design-wireframes` (or any future artifact-producing skill) writes files
- After the user manually adds, renames, or removes files in any artifact directory
- When the launcher page looks stale

If `prototype/` doesn't exist yet, do not run this skill. Direct the user to `/prototype-init` first.

## How to Run
From the user's project root:

```bash
python3 <skill-path>/scripts/regenerate.py prototype/
```

Where `<skill-path>` resolves to this skill's directory (e.g., `~/.claude/skills/prototype-update/`).

The script accepts an optional positional argument — the path to the prototype directory. It defaults to `./prototype`. Running from the project root with no argument is the common case.

## What Gets Included
- Top-level `.html` files in each artifact subdirectory
- Display name comes from the file's `<title>` tag, falling back to the filename stem (e.g., `signup.html` → "signup")
- Files are sorted alphabetically within each section

## What Gets Skipped
- Non-HTML files (`.md`, `.json`, `.png`, etc.) — silently ignored
- Files in nested subdirectories — only the top level of each artifact directory is scanned
- Hidden files and the `.server.pid` / `.server.log` files left by `prototype-init`

If the user wants markdown PRD files rendered, that's a separate skill's job (a future `prd-render` would convert `.md` to `.html` and drop the result into `prd/`, where this skill would then pick it up).

## What This Skill Does Not Do
- Restart the server — `python3 -m http.server` watches the filesystem and serves the new index.html on the next request, so a restart is unnecessary.
- Validate the wireframes themselves — broken HTML in a wireframe is the artifact-producing skill's responsibility.
- Track history — if a wireframe is deleted, its link disappears. There's no archive.

## Why This Is a Script, Not Inline Agent Work
Regenerating the launcher is deterministic, runs every time a skill adds files, and benefits from being byte-identical across invocations. A bundled script gives downstream skills (`design-wireframes`, future style/hi-fi skills) a one-line shell command to call after they finish writing files — no agent reasoning required, no token spend, no drift in the launcher format.

## Why No Manifest File
An earlier version of this design used a `manifest.json` that every skill updated when adding artifacts. This created two problems: skills had to remember to update it (they sometimes wouldn't), and concurrent agents would conflict on the file. Filesystem rescanning at update time avoids both — the disk is the source of truth, and this script is the only thing that reads it.
