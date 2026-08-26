#!/usr/bin/env python3
"""Render and send the daily contest digest to a WeCom group robot."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date
from typing import Callable
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlparse
from urllib.request import Request, urlopen

from build_readme import CATEGORY_LABELS, load_contests, parse_date


WEBHOOK_ENV_NAME = "WECOM_WEBHOOK_URL"
WECOM_WEBHOOK_HOST = "qyapi.weixin.qq.com"
WECOM_WEBHOOK_PATH = "/cgi-bin/webhook/send"
# WeCom markdown messages allow 4,096 bytes. Keep headroom for encoding and
# future formatting changes.
# https://developer.work.weixin.qq.com/document/path/91770
MAX_MESSAGE_BYTES = 3_800
REPOSITORY_URL = "https://github.com/MartinDelophy/Awesome-AIGC-Creative-Contests"
DIRECTORY_URL = f"{REPOSITORY_URL}/blob/main/README.zh-CN.md"


def clean_markdown(value: str) -> str:
    """Keep data on one line and escape characters that change markdown meaning."""

    cleaned = " ".join(str(value).split())
    for character in ("\\", "`", "*", "_", "[", "]"):
        cleaned = cleaned.replace(character, f"\\{character}")
    return cleaned


def deadline_status(item: dict, today: date) -> str:
    start = parse_date(item["start_date"], "start_date", item["id"])
    deadline = parse_date(item["deadline"], "deadline", item["id"])
    if start > today:
        days = (start - today).days
        return f"🔵 {days} 天后开放"

    days = (deadline - today).days
    if days == 0:
        return "🔥 今天截止"
    if days <= 3:
        return f"🔥 {days} 天后截止"
    if days <= 7:
        return f"⏳ {days} 天后截止"
    return f"🟢 报名中 · {days} 天后截止"


def render_contest(item: dict, today: date) -> str:
    categories = "、".join(CATEGORY_LABELS["zh"][name] for name in item["categories"])
    return "\n".join(
        [
            f"### {deadline_status(item, today)}｜{clean_markdown(item['title'])}",
            (
                f"> **截止**：{clean_markdown(item['deadline'])}"
                f"（{clean_markdown(item['timezone'])}）｜**类别**：{categories}"
            ),
            f"> **参赛资格**：{clean_markdown(item['eligibility'])}",
            f"[活动地址]({item['official_url']}) ｜ [比赛规则]({item['rules_url']})",
        ]
    )


def render_header(today: date, contest_count: int) -> str:
    return "\n".join(
        [
            "## AIGC 创作比赛每日提醒",
            f"> {today.isoformat()}｜最近更新优先｜共 {contest_count} 项",
        ]
    )


def render_footer(hidden_count: int) -> str:
    if hidden_count:
        return (
            f"> 另有 {hidden_count} 项未展示，查看 [完整比赛清单]({DIRECTORY_URL})；"
            "报名与投稿前请核对官方规则。"
        )
    return f"> 已展示全部比赛；报名与投稿前请核对 [官方清单]({DIRECTORY_URL})。"


def encoded_size(value: str) -> int:
    return len(value.encode("utf-8"))


def active_by_latest(contests: list[dict], today: date) -> list[dict]:
    active = [
        item
        for item in contests
        if parse_date(item["deadline"], "deadline", item["id"]) >= today
    ]
    return sorted(
        active,
        key=lambda item: parse_date(item["verified_on"], "verified_on", item["id"]),
        reverse=True,
    )


def compose_message(header: str, blocks: list[str], footer: str) -> str:
    return "\n\n".join([header, *blocks, footer])


def build_digest_messages(
    contests: list[dict],
    today: date,
    max_message_bytes: int = MAX_MESSAGE_BYTES,
) -> list[str]:
    active = active_by_latest(contests, today)
    header = render_header(today, len(active))
    if not active:
        return [
            compose_message(
                header,
                ["今日暂无尚未截止的已核验赛事。"],
                render_footer(0),
            )
        ]

    blocks = [render_contest(item, today) for item in active]
    selected: list[str] = []
    for block in blocks:
        candidate = [*selected, block]
        hidden_count = len(blocks) - len(candidate)
        message = compose_message(header, candidate, render_footer(hidden_count))
        if encoded_size(message) > max_message_bytes:
            break
        selected = candidate

    if not selected:
        raise ValueError("单条赛事信息超过企业微信消息长度上限，请精简该赛事字段")
    hidden_count = len(blocks) - len(selected)
    return [compose_message(header, selected, render_footer(hidden_count))]


def validate_webhook_url(webhook_url: str) -> str:
    value = webhook_url.strip()
    parsed = urlparse(value)
    query = parse_qs(parsed.query, keep_blank_values=True)
    key_values = query.get("key", [])
    if (
        parsed.scheme != "https"
        or parsed.netloc != WECOM_WEBHOOK_HOST
        or parsed.path != WECOM_WEBHOOK_PATH
        or set(query) != {"key"}
        or len(key_values) != 1
        or not key_values[0].strip()
        or parsed.fragment
    ):
        raise ValueError("WECOM_WEBHOOK_URL 不是有效的企业微信群机器人地址")
    return value


def send_markdown(
    webhook_url: str,
    content: str,
    timeout: float = 15,
    opener: Callable = urlopen,
) -> dict:
    url = validate_webhook_url(webhook_url)
    payload = json.dumps(
        {"msgtype": "markdown", "markdown": {"content": content}},
        ensure_ascii=False,
    ).encode("utf-8")
    request = Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )

    try:
        with opener(request, timeout=timeout) as response:
            response_body = response.read().decode("utf-8")
    except HTTPError as exc:
        raise RuntimeError(f"企业微信接口返回 HTTP {exc.code}") from None
    except URLError:
        raise RuntimeError("无法连接企业微信接口") from None

    try:
        result = json.loads(response_body)
    except json.JSONDecodeError:
        raise RuntimeError("企业微信接口返回了无法解析的响应") from None
    if not isinstance(result, dict) or result.get("errcode") != 0:
        errcode = result.get("errcode", "unknown") if isinstance(result, dict) else "unknown"
        errmsg = result.get("errmsg", "unknown") if isinstance(result, dict) else "unknown"
        raise RuntimeError(f"企业微信发送失败：errcode={errcode}, errmsg={errmsg}")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--today",
        type=date.fromisoformat,
        default=date.today(),
        help="指定当前日期，格式 YYYY-MM-DD",
    )
    parser.add_argument("--dry-run", action="store_true", help="仅生成并打印通知，不调用企业微信接口")
    args = parser.parse_args()

    try:
        contests = load_contests()
        messages = build_digest_messages(contests, args.today)
        if args.dry_run:
            for index, message in enumerate(messages, start=1):
                print(f"--- 企业微信消息 {index}/{len(messages)}（{encoded_size(message)} bytes）---")
                print(message)
            return 0

        webhook_url = os.environ.get(WEBHOOK_ENV_NAME, "")
        if not webhook_url.strip():
            raise ValueError(f"未设置环境变量 {WEBHOOK_ENV_NAME}")
        for index, message in enumerate(messages, start=1):
            send_markdown(webhook_url, message)
            print(f"已发送企业微信消息 {index}/{len(messages)}")
        return 0
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
