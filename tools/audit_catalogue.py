"""Offline inventory of configured downloads; no artifact authenticity claim."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path

try:
    from .configlib import ConfigError, SourceRepository, contained_path, load_json_strict, ordered_equal
    from .validate_configs import download_urls, validate_project
except ImportError:
    from configlib import ConfigError, SourceRepository, contained_path, load_json_strict, ordered_equal
    from validate_configs import download_urls, validate_project

INVENTORY_PATH = 'config/catalogue-inventory.json'


def build_inventory(root: Path):
    issues = validate_project(root)
    if issues:
        raise ConfigError('; '.join(issues))
    repo = SourceRepository(root)
    outputs = repo.build_all()
    artifacts = {}
    for device in repo.manifest()['devices']:
        doc = outputs[device['output']]
        for entry, url in download_urls(doc):
            if not url:  # An empty recovery field is not an artifact.
                continue
            # This ID fingerprints a location string, never downloaded bytes.
            identifier = 'url-' + hashlib.sha256(url.encode('utf-8')).hexdigest()
            if identifier not in artifacts:
                artifacts[identifier] = {
                    'id': identifier,
                    'download_location': url,
                    'destination_kind': 'configured_download_url',
                    'transport_state': ('legacy_http_unverified' if url.lower().startswith('http://')
                                        else 'https_artifact_unverified'),
                    'verification_state': 'unverified',
                    'artifact_sha256': None,
                    'publisher_identity': None,
                    'signing_certificate_sha256': None,
                    'version': None,
                    'version_code': None,
                    'architectures': None,
                    'android_constraints': None,
                    'verified_device_eligibility': None,
                    'configuration_references': [],
                }
            item = None
            if entry.startswith('installPackages['):
                index = int(entry.split('[', 1)[1].split(']', 1)[0])
                item = doc['installPackages'][index]
            artifacts[identifier]['configuration_references'].append({
                'alias': device['alias'],
                'family': device['family'],
                'output': device['output'],
                'entry': entry,
                'display_name': item['name'] if item is not None else None,
                'expected_package': item.get('package') if item is not None else None,
                'identity_evidence': 'declared_in_configuration' if item is not None and 'package' in item else 'unknown',
                'compatibility_evidence': 'configuration_pin_only_runtime_unverified',
            })
    return {
        'inventory_version': 1,
        'source_configuration_baseline': 'c4c66c9c85e9d001c7bac04aeb2746a5af1b0194',
        'scope': 'Offline configured-download inventory; no network or APK inspection',
        'id_meaning': 'SHA256 of the exact URL text, not artifact bytes or publisher identity',
        'artifacts': [artifacts[key] for key in sorted(artifacts)],
    }


def render_inventory(inventory):
    return (json.dumps(inventory, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode('utf-8')


def validate_inventory(root: Path, inventory):
    # No promotion to verified is supported without a separate trusted inspector.
    if not ordered_equal(inventory, build_inventory(root)):
        return ['catalogue inventory differs from configured pins or claims unsupported verification; regenerate and review']
    return []


def write_inventory(root: Path):
    content = render_inventory(build_inventory(root))
    path = contained_path(Path(root), INVENTORY_PATH)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
            temporary = stream.name
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary and os.path.exists(temporary):
            os.unlink(temporary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true', help='read-only inventory audit')
    mode.add_argument('--write', action='store_true', help='replace only the catalogue inventory')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    try:
        if args.write:
            write_inventory(root)
            print('unverified catalogue inventory written; device outputs preserved')
            return 0
        path = contained_path(root, INVENTORY_PATH)
        inventory = load_json_strict(path)
        issues = validate_inventory(root, inventory)
        if not issues and path.read_bytes().replace(b'\r\n', b'\n') != render_inventory(inventory):
            issues.append('catalogue inventory formatting is stale')
        if issues:
            print('\n'.join(issues))
            return 1
        items = inventory['artifacts']
        references = sum(len(item['configuration_references']) for item in items)
        http = sum(item['transport_state'] == 'legacy_http_unverified' for item in items)
        print(f'catalogue audit passed: {len(items)} unverified locations, {references} configuration references, {http} HTTP locations')
        return 0
    except (ConfigError, OSError) as exc:
        print(exc)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
