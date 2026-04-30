---
name: design-wireframes
description: Generate per-screen HTML wireframes for a user flow (CUJ), using Tailwind v4 utility classes that consume the prototype's theme tokens. Each screen becomes one HTML file under `prototype/wireframes/` and shows up as its own link in the prototype launcher. Trigger when the user says "design-wireframes", "wireframe this flow", "mock up the signup screens", "let's get a layout for X", "draft the screens for the [feature/flow] CUJ", or has just finished mapping CUJs and is ready to translate them into something visual. Trigger proactively after `map-cujs` or `journey-writer` produces a flow, when the prototype scaffold exists, and the user mentions wanting to see what something would look like.
---

# Design Wireframes

## What This Does
Reads a CUJ (a user flow with steps) and produces one HTML wireframe per step, saved into `prototype/wireframes/`. Each wireframe is a standalone document that uses Tailwind v4 utility classes against the prototype's `tokens.css`, so the visual style updates automatically when the theme changes. The prototype launcher (refreshed via `prototype-update`) lists each wireframe by title.

The output is **lofi-but-themed** — real layout, sensible placeholder content, no real branding, but rendered with whatever theme is currently in `tokens.css`. Not grayscale, not high-fidelity. Enough structure to evaluate the flow; not so much that it pre-decides visual choices.

## Prerequisites
- `prototype/` exists (run `prototype-init` first if not)
- `prototype/tokens.css` exists (shipped by `prototype-init`; can be customized later via `design-themes`)

If either is missing, stop and direct the user to run `prototype-init` first.

## Granularity: One Screen Per File
Each step in the CUJ = one HTML file. A 4-step signup flow produces 4 files. This matches how the launcher shows them (one link per artifact) and lets the user open multiple screens side-by-side in browser tabs.

**Filename convention:** `<cuj-slug>-<NN>-<step-slug>.html` — zero-padded step number ensures alphabetical sort matches step order. Example for a "Signup" CUJ:

```
prototype/wireframes/
├── signup-01-email.html
├── signup-02-verify.html
├── signup-03-profile.html
└── signup-04-welcome.html
```

**Title convention:** `{Flow}: {Step description}` — e.g., `<title>Signup: Enter email</title>`. The launcher pulls `<title>` for the link text, so this becomes the user-facing label.

## Inputs

In priority order, look for the CUJ definition in:

1. **CUJ files in `prototype/cujs/`** — read them, extract step descriptions
2. **PRD content in `prototype/prd/`** — if no CUJ file exists yet but the PRD describes the flow
3. **Inline description from chat** — the user types out the flow

If none of these has enough detail to generate screens, ask for the flow's steps one at a time. Don't guess — it's faster to ask than to wireframe the wrong flow.

## Process

### Step 1 — Confirm the screen list
Before writing any HTML, list the screens you intend to produce and check with the user:

```
I'll generate 4 wireframes for the Signup flow:
  signup-01-email.html      — email entry
  signup-02-verify.html     — "check your email" confirmation
  signup-03-profile.html    — name + role
  signup-04-welcome.html    — onboarding complete
Sound right?
```

This catches cases where the CUJ has implicit screens (e.g., error states) or where multiple steps collapse into one screen.

### Step 2 — Check for existing files
If any target file already exists, ask before overwriting:
- **Overwrite** — replace it
- **Versioned** — save the new one as `signup-01-email-v2.html`
- **Skip** — don't regenerate that screen

Never silently overwrite. The user may have hand-edited a wireframe.

### Step 3 — Generate each wireframe

Read `assets/wireframe-template.html` for the page scaffold (Tailwind CDN, `@import` tokens.css, top nav with prev/next links, main content area). Substitute placeholders:

- `{TITLE}` — the page title (`Signup: Enter email`)
- `{FLOW_NAME}` — short flow name (`Signup`)
- `{STEP_N}` and `{STEP_TOTAL}` — step number and total
- `{PREV_LINK}` and `{NEXT_LINK}` — anchor tags (or empty strings on first/last step)
- `{CONTENT}` — the screen mockup

