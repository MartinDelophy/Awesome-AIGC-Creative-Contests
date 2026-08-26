#!/usr/bin/env python3
"""Validate contest data, remove expired entries, and render public outputs."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, time, timedelta, timezone
from email.utils import format_datetime
from html import escape as xml_escape
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "contests.json"
TEMPLATE_PATH = ROOT / "README.template.md"
ZH_TEMPLATE_PATH = ROOT / "README.zh-CN.template.md"
README_PATH = ROOT / "README.md"
ZH_README_PATH = ROOT / "README.zh-CN.md"
RSS_PATH = ROOT / "feed.xml"
ICS_PATH = ROOT / "deadlines.ics"
REPOSITORY_URL = "https://github.com/MartinDelophy/Awesome-AIGC-Creative-Contests"
PUBLIC_BASE_URL = "https://martindelophy.github.io/Awesome-AIGC-Creative-Contests"

REQUIRED_FIELDS = {
    "id",
    "title",
    "region",
    "categories",
    "organizer",
    "start_date",
    "deadline",
    "timezone",
    "eligibility",
    "fee",
    "prize",
    "official_url",
    "rules_url",
    "verified_on",
    "en",
}

CATEGORY_LABELS = {
    "en": {
        "video": "🎬 Video",
        "image": "🖼️ Image",
        "audio": "🎵 Audio",
        "text": "✍️ Writing",
        "app": "🧩 App",
    },
    "zh": {
        "video": "🎬 视频",
        "image": "🖼️ 图像",
        "audio": "🎵 音频",
        "text": "✍️ 文字",
        "app": "🧩 应用",
    },
}

TRANSLATED_FIELDS = {"title", "region", "organizer", "timezone", "eligibility", "fee", "prize"}

ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_date(value: str, field: str, contest_id: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError(f"{contest_id}: {field} 必须为 YYYY-MM-DD") from exc


def load_contests(path: Path = DATA_PATH) -> list[dict]:
    contests = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(contests, list):
        raise ValueError("data/contests.json 顶层必须是数组")
    validate_contests(contests)
    return contests


def validate_contests(contests: list[dict]) -> None:
    seen: set[str] = set()
    for item in contests:
        if not isinstance(item, dict):
            raise ValueError("每条赛事记录必须是对象")
        missing = REQUIRED_FIELDS - item.keys()
        if missing:
            raise ValueError(f"{item.get('id', '<unknown>')}: 缺少字段 {sorted(missing)}")
        unknown_fields = item.keys() - REQUIRED_FIELDS
        if unknown_fields:
            raise ValueError(f"{item.get('id', '<unknown>')}: 未知字段 {sorted(unknown_fields)}")

        contest_id = item["id"]
        if not isinstance(contest_id, str) or not ID_PATTERN.fullmatch(contest_id):
            raise ValueError(f"无效 id: {contest_id!r}，只能使用小写字母、数字和连字符")
        if contest_id in seen:
            raise ValueError(f"重复 id: {contest_id}")
        seen.add(contest_id)

        text_fields = REQUIRED_FIELDS - {"categories", "en"}
        empty_fields = [
            field for field in text_fields
            if not isinstance(item[field], str) or not item[field].strip()
        ]
        if empty_fields:
            raise ValueError(f"{contest_id}: 字段不能为空 {sorted(empty_fields)}")

        start = parse_date(item["start_date"], "start_date", contest_id)
        deadline = parse_date(item["deadline"], "deadline", contest_id)
        verified = parse_date(item["verified_on"], "verified_on", contest_id)
        if start > deadline:
            raise ValueError(f"{contest_id}: start_date 晚于 deadline")
        if verified > date.today():
            raise ValueError(f"{contest_id}: verified_on 不能晚于今天")

        if not isinstance(item["categories"], list) or not item["categories"]:
            raise ValueError(f"{contest_id}: categories 不能为空")
        if len(item["categories"]) != len(set(item["categories"])):
            raise ValueError(f"{contest_id}: categories 不能重复")
        unknown = set(item["categories"]) - CATEGORY_LABELS["en"].keys()
        if unknown:
            raise ValueError(f"{contest_id}: 未知类别 {sorted(unknown)}")
        for url_field in ("official_url", "rules_url"):
            parsed = urlparse(item[url_field])
            if parsed.scheme != "https" or not parsed.netloc:
                raise ValueError(f"{contest_id}: {url_field} 必须使用 https://")

        if not isinstance(item["en"], dict):
            raise ValueError(f"{contest_id}: en 必须是对象")
        missing_translations = TRANSLATED_FIELDS - item["en"].keys()
        unknown_translations = item["en"].keys() - TRANSLATED_FIELDS
        if missing_translations or unknown_translations:
            raise ValueError(
                f"{contest_id}: en 字段不匹配；缺少 {sorted(missing_translations)}；"
                f"未知 {sorted(unknown_translations)}"
            )
        empty_translations = [
            field for field in TRANSLATED_FIELDS
            if not isinstance(item["en"][field], str) or not item["en"][field].strip()
        ]
        if empty_translations:
            raise ValueError(f"{contest_id}: en 字段不能为空 {sorted(empty_translations)}")


def escape_cell(value: str) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def status_label(deadline: date, today: date, language: str = "en") -> str:
    days = (deadline - today).days
    if days <= 3:
        if language == "zh":
            return f"🔥 {days} 天内截止" if days else "🔥 今天截止"
        return f"🔥 {days} days left" if days else "🔥 Due today"
    if days <= 7:
        return "⏳ 7 天内截止" if language == "zh" else "⏳ Due within 7 days"
    return "🟢 报名中" if language == "zh" else "🟢 Open"


def localized(item: dict, field: str, language: str) -> str:
    return item[field] if language == "zh" else item["en"][field]


def render_table(contests: list[dict], today: date, upcoming: bool = False, language: str = "en") -> str:
    if not contests:
        return "_暂无已核验赛事。欢迎提交补充。_" if language == "zh" else "_No verified contests yet. Contributions are welcome._"

    header = (
        "| 状态 | 截止时间 | 类别 | 赛事与要求 | 地区 / 资格 | 奖励 / 费用 |\n|---|---|---|---|---|---|"
        if language == "zh"
        else "| Status | Deadline | Category | Contest & requirements | Region / eligibility | Prize / fee |\n|---|---|---|---|---|---|"
    )
    rows = []
    for item in sorted(contests, key=lambda entry: (entry["deadline"], entry["title"])):
        deadline = parse_date(item["deadline"], "deadline", item["id"])
        categories = "<br>".join(CATEGORY_LABELS[language][name] for name in item["categories"])
        if upcoming:
            status = f"🔵 {item['start_date']} 开放" if language == "zh" else f"🔵 Opens {item['start_date']}"
        else:
            status = status_label(deadline, today, language)
        rules_label = "规则" if language == "zh" else "Rules"
        fee_label = "费用" if language == "zh" else "Fee"
        label_separator = "：" if language == "zh" else ": "
        title = f"**[{localized(item, 'title', language)}]({item['official_url']})**<br><sub>{localized(item, 'eligibility', language)} · [{rules_label}]({item['rules_url']})</sub>"
        reward = f"{localized(item, 'prize', language)}<br><sub>{fee_label}{label_separator}{localized(item, 'fee', language)}</sub>"
        row = [
            status,
            f"{item['deadline']}<br><sub>{localized(item, 'timezone', language)}</sub>",
            categories,
            title,
            localized(item, "region", language),
            reward,
        ]
        rows.append("| " + " | ".join(escape_cell(cell) for cell in row) + " |")
    return header + "\n" + "\n".join(rows)


def render_readme(contests: list[dict], today: date, language: str = "en") -> str:
    visible = [item for item in contests if parse_date(item["deadline"], "deadline", item["id"]) >= today]
    open_now = [item for item in visible if parse_date(item["start_date"], "start_date", item["id"]) <= today]
    upcoming = [item for item in visible if parse_date(item["start_date"], "start_date", item["id"]) > today]
    verified_on = max((item["verified_on"] for item in visible), default=today.isoformat())
    template_path = ZH_TEMPLATE_PATH if language == "zh" else TEMPLATE_PATH
    template = template_path.read_text(encoding="utf-8")
    replacements = {
        "{{COUNT}}": str(len(visible)),
        "{{UPDATED_AT}}": verified_on,
        "{{OPEN_TABLE}}": render_table(open_now, today, language=language),
        "{{UPCOMING_TABLE}}": render_table(upcoming, today, upcoming=True, language=language),
    }
    for marker, value in replacements.items():
        template = template.replace(marker, value)
    return template


def visible_contests(contests: list[dict], today: date) -> list[dict]:
    return sorted(
        (
            item for item in contests
            if parse_date(item["deadline"], "deadline", item["id"]) >= today
        ),
        key=lambda item: (item["deadline"], item["title"]),
    )


def render_rss(contests: list[dict], today: date) -> str:
    active = visible_contests(contests, today)
    updated = max((parse_date(item["verified_on"], "verified_on", item["id"]) for item in active), default=today)
    pub_date = format_datetime(datetime.combine(updated, time.min, tzinfo=timezone.utc))
    items = []
    for item in active:
        item_verified = parse_date(item["verified_on"], "verified_on", item["id"])
        item_pub_date = format_datetime(datetime.combine(item_verified, time.min, tzinfo=timezone.utc))
        description = (
            f"Deadline: {item['deadline']} ({item['en']['timezone']}); "
            f"region/eligibility: {item['en']['region']}; fee: {item['en']['fee']}; "
            f"prize: {item['en']['prize']}."
        )
        items.append(
            "\n".join(
                [
                    "    <item>",
                    f"      <title>{xml_escape(item['en']['title'])}</title>",
                    f"      <link>{xml_escape(item['official_url'])}</link>",
                    f"      <guid isPermaLink=\"false\">{xml_escape(item['id'])}</guid>",
                    f"      <pubDate>{item_pub_date}</pubDate>",
                    f"      <description>{xml_escape(description)}</description>",
                    "    </item>",
                ]
            )
        )
    item_block = "\n".join(items)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Awesome AIGC Creative Contests</title>
    <link>{REPOSITORY_URL}</link>
    <description>Updates to active and upcoming AIGC creative contests worldwide</description>
    <language>en</language>
    <lastBuildDate>{pub_date}</lastBuildDate>
    <atom:link href="{PUBLIC_BASE_URL}/feed.xml" rel="self" type="application/rss+xml" />
{item_block}
  </channel>
</rss>
"""


