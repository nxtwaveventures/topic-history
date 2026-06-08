---
name: topic-history
description: Render the full historical arc of a topic (origins, eras, turning points, the last 30 days, and where it's heading) as a quick interactive mindmap. A grounding companion to last30days - where last30days makes you current, this makes you a master. Use when the user asks for a topic's history, background, timeline, evolution, or a mindmap of a subject.
---

# Topic History — historical arc as a mindmap

`last30days` tells you what happened in the last 30 days. **This skill tells you
the whole story** - how a topic got to today - and renders it as an interactive
mindmap you can scan in seconds.

Two halves:
1. **You (the model) research the arc** and write a markdown outline.
2. **`scripts/render_mindmap.py` (offline) renders it** into a self-contained
   markmap HTML and opens it. No API keys, no network in the renderer.

## Step 0 — Resolve Python (3.10+)

```bash
for py in python3.13 python3.12 python3.11 python3.10 python3; do
  command -v "$py" >/dev/null 2>&1 || continue
  "$py" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3,10) else 1)' && { TH_PY="$py"; break; }
done
[ -z "${TH_PY:-}" ] && echo "ERROR: need Python 3.10+ (try: brew install python@3.13)" >&2
```

## Step 1 — Build the historical arc (research)

If no topic was given, ask for one and stop. Otherwise:

- Run 3-6 dated web searches covering: **origins/founding**, **major eras/phases**,
  **turning points/controversies**, and **current state**. Prefer concrete years.
- If a `last30days` raw file exists for this topic (look in
  `${LAST30DAYS_MEMORY_DIR:-$HOME/Documents/Last30Days}/<slug>-raw*.md`), mine it
  for the **"Now (last 30 days)"** branch instead of re-researching the recent slice.
- Synthesize into the outline schema below. Keep leaves short; put a year on
  milestones. This is a scaffold for understanding, not a citation-grade record.

### Outline schema

```markdown
# {Topic}
## Origins ({year range})
- 2015: milestone in one line
## {Era 2} ({year range})
- ...
## {Era 3} ({year range})
- ...
## Now (last 30 days)
- from the latest last30days run, if available
## Where it's heading
- open questions / trajectory
```

`#` H1 = root node and page title. Each `##` = a branch (era/phase). Bullets = leaves.

## Step 2 — Render and open

Write the outline to a temp file, then render. The renderer lives next to this
SKILL.md under `scripts/`.

```bash
SKILL_DIR="<absolute dir of this SKILL.md>"
OUTLINE=$(mktemp "${TMPDIR:-/tmp}/topic-history.XXXXXX.md")
cat > "$OUTLINE" <<'MD'
{YOUR_OUTLINE_MARKDOWN}
MD
"$TH_PY" "$SKILL_DIR/scripts/render_mindmap.py" "$OUTLINE"
```

The mindmap is written to
`${LAST30DAYS_MEMORY_DIR:-$HOME/Documents/Last30Days}/mindmaps/<slug>-history.html`
and opened in the browser (use `--no-open` to skip, `--out PATH` to redirect).

## Step 3 — Tell the user

Confirm the file path, summarize the arc in 2-3 sentences, and offer to deepen any
era or pair it with a fresh `/last30days {topic}` run for the latest slice.

## Notes

- Viewing needs internet (markmap loads from CDN); rendering does not.
- `scripts/test_render.py` is an offline smoke test for the renderer.
- Save reusable outlines under `outlines/` (example: `outlines/openai.md`).
