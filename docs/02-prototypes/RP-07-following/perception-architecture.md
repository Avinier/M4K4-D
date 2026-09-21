# RP-07 perception architecture

| Field | Value |
|---|---|
| Status | Paper implementation lead; backend selection waits on replay evidence |
| Architecture ID | `PS-HYBRID-01` |

## 1. Processing graph

```text
Camera Module 3 Wide
  → Picamera2/libcamera request + metadata
  → bounded newest-frame queue
  → image-quality assessment
  → person detector ───────────────┐
  → optional face/landmarks ───────┤
  → multi-person association ──────┤
  → selected-target fast update ───┤
  → appearance evidence (sparse) ──┤
  → calibrated geometry + uncertainty
  → candidate observations
  → makad-core selection / continuity state
  → selected-target observation
```

Frames are never allowed to accumulate in an unbounded inference FIFO. When perception falls behind, older unprocessed frames are dropped, sequence gaps are logged, and the newest complete frame wins.

## 2. Service ownership

| Service | Owns | Forbidden |
|---|---|---|
| `makad-perception` | Camera session, frame metadata, image-quality state, detections, tracks, appearance evidence, transforms, uncertainty, replay | Selecting a replacement person; motor/head/base command |
| `makad-core` | Candidate-to-selected transition, target UUID, person continuity, action lifecycle, search/come/follow semantic intent | Opening camera/servo/wheel devices |
| `makad-hwd` | C2/C3 links, time reconciliation, bounded queues, base-yaw relay, evidence capture | Inventing behaviour or target identity |
| C2 | Head trajectory, limits, counter-yaw/recenter execution, head state | Selecting people; commanding wheels |
| C3 | Base velocity/trajectory execution, odometry, hazards, stop priority | Overriding a lost/stale target with predicted motion |

## 3. Camera acquisition

- Use Picamera2/libcamera on the selected visible-light Camera Module 3 Wide.
- Configure at least one analysis stream and retain the option of a separate evidence stream.
- Carry request sequence, `SensorTimestamp`, exposure time, frame duration, crop, focus, gain and image-quality flags.
- Define effective capture time from measured sensor/readout semantics. Host arrival time is diagnostic only.
- Autofocus may acquire before tracking. During critical measurements and head gestures, use a recorded focus policy that avoids unexplained focus breathing.
- A camera restart creates a new camera-session identifier and invalidates all old tracks.

## 4. Detection and tracking layers

### 4.1 Whole-person detector

The detector produces candidate boxes, confidence, class, frame ID and model revision. It does not produce durable identity. Active target is at least the inherited target rate after measurement; idle presence may duty-cycle.

### 4.2 Multi-person association

Association maintains tentative, confirmed, occluded and lost tracklets. It may use box overlap, predicted motion, confidence and appearance. It must incorporate measured camera motion before treating pixel displacement as person motion.

### 4.3 Selected-target fast path

Between detector refreshes, the selected target may be updated with:

- calibrated kinematic prediction;
- a lightweight local tracker or optical-flow measurement;
- the latest measured head/base motion.

Predicted output is labelled predicted, carries increasing uncertainty, and expires. A local tracker may fail early; it may not silently drift forever.

### 4.4 Appearance evidence

Appearance evidence is computed at controlled times:

- several clean views at selection;
- bounded refresh while the selected track is confidently associated;
- each plausible reacquisition candidate.

The short-session gallery has a fixed capacity, records view/quality/time, and is deleted when selection expires or the session ends. It is not a face-recognition database.

### 4.5 Face and landmarks

Face evidence associates to a person track. It provides social-gaze anchor and coarse face orientation when sufficiently resolved. Body continuity remains primary when the face turns away or is too small.

## 5. Confidence decomposition

One scalar confidence is forbidden. Every selected observation distinguishes:

| Quantity | Meaning |
|---|---|
| existence confidence | Evidence that the observation is a real person |
| association quality | Evidence that it belongs to this temporal track |
| selection match | Evidence that a candidate is the pinned selected person |
| bearing uncertainty | Angular uncertainty after geometry and timing |
| range uncertainty | Coarse distance uncertainty; never safety range |
| image quality | Blur/exposure/occlusion/edge/crop sufficiency |

## 6. Backpressure and degradation

| Condition | Required response |
|---|---|
| Detector misses one refresh; fast path valid | Publish predicted/updated target with widened uncertainty |
| Inference queue contains older frame | Drop old frame; record drop |
| Latency exceeds motion freshness | Mark stale; core suppresses/zeros locomotion intent |
| Appearance backend unavailable | Continue only while geometric track continuity is unambiguous; no risky reacquisition |
| Face backend unavailable | Use body anchor; report degradation |
| Joint pose unavailable/misaligned | No high-accuracy body-frame bearing; inhibit closed-loop head/base use |
| Calibration/config hash mismatch | Perception unavailable for motion |
| Sustained overload/throttling | Duty-cycle optional stages, then stop person-dependent motion if mandatory limits remain missed |

## 7. Replay determinism

An engineering recording contains raw frames, request metadata, calibrated time mapping, head/base state history, configuration/model hashes and user annotations. Replay uses the same processing graph after the camera source. Random seeds, runtime thread count and nondeterministic backend limits are recorded.

Replay is the selection instrument. It is not physical proof of head motion, stopping, obstacle handling or thermal enclosure performance.

