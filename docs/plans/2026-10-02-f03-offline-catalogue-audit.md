# F03 offline catalogue audit slice

Date: 2026-10-02. Owning checkout: work/miproja1, branch codex/projectivy-config-f01-f02; baseline c4c66c9c85e9d001c7bac04aeb2746a5af1b0194.

User intent: implement the supplied upgrade directive in reviewed slices, preserve existing download pins and outputs, and keep Marquee/Gateway excluded after the user's scope concern. F03 asks for a shared catalogue and honest package/artifact verification; this slice delivers only a deterministic inventory and offline audit. Actual download identity, signatures, runtime enforcement and device compatibility remain unverified or source blocked.

Build a shared catalogue from the twelve generated configurations, grouping identical download URLs into stable SHA256-derived IDs. The ID hashes the location string, not artifact bytes. Keep every exact device field/array occurrence, display name and explicitly declared package identity. Do not infer package/version/architecture/signing/digest from filenames. Record unknown metadata as null, all verification states as unverified, HTTP transport as a risk, and observed device pins as configuration references rather than supported-device eligibility.

Files: tools/audit_catalogue.py; config/catalogue-inventory.json; tests/test_catalogue_audit.py; docs/plans/2026-10-02-f03-offline-catalogue-audit.md; config/README.md; read-only workflow audit step. No source-layer/package reference redesign in this slice; installation arrays remain unchanged. This is an inventory foundation, not full F01 catalogue authoring or F03 authenticity verification.

1. Freeze and accept F01/F02 baseline independently before integrating this slice.
2. Add failing tests for deterministic IDs/reruns, every observed reference/URL/pin retained, explicit identity only, HTTP risk reporting, and rejection of stale/tampered inventory or a fabricated verified state.
3. Implement stdlib read-only check and deliberate catalogue-only write mode; validate existing configurations before inventory generation. No network calls or downloaded-byte execution. Contain inventory path to checkout.
4. Generate initial inventory and run tests/validator/generation freshness/audit. Published root files must still match baseline bytes.
5. Obtain independent final review, correct in-scope findings, and record actual acceptance and remaining verification blockers in the feature register. Do not claim mismatched APK identity rejection without APK inspection, identity/signing authority or device verification.

Uninstall deduplication stays a separate semantic slice. Public forms/admin/push/PR/release/device actions remain outside authorization.
