import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tools.configlib import ConfigError, SourceRepository, load_json_strict, ordered_equal
from tools.validate_configs import load_legacy_exceptions, validate_output_document, validate_project


ROOT = Path(__file__).resolve().parents[1]
LEGACY = ROOT / "tests" / "fixtures" / "legacy"
MALFORMED = ROOT / "tests" / "fixtures" / "malformed"


class ConfigGenerationTests(unittest.TestCase):
    def test_generated_configs_match_legacy_except_reviewed_uninstall_cleanup(self):
        generated = SourceRepository(ROOT).build_all()
        expected_names = sorted(path.name for path in LEGACY.glob("*.json"))
        self.assertEqual(sorted(generated), expected_names)
        for name in expected_names:
            expected = load_json_strict(LEGACY / name)
            expected['uninstallPackages'] = list(dict.fromkeys(expected['uninstallPackages']))
            self.assertTrue(ordered_equal(generated[name], expected), name)

    def test_aliases_resolve_to_published_outputs(self):
        repo = SourceRepository(ROOT)
        aliases = repo.alias_map()
        self.assertEqual(aliases, {
            'batman': 'batman.v2.json', 'conan': 'conan.v2.json',
            'doraemon': 'doraemon.json', 'franky': 'franky.json',
            'generic': 'generic.v2.json', 'goblin': 'goblin.v2.json',
            'jerry': 'jerry.v2.json', 'matrix': 'matrix.v2.json',
            'nemo': 'nemo.v2.json', 'rainman': 'rainman.v2.json',
            'xmen': 'xmen.v2.json', 'zodiac': 'zodiac.v2.json',
        })
        for alias, output in aliases.items():
            self.assertIn(output, repo.build_all())
            self.assertEqual(repo.resolve_alias(alias), output)

    def test_later_base_then_device_override_wins(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "config" / "source"
            (source / "bases").mkdir(parents=True)
            (source / "devices").mkdir()
            (source / "manifest.json").write_text(json.dumps({
                "devices": [{"alias": "demo", "family": "demo", "output": "demo.json", "source": "devices/demo.json"}]
            }), encoding="utf-8")
            (source / "bases" / "a.json").write_text(json.dumps({"values": {"author": "a", "version": 2}}), encoding="utf-8")
            (source / "bases" / "b.json").write_text(json.dumps({"extends": ["a"], "values": {"author": "b"}}), encoding="utf-8")
            (source / "devices" / "demo.json").write_text(json.dumps({"extends": ["b"], "values": {"author": "device"}}), encoding="utf-8")
            built = SourceRepository(root).build_output("demo.json")
            self.assertEqual(built["author"], "device")
            self.assertEqual(built["version"], 2)

            # A second independent base must replace a whole list, not append it.
            (source / 'bases' / 'c.json').write_text(json.dumps({
                'values': {'author': 'c', 'uninstallPackages': ['example.second']}
            }), encoding='utf-8')
            (source / 'bases' / 'a.json').write_text(json.dumps({
                'values': {'version': 2, 'author': 'a', 'uninstallPackages': ['example.first']}
            }), encoding='utf-8')
            (source / 'devices' / 'demo.json').write_text(json.dumps({
                'extends': ['a', 'c'], 'values': {'product': 'device'}
            }), encoding='utf-8')
            built = SourceRepository(root).build_output('demo.json')
            self.assertEqual(built['author'], 'c')
            self.assertEqual(built['uninstallPackages'], ['example.second'])
            self.assertEqual(built['product'], 'device')

    def test_override_cycle_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "config" / "source"
            (source / "bases").mkdir(parents=True)
            (source / "devices").mkdir()
            (source / "manifest.json").write_text(json.dumps({
                "devices": [{"alias": "demo", "family": "demo", "output": "demo.json", "source": "devices/demo.json"}]
            }), encoding="utf-8")
            (source / "bases" / "a.json").write_text(json.dumps({"extends": ["b"], "values": {}}), encoding="utf-8")
            (source / "bases" / "b.json").write_text(json.dumps({"extends": ["a"], "values": {}}), encoding="utf-8")
            (source / "devices" / "demo.json").write_text(json.dumps({"extends": ["a"], "values": {}}), encoding="utf-8")
            with self.assertRaisesRegex(ConfigError, "cycle"):
                SourceRepository(root).build_output("demo.json")


class StrictValidationTests(unittest.TestCase):
    def test_duplicate_object_key_fixture_fails_strict_parse(self):
        with self.assertRaisesRegex(ConfigError, "duplicate object key"):
            load_json_strict(MALFORMED / "duplicate-key.json")

    def test_malformed_output_fixtures_fail_for_specific_reason(self):
        cases = {
            "bad-type.json": "version must be an integer",
            "bad-package.json": "invalid package identifier",
            "bad-launcher.json": "launcher invalid package identifier",
            "unknown-field.json": "unknown output field",
        }
        for filename, expected in cases.items():
            with self.subTest(filename=filename):
                document = load_json_strict(MALFORMED / filename)
                issues = validate_output_document(document, filename, [])
                self.assertTrue(any(expected in issue for issue in issues), issues)

    def test_legacy_exceptions_are_visible_and_current_project_validates(self):
        exceptions = load_legacy_exceptions(ROOT)
        self.assertGreater(len(exceptions), 0)
        for entry in exceptions:
            self.assertTrue(entry["file"])
            self.assertTrue(entry["entry"])
            self.assertTrue(entry["rationale"])
            self.assertTrue(entry["owner"])
            self.assertTrue(entry["review_condition"])
        self.assertEqual(validate_project(ROOT), [])

    def test_new_duplicate_uninstall_entry_is_rejected(self):
        document = load_json_strict(LEGACY / "goblin.v2.json")
        document = copy.deepcopy(document)
        document["uninstallPackages"].append(document["uninstallPackages"][0])
        issues = validate_output_document(document, "new.json", [])
        self.assertTrue(any("duplicate uninstall package" in issue for issue in issues), issues)

    def test_missing_source_cross_reference_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "config" / "source"
            source.mkdir(parents=True)
            (source / "manifest.json").write_text(json.dumps({
                "devices": [{"alias": "demo", "family": "demo", "output": "demo.json", "source": "devices/missing.json"}]
            }), encoding="utf-8")
            issues = validate_project(root, check_published=False)
            self.assertTrue(any("missing source" in issue for issue in issues), issues)

    def test_generated_file_freshness_detects_drift(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "repo"
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            published = root / "goblin.v2.json"
            data = json.loads(published.read_text(encoding="utf-8"))
            data["author"] = "drift"
            published.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
            issues = validate_project(root)
            self.assertTrue(any("goblin.v2.json: generated output is stale" in issue for issue in issues), issues)


if __name__ == "__main__":
    unittest.main()
