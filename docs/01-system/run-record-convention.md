# Makad Run-Record Convention

| Field | Value |
|---|---|
| Status | Active |
| Version | 1.0 |
| Owner | Project builder |
| Created | 2026-08-22 |
| Last reviewed | 2026-08-22 |
| Governing plan | `risk-prototype-plan.md` |

This convention gives every physical test execution one permanent identity. The run ID is a pointer, not a summary of the entire experiment: the associated run record carries the build, software, configuration, rig, instruments, limits, conditions, and evidence. This prevents a result from being separated from the setup that produced it or mixed with data from another iteration.

Use it for every bounded physical prototype execution that energizes an actuator, applies representative electrical/mechanical load, or produces evidence used for an engineering decision. This includes exploratory and pilot executions, which use the appropriate class rather than bypassing the record. Routine assembly, soldering, passive inspection, and unpowered fit checks do not require a run ID unless their result will be cited as evidence. Casual unrecorded bench work must not be cited as evidence.

## Run-ID format

```text
RP<prototype>-<scope>-<class>-<UTC allocation>-<sequence>
```

Example:

```text
RP01-G03V1-scored-20260822T091530Z-01
```

| Segment | Rule | Example |
|---|---|---|
| Prototype | Two digits, matching the prototype plan | `RP01` |
| Scope | Registered gate plus gate version, or `EXP` when no gate applies | `G03V1`, `EXP` |
| Class | Exactly `exploratory`, `pilot`, or `scored` | `scored` |
| UTC allocation | UTC calendar time when the ID is allocated, `YYYYMMDDThhmmssZ` | `20260822T091530Z` |
| Sequence | Two digits, starting at `01`; increment only if IDs would otherwise collide | `01` |

Valid examples:

```text
RP01-EXP-exploratory-20260822T083000Z-01
RP01-G03V1-pilot-20260822T090000Z-01
RP01-G03V1-scored-20260822T091530Z-01
```

The first registered version of a gate is `V1`. If its metric, threshold, controlled conditions, repetitions, aggregation, or pass logic changes after data is inspected, register a new gate version and use `V2`, `V3`, and so on. Fixing a typo that cannot affect interpretation does not create a new version; record the correction in the gate record.

## Allocation and immutability rules

1. Allocate the run ID before the test starts and create its `run.md` from the template.
2. One physical execution gets one run ID. A retry, power cycle, changed controlled configuration, or repeated trial block gets a new ID. One run may contain preregistered repetitions or an input sweep only when every trial and input value is recorded.
3. Never rename, reuse, or delete a run ID. Aborted, unsafe, invalid, and failed runs remain in the record.
4. Do not encode validity or results in the ID. Run validity and threshold result belong in `run.md`; the gate or prototype's `pass`, `iterate`, `reject`, or `defer` conclusion belongs in its summary because it may depend on several runs.
5. Record time in UTC in the ID and record the local timezone separately in `run.md`. Use the logging computer's clock to allocate the ID; clock-quality and synchronization uncertainty belong in the run record.
6. The ID is not proof of reproducibility. A scored run is not ready until the workbench gate and the required `run.md` fields are complete.

## Evidence location

Store each run at:

```text
docs/02-prototypes/RP-<NN>/runs/<run-id>/
```

Recommended layout:

```text
<run-id>/
├── run.md             # identity, configuration, checks, artifact manifest, result
├── data/              # raw machine-readable logs retained in Git when practical
├── derived/           # calculations, plots, and processed tables
└── media/             # photographs/video retained in Git when practical
```

Large raw data or video may live outside Git. `run.md` must then contain a stable path or asset identifier, byte size, and SHA-256 hash. An external file without that manifest entry is not part of the evidence packet.

When an artifact leaves its run directory, prefix its filename or embedded metadata with the complete run ID. Data files should also carry the run ID inside their header or metadata when the format permits.

## Configuration identity

Every scored run records all of the following; `unknown`, `latest`, and `same as before` are not valid values:

- repository commit and whether the worktree was clean;
- firmware build/commit for every powered controller;
- software build/commit for the logging or control computer;
- applied configuration file path plus Git revision or SHA-256 hash;
- every runtime override not present in that configuration file;
- rig name and revision, including ballast and geometry revision;
- sourced-part/candidate revision where component substitution could affect the result;
- current, velocity, torque, joint-angle, temperature, timeout, and other active safety/test limits.

If a run uses uncommitted code, save the patch as an artifact and record its SHA-256 hash. If a setting exists only in a GUI, photograph or export it and include that artifact in the manifest.

## Bench workflow

Before the run:

1. copy `docs/02-prototypes/_templates/run-record.md` into the run directory as `run.md`;
2. fill identity, gate, revisions, configuration, conditions, instruments, limits, and readiness checks;
3. start logging and confirm that the created log contains the same run ID;
4. show or announce the run ID at the start of external video so it can be correlated later.

After the run:

1. record end time, validity, deviations, faults, and observations without deleting failed attempts;
2. add every raw and derived artifact to the manifest and calculate its SHA-256 hash;
3. record calculated metrics, trial-level results, and whether this run meets its frozen threshold;
4. link the run from the gate summary and any ADR or engineering-budget update that cites it.

## What this convention does not solve

The run ID tells us which evidence belongs together. It does not itself synchronize clocks, define log schemas, validate sensor timestamps, or align external video. Those require the separate monotonic-timebase, logging, and video-synchronization methods in the prototype plan.
