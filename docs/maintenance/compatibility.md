# Configuration inventory and compatibility matrix

Snapshot: 2026-10-02. All twelve root JSON files were inspected. **Every row is runtime unverified; none is a supported-device claim.** Config presence, identical content, or offline validation cannot establish actual model, firmware, Android, HOME behavior, installation safety, or playback compatibility.

Aliases and authoring families come from [the local manifest](../../config/source/manifest.json) and [authoring guide](../../config/README.md). A family is an authoring grouping, not a verified retail model mapping. Root `product` values name Projectivy Launcher rather than a device model. No verified model/firmware/Android mapping or device evidence was found in these root configs.

The stock-launcher strings below are copied from the root `launcher` fields. They describe stored configuration only: they are not Projectivy's package identity, a runtime detection result, or permission to disable a package. The release values are read from each `toolsUrl` path/filename, not verified artifact metadata or installed app versions.

| Alias | Authoring family | Root config | Configured stock-launcher field | toolsUrl release text | Model / firmware / Android | Runtime compatibility |
|---|---|---|---|---|---|---|
| batman | Xiaomi | [batman.v2.json](../../batman.v2.json) | `com.mitv.tvhome` | 4.67 | Unverified / unknown | Runtime unverified |
| conan | Xiaomi | [conan.v2.json](../../conan.v2.json) | `com.mitv.tvhome` | 4.67 | Unverified / unknown | Runtime unverified |
| doraemon | Xiaomi | [doraemon.json](../../doraemon.json) | `com.mitv.tvhome` | 4.67 | Unverified / unknown | Runtime unverified |
| franky | Xiaomi | [franky.json](../../franky.json) | `com.mitv.tvhome` | 4.67 | Unverified / unknown | Runtime unverified |
| generic | Generic | [generic.v2.json](../../generic.v2.json) | Field absent | 4.68 | Unverified / unknown | Runtime unverified |
| goblin | Fengmi | [goblin.v2.json](../../goblin.v2.json) | `cn.formovie.fengos.desktop` | 4.67 | Unverified / unknown | Runtime unverified |
| jerry | Fengmi | [jerry.v2.json](../../jerry.v2.json) | `cn.formovie.fengos.desktop` | 4.67 | Unverified / unknown | Runtime unverified |
| matrix | Xiaomi | [matrix.v2.json](../../matrix.v2.json) | `com.mitv.tvhome` | 4.67 | Unverified / unknown | Runtime unverified |
| nemo | Fengmi | [nemo.v2.json](../../nemo.v2.json) | `cn.formovie.fengos.desktop` | 4.67 | Unverified / unknown | Runtime unverified |
| rainman | Xiaomi | [rainman.v2.json](../../rainman.v2.json) | `com.mitv.tvhome` | 4.67 | Unverified / unknown | Runtime unverified |
| xmen | Xiaomi | [xmen.v2.json](../../xmen.v2.json) | `com.mitv.tvhome` | 4.67 | Unverified / unknown | Runtime unverified |
| zodiac | Xiaomi | [zodiac.v2.json](../../zodiac.v2.json) | `com.mitv.tvhome` | 4.67 | Unverified / unknown | Runtime unverified |

`generic` does not mean universal compatibility. The user's Shield is a proposed acceptance target in the handoff, not a tested device or an inferred alias. No Shield pass or general Android TV support claim is recorded here.

## Version and evidence policy

The root `version` field is `2`; it is manifest/configuration metadata, not the installed app version. The `.v2` suffix alone is also not an app version. The stored `releaseDate` is `2025-08-09T00:00:00.000Z`; it is not the date of this inspection, device testing, or a verified APK release. Do not rewrite these fields to invent freshness.

Preserve existing paths and device pins during the authorized configuration implementation. A proposed pin change needs independent artifact and device evidence; the F04 author's documentation boundary does not impose duplicate authorization on already authorized local configuration edits. Do not force every alias onto the newest APK, infer publisher authenticity from a checksum, or substitute HTTPS without verifying the actual endpoint/artifact. No APKs were downloaded, inspected, installed, or executed for this matrix.

## Recording future acceptance

For an authorized target-device check, record manufacturer/model (no serial number), firmware/Android version, installed launcher version, existing HOME/integration method, exact config filename, steps, expected/actual results, test date, and safe redacted evidence. Record each scenario separately:

- Cold boot and standby/wake without focus takeover.
- Launch/return with Back and Home and restored focus.
- Offline operation and a temporarily unavailable source without preference loss.
- Profile/permission revocation without private content leakage.
- Remote and gamepad input isolation.
- Large text, reduced motion, long labels, readable fallback and safe areas.
- Artwork/cache pressure without clearing settings; extended idle without interrupting playback.
- Interrupted appearance apply or restore with recoverable settings.

Untested scenarios stay unverified. A reported success is `reported`, a reproduced failure is `reproduced`, and a device pass requires actual scenario evidence. None alone authorizes a general supported-device designation. Testing and changing TV settings are outside this F04 document task.
