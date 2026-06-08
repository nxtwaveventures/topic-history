# Topic History Mindmap — Design (as built)

Date: 2026-06-08
Status: Built and verified (user requested fully-automatic build; formal approval
gate waived by the user with "fully automatic mode").

## Problem

`last30days` makes a user *current* on a topic but not a *master* — it only reaches
~30 days back. The user wants a companion that shows the *historical arc* of a topic,
rendered quickly as a **mindmap**, for deeper understanding.

## Decisions

- **History source — Hybrid.** The reasoning model (Claude, which has WebSearch)
  gathers the arc on demand via dated lookbacks and reuses any `last30days` raw `.md`
  already on disk for the recent slice. No API keys required.
- **Output — interactive mindmap HTML** via [markmap](https://markmap.js.org/)
  autoloader (CDN), self-contained single file, opens in the browser with a native
  fit/zoom toolbar.
- **Work split (mirrors `last30days`)** — model does research/synthesis into a
  markdown outline; an offline Python renderer does the mechanical HTML rendering.
  Renderer does no network, so it is deterministic and unit-testable.
- **Location** — `/Users/anamika/Projects/researcher/topic-history/` (NOT the plugin
  cache, which is overwritten on plugin update).

## Components

- `render_mindmap.py` — outline markdown → mindmap HTML; `--out`, `--title`,
  `--no-open`, and stdin (`-`) supported. Output defaults to
  `~/Documents/Last30Days/mindmaps/<slug>-history.html`.
- `template.html` — markmap-autoloader shell with `{{TITLE}}`, `{{DATE}}`,
  `{{MARKDOWN}}` placeholders; native toolbar enabled.
- `outlines/` — saved per-topic outlines (demo: `openai.md`).
- `test_render.py` — offline smoke tests (title derivation, slugify, substitution,
  empty-input rejection). All passing.

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

H1 = root + page title; each `##` = a branch (era); bullets = leaves.

## Verification

- `test_render.py`: all smoke tests pass.
- CDN assets confirmed reachable (autoloader 200; the earlier manual
  `markmap-lib` browser path 404'd and was replaced by the autoloader).
- End-to-end demo (`outlines/openai.md`) rendered and opened in the browser.

## Known limitations / possible v2

- Viewing needs internet (markmap JS loads from CDN); rendering does not. Vendoring
  the JS would make viewing fully offline.
- Historical depth is bounded by what the model can find/recall — the arc is a
  scaffold, not a citation-grade record.
- Possible v2: a thin wrapper command that runs `last30days` then auto-builds the
  outline's "Now" branch from the freshly-saved raw file.
