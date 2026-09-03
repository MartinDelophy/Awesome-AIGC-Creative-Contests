import importlib.util
import json
import unittest
import xml.etree.ElementTree as ET
from copy import deepcopy
from datetime import date
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build_readme.py"
SPEC = importlib.util.spec_from_file_location("build_readme", SCRIPT)
build_readme = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(build_readme)


class BuildReadmeTests(unittest.TestCase):
    def test_repository_data_is_valid(self):
        contests = build_readme.load_contests()
        self.assertGreater(len(contests), 0)

    def test_deadline_is_inclusive(self):
        deadline = date(2026, 8, 31)
        self.assertEqual(build_readme.status_label(deadline, deadline), "🔥 Due today")
        self.assertEqual(build_readme.status_label(deadline, deadline, "zh"), "🔥 今天截止")

    def test_future_contest_uses_upcoming_label(self):
        contests = build_readme.load_contests()
        upcoming = [item for item in contests if item["id"] == "next-art-ai-2026"]
        table = build_readme.render_table(upcoming, date(2026, 8, 26), upcoming=True)
        self.assertIn("🔵 Opens 2026-09-01", table)

    def test_render_omits_expired_contests(self):
        contests = build_readme.load_contests()
        output = build_readme.render_readme(contests, date(2026, 11, 1))
        self.assertNotIn("Dreamina Seedance 2.5", output)

    def test_both_readmes_render_full_contest_tables(self):
        contests = build_readme.load_contests()
        english = build_readme.render_readme(contests, date(2026, 8, 26), "en")
        chinese = build_readme.render_readme(contests, date(2026, 8, 26), "zh")
        self.assertIn("Austin AI Film Festival 2026", english)
        self.assertIn("美国 / 全球开放", chinese)
        self.assertNotIn("{{SOURCE_COUNT}}", english)
        self.assertIn("registered sources", english)
        self.assertIn("个来源", chinese)

    def test_rejects_unknown_fields(self):
        contests = deepcopy(build_readme.load_contests())
        contests[0]["unexpected"] = "value"
        with self.assertRaisesRegex(ValueError, "未知字段"):
            build_readme.validate_contests(contests)

    def test_rejects_duplicate_categories(self):
        contests = deepcopy(build_readme.load_contests())
        contests[0]["categories"] = ["video", "video"]
        with self.assertRaisesRegex(ValueError, "categories 不能重复"):
            build_readme.validate_contests(contests)

    def test_schema_required_fields_match_validator(self):
        schema_path = SCRIPT.parents[1] / "data" / "schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        self.assertEqual(set(schema["items"]["required"]), build_readme.REQUIRED_FIELDS)
        self.assertEqual(set(schema["items"]["properties"]), build_readme.REQUIRED_FIELDS)

    def test_core_rejects_extension_metadata(self):
        contests = deepcopy(build_readme.load_contests())
        contests[0]["scope"] = "aigc-native"
        with self.assertRaisesRegex(ValueError, "未知字段.*scope"):
            build_readme.validate_contests(contests)

    def test_rss_is_valid_xml_and_contains_active_contests(self):
        contests = build_readme.load_contests()
        today = date(2026, 8, 26)
        rss = build_readme.render_rss(contests, today)
        root = ET.fromstring(rss)
        self.assertEqual(root.tag, "rss")
        self.assertEqual(len(root.findall("./channel/item")), len(build_readme.visible_contests(contests, today)))

    def test_ics_contains_one_event_per_active_contest(self):
        contests = build_readme.load_contests()
        today = date(2026, 8, 26)
        calendar = build_readme.render_ics(contests, today)
        self.assertEqual(calendar.count("BEGIN:VEVENT"), len(build_readme.visible_contests(contests, today)))
        self.assertIn("X-WR-CALNAME:AIGC Creative Contest Deadlines", calendar)
        self.assertTrue(calendar.endswith("END:VCALENDAR\r\n"))


if __name__ == "__main__":
    unittest.main()
