#!/usr/bin/env python3
"""Discover contest candidates from the registered public sources.

Discovery is intentionally separated from publication. This script only writes
data/candidates.json; a candidate must still be checked against an official
event page and promoted manually to data/contests.json.
"""

from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import re
import sys
from datetime import date, datetime, timezone
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Callable, Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, urlencode, urljoin, urlparse, urlunparse
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
SOURCES_PATH = ROOT / "data" / "sources.json"
CANDIDATES_PATH = ROOT / "data" / "candidates.json"
CONTESTS_PATH = ROOT / "data" / "contests.json"

USER_AGENT = "Awesome-AIGC-Creative-Contests/1.0 (+https://github.com/MartinDelophy/Awesome-AIGC-Creative-Contests)"
MAX_RESPONSE_BYTES = 5 * 1024 * 1024

ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DEFAULT_TITLE_KEYWORDS = (
    "大赛",
    "比赛",
    "竞赛",
    "挑战赛",
    "作品征集",
    "创作征集",
    "hackathon",
    "challenge",
    "competition",
    "contest",
    "call for entries",
    "prize",
    "award",
)
DEFAULT_EXCLUDE_KEYWORDS = (
    "获奖名单",
    "获奖结果",
    "结果公示",
    "圆满落幕",
    "赛事回顾",
    "winner announced",
    "winners announced",
    "past challenge",
)
TRACKING_QUERY_KEYS = {
    "fbclid",
    "gclid",
    "mc_cid",
    "mc_eid",
    "ref",
    "source",
    "spm",
}

SOURCE_REQUIRED_FIELDS = {
    "id",
    "name",
    "url",
    "source_kind",
    "trust_tier",
    "region_codes",
    "industries",
    "cadence_hours",
    "enabled",
    "collector",
}
SOURCE_OPTIONAL_FIELDS = {"notes"}
SOURCE_KINDS = {"government", "organizer", "association", "official-platform", "aggregator"}
TRUST_TIERS = {"official-api", "official-page", "trusted-platform", "discovery-only"}
COLLECTOR_TYPES = {"html-links", "rss-atom", "json-api", "manual"}
INDUSTRIES = {
    "ai-ml",
    "advertising",
    "architecture",
    "culture-tourism",
    "data-science",
    "design",
    "education",
    "entrepreneurship",
    "film-video",
    "games",
    "innovation",
    "music-audio",
    "photography",
    "public-good",
    "science-engineering",
    "software",
    "writing",
}
COLLECTOR_FIELDS = {
    "type",
    "title_keywords",
    "link_patterns",
    "exclude_keywords",
    "same_host_only",
    "match_mode",
    "reject_past_years",
    "ignore_titles",
    "title_split_patterns",
    "items_path",
    "title_path",
    "url_path",
}
CANDIDATE_REQUIRED_FIELDS = {
    "id",
    "source_id",
    "title",
    "discovered_url",
    "source_tier",
    "first_seen",
    "last_seen",
    "status",
    "match_reason",
}
CANDIDATE_OPTIONAL_FIELDS = {"review_notes"}
CANDIDATE_STATUSES = {"new", "reviewing", "accepted", "rejected"}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def parse_iso_date(value: str, label: str) -> date:
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} 必须为 YYYY-MM-DD") from exc


def validate_https_url(value: str, label: str) -> None:
    if not isinstance(value, str):
        raise ValueError(f"{label} 必须是字符串")
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.hostname:
        raise ValueError(f"{label} 必须是公开的 https:// URL")
    hostname = parsed.hostname.lower()
    if hostname == "localhost" or hostname.endswith(".localhost"):
        raise ValueError(f"{label} 不允许指向本机")
    try:
        address = ipaddress.ip_address(hostname)
    except ValueError:
        return
    if not address.is_global:
        raise ValueError(f"{label} 不允许指向私有或保留地址")


def validate_string_list(value, label: str, allowed: set[str] | None = None) -> None:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{label} 必须是非空数组")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        raise ValueError(f"{label} 只能包含非空字符串")
    if len(value) != len(set(value)):
        raise ValueError(f"{label} 不能包含重复值")
    if allowed is not None and (unknown := set(value) - allowed):
        raise ValueError(f"{label} 包含未知值 {sorted(unknown)}")


