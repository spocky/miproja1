# F01/F02 implementation plan — generated configs and validation

Date: 2026-10-02
Checkout: local patch checkout of spocky/miproja1
Branch: codex/projectivy-config-f01-f02

## Scope

Implement F01 and F02 without changing the published root JSON semantics or silently updating device pins.

## Tasks

1. Capture all 12 current root JSON files as immutable legacy fixtures and document aliases/device families.
2. Add authoring sources with shared bases plus per-device overrides. Generation is authoring-time only; published root filenames remain unchanged.
3. Add a deterministic standard-library generator that reproduces all current root outputs byte-for-byte, with stable key/list ordering and explicit override precedence. Preserve checkout line endings; anchor fixtures to the upstream commit using normalized Git-content fingerprints.
4. Add strict offline validation for duplicate object keys, schema/types, package identifiers, cross-references, output-field allowlist, override cycles, and generated-file freshness.
5. Add exact-occurrence legacy HTTP/duplicate exceptions with file/entry/value/count, rationale, owner, and review condition; new, widened, and stale exceptions fail. Credentials and malformed URLs cannot be exempted.
6. Add malformed fixtures and automated tests that prove each failure mode and a CI workflow that runs offline validation/tests read-only.
7. Keep network health checks separate and deferred from this baseline slice; they must not gate offline schema correctness. Package authenticity/provenance verification belongs to F03.
8. Verify generation twice, compare root outputs to the baseline, run the full local test/validation suite, and record evidence in the feature register.

## Non-goals

- No Projectivy APK/version mass update.
- No HTTP-to-HTTPS rewrites in this slice.
- No semantic deduplication of uninstall arrays in the baseline-generation commit.
- No release, push, or device action.

## Review and acceptance gates

The independent initial review conditionally approved this plan and rejected the first tooling draft. Required corrections: path containment including directory links; validation before writes; exact-byte freshness and reruns; strict version/types/dates/package identifiers; validation of overridden source values; exact-count baseline exemptions; URL validation without credential disclosure; strict JSON constants; read-only CI permissions and pinned runtime/actions. These corrections are implemented and covered by regression tests. Final independent review is required before accepting the slice.

Acceptance evidence must include the complete local test result, generator freshness, offline validator result, all twelve fixture fingerprints independently compared with `git show` at the recorded baseline, and zero changes to published root JSON. F01 shared authoring and F02 offline validation can be locally verified while semantic deduplication, F03 catalogue verification, network checks, hosted CI, and hardware behavior remain separately tracked.

F04 maintenance documents are a parallel draft slice under `docs/maintenance/`; issue forms remain inactive. Marquee/Gateway implementation is excluded following the user's scope concern. Projectivy-core work stays blocked on authorized launcher source.
