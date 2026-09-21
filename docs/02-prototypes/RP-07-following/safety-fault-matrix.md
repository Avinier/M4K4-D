# RP-07 safety authority and fault matrix

| Field | Value |
|---|---|
| Status | Paper fault campaign; injection procedures require rig-specific registration |

## 1. Authority order

Highest first:

1. hardware E-stop / motor-gate loss;
2. energy or controller-readiness loss;
3. C3 cliff, pickup/tip, encoder, driver and registered obstacle protection;
4. command/heartbeat/session expiry;
5. explicit inhibit/cancel;
6. target freshness, selection and geometry eligibility;
7. valid come/follow intent;
8. expressive/procedural motion.

Higher authority may clamp, brake or reject. Recovery exposes availability but never replays an old action.

## 2. Following invariants

- C0 cannot keep motion alive without fresh semantic goals.
- C3 can stop without C0, network, perception or camera.
- `PC-04/05/06` implies no forward following command.
- `OM-02/03/04/06` rejects ordinary come/follow.
- A predicted target never becomes indefinitely fresh.
- An unavailable range blocks forward motion.
- A local obstacle response is successful safety intervention, not successful follow completion.
- Reconnection/reset returns to inhibited state and requires a fresh action/selection/arm sequence.

## 3. Fault campaign

| ID | Injection | Required result | Evidence |
|---|---|---|---|
| `F07-01` | Pause camera frames | Observation age rises; base goal expires/brakes; target may remain reserved only during stopped grace | Frame/goal/base timestamps |
| `F07-02` | Repeat one frame/metadata pair | Freeze detected from sequence/timestamp/content checks; no continued blind motion | Detection reason and stop timing |
| `F07-03` | Deliver frames late/out of order | Late frame rejected; no time regression or queue replay | Sequence trace |
| `F07-04` | Kill/restart `makad-perception` | Tracks/selections become unavailable; new session cannot inherit old track IDs | Process/session log |
| `F07-05` | Overload CPU/inference | Old frames drop; health degrades; motion stops if mandatory timing missed | Queue, CPU, latency, goals |
| `F07-06` | Invalid calibration hash | Motion-eligible geometry withheld | NACK/health state |
| `F07-07` | Freeze/stale head joint state | Bearing uncertainty invalidates closed-loop use; head/base intent inhibited | Pose age and inhibit |
| `F07-08` | Freeze/stale base yaw relay | Counter-yaw degrades/stops; no guessed integration | C2 trace |
| `F07-09` | Distractor crosses target | No selection switch; loss/ambiguity brakes | Selection UUID trace |
| `F07-10` | Target exits; distractor remains | Distractor stays candidate only; base stops; eventual `PC-06` | Track/PC/action trace |
| `F07-11` | Stale `PERSON_SELECT` | Explicit NACK; no substitute target | IPC trace |
| `F07-12` | Corrupt/nonfinite target geometry | Consumer rejects; no motor command | Validation reason |
| `F07-13` | C0↔C3 link loss | C3 expiry brakes within registered bound | Link/base/video timing |
| `F07-14` | C0↔C2 link loss | Head bounded stop/inhibit; base action also cancelled if tracking dependency lost | Link/head/base trace |
| `F07-15` | C3 obstacle during follow | Local clamp outranks goal; no automatic resume | Hazard/command/motion trace |
| `F07-16` | Cliff/edge input during permitted rig motion | Local stop/inhibit; action fails safely | Sensor and motion trace |
| `F07-17` | Switch Floor→Tabletop while action active | Base brakes; ordinary come/follow denied; fresh floor/action required later | Mode/action trace |
| `F07-18` | Reset C3 during follow | Motor output bounded; restart inhibited; stale goal not replayed | Reset reason/video |
| `F07-19` | Thermal throttling or memory pressure | Health visible; mandatory timing enforced; no silent degraded motion | Temperature/memory/latency |
| `F07-20` | Disk/logging failure | Nonessential recording degrades; safety links remain live; evidence health reports loss | I/O/lease trace |

## 4. Stale and frozen detection

Frame validity checks are independent:

- source sequence monotonicity and gaps;
- source timestamp monotonicity and age;
- host arrival and processing age;
- repeated-buffer/content indicator where practical;
- camera-session identifier;
- exposure/frame metadata plausibility.

A changing host arrival timestamp cannot make a repeated old image fresh.

## 5. Physical test constraints

Powered injections occur only after the workbench readiness gate, E-stop check, speed/acceleration registration, caught/guarded setup where required, and RP-03 prerequisite gates. Software-only faults are first proven in replay/simulation. No fault injection bypasses C3 or defeats a physical stop.

## 6. Safety-standard posture

ISO 13482 may inform hazard identification for a mobile servant robot, particularly autonomous-decision uncertainty and unexpected human/robot movement. RP-07 does not claim conformity, certification, validated injury limits, or safety integrity level.

