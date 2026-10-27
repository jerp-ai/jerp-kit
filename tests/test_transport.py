import io
import json
import sys
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills/jerp/scripts"))
import jerp_call


class FakeResponse(io.StringIO):
    pass


class TransportTests(unittest.TestCase):
    def test_fixed_destination_and_no_redirect(self):
        with patch("urllib.request.build_opener") as factory:
            factory.return_value.open.return_value = FakeResponse(json.dumps({"contract": "jerp.verdict.v2", "tool": "speaker"}))
            result = jerp_call.call("speaker", {"need": "card", "about": "getjerp.com"}, "test-key")
            request = factory.return_value.open.call_args[0][0]
            self.assertEqual(request.full_url, "https://getjerp.com/api/v1/speaker")
            self.assertEqual(request.get_header("Authorization"), "Bearer test-key")
            self.assertEqual(json.loads(request.data)["need"], "card")
            redirect_handler = factory.call_args[0][0]
            self.assertIsNone(redirect_handler.redirect_request(request, None, 302, "redirect", {}, "https://elsewhere.invalid"))
            self.assertEqual(result["contract"], "jerp.verdict.v2")

    def test_wrong_tool_response_is_not_accepted(self):
        with patch("urllib.request.build_opener") as factory:
            factory.return_value.open.return_value = FakeResponse(json.dumps({"contract": "jerp.verdict.v2", "tool": "guard"}))
            with self.assertRaises(ValueError):
                jerp_call.call("speaker", {}, "test-key")

    def test_invalid_inputs_never_reach_network(self):
        with patch("urllib.request.build_opener") as factory:
            for tool, payload, key in [("fetch", {}, "test"), ("speaker", [], "test"), ("speaker", {}, "")]:
                with self.assertRaises(ValueError):
                    jerp_call.call(tool, payload, key)
            factory.assert_not_called()

    def test_http_failure_does_not_retry_or_echo_submitted_content(self):
        with patch("sys.argv", ["jerp_call.py", "support", "--input", "-"]), patch("sys.stdin", io.StringIO('{}')), patch("jerp_call.call", side_effect=HTTPError("url", 429, "private submitted text", {}, None)) as call:
            output = io.StringIO()
            with redirect_stderr(output):
                self.assertEqual(jerp_call.main(), 1)
            call.assert_called_once()
            self.assertIn("429", output.getvalue())
            self.assertNotIn("private submitted text", output.getvalue())

    def test_application_error_is_not_success(self):
        with patch("sys.argv", ["jerp_call.py", "speaker", "--input", "-"]), patch("sys.stdin", io.StringIO('{}')), patch("jerp_call.call", return_value={"contract": "jerp.verdict.v2", "error": {"code": "invalid_input"}}), patch("builtins.print"):
            self.assertEqual(jerp_call.main(), 1)


if __name__ == "__main__":
    unittest.main()
