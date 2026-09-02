import importlib.util
import json
import unittest
from copy import deepcopy
from datetime import date
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "collect_sources.py"
SPEC = importlib.util.spec_from_file_location("collect_sources", SCRIPT)
collect_sources = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(collect_sources)


def source_fixture(collector=None):
    return {
        "id": "example-source",
        "name": "Example Source",
        "url": "https://example.com/opportunities/",
        "source_kind": "official-platform",
        "trust_tier": "official-page",
        "region_codes": ["GLOBAL"],
        "industries": ["ai-ml"],
        "cadence_hours": 12,
        "enabled": True,
        "collector": collector
        or {
            "type": "html-links",
            "title_keywords": ["challenge"],
            "link_patterns": ["/competitions/"],
            "same_host_only": True,
        },
    }


class SourceRegistryTests(unittest.TestCase):
    def test_repository_registry_is_valid_and_has_first_coverage_batch(self):
        sources = collect_sources.load_sources()
        self.assertGreaterEqual(len(sources), 40)
        self.assertGreaterEqual(sum(source["enabled"] for source in sources), 4)
        self.assertIn("CN", {region for source in sources for region in source["region_codes"]})
        self.assertIn("GLOBAL", {region for source in sources for region in source["region_codes"]})
        self.assertGreaterEqual(len({industry for source in sources for industry in source["industries"]}), 12)

    def test_enabled_manual_source_is_rejected(self):
        source = source_fixture({"type": "manual"})
        with self.assertRaisesRegex(ValueError, "manual 来源不能设置 enabled=true"):
            collect_sources.validate_sources([source])

    def test_private_literal_source_url_is_rejected(self):
        source = source_fixture()
        source["url"] = "https://127.0.0.1/source"
        with self.assertRaisesRegex(ValueError, "私有或保留地址"):
            collect_sources.validate_sources([source])

    def test_due_sources_honors_six_and_twelve_hour_cadence(self):
        six_hour = source_fixture()
        six_hour["id"] = "six-hour"
        six_hour["cadence_hours"] = 6
        twelve_hour = source_fixture()
        twelve_hour["id"] = "twelve-hour"
        twelve_hour["cadence_hours"] = 12
        self.assertEqual(
            [source["id"] for source in collect_sources.due_sources([six_hour, twelve_hour], 7)],
            ["six-hour"],
        )
        self.assertEqual(
            [source["id"] for source in collect_sources.due_sources([six_hour, twelve_hour], 13)],
            ["six-hour", "twelve-hour"],
        )

        twelve_hour["enabled"] = False
        self.assertEqual(
            [source["id"] for source in collect_sources.due_sources([six_hour, twelve_hour], 13)],
            ["six-hour"],
        )