def validate_sources(sources: list[dict]) -> None:
    if not isinstance(sources, list) or not sources:
        raise ValueError("data/sources.json 顶层必须是非空数组")

    seen: set[str] = set()
    for source in sources:
        if not isinstance(source, dict):
            raise ValueError("每个来源必须是对象")
        source_id = source.get("id", "<unknown>")
        missing = SOURCE_REQUIRED_FIELDS - source.keys()
        unknown = source.keys() - SOURCE_REQUIRED_FIELDS - SOURCE_OPTIONAL_FIELDS
        if missing or unknown:
            raise ValueError(f"{source_id}: 来源字段不匹配；缺少 {sorted(missing)}；未知 {sorted(unknown)}")
        if not isinstance(source_id, str) or not ID_PATTERN.fullmatch(source_id):
            raise ValueError(f"无效来源 id: {source_id!r}")
        if source_id in seen:
            raise ValueError(f"重复来源 id: {source_id}")
        seen.add(source_id)
        if not isinstance(source["name"], str) or not source["name"].strip():
            raise ValueError(f"{source_id}: name 不能为空")
        validate_https_url(source["url"], f"{source_id}.url")
        if source["source_kind"] not in SOURCE_KINDS:
            raise ValueError(f"{source_id}: 未知 source_kind")
        if source["trust_tier"] not in TRUST_TIERS:
            raise ValueError(f"{source_id}: 未知 trust_tier")
        validate_string_list(source["region_codes"], f"{source_id}.region_codes")
        validate_string_list(source["industries"], f"{source_id}.industries", INDUSTRIES)
        if not isinstance(source["cadence_hours"], int) or source["cadence_hours"] < 1:
            raise ValueError(f"{source_id}: cadence_hours 必须是正整数")
        if not isinstance(source["enabled"], bool):
            raise ValueError(f"{source_id}: enabled 必须是布尔值")

        collector = source["collector"]
        if not isinstance(collector, dict) or "type" not in collector:
            raise ValueError(f"{source_id}: collector 必须包含 type")
        if unknown_collector_fields := collector.keys() - COLLECTOR_FIELDS:
            raise ValueError(f"{source_id}: collector 包含未知字段 {sorted(unknown_collector_fields)}")
        if collector["type"] not in COLLECTOR_TYPES:
            raise ValueError(f"{source_id}: 未知 collector.type")
        if source["enabled"] and collector["type"] == "manual":
            raise ValueError(f"{source_id}: manual 来源不能设置 enabled=true")
        for field in ("title_keywords", "link_patterns", "exclude_keywords", "ignore_titles", "title_split_patterns"):
            if field in collector:
                validate_string_list(collector[field], f"{source_id}.collector.{field}")
        if "same_host_only" in collector and not isinstance(collector["same_host_only"], bool):
            raise ValueError(f"{source_id}: same_host_only 必须是布尔值")
        if collector.get("match_mode", "any") not in {"any", "all"}:
            raise ValueError(f"{source_id}: match_mode 必须为 any 或 all")
        if "reject_past_years" in collector and not isinstance(collector["reject_past_years"], bool):
            raise ValueError(f"{source_id}: reject_past_years 必须是布尔值")
        if collector["type"] == "json-api":
            for field in ("items_path", "title_path", "url_path"):
                if not isinstance(collector.get(field), str) or not collector[field].strip():
                    raise ValueError(f"{source_id}: json-api 缺少 {field}")


