# Awesome AIGC Creative Contests

English | [简体中文](README.zh-CN.md)

> A continuously maintained directory of active and officially announced AIGC creative contests worldwide, covering video, images, audio, writing, and AI applications.

![Contests](https://img.shields.io/badge/active-{{COUNT}}-2ea44f) ![Last verified](https://img.shields.io/badge/verified-{{UPDATED_AT}}-0969da) [![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

Missing a contest is often an information problem rather than a creative one. This project combines a verified core AIGC directory with a source-discovery pipeline. The core directory keeps only opportunities that are open for submissions or officially announced with a future opening date. Broader opportunities live in separate opt-in datasets. Expired entries are removed automatically and remain available through Git history.

**Data verified on {{UPDATED_AT}}.** Deadlines, eligibility, fees, and licensing terms may change without notice. Always read the official rules before submitting.

## Subscribe to deadline reminders

- [Subscribe via RSS](https://martindelophy.github.io/Awesome-AIGC-Creative-Contests/feed.xml) for active-directory updates.
- [Subscribe to the calendar](webcal://martindelophy.github.io/Awesome-AIGC-Creative-Contests/deadlines.ics) or [download the ICS file](deadlines.ics) to add every deadline to Apple Calendar, Google Calendar, Outlook, or another calendar app.

Both feeds are generated only from the core AIGC data and update automatically when that directory changes.

## Discovery coverage

- **{{SOURCE_COUNT}} registered sources** across China and international government, organizer, association, platform, and discovery-only entry points.
- **{{ENABLED_SOURCE_COUNT}} sources in the low-volume automated pilot**; sources blocked by robots, client-only rendering, or unclear listing status remain manual until a compliant adapter exists.
- **{{CANDIDATE_COUNT}} candidates awaiting review** in [`data/candidates.json`](data/candidates.json). Candidates never appear in the public directory, RSS, or calendar until an official page and rules are verified.

The source registry lives in [`data/sources.json`](data/sources.json). The scheduled discovery workflow checks enabled public sources, deduplicates links against published contests and previous candidates, and preserves review decisions.

## Opt-in opportunity datasets

The original compatibility contract stays unchanged: [`data/contests.json`](data/contests.json), [`data/schema.json`](data/schema.json), the tables below, RSS, and ICS contain only the core AIGC directory. Existing consumers do not need to change anything.

Broader verified opportunities are published separately under [`data/opportunities/`](data/opportunities/):

- Read the small [`manifest.json`](data/opportunities/manifest.json) first.
- Fetch only the shards relevant to your users, such as `global.json`, `cn-national.json`, or `cn-local.json`.
- Every shard has `default_included: false`; nothing is merged into the core feed automatically. An international client therefore does not need to download local Chinese opportunities.
- Optional records use their own [`schema.json`](data/opportunities/schema.json), including scope, industry, audience, AI policy, geography, and source evidence.

## Open for submissions

{{OPEN_TABLE}}

## Opening soon

{{UPCOMING_TABLE}}

## Categories

- 🎬 Video, film, animation, and micro-drama
- 🖼️ Images and visual art
- 🎵 Audio, music, and songs
- ✍️ Writing, scripts, and data journalism
- 🧩 Applications, interactive works, and mini programs

## Sources worth watching

These sources remain useful over time, but a listed past edition may no longer accept submissions.

- [Runway AI Festival](https://aif.runwayml.com/): an annual program spanning film, design, advertising, fashion, games, and new media.
- [Reply AI Film Festival](https://challenges.reply.com/challenges/creative/aifilmfestival/home/): a global AI filmmaking competition.
- [World AI Film Festival](https://worldaifilmfestival.com/): an international festival focused on generative-AI cinema.
- [AI Film Contests](https://aifilmcontests.com/): a third-party AI film deadline calendar; always verify discoveries on the organizer's official site.
- [AI Music Events Deadlines](https://aimusic.events/deadlines): a third-party music opportunity calendar; eligibility must be checked with the organizer.
- [Mango AI Creative Challenges](https://aigc.mgtv.com/challenges/): AI video, micro-drama, and animation contests in China.
- [ModelScope Events](https://modelscope.cn/events): model, developer, and AIGC events in China.

## Inclusion criteria

The core directory keeps its original AIGC focus. A contest must meet all of the following requirements:

1. AIGC is central to the contest rather than incidental.
2. An accessible official event page, rule page, or organizer announcement is available.
3. The submission window, eligibility, work requirements, fee, and reward can be recorded without guessing.
4. Submissions are currently open, or an official future opening date has been announced.
5. The event is not a giveaway, a course-sales campaign, an ordinary conference, or an unverifiable listing with conflicting dates.

Verified AI-compatible and selected general creative, technical, research, or innovation opportunities may instead enter an opt-in shard. They must have a concrete submission and outcome, explicit structured scope and AI-policy fields, and the same official-source standard. They never enter the core directory by default.

Official rules and organizer announcements take priority over media reports and aggregator sites. Paid contests are explicitly marked. A listing that is not marked “free” should not be assumed to be free.

## Contributing

You can [suggest a contest](../../issues/new?template=add-contest.yml) or [report a change](../../issues/new?template=update-contest.yml). When opening a pull request, put core AIGC contests in [`data/contests.json`](data/contests.json) and broader opportunities in the matching opt-in shard listed by [`data/opportunities/manifest.json`](data/opportunities/manifest.json).

Core field definitions are in [`data/schema.json`](data/schema.json), optional field definitions are in [`data/opportunities/schema.json`](data/opportunities/schema.json), source and candidate schemas sit beside their data files, the maintenance policy is in [`MAINTENANCE.md`](MAINTENANCE.md), and notable updates are recorded in [`CHANGELOG.md`](CHANGELOG.md).

```bash
python3 scripts/build_readme.py
python3 scripts/build_readme.py --check
python3 scripts/collect_sources.py --check
python3 scripts/validate_opportunities.py --check
python3 scripts/collect_sources.py --dry-run --source modelscope-events
python3 -m unittest discover -s tests -v
```

The daily workflow removes expired entries from the active directory and rebuilds both language editions, RSS, and ICS. Previous entries remain available through Git history.

## Community acknowledgment

Thanks to the [LINUX DO](https://linux.do/) community for providing a space for open-source sharing and discussion.

## Disclaimer

This is a community-maintained information index and is not affiliated with any organizer. It does not guarantee prize payments, licensing terms, fees, or last-minute rule changes. Before entering, pay particular attention to copyright ownership, likeness and voice permissions, AI-tool disclosure requirements, regional restrictions, and the organizer's rights to use submitted works.
