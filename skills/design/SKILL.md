---
name: design
description: Run Design-phase work from a canonical PRD. Produce a design brief, IA, UX goals, lightweight wireframes in code, visual style alternatives, local live prototypes, and finalized style guide/component library with explicit human approvals.
---

# Design

## Goal
1. Translate a canonical PRD into concrete UX and visual design artifacts.
2. Keep design work grounded in a lightweight but explicit problem definition.
3. Deliver live local prototypes and a high-value component library for implementation agents.

## Canonical Input Requirement
- Require a canonical PRD source before any design work:
  - Google Drive link
  - Notion link
  - Local file path (for example `specs/*.md`)
- If canonical PRD is missing, stop and ask for it.
- If link access is blocked, ask the user to paste relevant sections.
- Never proceed without at least a lightweight problem definition:
  - target audience/persona
  - primary goals
  - critical user journeys

## Design Workflow
1. Read and summarize PRD context:
   - canonical source link/path
   - source version/date
   - last synced timestamp
   - open questions that block design
2. Produce a draft design brief (two-pass default):
   - problem framing and UX goals
   - IA and navigation model
   - page-level layout intent and structural prototype plan
   - styling pass plan (same layout, multiple style options)
3. Round 1: Build and iterate a layout-first wireframe prototype:
   - create one baseline wireframe prototype route by default
   - keep content realistic enough for meaningful UX review
   - focus review on structure only: IA, hierarchy, spacing rhythm, CTA placement, responsive behavior
   - create additional layout variants only when the user explicitly asks
4. Round 2: After layout approval, apply style-guide options to the same approved layout:
   - generate style variants by changing color/typography/spacing tokens, not page structure
   - compare options side-by-side using the same content and layout
5. Publish artifacts to local/internal site:
   - write/update docs under `specs/`:
     - `site-design-brief.md`
     - `site-design-style-guide.md` (draft until approved)
   - update `/internal/specs` references so design docs are visible
   - ensure prototype links from internal pages use `target="_blank"` and `rel="noopener noreferrer"`
6. Request human approval gate (required):
   - design brief approved
   - wireframe/layout approved
   - one visual style direction selected
   - one styled prototype direction selected
   - style guide approved
7. Finalize design after approval:
   - finalize user flows and interaction states
   - finalize visual language (colors, typography, spacing, sizing, line-height, radius, elevation)
   - only after prototype and style guide approval: produce/update a live component library route used during development
   - update `site-design-style-guide.md` to final status

## Output Artifacts
- `Design Brief` in `specs/site-design-brief.md`
- `Design Style Guide` in `specs/site-design-style-guide.md`
- `Live Wireframe Prototype` under `src/pages/internal/prototypes/` (single baseline by default)
- `Styled Prototype Variants` reusing the approved layout (style-only differences by default)
- `Additional Prototype Variants` only on explicit user request
- `Live Component Library` under `src/pages/internal/design/`

## Style Guide Requirements
- Style guide must be visual, not text-only.
- Include:
  - color swatches with hex values and usage notes
  - typography preview (font family, size scale, line-height)
  - spacing rhythm preview (example blocks showing spacing steps)
  - UI examples that show how tokens change real components

## Approval Rules
- Do not mark design artifacts as final without explicit human sign-off in the current thread.
- Keep design artifacts in `In Review` until approval is explicit.
- Lock layout before style exploration unless user explicitly asks to skip.
- Do not build or expand the component library until both a prototype and style guide are explicitly approved.
- Include a final `## Human Review` section in design brief/style guide artifacts.
- The `## Human Review` section is human-owned: do not edit or remove existing content under it.

## Quality Gates
1. UX goals map to PRD goals and critical user journeys.
2. IA labels are clear and navigation paths are obvious.
3. Prototypes are viewable locally and linked from `/internal/specs`.
4. At least one accessibility pass is documented:
   - contrast
   - keyboard path
   - focus visibility
   - heading hierarchy
5. Style guide tokens are concrete enough for implementation and demonstrated visually.
6. Component library covers high-usage components for the approved flows (navigation, buttons, cards/lists, content blocks, form/contact elements if present).

## Output Contract
- Avoid subjective critique without reasoning.
- For alternatives, always include:
  - strengths
  - risks
  - recommended option
- Default stance: iterate the baseline layout prototype first, then branch into style variants on the approved layout.
- End each iteration with:
  - approval status
  - blocking questions
  - next 1-2 concrete actions

## Templates
- Use `DESIGN_BRIEF_TEMPLATE.md` when creating or refreshing design briefs.

## Self-Improvement Loop (Design)
- On user correction, append a design-specific lesson to `/.working/lessons/design-lessons.md`.
- Also append a distilled cross-skill lesson to `/.working/lessons/global-lessons.md`.
- At Design session start, review:
  - `/.working/lessons/global-lessons.md`
  - `/.working/lessons/design-lessons.md`
