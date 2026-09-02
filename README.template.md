# Awesome AIGC Creative Contests

English | [简体中文](README.zh-CN.md)

> A continuously maintained directory of active AIGC-native and AI-compatible creative, technology, and innovation competitions worldwide.

![Contests](https://img.shields.io/badge/active-{{COUNT}}-2ea44f) ![Last verified](https://img.shields.io/badge/verified-{{UPDATED_AT}}-0969da) [![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

Missing a contest is often an information problem rather than a creative one. This project combines a verified public directory with a source-discovery pipeline. The public directory keeps only opportunities that are open for submissions or officially announced with a future opening date. Expired entries are removed automatically and remain available through Git history.

**Data verified on {{UPDATED_AT}}.** Deadlines, eligibility, fees, and licensing terms may change without notice. Always read the official rules before submitting.

## Subscribe to deadline reminders

- [Subscribe via RSS](https://martindelophy.github.io/Awesome-AIGC-Creative-Contests/feed.xml) for active-directory updates.
- [Subscribe to the calendar](webcal://martindelophy.github.io/Awesome-AIGC-Creative-Contests/deadlines.ics) or [download the ICS file](deadlines.ics) to add every deadline to Apple Calendar, Google Calendar, Outlook, or another calendar app.

Both feeds are generated from the contest data and update automatically when the directory changes.

## Discovery coverage

- **{{SOURCE_COUNT}} registered sources** across China and international government, organizer, association, platform, and discovery-only entry points.
- **{{ENABLED_SOURCE_COUNT}} sources in the low-volume automated pilot**; sources blocked by robots, client-only rendering, or unclear listing status remain manual until a compliant adapter exists.
- **{{CANDIDATE_COUNT}} candidates awaiting review** in [`data/candidates.json`](data/candidates.json). Candidates never appear in the public directory, RSS, or calendar until an official page and rules are verified.

The source registry lives in [`data/sources.json`](data/sources.json). The scheduled discovery workflow checks enabled public sources, deduplicates links against published contests and previous candidates, and preserves review decisions.

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

The directory supports three explicitly tagged scopes: `aigc-native`, `ai-compatible`, and `general`. Legacy records without a scope are treated as AIGC-native. A contest must meet all of the following requirements:

1. It is either centered on AIGC, explicitly permits useful AI assistance, or is a high-value creative, technical, research, or innovation challenge with a concrete submission and outcome.
2. An accessible official event page, rule page, or organizer announcement is available.
3. The submission window, eligibility, work requirements, fee, reward, and AI-use policy can be recorded without guessing; unknown facts are labeled as unknown.
4. Submissions are currently open, or an official future opening date has been announced.
5. The event is not a giveaway, a course-sales campaign, an ordinary conference, or an unverifiable listing with conflicting dates.

Official rules and organizer announcements take priority over media reports and aggregator sites. Paid contests are explicitly marked. A listing that is not marked “free” should not be assumed to be free.

## Contributing

You can [suggest a contest](../../issues/new?template=add-contest.yml) or [report a change](../../issues/new?template=update-contest.yml). When opening a pull request, add or update the corresponding object in [`data/contests.json`](data/contests.json), run the commands below, and include the regenerated outputs.

Field definitions are in [`data/schema.json`](data/schema.json), source and candidate schemas sit beside their data files, the maintenance policy is in [`MAINTENANCE.md`](MAINTENANCE.md), and notable updates are recorded in [`CHANGELOG.md`](CHANGELOG.md).

```bash
python3 scripts/build_readme.py
python3 scripts/build_readme.py --check
python3 scripts/collect_sources.py --check
python3 scripts/collect_sources.py --dry-run --source modelscope-events
python3 -m unittest discover -s tests -v
```

The daily workflow removes expired entries from the active directory and rebuilds both language editions, RSS, and ICS. Previous entries remain available through Git history.

## Community acknowledgment

Thanks to the [LINUX DO](https://linux.do/) community for providing a space for open-source sharing and discussion.

## Disclaimer

This is a community-maintained information index and is not affiliated with any organizer. It does not guarantee prize payments, licensing terms, fees, or last-minute rule changes. Before entering, pay particular attention to copyright ownership, likeness and voice permissions, AI-tool disclosure requirements, regional restrictions, and the organizer's rights to use submitted works.
