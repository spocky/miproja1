# F04 validation record

Date: 2026-10-02. This record covers the F04 author's local maintenance-document work only in this `miproja1` checkout. The wider currently authorized configuration implementation includes F01/F02 and F03 catalogue/audit; the author-specific checks below neither restrict that work nor summarize its verification. Observed base: `c4c66c9c85e9d001c7bac04aeb2746a5af1b0194`; branch: `codex/projectivy-config-f01-f02`. The F04 author created no commit, release, issue or PR; authorized local implementation/integration commits do not require duplicate authorization. The original README and active Markdown templates were read along with the full upgrade handoff, root configs and existing authoring/test/tooling files.

## Authored paths

- `CONTRIBUTING.md`
- `docs/maintenance/README.md`
- `docs/maintenance/bug-report.yml`
- `docs/maintenance/feature-request.yml`
- `docs/maintenance/compatibility.md`
- `docs/maintenance/support.md`
- `docs/maintenance/labels.md`
- `docs/maintenance/roadmap.md`
- `docs/maintenance/validation.md`

These are new local files. Only these paths were written by the F04 author. The forms remain outside `.github/ISSUE_TEMPLATE`; proposed labels are not activated. Marquee/Gateway/server and launcher code were not changed by the F04 author. This author spawned no agents and claims author checks only. Independent review of the wider programme is in progress; this record does not claim that the programme had no agents or independent review.

## Checks performed

| Check | Actual invocation / method | Result and limit |
|---|---|---|
| Draft form parsing and structure | Inline standard-library Python checks via `python -B -`; strict JSON parsing rejects duplicate keys | Exit 0 on final run. Both JSON-syntax YAML drafts parse; top-level keys, allowed element types, unique field IDs, required bug fields, outcome/alternatives fields, optional evidence and privacy acknowledgements checked. No automatic labels/assignees. GitHub rendering/submission not tested. |
| Compatibility inventory | Inline Python reads all root JSONs and `config/source/manifest.json`, compares every matrix row | Exit 0 on final run. All 12 aliases, families, output names, stock-launcher fields and URL release text match the local files; every row states runtime unverified. No model/firmware or artifact compatibility inferred. |
| Roadmap coverage | Inline Python checks F01-F25 table rows, nonempty owner/evidence/blocker fields and F25 constraint text; author reviews ownership against handoff | Exit 0 on final run. Exactly 25 distinct ordered IDs; Marquee/Gateway excluded, F25 deferred under the assistant's commitment following repeated user concern, pending scope clarification, launcher core unavailable. Documentation does not complete source-gated features. |
| Local document links and whitespace | Inline Python resolves relative Markdown file links and checks final newline/trailing whitespace; `git diff --check` | Exit 0 on final run. The initial link check found the not-yet-written validation file; the record was added and checks rerun. `git diff --check` alone does not inspect untracked drafts, so the inline file checks cover them. |
| Existing offline configuration validation | `python -B tools/validate_configs.py` | Exit 0: `configuration validation passed; 212 explicit legacy exceptions retained`. This is a read-only local config check, not trusted-download, launcher-build or device evidence. |
| Existing generation freshness | `python -B tools/generate_configs.py --check` | Exit 0: `all generated configurations are fresh`. No `--write` command was run by the F04 author. |
| Preservation and edit boundary | Before/after byte digests computed locally, plus Git status/diff inspection and review of authored paths | Original README, both active issue templates and all 12 root JSON files match the captured baseline. Authored F04 paths are confined to the allowed scope. Digests are used for preservation only, not APK authenticity, and no artifact hash is asserted. |
| Existing issue references | Read-only public API request for the latest 100 repository issue entries, open/closed, excluding PRs | Linked issue numbers/titles were observed; mappings remain title-level leads. No comprehensive issue-body/duplicate/root-cause audit, issue creation, comments, closure or label application. |

The form checks are based on [GitHub's form schema](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-githubs-form-schema); JSON syntax is a [YAML 1.2 subset](https://yaml.org/spec/1.2.2/). No dependency was installed and no tracked verification script was added. Python's `-B` option prevents these commands from writing bytecode caches.

## Shared checkout observations

Other local work changed configuration tooling, tests, legacy exceptions, workflow content and cache files during document preparation, and added schema, baseline-hash and ignore files. Those paths were outside the F04 authored scope and were preserved. Consequently this record does not claim the entire shared checkout was unchanged, or attribute those changes or their tests to F04. The command results above describe the tool versions present when the commands ran.

## Unverified and deferred

The unit-test command in `CONTRIBUTING.md` is documented, not executed by the F04 author. This statement does not describe the wider implementation's test activity. The F04 author performed no app/APK build, network artifact verification, package/signature inspection, device/emulator test, controller test, hardware soak, diagnostic exporter, live integration, or runtime compatibility verification. No GitHub form was activated or submitted. All runtime matrix entries remain unverified.

F25 remains deferred under the assistant's commitment following repeated user concern, pending scope clarification; Marquee/Gateway edits remain excluded following the user's concern. Launcher source remains unavailable. Public administration, publishing and deployment require separate authority. Preserve existing licensing/notices; no licence was added.

Rollback for this document slice is to remove only the nine new authored files listed above after checking for subsequent edits. Do not reset the shared checkout, remove pre-existing files, or disturb other work. No rollback or deletion was performed.
