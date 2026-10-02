# Proposed labels

Draft suggestions only. No labels have been created or applied. Check existing repository labels before a later authorized administration step; reuse an equivalent label rather than adding duplicates. Colors and label identifiers are deliberately unspecified.

| Proposed label | Meaning and evidence rule |
|---|---|
| `type:bug` | Reported unexpected behavior; does not establish cause. |
| `type:feature` | Desired user outcome; does not imply acceptance or implementation. |
| `type:documentation` | Maintenance/reporting/contributor material such as F04. |
| `area:configuration` | Authoring sources, root outputs, generation or offline validation. |
| `area:launcher-core` | HOME, focus, rendering, profiles, global input/cache/idle or settings authority. |
| `area:wallpaper-provider` | Existing wallpaper-provider contract and provider-owned lifecycle/data. |
| `area:integration` | A verified provider/publisher contract; not proof that a service is supported. |
| `area:maintenance` | Triage, compatibility records, contributor guidance and roadmap. |
| `evidence:reported` | Unconfirmed observation or title-level reproduction lead. |
| `evidence:needs-reproduction` | Minimum non-sensitive steps or environment are missing. |
| `evidence:reproduced` | Specific reproduction and environment recorded; cause may remain unknown. |
| `evidence:verified-local` | Actual named local checks recorded; no device pass implied. |
| `evidence:hardware-unverified` | Required real-device acceptance is unavailable or not run. |
| `scope:device-specific` | Report limited to the supplied model/firmware; do not generalize it. |
| `blocked:source` | Actual authorized launcher implementation source is unavailable. |
| `blocked:contract` | Export/API/provider capability needs a real verified contract. |
| `scope:excluded` | Owning component is excluded from this task, including Marquee/Gateway. |
| `status:deferred-scope` | F25 is deferred under the assistant's commitment following repeated user concern, pending scope clarification; this label does not assert an explicit user deferral instruction. |
| `review:privacy` | Optional evidence or design needs redaction/authorization review. |

Use type, area, evidence and blocker independently. For example, a HOME report may be `type:bug`, `area:launcher-core`, `evidence:reported`, `scope:device-specific`, `blocked:source` and `evidence:hardware-unverified`. These are proposed classifications, not applied labels or a confirmed diagnosis.

Do not assign `fixed` or `supported` based on a proposal, document validation, config inventory, or an issue's closed state. Administrative activation and public status changes remain outside the local F04 work.
