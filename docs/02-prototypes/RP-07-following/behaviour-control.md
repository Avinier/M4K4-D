# RP-07 search, come, and follow control

| Field | Value |
|---|---|
| Status | Paper controller contract; all gains, limits and motion outcomes await RP-03/RP-07 evidence |

## 1. Authority decomposition

```text
makad-perception: what/where/uncertainty
makad-core: who is selected and what behaviour is authorized
C2: how the head executes bounded attention/counter-yaw
C3: how the base executes bounded motion and all local safety
```

No controller in this file weakens C3 clamps or the action/lease expiry chain.

## 2. Search

Search begins only from an authorized acquisition/reacquisition action.

- `HM-04` supplies the bounded head-sector motion.
- New candidate observations may interrupt the remaining search sectors.
- Initial acquisition may select under the configured interaction rule.
- Reacquisition searches only for the existing selection UUID.
- Reacquisition keeps the base stopped in V1.
- Search ends on selection, explicit cancel, timeout, head/pose fault, or permission loss.
- Search timeout produces explicit failure, not an endless scan.

Base-assisted initial search is deferred unless a later registered case proves need and safety. It is not required for the approved same-room envelope.

## 3. Head tracking and head/base handoff

The head normally absorbs small target-bearing changes. Base yaw is requested only when:

- the target is fresh and selected;
- head yaw approaches the registered useful limit or sustained bearing exceeds a registered handoff threshold;
- floor motion and C3 readiness are valid;
- the active behaviour permits body rotation;
- predicted stopping/clearance remains valid.

C2 reports measured pose and recenter need. Core authorizes an expiring base alignment goal. C3 executes/clamps it. `makad-hwd` relays timestamped measured base yaw/rate to C2, which counter-yaws so the camera does not whip away from the target.

Head counter-yaw is a trajectory primitive, not a high-rate cue graph. On missing/stale relay state it degrades or stops; it does not integrate guessed base motion.

## 4. Common control inputs

Each control cycle consumes:

- action and selection UUID/epoch;
- target observation ID and effective capture age;
- body-frame bearing and uncertainty;
- range/range uncertainty where forward motion is requested;
- target visibility/prediction state;
- measured base velocity/yaw and C3 safety state;
- measured head pose/limits;
- operating mode, energy and action lifecycle.

Any required invalid input suppresses the corresponding output.

## 5. Come controller

### 5.1 Phases

| Phase | Entry | Output | Exit |
|---|---|---|---|
| `COME-ACQUIRE` | action accepted; no current fresh target | Stationary bounded search | `PC-03` or failure |
| `COME-ALIGN` | fresh target; bearing outside launch window | Zero/limited forward speed; bounded yaw | aligned, loss, clamp or timeout |
| `COME-APPROACH` | bearing/range/clearance valid | Smooth forward/yaw goal with speed scheduled by stopping margin | brake trigger, loss, clamp or cancel |
| `COME-BRAKE` | predicted entry into settle band or any inhibit | Zero-speed/brake semantic goal | measured stop |
| `COME-SETTLE` | stopped in 0.6–0.9 m band | Hold base; head attention may continue | stable dwell then complete |
| `COME-FAIL` | invalid/lost/unsafe/timeout | Stop; bounded failure indication | new action only |

### 5.2 Control form

Paper form only:

```text
e_r = range - target_range
e_yaw = target bearing in body frame
v_cmd = scheduled bounded function(e_r, stopping margin, uncertainty)
omega_cmd = bounded function(e_yaw, head handoff, stability)
```

The final implementation must include deadbands, acceleration/jerk limits, anti-windup or equivalent saturation handling, measurement-age gates and measured-stop confirmation. Raw box error is inadmissible.

### 5.3 Settling

Completion requires the registered range band for a registered dwell while measured base speed is below the stop threshold. A transient range sample inside the band is not completion. Rollback or an unrequested second creep is failure/iteration evidence.

## 6. Follow controller

### 6.1 Objective

Maintain a registered target distance while following the selected person over the marked ≤3 m route, including one gentle turn, with speed ≤0.5 m/s and continuous C3 safety authority.

### 6.2 Policy

- Use a following setpoint outside the come settle band unless registration explicitly selects otherwise.
- Schedule speed down as range error shrinks, bearing error grows, uncertainty grows, clearance shrinks, or a head/base handoff begins.
- Permit forward motion only from fresh selected-target range.
- Permit bounded yaw alignment from fresh bearing when forward motion is inhibited, subject to C3.
- Never reverse toward an unseen person merely because range is reported too small.
- An obstacle clamp stops/denies the action; clearing it does not automatically resume.
- Route completion is an operator/test event or explicit stop request, not loss of target.

### 6.3 Initial unscored authority ladder

| Stage | Maximum allowed intent |
|---|---|
| Floor checkout | 0.10 m/s |
| Early come | 0.20–0.25 m/s |
| Mature come / straight follow | Value supported by stopping evidence |
| Final scored ceiling | Never above 0.5 m/s |

These are staging limits, not claims that any speed is safe.

## 7. Stopping-margin invariant

Before forward command, the controller computes a conservative required stopping distance using measured speed, registered deceleration, command/actuation latency, observation age, uncertainty and margin. C3 independently enforces its local envelope.

```text
available target/obstacle clearance > required stopping distance + registered margin
```

If the invariant is false or unknown, forward intent is zero. Camera person range may influence behaviour but never establishes obstacle-free clearance.

## 8. Terminal outcomes

| Outcome | Meaning |
|---|---|
| `COMPLETED` | Behaviour-specific endpoint reached and measured settle confirmed |
| `CANCELLED` | User/higher-priority action cancelled; stopped |
| `TARGET_LOST` | Selection expired after stopped reacquisition failed |
| `SAFETY_STOP` | C3 intervention or permission loss stopped motion |
| `PERCEPTION_FAULT` | Required geometry/freshness/calibration unavailable |
| `TIMEOUT` | Bounded phase/action deadline expired |

Only `COMPLETED` is success. Every terminal state is logged once and old goals are invalid afterward.

