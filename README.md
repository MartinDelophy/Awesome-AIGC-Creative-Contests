# Awesome AIGC Creative Contests

English | [简体中文](README.zh-CN.md)

> A continuously maintained directory of active and officially announced AIGC creative contests worldwide, covering video, images, audio, writing, and AI applications.

![Contests](https://img.shields.io/badge/active-11-2ea44f) ![Last verified](https://img.shields.io/badge/verified-2026-08-26-0969da) [![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

Missing a contest is often an information problem rather than a creative one. This project combines a verified core AIGC directory with a source-discovery pipeline. The core directory keeps only opportunities that are open for submissions or officially announced with a future opening date. Broader opportunities live in separate opt-in datasets. Expired entries are removed automatically and remain available through Git history.

**Data verified on 2026-08-26.** Deadlines, eligibility, fees, and licensing terms may change without notice. Always read the official rules before submitting.

## Subscribe to deadline reminders

- [Subscribe via RSS](https://martindelophy.github.io/Awesome-AIGC-Creative-Contests/feed.xml) for active-directory updates.
- [Subscribe to the calendar](webcal://martindelophy.github.io/Awesome-AIGC-Creative-Contests/deadlines.ics) or [download the ICS file](deadlines.ics) to add every deadline to Apple Calendar, Google Calendar, Outlook, or another calendar app.

Both feeds are generated only from the core AIGC data and update automatically when that directory changes.

## Discovery coverage

- **52 registered sources** across China and international government, organizer, association, platform, and discovery-only entry points.
- **5 sources in the low-volume automated pilot**; sources blocked by robots, client-only rendering, or unclear listing status remain manual until a compliant adapter exists.
- **15 candidates awaiting review** in [`data/candidates.json`](data/candidates.json). Candidates never appear in the public directory, RSS, or calendar until an official page and rules are verified.

The source registry lives in [`data/sources.json`](data/sources.json). The scheduled discovery workflow checks enabled public sources, deduplicates links against published contests and previous candidates, and preserves review decisions.

## Opt-in opportunity datasets

The original compatibility contract stays unchanged: [`data/contests.json`](data/contests.json), [`data/schema.json`](data/schema.json), the tables below, RSS, and ICS contain only the core AIGC directory. Existing consumers do not need to change anything.

Broader verified opportunities are published separately under [`data/opportunities/`](data/opportunities/):

- Read the small [`manifest.json`](data/opportunities/manifest.json) first.
- Fetch only the shards relevant to your users, such as `global.json`, `cn-national.json`, or `cn-local.json`.
- Every shard has `default_included: false`; nothing is merged into the core feed automatically. An international client therefore does not need to download local Chinese opportunities.
- Optional records use their own [`schema.json`](data/opportunities/schema.json), including scope, industry, audience, AI policy, geography, and source evidence.

## Open for submissions

| Status | Deadline | Category | Contest & requirements | Region / eligibility | Prize / fee |
|---|---|---|---|---|---|
| 🔥 2 days left | 2026-09-15<br><sub>Not stated on the official site</sub> | 🎬 Video | **[Austin AI Film Festival 2026](https://filmfreeway.com/AustinAIFilmFestival)**<br><sub>Creators aged 14+ worldwide; most AI categories require a majority of visual content to use AI-assisted creative tools · [Rules](https://filmfreeway.com/AustinAIFilmFestival)</sub> | United States / Open worldwide except restricted jurisdictions | Awards and selected screenings; see official page for prize details<br><sub>Fee: US$20 for most categories; a free option is listed for the student category</sub> |
| 🟢 Open | 2026-09-27<br><sub>AoE (UTC−12)</sub> | 🎵 Audio | **[AI Song Contest 2026 — Bangkok](https://www.aisongcontest.com/join)**<br><sub>Human–AI co-created songs up to 4 minutes; prompt-only generation without human post-production is ineligible · [Rules](https://www.aisongcontest.com/join)</sub> | Thailand / Open worldwide | US$1,000 plus a trip to the Bangkok award show<br><sub>Fee: Free</sub> |
| 🟢 Open | 2026-09-30<br><sub>Korea Standard Time, 23:59</sub> | 🖼️ Image<br>🎬 Video | **[AI ART AWARD — NEXT ART AI 2026](https://next-art-ai.com/en/apply/overview)**<br><sub>Open to all professions, nationalities, and ages; AI image and AI video categories · [Rules](https://next-art-ai.com/en/apply/overview)</sub> | South Korea / Open worldwide | KRW 21,000,000 total prize pool<br><sub>Fee: See official guidelines</sub> |
| 🟢 Open | 2026-09-30<br><sub>Not stated on the official site</sub> | 🎬 Video | **[On Art AI Film Festival 2026](https://filmfreeway.com/OnAI)**<br><sub>Films completed after January 1, 2025 in which AI plays a key role; non-English and non-Polish films need English subtitles · [Rules](https://filmfreeway.com/OnAI)</sub> | Poland / Open worldwide | Diplomas in six categories; no cash or material prizes<br><sub>Fee: Paid via FilmFreeway; varies by category and deadline stage</sub> |
| 🟢 Open | 2026-10-01<br><sub>Not stated on the official site</sub> | 🎬 Video | **[GenTO: Toronto AI Film Festival 2026](https://filmfreeway.com/GenTOAIFilmFestival)**<br><sub>AI-assisted, hybrid, or traditionally made short films, showcase films, music videos, and ads; non-English films need English subtitles · [Rules](https://filmfreeway.com/GenTOAIFilmFestival)</sub> | Canada / Open worldwide | Festival recognition and partner prizes; some categories may include mentorship or technology credits<br><sub>Fee: Regular US$30 / student US$25; late US$40 / student US$35</sub> |
| 🟢 Open | 2026-10-11<br><sub>China Standard Time; exact time not stated</sub> | ✍️ Writing<br>🖼️ Image<br>🎬 Video<br>🎵 Audio<br>🧩 App | **[First 2026 AIGC and Visualization Creation Competition](https://aigc.capt.cn/)**<br><sub>Institutional and individual divisions; individual division includes university students and adults · [Rules](https://www.cuc.edu.cn/_t86/2026/0811/c1761a273225/page.htm)</sub> | China | Certificates and commemorative gifts<br><sub>Fee: Free</sub> |
| 🟢 Open | 2026-10-15<br><sub>Not stated on the official site</sub> | 🎬 Video<br>🎵 Audio | **[AI Filmfest Athens 2026 — Myths Meet Machine](https://www.aifilmfestathens.gr/en)**<br><sub>Fully AI-generated short films of 3–15 minutes; no live-action hybrids; non-English films require English subtitles · [Rules](https://www.aifilmfestathens.gr/en)</sub> | Greece / Open worldwide | Four competitive awards of €1,000 each<br><sub>Fee: €30 through September 3 / €45 final deadline</sub> |
| 🟢 Open | 2026-10-16<br><sub>Not stated on the official site</sub> | 🎬 Video | **[AIGC Global Competition 2026](https://www.aigcglobal.com.cn/)**<br><sub>Age-group divisions from Primary 4 through an adult open division; themes and durations vary · [Rules](https://www.aigcglobal.com.cn/?a=index&c=Lists&m=home&tid=1)</sub> | Hong Kong, China / Open worldwide | HK$120,000 total prize pool<br><sub>Fee: Paid; see registration page</sub> |
| 🟢 Open | 2026-10-16<br><sub>Not stated on the official site</sub> | 🎬 Video<br>🎵 Audio | **[Disrupt AI Film Festival (DAIFF 2026)](https://www.daiff.com.au/)**<br><sub>Generative AI must be used for visuals, audio, effects, or animation; entrants must describe their creative process · [Rules](https://www.daiff.com.au/)</sub> | Australia / Open worldwide | Grand Prix and category awards; amounts not stated<br><sub>Fee: Via FilmFreeway; see submission page</sub> |
| 🟢 Open | 2026-10-17<br><sub>China Standard Time; see submission page for exact time</sub> | 🧩 App | **[2026 WeChat Mini Program Development Competition](https://watcha.cn/activities/activity-74)**<br><sub>Open regardless of education or profession; teams of 1–3; entries must be original published mini programs, not mini games · [Rules](https://watcha.cn/activities/activity-74)</sub> | China / Open worldwide | CNY 490,000 total; CNY 100,000 first prize<br><sub>Fee: Free</sub> |
| 🟢 Open | 2026-10-17<br><sub>Not stated on the official site</sub> | 🎬 Video<br>🖼️ Image<br>🎵 Audio | **[AIMA — AI Movie Awards London 2026](https://www.aimovieawards.org/)**<br><sub>Accepts AI film, motion art, image art, advertising, and music; scripts and text must be in English or include a translation · [Rules](https://www.aimovieawards.org/)</sub> | United Kingdom / Open worldwide | Trophies and certificates by category; selected shorts may opt into a distribution and revenue-sharing offer<br><sub>Fee: Paid and non-refundable; see the official submission page</sub> |

## Opening soon

_No verified contests yet. Contributions are welcome._

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
