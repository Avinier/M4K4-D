# RP-01 Intent — Head Motion Vocabulary and Coordination

| Field | Value |
|---|---|
| Status | Draft — user-authored head vocabulary captured; numeric storyboard and eye/audio placeholders remain provisional |
| Owner | Project builder |
| Last updated | 2026-08-27 |
| Physical baseline | `../../01-system/dimensional-baseline.md` — overrides earlier head envelope, ballast, and placement assumptions |
| Numeric storyboard | `storyboard.md` — keyframes, angles, timing, minimum viable and best-case envelopes |
| Feeds | `storyboard.md`, `physics.md`, `gates.md`, RP-01 procedure steps 3–5 |
| Method | Two passes kept separate: authored intent first, then quantified motion hypotheses. See `docs/intuition.md` §5.1 steps 1–2. |

## 1. Purpose and prototype boundary

The head is M4's primary physical instrument for readable attention and character. It must:

- show what M4 is attending to;
- communicate a small set of recognizable intentions and emotions through powered roll, pitch and yaw;
- perform both large expressive moves and small tracking/laugh micro-motions;
- carry the moving camera without making perception unusable;
- interrupt and settle safely;
- later coordinate with the display eyes, camera-side light and astromech audio as one performance.

RP-01 does **not** require working eye animation, status-light animation or astromech audio. It proves the mechanical head and motion firmware. This document nevertheless records provisional eye/audio cues so that head movements are authored with a future composition in mind. During RP-01, those cues may be represented only by timestamps, event markers or a visible timing indicator. Their detailed visual and acoustic design belongs to later implementation and RP-04 coordination work.

The cues below are original Makad design placeholders informed by reference analysis. They do not prescribe copied film animation, copyrighted sound samples, final synthesis, exact waveform, eye artwork or production timing.

### 1.1 Physical boundary inherited by RP-01

RP-01 designs and tests within the current system baseline:

- complete moving head, including ears: **100 H × 180 W × 130 D mm**;
- head core, excluding ears: **~100 H × 140–145 W × 125–130 D mm**;
- active display area: **~95 W × 54 H mm**, behind a **~110–120 W × 60–65 H mm** face opening/bezel;
- ear pods: **~55–65 mm diameter**, protruding **~17–20 mm** per side; no microphones/sensors, while a mechanism candidate may use removable shells to conceal pitch-bearing access carried by an inner yoke/frame;
- three-axis neck allocation: **60 mm vertical**, with only **~35–45 mm** expected to remain externally visible because the mechanism intrudes into the head and body;
- moving-head mass target: **~250 g**;
- one central moving camera; no microphones or speaker in the head;
- preliminary head inertia **~0.001 kg·m²** and preliminary neck peak-torque estimate **~0.2 N·m**, both subject to replacement by CAD mass properties and axis-specific calculations.

These are packaging and load inputs, not permission to treat the preliminary torque estimate as an actuator requirement. `physics.md` must calculate each candidate mechanism, and `gates.md` must register the representative load/configuration before scored runs.

## 2. Accepted intent decisions

