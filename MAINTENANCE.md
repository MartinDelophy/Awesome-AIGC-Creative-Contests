# Maintenance policy / 维护说明

This document describes how the active contest directory is kept accurate. 本文说明当前赛事清单的维护与核验方式。

## Maintenance cycle / 维护周期

- A separate discovery workflow runs four low-volume passes per day. It reads `data/sources.json` and writes links only to `data/candidates.json`; it never publishes a contest automatically.
- A scheduled GitHub Actions workflow runs daily in the `Asia/Shanghai` time zone.
- It validates `data/contests.json`, removes entries whose deadline has passed, and regenerates `README.md`, `README.zh-CN.md`, `feed.xml`, and `deadlines.ics`.
- A Codex scheduled task researches current contests, records its crawl status, and pushes a daily data refresh commit. That commit triggers a second workflow which sends a single-page Chinese WeCom digest of recently verified active and upcoming contests.
- GitHub Pages publishes the generated RSS and ICS files with subscription-friendly content types.
- Pull requests and pushes to `main` run validation, tests, and generated-file consistency checks.
- Expired records remain recoverable through Git history.

## Discovery and review / 发现与审核

The repository separates discovery from publication:

1. `data/sources.json` records the source owner, trust tier, geographic and industry coverage, cadence, and collector mode.
2. `scripts/collect_sources.py` makes at most one public-page request per due source, respects `robots.txt`, rejects private-network URLs, limits response size, normalizes tracking URLs, and extracts matching links.
3. New links are deduplicated against both `data/contests.json` and earlier candidates. Existing `reviewing` or `rejected` decisions are preserved across later runs.
4. A maintainer or research task verifies the official organizer, dates, eligibility, fee, reward, submission requirements, and AI-use policy.
5. Only then is the record added to `data/contests.json` and removed from the candidate queue by the next discovery run.

Candidate statuses are `new`, `reviewing`, `accepted`, and `rejected`. `accepted` means the reviewer has approved promotion; it does not make the candidate public by itself. Add a short `review_notes` explanation for rejections or unresolved facts.

Run a single source without changing files:

```bash
python3 scripts/collect_sources.py --dry-run --source modelscope-events
```

Use `enabled: false` and a `manual` collector when a source requires login, returns a captcha, relies entirely on client-side data, mixes open and historical records without a reliable status, or lacks a clearly permitted automated interface. Do not bypass technical restrictions.

## Source tiers / 来源等级

- `official-api`: documented public API from a government body, organizer, or platform.
- `official-page`: official organizer or government page.
- `trusted-platform`: established submission or competition platform; event facts still require checking.
- `discovery-only`: aggregator or secondary index. A candidate from this tier cannot be published until an official organizer source is found.

## WeCom daily digest / 企业微信每日摘要

The `Send WeCom contest digest` workflow is triggered by a pushed `data/**` change whose commit subject begins with `chore(data): daily contest refresh`, or by a manual dispatch. This keeps the Codex task as the single daily scheduler and prevents duplicate notifications. The workflow sorts non-expired contests by `verified_on` in descending order and fits as many recent entries as possible into one message below the [WeCom markdown size limit](https://developer.work.weixin.qq.com/document/path/91770). Equal verification dates retain their order in `data/contests.json`. Each displayed entry includes the title, official and rules links, deadline and time zone, eligibility, and category. A footer links to the complete directory when older entries do not fit, and upcoming contests use a separate status label.

Configure a repository-level Actions secret named `WECOM_WEBHOOK_URL` with the complete group-robot webhook URL. Forks do not inherit this secret, so each repository that runs the workflow must configure its own value. Never put the webhook URL in source code, workflow YAML, test fixtures, commits, or logs.

Preview the exact digest locally without sending it:

```bash
python3 scripts/send_wecom.py --dry-run
python3 scripts/send_wecom.py --dry-run --today 2026-08-26
```

The workflow also supports `workflow_dispatch` for a manual production test after it is present on the repository's default branch.

## Source verification / 信息核验

Official rules and organizer announcements are the preferred sources. Maintainers verify the submission window, time zone, eligibility, work requirements, fee, prize, and official links before accepting an entry. Conflicting dates are not guessed: the entry stays out of the directory until an official source resolves the conflict.

The `verified_on` field records the most recent date on which a maintainer or the Codex research task checked the official sources. Optional structured metadata records opportunity scope, industry, audience, AI policy, normalized geography, and source evidence. Automated research must omit a candidate when its official page does not establish the required facts; it must not guess missing dates or rules. Automation still cannot guarantee that an organizer has not changed its rules, so users should always re-read the official rules before submitting.

## Updating an entry / 更新赛事

1. Edit `data/contests.json`; do not edit generated files directly.
2. Follow the field constraints in `data/schema.json`.
3. Run:

   ```bash
   python3 scripts/build_readme.py
   python3 scripts/build_readme.py --check
   python3 scripts/collect_sources.py --check
   python3 -m unittest discover -s tests -v
   ```

4. Commit the data change together with `README.md`, `README.zh-CN.md`, `feed.xml`, and `deadlines.ics`.
5. Add a notable project-level change to `CHANGELOG.md` when appropriate. Routine contest additions and removals do not require changelog entries because Git history already records them.

## Incident handling / 异常处理

Broken links, early closures, extensions, and material rule changes should be reported through the repository's “赛事变更” Issue form. A confirmed incorrect listing should be corrected or removed promptly. Security issues in the generator should be reported privately to the repository owner through GitHub rather than placed in a public contest-data Issue.

## Release policy / 发布方式

The repository uses a continuously updated directory rather than numbered releases. `main` is the canonical version. Notable structural and policy changes are recorded in `CHANGELOG.md`; current contest facts live in `data/contests.json`.
