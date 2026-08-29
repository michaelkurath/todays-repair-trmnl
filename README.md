# Today's Repair

Your daily anti-doom screen for TRMNL.

Today's Repair shows one calm, sourced example of human progress, repair, or resilience each day. The tone is deliberately not "everything is fine." The point is better:

> Things are messy. Here is one real thing that got repaired anyway.

## MVP

- One sourced repair item per day
- Works in full, half-horizontal, half-vertical, and quadrant TRMNL views
- Static JSON data source for the first version
- Short e-ink-friendly copy
- Caveats included so the plugin does not overclaim

## Files

| File | Purpose |
| --- | --- |
| `src/settings.yml` | TRMNL polling settings |
| `src/shared.liquid` | Shared tab content: selection logic and scoped styles |
| `src/full.liquid` | Full-screen layout |
| `src/half_horizontal.liquid` | Half-horizontal layout |
| `src/half_vertical.liquid` | Half-vertical layout |
| `src/quadrant.liquid` | Quadrant layout |
| `data/sample-data.json` | Starter content payload |
| `data/today.json` | Tiny live payload for TRMNL polling |
| `scripts/build_today.py` | Builds `today.json` from the full dataset |
| `preview/index.html` | Browser preview for all four layouts |
| `.github/workflows/pages.yml` | Publishes the preview and data through GitHub Pages |
| `.github/workflows/update-today.yml` | Refreshes `data/today.json` daily |
| `docs/content-guide.md` | Editorial rules for adding entries |
| `docs/roadmap.md` | Product roadmap |

## Data Shape

For live TRMNL polling, the small endpoint should return:

```json
{
  "repair": {
    "id": "ozone-layer-recovery",
    "category": "climate_repair",
    "title": "The Ozone Layer Is Recovering",
    "summary": "Global action phased down ozone-depleting chemicals, and the ozone layer is on a path toward recovery.",
    "why_it_matters": "It proves international environmental agreements can work when the problem is clear and enforcement is real.",
    "caveat": "Recovery is still ongoing and depends on continued compliance.",
    "source_name": "UN Environment Programme",
    "source_url": "https://www.unep.org/news-and-stories/press-release/ozone-layer-recovery-track-helping-avoid-global-warming-05degc"
  }
}
```

The full dataset can return:

```json
{
  "repairs": [
    {
      "id": "ozone-layer-recovery",
      "category": "climate_repair",
      "title": "The Ozone Layer Is Recovering",
      "summary": "Global action phased down ozone-depleting chemicals, and the ozone layer is on a path toward recovery.",
      "why_it_matters": "It proves international environmental agreements can work when the problem is clear and enforcement is real.",
      "caveat": "Recovery is still ongoing and depends on continued compliance.",
      "source_name": "UN Environment Programme",
      "source_url": "https://www.unep.org/news-and-stories/press-release/ozone-layer-recovery-track-helping-avoid-global-warming-05degc"
    }
  ]
}
```

## First Test

1. Create a private TRMNL plugin or recipe.
2. Use the Polling strategy.
3. For quick testing, use `data/today.json` as the polling endpoint.
4. Paste `src/shared.liquid` into the TRMNL Shared tab.
5. Paste each view Liquid file into the matching TRMNL markup view.
6. Force refresh and check all four views.

Current polling URL:

```text
https://raw.githubusercontent.com/michaelkurath/todays-repair-trmnl/main/data/today.json
```

The GitHub repository must be public for TRMNL to fetch this URL.

## Local Preview

Run this from the project root:

```bash
python3 -m http.server 8080
```

Then open:

```text
http://127.0.0.1:8080/preview/
```

## Editorial Rule

Every entry needs:

- a credible source
- one specific improvement
- a caveat
- no inspirational fluff
- no claim that a problem is solved unless it truly is
