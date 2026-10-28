# RP-07 inherited contracts

| Field | Value |
|---|---|
| Status | Documentation baseline |
| Rule | Cite the owner; do not fork the same state, limit, or requirement in RP-07 |

## 1. Source order and precedence

1. approved foundation scope, constraints, scenarios, and success criteria;
2. registered RP-02 state/authority/time contracts;
3. RP-03 local-safety and base contracts;
4. RP-01 head motion and RP-04 coordination contracts;
5. RP-07 requirements, implementation choices and candidate thresholds.

If an RP-07 value conflicts with an approved upstream value, the upstream value wins until explicit change control records otherwise.

## 2. Inherited map

| Owner | RP-07 consumes | RP-07 must not redefine |
|---|---|---|
| Foundation | Single-room/3 m/0.5 m/s envelope; 1–2 m come start; 0.6–0.9 m settle; tabletop inhibition; person-following is Core | V1 scope or scenario semantics |
| Camera study | Camera Module 3 Wide SC0874; moving-head CSI path; source timestamp and image-quality obligations | Camera selection without a recorded hard failure |
| RP-01 | `HM-04` bounded search; `HM-05` acquire/track; measured joint state; limits; safe settle | Servo selection, trajectory limits, or head safety |
| RP-02 | `PC-01…06`, `BS-03/04/09`, `EV-18/19`, action lifecycle, modes, leases, timestamps, power cases | Person-continuity state names or permission semantics |
| RP-03 | C3 owns wheels, hazards, stop priority, speed/acceleration clamps, command expiry, odometry, tabletop inhibit | Wheel loops, obstacle policy, stopping physics, or sensor truth |
| RP-04 | Epochs, cancellation, cue identity, degradation, P-01/P-02 coordination, `BD-08` counter-yaw issue | A parallel composer or actuator command path |
| Compute architecture | `makad-perception`, `makad-core`, `makad-hwd`; UDS IPC; no ROS 2 in the V1 safety path | New process/MCU topology without evidence |

## 3. RP-07 paper performance candidates

These values are owned by [`requirements.md`](requirements.md). They are paper design candidates derived for RP-07, not inherited approvals or registered gate thresholds:

| Requirement | Candidate value |
|---|---:|
| Active candidate acquisition | ≤250 ms under nominal validated conditions |
| Established selected-target update | ≥15 Hz; target approximately 30 Hz |
| Active detector refresh | Target ≥10 Hz |
| Established capture-to-publication latency | ≤100 ms P95 under representative load |
| Short occlusion persistence | Initial target 0.3–0.7 s; tune empirically |
| Bearing error | Target ≤1.5° P95; minimum acceptable V1 ≤3° |
| Stationary bearing jitter | Target ≤0.5° RMS |
| Multiple people | At least two; target at least three |

RP-07 must measure these together with the following-specific motion and stop outcomes.

## 4. Conflict notes

- RP-07 classifies camera-derived person range as non-safety data; it cannot replace C3 obstacle clearance.
- RP-07 permits non-biometric short-term reacquisition only. Appearance descriptors remain session-local and are deleted at action/session expiry.
- RP-02 says the base remains stopped during `PC-04/05` unless RP-07 proves otherwise. RP-07 retains the stopped rule for V1.
- RP-04 `BD-08` concerns counter-yaw ownership. RP-07 proposes a closure in `decision.md`, but RP-04 must record the accepted answer before implementation claims closure.
- RP-03 physical gates are not passed. RP-07 floor-motion phases therefore remain blocked even if replay/head-only work succeeds.

## 5. Evidence classes

| Mark | Meaning |
|---|---|
| `D` | Datasheet or normative source |
| `E` | Engineering estimate, literature result, or paper allocation |
| `W` | Measured on representative Makad hardware/workload |
| `U` | Unknown; never treated as zero |

Every gate conclusion must identify which quantities became `W`.
