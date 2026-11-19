import copy
import unittest
from pathlib import Path

from tools.audit_catalogue import build_inventory, validate_inventory
from tools.configlib import SourceRepository
from tools.validate_configs import download_urls

ROOT = Path(__file__).resolve().parents[1]


class CatalogueAuditTests(unittest.TestCase):
    def test_inventory_is_deterministic_and_retains_every_pin(self):
        inventory = build_inventory(ROOT)
        self.assertEqual(inventory, build_inventory(ROOT))
        expected = {
            (name, entry, url)
            for name, doc in SourceRepository(ROOT).build_all().items()
            for entry, url in download_urls(doc) if url
        }
        actual = {
            (ref['output'], ref['entry'], item['download_location'])
            for item in inventory['artifacts'] for ref in item['configuration_references']
        }
        self.assertEqual(expected, actual)
        self.assertEqual(len(inventory['artifacts']), len({url for _, _, url in expected}))

    def test_unknown_metadata_is_never_inferred_from_filename(self):
        inventory = build_inventory(ROOT)
        for item in inventory['artifacts']:
            self.assertEqual(item['verification_state'], 'unverified')
            for key in ('artifact_sha256', 'publisher_identity', 'signing_certificate_sha256',
                        'version', 'version_code', 'architectures', 'android_constraints',
                        'verified_device_eligibility'):
                self.assertIsNone(item[key], key)
        declared = [(ref['output'], ref['expected_package'])
                    for item in inventory['artifacts'] for ref in item['configuration_references']
                    if ref['expected_package'] is not None]
        self.assertEqual(len(declared), 2)
        self.assertTrue(all(output == 'generic.v2.json' for output, _ in declared))

    def test_http_risk_remains_visible(self):
        inventory = build_inventory(ROOT)
        for item in inventory['artifacts']:
            self.assertEqual(item['transport_state'],
                             'legacy_http_unverified' if item['download_location'].lower().startswith('http://')
                             else 'https_artifact_unverified')

    def test_missing_fabricated_verification_and_identity_mismatch_are_rejected(self):
        expected = build_inventory(ROOT)
        for mode in ('verified', 'identity', 'pin', 'missing'):
            with self.subTest(mode=mode):
                changed = copy.deepcopy(expected)
                first = changed['artifacts'][0]
                if mode == 'verified':
                    first['verification_state'] = 'verified'
                elif mode == 'identity':
                    first['configuration_references'][0]['expected_package'] = 'example.fabricated'
                elif mode == 'pin':
                    first['download_location'] = 'https://example.invalid/new.apk'
                else:
                    del first['artifact_sha256']
                self.assertTrue(validate_inventory(ROOT, changed))
        self.assertEqual(validate_inventory(ROOT, expected), [])
