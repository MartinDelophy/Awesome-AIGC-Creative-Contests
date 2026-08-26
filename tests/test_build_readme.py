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
        self.assertEqual(build_readme.status_label(deadline, deadline), "🔥 今天截止")

    def test_future_contest_uses_upcoming_label(self):
        contests = build_readme.load_contests()
        upcoming = [item for item in contests if item["id"] == "next-art-ai-2026"]
        table = build_readme.render_table(upcoming, date(2026, 8, 26), upcoming=True)
        self.assertIn("🔵 2026-09-01 开放", table)

    def test_render_omits_expired_contests(self):
        contests = build_readme.load_contests()
        output = build_readme.render_readme(contests, date(2026, 11, 1))
        self.assertNotIn("Seedance 2.5 白模参考创作大赛", output)

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

    def test_rss_is_valid_xml_and_contains_active_contests(self):
        contests = build_readme.load_contests()
        rss = build_readme.render_rss(contests, date(2026, 8, 26))
        root = ET.fromstring(rss)
        self.assertEqual(root.tag, "rss")
        self.assertEqual(len(root.findall("./channel/item")), 11)

    def test_ics_contains_one_event_per_active_contest(self):
        contests = build_readme.load_contests()
        calendar = build_readme.render_ics(contests, date(2026, 8, 26))
        self.assertEqual(calendar.count("BEGIN:VEVENT"), 11)
        self.assertIn("X-WR-CALNAME:AIGC 创作赛事截止提醒", calendar)
        self.assertTrue(calendar.endswith("END:VCALENDAR\r\n"))


if __name__ == "__main__":
    unittest.main()
