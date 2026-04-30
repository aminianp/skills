#!/usr/bin/env python3
"""Regenerate prototype/index.html as a single-page launcher.

Layout: header on top, persistent sidebar on the left grouping artifacts
into three sections (Product Definition, CUJs, Design), and a main pane
that switches between three views — a welcome message, a page (iframe),
and a list (for design containers like Wireframes that hold multiple
items). Clicks on sidebar items either render the artifact inline in the
iframe or, for design containers like Wireframes/HiFi where each item is
a full-page artifact, open the chosen item in a new tab.

The Tailwind v4 browser CDN does not resolve @import to external files
inside its tagged style blocks, so we inline the @theme contents at
regenerate time. tokens.css remains the human-readable source of truth;
design-themes writes there, and regenerate.py syncs.

Usage:
    python3 regenerate.py [prototype_dir]

Default prototype_dir is ./prototype.
"""
import re
import sys
from datetime import datetime
from html import escape, unescape
from pathlib import Path

# Sidebar layout: three sections, each with items.
# Item kinds:
#   "page"  — direct artifact, click opens in iframe
#   "auto"  — auto-discover .html files in `dir`, each becomes an inline page item
#   "list"  — container directory; click shows item list in main pane
#             list items use `item_mode` ("inline" or "newtab")
SIDEBAR_SECTIONS = [
    {
        "label": "Product Definition",
        "items": [
            {"kind": "page", "label": "PRD", "src": "prd/site-prd.html"},
            {"kind": "page", "label": "FAQ", "src": "prd/site-prd-faq.html"},
            {"kind": "page", "label": "Decision Log", "src": "prd/site-prd-decision-log.html"},
        ],
    },
    {
        "label": "CUJs",
        "items": [
            {"kind": "auto", "dir": "cujs"},
        ],
    },
    {
        "label": "Design",
        "items": [
            {"kind": "list", "label": "Styles", "dir": "styles", "item_mode": "inline"},
            {"kind": "list", "label": "Wireframes", "dir": "wireframes", "item_mode": "newtab"},
            {"kind": "list", "label": "HiFi", "dir": "hi-fi", "item_mode": "newtab"},
            {"kind": "list", "label": "Components", "dir": "components", "item_mode": "inline"},
        ],
    },
]

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
THEME_BLOCK_RE = re.compile(r"@theme\s*\{[^}]*\}", re.DOTALL)

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
    """Extract the @theme block from prototype/tokens.css; fall back to default."""
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
    """Read <title> from an HTML file; fall back to filename stem.

    HTML entities in the <title> (e.g., &amp;) are decoded to their literal
    characters here. The rendering callsite re-encodes via html.escape so we
    don't end up with &amp;amp; in the launcher.
    """
    try:
        text = html_path.read_text(encoding="utf-8")
        match = TITLE_RE.search(text)
        if match:
            title = unescape(match.group(1).strip())
            if title:
                return title
    except (OSError, UnicodeDecodeError):
        pass
    return html_path.stem


def list_html_files(directory: Path) -> list[tuple[str, str]]:
    """Return (display_name, href) pairs for HTML files in a directory."""
    if not directory.is_dir():
        return []
    files = sorted(
        p for p in directory.iterdir()
        if p.is_file() and p.suffix.lower() == ".html"
    )
    return [(extract_title(p), f"{directory.name}/{p.name}") for p in files]


def sidebar_link(label: str, src: str, section: str) -> str:
    """Sidebar inline (nav-page) link."""
    return (
        f'          <li><a class="nav-page block px-2 py-1.5 rounded text-sm '
        f'cursor-pointer hover:bg-border/30" '
        f'data-src="{escape(src, quote=True)}" '
        f'data-section="{escape(section, quote=True)}" '
        f'data-label="{escape(label, quote=True)}">{escape(label)}</a></li>'
    )


