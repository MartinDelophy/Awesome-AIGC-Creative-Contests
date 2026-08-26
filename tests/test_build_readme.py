import importlib.util
import unittest
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


if __name__ == "__main__":
    unittest.main()

