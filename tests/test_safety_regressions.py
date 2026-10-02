import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tools.configlib import ConfigError, SourceRepository, load_json_strict
from tools.generate_configs import write_generated
from tools.validate_configs import load_legacy_exceptions, validate_output_document

ROOT = Path(__file__).resolve().parents[1]


class SafetyRegressionTests(unittest.TestCase):
    def copy_repo(self, directory):
        root = Path(directory) / 'repo'
        shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns('.git', '__pycache__'))
        return root

    def test_generation_preserves_current_output_bytes_on_reruns(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.copy_repo(directory)
            original = {p.name: p.read_bytes() for p in root.glob('*.json')}
            write_generated(root)
            self.assertEqual(original, {p.name: p.read_bytes() for p in root.glob('*.json')})
            write_generated(root)
            self.assertEqual(original, {p.name: p.read_bytes() for p in root.glob('*.json')})

    def test_known_duplicate_exception_cannot_allow_additional_duplicate(self):
        doc = load_json_strict(ROOT / 'batman.v2.json')
        doc['uninstallPackages'].append('com.mi.umi')
        issues = validate_output_document(doc, 'batman.v2.json', load_legacy_exceptions(ROOT))
        self.assertTrue(any('duplicate' in i for i in issues), issues)

    def test_changed_http_url_is_not_covered_by_legacy_exception(self):
        doc = load_json_strict(ROOT / 'batman.v2.json')
        doc['magiskUrl'] = 'http://example.invalid/different.zip'
        issues = validate_output_document(doc, 'batman.v2.json', load_legacy_exceptions(ROOT))
        self.assertTrue(any('HTTP' in i for i in issues), issues)

    def test_http_scheme_casing_cannot_bypass_exception_policy(self):
        for url in ('HTTP://example.invalid/a.apk', 'hTtP://example.invalid/a.apk'):
            with self.subTest(url=url):
                doc = load_json_strict(ROOT / 'generic.v2.json')
                doc['toolsUrl'] = url
                issues = validate_output_document(doc, 'generic.v2.json', load_legacy_exceptions(ROOT))
                self.assertTrue(any('HTTP' in issue for issue in issues), issues)

    def test_credentials_and_invalid_urls_fail_without_crashing(self):
        for url in ('https://user:secret@example.invalid/a.apk', 'https://[broken/a.apk',
                    'https://example.invalid:bad/a.apk', 'https://example.invalid/a.apk?token=secret',
                    'https://example.invalid/a.apk?jwt=secret',
                    'https://example.invalid/a.apk?access_key=secret',
                    'https://example.invalid/a.apk\x7f',
                    'https://example.invalid/a.apk\n'):
            with self.subTest(url=url):
                doc = load_json_strict(ROOT / 'generic.v2.json')
                doc['toolsUrl'] = url
                issues = validate_output_document(doc, 'generic.v2.json', load_legacy_exceptions(ROOT))
                self.assertTrue(any('toolsUrl' in i for i in issues), issues)

    def test_nonstandard_json_constants_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'invalid.json'
            for value in ('NaN', 'Infinity', '-Infinity'):
                path.write_text('{"version":' + value + '}', encoding='utf-8')
                with self.assertRaises(ConfigError):
                    load_json_strict(path)

    def test_generation_rejects_escape_paths_before_any_write(self):
        for field, value in (('output', '../outside.json'), ('output', 'C:/outside.json'),
                             ('source', '../outside.json'), ('source', 'devices/../../outside.json')):
            with self.subTest(field=field, value=value), tempfile.TemporaryDirectory() as directory:
                root = self.copy_repo(directory)
                path = root / 'config/source/manifest.json'
                data = json.loads(path.read_text())
                data['devices'][0][field] = value
                path.write_text(json.dumps(data), encoding='utf-8')
                before = {p.name: p.read_bytes() for p in root.glob('*.json')}
                with self.assertRaises(ConfigError):
                    write_generated(root)
                self.assertEqual(before, {p.name: p.read_bytes() for p in root.glob('*.json')})

    def test_family_change_affects_only_inheriting_devices(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.copy_repo(directory)
            before = SourceRepository(root).build_all()
            path = root / 'config/source/bases/fengmi.json'
            layer = json.loads(path.read_text())
            layer['values']['launcher'] = 'example.newlauncher'
            path.write_text(json.dumps(layer), encoding='utf-8')
            after = SourceRepository(root).build_all()
            self.assertEqual({'goblin.v2.json', 'jerry.v2.json', 'nemo.v2.json'},
                             {name for name in before if before[name] != after[name]})

    def test_invalid_source_cannot_overwrite_published_outputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.copy_repo(directory)
            path = root / 'config/source/bases/common.json'
            layer = json.loads(path.read_text())
            layer['values']['version'] = True
            path.write_text(json.dumps(layer), encoding='utf-8')
            before = {p.name: p.read_bytes() for p in root.glob('*.json')}
            with self.assertRaises(ConfigError):
                write_generated(root)
            self.assertEqual(before, {p.name: p.read_bytes() for p in root.glob('*.json')})

    def test_schema_rejects_wrong_version_date_empty_fields_and_null_package(self):
        for field, value in (('version', 3), ('releaseDate', '2026-02-31T00:00:00Z'),
                             ('product', ''), ('toolsUrl', '')):
            doc = load_json_strict(ROOT / 'generic.v2.json')
            doc[field] = value
            with self.subTest(field=field):
                self.assertTrue(any(field in i for i in validate_output_document(doc, 'demo.json', [])))
        doc = load_json_strict(ROOT / 'generic.v2.json')
        doc['installPackages'][0]['package'] = None
        self.assertTrue(any('package' in i for i in validate_output_document(doc, 'demo.json', [])))

    def test_unknown_manifest_fields_are_rejected_by_generator(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.copy_repo(directory)
            path = root / 'config/source/manifest.json'
            doc = json.loads(path.read_text())
            doc['unrecognized'] = True
            path.write_text(json.dumps(doc), encoding='utf-8')
            with self.assertRaises(ConfigError):
                SourceRepository(root).build_all()

    def test_duplicate_key_diagnostic_identifies_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'ambiguous.json'
            path.write_text('{"a": 1, "a": 2}', encoding='utf-8')
            with self.assertRaisesRegex(ConfigError, 'ambiguous.json.*duplicate object key'):
                load_json_strict(path)

    def test_formatting_only_drift_is_detected(self):
        from tools.generate_configs import check_generated
        with tempfile.TemporaryDirectory() as directory:
            root = self.copy_repo(directory)
            path = root / 'batman.v2.json'
            path.write_text(json.dumps(json.loads(path.read_text()), indent=4), encoding='utf-8')
            self.assertIn('batman.v2.json: generated output is stale', check_generated(root))

    def test_tampered_baseline_cannot_expand_exceptions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.copy_repo(directory)
            path = root / 'tests/fixtures/legacy/batman.v2.json'
            path.write_text(path.read_text() + ' ', encoding='utf-8')
            with self.assertRaisesRegex(ConfigError, 'baseline'):
                load_legacy_exceptions(root)

    def test_source_directory_link_escape_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.copy_repo(directory)
            source = root / 'config/source'
            outside = Path(directory) / 'outside'
            source.rename(outside)
            try:
                source.symlink_to(outside, target_is_directory=True)
            except OSError:
                self.skipTest('Directory symlink creation unavailable on this host')
            with self.assertRaisesRegex(ConfigError, 'escape'):
                SourceRepository(root).build_all()

    def test_invalid_baseline_metadata_and_missing_fixture_fail_cleanly(self):
        for scenario in ('nonobject', 'invalid-name', 'missing'):
            with self.subTest(scenario=scenario), tempfile.TemporaryDirectory() as directory:
                root = self.copy_repo(directory)
                metadata = root / 'tests/fixtures/baseline-hashes.json'
                if scenario == 'nonobject':
                    metadata.write_text('[]', encoding='utf-8')
                elif scenario == 'invalid-name':
                    data = json.loads(metadata.read_text())
                    data['sha256']['batman.v2.json/child'] = data['sha256'].pop('batman.v2.json')
                    metadata.write_text(json.dumps(data), encoding='utf-8')
                else:
                    (root / 'tests/fixtures/legacy/batman.v2.json').unlink()
                with self.assertRaises(ConfigError):
                    load_legacy_exceptions(root)

    def test_invalid_parent_field_is_rejected_even_when_device_replaces_it(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self.copy_repo(directory)
            base = root / 'config/source/bases/common.json'
            data = json.loads(base.read_text())
            data['values']['author'] = 123
            base.write_text(json.dumps(data), encoding='utf-8')
            device = root / 'config/source/devices/batman.json'
            data = json.loads(device.read_text())
            data['values']['author'] = 'replacement'
            device.write_text(json.dumps(data), encoding='utf-8')
            with self.assertRaisesRegex(ConfigError, 'author'):
                SourceRepository(root).build_output('batman.v2.json')

    def test_unsafe_parent_urls_fail_even_when_family_replaces_them(self):
        for url in ('http://example.invalid/new.apk', 'HTTP://example.invalid/new.apk',
                    'https://user:secret@example.invalid/a.apk',
                    'https://example.invalid/a.apk?jwt=secret'):
            with self.subTest(url=url), tempfile.TemporaryDirectory() as directory:
                root = self.copy_repo(directory)
                base = root / 'config/source/bases/common.json'
                data = json.loads(base.read_text())
                data['values']['toolsUrl'] = url
                base.write_text(json.dumps(data), encoding='utf-8')
                with self.assertRaises(ConfigError):
                    SourceRepository(root).build_output('batman.v2.json')
