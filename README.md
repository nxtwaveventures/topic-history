# Topic History 🧭

A Claude Code plugin that renders the **full historical arc** of any topic -
origins, eras, turning points, the last 30 days, and where it's heading - as a
quick **interactive mindmap**.

It's a grounding companion to [`last30days`](https://github.com/mvanhorn/last30days-skill):
where `last30days` makes you *current*, Topic History makes you a *master*. Being
up to date on the last 30 days isn't the same as understanding how something got
to where it is - this fills that gap, fast.

![arc: origins → eras → turning points → now → trajectory](https://img.shields.io/badge/arc-origins%20%E2%86%92%20now%20%E2%86%92%20trajectory-0f172a)

## How it works

Two halves, mirroring how `last30days` splits work:

1. **The model (Claude) researches the arc** via dated web lookbacks and reuses any
   `last30days` raw file already on disk for the recent slice, producing a markdown
   outline.
2. **An offline Python renderer** (`render_mindmap.py`) wraps that outline in a
   self-contained [markmap](https://markmap.js.org/) HTML and opens it. The renderer
   does no network and needs no API keys, so it's deterministic and unit-tested.

## Install (Claude Code)

```text
/plugin marketplace add nxtwaveventures/topic-history
/plugin install topic-history@topic-history
/reload-plugins
```

Then:

```text
/topic-history OpenAI
```

Requires Python 3.10+ (`brew install python@3.13` on macOS).

## Use the renderer directly

```bash
PY=python3.13
PY skills/topic-history/scripts/render_mindmap.py skills/topic-history/outlines/openai.md
# --no-open to skip the browser, --out PATH to redirect, '-' to read an outline from stdin
```

Output defaults to `~/Documents/Last30Days/mindmaps/<slug>-history.html`.

## Outline schema

```markdown
# {Topic}
## Origins ({year range})
- 2015: milestone
## {Era} ({year range})
- ...
## Now (last 30 days)
- from the latest last30days run
## Where it's heading
- trajectory / open questions
```

`#` = root + page title; each `##` = a branch (era); bullets = leaves.

## Layout

```
.claude-plugin/        plugin.json + marketplace.json (installable)
commands/              /topic-history slash command
skills/topic-history/  SKILL.md (drives the research + render)
  scripts/             render_mindmap.py, template.html, test_render.py
  outlines/            saved example outlines (openai.md)
docs/                  design spec
```

## Test

```bash
cd skills/topic-history/scripts && python3 test_render.py
```

## Limitations

- Viewing the mindmap needs internet (markmap loads from a CDN); rendering does not.
  Vendoring the JS for offline viewing is a planned v2.
- Historical depth is bounded by what the model can find/recall - treat the arc as a
  scaffold, not a citation-grade record.

## License

MIT
