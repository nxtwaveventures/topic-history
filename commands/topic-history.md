---
description: Render a topic's full historical arc as an interactive mindmap (companion to /last30days)
---

Invoke the `topic-history` skill for the topic: $ARGUMENTS

Research the topic's historical arc (origins, eras, turning points, the last 30
days, and trajectory), write a markdown outline per the skill's schema, then run
`scripts/render_mindmap.py` to render and open the mindmap. If no topic was
provided, ask for one first.
