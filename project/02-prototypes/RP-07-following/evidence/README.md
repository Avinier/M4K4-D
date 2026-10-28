# RP-07 evidence index

| Field | Value |
|---|---|
| Status | **Empty. No RP-07 recording or physical test has been executed.** |

Future evidence is organized by immutable run ID:

```text
evidence/
  RUN-ID/
    manifest.yaml
    test-plan-snapshot/
    configuration/
    calibration/
    logs/
    measurements/
    external-video/
    annotations/
    results.md
```

Each manifest records:

- test and gate revision;
- pilot/scored designation;
- date/operator/location/ambient/floor/lighting;
- subject/test-material consent and retention record where applicable;
- robot rig, ballast, hardware and harness revisions;
- OS/kernel/Picamera2/libcamera/runtime/model/source/config hashes;
- calibration revisions;
- clocks/time-sync method and external timing cue;
- instrument identifiers/checks and uncertainties;
- raw asset locations and hashes, including assets stored outside Git;
- deviations, faults, anomalies and terminal outcome.

Large frames/video may remain outside Git. The manifest must retain a stable asset identifier/path and cryptographic hash. A missing asset or revision makes that run incomplete for `RP07-G07`.

Do not add placeholder PASS files. A run directory exists only when evidence exists.

