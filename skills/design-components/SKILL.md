---
name: design-components
description: Extract a component library from the project's approved HiFi prototype. Each repeating UI pattern (button, tag pill, logo tile, post list item, icon link, etc.) becomes its own demo HTML page under `prototype/components/`, showing every variant/state with inline `@theme` markers so it stays themable. Trigger when the user says "design-components", "extract components", "build the component library", "let's pull out the components from the prototype", or has settled on an approved prototype and wants a reusable spec engineering can build against. Also trigger proactively after the user marks a prototype as approved and the next step is implementation handoff.
---

# Design Components

## What This Does

Reads the project's **approved HiFi prototype** and extracts the repeating UI patterns into a component library at `prototype/components/`. Each component lives in its own demo HTML page that shows the variants and states it supports (default, hover, active, disabled, sizes, etc.) plus a small "Used in" section that links back to the prototypes referencing it.

The library has two consumers:
1. **The user** &mdash; visual reference for what's in the system, place to iterate on a single component without touching the prototype.
2. **`implementation-brief`** &mdash; when handing off to engineering, the brief names components by file (`components/tag-pill.html`) so the eventual production code reuses one shared definition rather than reinventing per page.

This sits **after** `design-prototypes`. Components are *extracted from* an approved prototype, not specified ahead of it &mdash; for a personal site or small product, the design-system-first approach is too heavy. We let the prototype settle first, then crystallize what's actually there.

## When to Run

- After a HiFi prototype is approved (see "Approval tracking" below).
- Whenever the approved prototype changes substantially &mdash; re-extract so components stay in sync.
- Before `implementation-brief` so the brief can reference components.

If no prototype has been approved yet, ask the user which variant to extract from. Don't extract from variants that are intentionally divergent (e.g., a "different font" variant) &mdash; pick the one that represents the standard.

## Approval Tracking

The skill reads `prototype/APPROVED` &mdash; the project-level manifest that names which artifact is the source of truth for each category. Format:

```
# Approved artifacts. One line per category. Paths are relative to prototype/.
prd: prd/site-prd.md
prototype: hi-fi/cool-minimal-v1.html
theme: tokens.css
```

For this skill, the relevant key is `prototype:` &mdash; that's the source from which components are extracted. If the manifest is missing or the `prototype:` line is absent, ask the user which variant is approved and offer to write the manifest line. Don't extract from a variant that isn't the approved one &mdash; intentionally divergent variants (different theme, different flow) would pollute the library.

The launcher (via `prototype-update`) reads this manifest and renders a small "✓ Approved" badge next to matching items in each category's sidebar list, so the approved artifact is visually distinct everywhere.

## Output Layout

```
prototype/components/
├── button.html
├── tag-pill.html
├── logo-tile.html
├── icon-link.html
├── post-list-item.html
├── nav-link.html
└── ...
```

Components open **inline** in the launcher (not a new tab) &mdash; they're spec pages, not full screens.

## What Counts as a Component

