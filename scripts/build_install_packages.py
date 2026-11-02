#!/usr/bin/env python3
"""Merge installPackages/*.json into generic.v3.json, preserving other settings."""
import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ('wallpaper-plugin.json', 'icon-pack.json', 'file-manager.json', 'misc.json')


def load(path):
    with path.open(encoding='utf-8') as stream:
        return json.load(stream)


def build():
    apps, packages, names = [], set(), set()
    for filename in SOURCES:
        path = ROOT / 'installPackages' / filename
        data = load(path)
        if not isinstance(data, dict) or 'category' not in data or not isinstance(data.get('apps'), list):
            raise ValueError(f'{path}: expected category and apps array')
        category = data['category']
        if category is not None and (not isinstance(category, str) or not category.strip()):
            raise ValueError(f'{path}: category must be a non-empty string or null')
        for i, app in enumerate(data['apps'], 1):
            where = f'{filename} app #{i}'
            if not isinstance(app, dict) or not isinstance(app.get('name'), str) or not app['name'].strip():
                raise ValueError(f'{where}: missing name')
            if 'category' in app:
                raise ValueError(f'{where}: category belongs at file level')
            if not any(app.get(field) for field in ('url', 'package', 'downloader')):
                raise ValueError(f'{where}: missing installation method')
            for field in ('url', 'image'):
                if field in app and (not isinstance(app[field], str) or urlparse(app[field]).scheme != 'https' or not urlparse(app[field]).netloc):
                    raise ValueError(f'{where}: {field} must be an HTTPS URL')
            for field in ('official', 'googleplay'):
                if field in app and not isinstance(app[field], bool):
                    raise ValueError(f'{where}: {field} must be a boolean')
            package = app.get('package')
            if package:
                if package in packages:
                    raise ValueError(f'{where}: duplicate package {package}')
                packages.add(package)
            if app['name'] in names:
                print(f'WARNING: duplicate name {app["name"]}', file=sys.stderr)
            names.add(app['name'])
            merged = {'name': app['name']}
            if category is not None:
                merged['category'] = category
            merged.update({k: v for k, v in app.items() if k != 'name'})
            apps.append(merged)
    target = ROOT / 'generic.v3.json'
    config = load(target)
    config['installPackages'] = apps
    return target, json.dumps(config, ensure_ascii=False, indent=2) + '\n'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', help='Validate only; do not write')
    args = parser.parse_args()
    try:
        target, content = build()
        if not args.check:
            if not target.exists() or target.read_text(encoding='utf-8') != content:
                target.write_text(content, encoding='utf-8')
                print('Updated generic.v3.json')
            else:
                print('No changes')
        else:
            print('Validation OK')
    except (ValueError, OSError, json.JSONDecodeError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
