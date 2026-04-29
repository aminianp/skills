#!/usr/bin/env python3
"""Regenerate prototype/index.html by scanning artifact directories.

Reads `.html` files from prd/, cujs/, wireframes/, styles/, and hi-fi/
and rewrites the launcher page so each file is linked. Filenames map
to display names via the file's <title>, falling back to the stem.

The generated page uses Tailwind v4 (loaded from CDN) and pulls design
tokens from /tokens.css via the inline `@import` pattern that the
Tailwind browser script supports.

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

EMPTY_HINT = (
    'No artifacts yet. Run '
    '<code class="px-1.5 py-0.5 rounded bg-border/40 text-fg text-xs font-mono">/design-wireframes</code> '
    'to create wireframes, or drop files into '
    '<code class="px-1.5 py-0.5 rounded bg-border/40 text-fg text-xs font-mono">prototype/wireframes/</code> '
    '&mdash; then run '
    '<code class="px-1.5 py-0.5 rounded bg-border/40 text-fg text-xs font-mono">/prototype-update</code> '
    'to refresh this page.'
)


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


def render_section(label: str, items: list[tuple[str, str]]) -> str:
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
        '    <section class="border-t border-border py-5">\n'
        f'      <h2 class="text-xs font-semibold uppercase tracking-wider text-muted mb-3">{label}</h2>\n'
        f'      {body}\n'
        '    </section>'
    )


def regenerate(prototype_dir: Path) -> None:
    if not prototype_dir.is_dir():
        sys.exit(f"prototype directory not found: {prototype_dir}")

    section_lists = [
        (label, list_artifacts(prototype_dir / subdir))
        for label, subdir in SECTIONS
    ]
    has_any_artifacts = any(items for _, items in section_lists)

    sections_html = "\n".join(render_section(label, items) for label, items in section_lists)
    hint_block = (
        ""
        if has_any_artifacts
        else f'    <div class="rounded-md border border-border bg-surface px-4 py-3 mb-6 text-sm text-muted leading-relaxed">{EMPTY_HINT}</div>\n'
    )
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Prototype</title>
  <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
  <style type="text/tailwindcss">@import "/tokens.css";</style>
</head>
<body class="bg-bg text-fg font-sans antialiased min-h-screen">
  <main class="max-w-3xl mx-auto px-6 py-12">
    <header class="mb-8">
      <h1 class="text-3xl font-semibold tracking-tight">Prototype</h1>
      <p class="text-sm text-muted mt-1">Rapid-prototyping launcher. Links open in new tabs. Last updated {timestamp}.</p>
    </header>
{hint_block}{sections_html}
  </main>
</body>
</html>
"""

    out = prototype_dir / "index.html"
    out.write_text(html, encoding="utf-8")
    artifact_count = sum(len(items) for _, items in section_lists)
    print(f"Regenerated {out} ({artifact_count} artifact{'s' if artifact_count != 1 else ''})")


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("prototype")
    regenerate(target.resolve())
