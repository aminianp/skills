---
name: design-themes
description: Generate or iterate the design system for the local prototype site by walking the user through a structured taste-elicitation flow (constraints, references, adjectives, dials), then writing a Tailwind v4 `@theme` block to `prototype/tokens.css` so all wireframes re-theme on browser refresh. Trigger when the user says "design-themes", "let's pick a theme", "set up the design system", "make it look like X", "I want this to feel like Linear/Stripe/Notion/Anthropic", "warmer / more playful / sharper / more vivid", or asks to switch the prototype between aesthetic options. Trigger proactively after `prototype-init` runs and at least one wireframe has been created, since the default monochrome theme is a placeholder rather than a chosen direction.
---

# Design Themes

## What This Does
Writes `prototype/tokens.css` — a single Tailwind v4 `@theme` block that defines the design system for every artifact in the prototype (color, typography, radius, spacing). Every HTML file already `@import`s this file via Tailwind's browser script, so editing it re-themes the launcher and all wireframes simultaneously on the next browser refresh.

The skill works in two modes:

1. **First-run mode** — no opinionated theme yet (or the default monochrome is still in place). Walks through a 4-phase elicitation, picks the closest bundled preset, perturbs it based on the user's answers, and writes the result.
2. **Iteration mode** — a custom theme already exists. Reads it, asks what should change ("warmer", "softer corners", "more contrast"), and rewrites with targeted edits.

## When to Skip Elicitation
If the user gives clear direction up front — "make it Linear-like, dark mode, blue accent" — go straight to picking a preset and perturbing. No need to walk them through phases they've already answered. The elicitation is a fallback for when the user can't articulate what they want.

## The 4-Phase Elicitation

Run these in order. Skip any phase the user has already answered. Don't bombard with all questions at once — ask phase 1, wait, ask phase 2, etc. The whole point is to make this feel conversational, not like a survey.

### Phase 1 — Constraints (hard limits first)

These are non-negotiable, so capture them before asking about taste:

- Any locked brand colors? (specific hex values that must appear)
- Any required fonts? (e.g., the brand uses Inter)
- Is dark mode required for this prototype? (default: light only — adding dark mode well takes meaningful extra effort, skip it unless asked)
- Accessibility floor? (default: WCAG AA — text must hit 4.5:1 contrast against its background, UI elements 3:1)

If none, move on. Don't waste the user's time with "any constraints?" if they've given no signal of having any.

### Phase 2 — References (the strongest signal)

Ask: *"Name 2–3 products whose visual feel you'd want to be in the neighborhood of."*

Examples to suggest if the user is stuck: Linear, Stripe, Notion, Vercel, Anthropic, Apple, Figma, Discord, Substack, GitHub, Arc browser, Things 3.