def validate_candidates(candidates: list[dict], source_ids: set[str]) -> None:
    if not isinstance(candidates, list):
        raise ValueError("data/candidates.json 顶层必须是数组")
    seen: set[str] = set()
    for item in candidates:
        if not isinstance(item, dict):
            raise ValueError("每条候选必须是对象")
        candidate_id = item.get("id", "<unknown>")
        missing = CANDIDATE_REQUIRED_FIELDS - item.keys()
        unknown = item.keys() - CANDIDATE_REQUIRED_FIELDS - CANDIDATE_OPTIONAL_FIELDS
        if missing or unknown:
            raise ValueError(f"{candidate_id}: 候选字段不匹配；缺少 {sorted(missing)}；未知 {sorted(unknown)}")
        if not isinstance(candidate_id, str) or not ID_PATTERN.fullmatch(candidate_id):
            raise ValueError(f"无效候选 id: {candidate_id!r}")
        if candidate_id in seen:
            raise ValueError(f"重复候选 id: {candidate_id}")
        seen.add(candidate_id)
        if item["source_id"] not in source_ids:
            raise ValueError(f"{candidate_id}: 未注册来源 {item['source_id']}")
        if item["source_tier"] not in TRUST_TIERS:
            raise ValueError(f"{candidate_id}: 未知 source_tier")
        if item["status"] not in CANDIDATE_STATUSES:
            raise ValueError(f"{candidate_id}: 未知 status")
        if not isinstance(item["title"], str) or not item["title"].strip():
            raise ValueError(f"{candidate_id}: title 不能为空")
        validate_https_url(item["discovered_url"], f"{candidate_id}.discovered_url")
        first_seen = parse_iso_date(item["first_seen"], f"{candidate_id}.first_seen")
        last_seen = parse_iso_date(item["last_seen"], f"{candidate_id}.last_seen")
        if first_seen > last_seen:
            raise ValueError(f"{candidate_id}: first_seen 不能晚于 last_seen")
        validate_string_list(item["match_reason"], f"{candidate_id}.match_reason")
        if "review_notes" in item and not isinstance(item["review_notes"], str):
            raise ValueError(f"{candidate_id}: review_notes 必须是字符串")


def load_sources(path: Path = SOURCES_PATH) -> list[dict]:
    sources = read_json(path)
    validate_sources(sources)
    return sources


def load_candidates(path: Path = CANDIDATES_PATH, source_ids: set[str] | None = None) -> list[dict]:
    candidates = read_json(path) if path.exists() else []
    validate_candidates(candidates, source_ids or {source["id"] for source in load_sources()})
    return candidates


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", unescape(str(value))).strip()


def canonical_url(value: str, base_url: str | None = None) -> str | None:
    absolute = urljoin(base_url or "", normalize_text(value))
    parsed = urlparse(absolute)
    if parsed.scheme.lower() != "https" or not parsed.hostname:
        return None
    hostname = parsed.hostname.lower()
    try:
        port = parsed.port
    except ValueError:
        return None
    netloc = hostname if port in (None, 443) else f"{hostname}:{port}"
    path = re.sub(r"/{2,}", "/", parsed.path or "/")
    query = [
        (key, value)
        for key, value in parse_qsl(parsed.query, keep_blank_values=True)
        if not key.lower().startswith("utm_") and key.lower() not in TRACKING_QUERY_KEYS
    ]
    return urlunparse(("https", netloc, path, "", urlencode(query), ""))


class AnchorExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []
        self._href: str | None = None
        self._parts: list[str] = []
        self._fallback_title = ""
        self._heading_depth = 0
        self._heading_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        normalized_tag = tag.lower()
        if self._href is not None:
            if normalized_tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
                self._heading_depth += 1
            return
        if normalized_tag != "a":
            return
        values = {key.lower(): value or "" for key, value in attrs}
        if values.get("href"):
            self._href = values["href"]
            self._parts = []
            self._fallback_title = values.get("aria-label") or values.get("title") or ""
            self._heading_depth = 0
            self._heading_parts = []
        return

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)

    def handle_data(self, data: str) -> None:
        if self._href is not None:
            self._parts.append(data)
            if self._heading_depth:
                self._heading_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        normalized_tag = tag.lower()
        if self._href is not None and normalized_tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self._heading_depth = max(0, self._heading_depth - 1)
        if normalized_tag != "a" or self._href is None:
            return
        title = (
            normalize_text(self._fallback_title)
            or normalize_text(" ".join(self._heading_parts))
            or normalize_text(" ".join(self._parts))
        )
        if title:
            self.links.append((title, self._href))
        self._href = None
        self._parts = []
        self._fallback_title = ""
        self._heading_depth = 0
        self._heading_parts = []


