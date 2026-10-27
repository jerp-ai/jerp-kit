import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_kit import public_content_errors


class PublicContentTests(unittest.TestCase):
    def test_private_artifact_is_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "evals").mkdir()
            (root / "evals" / "private-review.md").write_text("Do not publish internal notes")
            self.assertTrue(public_content_errors(root))

    def test_credential_is_blocked_without_echoing_it(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sample = "ghp_" + "a" * 36
            (root / "example.txt").write_text(sample)
            errors = public_content_errors(root)
            self.assertTrue(errors)
            self.assertNotIn(sample, " ".join(errors))

    def test_placeholder_configuration_is_allowed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "config.json").write_text('{"url":"https://getjerp.com/mcp"}')
            self.assertEqual(public_content_errors(root), [])


if __name__ == "__main__":
    unittest.main()