1. **Neutral convention:** `roll=0°, pitch=0°, yaw=0°` names the calibrated attentive-forward pose. It is a coordinate convention, not yet a mechanical range or promise that an unpowered actuator holds it.
2. **Powered-off behaviour:** when M4 is truly off, no commanded movement occurs and the mechanism rests safely. Holding neutral while unpowered requires balancing, self-locking transmission, a brake, detent or physical support; it cannot be assumed.
3. **Sleep:** a commanded sleep transition lowers the head slowly over approximately **2–3 seconds** into a sustainable rest pose.
4. **Wake:** the target is to move from sleep/rest to an awake attentive pose within **1 second**, provided RP-01 proves this is possible without objectionable peak load, noise, overshoot, vibration or unsafe motion.
5. **Wake and search are separate semantics:** wake means "M4 is becoming attentive." Search means "M4 is trying to locate a person." A wake may flow immediately into search when no current person track exists.
6. **Search honesty:** a decorative scan may be used as an authored idle flourish, but it must not imply that a person was detected. Actual search ends only on acquisition, cancellation, timeout or failure.
7. **Yes and no:** vigorous pitch nodding communicates yes; vigorous yaw shaking communicates no. "Vigorous" means high character energy inside validated limits, not maximum actuator command.
8. **Laugh:** laughter uses small, quick pitch micro-motions and therefore creates a low-backlash, small-resolution and fast-reversal requirement.
9. **Indian head wobble:** the familiar Indian acknowledgement gesture is a roll-dominant oscillation. A small coupled yaw contribution may be evaluated if it improves readability.
10. **Compound expression:** M4 must be able to nod or shake while holding a curious roll tilt. These are true coordinated multi-axis cases, not a return to neutral followed by a single-axis move.
11. **Restraint:** not every state moves continuously. Stillness, holds and clean settling are part of the performance and preserve emotional range.

## 3. Reference-derived placeholder grammar

### 3.1 Visual/eye grammar

The WALL-E references support a small set of principles rather than a catalog to copy:

- pose **changes and timing** carry as much meaning as static shape;
- limited robot faces depend on restrained changes, clear silhouettes and readable gaze;
- simple graphic eye shapes read more reliably than constant complex animation;
- eye direction shows attention and can prepare the viewer for a head turn;
- a blink/flicker can punctuate the end of one thought and the beginning of another;
- closed upward arcs read as laughter in EVE's visual language;
- narrowed or flatter upper contours can support irritation/anger;
- head-down posture and reduced eye energy support sadness;
- emotional intensity needs range—every reaction must not use the largest eye change.

Makad's provisional eye primitives are therefore:

| Primitive | Placeholder meaning |
|---|---|
| `E-neutral` | Open, calm, symmetric attentive eyes |
| `E-sleep` | Eyes closed or reduced to a quiet sleep mark |
| `E-open` | Eyes expand/resolve from sleep into attention |
| `E-gaze(direction)` | Pupils/eye forms point toward the current attention target |
| `E-wide` | Surprise, alertness or delight; intensity remains bounded |
| `E-narrow` | Focus, irritation or anger depending on posture and timing |
| `E-soft` | Slightly reduced aperture/brightness for sadness or affection |
| `E-laugh` | Repeated closed upward arcs with irregular reopening |
| `E-blink` | Natural punctuation or state transition, not a metronomic loop |
| `E-think` | One deliberate flicker/blink marking a thought boundary |
| `E-lost` | Gaze uncertainty without pretending to have a target |

These names describe semantic cues only. Shape, color, brightness, frame rate and animation curves remain open.

### 3.2 Astromech audio grammar

The R2-D2 research points to a hybrid character voice: machine timbre shaped by human-like performance, intonation and timing. Emotional clarity comes from the contour and rhythm of a short utterance, not from random beeps. Makad should eventually use an original source library and synthesis/processing chain rather than copied R2-D2 recordings.

The placeholder parameters are:

- **register:** low / mid / high;
- **contour:** rising / falling / level / rise-fall / unstable;
- **density:** sparse / conversational / rapid;
- **articulation:** clean / chirped / trilled / rough / buzzy;
- **duration:** impulse / short phrase / long call;
- **spacing:** deliberate pauses and breath-like gaps;
- **intensity:** mild / normal / emphatic, independent of speaker volume;
- **silence:** a meaningful part of startle, sadness, listening and settling.

The provisional acoustic primitives are deliberately descriptive rather than literal samples:

