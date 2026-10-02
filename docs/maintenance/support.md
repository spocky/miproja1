# Support and triage proposal

This is local reporting guidance, not a support service, private reporting channel, or authorization to post. Use the [draft bug form](bug-report.yml) or [feature form](feature-request.yml) to prepare text. The original upstream Markdown templates remain active.

## Safe reports

Record the installed launcher version, device manufacturer/model, public firmware and Android version, existing integration method, starting state, exact reproduction sequence, frequency, and expected/actual behavior. Unknown values are acceptable. A text-only report can be sufficient; screenshots, logs, exports, device serial numbers, unique identifiers and credentials are never required.

Before sharing, manually preview text and attachments. Remove passwords, tokens, authorization headers/cookies, pairing secrets, raw stream URLs and their query strings, personal watch history, account/profile identifiers, private paths, network addresses, serial numbers, Android IDs and MAC addresses. Crop account names, private artwork and identifiers out of screenshots. Share only a small redacted excerpt when it helps; omit evidence if safe redaction is uncertain. Do not automatically upload support archives or raw settings exports.

For suspected security/privacy problems, keep sensitive details local until a maintainer's actual private reporting destination is independently confirmed. No private destination is established by this task. Do not publish live exploit details, credentials or another person's data in a public issue.

Report the current integration setup without changing it. No report requires stock-launcher disabling, root/recovery, private-storage edits, privileged helpers, accessibility scraping, network ADB or modified APKs. These documents do not diagnose OEM failures or recommend a universal HOME intent fix.

## Proposed triage sequence

1. Search existing open and closed issues, and the [roadmap](roadmap.md). Record a related link rather than silently treating similar titles as duplicates. Match launcher version, firmware, integration method and observed sequence before consolidating reports.
2. Assign the observed component and evidence state using the [proposed labels](labels.md). A symptom is `reported` until a reproducible record exists. A configuration file alone does not confirm runtime behavior or root cause.
3. Request only the minimum missing non-sensitive information. Keep environment collection separate from optional evidence; do not require identifying information or full archives.
4. Capture a failing reproduction before proposing a fix. Distinguish configuration validation from launcher implementation, source failure from revoked authorization, and artwork failure from launch-action failure.
5. Route launcher-owned behavior to authorized launcher source or maintainer work. Keep Marquee/Gateway work excluded following the user's concern. F25 remains deferred under the assistant's commitment following repeated user concern, pending scope clarification. The server remains externally owned and unchanged.
6. Record the actual changed files, commands/exit codes and acceptance evidence for the currently authorized F01/F02 configuration implementation and F03 catalogue/audit work. Other implementation follows its applicable scope and source/contract gates. A proposal, closed upstream issue, mocked contract, parser success or local lint result is not a demonstrated device fix.
7. Before marking a report fixed, verify the original reproduction on the relevant version/device and record rollback or disable behavior. Publishing, label application, duplicate closing and issue administration require separate authorization.

## Evidence record

For each later reviewed slice, retain owner, feature ID, observed base/branch/commit, changed paths, implemented behavior, exclusions, commands actually run with results, redacted visual/device evidence or its absence, privacy review, rollback, and remaining source/contract/hardware blockers. An empty evidence field remains unknown. Do not invent hashes, package identities, benchmark budgets, release dates, diagnoses or passing tests.

Optional enhancements remain reversible and preserve the lightweight, ad-free default. Source branding does not establish authorization for subscription access or playback. Each application owns its own interface and data boundaries.
