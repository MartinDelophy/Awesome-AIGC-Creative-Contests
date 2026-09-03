#!/usr/bin/env python3
"""Validate and prune opt-in opportunity datasets without changing the core feed."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

import build_readme as core


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "opportunities" / "manifest.json"
CORE_PATH = ROOT / "data" / "contests.json"
SOURCES_PATH = ROOT / "data" / "sources.json"

MANIFEST_FIELDS = {"$schema", "version", "updated_on", "default_core_path", "datasets"}
DATASET_FIELDS = {
    "id",
    "path",
    "label",
    "description",
    "region_codes",
    "record_count",
    "default_included",
}
LOCALIZED_FIELDS = {"zh", "en"}
SHARD_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.json$")
REGION_CODE_PATTERN = re.compile(r"^(?:GLOBAL|[A-Z]{2}(?:-(?:[A-Z0-9]{1,3}|\*))?)$")
EXTENDED_CATEGORIES = set(core.CATEGORY_LABELS["en"]) | {
    "code",
    "research",
    "hardware",
    "business",
    "other",
}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate_localized_text(value, label: str) -> None:
    if not isinstance(value, dict) or set(value) != LOCALIZED_FIELDS:
        raise ValueError(f"{label}: 必须且只能包含 zh、en")
    if any(not isinstance(text, str) or not text.strip() for text in value.values()):
        raise ValueError(f"{label}: zh、en 均不能为空")


def validate_string_list(value, label: str) -> None:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{label}: 必须是非空数组")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        raise ValueError(f"{label}: 只能包含非空字符串")
    if len(value) != len(set(value)):
        raise ValueError(f"{label}: 不能重复")


def validate_manifest(manifest: dict, *, today: date) -> list[dict]:
    if not isinstance(manifest, dict) or set(manifest) != MANIFEST_FIELDS:
        actual = set(manifest) if isinstance(manifest, dict) else set()
        raise ValueError(
            "data/opportunities/manifest.json 字段不匹配；"
            f"缺少 {sorted(MANIFEST_FIELDS - actual)}；未知 {sorted(actual - MANIFEST_FIELDS)}"
        )
    if manifest["$schema"] != "./manifest.schema.json":
        raise ValueError("manifest.$schema 必须为 ./manifest.schema.json")
    if manifest["version"] != 1 or isinstance(manifest["version"], bool):
        raise ValueError("manifest.version 必须为 1")
    if manifest["default_core_path"] != "../contests.json":
        raise ValueError("manifest.default_core_path 必须为 ../contests.json")
    updated_on = core.parse_date(manifest["updated_on"], "updated_on", "manifest")
    if updated_on > today:
        raise ValueError("manifest.updated_on 不能晚于指定日期")

    datasets = manifest["datasets"]
    if not isinstance(datasets, list) or not datasets:
        raise ValueError("manifest.datasets 必须是非空数组")
    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    for dataset in datasets:
        if not isinstance(dataset, dict):
            raise ValueError("manifest.datasets 中的每项必须是对象")
        dataset_id = dataset.get("id", "<unknown>")
        missing = DATASET_FIELDS - dataset.keys()
        unknown = dataset.keys() - DATASET_FIELDS
        if missing or unknown:
            raise ValueError(
                f"{dataset_id}: 分片字段不匹配；缺少 {sorted(missing)}；未知 {sorted(unknown)}"
            )
        if not isinstance(dataset_id, str) or not core.ID_PATTERN.fullmatch(dataset_id):
            raise ValueError(f"无效分片 id: {dataset_id!r}")
        if dataset_id in seen_ids:
            raise ValueError(f"重复分片 id: {dataset_id}")
        seen_ids.add(dataset_id)

        shard_name = dataset["path"]
        if not isinstance(shard_name, str) or not SHARD_NAME_PATTERN.fullmatch(shard_name):
            raise ValueError(f"{dataset_id}.path: 必须是当前目录下的小写 JSON 文件名")
        if shard_name in {"manifest.json", "schema.json", "manifest.schema.json"}:
            raise ValueError(f"{dataset_id}.path: 不能指向清单或 schema")
        if shard_name in seen_paths:
            raise ValueError(f"重复分片路径: {shard_name}")
        seen_paths.add(shard_name)

        validate_localized_text(dataset["label"], f"{dataset_id}.label")
        validate_localized_text(dataset["description"], f"{dataset_id}.description")
        validate_string_list(dataset["region_codes"], f"{dataset_id}.region_codes")
        invalid_regions = [
            value for value in dataset["region_codes"] if not REGION_CODE_PATTERN.fullmatch(value)
        ]
        if invalid_regions:
            raise ValueError(f"{dataset_id}.region_codes: 格式无效 {invalid_regions}")
        record_count = dataset["record_count"]
        if isinstance(record_count, bool) or not isinstance(record_count, int) or record_count < 0:
            raise ValueError(f"{dataset_id}.record_count: 必须是非负整数")
        if dataset["default_included"] is not False:
            raise ValueError(f"{dataset_id}.default_included: 可选分片必须为 false")
    return datasets


def source_tiers(sources) -> dict[str, str]:
    if not isinstance(sources, list):
        raise ValueError("data/sources.json 顶层必须是数组")
    tiers: dict[str, str] = {}
    for source in sources:
        if not isinstance(source, dict):
            raise ValueError("data/sources.json 中的每项必须是对象")
        source_id = source.get("id")
        tier = source.get("trust_tier")
        if not isinstance(source_id, str) or not core.ID_PATTERN.fullmatch(source_id):
            raise ValueError(f"data/sources.json 包含无效来源 id: {source_id!r}")
        if source_id in tiers:
            raise ValueError(f"data/sources.json 包含重复来源 id: {source_id}")
        if tier not in core.SOURCE_TIERS:
            raise ValueError(f"{source_id}: trust_tier 无效")
        tiers[source_id] = tier
    return tiers


def normalized_official_url(value: str) -> str:
    return value.rstrip("/")


def validate_repository(
    *,
    manifest_path: Path = MANIFEST_PATH,
    core_path: Path = CORE_PATH,
    sources_path: Path = SOURCES_PATH,
    today: date = date.today(),
) -> tuple[dict, dict[str, tuple[Path, list[dict]]]]:
    manifest = read_json(manifest_path)
    datasets = validate_manifest(manifest, today=today)
    core_records = core.load_contests(core_path)
    registered_sources = source_tiers(read_json(sources_path))

    manifest_dir = manifest_path.parent
    if not (manifest_dir / "schema.json").is_file():
        raise ValueError("缺少 data/opportunities/schema.json")
    if not (manifest_dir / "manifest.schema.json").is_file():
        raise ValueError("缺少 data/opportunities/manifest.schema.json")

    listed_paths = {dataset["path"] for dataset in datasets}
    actual_paths = {
        path.name
        for path in manifest_dir.glob("*.json")
        if path.name not in {"manifest.json", "schema.json", "manifest.schema.json"}
    }
    if listed_paths != actual_paths:
        raise ValueError(
            "可选分片与 manifest 不一致；"
            f"缺少文件 {sorted(listed_paths - actual_paths)}；未登记文件 {sorted(actual_paths - listed_paths)}"
        )

    seen_ids = {record["id"] for record in core_records}
    seen_urls = {normalized_official_url(record["official_url"]) for record in core_records}
    shards: dict[str, tuple[Path, list[dict]]] = {}
    for dataset in datasets:
        shard_path = manifest_dir / dataset["path"]
        records = read_json(shard_path)
        if not isinstance(records, list):
            raise ValueError(f"{dataset['path']}: 顶层必须是数组")
        core.validate_contests(
            records,
            allowed_extra_fields=core.EXTENDED_FIELDS,
            required_extra_fields=core.EXTENDED_FIELDS,
            category_names=EXTENDED_CATEGORIES,
        )
        if dataset["record_count"] != len(records):
            raise ValueError(
                f"{dataset['id']}.record_count: manifest 为 {dataset['record_count']}，"
                f"实际为 {len(records)}"
            )

        for record in records:
            record_id = record["id"]
            if record_id in seen_ids:
                raise ValueError(f"核心清单或可选分片中存在重复 id: {record_id}")
            seen_ids.add(record_id)
            official_url = normalized_official_url(record["official_url"])
            if official_url in seen_urls:
                raise ValueError(f"核心清单或可选分片中存在重复 official_url: {official_url}")
            seen_urls.add(official_url)

            metadata = record["source_meta"]
            source_id = metadata["source_id"]
            if source_id not in registered_sources:
                raise ValueError(f"{record_id}: source_meta.source_id 未在 data/sources.json 注册")
            if metadata["source_tier"] != registered_sources[source_id]:
                raise ValueError(f"{record_id}: source_meta.source_tier 与来源注册表不一致")
            last_checked = core.parse_date(
                metadata["last_checked"], "source_meta.last_checked", record_id
            )
            if last_checked > today:
                raise ValueError(f"{record_id}: source_meta.last_checked 不能晚于指定日期")
        shards[dataset["id"]] = (shard_path, records)
    return manifest, shards


def prune_expired(
    *,
    manifest_path: Path = MANIFEST_PATH,
    core_path: Path = CORE_PATH,
    sources_path: Path = SOURCES_PATH,
    today: date,
) -> int:
    manifest, shards = validate_repository(
        manifest_path=manifest_path,
        core_path=core_path,
        sources_path=sources_path,
        today=today,
    )
    removed = 0
    by_id = {dataset["id"]: dataset for dataset in manifest["datasets"]}
    for dataset_id, (path, records) in shards.items():
        active = [
            record
            for record in records
            if core.parse_date(record["deadline"], "deadline", record["id"]) >= today
        ]
        if active != records:
            removed += len(records) - len(active)
            write_json(path, active)
            by_id[dataset_id]["record_count"] = len(active)
    if removed:
        manifest["updated_on"] = today.isoformat()
        write_json(manifest_path, manifest)
        validate_repository(
            manifest_path=manifest_path,
            core_path=core_path,
            sources_path=sources_path,
            today=today,
        )
    return removed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="只校验核心/扩展边界、manifest 和分片")
    mode.add_argument("--prune", action="store_true", help="只从可选分片删除已截止记录")
    parser.add_argument("--today", type=date.fromisoformat, default=date.today())
    args = parser.parse_args()

    try:
        removed = 0
        if args.prune:
            removed = prune_expired(today=args.today)
        manifest, shards = validate_repository(today=args.today)
        record_count = sum(len(records) for _, records in shards.values())
        message = (
            f"已校验 {len(manifest['datasets'])} 个可选分片和 {record_count} 条扩展机会；"
            "核心清单保持独立"
        )
        if args.prune:
            message += f"；删除 {removed} 条已截止扩展机会"
        print(message)
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
