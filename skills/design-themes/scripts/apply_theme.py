#!/usr/bin/env python3
"""Propagate prototype/tokens.css @theme block to every HTML file.

Why this script exists: the Tailwind v4 browser CDN does not resolve @import
to external files inside <style type="text/tailwindcss"> blocks, so each HTML
artifact in the prototype site inlines a copy of the @theme block between
`/* @theme:start */` and `/* @theme:end */` marker comments. tokens.css
remains the human-readable canonical source; this script syncs it into every
HTML file so a refresh in the browser actually reflects the change.

design-themes calls this as the final step after writing prototype/tokens.css.
prototype-update's regenerator handles the launcher (index.html) on its own,
so this script focuses on the artifact pages — though it will also update
index.html if it carries the markers.

Usage:
    python3 apply_theme.py [prototype_dir]

Default prototype_dir is ./prototype.
"""
import re
import sys
from pathlib import Path

THEME_BLOCK_RE = re.compile(r"@theme\s*\{[^}]*\}", re.DOTALL)
INLINE_THEME_RE = re.compile(
    r"(/\*\s*@theme:start[^\n]*\*/)\s*(?:.*?)\s*(/\*\s*@theme:end\s*\*/)",
    re.DOTALL,
)


def read_theme_block(prototype_dir: Path) -> str:
    tokens_path = prototype_dir / "tokens.css"
    if not tokens_path.exists():
        sys.exit(f"tokens.css not found at {tokens_path}")
    content = tokens_path.read_text(encoding="utf-8")
    match = THEME_BLOCK_RE.search(content)
    if not match:
        sys.exit(f"no @theme block found in {tokens_path}")
    return match.group(0)


def apply_theme(prototype_dir: Path) -> None:
    if not prototype_dir.is_dir():
        sys.exit(f"prototype directory not found: {prototype_dir}")

    theme_block = read_theme_block(prototype_dir)
    indented = "\n".join("    " + line for line in theme_block.splitlines())
    updated: list[Path] = []
    no_markers: list[Path] = []
    unchanged: list[Path] = []

    for path in sorted(prototype_dir.rglob("*.html")):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        rel = path.relative_to(prototype_dir)
        if not INLINE_THEME_RE.search(text):
            no_markers.append(rel)
            continue

        new_text = INLINE_THEME_RE.sub(
            lambda m: f"{m.group(1)}\n{indented}\n    {m.group(2)}",
            text,
        )
        if new_text == text:
            unchanged.append(rel)
            continue

        path.write_text(new_text, encoding="utf-8")
        updated.append(rel)

    print(f"Updated {len(updated)} file(s) with theme from tokens.css:")
    for p in updated:
        print(f"  ✓ {p}")
    if unchanged:
        print(f"\n{len(unchanged)} file(s) already had matching theme:")
        for p in unchanged:
            print(f"  = {p}")
    if no_markers:
        print(f"\n{len(no_markers)} file(s) skipped (no @theme:start/@theme:end markers):")
        for p in no_markers:
            print(f"  - {p}")


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("prototype")
    apply_theme(target.resolve())
