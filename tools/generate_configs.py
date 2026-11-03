from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path

try:
    from .configlib import ConfigError, SourceRepository, contained_path, load_json_strict, ordered_equal
except ImportError:
    from configlib import ConfigError, SourceRepository, contained_path, load_json_strict, ordered_equal


def render_output(root, filename, document):
    baseline = contained_path(Path(root), 'tests/fixtures/legacy/' + filename)
    if baseline.is_file() and ordered_equal(document, load_json_strict(baseline)):
        return baseline.read_bytes()
    return (json.dumps(document, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode('utf-8')


def check_generated(root: Path) -> list[str]:
    issues: list[str] = []
    generated = SourceRepository(root).build_all()
    for filename, document in generated.items():
        path = contained_path(Path(root), filename)
        if not path.is_file():
            issues.append(f"{filename}: generated output is missing")
            continue
        load_json_strict(path)
        if path.read_bytes() != render_output(root, filename, document):
            issues.append(f"{filename}: generated output is stale")
    return issues


def write_generated(root: Path) -> None:
    try:
        from .validate_configs import validate_project
    except ImportError:
        from validate_configs import validate_project
    issues = validate_project(root, check_published=False)
    if issues:
        raise ConfigError('; '.join(issues))
    rendered = {contained_path(root, name): render_output(root, name, document)
                for name, document in SourceRepository(root).build_all().items()}
    for path, content in rendered.items():
        if path.is_file() and path.read_bytes() == content:
            continue
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Projectivy device configuration outputs")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="read-only freshness check")
    mode.add_argument("--write", action="store_true", help="write generated root JSON files")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    try:
        if args.check:
            issues = check_generated(root)
            if issues:
                print("\n".join(issues))
                return 1
            print("all generated configurations are fresh")
            return 0
        write_generated(root)
        print("generated configurations written")
        return 0
    except ConfigError as exc:
        print(exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
