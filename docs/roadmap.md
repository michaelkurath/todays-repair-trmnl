# Roadmap

Today's Repair deliberately keeps the TRMNL experience simple: one sourced repair,
chosen randomly whenever the device refreshes. The website keeps a separate stable
daily schedule for sharing and browsing.

## Shipped

- Four responsive TRMNL views: full, half horizontal, half vertical, and quadrant
- Support for TRMNL OG and TRMNL X display profiles
- Random selection from the full dataset on every TRMNL refresh
- 15-minute polling interval with no ordering, history, or repeat protection
- 90 curated entries with source, checked date, explanation, and caveat fields
- One matching verification record for every entry
- Automated schema, source URL, schedule, missing-record, and duplicate-ID checks
- TRMNLP linting and rendered OG/X layout QA in GitHub Actions
- Crossed-bandage icon in the website branding and TRMNL status bars
- Public website with a stable daily repair
- Searchable archive with category filtering and direct source links
- Stable annual schedule used by the website only
- GitHub Pages deployment and daily website-payload workflow
- PayPal support link

## Next Priorities

### 1. Reach 100 Checked Entries

- Add 10 strong entries without increasing the existing health bias
- Prefer climate, energy, education, infrastructure, science, and everyday-life repairs
- Keep every claim concise enough for all four TRMNL layouts

### 2. Source Health Checks

- Check source links automatically for failures and redirects
- Flag old `source_checked` dates for human review
- Produce a simple review report without pretending that link checks are fact checks

### 3. TRMNL Recipe Install Link

- Add the public recipe link to the website and README when the listing URL is final
- Keep the install call-to-action secondary to the current repair

### 4. Shareable Repair Pages

- Give each repair a stable website URL
- Include the claim, why it matters, caveat, source, and verification date
- Preserve the searchable archive as the main browsing interface

### 5. Stronger Content QA

- Detect likely semantic duplicates, not only duplicate IDs
- Report category and source concentration before accepting a batch
- Periodically recheck claims that depend on changing totals or projections

## Later

- Translation-ready data fields
- German and French translations
- Weekly digest page
- Reviewed "Submit a repair" workflow
- Visible verification badge on individual repair pages
- Optional share cards for individual repairs

## Parked Ideas

These ideas add complexity to the device experience and are intentionally not planned
for the current simple version:

- TRMNL category filters
- Family-safe mode
- Primary-source-only or "skeptic" mode
- QR codes on the device
- A fixed daily schedule on TRMNL
- Region-specific, engineering, nature, or classroom modes
- User-submitted local repairs shown without editorial review

Revisit them only if real user feedback shows that the simple random experience is
insufficient.
