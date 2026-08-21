# Makad V1 Success Criteria

| Field | Value |
|---|---|
| Status | Approved |
| Version | 1.1 |
| Owner | Project builder |
| Last reviewed | 2026-08-14 |
| Depends on | Approved `vision.md`, `v1-scope.md`, `constraints.md`, and `core-interaction-scenarios.md` |

## Definition of success

Makad V1 succeeds when M4 delivers a convincing, safe-for-its-real-hazards, repeatable droid encounter on battery power. The encounter must demonstrate that natural-language understanding, visual perception, display expression, astromech audio, expressive head movement, wheeled movement, and timing operate as one character.

V1 must also produce credible evidence of learning across mechanics, electronics, control, perception, software, and integration. Powered roll, pitch, and yaw head motion, sustained person tracking, and come/follow behaviour are Core. Success does not require spatial hearing, utility beyond the approved time/timer/alarm/Spotify set, or a production-quality industrial design.

## Core acceptance criteria

| ID | Criterion | Proposed pass condition | Evidence |
|---|---|---|---|
| SC-01 | Droid identity | Reviewers recognize M4 as one consistent droid character rather than a group of subsystem demos. | Unedited demonstration and observer responses. |
| SC-02 | Integrated encounter | The approved wake/social and come/follow scenarios run as coherent encounters combining idle, wake, visual attention, spoken input, astromech output, display/status-light expression, head motion, and base motion where applicable. | Unedited video plus timestamped behaviour/event log. |
| SC-03 | Display quality | The onboard face animates continuously during the approved scenarios, remains visually legible, and shows no distracting stalls or transitions that break the character. | Direct-display video and frame/performance log. |
| SC-04 | Three-axis head expression | Powered roll, pitch, and yaw each contribute to attention and authored expression with controlled starts, reversals, coordination, and settling. Motion does not visibly resemble abrupt raw actuator commands. | Repeated behaviour video and per-axis command/state logs. |
| SC-05 | Timing and composition | Display, head, sound, and base actions express the same intent. Their ordering and follow-through feel deliberate rather than simultaneous by accident or disconnected by latency. | Behaviour timeline and observer review. |
| SC-06 | Natural-language understanding | In the defined Core scenarios, different natural phrasings of the approved intents are understood with adequate reliability and response time. Exact intent set, trial count, and threshold remain to be fixed. | Scripted utterance test and event timestamps. |
| SC-07 | Astromech communication | M4 uses the builder-authored sound vocabulary, never relies on ordinary spoken English as its in-character response, and pairs each tested sound with the intended display/motion behaviour. | Vocabulary record and scenario video. |
| SC-08 | Person/face tracking | Under normal household lighting and the approved interaction geometry, Makad acquires the nearby test person, visibly directs attention toward them, and maintains or reacquires the track through the approved motion cases. | Detection/tracking log and external video. |
| SC-09 | Idle aliveness | Without manual control, M4 exhibits bounded variation and remains recognizably alive without constantly moving or becoming distracting. | Timed idle observation and behaviour log. |
| SC-10 | Authored behaviours | At least three distinct behaviours have recognizable intent, a beginning, coordinated execution, and recovery to idle. They run through the behaviour system rather than manual subsystem commands. | Behaviour definitions and repeated trials. |
| SC-11 | Floor locomotion | On the approved indoor floor, M4 performs the defined forward, reverse, turning, and stopping actions without instability or uncontrolled motion. | Marked-course video and motion logs. |
| SC-12 | Obstacle handling | Within the approved speed and sensing envelope, M4 detects representative obstacles and stops or redirects without harmful contact. Exact obstacles, speeds, and clearance threshold remain to be fixed. | Repeated obstacle-course trials. |
| SC-13 | Tabletop protection | In tabletop mode, ordinary autonomous locomotion is inhibited by default. Edge/fall protection prevents the robot from driving off the approved test surface under the defined fault and activation trials. | Tabletop mode and edge-rig test record. |
| SC-14 | Battery operation | The integrated droid completes at least 20 minutes of representative mixed-duty untethered operation and the full Core demonstration without reset, unsafe voltage drop, or thermal failure. | Power/current/voltage log and timed demonstration. |
| SC-15 | Controlled stop and failure | The approved physical stop/power method halts hazardous outputs, and injected loss of required sensing, control, network, or communication causes a bounded state rather than continued uncontrolled movement. | Stop and fault-injection record. |
| SC-16 | Physical robustness | M4 completes repeated demonstrations without loose assemblies, cable interference, overheating, unstable support, or damage. | Inspection checklist, temperature record, and test notes. |
| SC-17 | Serviceability | A named high-risk module can be accessed and replaced without destroying the enclosure or unrelated assemblies. | Service procedure with time and tool list. |
| SC-18 | Reproducibility | A cold start using documented setup instructions reaches the demonstration state without code edits or undocumented intervention. | Startup checklist and consecutive run record. |
| SC-19 | Learning outcome | The final report records measurements, failed assumptions, design changes, and substantive lessons in mechanics, electronics, control, perception, and integration. | Project report and `MEMORY.md`. |
| SC-20 | Scope discipline | Every shipped capability maps to an approved Core, Target, or Candidate. Cutting a Target or Candidate does not invalidate V1. | Final scope review. |
| SC-21 | Named wake and status light | From idle/head-down, each approved name form triggers a wake sequence using head lift, visual attention, display expression, astromech sound, and the camera-side status LED. False-wake tolerance remains to be set. | Wake-word trial matrix, event log, and video. |
| SC-22 | Time, timer, and alarm | Natural requests can display the current time, create a timer, and create an alarm; each produces a legible confirmation and the timer/alarm fires at the correct time. | Scripted functional trials and display/event logs. |
| SC-23 | Spotify and music expression | A natural request starts the intended Spotify playback through the approved integration, and M4 enters and exits a coordinated music-response state using at least its eyes. | Playback trials, integration log, and video. |
| SC-24 | Come and follow | In the approved single-room household envelope, “come here” causes M4 to find and approach the person to the approved stopping band; “follow me” maintains following over the short indoor route and slow walking speed without harmful contact or loss of control. | Marked-route trials, tracking/control logs, and external video. |
| SC-25 | Expressive spin | M4 performs a deliberate excited spin on the approved floor, remains stable and within its validated footprint, and settles without uncontrolled motion. | Marked-floor video and control/state logs. |