def clean_title(source: dict, title: str) -> str:
    cleaned = normalize_text(title)
    cleaned = re.sub(r"^\d+\s+Min Read\s+", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s+Article$", "", cleaned, flags=re.IGNORECASE)
    for marker in source["collector"].get("title_split_patterns", []):
        if marker in cleaned:
            cleaned = cleaned.split(marker, 1)[0].strip()
    return cleaned[:500].strip()


def match_reasons(source: dict, title: str, url: str) -> list[str]:
    collector = source["collector"]
    searchable_title = title.casefold()
    searchable_url = url.casefold()
    if searchable_title in {value.casefold() for value in collector.get("ignore_titles", [])}:
        return []
    excludes = tuple(DEFAULT_EXCLUDE_KEYWORDS) + tuple(collector.get("exclude_keywords", []))
    if any(term.casefold() in searchable_title for term in excludes):
        return []
    if collector.get("reject_past_years"):
        years = [int(value) for value in re.findall(r"\b20\d{2}\b", title)]
        years.extend(2000 + int(value) for value in re.findall(r"[\'’](\d{2})\b", title))
        if years and max(years) < date.today().year:
            return []

    keyword_reasons: list[str] = []
    keywords = collector.get("title_keywords", DEFAULT_TITLE_KEYWORDS)
    for keyword in keywords:
        if keyword.casefold() in searchable_title:
            keyword_reasons.append(f"title:{keyword}")
    pattern_reasons: list[str] = []
    for pattern in collector.get("link_patterns", []):
        if pattern.casefold() in searchable_url:
            pattern_reasons.append(f"url:{pattern}")
    if collector.get("match_mode", "any") == "all":
        if keywords and not keyword_reasons:
            return []
        if collector.get("link_patterns") and not pattern_reasons:
            return []
    reasons = keyword_reasons + pattern_reasons
    return list(dict.fromkeys(reasons))


def same_host(source_url: str, candidate_url: str) -> bool:
    source_host = (urlparse(source_url).hostname or "").lower()
    candidate_host = (urlparse(candidate_url).hostname or "").lower()
    return candidate_host == source_host or candidate_host.endswith(f".{source_host}")


def extract_html_candidates(source: dict, content: str) -> list[dict]:
    parser = AnchorExtractor()
    parser.feed(content)
    discovered: dict[str, dict] = {}
    for raw_title, href in parser.links:
        title = clean_title(source, raw_title)
        url = canonical_url(href, source["url"])
        if not url or url == canonical_url(source["url"]):
            continue
        if source["collector"].get("same_host_only", True) and not same_host(source["url"], url):
            continue
        reasons = match_reasons(source, title, url)
        if reasons:
            discovered[url] = {"title": title, "url": url, "match_reason": reasons}
    return list(discovered.values())


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower()


def child_text(element: ElementTree.Element, name: str) -> str:
    for child in element.iter():
        if local_name(child.tag) == name and child.text:
            return normalize_text(child.text)
    return ""


def extract_rss_candidates(source: dict, content: str) -> list[dict]:
    root = ElementTree.fromstring(content)
    discovered: dict[str, dict] = {}
    for entry in root.iter():
        if local_name(entry.tag) not in {"item", "entry"}:
            continue
        title = clean_title(source, child_text(entry, "title"))
        href = child_text(entry, "link")
        if not href:
            for child in entry.iter():
                if local_name(child.tag) == "link" and child.attrib.get("href"):
                    href = child.attrib["href"]
                    break
        url = canonical_url(href, source["url"])
        if not title or not url:
            continue
        if source["collector"].get("same_host_only", True) and not same_host(source["url"], url):
            continue
        reasons = match_reasons(source, title, url)
        if reasons:
            discovered[url] = {"title": title, "url": url, "match_reason": reasons}
    return list(discovered.values())


def value_at_path(value, path: str):
    current = value
    for part in path.split("."):
        if not part:
            continue
        if isinstance(current, list):
            current = current[int(part)]
        elif isinstance(current, dict):
            current = current[part]
        else:
            raise KeyError(path)
    return current


def extract_json_candidates(source: dict, content: str) -> list[dict]:
    payload = json.loads(content)
    collector = source["collector"]
    items = value_at_path(payload, collector["items_path"])
    if not isinstance(items, list):
        raise ValueError(f"{source['id']}: items_path 没有指向数组")
    discovered: dict[str, dict] = {}
    for item in items:
        try:
            title = clean_title(source, normalize_text(value_at_path(item, collector["title_path"])))
            url = canonical_url(value_at_path(item, collector["url_path"]), source["url"])
        except (KeyError, IndexError, TypeError, ValueError):
            continue
        if not title or not url:
            continue
        if collector.get("same_host_only", True) and not same_host(source["url"], url):
            continue
        reasons = match_reasons(source, title, url)
        if reasons:
            discovered[url] = {"title": title, "url": url, "match_reason": reasons}
    return list(discovered.values())


def extract_candidates(source: dict, content: str) -> list[dict]:
    collector_type = source["collector"]["type"]
    if collector_type == "html-links":
        return extract_html_candidates(source, content)
    if collector_type == "rss-atom":
        return extract_rss_candidates(source, content)
    if collector_type == "json-api":
        return extract_json_candidates(source, content)
    return []


def robots_allowed(url: str, timeout: float = 15.0) -> bool:
    parsed = urlparse(url)
    robots_url = urlunparse((parsed.scheme, parsed.netloc, "/robots.txt", "", "", ""))
    request = Request(robots_url, headers={"User-Agent": USER_AGENT, "Accept": "text/plain"})
    try:
        with urlopen(request, timeout=timeout) as response:
            text = response.read(512 * 1024).decode("utf-8", errors="replace")
    except HTTPError as exc:
        if exc.code in {401, 403}:
            return False
        if 400 <= exc.code < 500:
            return True
        return False
    except (OSError, URLError):
        return False
    parser = RobotFileParser()
    parser.set_url(robots_url)
    parser.parse(text.splitlines())
    return parser.can_fetch(USER_AGENT, url)


def fetch_text(source: dict, timeout: float = 20.0) -> str:
    if not robots_allowed(source["url"], timeout=min(timeout, 15.0)):
        raise PermissionError("robots.txt 不允许抓取或暂时无法核验")
    request = Request(
        source["url"],
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/rss+xml,application/atom+xml,application/json",
        },
    )
    with urlopen(request, timeout=timeout) as response:
        content = response.read(MAX_RESPONSE_BYTES + 1)
        if len(content) > MAX_RESPONSE_BYTES:
            raise ValueError("响应超过 5 MiB 限制")
        charset = response.headers.get_content_charset()
    for encoding in (charset, "utf-8", "gb18030"):
        if not encoding:
            continue
        try:
            return content.decode(encoding)
        except (LookupError, UnicodeDecodeError):
            continue
    return content.decode("utf-8", errors="replace")


