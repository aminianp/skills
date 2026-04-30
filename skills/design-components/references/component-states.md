# Component States Cheatsheet

Components have **variants** (visual flavors of the same component) and **states** (how the same variant responds to interaction or content lifecycle). Both should be documented; they answer different questions.

| Question | Answered by |
|---|---|
| What kinds of this component exist? | Variants |
| How does the user know it can be tapped? | States (hover, focus) |
| What happens when they tap it? | States (active) |
| What if they can't tap it right now? | States (disabled) |
| What if the data hasn't arrived yet? | Dynamic states (loading, empty, error) |

## Variants

Examples:
- **Button**: primary / secondary / ghost; with/without trailing icon; sizes
- **Tag pill**: clickable / static / count-bearing
- **Logo tile**: gradient / monochrome; sizes

Variants change the component's *identity*. A primary button and a secondary button are different things, not different states.

## Interactive states

Document under a "States" section in the component file. Apply to anything tappable / hoverable / focusable.

- **default** &mdash; at rest, no interaction
- **hover** &mdash; pointer over (desktop only; ignored on touch)
- **focus** &mdash; keyboard focus. Use `:focus-visible` so mouse clicks don't trigger the outline. Outline must be visible against the background.
- **active** &mdash; currently being pressed/tapped (briefly, on press)
- **disabled** &mdash; non-interactive. Lower contrast, no hover response, `aria-disabled="true"` or the disabled attribute.

Common mistakes:
- Removing `:focus` outlines without replacing them &rarr; keyboard users can't see what's focused.
- Hover state too dramatic (big color jump) &rarr; reads as a bug.
- Disabled state visually identical to enabled &rarr; users tap and nothing happens, with no feedback.
- "Hover" affordances on touch devices &rarr; user has no way to see they exist.

## Dynamic states

Document under a "Dynamic states" section, only on components that wrap **asynchronous content** (lists from an API, search results, fetched profile data, forms with server validation).

- **loading** &mdash; fetch in progress. Show a skeleton (preferred) or a spinner. Keep the layout stable so content doesn't jump in.
- **empty** &mdash; fetch succeeded but returned nothing. Show helpful copy explaining why and what to try ("No posts in this topic yet" beats "No results"). Often paired with a recovery action ("Browse all").
- **error** &mdash; fetch failed. Show a clear message and a retry. Don't fail silently.
- **partial / paginated** &mdash; some loaded, more available. Show a "Load more" or progressive-pagination cue.

For a list: each of those states is a state of the *list*, not a different component. Document them on the list-component's page.

## Form-specific states

For inputs (text, select, etc.):

- **default**, **focus**, **filled**
- **invalid** (validation failed; show the message, don't just paint the border red)
- **valid** (subtle confirmation; rarely needed except for password rules)
- **disabled** / **read-only** (different things: disabled isn't submitted, read-only is)

For input groups: also document **submitting** (button disabled, spinner on it) and **submitted** (form replaced with a confirmation or a redirect).

## How to document in a component file

Add a `States` section after `Variants`. Each cell shows the state, an inline live example, and the escaped HTML snippet. Same chrome as variants.

For dynamic states (loading / empty / error), show all three with realistic copy. The empty state in particular tends to be where products feel rough &mdash; an "empty inbox" should celebrate, not apologize.

## Anti-patterns

- "Loading" states that just freeze the screen with no indicator
- Empty states that say "no results" with no explanation or recovery
- Errors that fail silently or bury the message in a toast that auto-dismisses
- Disabled states that are achievable from a hover (so the user can't see why)
- Removing `:focus` outlines without replacing them
- Using color alone to convey state (pair with text, icon, or border)
