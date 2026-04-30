#!/usr/bin/env python3
"""Update or remove a category in prototype/APPROVED.

The approval manifest is a flat key:value text file. This script is the
canonical way for skills to write into it — each skill calls it instead of
embedding manifest-write logic, so the format stays consistent and changes
to the format only touch one place.

Usage:
    python3 bump_approval.py <prototype_dir> <category> [value]

If value is omitted (or empty), the category line is removed from the
manifest. The manifest file is created with a header comment if it doesn't
exist yet.

Examples:
    # PRD signed off:
    bump_approval.py prototype/ prd prd/site-prd.md

    # CUJs aligned (group marker, not a path):
    bump_approval.py prototype/ cujs aligned

    # Switch the selected prototype variant:
    bump_approval.py prototype/ prototype hi-fi/cool-minimal-v2.html

    # Un-approve the prototype (drop the line entirely):
    bump_approval.py prototype/ prototype
"""
import sys
from pathlib import Path

DEFAULT_HEADER = """# Approved artifacts. One line per category. Paths are relative to prototype/.
# Edit when an artifact's approval state changes; the launcher and skills read
# this file to know which versions are the source of truth.
"""


def parse_lines(text):
    """Return list of (kind, key, raw_line) tuples preserving original order.

    kind is 'kv' for category:value lines, 'other' for comments / blank /
    malformed lines. We preserve all 'other' lines verbatim.
    """
    out = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or ":" not in stripped:
            out.append(("other", None, line))
            continue
        key = stripped.split(":", 1)[0].strip()
        if not key:
            out.append(("other", None, line))
        else:
            out.append(("kv", key, line))
    return out


def render(parsed):
    return "\n".join(line for _, _, line in parsed)


def bump(prototype_dir: Path, category: str, value: str) -> str:
    """Update or remove `category` in `prototype_dir / APPROVED`.

    Returns a one-line summary of what changed.
    """
    path = prototype_dir / "APPROVED"
    text = path.read_text(encoding="utf-8") if path.exists() else DEFAULT_HEADER
    parsed = parse_lines(text)

    new_line = f"{category}: {value}" if value else None

    # Find existing entry for this category
    found_idx = next(
        (i for i, (kind, key, _) in enumerate(parsed) if kind == "kv" and key == category),
        None,
    )

    if found_idx is not None:
        if new_line is not None:
            parsed[found_idx] = ("kv", category, new_line)
            action = f"updated {category}: {value}"
        else:
            del parsed[found_idx]
            action = f"removed {category}"
    else:
        if new_line is not None:
            # Append (with a leading blank if the file doesn't end in one)
            if parsed and parsed[-1][2].strip():
                parsed.append(("other", None, ""))
            parsed.append(("kv", category, new_line))
            action = f"added {category}: {value}"
        else:
            action = f"{category} already absent (no-op)"

    output = render(parsed)
    if not output.endswith("\n"):
        output += "\n"
    path.write_text(output, encoding="utf-8")
    return action


def main():
    if len(sys.argv) < 3:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    proto_dir = Path(sys.argv[1])
    if not proto_dir.is_dir():
        sys.exit(f"prototype directory not found: {proto_dir}")
    category = sys.argv[2]
    value = sys.argv[3] if len(sys.argv) > 3 else ""
    print(bump(proto_dir, category, value))


if __name__ == "__main__":
    main()
