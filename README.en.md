# Awesome AIGC Creative Contests

[简体中文](README.md) | English

> A continuously maintained directory of active and officially announced AIGC creative contests worldwide, covering video, images, audio, writing, and AI applications.

The current contest table is maintained in the [Chinese README](README.md). Contest names link to official event pages, and every listing includes its deadline, time zone, eligibility, fee, prize, and official rules. Always verify the official rules before submitting: organizers may change deadlines, eligibility, licensing terms, or fees without notice.

## What is included

A contest must meet all of the following requirements:

1. AIGC is central to creating or judging the work, rather than appearing only in promotional copy.
2. An accessible official event page, rule page, or organizer announcement is available.
3. The submission window, eligibility, and work requirements can be verified.
4. Submissions are currently open, or an official future opening date has been announced.
5. The event is not a giveaway, a course-sales campaign, or an unverifiable listing with conflicting dates.

Official rules and organizer announcements take priority over media reports and aggregator sites. Paid contests are explicitly marked. A listing that is not marked “free” should not be assumed to be free.

## Categories

- 🎬 Video, film, animation, and micro-drama
- 🖼️ Images and visual art
- 🎵 Audio, music, and songs
- ✍️ Writing, scripts, and data journalism
- 🧩 Applications, interactive works, and mini programs

## Data

The source data lives in [`data/contests.json`](data/contests.json). Its machine-readable field definitions are available in [`data/schema.json`](data/schema.json). `README.md` is generated from the data and should not be edited manually.

```bash
python3 scripts/build_readme.py
python3 scripts/build_readme.py --check
python3 -m unittest discover -s tests -v
```

The daily workflow removes expired entries from the active directory and rebuilds the README. Previous entries remain available through Git history.

## Contributing

You can [suggest a contest](../../issues/new?template=add-contest.yml) or [report a change](../../issues/new?template=update-contest.yml). When opening a pull request, add or update the corresponding object in `data/contests.json`, run the commands above, and include the regenerated `README.md`.

Every submission needs a stable lowercase English `id`, ISO `YYYY-MM-DD` dates, a time zone, eligibility, fee and prize information, and HTTPS links to the official event and rules pages. Accepted categories are `video`, `image`, `audio`, `text`, and `app`.

## Disclaimer

This is a community-maintained information index and is not affiliated with any organizer. It does not guarantee prize payments, licensing terms, fees, or last-minute rule changes. Before entering, pay particular attention to copyright ownership, likeness and voice permissions, AI-tool disclosure requirements, regional restrictions, and the organizer's rights to use submitted works.