def normalized_title(value: str) -> str:
    return re.sub(r"[^0-9a-z\u3400-\u9fff]+", "", normalize_text(value).casefold())


def candidate_id(source_id: str, url: str) -> str:
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]
    return f"{source_id}-{digest}"


def published_keys(contests: Iterable[dict]) -> tuple[set[str], set[str]]:
    urls: set[str] = set()
    titles: set[str] = set()
    for contest in contests:
        for field in ("official_url", "rules_url"):
            if url := canonical_url(contest.get(field, "")):
                urls.add(url)
        for title in (contest.get("title", ""), contest.get("en", {}).get("title", "")):
            if title:
                titles.add(normalized_title(title))
    return urls, titles


def merge_candidates(
    existing: list[dict],
    discoveries: list[tuple[dict, dict]],
    contests: list[dict],
    today: date,
) -> list[dict]:
    published_urls, published_titles = published_keys(contests)
    by_id = {item["id"]: dict(item) for item in existing}
    today_text = today.isoformat()

    for source, discovery in discoveries:
        url = discovery["url"]
        if url in published_urls or normalized_title(discovery["title"]) in published_titles:
            continue
        identifier = candidate_id(source["id"], url)
        if identifier in by_id:
            item = by_id[identifier]
            item["last_seen"] = today_text
            item["title"] = discovery["title"]
            item["match_reason"] = discovery["match_reason"]
            continue
        by_id[identifier] = {
            "id": identifier,
            "source_id": source["id"],
            "title": discovery["title"],
            "discovered_url": url,
            "source_tier": source["trust_tier"],
            "first_seen": today_text,
            "last_seen": today_text,
            "status": "new",
            "match_reason": discovery["match_reason"],
        }

    visible = [
        item
        for item in by_id.values()
        if canonical_url(item["discovered_url"]) not in published_urls
        and normalized_title(item["title"]) not in published_titles
    ]
    status_order = {"new": 0, "reviewing": 1, "accepted": 2, "rejected": 3}
    return sorted(visible, key=lambda item: (status_order[item["status"]], item["first_seen"], item["id"]))


