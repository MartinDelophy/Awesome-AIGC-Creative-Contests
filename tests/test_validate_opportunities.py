import json
import shutil
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import build_readme  # noqa: E402
import validate_opportunities  # noqa: E402


class OpportunityDatasetTests(unittest.TestCase):
    def test_repository_bundle_is_valid_and_opt_in(self):
        manifest, shards = validate_opportunities.validate_repository(today=date(2026, 9, 3))
        self.assertTrue(all(dataset["default_included"] is False for dataset in manifest["datasets"]))
        self.assertEqual(sum(len(records) for _, records in shards.values()), 2)
        self.assertEqual(set(shards), {"global", "cn-national", "cn-local"})

    def test_core_and_extension_use_separate_schemas(self):
        core_schema = json.loads((ROOT / "data" / "schema.json").read_text(encoding="utf-8"))
        extension_schema = json.loads(
            (ROOT / "data" / "opportunities" / "schema.json").read_text(encoding="utf-8")
        )
        self.assertEqual(set(core_schema["items"]["properties"]), build_readme.REQUIRED_FIELDS)
        self.assertEqual(
            set(extension_schema["items"]["required"]),
            build_readme.REQUIRED_FIELDS | build_readme.EXTENDED_FIELDS,
        )

    def test_manifest_rejects_path_traversal(self):
        manifest = json.loads(
            (ROOT / "data" / "opportunities" / "manifest.json").read_text(encoding="utf-8")
        )
        manifest["datasets"][0]["path"] = "../global.json"
        with self.assertRaisesRegex(ValueError, "当前目录下"):
            validate_opportunities.validate_manifest(manifest, today=date(2026, 9, 3))

    def test_manifest_rejects_default_inclusion(self):
        manifest = json.loads(
            (ROOT / "data" / "opportunities" / "manifest.json").read_text(encoding="utf-8")
        )
        manifest["datasets"][0]["default_included"] = True
        with self.assertRaisesRegex(ValueError, "必须为 false"):
            validate_opportunities.validate_manifest(manifest, today=date(2026, 9, 3))

    def test_record_count_must_match_shard(self):
        with self.copied_bundle() as bundle:
            manifest_path = bundle / "manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["datasets"][0]["record_count"] += 1
            manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "实际为"):
                validate_opportunities.validate_repository(
                    manifest_path=manifest_path,
                    core_path=ROOT / "data" / "contests.json",
                    sources_path=ROOT / "data" / "sources.json",
                    today=date(2026, 9, 3),
                )

    def test_ids_must_be_unique_across_core_and_shards(self):
        core_record = build_readme.load_contests()[0]
        with self.copied_bundle() as bundle:
            global_path = bundle / "global.json"
            records = json.loads(global_path.read_text(encoding="utf-8"))
            records[0]["id"] = core_record["id"]
            global_path.write_text(json.dumps(records, ensure_ascii=False), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "重复 id"):
                validate_opportunities.validate_repository(
                    manifest_path=bundle / "manifest.json",
                    core_path=ROOT / "data" / "contests.json",
                    sources_path=ROOT / "data" / "sources.json",
                    today=date(2026, 9, 3),
                )

    def copied_bundle(self):
        temporary = tempfile.TemporaryDirectory()
        bundle = Path(temporary.name)
        for source in (ROOT / "data" / "opportunities").glob("*.json"):
            shutil.copy2(source, bundle / source.name)

        class BundleContext:
            def __enter__(self):
                return bundle

            def __exit__(self, exc_type, exc, traceback):
                temporary.cleanup()

        return BundleContext()


if __name__ == "__main__":
    unittest.main()