class ExtractorTests(unittest.TestCase):
    def test_html_extractor_resolves_urls_deduplicates_and_filters_results(self):
        source = source_fixture()
        content = """
        <a href="/competitions/open-ai?utm_source=newsletter">Open AI Challenge</a>
        <a href="/competitions/open-ai">Open AI Challenge</a>
        <a href="/competitions/old">Challenge winners announced</a>
        <a href="https://outside.example/competitions/external">External Challenge</a>
        <a href="/about">About us</a>
        """
        candidates = collect_sources.extract_html_candidates(source, content)
        self.assertEqual(candidates, [{
            "title": "Open AI Challenge",
            "url": "https://example.com/competitions/open-ai",
            "match_reason": ["title:challenge", "url:/competitions/"],
        }])

    def test_atom_extractor_supports_href_links(self):
        source = source_fixture({
            "type": "rss-atom",
            "title_keywords": ["competition"],
            "same_host_only": True,
        })
        content = """<?xml version="1.0"?>
        <feed xmlns="http://www.w3.org/2005/Atom">
          <entry>
            <title>Generative Art Competition</title>
            <link href="https://example.com/competitions/art" />
          </entry>
        </feed>"""
        candidates = collect_sources.extract_rss_candidates(source, content)
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0]["url"], "https://example.com/competitions/art")

    def test_atom_extractor_enforces_same_host(self):
        source = source_fixture({
            "type": "rss-atom",
            "title_keywords": ["competition"],
            "same_host_only": True,
        })
        content = """<?xml version="1.0"?>
        <rss><channel><item><title>External Competition</title>
        <link>https://outside.example/competitions/art</link></item></channel></rss>"""
        self.assertEqual(collect_sources.extract_rss_candidates(source, content), [])

    def test_json_extractor_uses_configured_paths(self):
        source = source_fixture({
            "type": "json-api",
            "items_path": "result.items",
            "title_path": "name",
            "url_path": "links.official",
            "title_keywords": ["大赛"],
        })
        content = json.dumps({
            "result": {
                "items": [
                    {"name": "人工智能创作大赛", "links": {"official": "/competitions/aigc"}},
                    {"name": "普通会议", "links": {"official": "/events/meeting"}},
                ]
            }
        })
        candidates = collect_sources.extract_json_candidates(source, content)
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0]["url"], "https://example.com/competitions/aigc")

    def test_json_extractor_enforces_same_host(self):
        source = source_fixture({
            "type": "json-api",
            "items_path": "items",
            "title_path": "name",
            "url_path": "url",
            "title_keywords": ["competition"],
            "same_host_only": True,
        })
        content = json.dumps({"items": [{
            "name": "External Competition",
            "url": "https://outside.example/competitions/art",
        }]})
        self.assertEqual(collect_sources.extract_json_candidates(source, content), [])

    def test_canonical_url_removes_tracking_and_fragment(self):
        actual = collect_sources.canonical_url(
            "https://EXAMPLE.com:443/a//b?utm_campaign=x&id=7&spm=abc#details"
        )
        self.assertEqual(actual, "https://example.com/a/b?id=7")

    def test_all_match_mode_requires_title_and_url_matches(self):
        source = source_fixture({
            "type": "html-links",
            "title_keywords": ["challenge"],
            "link_patterns": ["/competitions/"],
            "match_mode": "all",
            "same_host_only": True,
        })
        content = """
        <a href="/news/challenge">Current Challenge</a>
        <a href="/competitions/regular-event">Regular event</a>
        <a href="/competitions/current">Current Challenge</a>
        """
        candidates = collect_sources.extract_html_candidates(source, content)
        self.assertEqual([item["url"] for item in candidates], ["https://example.com/competitions/current"])

    def test_source_title_cleanup_uses_card_status_marker(self):
        source = source_fixture({
            "type": "html-links",
            "title_keywords": ["大赛"],
            "title_split_patterns": [" 进行中"],
            "same_host_only": True,
        })
        content = '<a href="/event/7">AI 创作大赛 进行中 很长的卡片描述和报名信息</a>'
        candidates = collect_sources.extract_html_candidates(source, content)
        self.assertEqual(candidates[0]["title"], "AI 创作大赛")

    def test_anchor_prefers_nested_heading_over_card_description(self):
        parser = collect_sources.AnchorExtractor()
        parser.feed(
            '<a href="/challenge"><h3>Open AI Challenge</h3>'
            '<p>A much longer description about the opportunity.</p></a>'
        )
        self.assertEqual(parser.links, [("Open AI Challenge", "/challenge")])

    def test_reject_past_years_understands_abbreviated_years(self):
        source = source_fixture({
            "type": "html-links",
            "title_keywords": ["challenge"],
            "reject_past_years": True,
            "same_host_only": True,
        })
        self.assertEqual(
            collect_sources.match_reasons(source, "KDD Cup '23 Challenge", "https://example.com/challenge"),
            [],
        )


class CandidateTests(unittest.TestCase):
    def test_merge_filters_published_and_preserves_review_state(self):
        source = source_fixture()
        existing_url = "https://example.com/competitions/existing"
        existing_id = collect_sources.candidate_id(source["id"], existing_url)
        existing = [{
            "id": existing_id,
            "source_id": source["id"],
            "title": "Existing Challenge",
            "discovered_url": existing_url,
            "source_tier": "official-page",
            "first_seen": "2026-08-01",
            "last_seen": "2026-08-01",
            "status": "reviewing",
            "match_reason": ["title:challenge"],
            "review_notes": "Checking the rules",
        }]
        discoveries = [
            (source, {
                "title": "Existing Challenge Updated",
                "url": existing_url,
                "match_reason": ["title:challenge"],
            }),
            (source, {
                "title": "Already Published Competition",
                "url": "https://example.com/competitions/published",
                "match_reason": ["title:competition"],
            }),
        ]
        contests = [{
            "title": "Already Published Competition",
            "official_url": "https://example.com/competitions/published",
            "rules_url": "https://example.com/competitions/published/rules",
            "en": {"title": "Already Published Competition"},
        }]
        merged = collect_sources.merge_candidates(existing, discoveries, contests, date(2026, 9, 2))
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["status"], "reviewing")
        self.assertEqual(merged[0]["review_notes"], "Checking the rules")
        self.assertEqual(merged[0]["last_seen"], "2026-09-02")
        self.assertEqual(merged[0]["title"], "Existing Challenge Updated")

    def test_candidate_requires_registered_source(self):
        candidate = {
            "id": "missing-source-deadbeef",
            "source_id": "missing-source",
            "title": "Open Challenge",
            "discovered_url": "https://example.com/challenge",
            "source_tier": "official-page",
            "first_seen": "2026-09-01",
            "last_seen": "2026-09-02",
            "status": "new",
            "match_reason": ["title:challenge"],
        }
        with self.assertRaisesRegex(ValueError, "未注册来源"):
            collect_sources.validate_candidates([candidate], {"example-source"})


if __name__ == "__main__":
    unittest.main()
