# Device configuration authoring

The twelve root JSON files remain the published compatibility surface. They do not contain runtime inheritance. Shared authoring data lives under `config/source/` and is expanded before publication.

## Source layout

- `source/manifest.json` maps every device alias to its existing published filename, family, and device override file.
- `source/bases/common.json` contains fields shared by every manifest.
- `source/bases/xiaomi.json`, `fengmi.json`, and `generic.json` contain family-level values.
- `source/devices/*.json` contains only values that differ from the selected family base.
- `legacy-exceptions.json` records exact, reviewed violations retained solely for compatibility with the current published manifests.

Override precedence is deterministic: parent bases are applied in listed order, later bases replace earlier top-level fields, and device `values` are applied last. Arrays are replaced as complete values. Generation never merges, sorts, or deduplicates package lists implicitly.

## Published aliases and families

| Alias | Family | Published file |
|---|---|---|
| `batman` | Xiaomi | `batman.v2.json` |
| `conan` | Xiaomi | `conan.v2.json` |
| `doraemon` | Xiaomi | `doraemon.json` |
| `franky` | Xiaomi | `franky.json` |
| `generic` | Generic | `generic.v2.json` |
| `goblin` | Fengmi | `goblin.v2.json` |
| `jerry` | Fengmi | `jerry.v2.json` |
| `matrix` | Xiaomi | `matrix.v2.json` |
| `nemo` | Fengmi | `nemo.v2.json` |
| `rainman` | Xiaomi | `rainman.v2.json` |
| `xmen` | Xiaomi | `xmen.v2.json` |
| `zodiac` | Xiaomi | `zodiac.v2.json` |

## Local workflow

Run the read-only checks before changing a published manifest:

```text
python -m unittest discover -s tests -v
python tools/validate_configs.py
python tools/generate_configs.py --check
```

Edit the authoring source, then use `python tools/generate_configs.py --write` only when intentionally updating published root files. Review the resulting diff before committing. Network health and download availability are deliberately outside these offline checks.

The 212 legacy exceptions retain existing HTTP download URLs and duplicate uninstall-package occurrences. Each identifies the exact file, array position or field, value, and count of one, plus a rationale, owner, and review condition. They are local compatibility decisions awaiting upstream review. New or changed HTTP URLs, extra duplicates, widened exemptions, and stale exceptions fail validation. URL credentials and malformed URLs always fail; exceptions cannot permit them. Download contents and HTTP transport remain unverified.

## Compatibility and validation boundaries

This slice supports the observed version 2 output format. The explicit schema covers output fields and nested records; the standard-library evaluator implements only the keywords used by that schema and never resolves network references. Strict parsing also rejects duplicate object keys and nonstandard JSON constants. Source layers are validated even if a later layer would replace an invalid value. Every source-layer URL must be safe; any HTTP value must already occur in the recorded baseline exceptions. Shared bases can contain an original value that a device overrides. Final generated outputs still require their exact file/entry/value/count exemption; a known URL does not grant an exemption at a new output location.

Legacy fixtures reproduce the original checkout bytes, including formatting and line endings. `tests/fixtures/baseline-hashes.json` anchors their contents to upstream commit `c4c66c9c85e9d001c7bac04aeb2746a5af1b0194`, normalizing only CRLF to LF for Git checkout comparison. Fixture and fingerprint changes require explicit review together. Identical generated data reuses the fixture bytes; intentional data changes use two-space indentation and LF. Freshness checks compare bytes, including formatting. Repeated baseline writes are byte-identical.

Generation resolves and confines source, fixture, and output paths to the checkout, rejects cycles and invalid references, and validates all outputs before writing any of them. Each changed file is replaced atomically; replacement across all twelve files is not a transaction. Review every output diff after a write.

No third-party Python dependencies are needed. Local tests ran on Python 3.14.6; the proposed CI pins Python 3.12.12 and action commit hashes, disables checkout credential persistence, and requests read-only repository permissions. Hosted CI has not run. Link-health checks, artifact authenticity/hash verification, runtime compatibility, and a separately reviewed uninstall-list deduplication change remain outside this baseline slice.

## Offline shared catalogue audit (F03 foundation)

`catalogue-inventory.json` groups the exact configured download URLs and keeps every device pin and source position. Run `python tools/audit_catalogue.py --check` for its read-only audit, or `--write` to intentionally regenerate only that inventory after a reviewed configuration change. The audit is a CI check separate from network health. Source layers and installation arrays still use the original values; this inventory does not add a new runtime or authoring reference format.

All artifacts remain `unverified`. URL-derived IDs hash location text, not artifact bytes. Explicit package identifiers are copied only where the configuration declares them; all other identities, versions, signatures, publisher identities, digests, architectures, Android constraints and supported-device eligibility stay unknown. A device reference records an existing pin, not compatibility. HTTPS transport alone does not verify an APK.

The audit rejects drift from configured locations/declared identities and fabricated verification claims. It cannot inspect an APK or prove package identity/signature/authenticity. Trusted artifact inspection, bounded redirect/download checks, catalogue-driven authoring and downloader enforcement remain separate work; actual downloader enforcement needs authorized launcher source. No bytes are downloaded or executed, and no device pin is replaced.
