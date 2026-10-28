# Makad V1 Core Interaction Scenarios

| Field | Value |
|---|---|
| Status | Approved at scenario level; implementation details open |
| Version | 1.1 |
| Owner | Project builder |
| Last reviewed | 2026-08-14 |
| Depends on | `vision.md`, `v1-scope.md`, `constraints.md` |

## Purpose

These scenarios define what the Core V1 must make possible. They describe observable interaction semantics, not the final intent grammar, architecture, components, or astromech vocabulary.

Example utterances below are illustrative. The detailed natural-language phrase set and M4's authored sound language will be designed later.

## Scenario 1 — Wake, socialize, and assist

### Starting state

- M4 is powered on, stationary, and idle.
- The head may rest in a lowered or sleeping pose.
- The face shows a quiet idle state.
- The camera-side status LED reflects the approved idle state.

### Wake

1. The person calls “M4,” “M4K4,” or “Makad.”
2. M4 recognizes the invocation and transitions out of idle.
3. The head rises through a coordinated three-axis performance using powered roll, pitch, and yaw as appropriate.
4. The eyes wake, blink, or perform another approved transition.
5. The camera-side LED produces an approved wake/attention signal.
6. M4 emits a short astromech wake or acknowledgement sound.
7. M4 detects/acquires the person's face and directs its eyes and head toward them.

The response should read as one wake-up performance rather than a list of sequential device actions.

### Social exchange

1. The person says a natural greeting such as “Hi, how are you?”
2. M4 demonstrates understanding through an in-character response.
3. The response combines an astromech chirp/beep phrase, expressive eyes, three-axis head bobs/tilts/orientation, status-light behaviour where appropriate, and deliberate timing.
4. M4 remains attentive or returns naturally to idle depending on the interaction state.

Ordinary English speech output is not required and should not replace the authored astromech voice.

### Utility interactions

While awake, the person can naturally request:

- the current time, which M4 presents legibly on its display before returning to its face;
- a timer, which M4 confirms and signals when complete;
- an alarm, which M4 confirms and activates at the requested time;
- a song through Spotify, which M4 starts through the approved connected integration.

During music playback, M4 enters a characterful music-response state. At minimum the eyes “vibe” to the playback; richer head, light, or body motion may be added only within validated limits.

### Recovery and failure semantics

- An unrecognized or ambiguous request produces an in-character clarification/failure response rather than a false success.
- Network or Spotify failure produces a bounded failure response and does not leave motion or the display stuck.
- Timers and alarms have explicit stop/cancel behaviour, to be specified with the detailed intent set.

## Scenario 2 — Come here and follow me

### Starting state

- M4 is on an approved indoor floor in floor mode.
- The person is within the later-validated perception and movement envelope.
- M4 may initially be looking elsewhere.

### Come here

1. The person invokes M4 and asks it to “come here.”
2. M4 acknowledges the request through eyes, the status LED, head motion, or an astromech sound.
3. M4 searches for and acquires the person. Direct spatial-audio localization is optional; an initial implementation may use wake detection followed by visual search.
4. M4 turns its attention and body toward the person.
5. M4 approaches while maintaining person awareness, respecting obstacles, and controlling its speed within the approved household envelope.
6. M4 stops approximately 0.6–0.9 m from the person and visibly settles into an attentive state.

### Follow me

1. The person asks M4 to “follow me.”
2. M4 acknowledges and enters the following state.
3. M4 follows the selected person over the approved same-room route of up to approximately 3 m at a slow walking speed no greater than approximately 0.5 m/s while maintaining a bounded following distance.
4. M4 handles temporary person loss, obstacles, stopping, and reacquisition according to the later-approved policy.
5. If continuing safely is not possible, M4 stops and communicates the loss/failure instead of moving blindly.

### Expressive movement

M4 performs at least one excited spin as an authored character action during the approved Core demonstration. Expressive base motion remains subordinate to stability, obstacle constraints, and awareness of the person.

### End state

The scenario ends when the person asks M4 to stop, following becomes unsafe, or the approved destination/state is reached. M4 stops, acknowledges, and transitions to attentive idle.

## Cross-scenario requirements

- Display, astromech audio, status light, head, and base actions express one coherent intent.
- A named wake event does not directly trigger locomotion without the corresponding request and validated state.
- Person selection must avoid silently switching to another visible person.
- Tabletop mode inhibits ordinary come/follow movements and the excited spin. Only explicitly enabled low-speed test/calibration movement inside the validated circular footprint is permitted.
- Physical stop, low battery, sensor failure, controller failure, and cloud/service failure override or degrade the scenarios safely.
- Logs expose enough timestamps and state transitions to measure perception, reasoning, response, and physical onset separately.

## Details deliberately deferred

- complete intent list and accepted phrasing;
- wake-word implementation and thresholds;
- astromech vocabulary, grammar, and sound synthesis;
- display layouts for time, timer, alarm, and music;
- status-LED colour and animation language;
- person identity/selection, tracking, and reacquisition policy;
- final tolerances, pass rate, and loss/reacquisition thresholds within the approved household following envelope;
- drive, camera, microphone, compute, and cloud architecture;
- Spotify authentication and playback-control implementation;
- numeric success thresholds.

## Approval note

The project builder approved these scenario semantics on 2026-08-14. Version 1.1 adds Core three-axis head motion and the initial household following/tabletop envelopes. Deferred implementation details may be resolved later without changing the scenario, provided the observable Core behaviour is preserved.
