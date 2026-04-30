# Approval Protocol

The project carries a single approval manifest at `prototype/APPROVED`. Each line names a category (PRD, CUJs, theme, prototype, etc.) and the artifact &mdash; either a relative path or a group marker like `aligned` &mdash; that's currently the source of truth.

This is the canonical convention every skill in the toolchain uses. Don't reinvent it.

## Format

Plain text, one `category: value` per line. Comments allowed with `#`. Blank lines OK. Categories are open-ended; tools that don't recognize a key just ignore it.

```
# Approved artifacts. One line per category.
prd: prd/site-prd.md
cujs: aligned
styles: styles/cool-minimal.html
wireframes: aligned
prototype: hi-fi/cool-minimal-v1.html
theme: tokens.css
components: aligned
target: web-spa
```

## When to write

When the user signals an artifact is approved / aligned / selected (phrases like *"looks good"*, *"let's lock this in"*, *"let's go with v1"*, *"ship it"*, *"this is the one"*), update the manifest.

**Don't update during iteration.** "Warmer", "tighter", "make this bigger" are mid-flight refinements, not decisions. Approval marks a commitment, not a checkpoint.

## How to write

Use the bundled script &mdash; never edit the file by hand from inside a skill, and never write a one-off Python snippet:

```bash
python3 ~/.claude/skills/prototype-update/scripts/bump_approval.py prototype/ <category> <value>
```

Examples:

```bash
# PRD approved
bump_approval.py prototype/ prd prd/site-prd.md

# CUJs aligned (group marker)
bump_approval.py prototype/ cujs aligned

# Prototype selected
bump_approval.py prototype/ prototype hi-fi/cool-minimal-v1.html

# Theme committed
bump_approval.py prototype/ theme tokens.css
bump_approval.py prototype/ styles styles/cool-minimal.html
```

Omitting the value removes the line (un-approval):

```bash
bump_approval.py prototype/ prototype
```

The script handles: missing manifest (creates one with the header), category exists (updates in place), category doesn't exist (appends with a leading blank line), category absent on a delete (no-op). It preserves comments, blank lines, and the order of unrelated entries.

## After updating

Always run `prototype-update`'s `regenerate.py` so the launcher reflects the new state:

```bash
python3 ~/.claude/skills/prototype-update/scripts/regenerate.py prototype/
```

The launcher reads the manifest and renders:
- A small green &#x2713; next to section headers (CUJs, Styles, Wireframes, Prototypes, Components) when the matching key is set
- A "&#x2713; Selected" pill on the matching item card in list views (Styles, Prototypes)
- A bare &#x2713; next to PRD in the sidebar when `prd:` is set

## Categories used by the toolchain

| Key | Set by | Value | Example |
|---|---|---|---|
| `prd:` | `prd-crit` | path to PRD source file | `prd/site-prd.md` |
| `cujs:` | `map-cujs` | group marker | `aligned` |
| `styles:` | `design-themes` | path to selected style preview | `styles/cool-minimal.html` |
| `theme:` | `design-themes` | active tokens file | `tokens.css` |
| `wireframes:` | `design-wireframes` | group marker | `aligned` |
| `prototype:` | `design-prototypes` | path to selected variant | `hi-fi/cool-minimal-v1.html` |
| `components:` | `design-components` | group marker | `aligned` |
| `target:` | `prototype-init` (initial) / `design-prototypes` (when changed) | render target slug | `web-spa`, `phone-ios`, `terminal`, etc. |

## Reverting / un-approving

If the user un-approves an artifact (*"hold on, let's not consider this final"*, *"un-pick the v1"*), drop the line:

```bash
bump_approval.py prototype/ <category>
```

Then run regenerate. The launcher drops the corresponding badge.

## Why a script and not just `>>` or `sed`

Three reasons:
1. **Single source of truth for the format.** If the format changes (e.g., adds frontmatter, gains nested values), the script changes; skills don't have to.
2. **Idempotent updates.** Running the same command twice is a no-op rather than appending duplicate lines.
3. **Order + comment preservation.** Hand-editing inside a skill loses comments and risks reordering on update; the script preserves both.