| Primitive | Placeholder character |
|---|---|
| `A-wake-rise` | Short low-to-high boot/wake phrase, resolving rather than alarming |
| `A-query-rise` | Sparse rising whistle/chirp ending openly, used for curiosity or search |
| `A-affirm` | Compact paired phrase with confident upward resolution |
| `A-reject` | Compact clipped phrase with downward or shut-off resolution |
| `A-laugh` | Irregular rapid chirp/trill clusters separated by breath-like gaps |
| `A-happy` | Higher register, varied ascending contour and lively rhythm |
| `A-sad` | Sparse lower-register descending phrase with a longer tail |
| `A-angry` | Clipped, denser, rougher mid/low phrase; controlled rather than simply louder |
| `A-startle` | Sharp high onset or unstable sweep followed by a meaningful silence |
| `A-relief` | Falling tension contour that settles into a soft short chirp |
| `A-confused` | Two-part phrase: uncertain rise, pause, then unresolved short response |
| `A-affection` | Soft, rounded rise-fall phrase with unhurried spacing |
| `A-sleep-fall` | Sparse descending phrase that ends before or as the head reaches rest |
| `A-fail` | Distinct bounded failure motif; never confused with success |

Pitch, tempo and loudness alone will not be treated as an emotion generator. Final utterances must be hand-authored or curated, varied within a recognizable family and observer-tested with their corresponding motion.

## 4. Pass 1 — Authored head moves and coordination placeholders

The head column is binding intent for the next design pass. Eye/audio columns are non-binding coordination placeholders for later implementation. "Sync anchor" records the causal relationship; it is not yet a millisecond timing requirement.