For prev/next links use same-tab navigation (no `target="_blank"`) — the user is reviewing the flow in sequence inside one tab. Format:

```html
<a href="signup-01-email.html" class="text-fg hover:text-accent">&larr; Email</a>
<a href="signup-03-profile.html" class="text-fg hover:text-accent">Profile &rarr;</a>
```

On the first step, `{PREV_LINK}` is empty. On the last, `{NEXT_LINK}` is empty.

### Step 4 — Compose the screen content

Each screen's `{CONTENT}` block is yours to design. Some principles:

**Use semantic theme classes, not raw Tailwind colors.** Good: `bg-bg`, `text-fg`, `text-muted`, `border-border`, `bg-primary text-primary-fg`. Bad: `bg-white`, `text-gray-700`, `bg-blue-500`. Theme classes propagate when the user runs `design-themes`; raw colors don't.

**Use realistic placeholder content, not Lorem ipsum.** "Continue with Google", "you@example.com", "We'll send a verification link" — content a real user would see. Helps the user evaluate the layout against actual copy.

**Common patterns:**
- Forms: `<label>` with text-sm font-medium, `<input>` with `w-full px-3 py-2 rounded border border-border bg-surface`, primary button `bg-primary text-primary-fg rounded py-2 px-4 font-medium`
- Lists: `<ul class="divide-y divide-border">` with `<li class="py-3">` items
- Headers: `text-2xl font-semibold mb-2` for screen title, `text-muted mb-8` for subtitle
- Cards: `rounded-md border border-border bg-surface p-6`
- Containers: `max-w-md mx-auto` for narrow flows, `max-w-3xl mx-auto` for content-heavy screens

**Don't include:**
- Real logos or brand names — use a text placeholder like "Brand"
- Custom `<style>` blocks — Tailwind handles all styling
- Animations — wireframes are static
- Hover/focus states on buttons beyond Tailwind defaults — those are hi-fi concerns

### Step 5 — Write all files, then run prototype-update

After all wireframes are written, regenerate the launcher so the new files show up:

```bash
python3 ~/.claude/skills/prototype-update/scripts/regenerate.py prototype/
```