**If a pattern is used (or you'd reach for it) more than once across the site, it's a component.** That's the bar.

This applies to anything visually reusable: buttons, navbars, link styles, pills, logo tiles, post list items, icon links, section headers, footer blocks, and so on. Not just "buttons" in the narrow sense &mdash; if you've written the same chunk of markup with the same classes twice, extract it.

A pattern does *not* qualify if it only appears once and you don't expect to use it again. A pure typography pattern (a heading with a specific class) lives in `tokens.css` and global styles, not in `components/` &mdash; components have structure, not just text styling.

Common components extracted from a typical site prototype:

- **Button** &mdash; primary, secondary, ghost; with/without trailing icon; sizes
- **Tag pill** &mdash; default, active, with count, clickable vs static
- **Logo tile / avatar** &mdash; sizes, color variants
- **Icon link** &mdash; default, hover, sizes (nav vs footer)
- **Post list item** &mdash; with/without summary, with metadata row
- **Nav link** &mdash; default, hover, active (with underline)
- **Section header** &mdash; eyebrow + title + optional subtitle
- **Footer block** &mdash; copyright + social icon row

Err on the side of extracting. It's cheaper to delete a component nobody uses than to leave duplicated markup that drifts.

## Document States (Not Just Variants)

Components have **variants** (visual flavors of the same component) and **states** (how the same variant responds to interaction or content lifecycle). Both should appear in the component file.

- **Variants** answer "what kinds of this component exist?" &mdash; primary vs secondary button, clickable vs static pill.
- **Interactive states** answer "how does the user know it can be tapped, what happens when they tap, what if they can't right now?" &mdash; default / hover / focus / active / disabled. Document on every interactive component.
- **Dynamic states** answer "what if the data hasn't arrived yet?" &mdash; loading / empty / error / partial. Document on components that wrap async content (lists, search results, forms with server validation).

For the full taxonomy plus anti-patterns, see [component-states.md](references/component-states.md). Reserve State sections for components where the state actually changes the rendering &mdash; a static logo tile doesn't need a Disabled state.

## Default to Modern Patterns

Don't reinvent 2010 defaults. Components should reach for current practice unless there's a reason to deviate:

- Pills are `rounded-full`, not square
- Active/selected states use a soft tint (`color-mix(fg 8%, transparent)`), not solid black
- Touch targets are ≥ 44px on mobile (`py-3`)
- Social links are SVG icons, not text labels
- Buttons in groups stack vertically full-width below sm
- Use `:focus-visible` rings on every interactive element

The full reference is [modern-web-defaults.md](references/modern-web-defaults.md). Skim it before writing the first component on a project; deviate only when the brand explicitly requires it.

## Accessibility Floor

Every component must clear a baseline:

- **Icon-only buttons need `aria-label`** describing the action ("Open menu", not "menu icon"). Without this, screen readers announce them as "button" with no context.
- **Decorative SVGs get `aria-hidden="true"`** so they don't get spoken redundantly when they're inside a labeled button.
- **Meaningful images need `alt` text**; decorative ones get `alt=""` (don't omit the attribute).
- **Don't convey state with color alone** &mdash; pair color with text, icon, or border weight.
- **`:focus-visible` ring** on every interactive component, with sufficient contrast against the background.
- **Keyboard tab order matches visual order.** No `tabindex` other than `0` or `-1` (positive `tabindex` is an anti-pattern).
- **Disclosure widgets** (drawers, dropdowns, accordions) need `aria-expanded`, `aria-controls`, and consistent open/close state.

Document the accessibility contract for each component near its States section &mdash; what aria attributes it expects, what keyboard interactions it supports.

## Document Responsive Behavior (When It Changes)

For web-target components whose layout **actually changes at a breakpoint** &mdash; a nav row that hides items below `sm`, a two-column grid that collapses to one, a hero that stacks vertically, a heading that scales down &mdash; add a `Responsive` section to the component page describing the change. Include the breakpoint, what shifts, and a code snippet showing the responsive class string.

For components that render the same at every viewport (a button, a tag pill, a single-letter logo tile, an icon link) &mdash; **don't** add a `Responsive` section. Padding it onto every component is noise. Reserve the section for actual breakpoint behavior.

Common shape:

```html
<section>
  <h2>Responsive</h2>
  <p>Below the <code>sm</code> breakpoint (640px), the row stacks vertically...</p>
  <pre><code>... escaped class string showing the responsive prefixes ...</code></pre>
  <p>Rationale: at phone widths there's no room for ...</p>
</section>
```

Place this section after `Variants` / `States` and before `Tokens`. The pattern is "show what changes, then say why." Engineering uses it to avoid re-deriving breakpoints when translating to production code.

## Component Page Structure

Each component HTML follows this shape:

```html
<head>
  Tailwind v4 CDN
  Inline @theme block (with /* @theme:start */ ... /* @theme:end */ markers
    so design-themes propagates theme changes)
  Page-level CSS for any component-specific styles (e.g., .tag-active)
</head>
<body>

  <!-- Launcher chrome (← Prototype / Components / <component name>) -->
  <header>...</header>

  <main>
    <!-- Title + 1-line description -->
    <section>
      <h1>Tag Pill</h1>
      <p>Filterable category pill, used in the blog index and home topic list.</p>
    </section>

    <!-- Variants grid: each cell shows one state with the inline HTML below -->
    <section>
      <h2>States</h2>
      <div class="grid">
        <div>
          <p>Default</p>
          <div class="example"><a class="px-3 py-1 ...">PM <span>(4)</span></a></div>
          <pre><code>...escaped HTML snippet...</code></pre>
        </div>
        <div>
          <p>Active</p>
          <div class="example"><a class="tag-active px-3 py-1 ...">PM <span>(4)</span></a></div>
          <pre><code>...</code></pre>
        </div>
        <!-- hover, disabled, etc. -->
      </div>
    </section>

    <!-- Tokens / classes used (so engineering can map back to the system) -->
    <section>
      <h2>Tokens</h2>
      <ul>
        <li><code>--color-fg</code> &mdash; active background tint and border</li>
        <li><code>--color-border</code> &mdash; default border</li>
        <li><code>rounded-full</code> Tailwind utility</li>
      </ul>
    </section>

    <!-- Where this component is used (backlinks to prototypes) -->
    <section>
      <h2>Used in</h2>
      <ul>
        <li><a href="../hi-fi/cool-minimal-v1.html#/blog">Cool & Minimal v1 — Blog</a> (tag filter)</li>
        <li><a href="../hi-fi/cool-minimal-tag-filter-v1.html#/home">Cool & Minimal — Tag Filter v1 — Home</a> (topic chips)</li>
      </ul>
    </section>
  </main>

  <footer>Generated by design-components &middot; <component-slug></footer>
</body>
```

## Naming Convention

`<component-slug>.html` &mdash; kebab-case, descriptive, theme-agnostic.

- ✅ `tag-pill.html`, `logo-tile.html`, `post-list-item.html`
- ❌ `blue-pill.html`, `pill-v1.html`, `cool-minimal-button.html`

The slug names the component, not its color/theme/variant. A theme change shouldn't rename the component.

## Steps

Once the prototype has been approved, you don't need a second approval to extract components &mdash; approving the prototype implicitly approves what's in it. The user can chat with you to rename, merge, or split components after they exist; that's normal iteration, not gating.

1. **Read `prototype/APPROVED`** to find the `prototype:` line. If missing, ask the user which prototype is approved and offer to write the manifest line via `bump_approval.py`.
2. **Read the approved prototype** and identify every reused pattern using the bar above (used more than once = component).
3. **Cross-reference other prototypes** in `prototype/hi-fi/` to find additional usages of each pattern &mdash; this powers the "Used in" backlinks. Skip variants that intentionally diverge (e.g., a "different theme" variant) when collecting backlinks; the component reflects the *approved* shape.
4. **Write each component** to `prototype/components/<slug>.html`, starting from the bundled template at [`references/component-page-template.html`](references/component-page-template.html). Fill in Variants, States (where applicable), Dynamic states (where applicable), Responsive (where applicable), Tokens, and Used-in backlinks. Use semantic theme classes (`bg-bg`, `text-fg`, `border-border`) not raw Tailwind colors. Keep `@theme:start` / `@theme:end` markers so theme changes propagate.
5. **Run `prototype-update`** to refresh the launcher's Components list:

   ```bash
   python3 ~/.claude/skills/prototype-update/scripts/regenerate.py prototype/
   ```

6. **Mark components aligned** in the manifest:

   ```bash
   python3 ~/.claude/skills/prototype-update/scripts/bump_approval.py prototype/ components aligned
   ```

   See [Approval Protocol](../prototype-update/references/approval-protocol.md).

7. **Report back.** List the components written with one-line descriptions, and flag anything ambiguous (e.g., "two patterns looked similar but I extracted them separately because their structure differs &mdash; merge if you'd rather"). Iteration after the fact is expected.

## Pipeline

- **Reads from**: the approved prototype (`prototype:` in APPROVED); cross-references other prototypes in `hi-fi/` for backlinks
- **Produces**: component HTML files in `prototype/components/`
- **Feeds out to**: `implementation-brief` (which references components by filename so engineering reuses one shared definition)

## Keeping Components in Sync With the Prototype

**Whenever the approved prototype is edited, components must be re-checked and updated.** The approved prototype is the spec; the component library is its crystallized form; they cannot drift.

In practice this means: any time a skill (or you, in conversation) modifies the file referenced by the manifest's `prototype:` line, run this skill's extraction logic again afterward. For each component:

- **Pattern still appears, structure unchanged** &mdash; no-op.
- **Pattern still appears, structure or classes changed** &mdash; rewrite the component file to match. Update the "Used in" backlinks if affected.
- **Pattern no longer appears anywhere** &mdash; flag it to the user ("the `tag-pill` component is no longer used in the approved prototype; remove it?") rather than auto-deleting, since the absence may be temporary.
- **A new pattern now appears more than once** &mdash; create a new component file for it.

Manually authored components (ones you didn't extract) are still respected: if a file exists in `components/` that you didn't write and don't recognize as one of your slugs, leave it alone. The user can chat with you to fold a manual component into the auto-extracted set if they want.

After any sync, run `prototype-update` so the launcher reflects the new state.

## What This Skill Does *Not* Do

- **Pixel-perfect production code.** Components are still mockups. They reuse Tailwind, the snippets are realistic but the engineering team will translate them into framework-native code.
- **A full design system.** Tokens (colors, type, spacing) live in `prototype/tokens.css` and are owned by `design-themes`. Components consume tokens; they don't define them.
- **Auto-update prototypes when a component changes.** One-way flow: prototype → component. If the user iterates on a component file, they're refining the spec; they should then update the prototype to match (or not, if the iteration was experimental).
- **Storybook / live component playground.** The component HTML is static. If you want clickable stories, that's an engineering concern downstream.

## Reporting Back

When done, tell the user:

- The list of components written (with one-line description each).
- Patterns that didn't cluster, with a brief reason ("only one usage; not promoted to a component").
- Whether `prototype/APPROVED` already existed or you wrote the `prototype:` line for them.
- Whether you ran `prototype-update` (you should have) and `bump_approval.py components aligned` (you should have).
- A reminder: when `implementation-brief` is run next, it should reference these components by filename so engineering reuses one shared definition.

If the user wants to iterate on the component set after seeing the result &mdash; rename, merge, split, drop &mdash; treat that as a normal next conversation. The library is meant to be edited, not frozen.

## Worked examples

Bundled in `references/examples/`, copied from pouyan.fyi after this skill ran on it:

- `button.html` &mdash; primary + secondary, with/without trailing icon. Includes a Responsive section showing the full-width-stacked-on-mobile pattern.
- `tag-pill.html` &mdash; static / inactive / active / hover variants. Demonstrates the soft-tint active state.
- `site-nav.html` &mdash; sticky top nav composed of nav-link + icon-link. Includes the hamburger drawer pattern in its Responsive section.
- `post-list-item.html` &mdash; compact / full / related variants. Demonstrates the grid-collapse-to-single-column responsive pattern.
- `page-intro.html` &mdash; eyebrow + h1 + lede; standard / blog-post / hero variants. Demonstrates the type-scale-on-mobile pattern.

These are the canonical "what good looks like" for a content-led web component library. Use them as reference when extracting from a similar project.