def collect(
    sources: list[dict],
    fetcher: Callable[[dict, float], str] = fetch_text,
    timeout: float = 20.0,
) -> tuple[list[tuple[dict, dict]], list[tuple[str, str]], int]:
    discoveries: list[tuple[dict, dict]] = []
    failures: list[tuple[str, str]] = []
    successful = 0
    for source in sources:
        if not source["enabled"]:
            continue
        try:
            content = fetcher(source, timeout)
            for item in extract_candidates(source, content):
                discoveries.append((source, item))
            successful += 1
        except (ElementTree.ParseError, HTTPError, OSError, PermissionError, URLError, ValueError, json.JSONDecodeError) as exc:
            failures.append((source["id"], str(exc)))
    return discoveries, failures, successful


def due_sources(sources: list[dict], utc_hour: int) -> list[dict]:
    """Select sources due in the current six-hour workflow window."""
    if not 0 <= utc_hour <= 23:
        raise ValueError("utc_hour 必须在 0 到 23 之间")
    return [
        source
        for source in sources
        if source["enabled"] and utc_hour % source["cadence_hours"] < 6
    ]


def validate_contest_source_references(contests: list[dict], source_ids: set[str]) -> None:
    for contest in contests:
        source_meta = contest.get("source_meta")
        if source_meta and source_meta.get("source_id") not in source_ids:
            raise ValueError(f"{contest['id']}: source_meta.source_id 未在 data/sources.json 注册")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="只校验来源注册表和候选库")
    mode.add_argument("--collect", action="store_true", help="抓取已启用来源并更新候选库")
    mode.add_argument("--dry-run", action="store_true", help="抓取并显示摘要，但不写文件")
    parser.add_argument("--source", action="append", default=[], help="只运行指定来源，可重复传入")
    parser.add_argument("--today", type=date.fromisoformat, default=date.today())
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--respect-cadence", action="store_true", help="按照来源 cadence_hours 选择本轮来源")
    args = parser.parse_args()

    try:
        sources = load_sources()
        source_ids = {source["id"] for source in sources}
        candidates = load_candidates(source_ids=source_ids)
        contests = read_json(CONTESTS_PATH)
        validate_contest_source_references(contests, source_ids)
        if args.check:
            enabled = sum(source["enabled"] for source in sources)
            print(f"已校验 {len(sources)} 个来源（{enabled} 个启用）和 {len(candidates)} 条候选")
            return 0

        if args.timeout <= 0:
            raise ValueError("timeout 必须大于 0")

        selected = sources
        if args.source:
            requested = set(args.source)
            unknown = requested - source_ids
            if unknown:
                raise ValueError(f"未知来源: {', '.join(sorted(unknown))}")
            selected = [source for source in sources if source["id"] in requested]
            manual = [source["id"] for source in selected if source["collector"]["type"] == "manual"]
            if manual:
                raise ValueError(f"来源仅支持人工核验: {', '.join(sorted(manual))}")
            selected = [{**source, "enabled": True} for source in selected]
        elif args.respect_cadence:
            selected = due_sources(selected, datetime.now(timezone.utc).hour)

        discoveries, failures, successful = collect(selected, timeout=args.timeout)
        enabled_count = sum(source["enabled"] for source in selected)
        if enabled_count and successful == 0:
            for source_id, message in failures:
                print(f"警告：{source_id}: {message}", file=sys.stderr)
            raise RuntimeError("所有已启用来源均抓取失败，未更新候选库")
        merged = merge_candidates(candidates, discoveries, contests, args.today)
        validate_candidates(merged, source_ids)

        new_ids = {item["id"] for item in merged} - {item["id"] for item in candidates}
        print(
            f"来源成功 {successful}/{enabled_count}；发现链接 {len(discoveries)}；"
            f"新增候选 {len(new_ids)}；候选总数 {len(merged)}"
        )
        for source_id, message in failures:
            print(f"警告：{source_id}: {message}", file=sys.stderr)
        if args.dry_run:
            for item in merged:
                if item["id"] in new_ids:
                    print(f"NEW\t{item['source_id']}\t{item['title']}\t{item['discovered_url']}")
            return 0

        CANDIDATES_PATH.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return 0
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