| ID | Move/state | Head intent | Eye placeholder | Audio placeholder | Provisional sync anchor |
|---|---|---|---|---|---|
| `HM-00` | Powered-off rest | No commanded motion; structure reaches a safe unpowered condition without a damaging fall, cable pull or hard-stop impact. | Off | Silent | Power removal dominates every expressive cue. |
| `HM-01` | Neutral attentive | Calibrated forward pose; quiet, available and not rigidly statuesque. | `E-neutral`; occasional non-periodic `E-blink` later | Usually silent | Neutral is a hold, not a loop of compulsory movement. |
| `HM-02` | Sleep | Slow pitch-down transition into a sustainable rest pose; optional very small roll/yaw asymmetry may prevent a dead mechanical look. | `E-sleep` develops during the descent | `A-sleep-fall` | Eyes soften/close during the descent; audio resolves no later than arrival at rest. |
| `HM-03` | Wake rise | Head rises from sleep into attention with deliberate acceleration and a clean settle. It should feel newly alert, not instantaneously switched on. | `E-open`, then `E-neutral` or target gaze | `A-wake-rise` | A small eye/audio cue may lead or overlap motion onset; wake completes before search is declared. |
| `HM-04` | Search sweep | Purposeful yaw sweep with measured pitch contribution; pauses at candidate directions rather than continuously panning like a scanner. | `E-gaze(direction)` leads or travels with each search sector; `E-lost` while unresolved | Sparse `A-query-rise`, not continuous chatter | Gaze indicates the next sector; head follows; acquisition interrupts the sweep immediately. |
| `HM-05` | Acquire and track | Orient decisively to the acquired person, then use small smooth yaw/pitch corrections. Tracking should register as sustained attention, not twitching. | Eyes lock to the target and absorb the smallest corrections where possible | One short acknowledgement or silence | Acquisition cue occurs once; ordinary tracking remains mostly quiet. |
| `HM-06` | Yes | Vigorous, controlled pitch oscillation with readable repetitions and a clean return/settle. | Eyes stay engaged with the person; one blink may punctuate completion | `A-affirm` | Short audio phrase begins with or just before the first decisive nod; do not beep on every reversal. |
| `HM-07` | No | Vigorous, controlled yaw oscillation with readable repetitions and a clean return/settle. | Eyes remain readable; may counter-gaze slightly to preserve person attention | `A-reject` | Audio marks rejection once; head motion carries the repeated emphasis. |
| `HM-08` | Laugh | Low-amplitude quick pitch micro-bursts with slight irregularity and complete recovery; not high-frequency motor chatter. | `E-laugh` arcs pulse in phrases rather than every mechanical cycle | `A-laugh` | Motion clusters follow the audio's phrase/breath structure; both share irregular grouping. |
| `HM-09` | Indian head wobble | Friendly roll-dominant side-to-side oscillation, potentially with a small yaw component, centered on the current attention pose. | Warm attentive eyes; gaze remains on the person | Soft `A-affirm` or `A-affection` depending on context | Sound is optional; gesture must remain readable without it. |
| `HM-10` | Curious tilt | Establish and hold a slight roll tilt, possibly with a small pitch lift, aimed at a speaker or object. Stillness after the tilt communicates processing. | `E-gaze(target)` plus `E-wide` or `E-think` | `A-query-rise` | Gaze identifies the subject first or with head onset; a thought blink may follow the hold. |
| `HM-11A` | Curious yes | Maintain the curious roll bias while performing the pitch-based yes gesture; return to curious hold or attentive neutral. | Curious eye state remains coherent through the nod | Softer `A-affirm` | Compound axes must not visually collapse into an unintended diagonal shake. |
| `HM-11B` | Curious no | Maintain the curious roll bias while performing the yaw-based no gesture; return to curious hold or attentive neutral. | Curious eye state remains coherent through the shake | Softer `A-reject` or `A-confused` | Compound axes must remain legible and clear the physical workspace. |
| `HM-12` | Happy/excited | Brisk lifted pose with a bounded pitch/roll flourish; energetic without using the full startle envelope. | `E-wide` with lively but restrained blink timing | `A-happy` | Eye expansion and rising audio reinforce the lift; hold briefly before settle. |
| `HM-13` | Angry/irritated | Slight forward/down pitch bias, reduced friendly roll, restrained sharp correction or short shake; tension comes from pose and timing, not uncontrolled speed. | `E-narrow`; flatter upper contour later | `A-angry` | A short still hold before/after the phrase gives the clipped motion weight. |
| `HM-14` | Sad | Slow downward pitch, reduced amplitude and energy, with optional small asymmetric roll; no repetitive bobbing. | `E-soft`, lowered gaze or reduced brightness later | `A-sad` | Head and audio descend together or audio trails the droop; allow silence afterward. |
| `HM-15` | Fear/startle | Fast recoil away from the stimulus, then freeze and assess. This is the sharp simultaneous three-axis case, not necessarily the largest single-axis acceleration. | Immediate `E-wide`; gaze returns to the stimulus only during assessment | `A-startle` | Sharp cue/recoil, then intentional silence and stillness before recovery. |
| `HM-16` | Confused/uncertain | Small alternating tilt or incomplete orienting move followed by a hold; must differ from categorical no. | `E-think`, then unresolved gaze | `A-confused` | Pause between the two audio parts aligns with the held uncertain pose. |
| `HM-17` | Affection/warm attention | Gentle small roll toward the person with soft pitch lift and a longer comfortable hold. | `E-soft` while maintaining direct readable gaze | `A-affection` | Sound may arrive after eye contact; no hurried settle. |
| `HM-18` | Safe stop and settle | Interrupt any active phrase, decelerate inside the safe envelope and reach the nearest valid bounded hold. It does not finish stale expressive beats. | Freeze/current safe state, then explicit bounded-state indication later | Silence or `A-fail` only when a user-facing failure must be communicated | Safety interruption pre-empts head, eye and audio choreography. |

## 5. RP-01 mechanical test subset

RP-01 does not need to score every emotional nuance. Its representative motion set must cover the mechanics created by the full vocabulary:

1. `HM-02` sleep — slow gravity-loaded motion and sustainable rest;
2. `HM-03` wake — target one-second rise and controlled settling;
3. `HM-04` search — large usable yaw workspace, reversals and pauses;
4. `HM-05` tracking — smallest intentional corrections and reversal loss;
5. `HM-06`/`HM-07` vigorous yes/no — repeated pitch/yaw reversals;
6. `HM-08` laugh — low-amplitude resolution, backlash and fast micro-reversal;
7. `HM-09` roll wobble — readable powered roll and repeated reversal;
8. `HM-11A`/`HM-11B` curious compound moves — cross-axis loading and coordination away from neutral;
9. `HM-15` startle — provisional peak acceleration and interruption case;
10. `HM-18` safe stop — cancellation from every motion class.

