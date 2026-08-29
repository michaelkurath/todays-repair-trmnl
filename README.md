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
| `index.html` | Public website with today's repair and searchable archive |
| `src/settings.yml` | TRMNL polling settings |
| `src/shared.liquid` | Shared selection logic and adaptive typography classes |
| `src/full.liquid` | Full-screen layout |
| `src/half_horizontal.liquid` | Half-horizontal layout |
| `src/half_vertical.liquid` | Half-vertical layout |
| `src/quadrant.liquid` | Quadrant layout |
| `data/sample-data.json` | Starter content payload |
| `data/today.json` | Tiny live payload for TRMNL polling |
| `data/schedules/YEAR.json` | Immutable annual date-to-repair-ID schedule |
| `data/verifications.json` | Verification status and evidence notes for every repair |
| `scripts/generate_schedule.py` | Creates a stable annual schedule without replacing an existing one |
| `scripts/build_today.py` | Builds `today.json` from the annual schedule |
| `scripts/validate_data.py` | Validates entries, verification coverage, and annual schedules |
| `preview/index.html` | Browser preview for all four layouts |
| `.github/workflows/pages.yml` | Publishes the preview and data through GitHub Pages |
| `.github/workflows/update-today.yml` | Refreshes `data/today.json` daily |
| `.github/workflows/trmnlp-qa.yml` | Lints the plugin and renders OG/X preview artifacts |
| `.trmnlp.yml` | TRMNLP local and CI preview configuration |
| `docs/content-guide.md` | Editorial rules for adding entries |
| `docs/roadmap.md` | Product roadmap |

## Data Shape

For live TRMNL polling, the small endpoint should return:

```json
{
  "date": "2026-08-29",
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

## Daily Schedule

The daily repair is not calculated from the array position. Each calendar year has a
committed file such as `data/schedules/2026.json` that maps every UTC date to a stable
repair ID. The schedule is generated in balanced deterministic cycles, so each repair
appears roughly equally often and the same repair never appears on consecutive days.

Generate a schedule once:

```bash
python3 scripts/generate_schedule.py --year 2026
```

If that year's file already exists, the command leaves it unchanged. This is deliberate:
adding, removing, or reordering repairs must not rewrite dates that have already been
planned or shared. `--force` exists for an intentional pre-publication reset and should
not be used after a schedule is published.

Build or inspect any date deterministically:

```bash
python3 scripts/build_today.py --date 2026-08-29
```

The scheduled workflow creates the current year's schedule if it is missing, validates
all scheduled IDs, builds the small `data/today.json` payload, and commits only if either
file changed. All dates use UTC.

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
http://127.0.0.1:8080/
http://127.0.0.1:8080/preview/
```

For framework-accurate plugin previews, run TRMNLP through Docker:

```bash
docker run --rm --pull always \
  --publish 4567:4567 \
  --volume "$(pwd):/plugin" \
  trmnl/trmnlp serve --bind 0.0.0.0
```

Every push to `main` also runs TRMNLP linting and produces downloadable PNG
and HTML artifacts for TRMNL OG (800×480, 1-bit) and TRMNL X
(1872×1404, 4-bit) in GitHub Actions. The render jobs use the framework's
`screen--og` and `screen--v2` device profiles so responsive classes are tested
against each device's real layout density, not only a larger browser viewport.

## Editorial Rule

Every entry needs:

- a credible source
- one specific improvement
- a caveat
- no inspirational fluff
- no claim that a problem is solved unless it truly is

## Data Verification

Today's Repair uses a separate verification file, similar to the Built & Broken workflow.
Every repair ID in `data/sample-data.json` must have one matching record in `data/verifications.json`.
Every annual schedule must cover every date in its year and may only reference repair IDs
that still exist in the dataset. New repairs do not need to appear in an already-published
schedule; they can enter the next annual schedule.

Allowed verification statuses:

- `verified`
- `verified_with_note`
- `needs_follow_up`
- `corrected`

Run this before publishing new entries:

```bash
python3 scripts/validate_data.py
```
