# Topic History — a mindmap companion to `last30days`

`last30days` makes you *current*. This makes you *grounded*: it renders the whole
**arc** of a topic - origins, eras, turning points, the last 30 days, and where
it's heading - as a quick, interactive **mindmap** you can scan in seconds.

## How it works (two halves)

1. **Research (the model / Claude):** gather the topic's historical arc with dated
   web lookbacks, and reuse any `last30days` raw file already on disk for the
   recent slice. Produce a markdown outline following the schema below.
2. **Render (this Python tool, offline):** `render_mindmap.py` wraps the outline
   in a self-contained [markmap](https://markmap.js.org/) HTML file and opens it.
   No network, no API keys - just templating, so it's deterministic and testable.

This mirrors how `last30days` splits work: the reasoning model does the
search/synthesis; Python does the mechanical rendering.

## Usage

```bash
PY=/opt/homebrew/bin/python3.13   # any Python 3.10+

# render an outline file and open it in the browser
$PY render_mindmap.py outlines/openai.md

# render only, no browser
$PY render_mindmap.py outlines/openai.md --no-open

# pipe an outline in
cat outlines/openai.md | $PY render_mindmap.py -

# custom output path
$PY render_mindmap.py outlines/openai.md --out ~/Desktop/openai.html
```

Output defaults to `~/Documents/Last30Days/mindmaps/<slug>-history.html` (next to
the `last30days` raw files).

## Outline schema

markmap turns heading + bullet nesting into branches. Keep leaves short and put a
year on milestones.

```markdown
# {Topic}
## Origins ({year range})
- 2015: milestone in one line
## {Era 2} ({year range})
- ...
## Now (last 30 days)
- pulled from the latest last30days run
## Where it's heading
- open questions / trajectory
```

- One `#` H1 = the root node (also becomes the page title).
- Each `##` = a major branch (an era / phase).
- Bullets = leaves. Sub-bullets nest one level deeper.

## Suggested flow with `last30days`

1. Run `/last30days {topic}` for the fresh slice (saves a raw `.md`).
2. Build the historical arc (model research) into `outlines/{slug}.md`, using the
   raw file for the "Now (last 30 days)" branch.
3. `render_mindmap.py outlines/{slug}.md` → interactive mindmap.

## Files

- `render_mindmap.py` — offline renderer (outline markdown → mindmap HTML).
- `template.html` — markmap HTML shell with `{{TITLE}}`, `{{DATE}}`, `{{MARKDOWN}}`.
- `outlines/` — saved topic outlines (e.g. `openai.md`).
- `test_render.py` — smoke tests for the renderer.

## Notes / limitations

- The mindmap HTML loads markmap from a CDN at view time, so viewing needs
  internet (rendering the file does not). Vendoring the JS for fully-offline
  viewing is a possible v2.
- Historical depth is only as good as what the model can find/recall; treat the
  arc as a scaffold, not a citation-grade record.
