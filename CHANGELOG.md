# Changelog

Notable project-level changes are documented here. Routine contest additions, updates, and expiry removals remain visible in Git history and are not listed individually.

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