Happy, angry, sad, confused and affectionate performances can initially reuse this mechanical coverage. Their final readability is an authoring and observer-testing question for RP-04, not a reason to add arbitrary RP-01 mechanisms.

## 6. Pass 2 — Quantification

The full panel-by-panel quantification is maintained in `storyboard.md`. This summary prevents the semantic document from becoming a second, drifting numeric source.

| Move | Minimum viable authored motion | Best-case authored motion | Movement profile | Mechanical reason it matters |
|---|---|---|---|---|
| Sleep | Pitch to `+28°` over 3.0 s | Pitch to `+35°` with `R+4°` over 2.4 s | `MS7` descent → `HOLD` | Slow gravity-loaded travel and sustainable rest |
| Wake | `P+28° → 0°` within 1.0 s | `P+35° → P-3° → 0°` within 0.85 s | `MS7` rise + `MJ5` overshoot/settle | Fast rise, reversal/overshoot control and settle |
| Search | Yaw sectors at `±35°` | Yaw sectors at `±50°` | `MJ5` sector turns + `HOLD`s | Usable yaw workspace and cable/camera clearance |
| Track | Intentional 4° correction | Intentional 2–4° correction | Online `TRACK`; `MJ5` test proxy | Small resolution, reversal loss and chatter |
| Yes | Exactly 2 pitch cycles to `+14°/-6°` in 1.0 s | Exactly 2 pitch cycles to `+18°/-8°` in 0.9 s; forward/rebound decay `0.83×/0.63×` | Accented `MJ5` strokes | Pitch speed case and repeated reversal |
| No | Exactly 2 yaw cycles to `±16°` in 1.0 s | Exactly 2 yaw cycles in 0.95 s; extrema `22°, 22°, 18°, 14°` | Declining stitched `MJ5` reversals | Yaw speed/acceleration case |
| Laugh | Two `+4°/-1°` pitch pulses in 0.80 s | Three unequal pulses in a 0.68 s active window plus 0.17 s terminal hold | Irregular `MJ5` pulse train | Pitch acceleration, modal and output lost-motion case |
| Indian head wobble | Pure roll to `±8°` over 1.15 s | Roll to `±12°`, optional `Y±3°`, over 1.08 s | Declining stitched `MJ5` roll wave | Roll speed/acceleration case and rounded reversal |
| Curious | Hold `R+8° P-2°` | Hold `R+12° P-4°` | `MS7` tilt → `HOLD` | Static off-neutral load and readable roll |
| Curious yes | Hold `R+8°`; pitch `-2° → +10° → -5° → -2°` | Hold `R+12°`; pitch `-4° → +12° → -7° → +8° → -4°` | `MJ5` nod in held roll | Roll static gravity load during dynamic pitch motion |
| Curious no | Hold `R+8° P-2°`; yaw to `±13°` | Hold `R+12° P-4°`; yaw `L18° → R18° → L12° → 0°` | Stitched `MJ5` yaw reversals in held roll | Roll static gravity load during dynamic yaw motion |
| Startle | Outbound to `P-10° Y±5° R±4°` in 0.25 s | Outbound to `P-15° Y±8° R±6°` in 0.18 s; return is separate and slower | `MJ5` outbound → `HOLD` → slower `MJ5` | Sharp simultaneous three-axis recoil and freeze |
| Controlled cancel | Proposed settle within 0.5 s where safe | Proposed settle within 0.3 s where safe | Online jerk-limited `BRAKE` | Interruption from an arbitrary current state |

