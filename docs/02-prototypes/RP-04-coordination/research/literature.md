# RP-04 literature (Exa redo)

| Field | Value |
|---|---|
| Status | **Literature pass 2026-09-21.** Grounds the four axes. Does not unwind `RP04-P3/P5-REG-01`. Not G01. Not ADR-05 |
| Owner | Project builder |
| Method | Exa Agent (4 runs) + Exa search subagents (4). Adjacent practice as **mechanism evidence**, not product selection |
| Bound | `BD-07`; [`trigger-comparison.md`](trigger-comparison.md); remaining empirical: [`experiment-spec.md`](experiment-spec.md) |

## Compact statement

> Adjacent show-control, game sequencers, and character-robot systems **support a TIME / PROG / mixed taxonomy**. Makad’s selected adapter is `CS-HYBRID`: a versioned cue list where **each cue names exactly one trigger kind** (`time` or `progress`). That exact-one-trigger rule is Makad’s constraint, not a claim that those systems implement the same architecture. Treat continuous counter-yaw as an executor primitive. Split the unregistered 80–170 ms class into three quantities: authored face/light→head **lead**, same-beat **tolerance**, and engineering **deadline**. A denied optional channel must not stall a required one.

This pass **supports** keeping `CS-HYBRID` and the cue-list representation. It does not shortlist middleware, ROS, or a graph-as-trigger. Family research stays closed.

---

## 0. Scope

| In | Out |
|---|---|
| Four axes from [`plan.md`](../plan.md) §5 / `BD-07` | Product catalogue; ROS 2 as V1 safety path (`CA-07`) |
| Named systems as evidence of a mechanism | Re-spiking TIME/PROG/HYBRID |
| Numeric windows that can become `E` | `W` gates; observer freeze |
| Wait language (any / all / threshold / deadline) | Treating `any()` as a new architecture family |

Coverage is **best-effort**, not exhaustive. Strongest evidence: QLab/MSC, Unity Timeline / Unreal Sequencer, Jibo, Vector, Disney gaze/catch papers, Haru VOM 2024, Sidenmark gaze 2019, ITU-R BT.1359, Chao/Thomaz interruption.

---

## 1. Four axes (filled)

### 1.1 Score representation — cue list, not a graph-by-default

