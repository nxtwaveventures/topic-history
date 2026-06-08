#!/usr/bin/env python3
"""
render_mindmap.py — turn a topic-history markdown outline into a self-contained
interactive mindmap (markmap) HTML file and open it.

This is the *mechanical* half of the Topic History addon. It does NO network
research itself: the reasoning model (Claude) produces the markdown outline by
researching the topic's arc, then hands the outline here to be rendered. Keeping
this offline makes it deterministic and easy to test.

Usage:
    python3 render_mindmap.py OUTLINE.md            # render + open in browser
    python3 render_mindmap.py OUTLINE.md --no-open  # render only
    cat OUTLINE.md | python3 render_mindmap.py -     # read outline from stdin
    python3 render_mindmap.py OUTLINE.md --out ~/Documents/Last30Days/mindmaps/x.html

Outline schema the model should produce (markmap uses heading + bullet nesting):

    # {Topic}
    ## Origins ({year range})
    - milestone — one line, with a year
    ## {Era 2} ({year range})
    - ...
    ## Now (last 30 days)
    - pulled from the latest last30days run
    ## Where it's heading
    - open questions / trajectory

Each `##` becomes a major branch; bullets become leaves. Keep leaves short.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import re
import sys
import webbrowser
from pathlib import Path

TEMPLATE_PATH = Path(__file__).resolve().parent / "template.html"
DEFAULT_OUT_DIR = Path.home() / "Documents" / "Last30Days" / "mindmaps"


def _slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "topic"


def _derive_title(markdown: str) -> str:
    for line in markdown.splitlines():
        m = re.match(r"\s*#\s+(.*\S)", line)
        if m:
            return m.group(1).strip()
    return "Untitled Topic"


def render(markdown: str, out_path: Path, *, title: str | None = None) -> Path:
    if not markdown.strip():
        raise ValueError("Outline markdown is empty — nothing to render.")
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    title = title or _derive_title(markdown)
    today = _dt.date.today().isoformat()
    # Order matters: inject MARKDOWN last so a title/date containing the literal
    # placeholder text can't collide with the content swap.
    html = (
        template
        .replace("{{TITLE}}", title)
        .replace("{{DATE}}", today)
        .replace("{{MARKDOWN}}", markdown)
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    return out_path


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Render a topic-history outline into a mindmap HTML.")
    p.add_argument("outline", help="Path to the markdown outline, or '-' for stdin.")
    p.add_argument("--out", help="Output HTML path. Default: ~/Documents/Last30Days/mindmaps/<slug>.html")
    p.add_argument("--title", help="Override the page title (default: first H1 in the outline).")
    p.add_argument("--no-open", action="store_true", help="Do not open the result in a browser.")
    args = p.parse_args(argv)

    if args.outline == "-":
        markdown = sys.stdin.read()
    else:
        src = Path(args.outline).expanduser()
        if not src.is_file():
            print(f"ERROR: outline not found: {src}", file=sys.stderr)
            return 1
        markdown = src.read_text(encoding="utf-8")

    title = args.title or _derive_title(markdown)
    if args.out:
        out_path = Path(args.out).expanduser()
    else:
        out_path = DEFAULT_OUT_DIR / f"{_slugify(title)}-history.html"

    try:
        result = render(markdown, out_path, title=title)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    print(f"Mindmap written to {result}")
    if not args.no_open:
        webbrowser.open(result.as_uri())
        print("Opened in browser.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
