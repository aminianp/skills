#!/usr/bin/env python3
"""Regenerate prototype/index.html by scanning artifact directories.

Reads `.html` files from prd/, cujs/, wireframes/, styles/, and hi-fi/
and rewrites the launcher page so each file is linked. Filenames map
to display names via the file's <title>, falling back to the stem.

The generated page uses Tailwind v4 (loaded from CDN) with the @theme
block inlined directly into the launcher's <style type="text/tailwindcss">
element. Theme contents are read from prototype/tokens.css at regenerate
time. We inline rather than @import because the v4 browser CDN does not
resolve external @imports inside its tagged style blocks; theme classes
silently fail without inlining.

Usage:
    python3 regenerate.py [prototype_dir]

Default prototype_dir is ./prototype.
"""
import re
import sys
from datetime import datetime
from html import escape
from pathlib import Path

SECTIONS = [
    ("PRD", "prd"),
    ("CUJs", "cujs"),
    ("Wireframes", "wireframes"),
    ("Styles", "styles"),
    ("Hi-fi", "hi-fi"),
]

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
THEME_BLOCK_RE = re.compile(r"@theme\s*\{[^}]*\}", re.DOTALL)

EMPTY_HINT = (
    'No artifacts yet. Run '
    '<code class="px-1.5 py-0.5 rounded bg-border/40 text-fg text-xs font-mono">/design-wireframes</code> '
    'to create wireframes, or drop files into the artifact subdirectories &mdash; then run '
    '<code class="px-1.5 py-0.5 rounded bg-border/40 text-fg text-xs font-mono">/prototype-update</code> '
    'to refresh this page.'
)

DEFAULT_THEME = """@theme {
  --color-bg: oklch(0.99 0 0);
  --color-surface: oklch(1 0 0);
  --color-fg: oklch(0.18 0 0);
  --color-muted: oklch(0.5 0 0);
  --color-border: oklch(0.92 0 0);
  --color-primary: oklch(0.28 0 0);
  --color-primary-fg: oklch(0.99 0 0);
  --color-accent: oklch(0.55 0 0);
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
  --font-mono: "SF Mono", Menlo, Consolas, monospace;
  --radius: 0.375rem;
}"""


def read_theme_block(prototype_dir: Path) -> str:
    """Extract the @theme {...} block from prototype/tokens.css.

    The Tailwind v4 browser CDN does not resolve @import to external files
    inside <style type="text/tailwindcss"> blocks, so we inline the @theme
    contents at regenerate time. tokens.css remains the human-readable
    source of truth; design-themes writes there, and regenerate.py syncs.
    """
    tokens_path = prototype_dir / "tokens.css"
    if tokens_path.exists():
        try:
            content = tokens_path.read_text(encoding="utf-8")
            match = THEME_BLOCK_RE.search(content)
            if match:
                return match.group(0)
        except (OSError, UnicodeDecodeError):
            pass
    return DEFAULT_THEME


def extract_title(html_path: Path) -> str:
    """Read <title> from an HTML file; fall back to filename stem."""
    try:
        text = html_path.read_text(encoding="utf-8")
        match = TITLE_RE.search(text)
        if match:
            title = match.group(1).strip()
            if title:
                return title
    except (OSError, UnicodeDecodeError):
        pass
    return html_path.stem


def list_artifacts(section_dir: Path) -> list[tuple[str, str]]:
    """Return (display_name, href) pairs for HTML files in a section dir."""
    if not section_dir.is_dir():
        return []
    files = sorted(
        p for p in section_dir.iterdir()
        if p.is_file() and p.suffix.lower() == ".html"
    )
    return [(extract_title(p), f"{section_dir.name}/{p.name}") for p in files]


def render_sidebar(section_data: list[dict]) -> str:
    items = []
    for d in section_data:
        items.append(
            f'        <a href="#{d["subdir"]}" class="flex items-center justify-between px-2 py-1.5 rounded hover:bg-border/30">\n'
            f'          <span>{escape(d["label"])}</span><span class="text-muted text-xs tabular-nums">{d["count"]}</span>\n'
            f'        </a>'
        )
    return "\n".join(items)