def escape_ics(value: str) -> str:
    return value.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def fold_ics_line(line: str) -> list[str]:
    folded: list[str] = []
    current = ""
    limit = 75
    for char in line:
        if current and len((current + char).encode("utf-8")) > limit:
            folded.append(current)
            current = " " + char
            limit = 75
        else:
            current += char
    folded.append(current)
    return folded


def render_ics(contests: list[dict], today: date) -> str:
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Awesome AIGC Creative Contests//Deadlines//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:AIGC Creative Contest Deadlines",
        "X-WR-CALDESC:Current deadlines from Awesome AIGC Creative Contests",
    ]
    for item in visible_contests(contests, today):
        deadline = parse_date(item["deadline"], "deadline", item["id"])
        verified = parse_date(item["verified_on"], "verified_on", item["id"])
        description = (
            f"{item['en']['eligibility']}\nTime zone: {item['en']['timezone']}\n"
            f"Fee: {item['en']['fee']}\nPrize: {item['en']['prize']}"
        )
        lines.extend(
            [
                "BEGIN:VEVENT",
                f"UID:{item['id']}@awesome-aigc-creative-contests",
                f"DTSTAMP:{verified.strftime('%Y%m%d')}T000000Z",
                f"DTSTART;VALUE=DATE:{deadline.strftime('%Y%m%d')}",
                f"DTEND;VALUE=DATE:{(deadline + timedelta(days=1)).strftime('%Y%m%d')}",
                f"SUMMARY:{escape_ics('Deadline: ' + item['en']['title'])}",
                f"DESCRIPTION:{escape_ics(description)}",
                f"URL:{item['official_url']}",
                "TRANSP:TRANSPARENT",
                "END:VEVENT",
            ]
        )
    lines.append("END:VCALENDAR")
    return "\r\n".join(part for line in lines for part in fold_ics_line(line)) + "\r\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="检查 README、RSS 和 ICS 是否为最新，不写文件")
    parser.add_argument("--prune", action="store_true", help="从数据文件删除已经截止的赛事")
    parser.add_argument("--today", type=date.fromisoformat, default=date.today(), help="指定当前日期，格式 YYYY-MM-DD")
    args = parser.parse_args()

    try:
        contests = load_contests()
        if args.prune:
            active = [
                item
                for item in contests
                if parse_date(item["deadline"], "deadline", item["id"]) >= args.today
            ]
            if active != contests:
                DATA_PATH.write_text(json.dumps(active, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            contests = active

        outputs = {
            README_PATH: render_readme(contests, args.today, "en"),
            ZH_README_PATH: render_readme(contests, args.today, "zh"),
            RSS_PATH: render_rss(contests, args.today),
            ICS_PATH: render_ics(contests, args.today),
        }
        if args.check:
            outdated = [
                path.name for path, rendered in outputs.items()
                if not path.exists() or path.read_bytes().decode("utf-8") != rendered
            ]
            if outdated:
                print(f"生成文件不是最新：{', '.join(outdated)}；请运行 python3 scripts/build_readme.py", file=sys.stderr)
                return 1
            print("README.md、README.zh-CN.md、feed.xml 和 deadlines.ics 已是最新")
            return 0

        for path, rendered in outputs.items():
            path.write_text(rendered, encoding="utf-8")
        print(f"已生成 README.md、README.zh-CN.md、feed.xml 和 deadlines.ics，收录 {len(contests)} 条赛事")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
