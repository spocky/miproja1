# Contributing to the configuration checkout

This repository contains special-device configurations and serves as an issue/request tracker; see the [existing README](README.md). It does not provide authorized Projectivy launcher core implementation source. The [F01-F25 roadmap](docs/maintenance/roadmap.md) identifies real owners and source/contract blockers.

The F04 author's write scope is `docs/maintenance/**` and this file. The wider currently authorized local configuration implementation includes F01/F02 and F03 catalogue/audit work; the F04 authoring boundary does not restrict that work. Already authorized configuration edits and local commits do not require duplicate authorization. Marquee and Gateway edits remain excluded following the user's concern. The assistant committed to defer F25 pending user scope clarification after repeated concern; this is not attributed to an explicit user deferral instruction. The externally owned server remains unchanged.

## Before changing anything

Read repository/user instructions and existing plans. Inspect the active branch, base and dirty state, and preserve all current edits and untracked files. Define the smallest reviewed slice with its owner and acceptance evidence. Do not infer the launcher's Kotlin/UI source from a configuration fork or modify a wallpaper contract to impersonate a native widget API.

For reports, prepare an observation or desired outcome using the [maintenance drafts](docs/maintenance/README.md) and [safe reporting guidance](docs/maintenance/support.md). Search both open and closed issues before suggesting a new one. Do not post issues or PRs as a side effect of editing documents.

## Existing configuration workflow

Python is used by the current standard-library tooling and tests. No new package dependency is introduced by these docs. From the repository root, the existing commands are:

```text
python -m unittest discover -s tests -v
python tools/validate_configs.py
python tools/generate_configs.py --check
```

The unit tests exercise configuration logic and use temporary fixtures; they do not install APKs or verify a TV. Validation and `--check` inspect local configuration and output freshness without generating root files or proving download authenticity. Run them for the authorized configuration implementation and record actual exit codes and results. Document-only review must not claim these tests ran merely because their commands are listed.

See [config/README.md](config/README.md) for the authoring layout. Shared bases, device overrides and alias/output mappings live under `config/source/`; generation expands them before publication. Runtime inheritance is not introduced. Later parent bases override earlier top-level fields, device values apply last, and arrays are replaced as complete values. Preserve all twelve existing root output filenames and ordered semantics; identical aliases remain individually documented.

For a configuration change within the already authorized implementation scope, edit authoring sources and then intentionally regenerate:

```text
python tools/generate_configs.py --write
```

`--write` changes root JSON outputs and is outside the F04 author's documentation slice; it remains available to the authorized configuration implementer. Review the source and resulting output diff, rerun the three checks above, and retain a rollback to the prior reviewed source/output pair. Do not manually edit root outputs as a substitute for updating their authoring source.

Legacy exceptions live in `config/legacy-exceptions.json`. Review exact rule/file/entry, rationale, owner and removal condition. Do not broaden an exception to hide a new violation. Semantic uninstall-list cleanup must be a separate reviewed change from baseline generation. Retain device-specific pins; never silently update downloads, uninstall lists, properties, recovery packages, stock-launcher behavior or root instructions.

## Safety, licensing and verification

Keep offline syntax/schema/freshness checks separate from bounded network/artifact checks. Do not mechanically rewrite HTTP URLs to HTTPS, execute downloaded bytes, fabricate artifact metadata or treat a digest as proof of publisher identity. Preserve existing signing identity, licences and notices; do not assign a new licence to unverified third-party material.

Maintain the lightweight, ad-free default and optional/reversible enhancements. Do not change app-private preferences, scrape through accessibility, disable stock packages, install privileged helpers, enable network ADB, root/flash a device, patch an APK or silently build a replacement launcher. No code, TV or server action is part of the F04 author's documentation work; local configuration code implementation remains authorized in the wider programme.

Record observed base/branch/commit, changed paths, commands actually run with exit codes, behavior/exclusions, redacted evidence, privacy review, rollback and blockers. Distinguish document parsing, local logic checks, contract tests, builds, emulator behavior and actual device acceptance. The [compatibility matrix](docs/maintenance/compatibility.md) remains runtime unverified until real evidence is recorded. Missing hardware/source must not become a passed checkbox.

## Administration and publishing

The forms in `docs/maintenance` are inactive drafts; existing `.github/ISSUE_TEMPLATE` Markdown files remain unchanged. Label creation/application, template activation, issue posting or closing, enabling Discussions, pushing, opening a PR, releasing and deployment require separate authorization. Preserve current repository licensing; this document adds no licence and grants no new reuse rights.