(Adjust the path if the user's skills directory lives elsewhere.)

### Step 5a — Web targets must be responsive

If `target:` is `web-spa` (default) or any web target, the wireframe **must** work at mobile, tablet, and desktop widths. This is non-negotiable. Most web traffic is mobile; a desktop-only wireframe hides the hardest layout problems until production. "Responsive" doesn't mean "the desktop layout shrinks gracefully" &mdash; it means the layout fundamentally restructures so each form factor reads naturally.

Wireframes are lower-fidelity than prototypes, but the responsive structure still has to be correct &mdash; engineering uses the wireframe to know where things stack, where buttons go full-width, where the nav collapses to a hamburger.

For the full responsive checklist (touch targets, hamburger drawer, button stacking, hero centering, validation widths, anti-patterns), see the matching section in `design-prototypes` &mdash; the rules are identical at the wireframe and prototype stages. The short version:

- **Touch targets &ge; 44px** (use `py-3` for buttons on mobile)
- **Hamburger drawer below md** for any nav with 3+ items + secondary actions
- **Primary CTA groups stack vertically and full-width below sm** with `flex flex-col sm:flex-row gap-3` and `text-center` on each button
- **Hero centers on mobile** (`items-center sm:items-start`, `text-center sm:text-left`)
- **Multi-column lists collapse** (`grid grid-cols-1 sm:grid-cols-[7rem_1fr]`)
- **Footer stacks vertically** below sm
- **Container padding tightens** (`px-4 sm:px-6`); section padding halves (`py-10 sm:py-20`)
- **Headings shrink with looser leading** on mobile

Validate at 320px / 390px / 768px / 1024px / 1440px. No horizontal scroll anywhere. Test the hamburger drawer opens and closes cleanly.

For non-web targets (phone-ios, watch, etc.), the frame template handles "what device shape is this" &mdash; you don't need responsive prefixes on the inner content because it's rendering inside a fixed-width device frame.

### Step 5b — Frame the wireframe to the target form factor

Read `target:` from `prototype/APPROVED`. If it's anything other than `web-spa`, wrap the wireframe content inside the matching frame from `prototype/frames/<target>.html` &mdash; phone shape, watch face, terminal window, etc. The wireframe page should still render standalone in a browser; the frame is part of its markup, not an iframe.

For `web-spa` (default), no frame &mdash; the wireframe content fills the viewport.

When in doubt about platform conventions for the target (e.g., where status bars go on Android vs iOS, what a watch glance looks like), open `prototype/styles/design-guidelines.html` and follow the vendor link for that target. Don't approximate from memory; anchor to the canonical source.

### Step 6 — Tell the user what to do next

Direct them to refresh the prototype tab to see the new wireframes listed, and remind them they can run `design-themes` if they want to change the visual style — wireframes will re-theme on browser refresh.

### Step 7 — Mark wireframes aligned (once the user signs off)

When the user signals the wireframes look right ("these flows look good", "let's move on to hi-fi"), call the approval script:

```bash
python3 ~/.claude/skills/prototype-update/scripts/bump_approval.py prototype/ wireframes aligned
```

Wireframes are typically aligned as a set rather than individually &mdash; they're then superseded by the HiFi prototype. Run `prototype-update` afterward. See [Approval Protocol](../prototype-update/references/approval-protocol.md).

## Pipeline

- **Reads from**: aligned CUJs from `map-cujs` (in `prototype/cujs/`); active theme from `prototype/tokens.css`; render `target:` from APPROVED
- **Produces**: per-screen wireframe HTML files in `prototype/wireframes/`
- **Feeds out to**: `design-prototypes` (which consolidates the wireframes into a single navigable interactive prototype)

## Iteration

Wireframes are draft layouts and are expected to iterate. If the user asks for substantial changes (new screens, restructured flow), drop the alignment line until they sign off again:

```bash
python3 ~/.claude/skills/prototype-update/scripts/bump_approval.py prototype/ wireframes
```

Minor in-place edits to a single wireframe (a tightening pass, copy change) don't require unmarking.

When CUJs change upstream, the wireframes for the affected flows are likely stale &mdash; re-run this skill on those CUJs to refresh.

## Worked example

`references/examples/blog-02-post.html` &mdash; the blog-post wireframe from pouyan.fyi. Single-column article layout with metadata header and related-posts footer; demonstrates the lofi blueprint style (real Tailwind, real type scale, placeholder-but-realistic content).

## Iteration on Existing Wireframes

If the user asks to modify a wireframe ("make the signup email screen tighter", "add a 'sign in instead' link"), read the existing file, apply the change, and rewrite. Don't regenerate from scratch — the user may have hand-tuned class choices or content.

When iterating, don't run `prototype-update` unless filenames changed (renames count, content edits don't — the launcher already lists the file).

## What This Skill Does Not Do

- **Pick a visual style** — that's `design-themes`. Wireframes use whatever's in `tokens.css` at the time.
- **Add real interactivity** — no JavaScript event handlers, no form submission. Wireframes are static layouts.
- **Build hi-fi prototypes** — those go in `prototype/hi-fi/`. Wireframes are intentionally less polished.
- **Generate component libraries** — wireframes write inline classes per element. Components are a future skill if needed.
- **Mock data fetching or backends** — show static placeholder content. Real APIs are out of scope.
- **Update the CUJ files in `prototype/cujs/`** — those are inputs, not outputs. If the wireframing process surfaces issues with the CUJ, flag them to the user but don't edit the CUJ.

## Why Tailwind Utility Classes Instead of Component Classes

Two reasons. First, the user can edit a wireframe by hand without knowing any custom CSS — Tailwind utilities are self-describing and well-documented. Second, when `design-themes` re-themes the prototype, every wireframe's semantic classes (`bg-primary`, `text-fg`, etc.) automatically pick up the new tokens. There's no component-level CSS to update, no cascade to debug. The cost is verbose class lists, which is acceptable for prototyping artifacts.