Provisional authored pose envelopes are pitch `-12°…+28°`, yaw `±35°`, roll `±10°` minimum viable; pitch `-18°…+35°`, yaw `±50°`, roll `±14°` best case. Proposed usable mechanism travel adds margin and lives only in `storyboard.md` until gate registration.

## 7. Research basis

### WALL-E/EVE visual performance

- [Victor Navone interview on animating WALL-E](https://animatedviews.com/2008/wall-e-victor-navone-on-wall-e-and-cars-toon/) — limited robot characters rely on subtle changes, timing, pose transitions and clear internal thought progression; EVE's emotional sequence was mapped shot-by-shot through body language and eye shapes.
- [Angus MacLane on WALL-E and EVE's visual language](https://variety.com/2008/digital/news/how-to-build-a-better-robot-1117987668/) — minimal acting, restrained emotional range, EVE's laughing arcs, angry line forms and flicker/blink as thought punctuation.
- [Animation World Network production analysis](https://www.awn.com/animationworld/hello-wall-e-pixar-reaches-stars) — robot movement begins with credible machine function; WALL-E uses constrained mechanical vocabulary while EVE favors smooth arcs and figure-eight-like motion.
- [Pixar's WALL-E production page](https://www.pixar.com/wall-e) — visual storytelling and readable character identity operate with minimal dialogue.

### Astromech and nonverbal robot audio

- [Ben Burtt demonstrates R2-D2 sound design](https://www.youtube.com/watch?v=WBKKXjNf1sE) — the voice combines electronic synthesis with human performance; intonation supplies the character's thought and emotion.
- [Collected Ben Burtt sound-design material](https://www.filmsound.org/starwars/index.htm) — R2-D2's sound uses synthetic and organic sources, while movement texture helps maintain the belief that the character is a machine.
- [R2-D2 Vocalizer research project](https://humancyborgrelations.com/r2d2/) — an unofficial but detailed reverse-engineering reference emphasizing phoneme families, pitch/time variants, emotion-specific sequencing and strict rhythmic relationships rather than random sound selection.
- [Astromech Vocalizer design controls](https://humancyborgrelations.com/astromech/) — useful design dimensions include vocabulary mix, pitch, delivery rate, drawl, processing and personality bias.
- [Study of non-lexical/non-linguistic robot emotion cues](https://dl.acm.org/doi/10.1145/3626185) — synchronized non-speech vocalizations and gestures can improve emotion recognition; happiness and sadness were more reliably recognized than several other tested emotions, reinforcing the need for observer testing and a restrained palette.

### Robot gaze and posture

- [Robot emotion from eye properties, gaze and head posture](https://link.springer.com/article/10.1007/s12369-025-01236-3) — eye cues and head posture interact; head-down postures strongly support sadness, and simple graphic patterns can be more legible than complex ones.
- [Predictive robot-eye gaze study](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2023.1178433/full) — abstract anthropomorphic eyes can efficiently direct human attention, supporting an explicit gaze cue before or during orientation.

## 8. Open authoring questions

- Review the provisional keyframes in `storyboard.md` through simple animation or an acted mock-up; revise them for readability before gate registration, not to make later hardware results pass.
- If reference clips are frame-scrubbed, use them only to challenge amplitude, duration, onset and settle hypotheses—not to reproduce exact copyrighted performances.
- Decide whether M4's displayed eyes can move independently of the camera/head and how much gaze offset remains honest before the head must follow.
- Determine whether the best-case Indian head wobble's small yaw coupling improves readability over the pure-roll minimum after observer comparison.
- Decide whether sleep is an actively held pose or a mechanically supported/unpowered rest target.
- Define search sectors, sweep order, timeout, acquisition interruption and person-loss behavior with the perception prototype.
- Design original Makad audio assets and validate them without motion, with motion, and under mismatched conditions before promoting any placeholder to vocabulary.
- Register all numeric RP-01 motion gates before scored runs; do not tune thresholds after seeing results.
