from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


class ConfigError(ValueError):
    pass


def _strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ConfigError(f"duplicate object key: {key}")
        result[key] = value
    return result


def load_json_strict(path: Path) -> Any:
    def reject_constant(value):
        raise ConfigError('nonstandard JSON constant')
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_strict_object,
                          parse_constant=reject_constant)
    except (ConfigError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ConfigError(f"{path}: {exc}") from exc


def contained_path(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or '\\' in relative or ':' in relative:
        raise ConfigError('invalid relative path')
    parts = relative.split('/')
    if any(part in {'', '.', '..'} for part in parts):
        raise ConfigError('path escape rejected')
    candidate = (root / relative).resolve()
    if not candidate.is_relative_to(root.resolve()):
        raise ConfigError('resolved path escape rejected')
    return candidate


def ordered_equal(left: Any, right: Any) -> bool:
    if isinstance(left, dict) and isinstance(right, dict):
        if list(left) != list(right):
            return False
        return all(ordered_equal(left[key], right[key]) for key in left)
    if isinstance(left, list) and isinstance(right, list):
        return len(left) == len(right) and all(
            ordered_equal(a, b) for a, b in zip(left, right)
        )
    return type(left) is type(right) and left == right


def _merge(target: dict[str, Any], values: dict[str, Any]) -> dict[str, Any]:
    merged = dict(target)
    for key, value in values.items():
        merged[key] = value
    return merged


class SourceRepository:
    def __init__(self, root: Path):
        self.root = Path(root)
        self.source_root = contained_path(self.root, 'config/source')
        self.manifest_path = contained_path(self.root, 'config/source/manifest.json')
        self._manifest: dict[str, Any] | None = None
        self._legacy_http_values: set[str] | None = None

    def manifest(self) -> dict[str, Any]:
        if self._manifest is None:
            data = load_json_strict(self.manifest_path)
            if not isinstance(data, dict):
                raise ConfigError("manifest must be an object")
            if set(data) != {'devices'}:
                raise ConfigError('manifest must contain only devices')
            self._manifest = data
        return self._manifest

    def _devices(self) -> list[dict[str, Any]]:
        devices = self.manifest().get("devices")
        if not isinstance(devices, list):
            raise ConfigError("manifest devices must be a list")
        if not all(isinstance(item, dict) for item in devices):
            raise ConfigError("manifest device entries must be objects")
        aliases = set()
        outputs = set()
        for device in devices:
            if set(device) != {'alias', 'output', 'source', 'family'}:
                raise ConfigError('device must contain alias, output, source and family')
            for field in ('alias', 'family'):
                value = device[field]
                if not isinstance(value, str) or not re.fullmatch(r'[a-z][a-z0-9-]*', value):
                    raise ConfigError(f'device {field} must be a simple name')
            output = device['output']
            if not isinstance(output, str) or not re.fullmatch(r'[a-z][a-z0-9-]*(?:\.v2)?\.json', output):
                raise ConfigError('output must be a root JSON filename')
            contained_path(self.root, output)
            source = device['source']
            path = contained_path(self.source_root, source)
            if not isinstance(source, str) or not source.startswith('devices/') or path.suffix != '.json':
                raise ConfigError('source must be a device JSON path')
            if device['alias'] in aliases or output in outputs:
                raise ConfigError('duplicate alias or output')
            aliases.add(device['alias'])
            outputs.add(output)
        return devices

    def alias_map(self) -> dict[str, str]:
        aliases: dict[str, str] = {}
        for device in self._devices():
            alias = device.get("alias")
            output = device.get("output")
            if not isinstance(alias, str) or not alias:
                raise ConfigError("device alias must be a non-empty string")
            if not isinstance(output, str) or not output:
                raise ConfigError(f"{alias}: output must be a non-empty string")
            if alias in aliases:
                raise ConfigError(f"duplicate alias: {alias}")
            aliases[alias] = output
        return aliases

    def resolve_alias(self, alias: str) -> str:
        try:
            return self.alias_map()[alias]
        except KeyError as exc:
            raise ConfigError(f"unknown alias: {alias}") from exc

    def _device_for_output(self, output: str) -> dict[str, Any]:
        matches = [device for device in self._devices() if device.get("output") == output]
        if len(matches) != 1:
            raise ConfigError(f"output {output!r} must have exactly one device source")
        return matches[0]

    def _load_layer(self, path: Path) -> dict[str, Any]:
        data = load_json_strict(path)
        if not isinstance(data, dict):
            raise ConfigError(f"{path}: layer must be an object")
        extends = data.get("extends", [])
        values = data.get("values", {})
        if not isinstance(extends, list) or not all(isinstance(x, str) for x in extends):
            raise ConfigError(f"{path}: extends must be a list of base names")
        if not isinstance(values, dict):
            raise ConfigError(f"{path}: values must be an object")
        try:
            from .schema import validate_shape
        except ImportError:
            from schema import validate_shape
        issues = validate_shape(values, partial=True)
        if issues:
            raise ConfigError(f'{path}: ' + '; '.join(issues))
        try:
            from .validate_configs import download_urls, load_legacy_exceptions, valid_url
        except ImportError:
            from validate_configs import download_urls, load_legacy_exceptions, valid_url
        for entry, value in download_urls(values):
            if entry == 'customRecoveryZipUrl' and value == '':
                continue
            if not valid_url(value):
                raise ConfigError(f'{path}: {entry} must be a safe http(s) URL without credentials')
            if value.lower().startswith('http://'):
                if self._legacy_http_values is None:
                    self._legacy_http_values = {
                        item['value'] for item in load_legacy_exceptions(self.root)
                        if item['rule'] == 'legacy_http'
                    }
                if value not in self._legacy_http_values:
                    raise ConfigError(f'{path}: {entry} new HTTP download is not permitted in source layers')
        extra = set(data) - {"extends", "values"}
        if extra:
            raise ConfigError(f"{path}: unknown layer fields: {', '.join(sorted(extra))}")
        return data

    def _build_base(self, name: str, stack: tuple[str, ...]) -> dict[str, Any]:
        if not re.fullmatch(r'[a-z][a-z0-9-]*', name):
            raise ConfigError('invalid base name')
        if len(stack) >= 32:
            raise ConfigError('base inheritance exceeds 32 layers')
        if name in stack:
            chain = " -> ".join((*stack, name))
            raise ConfigError(f"override cycle: {chain}")
        path = contained_path(self.source_root, f'bases/{name}.json')
        if not path.is_file():
            raise ConfigError(f"missing base: {name}")
        layer = self._load_layer(path)
        result: dict[str, Any] = {}
        next_stack = (*stack, name)
        for parent in layer.get("extends", []):
            result = _merge(result, self._build_base(parent, next_stack))
        return _merge(result, layer.get("values", {}))

    def build_output(self, output: str) -> dict[str, Any]:
        device = self._device_for_output(output)
        source = device.get("source")
        if not isinstance(source, str) or not source:
            raise ConfigError(f"{output}: source must be a non-empty string")
        path = contained_path(self.source_root, source)
        if not path.is_file():
            raise ConfigError(f"{output}: missing source {source}")
        layer = self._load_layer(path)
        result: dict[str, Any] = {}
        for base in layer.get("extends", []):
            result = _merge(result, self._build_base(base, ()))
        return _merge(result, layer.get("values", {}))

    def build_all(self) -> dict[str, dict[str, Any]]:
        result: dict[str, dict[str, Any]] = {}
        for device in self._devices():
            output = device.get("output")
            if not isinstance(output, str):
                raise ConfigError("device output must be a string")
            if output in result:
                raise ConfigError(f"duplicate output: {output}")
            result[output] = self.build_output(output)
        return result
