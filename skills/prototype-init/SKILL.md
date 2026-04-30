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
├── index.html       # SPA launcher: header, sidebar nav, main pane (welcome / iframe / list)
├── tokens.css       # @theme block — human-readable source of truth for design tokens
├── prd/             # Product Definition: PRD, FAQ, Decision Log (each as a markdown wrapper)
├── cujs/            # CUJ flow pages (Mermaid + step text + JTBD anchor block)
├── wireframes/      # lofi wireframe pages (per-screen, opens in new tab from launcher)
├── styles/          # style-token preview pages (opens inline)
├── hi-fi/           # interactive prototypes (one HTML per variant; opens in new tab from the "Prototypes" sidebar item)
└── components/      # component library pages (opens inline)
```

## Opinionated launcher

The launcher (`index.html`) is **not** a generic file list. It's a single-page app shell with three views:

- **Welcome view** — shown initially; brief intro to the three sidebar sections
- **Page view** — iframe rendering an inline artifact (PRD, FAQ, CUJ, Style, Component)
- **List view** — for design containers (Wireframes, Styles, Prototypes, Components); shows the items inside one container, click opens (inline or new-tab depending on the container's mode)

The sidebar is grouped into three standard sections: **Product Definition**, **CUJs**, **Design**. These are the same across every project; only the items inside them change. A "Close ✕" appears in the launcher's top header whenever an artifact is loaded, so the user can always get back to the welcome view.

### Where the launcher template lives

The launcher is generated, not handwritten. Two artifacts together produce it:

- **`prototype-update/scripts/regenerate.py`** — the canonical generator. Holds the `SIDEBAR_SECTIONS` constant (where you customize per-project section/item layout), the inlined HTML template (header + sidebar + 3 views + footer), and the SPA JavaScript (click handlers, view switching, `Close ✕` behavior). Run this whenever artifact files change.
- **`prototype-init/assets/index.html`** — a static snapshot of the empty-state launcher (what `regenerate.py` produces against an empty `prototype/`). Copied during init as a placeholder so the user can see the shell immediately, and overwritten by the first run of `regenerate.py`.

If you need to change the launcher's structure, edit `regenerate.py` and regenerate the static snapshot via:

```bash
tmp=$(mktemp -d) && mkdir -p "$tmp/prototype/{prd,cujs,wireframes,styles,hi-fi,components}" \
  && python3 ~/.claude/skills/prototype-update/scripts/regenerate.py "$tmp/prototype/" \
  && cp "$tmp/prototype/index.html" ~/.claude/skills/prototype-init/assets/index.html \
  && rm -rf "$tmp"
```

### Inline `@theme` (not `@import`)

Every HTML file inlines its own copy of the `@theme` block between `/* @theme:start */` and `/* @theme:end */` markers. This is because the Tailwind v4 browser CDN does not resolve `@import` to external files inside its tagged `<style>` blocks. `tokens.css` remains the canonical source; `design-themes`'s `apply_theme.py` script propagates token changes to every HTML file. Anything you create in the prototype tree should keep these markers so it stays themeable.

### Inline-vs-newtab behavior

- Product Definition + CUJs + Styles + Components → click opens **inline** (in the launcher's iframe)
- Wireframes + Prototypes → click opens in a **new tab** (full-page artifacts deserve full-tab focus; interactive prototypes own their full viewport)

This is configured per item in `SIDEBAR_SECTIONS` in `regenerate.py`.

## Pipeline

- **Reads from**: nothing &mdash; this is the entry point of the toolchain
- **Produces**: scaffolded `prototype/` directory tree, empty APPROVED manifest, default tokens.css, frame templates, design-guidelines reference, and a placeholder launcher
- **Feeds out to**: every other prototype skill consumes this scaffold

## Iteration

This skill is run **once per project**. If the user wants to start over, ask whether to delete + re-scaffold or keep the existing artifacts.

The scaffold is intentionally generic. Per-project customization happens by:
- `design-themes` rewriting `tokens.css`
- `prd-crit` and `map-cujs` filling in the artifact subdirectories
- The user editing `APPROVED` (via `bump_approval.py`) to set `target:` and approval state

Don't re-run this skill to "refresh" the scaffold; that risks overwriting the user's work. If the launcher template needs updating, edit `regenerate.py` and re-run that.

## Steps

### 1. Check for existing scaffold
Run `test -d prototype/`. If it exists, ask the user whether to keep it (stop here), replace it (move to step 2, but confirm destructive action first), or scaffold under a different name.

### 2. Copy scaffold files
From this skill's `assets/` directory into the user's project:
- `assets/index.html` → `prototype/index.html`
- `assets/tokens.css` → `prototype/tokens.css`
- `assets/APPROVED` → `prototype/APPROVED`
- `assets/styles/design-guidelines.html` → `prototype/styles/design-guidelines.html` (vendor design guidelines reference)
- `assets/frames/*.html` → `prototype/frames/` (six frame templates: web-spa, phone-ios, phone-android, watch, desktop, terminal)

Then create the empty artifact subdirectories: `prototype/{prd,cujs,wireframes,styles,hi-fi,components,frames}/` (the `frames/` dir already has the six templates from above; the rest start empty).

The `APPROVED` file is the project's approval manifest. It lists which artifact in each category is the source of truth (approved PRD, approved prototype, approved theme, etc.) and which **render target** the project uses (web-spa, phone-ios, watch, terminal, etc.). Format: `category: value`, one per line, comments allowed with `#`. The scaffold ships with `target: web-spa` as the default; ask the user during init if their project targets a different form factor.

Downstream skills (`prd-crit`, `design-prototypes`, `design-themes`, `map-cujs`, `design-wireframes`) write into this file as the user signs off on each artifact. The launcher's `regenerate.py` reads it to render "✓ Selected" pills next to matching items and a small green check next to aligned section headers.

The `frames/` directory holds illustrative form-factor wrappers (iPhone shape, watch face, terminal window, etc.). They serve two purposes: as visual reference for what each target looks like, and as starting templates that `design-prototypes` and `design-wireframes` can copy from when building artifacts for non-web targets. See `styles/design-guidelines.html` for the canonical vendor reference each target maps to (Apple HIG, Material 3, Microsoft Fluent, Meta Horizon, etc.).

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
