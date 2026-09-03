# Changelog

Notable project-level changes are documented here. Routine contest additions, updates, and expiry removals remain visible in Git history and are not listed individually.

## 2026-09-02

### Added

- A 52-entry source registry spanning China, regional government entry points, international platforms, organizers, associations, and discovery-only aggregators.
- A review-only candidate queue with stable URL fingerprints, source provenance, first/last-seen dates, review states, and deduplication against published contests.
- Low-volume HTML, RSS/Atom, and JSON discovery adapters with robots checks, response limits, tracking-URL normalization, source-specific matching, and failure isolation.
- A scheduled candidate-discovery workflow and a source-suggestion Issue form.
- A manifest-driven `data/opportunities/` extension layer with independent global, China-wide, and China-local opt-in shards.
- An independent extension schema and validator for opportunity scope, type, industries, audiences, AI-use policy, normalized geography, source evidence, record counts, and cross-dataset uniqueness.

### Changed

- Kept the original `data/contests.json` and `data/schema.json` contract focused on core AIGC contests; AI-compatible and selected general opportunities are available only through shards whose `default_included` value is `false`.
- Kept README tables, RSS, ICS, and WeCom output on the core dataset so existing consumers are unaffected and clients can fetch only relevant regional extensions.
- Kept discovery separate from publication so no automatically found link enters the public JSON, RSS, or calendar without official-source verification.

## 2026-08-26

### Added

- English project documentation and a bilingual navigation entry.
- A machine-readable JSON Schema for contest data.
- RSS and ICS subscriptions generated from the active contest directory.
- A maintenance policy and MIT license.
- A custom repository social preview image.
- Initial active AIGC creative contest directory.
- Data-driven README generation, tests, contribution forms, and daily expiry cleanup.
- A single-page daily WeCom group digest with recent-verification ordering, compact contest details, overflow linking, and manual dry-run support.

### Changed

- Made English the primary repository README and added a fully generated Simplified Chinese edition.
- Localized contest records for bilingual output and switched RSS and ICS content to English.
- Expanded the active directory with verified contests in the United States, Canada, Poland, and the United Kingdom.
- Strengthened validation for identifiers, empty and unknown fields, duplicate categories, dates, and HTTPS URLs.
- Expanded continuous integration to validate pull requests and pushes to `main`.
- Made the Codex daily research refresh the trigger for the WeCom digest, avoiding a second independent notification schedule.
