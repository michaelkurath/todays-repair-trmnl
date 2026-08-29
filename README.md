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
| `src/settings.yml` | Draft TRMNL recipe settings |
| `src/shared.liquid` | Shared tab content: selection logic and scoped styles |
| `src/full.liquid` | Full-screen layout |
| `src/half_horizontal.liquid` | Half-horizontal layout |
| `src/half_vertical.liquid` | Half-vertical layout |
| `src/quadrant.liquid` | Quadrant layout |
| `data/sample-data.json` | Starter content payload |
| `preview/index.html` | Browser preview for all four layouts |
| `docs/content-guide.md` | Editorial rules for adding entries |
| `docs/roadmap.md` | Product roadmap |

## Data Shape

The data endpoint should return:

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
2. Use `merge_tag` polling with a JSON endpoint.
3. For quick testing, paste the contents of `data/sample-data.json` into a simple static endpoint.
4. Paste `src/shared.liquid` into the TRMNL Shared tab.
5. Paste each view Liquid file into the matching TRMNL markup view.
6. Force refresh and check all four views.

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
