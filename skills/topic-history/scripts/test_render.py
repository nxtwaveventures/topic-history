"""Smoke tests for render_mindmap.py — offline, no browser, no network.

Run: python3 test_render.py   (exits non-zero on failure)
"""
import sys
import tempfile
from pathlib import Path

import render_mindmap as r


def _check(cond, msg):
    if not cond:
        print(f"FAIL: {msg}")
        sys.exit(1)
    print(f"ok: {msg}")


def test_derive_title():
    _check(r._derive_title("# Hello World\n## x") == "Hello World", "derive title from H1")
    _check(r._derive_title("no heading here") == "Untitled Topic", "fallback title")


def test_slugify():
    _check(r._slugify("OpenAI: The Arc!") == "openai-the-arc", "slugify punctuation")
    _check(r._slugify("   ") == "topic", "slugify empty fallback")


def test_render_substitutes_and_has_no_placeholders():
    md = "# Demo\n## Origins (2015)\n- founded\n## Now\n- shipping\n"
    with tempfile.TemporaryDirectory() as d:
        out = Path(d) / "demo.html"
        r.render(md, out, title="Demo")
        html = out.read_text(encoding="utf-8")
    _check("{{" not in html, "no leftover placeholders")
    _check("## Origins (2015)" in html, "outline injected verbatim")
    _check("<title>Demo" in html, "title applied")
    _check("markmap-autoloader" in html, "markmap loader present")


def test_empty_outline_rejected():
    try:
        r.render("   ", Path(tempfile.gettempdir()) / "x.html")
    except ValueError:
        print("ok: empty outline rejected")
        return
    print("FAIL: empty outline should raise ValueError")
    sys.exit(1)


if __name__ == "__main__":
    test_derive_title()
    test_slugify()
    test_render_substitutes_and_has_no_placeholders()
    test_empty_outline_rejected()
    print("\nAll smoke tests passed.")
