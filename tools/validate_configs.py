from __future__ import annotations

import argparse
import hashlib
import ipaddress
import re
from pathlib import Path
from urllib.parse import parse_qsl, urlparse

try:
    from .configlib import ConfigError, SourceRepository, contained_path, load_json_strict
    from .schema import validate_shape
except ImportError:
    from configlib import ConfigError, SourceRepository, contained_path, load_json_strict
    from schema import validate_shape


def valid_url(value):
    if not isinstance(value, str) or any(c.isspace() or ord(c) < 32 or ord(c) == 127 or c == '\\' for c in value):
        return False
    try:
        parsed = urlparse(value)
        if parsed.scheme not in {'http', 'https'} or not parsed.hostname or parsed.username is not None:
            return False
        if parsed.fragment or '%' in parsed.netloc or parsed.port == 0:
            return False
        host = parsed.hostname
        try:
            ipaddress.ip_address(host)
        except ValueError:
            host = host.encode('idna').decode('ascii')
            if not all(re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?', part)
                       for part in host.rstrip('.').split('.')):
                return False
        for name, _ in parse_qsl(parsed.query, keep_blank_values=True):
            key = re.sub('[^a-z]', '', name.lower())
            if any(word in key for word in ('token', 'password', 'secret', 'auth', 'signature', 'apikey', 'accesskey', 'jwt', 'credential')):
                return False
        return True
    except (ValueError, UnicodeError):
        return False


def download_urls(document):
    urls = [(key, document.get(key)) for key in ('toolsUrl', 'customRecoveryZipUrl', 'magiskUrl')]
    for index, item in enumerate(document.get('installPackages', [])):
        if isinstance(item, dict):
            urls.append((f'installPackages[{index}].url', item.get('url')))
    return [(entry, value) for entry, value in urls if value is not None]


def policy_violations(document):
    """Exact occurrence identity; diagnostics never echo download URLs."""
    violations = []
    seen = set()
    for index, package in enumerate(document.get('uninstallPackages', [])):
        if isinstance(package, str):
            if package in seen:
                violations.append(('duplicate_uninstall_package', f'uninstallPackages[{index}]',
                                   package, 'duplicate uninstall package'))
            seen.add(package)
    for entry, value in download_urls(document):
        if isinstance(value, str) and value.lower().startswith('http://'):
            violations.append(('legacy_http', entry, value, 'new HTTP download is not permitted'))
    return violations


def load_legacy_exceptions(root):
    root = Path(root)
    baseline_record = load_json_strict(contained_path(root, 'tests/fixtures/baseline-hashes.json'))
    if not isinstance(baseline_record, dict) or set(baseline_record) != {'commit', 'normalization', 'sha256'}:
        raise ConfigError('invalid baseline metadata')
    if baseline_record.get('commit') != 'c4c66c9c85e9d001c7bac04aeb2746a5af1b0194':
        raise ConfigError('baseline commit mismatch')
    hashes = baseline_record.get('sha256')
    if not isinstance(hashes, dict) or len(hashes) != 12:
        raise ConfigError('baseline must record twelve hashes')
    for name, digest in hashes.items():
        if not re.fullmatch(r'[a-z][a-z0-9-]*(?:\.v2)?\.json', name) or not isinstance(digest, str) or not re.fullmatch(r'[0-9a-f]{64}', digest):
            raise ConfigError('invalid baseline filename or fingerprint')
        path = contained_path(root, 'tests/fixtures/legacy/' + name)
        try:
            content = path.read_bytes()
        except OSError as exc:
            raise ConfigError(f'{name}: baseline fixture unavailable') from exc
        if hashlib.sha256(content.replace(b'\r\n', b'\n')).hexdigest() != digest:
            raise ConfigError(f'{name}: immutable baseline fingerprint mismatch')
    data = load_json_strict(contained_path(root, 'config/legacy-exceptions.json'))
    if not isinstance(data, dict) or set(data) != {'exceptions'} or not isinstance(data['exceptions'], list):
        raise ConfigError('legacy exceptions must contain only an exceptions list')
    required = {'rule', 'file', 'entry', 'value', 'count', 'rationale', 'owner', 'review_condition'}
    seen = set()
    for index, item in enumerate(data['exceptions']):
        if not isinstance(item, dict) or set(item) != required:
            raise ConfigError(f'legacy exception {index}: invalid fields')
        if any(not isinstance(item[key], str) or not item[key].strip() for key in required - {'count'}):
            raise ConfigError(f'legacy exception {index}: fields must be non-empty strings')
        if type(item['count']) is not int or item['count'] != 1:
            raise ConfigError(f'legacy exception {index}: count must be exactly one occurrence')
        key = (item['rule'], item['file'], item['entry'], item['value'])
        if key in seen:
            raise ConfigError(f'legacy exception {index}: duplicate exception')
        seen.add(key)
        baseline = contained_path(root, 'tests/fixtures/legacy/' + item['file'])
        violations = policy_violations(load_json_strict(baseline))
        if not any((rule, entry, value) == (item['rule'], item['entry'], item['value'])
                   for rule, entry, value, _ in violations):
            raise ConfigError(f'legacy exception {index}: not applicable to immutable baseline')
    return data['exceptions']


def validate_output_document(document, filename, exceptions):
    issues = [f'{filename}: {issue}' for issue in validate_shape(document)]
    if not isinstance(document, dict) or issues:
        return issues
    for entry, value in download_urls(document):
        if value is not None and not (entry == 'customRecoveryZipUrl' and value == '') and not valid_url(value):
            issues.append(f'{filename}: {entry} must be a safe http(s) URL without credentials')
    observed = {(rule, entry, value): message for rule, entry, value, message in policy_violations(document)}
    allowed = {(item['rule'], item['entry'], item['value']) for item in exceptions if item['file'] == filename}
    for (rule, entry, value), message in observed.items():
        if (rule, entry, value) not in allowed:
            issues.append(f'{filename}: {entry} {message}')
    for rule, entry, value in allowed - observed.keys():
        issues.append(f'{filename}: {entry} stale legacy exception; remove explicitly')
    seen = set()
    for index, prop in enumerate(document['customPropsOverrides']):
        if prop['key'] in seen:
            issues.append(f'{filename}: customPropsOverrides[{index}] duplicate property key')
        seen.add(prop['key'])
    return issues


def validate_project(root, check_published=True):
    try:
        root = Path(root)
        generated = SourceRepository(root).build_all()
        expected_names = {path.name for path in (root / 'tests/fixtures/legacy').glob('*.json')}
        issues = []
        if set(generated) != expected_names:
            issues.append('manifest output filenames differ from the twelve legacy paths')
        exceptions = load_legacy_exceptions(root)
        for filename, document in generated.items():
            issues.extend(validate_output_document(document, filename, exceptions))
        if check_published:
            try:
                from .generate_configs import check_generated
            except ImportError:
                from generate_configs import check_generated
            issues.extend(check_generated(root))
            for filename in generated:
                path = contained_path(root, filename)
                if path.is_file():
                    issues.extend(validate_output_document(load_json_strict(path), filename, exceptions))
            if {p.name for p in root.glob('*.json')} != set(generated):
                issues.append('root JSON filenames differ from source manifest')
        return issues
    except ConfigError as exc:
        return [str(exc)]


def main():
    argparse.ArgumentParser(description='Strict offline configuration validation').parse_args()
    root = Path(__file__).resolve().parents[1]
    issues = validate_project(root)
    if issues:
        print('\n'.join(issues))
        return 1
    exceptions = load_legacy_exceptions(root)
    print(f'configuration validation passed; {len(exceptions)} explicit legacy exceptions retained')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