def sidebar_list_link(label: str, list_id: str, count: int, section: str) -> str:
    """Sidebar list (nav-list) link with count badge."""
    return (
        f'          <li><a class="nav-list flex items-center justify-between px-2 py-1.5 rounded text-sm '
        f'cursor-pointer hover:bg-border/30" '
        f'data-list="{escape(list_id, quote=True)}" '
        f'data-section="{escape(section, quote=True)}" '
        f'data-label="{escape(label, quote=True)}">'
        f'<span>{escape(label)}</span><span class="text-muted text-xs tabular-nums">{count}</span>'
        f'</a></li>'
    )


def render_sidebar(prototype_dir: Path) -> tuple[str, str]:
    """Return (sidebar_html, list_templates_html)."""
    sections_html: list[str] = []
    templates_html: list[str] = []

    for section in SIDEBAR_SECTIONS:
        section_label = section["label"]
        items_html: list[str] = []
        for item in section["items"]:
            kind = item["kind"]
            if kind == "page":
                items_html.append(sidebar_link(item["label"], item["src"], section_label))
            elif kind == "auto":
                files = list_html_files(prototype_dir / item["dir"])
                if not files:
                    items_html.append(
                        '          <li class="px-2 py-1.5 text-sm text-muted italic">&mdash; none &mdash;</li>'
                    )
                for name, href in files:
                    items_html.append(sidebar_link(name, href, section_label))
            elif kind == "list":
                files = list_html_files(prototype_dir / item["dir"])
                items_html.append(
                    sidebar_list_link(item["label"], item["dir"], len(files), section_label)
                )
                templates_html.append(render_list_template(item, files))

        sections_html.append(
            f'      <div class="mb-6">\n'
            f'        <h3 class="text-xs font-semibold uppercase tracking-wider text-muted pb-1.5 mb-2 border-b border-border">'
            f'{escape(section_label)}</h3>\n'
            f'        <ul class="space-y-0.5">\n'
            + "\n".join(items_html) + "\n"
            f'        </ul>\n'
            f'      </div>'
        )

    return "\n".join(sections_html), "\n".join(templates_html)


def render_list_template(item: dict, files: list[tuple[str, str]]) -> str:
    """Render a <template> element holding the item list for a Design container."""
    list_id = item["dir"]
    item_mode = item["item_mode"]
    section_label = "Design"
    parent_label = item["label"]

    if not files:
        body = (
            '<p class="text-sm text-muted italic">&mdash; no items &mdash;</p>'
        )
    else:
        lis: list[str] = []
        for name, href in files:
            if item_mode == "newtab":
                lis.append(
                    f'<li><a href="{escape(href, quote=True)}" target="_blank" rel="noopener" '
                    f'class="block px-3 py-2 rounded border border-border bg-surface hover:border-accent hover:text-accent text-sm">'
                    f'{escape(name)}</a></li>'
                )
            else:  # inline
                lis.append(
                    f'<li><a class="nav-page block px-3 py-2 rounded border border-border bg-surface '
                    f'hover:border-accent hover:text-accent text-sm cursor-pointer" '
                    f'data-src="{escape(href, quote=True)}" '
                    f'data-section="{escape(parent_label, quote=True)}" '
                    f'data-label="{escape(name, quote=True)}">{escape(name)}</a></li>'
                )
        body = '<ul class="space-y-2">' + "".join(lis) + "</ul>"

    return f'    <template id="template-{escape(list_id, quote=True)}">{body}</template>'


SPA_SCRIPT = """
    (function () {
      function showView(id) {
        ['welcome-view', 'page-view', 'list-view'].forEach(function (v) {
          document.getElementById(v).hidden = (v !== id);
        });
        document.getElementById('header-close').hidden = (id === 'welcome-view');
      }
      function showPage(src) {
        document.getElementById('page-frame').src = src;
        showView('page-view');
      }
      function showList(listId, section, label) {
        var template = document.getElementById('template-' + listId);
        var content = document.getElementById('list-content');
        content.innerHTML = template ? template.innerHTML : '<p class="text-muted">No items.</p>';
        document.getElementById('list-section').textContent = section || '';
        document.getElementById('list-label').textContent = label || '';
        showView('list-view');
      }
      document.body.addEventListener('click', function (e) {
        var link = e.target.closest('.nav-page, .nav-list');
        if (!link) return;
        e.preventDefault();
        if (link.classList.contains('nav-page')) {
          showPage(link.dataset.src);
        } else {
          showList(link.dataset.list, link.dataset.section, link.dataset.label);
        }
      });
      document.getElementById('header-close').addEventListener('click', function (e) {
        e.preventDefault();
        document.getElementById('page-frame').src = '';
        showView('welcome-view');
      });
    })();
"""