Extract the following from each named product (using your knowledge of how they actually look — don't guess):
- Neutral temperature: warm grey / cool grey / true black
- Accent saturation: muted / medium / vivid
- Radius personality: sharp (≤4px) / medium (~6–10px) / soft (≥12px)
- Density: airy / balanced / dense
- Type contrast: tight (single sans family) / dramatic (display + body split)

If the references conflict (Linear is cool/sharp, Substack is warm/serif), surface the conflict and ask which direction to lean.

### Phase 3 — Adjective lexicon (pick 2–3)

Ask the user to pick 2–3 from this fixed list:

- *temperature*: warm / cool / neutral
- *density*: airy / balanced / dense
- *personality*: minimal / editorial / playful / technical / brutalist
- *finish*: soft / sharp / refined

Keep the list closed. Free-form adjectives ("dynamic", "approachable") are noisy — they map to too many things.

### Phase 4 — Dials (1–5 scales, optional)

Only ask these if Phase 2 and 3 left the picture ambiguous, or if the user volunteers preferences that fit naturally:

- **Sharp ↔ Soft** (1 = `--radius` ~2px; 5 = ~12px+)
- **Muted ↔ Vivid** (1 = chroma near 0.05; 5 = chroma 0.20+)
- **Warm ↔ Cool** (1 = neutrals at hue ~50°; 5 = neutrals at hue ~250°)

Skip dials if the user already gave 2–3 references and 2–3 adjectives — that's enough signal. Dials are a tiebreaker tool, not a required step.

## Mapping Answers to a Preset + Perturbing

The skill ships three presets in `assets/presets/`:

- **`monochrome.css`** — neutral greys, sharp-ish, system font. Best for: "minimal", "wireframe-y", "no-color", "neutral", or no opinion.
- **`linear-like.css`** — cool bluish neutrals, electric blue accent, sharp radii, Inter. Best for: "technical", "developer tool", "modern SaaS", references like Linear / Vercel / Anthropic.
- **`editorial.css`** — warm cream backgrounds, deep brown text, generous radii, serif body. Best for: "warm", "publication", "writing tool", references like Substack / Stripe Press / The New Yorker.

### Step 1 — Pick the closest preset

Map the user's answers to one of the three. Be generous — close enough is fine, perturbation handles the rest.

### Step 2 — Perturb the preset

Read the preset file. Rewrite token values based on the user's signals using OKLCH (lightness chroma hue):
- *Warmer* → shift hue toward 30–80° (orange/yellow). *Cooler* → shift toward 220–280° (blue).
- *More vivid* → increase chroma in `--color-primary` and `--color-accent` (e.g., 0.15 → 0.22).
- *More muted* → decrease chroma (e.g., 0.20 → 0.08).
- *Softer* → increase `--radius` (0.25rem → 0.5rem → 0.75rem).
- *Sharper* → decrease `--radius` (0.5rem → 0.25rem → 0.125rem).
- *Brand color override* → replace `--color-primary` with the user's hex, derive `--color-accent` as a slightly lighter sibling.
- *Required font* → swap into `--font-sans`, keep system fallbacks at the end of the stack.

Use judgment. The presets are anchors, not templates.

### Step 3 — Verify contrast (WCAG AA)

Before writing, mentally check:
- `--color-fg` against `--color-bg` ≥ 4.5:1 (body text)
- `--color-muted` against `--color-bg` ≥ 4.5:1 (secondary text)
- `--color-primary-fg` against `--color-primary` ≥ 4.5:1 (button labels)
- `--color-border` against `--color-bg` ≥ 3:1 (UI elements / lines)

If a check fails, adjust the lightness in OKLCH (lower the L for fg colors, raise it for bg colors) until it passes. Don't ship a theme that fails AA.

### Step 4 — Write `prototype/tokens.css`

Replace the entire file. Preserve the leading comment block — explain at the top of the file what theme this is and what preset it derived from, so it's self-documenting:

```css
/* prototype/tokens.css — generated by design-themes
 * Anchor preset: linear-like
 * Direction: cooler, more vivid blue, slightly softer corners
 */
@theme {
  ...
}
```

### Step 5 — Propagate the new theme to every HTML file

**Critical** — `tokens.css` is the human-readable source of truth, but Tailwind's browser CDN does not resolve `@import` to external files inside its tagged `<style>` blocks. Every HTML file in `prototype/` therefore inlines a copy of the `@theme` block between `/* @theme:start */` and `/* @theme:end */` markers. Without propagation, editing `tokens.css` has zero visible effect.

Run the bundled propagation script:

```bash
python3 ~/.claude/skills/design-themes/scripts/apply_theme.py prototype/
```

The script reads `prototype/tokens.css`, extracts the `@theme` block, walks every `.html` file in the prototype tree, and replaces the content between the marker comments with the new block. It reports which files were updated, which were already in sync, and which were skipped (no markers found — usually means a hand-rolled artifact that needs the markers added).

### Step 6 — Tell the user how to see the change

After propagation, a browser refresh is sufficient. Tell them: "Refresh the prototype tab(s) to see the new theme." Don't run `prototype-update` — that regenerates the launcher's HTML structure, which hasn't changed (and the regenerator pulls from `tokens.css` itself, so it stays in sync independently).

## Iteration Mode

If `prototype/tokens.css` already exists with custom values (not just the default monochrome), assume iteration. Read the current file, ask the user what should change, then rewrite — don't re-run the full elicitation.

Examples of iteration prompts and how to respond:
- *"warmer"* → shift neutral hues toward 60–80°, slight chroma bump
- *"softer corners"* → increase `--radius`
- *"more contrast"* → darken `--color-fg`, lighten `--color-bg`, deepen `--color-border`
- *"too playful, dial back"* → reduce chroma, neutralize hue toward 0
- *"swap the accent to green"* → replace `--color-primary` and `--color-accent` with green-family OKLCH values, re-check contrast on `--color-primary-fg`

Always show the user a diff or short summary of what changed ("Increased radius 0.25rem → 0.5rem; warmed neutrals from hue 260 to hue 80; chroma on primary 0.20 → 0.10"). Helps them decide if the change went too far.

## Common Pitfalls to Avoid

- **Tokenizing component-specific values.** Don't add `--color-button-hover-bg` — that's a component decision, not a theme one. Stick to the ~12 semantic roles in the presets.
- **Building from scratch.** Always anchor on a preset. The presets are calibrated; building from zero produces inconsistent themes.
- **Ignoring contrast.** A pretty palette that fails AA is a broken palette. The mental contrast check is part of generation, not a separate review step.
- **Asking too many questions.** The elicitation is 4 phases on paper; in practice, 2 references and 2 adjectives is often enough. Don't drag the user through dials they don't need.
- **Writing utility-class overrides.** This skill only writes `@theme`. If you find yourself writing `.button { ... }` rules, you're out of scope.

## What This Skill Does Not Do

- **Generate component styles** — wireframes use Tailwind utility classes directly. Theme changes propagate via tokens.
- **Add dark mode** — defaultly light only. Adding dark mode requires a `[data-theme="dark"]` selector pattern and re-defining every color token; only do this if the user explicitly asks.
- **Update wireframes themselves** — wireframes already reference `var(--…)` via Tailwind classes. They re-theme automatically.
- **Choose between sans/serif body for the user** — that's a Phase 3 / preset decision. If the user says "editorial", they get serif; if they say "minimal", they get sans. Don't second-guess the preset.
