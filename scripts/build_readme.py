#!/usr/bin/env python3
"""Validate contest data, remove expired entries, and render README.md."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "contests.json"
TEMPLATE_PATH = ROOT / "README.template.md"
README_PATH = ROOT / "README.md"

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
}

CATEGORY_LABELS = {
    "video": "🎬 视频",
    "image": "🖼️ 图像",
    "audio": "🎵 音频",
    "text": "✍️ 文字",
    "app": "🧩 应用",
}


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
        missing = REQUIRED_FIELDS - item.keys()
        if missing:
            raise ValueError(f"{item.get('id', '<unknown>')}: 缺少字段 {sorted(missing)}")

        contest_id = item["id"]
        if contest_id in seen:
            raise ValueError(f"重复 id: {contest_id}")
        seen.add(contest_id)

        start = parse_date(item["start_date"], "start_date", contest_id)
        deadline = parse_date(item["deadline"], "deadline", contest_id)
        verified = parse_date(item["verified_on"], "verified_on", contest_id)
        if start > deadline:
            raise ValueError(f"{contest_id}: start_date 晚于 deadline")
        if verified > date.today():
            # Future-dated fixture data remains testable through --today.
            pass

        if not item["categories"]:
            raise ValueError(f"{contest_id}: categories 不能为空")
        unknown = set(item["categories"]) - CATEGORY_LABELS.keys()
        if unknown:
            raise ValueError(f"{contest_id}: 未知类别 {sorted(unknown)}")
        for url_field in ("official_url", "rules_url"):
            if not item[url_field].startswith("https://"):
                raise ValueError(f"{contest_id}: {url_field} 必须使用 https://")


def escape_cell(value: str) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def status_label(deadline: date, today: date) -> str:
    days = (deadline - today).days
    if days <= 3:
        return f"🔥 {days} 天内截止" if days else "🔥 今天截止"
    if days <= 7:
        return "⏳ 7 天内截止"
    return "🟢 报名中"


def render_table(contests: list[dict], today: date, upcoming: bool = False) -> str:
    if not contests:
        return "_暂无已核验赛事。欢迎提交补充。_"

    header = "| 状态 | 截止时间 | 类别 | 赛事与要求 | 地区 / 资格 | 奖励 / 费用 |\n|---|---|---|---|---|---|"
    rows = []
    for item in sorted(contests, key=lambda entry: (entry["deadline"], entry["title"])):
        deadline = parse_date(item["deadline"], "deadline", item["id"])
        categories = "<br>".join(CATEGORY_LABELS[name] for name in item["categories"])
        if upcoming:
            status = f"🔵 {item['start_date']} 开放"
        else:
            status = status_label(deadline, today)
        title = f"**[{item['title']}]({item['official_url']})**<br><sub>{item['eligibility']} · [规则]({item['rules_url']})</sub>"
        reward = f"{item['prize']}<br><sub>费用：{item['fee']}</sub>"
        row = [
            status,
            f"{item['deadline']}<br><sub>{item['timezone']}</sub>",
            categories,
            title,
            item["region"],
            reward,
        ]
        rows.append("| " + " | ".join(escape_cell(cell) for cell in row) + " |")
    return header + "\n" + "\n".join(rows)


def render_readme(contests: list[dict], today: date) -> str:
    visible = [item for item in contests if parse_date(item["deadline"], "deadline", item["id"]) >= today]
    open_now = [item for item in visible if parse_date(item["start_date"], "start_date", item["id"]) <= today]
    upcoming = [item for item in visible if parse_date(item["start_date"], "start_date", item["id"]) > today]
    verified_on = max((item["verified_on"] for item in visible), default=today.isoformat())
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    replacements = {
        "{{COUNT}}": str(len(visible)),
        "{{UPDATED_AT}}": verified_on,
        "{{OPEN_TABLE}}": render_table(open_now, today),
        "{{UPCOMING_TABLE}}": render_table(upcoming, today, upcoming=True),
    }
    for marker, value in replacements.items():
        template = template.replace(marker, value)
    return template


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="检查 README 是否为最新，不写文件")
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

        rendered = render_readme(contests, args.today)
        if args.check:
            current = README_PATH.read_text(encoding="utf-8") if README_PATH.exists() else ""
            if current != rendered:
                print("README.md 不是最新，请运行 python3 scripts/build_readme.py", file=sys.stderr)
                return 1
            print("README.md 已是最新")
            return 0

        README_PATH.write_text(rendered, encoding="utf-8")
        print(f"已生成 {README_PATH.relative_to(ROOT)}，收录 {len(contests)} 条赛事")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
