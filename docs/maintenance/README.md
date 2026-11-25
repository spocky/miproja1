# F04 local maintenance drafts

Prepared 2026-10-02 for this local configuration checkout. These files implement the documentation portion of F04 in the full upgrade handoff; they do not implement launcher features or change upstream administration.

The F04 author's write scope is `docs/maintenance/**` and `CONTRIBUTING.md`. The wider currently authorized configuration implementation includes F01/F02 plus F03 catalogue/audit work; this authoring boundary is not a limit on the overall programme. Already authorized local configuration edits and local commits need no duplicate authorization. Marquee and Gateway edits remain excluded following the user's concern. F25 is deferred under the assistant's commitment following repeated user concern, pending scope clarification, rather than an asserted explicit user deferral instruction. The externally owned server remains unchanged, and authorized Projectivy launcher core source is unavailable. The F04 author spawned no agents and performed author checks only; independent programme review is in progress.

## Contents

- [Draft bug report](bug-report.yml): environment, reproduction, expected/actual behavior, optional redacted evidence.
- [Draft feature request](feature-request.yml): user outcome, alternatives, optional environment and evidence.
- [Compatibility matrix](compatibility.md): all twelve root configs, with runtime compatibility explicitly unverified.
- [Support and triage](support.md): privacy, reproduction, evidence, and closure guidance.
- [Proposed labels](labels.md): suggestions for a later authorized administration step.
- [F01-F25 roadmap](roadmap.md): component ownership, evidence, existing issue leads, and blockers.
- [Contribution guide](../../CONTRIBUTING.md): the existing Python test, validate, and generate workflow.
- [Validation record](validation.md): document checks actually performed and their limits.

## Draft forms and activation boundary

The two `.yml` files are structured GitHub issue-form drafts kept outside `.github/ISSUE_TEMPLATE`. They use JSON syntax, which is a subset of [YAML 1.2](https://yaml.org/spec/1.2.2/), so they can be parsed offline with Python's standard-library JSON parser. Their elements follow [GitHub's form schema](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-githubs-form-schema). This format avoids adding a parser dependency for local review.

The drafts set no automatic labels or assignees. Existing `bug_report.md` and `feature_request.md` remain the active templates. Moving drafts into `.github`, creating labels, posting or closing issues, enabling Discussions, pushing, releasing, or opening a PR requires separate authorization. GitHub rendering/submission has not been tested because the drafts have not been activated.

## Evidence boundaries

The [repository README](../../README.md), [configuration authoring guide](../../config/README.md), root JSON files, local tooling/tests, and the full `../projectivy-package/Projectivy_Full_Upgrade_Codex_Handoff.md` (path relative to the repository root) informed these drafts. The observed base is `c4c66c9c85e9d001c7bac04aeb2746a5af1b0194` on local branch `codex/projectivy-config-f01-f02`; pre-existing untracked configuration, workflow, test, tool, and plan files were preserved. The F04 author created no commit; this is an action record, not a restriction on authorized local integration commits.

An existing config is evidence of stored configuration, not device support. A named artifact in a URL is not a verified package, signing identity, digest, or compatibility pin. An issue title is a reported symptom or request, not a confirmed root cause. Keep these distinctions in future updates.
