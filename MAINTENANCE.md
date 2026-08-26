# Maintenance policy / 维护说明

This document describes how the active contest directory is kept accurate. 本文说明当前赛事清单的维护与核验方式。

## Maintenance cycle / 维护周期

- A scheduled GitHub Actions workflow runs daily in the `Asia/Shanghai` time zone.
- It validates `data/contests.json`, removes entries whose deadline has passed, and regenerates `README.md`, `README.zh-CN.md`, `feed.xml`, and `deadlines.ics`.
- GitHub Pages publishes the generated RSS and ICS files with subscription-friendly content types.
- Pull requests and pushes to `main` run validation, tests, and generated-file consistency checks.
- Expired records remain recoverable through Git history.

## Source verification / 信息核验

Official rules and organizer announcements are the preferred sources. Maintainers verify the submission window, time zone, eligibility, work requirements, fee, prize, and official links before accepting an entry. Conflicting dates are not guessed: the entry stays out of the directory until an official source resolves the conflict.

The `verified_on` field records the most recent manual verification date. Automation can detect structural errors and expired dates, but it cannot guarantee that an organizer has not changed its rules. Users should always re-read the official rules before submitting.

## Updating an entry / 更新赛事

1. Edit `data/contests.json`; do not edit generated files directly.
2. Follow the field constraints in `data/schema.json`.
3. Run:

   ```bash
   python3 scripts/build_readme.py
   python3 scripts/build_readme.py --check
   python3 -m unittest discover -s tests -v
   ```

4. Commit the data change together with `README.md`, `README.zh-CN.md`, `feed.xml`, and `deadlines.ics`.
5. Add a notable project-level change to `CHANGELOG.md` when appropriate. Routine contest additions and removals do not require changelog entries because Git history already records them.

## Incident handling / 异常处理

Broken links, early closures, extensions, and material rule changes should be reported through the repository's “赛事变更” Issue form. A confirmed incorrect listing should be corrected or removed promptly. Security issues in the generator should be reported privately to the repository owner through GitHub rather than placed in a public contest-data Issue.

## Release policy / 发布方式

The repository uses a continuously updated directory rather than numbered releases. `main` is the canonical version. Notable structural and policy changes are recorded in `CHANGELOG.md`; current contest facts live in `data/contests.json`.
