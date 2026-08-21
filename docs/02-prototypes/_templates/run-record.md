# Run record: `<run-id>`

Copy this file to `docs/02-prototypes/RP-<NN>/runs/<run-id>/run.md` before the run. Replace every required placeholder; do not use `same as before`, `latest`, or `unknown` for a scored run.

## Identity

| Field | Value |
|---|---|
| Run ID | `<RP01-G03V1-scored-20260822T091530Z-01>` |
| Prototype | `<RP01>` |
| Gate / version | `<RP01-G03 / V1, or EXP>` |
| Class | `<exploratory / pilot / scored>` |
| Operator | `<name>` |
| Start UTC | `<YYYY-MM-DDThh:mm:ss.sssZ>` |
| End UTC | `<YYYY-MM-DDThh:mm:ss.sssZ>` |
| Local timezone | `<IANA name, e.g. Asia/Kolkata>` |
| State | `<planned / running / complete / aborted>` |
| Evidence validity | `<pending / valid / invalid / aborted>` |
| Threshold result | `<unscored / meets / misses / not evaluated>` |

## Test and gate snapshot

| Field | Value |
|---|---|
| Test-plan revision/path | `<commit + path or artifact>` |
| Gate-registration revision/path | `<commit + path or artifact; n/a only for EXP>` |
| Metric and unit | `<definition>` |
| Frozen threshold / allowed range | `<value>` |
| Repetitions and aggregation | `<count + method>` |

## Build and configuration

| Field | Value |
|---|---|
| Repository commit | `<full commit hash>` |
| Worktree state | `<clean, or patch artifact + SHA-256>` |
| Firmware revisions | `<controller: build/commit; repeat as needed>` |
| Software revisions | `<component: build/commit; repeat as needed>` |
| Configuration | `<path + Git revision or SHA-256>` |
| Runtime overrides | `<explicit key=value list, or none>` |
| Rig name / revision | `<stable rig ID + revision>` |
| Ballast / geometry | `<mass, centre-of-mass proxy, dimensions, fixture state>` |
| Candidate / sourced-part revisions | `<identifiers>` |

## Conditions and active limits

| Field | Value |
|---|---|
| Supply | `<set voltage, current limit, measured idle voltage>` |
| Current limits | `<values and locations>` |
| Velocity / acceleration limits | `<values>` |
| Torque limits | `<values>` |
| Joint-angle / travel limits | `<values>` |
| Temperature / timeout limits | `<values>` |
| Environment | `<surface, lighting, distance, ambient temperature, other controlled conditions>` |

## Instruments and readiness

| Check | Record |
|---|---|
| Instrument list | `<instrument, model/ID, sample rate/resolution>` |
| Calibration / check | `<method, result, time>` |
| E-stop verified this session | `<UTC time + result>` |
| Rig restrained / cannot leave surface | `<method + result>` |
| Limits checked for this test | `<UTC time + result>` |
| Logging confirmed writing | `<UTC time + sample/log path>` |
| Timebase / clock synchronization | `<method + measured/estimated uncertainty>` |
| External video synchronization | `<method + cue/event>` |

## Procedure and deviations

Planned procedure:

1. `<step>`

Deviations, faults, unsafe observations, or reasons for abort:

- `<none, or timestamped observation>`

## Artifact manifest

Every external artifact requires a stable path or asset ID, byte size, and SHA-256 hash.

| Artifact | Role | Location / asset ID | Bytes | SHA-256 |
|---|---|---|---:|---|
| `<filename>` | `<raw log / video / photo / patch / derived table / plot>` | `<relative path or stable external identifier>` | `<size>` | `<hash>` |

## Results

| Trial | Metric | Result | Valid? | Notes |
|---:|---|---:|---|---|
| 1 | `<metric>` | `<value + unit>` | `<yes/no>` | `<note>` |

Calculated aggregate and uncertainty:

`<result>`

## Result and traceability

- Evidence validity: `<valid / invalid / aborted, with reason>`
- Threshold result: `<unscored / meets / misses / not evaluated>`
- Engineering conclusion: `<what this evidence supports and does not support>`
- Follow-up change: `<bounded next action or none>`
- Gate summary link: `<path>`
- ADR / budget / requirement updates: `<paths or none>`

The gate or prototype summary—not an individual run record—owns the final `pass`, `iterate`, `reject`, or `defer` decision when multiple runs contribute.
