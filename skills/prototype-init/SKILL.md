---
name: prototype-init
description: Scaffold a local static prototype site and launch it at localhost:3000. Creates the directory structure that design-wireframes and other prototyping skills write into. Trigger when the user says "prototype-init", "scaffold the prototype", "set up the prototype site", wants to start rapid prototyping from a PRD, or is about to invoke design-wireframes for the first time on a project. Also trigger proactively when a PRD is approved and downstream wireframe/visual design work is about to begin and no `prototype/` directory exists yet.
---

# Prototype Init

## What This Does
Creates a minimal static-site scaffold in `prototype/` — HTML + a single `tokens.css` file, served by Python's stdlib HTTP server — and launches it at `http://localhost:3000`. Styling comes from Tailwind v4 loaded via the browser CDN (`@tailwindcss/browser@4`); design tokens live in `tokens.css` as a `@theme` block, which Tailwind picks up automatically. Downstream skills (`design-wireframes`, later visual-style and hi-fi skills) write artifact files into this scaffold; `prototype-update` regenerates the landing page to list whatever artifacts exist.

The scaffold is deliberately stack-less. No npm, no package.json, no build step. Tailwind via CDN gives every artifact polished defaults and a complete utility library; `tokens.css` lets the user (via `design-themes`) re-theme everything by editing one file. The "launch in 5 seconds" promise survives because nothing has to be installed.

## When to Run This
- Starting a new prototyping session from a PRD
- Before invoking `design-wireframes` or other artifact-producing skills — they assume the scaffold exists and write into its subdirectories

If `prototype/` already exists, do not overwrite. Ask the user whether they want to keep the existing scaffold (common — they already have artifacts in it) or start fresh. Overwriting silently will destroy work.

## Scaffold Structure
```
prototype/
├── index.html       # landing page with grouped links to artifacts
├── tokens.css       # @theme block — single source of truth for design tokens
├── prd/             # PRD renders
├── cujs/            # CUJ flow pages (Mermaid + step text)
├── wireframes/      # lofi wireframe pages (one per screen)
├── styles/          # style-token previews
└── hi-fi/           # high-fidelity pages
```

All artifact links on the landing page use `target="_blank"` so artifacts open in new tabs. This gives CSS isolation for free (a wireframe's classes can't leak into the launcher chrome) and keeps the launcher stable across navigation.

Every HTML file in the scaffold pulls in Tailwind via the same two lines in `<head>`:

```html
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
<style type="text/tailwindcss">@import "/tokens.css";</style>
```

The browser script reads the `@theme` block from `tokens.css` and generates utility classes on the fly. Swap `tokens.css` and every page re-themes on next refresh — no rebuild needed.

## Steps

### 1. Check for existing scaffold
Run `test -d prototype/`. If it exists, ask the user whether to keep it (stop here), replace it (move to step 2, but confirm destructive action first), or scaffold under a different name.

### 2. Copy scaffold files
From this skill's `assets/` directory into the user's project:
- `assets/index.html` → `prototype/index.html`
- `assets/tokens.css` → `prototype/tokens.css`

Then create the empty artifact subdirectories: `prototype/{prd,cujs,wireframes,styles,hi-fi,components}/`.

The default `tokens.css` ships a neutral monochrome theme so wireframes look reasonable on first run. The `design-themes` skill replaces this file with a custom theme later.

The `index.html` shipped here is a placeholder that tells the user to run `/prototype-update`. Step 6 below should run that automatically so the user lands on a populated launcher.

### 3. Check if port 3000 is free
Run `lsof -i :3000`. If something is bound:
- If it's an old `python3 -m http.server` from a previous session (check `prototype/.server.pid` if present), ask the user whether to stop it and restart.
- Otherwise, ask the user which port to use instead.

Don't kill processes without asking — the bound process might be something the user cares about.

### 4. Launch the server in the background
```bash
nohup python3 -m http.server 3000 --directory prototype/ > prototype/.server.log 2>&1 &
echo $! > prototype/.server.pid
```

The PID file lets a future session (or a shutdown command) stop the right process. The log file captures request traffic for debugging.

### 5. Run `prototype-update` once to populate the launcher
The static placeholder `index.html` shipped in step 2 just tells the user to run `/prototype-update`. Run it now so the user lands on a populated launcher with the proper sidebar (Product Definition, CUJs, Design):

```bash
python3 ~/.claude/skills/prototype-update/scripts/regenerate.py prototype/
```

If artifacts already exist in the subdirectories, they show up immediately. If not, sections show "— none —" or counts of 0 — still useful as a navigable shell.

### 6. Report to the user
Tell them:
- The URL (`http://localhost:3000`)
- The next logical step (`/design-wireframes` to add wireframes, or drop PRD/CUJ content into `prototype/prd/` and `prototype/cujs/` manually)
- That they should run `/prototype-update` after adding artifacts to refresh the launcher

## Shutdown
If the user wants to stop the server:
```bash
kill $(cat prototype/.server.pid) 2>/dev/null && rm -f prototype/.server.pid
```

Don't run this as part of `prototype-init` — surface it as a one-liner when asked.

## Why These Choices
- **Python's `http.server` over Node/Vite/etc.** — Python 3 ships with macOS; npm tools require install + version management. Zero dependencies wins for a rapid-prototyping tool.
- **Tailwind v4 via CDN, not npm** — Tailwind's browser bundle (`@tailwindcss/browser@4`) reads `@theme` blocks at runtime and generates utilities on the fly. We get the entire utility library and a tested type/spacing/color foundation without a build pipeline. Cost is ~50KB of JS per page and an internet connection — both acceptable for local prototyping.
- **`tokens.css` as the only theming surface** — every HTML file `@import`s the same file inside its inline `<style type="text/tailwindcss">` block. One file, every page re-themes. Means `design-themes` only ever rewrites one file, and skills writing wireframes never make style decisions.
- **`target="_blank"` for artifact links** — each artifact is a standalone document. Opening in a new tab means the artifact's classes live in their own document context and can't leak into the launcher, and the user can tile multiple wireframes side-by-side when comparing.
- **Flat directory structure** — one subdirectory per artifact type. No nesting, no manifest file. `prototype-update` rescans these directories to regenerate the landing page.
