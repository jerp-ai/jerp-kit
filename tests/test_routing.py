import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_trace import check


class RoutingTests(unittest.TestCase):
    def test_missing_trace_is_not_a_pass(self):
        self.assertTrue(check({}))
        self.assertTrue(check({"events": []}))

    def test_behavioral_traces(self):
        fixtures = json.loads((ROOT / "evals/cases.json").read_text())
        for case in fixtures["cases"]:
            with self.subTest(case=case["name"]):
                self.assertEqual(not check(case["trace"]), case["valid"])


if __name__ == "__main__":
    unittest.main()
