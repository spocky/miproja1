"""Offline evaluator for the explicit subset used by the v2 output schema.

No remote references or network resolution. Not a general JSON Schema engine.
"""
from datetime import datetime
from pathlib import Path
import re

try:
    from .configlib import load_json_strict
except ImportError:
    from configlib import load_json_strict

SCHEMA_PATH = Path(__file__).resolve().parents[1] / 'config/schema/output-v2.json'


def validate_shape(document, partial=False):
    schema = load_json_strict(SCHEMA_PATH)
    errors = []

    def visit(value, rule, path, optional=False):
        kind = rule.get('type')
        valid = {'object': isinstance(value, dict), 'array': isinstance(value, list),
                 'string': isinstance(value, str),
                 'integer': isinstance(value, int) and not isinstance(value, bool)}
        if kind and not valid.get(kind, False):
            errors.append(f'{path} must be an {kind}' if kind in {'integer', 'object', 'array'} else f'{path} must be a {kind}')
            return
        if 'const' in rule and value != rule['const']:
            errors.append(f'{path} must equal supported value {rule["const"]}')
        if isinstance(value, dict):
            properties = rule.get('properties', {})
            if not optional:
                for key in rule.get('required', []):
                    if key not in value:
                        errors.append(f'{path}.{key} is required')
            for key, child in value.items():
                if key in properties:
                    visit(child, properties[key], f'{path}.{key}')
                elif rule.get('additionalProperties') is False:
                    errors.append(f'{path}: unknown output field {key}')
        if isinstance(value, list) and 'items' in rule:
            for index, child in enumerate(value):
                visit(child, rule['items'], f'{path}[{index}]')
        if isinstance(value, str):
            if len(value) < rule.get('minLength', 0):
                errors.append(f'{path} must be a non-empty string')
            if 'pattern' in rule and re.fullmatch(rule['pattern'], value) is None:
                errors.append(f'{path} invalid package identifier')
            if rule.get('format') == 'date-time':
                try:
                    if 'T' not in value or datetime.fromisoformat(value.replace('Z', '+00:00')).tzinfo is None:
                        raise ValueError()
                except ValueError:
                    errors.append(f'{path} must be an ISO timestamp with timezone')

    visit(document, schema, 'output', optional=partial)
    return errors
