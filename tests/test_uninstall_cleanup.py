import unittest
from pathlib import Path

from tools.configlib import SourceRepository, load_json_strict, ordered_equal
from tools.validate_configs import load_legacy_exceptions

ROOT = Path(__file__).resolve().parents[1]


class UninstallCleanupTests(unittest.TestCase):
    def test_cleanup_removes_only_duplicate_uninstall_occurrences_in_original_order(self):
        removed = 0
        changed = []
        for name, generated in SourceRepository(ROOT).build_all().items():
            baseline = load_json_strict(ROOT / 'tests/fixtures/legacy' / name)
            expected = dict(baseline)
            expected['uninstallPackages'] = list(dict.fromkeys(baseline['uninstallPackages']))
            self.assertTrue(ordered_equal(generated, expected), name)
            count = len(baseline['uninstallPackages']) - len(generated['uninstallPackages'])
            if count:
                changed.append(name)
            removed += count
        self.assertEqual(removed, 27)
        self.assertEqual(len(changed), 9)
        exceptions = load_legacy_exceptions(ROOT)
        self.assertEqual(len(exceptions), 185)
        self.assertTrue(all(item['rule'] == 'legacy_http' for item in exceptions))
