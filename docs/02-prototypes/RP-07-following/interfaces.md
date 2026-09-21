# RP-07 interfaces

| Field | Value |
|---|---|
| Status | Semantic contract; serialization and byte layout open |
| Transport | C0 Unix-domain sockets; existing C0↔C2/C3 link contract |

All records include schema revision, source boot/session ID, sequence, monotonic source timestamp, validity/expiry, and configuration hash where relevant.

## 1. `PERSON_OBSERVATION`

One candidate or temporal track observation from `makad-perception`:

```text
frame_id, effective_capture_us, publish_us
track_id, track_state
person_box, optional face_box, anchor_type
existence_confidence, association_quality
bearing_camera[yaw,pitch], bearing_body[yaw,pitch]
bearing_uncertainty[yaw,pitch]
optional coarse_range_m, optional range_sigma_m, range_cue
image_quality_flags, visible_fraction
head_pose_sample_ids, base_pose_sample_ids
model_revision, calibration_revision
```

Rules:

- `track_id` is scoped to one perception session.
- absent range is valid; invented zero range is not.
- prediction-only observations say so and include time since last visual measurement.
- a box without calibrated geometry may support diagnostics, never motor intent.

## 2. `PERSON_CANDIDATE_SET`

Bounded list of current candidate observations plus capacity/overflow state. The selected target, if present, is pinned and cannot be evicted solely because the list is full.

## 3. `PERSON_SELECT`

Command from `makad-core`:

```text
action_id, selection_epoch
track_id
command_timestamp_us, expiry_us
selection_reason
```

Acceptance requires the named track to remain current and selectable. A stale/invalid track returns `NACK(STALE_TARGET|INVALID_TARGET|AMBIGUOUS)`; it never selects a different track.

## 4. `SELECTED_PERSON_STATE`

Owned by `makad-core` and keyed by a selection UUID independent of `track_id`:

```text
selection_uuid, selection_epoch
current_track_id or absent
PC state
freshness state
selection_match score and decision reason
last_visual_us, observation_age_us
loss_started_us, grace_expires_us, search_expires_us
current geometry and uncertainty
```

## 5. `TARGET_GEOMETRY`

The only person-derived geometry consumed by attention/come/follow:

```text
selection_uuid, observation_id
frame_id, effective_capture_us, publish_us, expires_us
body_bearing_rad, bearing_sigma_rad
optional range_m, optional range_sigma_m
radial_velocity estimate + uncertainty if valid
measured/predicted flag
quality and inhibit reasons
```

Consumers reject wrong UUID/epoch, expired observations, missing required geometry, nonfinite values and uncertainty outside their registered envelope.

## 6. Semantic base goal

`makad-core` may issue an expiring person-relative goal to the existing base interface:

```text
action_id, epoch, selection_uuid
mode = ALIGN | APPROACH | FOLLOW | BRAKE | HOLD
target_range_m, range_band_m
target_bearing_rad
v_limit_mps, omega_limit_radps
source_observation_id, source_age_us
expiry_us
```

C3 validates mode permission, session, expiry, hard limits and local hazards. It may clamp or reject. It never reinterprets another person as the target.

## 7. Head/base handoff

| Message | Producer | Consumer | Purpose |
|---|---|---|---|
| `HEAD_STATE` | C2 | C0 | Measured joints, limits, saturation/recenter request |
| `BASE_STATE` | C3 | C0/relay | Measured yaw, yaw rate, velocity, safety state |
| `BASE_YAW_RELAY` | `makad-hwd` | C2 | Timestamped C3 yaw/rate for counter-yaw primitive |
| `HEAD_GOAL` | core/composer | C2 | Selected-target attention goal with epoch/expiry |
| `BASE_GOAL` | core | C3 | Semantic person-relative base intent |

The relay transports measured state, not behavioural authority. Core remains the only source of a new base turn.

## 8. Health and reasons

Minimum reason codes:

```text
NO_CANDIDATE, AMBIGUOUS_CANDIDATE, TARGET_LOST,
REACQUISITION_REJECTED, OBSERVATION_STALE, FRAME_FROZEN,
CAMERA_UNAVAILABLE, CALIBRATION_INVALID, HEAD_POSE_STALE,
BASE_POSE_STALE, RANGE_UNAVAILABLE, RANGE_UNCERTAIN,
COMPUTE_OVERLOAD, THERMAL_THROTTLE, TABLETOP_DENIED,
LOCAL_SAFETY_CLAMP, LINK_EXPIRED, ACTION_CANCELLED
```

Completion and failure are explicit. A stop caused by loss or obstacle is never reported as successful follow completion.