| Mechanism | Evidence | When it fails | Makad |
|---|---|---|---|
| Versioned ordered **cue list** / multi-track timeline | [QLab sequences](https://qlab.app/docs/v4/general/cue-sequences/); [Unreal Event Track](https://docs.unrealengine.com/4.27/en-US/AnimatingObjects/Sequencer/Overview/Tracks/EventTrackOverview/); [Unity Timeline signals](https://docs.unity3d.com/Packages/com.unity.timeline@6.6/manual/wf-signals.html); Vector multi-track `.bin` clips | Arbitrary-order recall (QLab **carts** cannot auto-follow); human seizes the floor (BTs / timed Petri nets) | Keep the list for P-01…P-03 |
| Small **statechart** above clips | [rFSM](https://doi.org/10.6092/joser_2012_03_01_p28): coordination ≠ computation; time events are configurable, not a flowchart | Modelling every continuous value as a node | Open **only** if P-02 *discrete* hand-off needs runtime score mutation ([`experiment-spec.md`](experiment-spec.md) §3) |
| Behavior tree | Unreal BT; Axelsson–Skantze presentation BT | Obscures durable phase ownership | Not required for the three scored performances |
| Parametric **executor primitive** | Unity blend trees; Disney body-yaw ↔ inverse head yaw; Haru VOM | Encoding continuous yaw as discrete cue edges jitters at thresholds. A **graph also cannot fix a slow C0-mediated yaw loop** | Counter-yaw and P-03 body-relative flourish live **here**, not in the score topology. Owner and yaw source: `BD-08` |

QLab: “Timecode is a bit at odds with the fundamental design premise of QLab, which is that you don't necessarily know the amount of time that will elapse between cues.” ([docs](https://qlab.app/docs/v5/networking/using-timecode/)). That is the PROG case. Auto-continue (fire after a wait from *start*, whether or not the first cue finished) is the TIME case. Both exist **on one list**.

**Disagreement, resolved for V1.** rFSM-style coordinators would put AND/OR joins in a graph. QLab/Unreal put them as list waits (auto-follow vs auto-continue; any vs all). Makad keeps **wait language on the list**. Graduate only on the §3 falsifier.

### 1.2 Trigger — TIME / PROG / HYBRID is the right shortlist

| Kind | Named in the wild | Failure | Makad adapter |
|---|---|---|---|
| Scheduled time / timecode / playhead | QLab LTC/MTC chase + 0–2 s freewheel then stop/pause/keep; Unreal Trigger keys; Unity SignalEmitter (`retroactive` if start after marker) | Clock drop, wrong rate, jumps; **scheduled start is not completion** | `CS-TIME` |
| GO / progress / named event | [MSC](http://www.richmondsounddesign.com/docs/midi-show-control-specification.pdf) GO / STOP / TIMED_GO / ALL_OFF; QLab auto-follow; BML sync-points (start/ready/stroke/end); animation notifies | Missing event → hang; blend can double-fire notifies | `CS-PROG` |
| Bounded hybrid (Makad: exactly one trigger per cue) | Systems mix scheduled time with progress/GO/auto-follow on one list (QLab, BML/AsapRealizer, ACE). That **supports the taxonomy**, not an identical product | Unbounded event graph; unnamed dual-trigger cue | `CS-HYBRID`. Exact-one-trigger is **Makad’s** rule |

**Keep HYBRID.** Literature supports mixing authored lead (time) with causal chain (progress). Makad binds that mix as one named trigger per cue. PROG cannot author a face/light lead without becoming HYBRID. TIME still wipes scheduled work on `OX-TIME` (QLab freewheel then stop/pause/keep is the same class). Virtual spike result stands.

MSC **STOP ≠ ALL_OFF** (pause vs panic). ROS 2 actions are cited **only** to name the shared lifecycle (accept/reject, EXECUTING, CANCELING, SUCCEEDED/ABORTED/CANCELED, progress). Not a V1 bus.

### 1.3 Action lifecycle — shared

Canonical chain, independently named:

`goal → accept|deny → start → feedback/progress → succeed|abort|expire`

Sources: [ROS 2 actions design](https://design.ros2.org/articles/actions.html) (mechanism only); Chao & Thomaz atomic acts are **start / keep / stop**, not “run to completion then react” ([JHRI 2012](https://doi.org/10.5898/jhri.1.1.chao)); QLab panic then **second panic = hard stop**.

Cancellation is its own intent. After Chao’s **minimum necessary information**, leftover follow-through implies the robot thinks the beat was not received.

### 1.4 Supervision — shared

| Who | May | Must not |
|---|---|---|
| Composer / SM analogue (`makad-core`) | Allocate epoch, GO the next beat, panic/flush, pick degraded variant | Overrule local stop; invent MCU legality |
| Local executor (C2/C3 analogue of board op / safety PLC) | Accept/deny, NACK stale, stop first on hazard | Choose the next semantic performance |
| Lease / heartbeat | Kill the epoch (`CA-09`) | Resume the old epoch after restart (Operabot: return to start, [MIT](http://hdl.handle.net/1721.1/65324)) |

Jibo [Embodied Speech](https://hri2024.jibo.media.mit.edu/attachments/SDK-SDK---ESML-121023-203758.pdf): concurrent animations **only** on different MetaLayers; same-layer collision **rejects**. Vector: track-ignore flags. QRIO: resource keys; higher-priority modules move lower ones to waiting ([Hoshino 2004](https://web.mit.edu/zoz/Public/ICRA04-Hoshino.pdf)).

---

## 2. Adjacent character systems (evidence, not stack)

| System | What they compose | Scheduling | Gaze / body | Implication |
|---|---|---|---|---|
| **Jibo** | Motors, LED ring, eye graphics, SFX/TTS | Exclusive MetaLayers; look-at + orientation | Face/light as fastest layer | Shared score; same-layer reject |
| **Vector / Cozmo** | Head, lift, treads, face, audio, lights as **one clip** | Keyframed tracks; trigger picks a clip | `TurnToRecordedHeading` is a spin primitive, not world-gaze servo | Multi-track clip + ownership mask |
| **Disney BD-X / gaze / catch** | Eyes, head, torso, face, audio | Layered shows; face blend **Tβ = 0.1 s**, body **Tα = 0.35 s** ([BD-X](https://la.disneyresearch.com/wp-content/uploads/BD_X_paper.pdf)); subsumption fallback “read” show ([gaze](https://la.disneyresearch.com/wp-content/uploads/root.pdf)) | **Joystick primitive:** body yaw counter-rotates head to keep world gaze; torso adds only at **neck limits**. Catch: eyes faster than head than body ([2014](https://la.disneyresearch.com/wp-content/uploads/Playing-Catch-and-Juggling-with-a-Humanoid-Robot-Paper.pdf)) | P-02 counter-yaw is this primitive. Face faster than body |
| **Haru VOM 2024** | Screen pupils + head | Continuous attention→motion | Eyes saccade **25–40 ms** before head; eyes **counter-move** at equal speed during head yaw; VOM window **200–700 ms** ([Fang et al.](https://doi.org/10.1080/01691864.2024.2398556)) | Closest published VOR analogue. 25–40 ms is eye-in-head, **not** Makad’s authored face/light lead |
| **Mobile body–head–eye 2023** | Eyes, head, wheeled base | Allocate by range / cost / stability | Eyes, then head, then **base** when ranges are exceeded ([Sensors](https://doi.org/10.3390/s23146299)) | P-02 hand-off threshold is remaining gaze error vs neck limit |
| **Pepper / NAO** | Speech, gesture, LEDs, (Pepper) head gaze | BML / ALAnimatedSpeech `run`/`start`/`wait` | Referential gaze timed to last syllable; APIs often **cannot** interrupt mid-gesture ([de Kok 2017](https://pub.uni-bielefeld.de/record/2914703)) | Do not wait on speech to certify motion; physical robots pause speech, not the reverse |
| **Furhat** | Face + head + speech (no base) | Gaze **target first**, then head | Interruption: pause/resume vs stop; barge-in can miss the first phonemes ([docs](https://docs.furhat.io/interruptable_speech/)) | Epoch cut is atomic; speech is not mid-resume |
| **Kismet / Leonardo** | Face, gaze, vocalization, (Leo) gesture | Layered drives + motor primitives | Attention owns gaze; not a wheeled counter-yaw result | Separate attention arbitration from motor realization |
| **ATR Robovie** | Gaze, head, utterance, mobile base | Situated modules | Attention-expression couples head toward target with gesture; no published counter-yaw law | Reusable attention units, not wheel-owned timing |
| **Simon / Chao TPN** | Speech, gaze, gesture as **independent resources** | Timed Petri nets; yield **abandons future acts** | Gaze is its own resource | `OX-PREEMPT`: flush future beats, not stitch |

**Takayama, Dooley, Ju ([HRI 2011](https://www.leilatakayama.org/downloads/Takayama.Animation_HRI2011_prepress.pdf), N=273 video):** eyes/head **lead** a considered action; **body first** when surprised. That is P-01/P-02 vs P-03.

**Human gaze–head–trunk.** Unpredictable: eyes → head → trunk ([Hollands 2004](https://doi.org/10.1007/s00221-003-1718-8); [Sidenmark 2019](https://doi.org/10.1145/3361218)). Predictable large/fast redirect: body can lead, world-gaze lock is abandoned mid-turn ([von Laßberg 2014](https://doi.org/10.1371/journal.pone.0095450)). **P-03 must not world-gaze-lock through two revolutions.**

---

## 3. Timing — three `E` quantities, not one

The 80–170 ms class in [`intuition.md`](../../../intuition.md) mixed three different things. Literature will not let them share a number.

| ID | Quantity | Planning `E` | What the literature is | Not |
|---|---|---|---|---|
| `T-LEAD` | Authored face/light **before** head onset | **80–170 ms** (best-supported motor band **80–150**; 170 is the plausible edge) | Eye→head onset lag **150 ms** reactive in-view, **30 ms** predictive beyond-view ([Sidenmark & Gellersen 2019](https://doi.org/10.1145/3361218)); Haru saccade 25–40 ms is a different (faster) effector | AV simultaneity; Disney “anticipation” of a whole action (seconds, no ms) |
| `T-BEAT` | Same-beat **tolerance** around an intended coincidence | **~150 ms** as a generous envelope; tighten toward **~80–100 ms** for a hard transient (flash/hit) | Flash+beep fusion ~**±40 ms** ([Vidal 2017](https://doi.org/10.1371/journal.pone.0172028)); speech TBW ~**203 ms** (−76 audio-lead / +127 visual-lead) ([van Wassenhove 2007](https://doi.org/10.1016/j.neuropsychologia.2006.01.001)); [ITU-R BT.1359](https://www.itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.1359-1-199811-I!!PDF-E.pdf) detectability **+45 / −125 ms**, acceptability **+90 / −185 ms** (audio relative to video) | Authored lead |
| `T-DEAD` | Bounded wait before `OX-DELAY` | **300 ms from that wait’s intended start** — not stacked after `T-BEAT` | Engineering overlay. Independent of same-beat scoring. Past ITU acceptability (−185 ms) as a *perception* bound; this is a hang ceiling. Hoffman functional delays are **task** delays (~200–440 ms), category-error as AV binding | “Still the same beat”; `T-BEAT` + 300 ms |

**Audio.** Phrase shape, not forced sample simultaneity: supported (speech TBW wider and **asymmetric**; visual-lead tolerated more than audio-lead). Uncalibrated display/audio paths already eat **20–150+ ms** before photons/room sound ([Eckhoff 2024](https://doi.org/10.1371/journal.pone.0295817); HMD motion-to-photon **21–42 ms** at onset). G01 must stamp **witnessed** onset, as [`timing-budgets.md`](../timing-budgets.md) already requires.

**Disney/Lasseter** give craft, not ms: zip-off in 3–4 frames; follow-through 2 frames after land ([1987](https://courses.cs.duke.edu/cps124/fall01/resources/p35-lasseter.pdf)). Playback rate unstated — do not back-solve 80–170 from frames.

No retrieved study tests a character robot whose **face/light leads head by exactly 80–170 ms**. Support is triangulated from gaze coupling, not a Makad trial.

---

## 4. Interruption, denial, wait language

Famous failures this architecture is already designed against, now cited:

| Failure | Where it shows up | Overlay |
|---|---|---|
| Stale cue after abort | QLab follow-actions/prewaits keep running unless the **epoch** is killed; SCS SFR must inhibit auto-start | `OX-CANCEL` / `OX-PREEMPT` / `OX-STALE` |
| Wait-forever on missing event | Quadrant `wait` with no timeout; ABL waits on a status WME that never arrives | `OX-TIME` / `OX-DELAY` / deadline |
| False success when a channel is missing | BT **Succeeder** decorator; reporting success from a denied face | `OX-DENY` — deny ≠ complete |
| Snap-cancel | Unity CrossFade vs hard cut; Chao hesitation then interrupt | Fade/hold then new epoch; not a multi-second hang |
| Resume old epoch after restart | Operabot: return to **start** | `OX-RESTART` |

**Wait language (still HYBRID, not a new adapter).** Matches [`experiment-spec.md`](experiment-spec.md) §2.3 and QLab/Quadrant/EDBT practice:

| Form | Use | Do not |
|---|---|---|
| Single named event | Required channel | Unqualified `progress` |
| `any(...)` | Optional visible onset (face **or** light) so `OX-DENY(face)` cannot stall the head | `all` across optional channels |
| `all(...)` | Required conjunction (P-02 body release: C3 accept **and** eligible) | Optional face |
| Named threshold | `progress>=HM-03.rise_commit` | Generic progress |
| Deadline | Then `OX-DELAY` / degrade / proceed as registered | Hang |

QLab: a **disarmed** cue still lets waits elapse, but the action does not run. MSC two-phase: no standing-by within seconds → treat as abort, not success.

Cancel that still reads as one character: wrap at a gesture/word boundary or **≲ 200–720 ms**, then new epoch (dialogue barges; not a face-lead number). No general “looks intentional” cancel-latency for a character robot was found — measure it.

---

## 5. Observer — draft instrument, not freeze

“One reaction or separate devices” is **not** a Godspeed/RoSAS subscale. Adjacent constructs that actually moved:

- **Entitativity / group vs individuals** (outliers split the entity)
- **Fluency / cohesion** (“worked fluently together”, “one shared goal”) — large sync vs async effects
- **2AFC / forced preference** — more discriminating than Likert; keyframed/naive clips get fewer fixations
- **Attention-direction** (shared target vs anti-gaze vs still)

Godspeed likeability/intelligence **ceiling / compliment bias** after a friendly demo. Live > video on presence; **composition timing items can survive on video** when GQS does not. Woods/Walters: video is a surrogate for low-contingency watch; a late “smart” extra clip washes out the IV.

**Keep the draft primary wording.** Freeze questions, N, pass, and clip-selection in `gates.md` **after** engineering tuning on non-scored runs and **before** capturing scored clips. `BD-05` (no household/mock panel) is a **builder** decision, not a literature consequence. Sequence: [`observer-protocol.md`](../observer-protocol.md). Hide engineering LEDs. Counterbalance pair order. Do not use Godspeed as the primary composed-vs-independent endpoint. Video is a valid medium for *composition* timing; it under-reads social presence.

Hoffman & Zhao ([THRI 2020](https://hrc2.io/assets/pdfs/papers/HoffmanZhaoTHRI20.pdf)): freeze wording, exclusions, and analysis before scored recruitment.

---

## 6. What this pass changes

| Item | Before | After this pass |
|---|---|---|
| TIME/PROG/HYBRID shortlist | Virtual spike only | Literature **supports the selected taxonomy**. Exact-one-trigger is Makad’s constraint. Do not add a fourth family |
| Cue list vs graph | Open if P-02 list fails | Same rule. Literature treats counter-yaw as **primitive** (Disney, Haru, blend trees). Wait language stays on the list. Graph cannot fix a slow C0 yaw loop |
| 80–170 ms | One class | Split `T-LEAD` / `T-BEAT` / `T-DEAD` in [`timing-budgets.md`](../timing-budgets.md). `T-DEAD` is 300 ms from the wait’s intended start |
| P-03 world gaze | Already body-relative flourish | Human + Takayama: **abandon** world lock on a deliberate spin |
| Face-deny stall | Already a falsifier | **Adopt** `any(face, light)` + `T-DEAD`. Succeeder/false-success is the named anti-pattern |
| Observer sequence | Conflicting “tune after freeze” vs “never tune after freeze” | Engineering tuning on **non-scored** runs, then freeze, then scored capture. `BD-05` is a builder decision, not a literature finding |

**Does not change.** `RP04-P3-REG-01` / `P5-REG-01`. No ROS. No UART/COBS. No ADR-05. No G03 from paper. TIME/PROG adapters stay in `prototype/`.

---

## 7. Remaining empirical (unchanged owners)

Still [`experiment-spec.md`](experiment-spec.md): **adopted** `any(face, light)` + `T-DEAD` (harness not yet); P-02 cue list on paper; `BD-08` before counter-yaw implementation; physical G01–G05; G03 sequence (tune non-scored → freeze → scored capture).

No published numeric law for wheeled-character head-to-base hand-off thresholds or two-revolution spin gaze policy. Instrument Makad.

---

## 8. Key sources

Show control: [QLab timecode](https://qlab.app/docs/v5/networking/using-timecode/), [cue sequences](https://qlab.app/docs/v4/general/cue-sequences/), [MSC spec](http://www.richmondsounddesign.com/docs/midi-show-control-specification.pdf). Game: [Unreal Event Track](https://docs.unrealengine.com/4.27/en-US/AnimatingObjects/Sequencer/Overview/Tracks/EventTrackOverview/), [Unity signals](https://docs.unity3d.com/Packages/com.unity.timeline@6.6/manual/wf-signals.html). Character: [Jibo ESML](https://hri2024.jibo.media.mit.edu/attachments/SDK-SDK---ESML-121023-203758.pdf), [Vector animation](https://vector.ikkez.de/generated/anki_vector.animation.html), [Disney BD-X](https://la.disneyresearch.com/wp-content/uploads/BD_X_paper.pdf), [Disney gaze](https://la.disneyresearch.com/wp-content/uploads/root.pdf), [Haru VOM](https://doi.org/10.1080/01691864.2024.2398556), [Takayama 2011](https://www.leilatakayama.org/downloads/Takayama.Animation_HRI2011_prepress.pdf), [Chao JHRI 2012](https://doi.org/10.5898/jhri.1.1.chao), [Hoffman & Breazeal TRO 2007](https://doi.org/10.1109/tro.2007.907483). Timing: [Sidenmark 2019](https://doi.org/10.1145/3361218), [van Wassenhove 2007](https://doi.org/10.1016/j.neuropsychologia.2006.01.001), [ITU-R BT.1359](https://www.itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.1359-1-199811-I!!PDF-E.pdf). Observer: [Godspeed](https://doi.org/10.1007/s12369-008-0001-3), [Hoffman & Zhao THRI 2020](https://hrc2.io/assets/pdfs/papers/HoffmanZhaoTHRI20.pdf).