## Expressiveness review

“Top notch” expression is a design objective that needs both evidence and human judgment. The review should evaluate:

- whether attention direction is immediately readable;
- whether display animation remains fluid and characterful;
- whether head motion shows anticipation, ease, follow-through, and settling;
- whether audio, display, head, and base communicate the same intent;
- whether system latency looks like deliberate character timing rather than lag;
- whether idle behaviour feels alive without becoming random noise;
- whether M4 retains a recognizable personality across different behaviours.

The final observer protocol and pass threshold must be approved before final tuning so the test is not rewritten to fit the result.

## Minimum Core demonstration

The authoritative scenario flow is defined in `core-interaction-scenarios.md`. At minimum, final validation demonstrates:

1. M4 cold-starts on battery and settles into an idle/head-down state.
2. Each approved name form can initiate the coordinated wake response.
3. M4 acquires the person, responds to a greeting, and performs the approved expressive exchange using powered roll, pitch, and yaw head motion.
4. Time display, timer, alarm, and Spotify playback are demonstrated through natural requests.
5. During music playback, M4 performs its approved visual “vibe” behaviour.
6. On the floor, “come here” causes M4 to find and safely approach the person.
7. “Follow me” causes M4 to track and follow through the approved route.
8. M4 performs an excited spin only inside the validated motion envelope, then returns to a stable state.
9. Obstacle handling, tabletop locomotion inhibition, edge/fall protection, physical stop, and fault behaviour are demonstrated separately.

## Non-Core demonstrations that do not gate V1

- spatial hearing that improves orientation toward a speaker.

Results from these Target or Candidate prototypes should be documented even when the capability is cut.

## What does not prove success by itself

- a face animation running only on a development computer;
- isolated neck, camera, speech, sound, or motor demonstrations;
- English speech output substituted for the authored astromech language;
- a long feature list without a reliable integrated encounter;
- one carefully rescued successful run;
- visual similarity to a concept render;
- completion of every exploratory specsheets requirement;
- success of face-following while Core collision, language, or expressive behaviour remains unreliable.

## Thresholds still requiring decisions or measurement

| ID | Threshold | Decision needed |
|---|---|---|
| SC-TBD-01 | Expressiveness observer review | Sample size, questions, and pass percentage |
| SC-TBD-02 | Repeatability | Required consecutive successful cold-start demonstrations |
| SC-TBD-03 | Display performance | Minimum frame/update rate and permitted stalls |
| SC-TBD-04 | Three-axis head motion quality | Per-axis range, tracking error, reversal quality, cross-axis coupling, settling, noise, and coordination limits after the representative mechanism prototype |
| SC-TBD-05 | Natural-language capability | Required intents, example phrasing diversity, environment, trial count, accuracy, and maximum latency |
| SC-TBD-06 | Visual awareness | Distance range, pose/lighting cases, acquisition time, and success rate |
| SC-TBD-07 | Floor locomotion | Surfaces, speed, slope/threshold tolerance, stopping, and stability limits |
| SC-TBD-08 | Obstacle protection | Obstacle set, approach speeds, test count, contact/clearance policy, and failure trials |
| SC-TBD-09 | Tabletop protection | Surface/edge test geometry, permitted motion, detection coverage, and pass count |
| SC-TBD-10 | Battery | Initial minimum runtime is 20 minutes; decide recharge expectation, reserve, low-battery behaviour, and whether later evidence justifies a longer runtime target |
| SC-TBD-11 | Endurance | Required continuous operating time and duty cycle |
| SC-TBD-12 | Thermal | Maximum permitted component, battery, motor, and enclosure temperatures |
| SC-TBD-13 | Astromech language | Minimum vocabulary, intended meanings, observer comprehension goal, and acoustic-quality bar |
| SC-TBD-14 | Cloud dependency | Service-loss timeout, degradation behaviour, and final-demo connectivity plan |
| SC-TBD-15 | Wake interaction | Accepted aliases, test utterances, false-wake rate, response latency, and retry behaviour |
| SC-TBD-16 | Utility timing | Clock source, timer/alarm timing tolerance, simultaneous-event handling, and cancellation behaviour |
| SC-TBD-17 | Spotify | Supported request types, authentication state, playback-start latency, device/output path, and failure behaviour |
| SC-TBD-18 | Person following | The initial household envelope is defined in `constraints.md`; close exact marked route, tolerances, loss/reacquisition time, obstacle cases, and pass rate after representative prototypes |
| SC-TBD-19 | Status light | Meaning, brightness, colour capability, timing, and camera-image interference limit |

## Open validation decisions

- [ ] Formalize the detailed natural-language intent/phrase set after the scenario semantics are stable.
- [ ] Define the initial astromech vocabulary needed by those behaviours.
- [ ] Set the observer-review and repeatability thresholds before final validation.
- [ ] Set safety, locomotion, tabletop, battery, and thermal thresholds after representative prototypes.

### Review notes

Approved by the project builder on 2026-08-14. Version 1.1 makes powered roll, pitch, and yaw Core and adopts the initial runtime and bounded household-following envelope. Detailed language design and remaining numeric thresholds remain later validation work.
