import importlib.util
import json
import sys
import unittest
from copy import deepcopy
from datetime import date
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "send_wecom.py"
sys.path.insert(0, str(SCRIPT.parent))
SPEC = importlib.util.spec_from_file_location("send_wecom", SCRIPT)
send_wecom = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(send_wecom)


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


class SendWecomTests(unittest.TestCase):
    def setUp(self):
        self.contests = send_wecom.load_contests()
        self.today = date(2026, 8, 26)

    def test_digest_contains_requested_contest_fields(self):
        messages = send_wecom.build_digest_messages(self.contests, self.today)
        digest = "\n".join(messages)
        first = self.contests[0]

        self.assertIn(first["title"], digest)
        self.assertIn(first["official_url"], digest)
        self.assertIn(first["deadline"], digest)
        self.assertIn(first["region"], digest)
        self.assertIn(first["eligibility"], digest)
        self.assertIn(first["prize"], digest)
        self.assertIn(first["organizer"], digest)

    def test_digest_includes_upcoming_and_omits_expired_contests(self):
        contests = deepcopy(self.contests[:2])
        expired = contests[0]
        expired["deadline"] = "2026-08-25"
        upcoming = contests[1]
        upcoming["start_date"] = "2026-08-28"
        upcoming["deadline"] = "2026-09-30"

        digest = "\n".join(send_wecom.build_digest_messages(contests, self.today))

        self.assertNotIn(expired["title"], digest)
        self.assertIn(upcoming["title"], digest)
        self.assertIn("2 天后开放", digest)

    def test_messages_are_split_without_exceeding_byte_limit(self):
        max_bytes = 2_000
        messages = send_wecom.build_digest_messages(
            self.contests,
            self.today,
            max_message_bytes=max_bytes,
        )

        self.assertGreater(len(messages), 1)
        self.assertTrue(
            all(send_wecom.encoded_size(message) <= max_bytes for message in messages)
        )
        for contest in self.contests:
            self.assertEqual(sum(contest["title"] in message for message in messages), 1)

    def test_digest_is_sorted_by_deadline(self):
        contests = deepcopy(self.contests[:2])
        contests[0]["deadline"] = "2026-09-30"
        contests[1]["deadline"] = "2026-08-30"

        digest = "\n".join(send_wecom.build_digest_messages(contests, self.today))

        self.assertLess(digest.index(contests[1]["title"]), digest.index(contests[0]["title"]))

    def test_no_active_contests_returns_an_empty_digest(self):
        messages = send_wecom.build_digest_messages(self.contests, date(2027, 1, 1))
        self.assertEqual(len(messages), 1)
        self.assertIn("暂无尚未截止", messages[0])

    def test_rejects_non_wecom_webhook(self):
        with self.assertRaisesRegex(ValueError, "不是有效"):
            send_wecom.validate_webhook_url("https://example.com/cgi-bin/webhook/send?key=test")

    def test_rejects_unexpected_webhook_query_parameters(self):
        with self.assertRaisesRegex(ValueError, "不是有效"):
            send_wecom.validate_webhook_url(
                "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=test&redirect=unexpected"
            )

    def test_send_markdown_posts_expected_payload(self):
        captured = {}

        def opener(request, timeout):
            captured["request"] = request
            captured["timeout"] = timeout
            return FakeResponse({"errcode": 0, "errmsg": "ok"})

        result = send_wecom.send_markdown(
            "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=test-key",
            "测试内容",
            opener=opener,
        )

        body = json.loads(captured["request"].data.decode("utf-8"))
        self.assertEqual(result["errcode"], 0)
        self.assertEqual(captured["timeout"], 15)
        self.assertEqual(body, {"msgtype": "markdown", "markdown": {"content": "测试内容"}})

    def test_send_markdown_raises_on_api_error(self):
        def opener(_request, timeout):
            self.assertEqual(timeout, 15)
            return FakeResponse({"errcode": 93000, "errmsg": "invalid webhook url"})

        with self.assertRaisesRegex(RuntimeError, "errcode=93000"):
            send_wecom.send_markdown(
                "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=test-key",
                "测试内容",
                opener=opener,
            )


if __name__ == "__main__":
    unittest.main()
