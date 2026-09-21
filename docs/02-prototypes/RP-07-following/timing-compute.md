# RP-07 timing, compute, memory, and thermal plan

| Field | Value |
|---|---|
| Status | Paper budgets and measurement plan; no Pi workload result |
| Hardware | Selected Raspberry Pi 5 2 GB + official Active Cooler + Camera Module 3 Wide |

## 1. Time points

| Stamp | Meaning |
|---|---|
| `t_sensor` | Camera start-of-frame/source timestamp |
| `t_effective` | Modeled effective time for target anchor/row |
| `t_available` | Completed request available to application |
| `t_detected` | Detector result complete |
| `t_tracked` | Association/fast-path update complete |
| `t_geometry` | Body-frame target and uncertainty complete |
| `t_published` | `TARGET_GEOMETRY` sent |
| `t_goal` | Core semantic goal sent |
| `t_c3_accept` | C3 validates/clamps goal |
| `t_motion` | Measured wheel/base response |
| `t_stop` | Measured stopped state |

Every scored run must make these joinable to external video through the project timebase procedure.

## 2. Existing perception budget

The inherited established-target requirement is:

```text
t_published - t_effective ≤ 100 ms at P95
```

RP-07 uses the following unregistered planning allocation as a starting structure:

| Stage | Existing planning direction |
|---|---:|
| Frame availability / transport | ≤35 ms |
| Tracker / landmarks | ≤30 ms |
| Geometry / filtering | ≤10 ms |
| Scheduling / IPC | ≤15 ms |
| Integration reserve | ≥10 ms |

Detector refresh may be slower than target publication if the fast path remains measured, bounded and periodically re-anchored. A prediction publication does not reset time since last visual measurement.

## 3. Rate plan

| Function | Candidate direction | Evidence required |
|---|---:|---|
| Camera capture | ≥30 fps mode | Source sequence/timestamps and drops |
| Active detector | ≥10 Hz target | End-to-end, not isolated model loop |
| Selected-target publication | ≥15 Hz MUST; ~30 Hz target | Fresh/predicted labels and jitter |
| Appearance descriptor | Event/low-rate | Worst reacquisition burst cost |
| Core behaviour loop | Existing 50–100 Hz design | Deadline/lease trace |
| Base/head telemetry | Existing architecture rates | Link and relay trace |

## 4. Pipeline rules

- One bounded capture queue; newest complete frame wins under overload.
- Dedicated metrics for capture, preprocessing, inference, association, appearance, geometry, IPC and consumer age.
- Thread counts are fixed/recorded for scored runs.
- Performance includes simultaneous representative audio, face/UI, logging, serial links and core behaviour.
- Isolated inference FPS is diagnostic only.
- P50/P95/P99/max and dropped-frame/late-publication counts are reported; averages alone do not pass.

## 5. C0 acceptance

| Resource | Candidate acceptance direction before freeze |
|---|---|
| Memory | No OOM kill; zero swap during scored interaction; `MemAvailable` target ≥20% sustained |
| CPU | Mandatory services meet deadlines; run queue and per-service utilization recorded |
| Thermal | No throttling in final body airflow at registered ambient; temperature and cooler RPM logged |
| Camera | No unexplained sequence/timestamp regression; drop rate registered |
| Storage | Logging/capture cannot violate authority lease; bounded write rate |
| Power | RP02 coexistence invariant rerun with the measured RP-07 workload |

## 6. Compute fallback ladder

Apply one controlled change at a time and rerun the same corpus:

1. remove preview/debug rendering;
2. use direct Picamera2 analysis stream and avoid format copies;
3. reduce/align inference input while preserving evidence resolution;
4. choose the faster validated runtime/quantization;
5. reduce appearance/face duty cycle, never mandatory freshness checks;
6. pin/bound threads after latency-jitter measurement;
7. revise detector/fast-path split;
8. only then evaluate an accelerator or camera architecture change.

An accelerator is not justified by one isolated low-FPS observation. It is justified only by repeatable failure of mandatory latency/rate/coexistence gates after bounded optimization, with power, heat, cost, packaging, driver and model constraints added to the comparison.

## 7. Thermal run

The workload run must include at least the final registered sustained duration and representative enclosure/airflow, ambient, active cooler control, camera, detector/tracker, face/UI, audio capture, core/hardware links and bounded logging. Record throttling flags, clock, temperature, fan RPM, latency and drops throughout—not only start/end temperatures.