def render_section(label: str, subdir: str, items: list[tuple[str, str]]) -> str:
    if not items:
        body = '<ul class="space-y-1"><li class="text-sm text-muted italic">&mdash; none &mdash;</li></ul>'
    else:
        lis = "".join(
            f'<li class="text-sm"><a href="{escape(href)}" target="_blank" rel="noopener" '
            f'class="text-fg underline decoration-accent underline-offset-2 hover:text-accent">'
            f'{escape(name)}</a></li>'
            for name, href in items
        )
        body = f'<ul class="space-y-1">{lis}</ul>'
    return (
        f'        <section id="{escape(subdir)}" class="mb-10">\n'
        f'          <h2 class="text-xs font-semibold uppercase tracking-wider text-muted mb-3">{escape(label)}</h2>\n'
        f'          {body}\n'
        '        </section>'
    )


def regenerate(prototype_dir: Path) -> None:
    if not prototype_dir.is_dir():
        sys.exit(f"prototype directory not found: {prototype_dir}")

    section_data = []
    for label, subdir in SECTIONS:
        items = list_artifacts(prototype_dir / subdir)
        section_data.append({"label": label, "subdir": subdir, "items": items, "count": len(items)})

    has_any = any(d["count"] > 0 for d in section_data)
    total = sum(d["count"] for d in section_data)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    sidebar_html = render_sidebar(section_data)
    sections_html = "\n".join(render_section(d["label"], d["subdir"], d["items"]) for d in section_data)
    hint_block = (
        ""
        if has_any
        else f'        <div class="rounded-md border border-border bg-surface px-4 py-3 mb-8 text-sm text-muted leading-relaxed">{EMPTY_HINT}</div>\n'
    )
    theme_block = read_theme_block(prototype_dir)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Prototype</title>
  <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
  <style type="text/tailwindcss">
    /* @theme:start — synced from prototype/tokens.css */
    {theme_block}
    /* @theme:end */
  </style>
  <style>
    html, body {{ height: 100%; }}
    body {{ display: flex; flex-direction: column; }}
    .layout {{ display: flex; flex: 1; min-height: 0; }}
    .layout > main {{ overflow-y: auto; }}
    section[id] {{ scroll-margin-top: 1rem; }}
  </style>
</head>
<body class="bg-bg text-fg font-sans antialiased">
  <header class="border-b border-border px-6 py-3 flex items-center justify-between bg-surface shrink-0">
    <div>
      <h1 class="text-base font-semibold tracking-tight">Prototype</h1>
      <p class="text-xs text-muted">Rapid-prototyping launcher &middot; links open in new tabs</p>
    </div>
    <div class="text-xs text-muted text-right space-y-0.5">
      <div>Last updated {timestamp}</div>
      <div class="font-mono">localhost:3000</div>
    </div>
  </header>

  <div class="layout">
    <aside class="w-52 shrink-0 border-r border-border bg-surface p-4">
      <nav class="text-sm space-y-0.5">
{sidebar_html}
      </nav>
    </aside>

    <main class="px-8 py-8">
      <div class="max-w-2xl">
{hint_block}{sections_html}
      </div>
    </main>
  </div>

  <footer class="border-t border-border px-6 py-2 text-xs text-muted flex items-center justify-between bg-surface shrink-0">
    <div>Generated by <code class="font-mono">prototype-update</code></div>
    <div>Stop server: <code class="px-1 py-0.5 rounded bg-border/40 text-fg font-mono">kill $(cat prototype/.server.pid)</code></div>
  </footer>
</body>
</html>
"""

    out = prototype_dir / "index.html"
    out.write_text(html, encoding="utf-8")
    print(f"Regenerated {out} ({total} artifact{'s' if total != 1 else ''})")


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("prototype")
    regenerate(target.resolve())
