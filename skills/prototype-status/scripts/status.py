#!/usr/bin/env python3
"""Print a Markdown summary of the prototype project's current state.

Reads prototype/APPROVED + scans the artifact directories and reports:
  - Render target
  - Pipeline stage status (PRD / CUJs / Theme / Wireframes / Prototypes / Components)
  - What's selected vs. what exists vs. what's missing
  - The next suggested step

Usage:
    python3 status.py [prototype_dir]

Default prototype_dir is ./prototype.
"""
import re
import sys
from pathlib import Path
from html import unescape

TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)


def read_approved(prototype_dir: Path) -> dict:
    path = prototype_dir / "APPROVED"
    if not path.exists():
        return {}
    approved: dict = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if key and value:
            approved[key] = value
    return approved


def list_html(directory: Path) -> list:
    if not directory.is_dir():
        return []
    return sorted(p for p in directory.iterdir()
                  if p.is_file() and p.suffix.lower() == ".html")


def title_of(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8")
        match = TITLE_RE.search(text)
        if match:
            return unescape(match.group(1).strip()) or path.stem
    except (OSError, UnicodeDecodeError):
        pass
    return path.stem


def stage_row(label: str, present: str, approved_value, suggested_next: list):
    """Format a one-line table row. Mutates suggested_next with the next gap."""
    if approved_value:
        status = f"✓ {approved_value}"
    elif present:
        status = f"⚠ exists, not approved ({present})"
        suggested_next.append(f"approve {label.lower()}")
    else:
        status = "— not started"
        suggested_next.append(f"start {label.lower()}")
    return f"| {label} | {status} |"


def main():
    prototype_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("prototype")
    if not prototype_dir.is_dir():
        sys.exit(f"prototype directory not found: {prototype_dir}")

    approved = read_approved(prototype_dir)
    target = approved.get("target", "(unset; defaults to web-spa)")

    # Inventory each artifact directory
    inventory = {
        "prd":        list_html(prototype_dir / "prd"),
        "cujs":       list_html(prototype_dir / "cujs"),
        "styles":     list_html(prototype_dir / "styles"),
        "wireframes": list_html(prototype_dir / "wireframes"),
        "hi-fi":      list_html(prototype_dir / "hi-fi"),
        "components": list_html(prototype_dir / "components"),
    }

    suggested = []
    rows = []

    # PRD
    rows.append(stage_row(
        "PRD",
        f"{len(inventory['prd'])} file(s)" if inventory["prd"] else "",
        approved.get("prd"),
        suggested,
    ))
    # CUJs
    cuj_count = len(inventory["cujs"])
    rows.append(stage_row(
        "CUJs",
        f"{cuj_count} flow(s)" if cuj_count else "",
        approved.get("cujs"),
        suggested,
    ))
    # Theme + styles
    rows.append(stage_row(
        "Theme",
        "tokens.css" if (prototype_dir / "tokens.css").exists() else "",
        approved.get("theme"),
        suggested,
    ))
    rows.append(stage_row(
        "Style preview",
        f"{len(inventory['styles'])} preview(s)" if inventory["styles"] else "",
        approved.get("styles"),
        suggested,
    ))
    # Wireframes
    rows.append(stage_row(
        "Wireframes",
        f"{len(inventory['wireframes'])} screen(s)" if inventory["wireframes"] else "",
        approved.get("wireframes"),
        suggested,
    ))
    # Prototypes
    rows.append(stage_row(
        "Prototypes",
        f"{len(inventory['hi-fi'])} variant(s)" if inventory["hi-fi"] else "",
        approved.get("prototype"),
        suggested,
    ))
    # Components
    rows.append(stage_row(
        "Components",
        f"{len(inventory['components'])} extracted" if inventory["components"] else "",
        approved.get("components"),
        suggested,
    ))

    # Render
    out = []
    out.append(f"# Project status: {prototype_dir.resolve().name}")
    out.append("")
    out.append(f"**Render target:** `{target}`")
    out.append("")
    out.append("## Pipeline")
    out.append("")
    out.append("| Stage | Status |")
    out.append("|---|---|")
    out.extend(rows)
    out.append("")

    # Approved details
    if approved:
        out.append("## Approval manifest")
        out.append("")
        out.append("```")
        for k, v in approved.items():
            out.append(f"{k}: {v}")
        out.append("```")
        out.append("")

    # Inventory details
    out.append("## Inventory")
    out.append("")
    for label, files in inventory.items():
        if not files:
            out.append(f"- **{label}/** — empty")
        else:
            out.append(f"- **{label}/** ({len(files)})")
            for f in files:
                marker = ""
                rel = f"{label}/{f.name}"
                # Mark approved entries
                for category, value in approved.items():
                    if value.rsplit(".", 1)[0] == rel.rsplit(".", 1)[0]:
                        marker = f" ← `{category}:`"
                        break
                out.append(f"  - {f.name} — _{title_of(f)}_{marker}")
    out.append("")

    # Next step suggestion
    out.append("## Suggested next step")
    out.append("")
    if suggested:
        out.append(f"**{suggested[0]}** (gap detected; first thing to fix)")
    else:
        # Everything is approved — recommend implementation-brief
        out.append("All design stages are approved. Next: run `implementation-brief` to convert the approved PRD + components into a developer-ready brief.")
    out.append("")

    print("\n".join(out))


if __name__ == "__main__":
    main()
