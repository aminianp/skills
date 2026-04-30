# Modern Web Defaults

Defaults to reach for when designing components and prototypes for the web. These reflect 2026 practice across well-designed products (Linear, Stripe, GitHub, Vercel, Notion, etc.). **Deviate when there's a reason; default here when there isn't.**

The goal of this document: stop the agent from rediscovering 2010-era defaults (square pills, solid-black active states, text labels for social icons, desktop-only nav, ignored keyboard users) on every new project.

## Pills / chips

- `rounded-full` &mdash; **not** square corners
- Soft tinted active state, **not** solid black:
  - `background: color-mix(in oklch, var(--color-fg) 8%, transparent)`
  - `border-color: var(--color-fg)`
  - `font-weight: 500`
- Px ≥ 12 (`px-3`), py ≥ 4 (`py-1`). Tighter is too cramped at typical browser zoom.

## Buttons

- ≥ 44px tap target on mobile (`py-3` minimum)
- Two adjacent CTAs: stack vertically full-width below `sm` (640px), inline above
- Primary: filled background; Secondary: 1px border + transparent fill
- `text-center` on labels (so full-width buttons read right)
- Hover: subtle (`opacity-90` or border shift, **not** a big color jump)
- Focus: visible ring (`focus-visible:ring-2 ring-accent`)
- Avoid rounded-full on rectangular CTAs &mdash; use `rounded` for buttons, `rounded-full` for pill-shaped chips and icon buttons

## Logos / avatars

- ≥ 40px on mobile (touch targets), ≥ 44px when paired with adjacent tappable text
- Square logos: `rounded` (slight, ~4px). Circular avatars: `rounded-full`
- Monogram fallback: gradient using the project's primary + accent at ~65/35 mix

## Social links

- Inline SVG icons, **not** text labels &mdash; saves horizontal space, looks crafted, scales with the type
- `fill="currentColor"` so they pick up theme colors via the parent
- 18px in nav, 20px in footer (give the foot a touch more weight)
- Always `aria-label` and `title` so screen readers + tooltips work

## Nav

- **Hamburger drawer below `md`** (768px) for any nav with 3+ items + secondary actions
- Don't hide important nav items on mobile &mdash; put them in the drawer
- Sticky nav: `sticky top-0 z-10 backdrop-blur` (translucent surface)
- Active link: subtle accent underline 2-4px below baseline, **not** a different color block

## Type

- Body: ≥ 16px on mobile (avoids iOS Safari auto-zoom on input focus)
- Eyebrow: `text-xs uppercase tracking-[0.2em] text-muted`
- Display heading: tight letter-spacing -0.02em to -0.025em via a custom `.display` class
- Heading scale: `text-3xl` on mobile, `text-4xl`/`text-5xl` on desktop with looser leading on mobile (`leading-tight sm:leading-[1.05]`)
- Line length: max ~70 characters for body copy (use `max-w-2xl` or `max-w-prose`)
- **Don't** justify text. Left-align (or center for hero); ragged right is more readable

## Color

- Use **OKLCH** for token definitions, not HSL. OKLCH is perceptually uniform &mdash; lightness 0.5 reads the same brightness across hues
- WCAG AA minimum: **4.5:1** for body text, **3:1** for large headings (≥18px or 14px bold)
- Active / selected states: ~8% tint of the foreground color, **not** a solid slab
- Don't use color alone to convey state &mdash; pair with text, icon, or border weight (some users have color-vision differences)
- Mid-tone neutrals (text-muted) often need a chroma tweak to feel "warm" or "cool" with the brand

## Spacing

- Container: `max-w-5xl mx-auto px-4 sm:px-6` (default project width)
- Section padding: `py-10 sm:py-20` &mdash; halves on mobile
- Gap between elements: `gap-3` to `gap-6`. Avoid `gap-2` &mdash; visually too tight in most contexts
- Form fields: vertical rhythm 1.25rem (20px) between rows, not less

## Animation

- Transitions: 120-150ms `ease` (faster than Material's 200ms; matches modern feel)
- Hover: only color, border, opacity. **Not** size or position changes
- Don't animate everything; restraint reads as quality
- Respect `prefers-reduced-motion: reduce` &mdash; disable non-essential animation for users who've opted out

## Accessibility

- `:focus-visible` ring on every interactive element
- `aria-label` on icon-only buttons
- `aria-expanded`, `aria-controls`, `aria-modal` on disclosure widgets (drawers, dialogs)
- `alt` text on every meaningful image; `alt=""` on decorative ones (don't omit)
- Keyboard tab order matches visual order; trap focus inside open modals/drawers
- Don't use color alone to convey state

## Anti-patterns

| Don't | Do instead |
|---|---|
| Square pills | `rounded-full` |
| Solid black active state | `color-mix(fg 8%, transparent)` + dark border |
| Sub-44px touch targets | `py-3` minimum on mobile |
| Text labels for social icons | Inline SVG with `aria-label` |
| Hover-only menus | Click/tap-to-open with focus management |
| Hamburger that hides important items | Drawer that includes everything |
| Center-aligned multi-line body copy on desktop | Left-align (faster to read) |
| Gradients on text | Solid color (clarity > flair) |
| Removing `:focus` outlines | Replace with a visible ring |
| Disabled buttons that look enabled | Lower opacity + `cursor-not-allowed` + `aria-disabled` |
| Body text < 16px on mobile | ≥ 16px (`text-base`) |
| Justified body copy | Left-aligned |
| Animating size on hover | Only color/opacity |
| 200ms+ animations | 120-150ms `ease` |

## When to deviate

These are defaults, not laws. Deviate when the brand explicitly demands it (a corner-heavy editorial brand might use square chips; an art-directed magazine might justify) and when the deviation is consistent across the system. The smell to avoid is *accidental* deviation &mdash; an active state that's harsh because nobody thought about it, not because the brand needed it to be.