def regenerate(prototype_dir: Path) -> None:
    if not prototype_dir.is_dir():
        sys.exit(f"prototype directory not found: {prototype_dir}")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    sidebar_html, templates_html = render_sidebar(prototype_dir)
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
    iframe {{ background: var(--color-bg); }}
  </style>
</head>
<body class="bg-bg text-fg font-sans antialiased">
  <header class="border-b border-border px-6 py-3 flex items-center justify-between bg-surface shrink-0">
    <div>
      <h1 class="text-base font-semibold tracking-tight">Prototype</h1>
      <p class="text-xs text-muted">Pick something from the sidebar to view it inline. Wireframes / HiFi open in a new tab.</p>
    </div>
    <div class="flex items-center gap-4">
      <a id="header-close" hidden class="text-xs text-muted hover:text-accent cursor-pointer">Close &times;</a>
      <div class="text-xs text-muted text-right space-y-0.5">
        <div>Last updated {timestamp}</div>
        <div class="font-mono">localhost:3000</div>
      </div>
    </div>
  </header>

  <div class="flex-1 flex min-h-0">
    <aside class="w-56 shrink-0 border-r border-border bg-surface px-4 py-6 overflow-y-auto">
{sidebar_html}
    </aside>

    <main class="flex-1 flex flex-col min-w-0 bg-bg">
      <div id="welcome-view" class="px-8 py-12 max-w-2xl">
        <h2 class="text-2xl font-semibold mb-3 tracking-tight">Welcome</h2>
        <p class="text-muted leading-relaxed">Pick something from the sidebar.</p>
        <ul class="mt-6 space-y-2 text-sm text-muted">
          <li><strong class="text-fg">Product Definition</strong> &mdash; the PRD, its FAQ, and the decision log.</li>
          <li><strong class="text-fg">CUJs</strong> &mdash; job-anchored user journeys with Mermaid flow diagrams.</li>
          <li><strong class="text-fg">Design</strong> &mdash; wireframes and hi-fi prototypes (open in new tabs); style and component pages (open inline).</li>
        </ul>
      </div>

      <div id="page-view" hidden class="flex flex-col h-full min-h-0">
        <iframe id="page-frame" src="" class="flex-1 w-full border-0"></iframe>
      </div>

      <div id="list-view" hidden class="flex flex-col h-full min-h-0">
        <div class="border-b border-border px-6 py-2.5 flex items-center justify-between bg-surface text-sm shrink-0">
          <div class="text-muted">
            <span id="list-section">Section</span>
            <span class="mx-1.5">/</span>
            <span id="list-label" class="text-fg font-medium">Label</span>
          </div>
          <div class="text-xs text-muted">List</div>
        </div>
        <div class="flex-1 overflow-y-auto px-8 py-8">
          <div id="list-content" class="max-w-2xl"></div>
        </div>
      </div>

{templates_html}
    </main>
  </div>

  <footer class="border-t border-border px-6 py-2 text-xs text-muted flex items-center justify-between bg-surface shrink-0">
    <div>Generated by <code class="font-mono">prototype-update</code></div>
    <div>Stop server: <code class="px-1 py-0.5 rounded bg-border/40 text-fg font-mono">kill $(cat prototype/.server.pid)</code></div>
  </footer>

  <script>{SPA_SCRIPT}</script>
</body>
</html>
"""

    out = prototype_dir / "index.html"
    out.write_text(html, encoding="utf-8")
    print(f"Regenerated {out}")


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("prototype")
    regenerate(target.resolve())
