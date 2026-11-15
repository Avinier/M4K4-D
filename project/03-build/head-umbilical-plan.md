# Head umbilical plan: one loose bundle up the yaw axis replaces the head ribbons

| Field | Value |
|---|---|
| Status | **SELECTED 2026-11-13 as [D-107](decisions.md#d-107), amended the same day to the centre route and to the B0091 camera link.** Study and packaging survey done (§11). PCB-08 rev B and D107 CAD functional corrections are implemented; fabrication remains HOLD, including received geometry, printed strength/proof, thermal/camera tests and the older-register adverse mass sensitivity. Implementation and evidence in [d107-execution.md](final/v1/d107-execution.md). Received-part, camera and wear gates remain open |
| Decision | **[D-107](decisions.md#d-107)**, superseding [D-103](decisions.md#d-103), [D-104](decisions.md#d-104), [D-105](decisions.md#d-105) (including the former copper-ballast amendment; current mass screen retains steel) and the head-cable parts of [D-052](decisions.md#d-052), [D-100](decisions.md#d-100), [D-101](decisions.md#d-101) and [D-102](decisions.md#d-102) |
| Origin | Builder, 2026-11-13: the ribbon, joiner, bracket and trunnion chain is too complicated; proposed a C-shaped tube from the body's rear, above the mushroom button, to the head |
| Evidence marks | `D` documented, `E` estimate, `U` verify on receipt, `W` measured. Every number in this plan is `D` or `E`; nothing is measured |
| Sunk cost | None in parts: every affected BOM row is `NOT_ORDERED`, `HOLD`, `DESIGN` or `CANDIDATE`. The cost is design time already spent on PCB-14, PCB-16 and the D-104/D-105 CAD |
| Camera | The camera stays the locked Raspberry Pi Camera Module 3 Wide, SC0874. This plan changes its **link** only: the Arducam B0091 passive HDMI pair, chosen by the builder after U6248's receiver was found to have no home in the body |
| Revised | 2026-11-13, builder review: camera requirements and an acceptance gate added (§3.5); U6248 replaces the USB camera as the first candidate; the USB camera is a contingency |
| Functional correction | 2026-11-14: broad cradle roots/gusset, captured liner flange, two separately counted150mm ribbons, isolated head-power fills and1.5mm yaw tracks; roll anchor moved; HDMI receipt gate and tape-to-size clamp. [Correction record](final/v1/d107-corrections.md) |
| Revised again | 2026-11-13, after the Level 2 study: the rear hose is withdrawn and §2–§10 are rewritten for the centre route. §11 keeps the study record, including the rear-hose results |

**Umbilical**, as used here: the one bundle that carries every wire between the body and the head and unplugs at one end.

---

## 1. Why change

The path from the body to the head today:

| Item | Count today |
|---|---|
| Flat ribbon cables (three in the yaw cassette, three in the disc channel, W45, W46) | 8 |
| Round wires from PCB-16 through the leg and the hollow trunnion | 13 |
| PCB-14 joiner boards (three in the yaw hub, one on the camera bracket) | 4 |
| PCB-16 junction board on the yaw disc | 1 |
| Ribbon sockets (FH34SRJ; a ribbon socket is a small latch connector that clamps a ribbon's end) | 12 |
| Camera path length, Pi to camera | about 890 mm `E`, against Raspberry Pi's 500 mm guidance |
| Printed and bought parts that exist only to carry cables (cassette stator, hollow trunnion tube and bearing, bracket, two carbon tubes, head clamp, roof guide) | 8 |

Open problems in that design:

- The −Y leg is cut into a box section with 0.8 mm walls for the wire channel; it needs a printed coupon and a load test.
- The 13 wires twist through an 8 mm bore over 4–6 mm of free length; it needs a cycle test.
- The camera ribbon is flexed and twisted in a 140 mm loop behind the head; the official cable is not rated for continuous flexing.
- The camera path is well past the recommended length and has four extra connector pairs; the stream test gates the whole design.
- The bracket puts 19 g high and behind the head and left a 0.5 % tipping margin, bought back with a copper ballast bar.
- The wire split after the trunnion was never finished: `head_harness.py` shows an assumed four-wire / nine-wire split, and the display leads and servo chain are marked as dressing.

---

## 2. What decides the design

The three head axes nearly meet at one point, 80 mm above the yaw disc (world X 16, Y 0, Z 235). Any cable from the body to the head has to follow the head round that point.

- **A cable to the back of the head** sees a span that runs from 72 to 178 mm, because nodding swings the back of the head up and down. It needs a large loose loop that rubs on the head (§11.2). The builder first selected this and withdrew it after the study.
- **A cable up the yaw axis into the head's underside** sees a span of 50–73 mm. On the yaw axis the lower end neither moves nor turns when the head turns, so yaw only twists the cable. This is the selected route.
- **The cost of the centre route** is the short neck gap (34.5 mm at neutral): the spare length folds into bends of about R 10 mm at every pose and with every clamp layout tried (§11.3). Loose fine-strand wires take that; a jacketed cable or a hose does not.

So the design rule is: **in the neck, everything is loose wire.** That includes the camera link, whose cable is stripped to its inner pairs over the neck section.

---

## 3. Design: one loose bundle up the yaw axis

```
 HEAD (roll frame: shell, C2 board, display, camera)
   ┌───────────────────────────────────────────┐
   │ camera ── ribbon ── camera-link board     │
   │ PCB-12 (C2)   display   servo lead        │
   │            clamp on the lower skin        │
   └──────────────── opening ──────────────────┘
                       │   loose bundle, about 95 mm free,
                       │   folds in the 34.5 mm neck gap
   ════════════ yaw disc, Ø21 bore ═════════════
 BODY                  │   down through the hub and rotor
   camera-link board ──┤
   PCB-09 ── W24 ──► PCB-08 rev B (23 mm from the yaw axis)
   head power W13 ──►┘
```

### 3.1 The bundle in the neck

- **Lower end:** a smooth printed bushing with a flared mouth in the yaw disc's bare Ø21 bore; the bushing and rotor liner give a finished **Ø18 passage**. The disc turns with the head; the bundle passes through the bushing and twists inside it.
- **Upper end:** a clamp in the head's roll frame at head-local X −50.4, Y 0, Z 6 (8 mm behind the yaw axis), with the bundle arriving straight up.
- **Free length:** about 95 mm between the two (`E`, from the solver; 10–30 % over the longest span of 73 mm).
- **Shape:** an S-fold in the neck gap. Smallest bend about 10 mm at every pose. Clearance from a 7 mm bundle to the yaw-, pitch- and roll-carried parts: 5.9, 5.9 and 3.4 mm over 45 poses (`E`).
- **Twist:** ±61° of yaw over the free length, about 0.65°/mm at the neck alone. The bundle is also free below the disc down to its body clamp, which roughly halves that.
- **Wire:** fine-strand silicone wire (strands of about 0.08 mm, `E`), each wire free to move. No hose. At most a loose, soft braided sleeve for looks, if it adds no stiffness.
- **Load on the head:** with loose wires the bundle's stiffness is far below the solver's softest case (EI 2 000 N·mm², 0.36 N·m on pitch). A stiff bundle is not acceptable: at EI 8 000 it reaches 1.49 N·m.

### 3.2 Opening and clamp in the head's underside

- The bundle crosses the head's underside within head-local X −56.8…−39.8 and Y −7.2…+5.9 over the envelope. With the bundle's 7 mm and 2 mm of margin the final opening is **34 × 30.2 mm**, centred at head-local(−48.3,−0.7); limits X−65.3…−31.3, Y−15.8…14.4. These supersede the study’s smaller opening.
- The opening cuts **one part: the lower skin** (`main_octagonal_skin_lower`, 1.3 mm thick there). Nothing else lies in it. The pitch frame's underside is 8.7 mm from the clamp point and belongs to another frame.
- The clamp is a printed collar fused to the lower skin round the opening, with a bridge that holds the bundle axis at Z6. It is a droid edit to a head-owned part, like the other D-10x edits.
- From the clamp the leads lie on the skin's floor: PCB-12's plugs are 20 mm forward, the servos are above on the pitch frame.

### 3.3 Below the disc

- The passage already exists: the disc's Ø21 bore, the hub's R13.15 bore and the rotor's R11 core. With the cassette stator removed, the only body part within 14 mm of the yaw axis above the Pi is gone (its floor at Z 120–121). The Pi and cooler top out at Z 111 there.
- The bundle comes down the axis to about Z 114–120 and turns towards −Y to PCB-08, whose near edge is 23 mm from the axis. The corridor is about 8–10 mm tall, between the Pi and the rotor.
- A gusseted body saddle beside PCB-08 takes the pull. The PCB08 cradle has a9.6×18mm web, deep beams and an upper rear-crossrail tie; the saddle has a6.4×9.4mm minimum throat. See the functional load screens and first-print proof conditions in [corrections](final/v1/d107-corrections.md). The bundle is free from that clamp to the head clamp.
- The rotor turns round the bundle. Its ribbon slit and core edges are shielded by an OD21.6/ID18 liner with an OD24.8 flange seated on the rotor top at worldZ137; the flange prevents downward escape. Remove the disc bushing before lifting the liner upward.

The clamp’s hard bore is7.2mm. Two0.25mm silicone pads give a6.7mm soft bore: repack and tape the loose bundle to **6.8±0.05mm** at the clamp (nominal20% pad compression). If the bare bundle exceeds6.85mm, revise the clamp/pads instead of crushing the camera pairs. Actual grip and wear remain physical gates.

### 3.4 What runs in the bundle

Twelve wires (schedule in §11.5) and the camera link's inner conductors:

| Group | Wires | From | To |
|---|---|---|---|
| Servo power | `+6V3_HEAD_PR`, `GND_HEAD`, AWG22 | PCB-08 rev B `J8-9` | First head servo's plug |
| C2 power | `+5V_C2`, `GND_C2`, AWG26 | `J8-9` | PCB-12 `J1-6`, `J1-7` |
| Display power | `+5V_DISPLAY`, `GND_DISPLAY`, AWG26 | `J8-9` | D1 |
| Head link | `GND_SIG`, `C0TX±`, `C2TX±`, AWG28 | PCB-08 rev B `J8-10` | PCB-12 `J1-1…5` |
| Servo data | `SERVO_DATA`, AWG28 | `J8-10` | Servo plug and PCB-12 `J2-2` |
| Camera link | A slim HDMI cable's inner pairs and wires, outer jacket and braid removed over about 120 mm | B0091 board near the Pi | B0091 board near the camera |

**Voltage drop improves.** The ribbon path lost about 0.71 V at 2.4 A before PCB-08 ([D-100](decisions.md#d-100) amendment). AWG22 over about 0.3 m each way loses about 0.08 V (`E`). M2's 6.3 V setpoint was raised to cover the ribbon loss and should be reviewed.

PCB08’s head rail uses a dedicated solid +6V3_HEAD_PR fill on In1 and a separate GND_HEAD fill on In2, with solid pad connections; no shared return plane. Yaw supply and return use1.5mm outer tracks. Specify **at least35µm finished inner copper** to the fab; its usual17.5µm inner foil is not an approved substitution. DRC and resistance screens do not establish operating temperature; N2(b) still measures temperature under load.

### 3.5 Camera and its link

**Installed static ribbons, corrected2026-11-14:** HD-026 is a150mm15-way1.0mm-pitch head ribbon; routed111.20mm plus10mm socket insertion and15mm service allowance leaves13.80mm reserve. HD-027 is a150mm15-way1.0mm to22-way0.5mm Pi5 ribbon (Arducam B0210-class); route59.97mm plus the same25mm allowances leaves65.03mm. The B0091 kit’s60mm15-way ribbon fails even the63.36mm straight head span and is not installed. Verify contact faces/pin mapping and dress unused length clear of nearby parts. These are separate BOM rows, not assumed kit contents.

**What stays fixed.** The camera is the Raspberry Pi Camera Module 3 Wide, SC0874: autofocus, 102° horizontal view, the Pi's native camera pipeline. It is a locked selection in the [camera candidate study](../01-system/camera-candidate-study.md). That study reopens the selection only after a recorded hard failure, and says a failed ribbon "first triggers moving-link redesign". So this plan redesigns the link and keeps the camera.

**What the camera must do.**

| Requirement | Source |
|---|---|
| Ordinary interaction at about 0.3–2.0 m | [CON-19](../00-foundation/constraints.md) |
| "Come here" starts at 1–2 m and stops **0.6–0.9 m** from the person, where the robot settles and attends | CON-19; [core interaction scenarios](../00-foundation/core-interaction-scenarios.md) |
| Following over a route up to about 3 m | CON-19 |
| Face and person detection evidence at 0.6, 0.9, 1, 2 and 3 m | Camera study, shopping criterion 10 |
| About 102° horizontal view, for acquisition with one camera | Camera study |
| Focus held still during head gestures (lens position locked in software) | Camera study |

**The link.** A pair of boards carries the camera signal over a round cable: one board by the camera, one by the Pi. In the neck the cable's outer jacket is removed, so only its thin inner pairs flex. The cable unplugs at both ends and is a wear part.

**Kit, after the packaging survey (§11.7).**

| Kit | Head-side board | Body-side board | Cable in the neck |
|---|---|---|---|
| Arducam U6248 (first selected, dropped on packaging) | Fits: 122 positions for a 25 × 62 × 16 mm board with its jack and plug, under the roof, 56–64 mm from the camera | **No home as shipped.** A 65 × 56 mm board 18 mm or 14 mm thick fits nowhere in the body. With its network jack removed and the cable soldered on, one 7–10 mm slot exists, under the compute tray above the regulators | Four plain twisted pairs: the easiest to strip and flex |
| **Arducam B0091** (passive HDMI pair), **selected** | 25.2 × 27.8 × 12.6 mm (Arducam drawing): fits wherever the U6248 board does | Fits: 88 positions with a straight slim plug, 294 with a right-angle plug | An HDMI cable's pairs are each foil-wrapped: fiddlier to strip, and the foil ages with flexing |

Board sizes for U6248 are estimates from Arducam's photographs; its receiver may differ by a few millimetres, not by the 10 mm the survey would need. **The builder chose B0091 on 2026-11-13.**

**B0091, as it will be used.**
- Two identical boards with a full-size HDMI socket and a 15-way ribbon socket each; no power, no software. Arducam lists Raspberry Pi 5 and the Camera Module 3.
- **Head side:** separate HD-026150mm15-way ribbon from camera to board; static. The included60mm15-way ribbon cannot reach.
- **Body side:** separate HD-027150mm15-to22 Pi5 camera FPC (Arducam B0210-class), static; verify contacts and dress excess.
- **Cable:** a slim HDMI cable, about 0.5 m, plugs at both ends. Over the neck its outer jacket and braid come off; the foil-wrapped pairs and single wires stay whole. A right-angle plug at the body end widens the choice of positions.
- **CAD checked:** both B0091 cradle positions, static routing and separate150mm ribbon reach. **Still unqualified:** the received HDMI plug through finishedØ18; measure housing/latch/boot before closed inserts. The cable can stay in the body when the head comes off by unplugging at the head-side board.

**Camera acceptance gate.** The builder has no test equipment and no sample parts, so there is no bench gate before CAD. The gate runs on the built robot at first power-up, against the same camera on its short supplied ribbon plugged straight into the Pi.

| # | Gate | Method | Pass |
|---|---|---|---|
| C0 | Table check, before assembly | When the parts arrive: camera, kit and stripped cable on the Pi on a table. Watch the picture while bending the stripped section to about 10 mm and twisting it | Picture stays clean. Needs only the parts |
| C1 | Function | Pi 5 with the stock camera setup, camera through the link | Camera detected with no added configuration; autofocus, lens-position lock and HDR respond |
| C2 | **Sharpness at 0.6 and 0.9 m** (also 0.3, 1, 2 and 3 m) | A printed target and a face-size print, by eye or by a sharpness score | No visible loss against the short ribbon |
| C3 | **Acquisition at 0.6 and 0.9 m** (also 1, 2 and 3 m) | The detector chosen for RP-07 (a stock face detector until then) | Detection at RP-07's registered pass rate at every distance |
| C4 | Stream integrity in motion | Streaming while the head runs its full yaw, pitch and roll range and the servos load up | No frame errors or dropped frames beyond the short ribbon's |

If a gate fails, the camera link alone falls back (§10); the twelve wires stay.

### 3.6 Body end: PCB-08 rev B

PCB-08 stays where it is and stays the place where the head's nets meet. Rev A is a draft and was never ordered.

- **Removed:** both ribbon sockets (`J8-6`, `J8-7`) and the +X extension that carries them.
- **Added:** `J8-9`, Micro-Fit 3.0 2×3, the mirror of `J8-1`, for the three power pairs; `J8-10`, JST GH 6, for `GND_SIG`, the two RS-422 pairs and `SERVO_DATA`.
- **Kept:** `J8-1` (head power in), `J8-4` (head link from PCB-09), `J8-8` (yaw servo plug), the yaw power pads, and the D-100 grounding (`GND_SIG` net, R1).
- The camera link does not touch PCB-08.

The board becomes a simpler passive board, a good second lesson board after PCB-14 for the builder's PCB learning.

### 3.7 Head end

- At the clamp the bundle fans out into pre-made leads: a GH7 lead to PCB-12 `J1`, a two-wire lead to the display, the camera pairs to the head-side board, and a three-wire servo lead.
- **Servo chain:** both head servos are on the pitch frame, daisy-chained through their two ports. Three wires (`+6V3`, `GND`, `SERVO_DATA`) cross the roll joint (±21°) in a short free loop near the roll axis.
- **Camera:** the head-side board sits in the roll frame with the camera. A short static ribbon joins them; it never flexes.
- The yaw servo keeps its own 11.1 V supply. Only `SERVO_DATA` and ground link it to the head chain, through PCB-08, as today.

### 3.8 Service

- **Head off:** unplug the bundle's two plugs at PCB-08 and the camera cable at the body-side board, free the body clamp, then lift the head: received plugs must fit the finishedØ18 passage one at a time. This is unqualified until the whole housing/latch/boot is measured. Buy the HDMI cable before printing closed inserts; if it fails, unplug it at the head or redesign/check split inserts to recover the bareØ21 bore. A Micro-Fit 3.0 2×3 housing is about 10 × 7 mm in section (`E`).
- **Bundle or camera cable replacement:** open the head's rear cover, unplug the leads, free the clamp, and draw the bundle down through the opening.

---

## 4. Removed, kept, added

### Removed

| Item | IDs | Where it lives now |
|---|---|---|
| Ribbon cassette stator and all cassette ribbons | BO-059, BO-050 | Body v1 source; removed in the droid CAD |
| PCB-14 joiner boards ×4, their rotor posts | BO-062 | `PCB14_*`, `pcb14_posts()` in `makad-v1.step.py`; `pcb_integration.py` |
| PCB-16 head junction, its screws and disc pockets | CH-111 | `PCB16`, `PCB16_RESERVES` |
| Hollow trunnion tube, plug, 6700-2Z bearing, leg channel, grown boss | D104 replacement geometry (not HD-008/009, which are restored D051 parts) | `D104`, `d104_local()`, droid tables |
| Camera bracket, carbon tubes, head clamp, slotted roof guide, cover slot | HD-018, HD-019, HD-020 | `D105`, `d105_local()`, droid tables |
| Camera loop cable and the static camera ribbon | HD-017, W45, W46 | Harness |
| Ribbons W37, W42, W43 | — | Harness |
| 12 FH34SRJ ribbon sockets | on PCB-08, PCB-14, PCB-16 | Board designs |

### Restored

| Item | Why it comes back |
|---|---|
| D-051 −Y pivot: Ø6 pin, MR106ZZ, retainer and two M2 × 4 screws (HD-008/009/010 restored) | The head's own sources still describe it; removing the D-104 droid edits restores it |
| The solid −Y leg | The channel cut and the fill-backs are droid edits |

### Kept unchanged

- PCB-12 rev A, PCB-09, the yaw stage's bearing, hub, gear, servo and hard stops.
- The yaw rotor (BO-058): it clamps the bearing's inner ring and carries the stop dog. Its core is now the bundle's passage.
- The yaw disc's Ø21 bore. Its ribbon channel is harmless if left.
- The original steel ballast bar (CH-013): current mass/tipping and extra10g camera sensitivity are recorded in [execution](final/v1/d107-execution.md); steel is retained.
- The rear panel, the shell rim and the head's rear cover: nothing is cut there.

### Added

| Item | Proposed ID | Notes |
|---|---|---|
| Bundle W47 (twelve wires, leads, plugs) | W47 (harness), HD-021 | About 350 mm end to end `E` |
| Bore bushing, printed | HD-022 | In the yaw disc's bore, flared both ways |
| Underside collar and split clamp | droid edit to lower skin, clamp bar HD-024 | 34 × 30.2mm opening, centre(-50.4,0,6), two M2×8 plus inserts and soft pads |
| Body clamp beside PCB-08 | BO-069 | Printed, on the frame or the yaw plate |
| Camera link: B0091 pair, two mounts, slim HDMI,150mm15-way head ribbon and150mm15-to22 Pi ribbon | HD-023, HD-026, HD-027, HD-028, BO-070 | Boards 25.2 × 27.8 × 12.6 mm |
| PCB-08 rev B | CH-083 | Same BOM row, new revision |

IDs are proposals; the BOM is checked for the next free numbers when the rows are written.

**Board count:** custom designs drop from 8 (PCB-08, 09, 10, 11, 12, 14, 15, 16) to **6** (PCB-08, 09, 10, 11, 12, 15), and PCB-08 gets simpler.

---

## 5. Decisions

### Decided by the builder (2026-11-13, [D-107](decisions.md#d-107) and its amendments)

| Decision | Outcome |
|---|---|
| Replace the ribbon, joiner, trunnion and bracket path | Yes |
| Route | Centre route. The rear hose was selected first and withdrawn after the study |
| Camera | SC0874 stays; its link is redesigned |
| Testing | No bench test is possible; the camera link is first proved on the built robot |

### Open

None of these blocks PCB-08 rev B or the CAD work.

| # | Question | Recommendation |
|---|---|---|
| K1 | Camera link kit | **Decided 2026-11-13: B0091.** U6248's receiver has no home as shipped |
| K2 | Who drives the PCB-11 status LED (§11.5) | A spare C2 pad on PCB-12, decided before PCB-12 is ordered |
| K3 | D1's power input (§11.5) | Read it off the received display or its schematic |
| Q4 | `SERVO_DATA` joined in the head or at the servo | In the head: three wires cross the roll joint instead of five |
| Q5 | Rotor drum: leave, deburr or sleeve | Sleeve the core with a smooth printed liner |
| Q6 | Ballast: keep copper or return to steel | Decide from the mass check; keep copper if the margin is under 3 % |
| Q9 | Sharpness pass level for gate C2 | Builder sets it with RP-07 |

---

## 6. Impact by project area

### 6.1 Decisions ledger

D-107, its two amendments and the kit choice (B0091) are written.

### 6.2 PCBs ([04-pcbs](04-pcbs/README.md))

- Board register: PCB-14 and PCB-16 marked superseded by D-107, folders kept as the record. PCB-08 rescoped to rev B.
- [workflow.md](04-pcbs/workflow.md) and each board README updated together.
- PCB-08 rev B: schematic, netlist audit, layout, DRC, STEP and a new fit check, following the board workflow and recording each stage.
- PCB-12 rev A: K2 may add one net before it is ordered.

### 6.3 Harness ([05-harness](05-harness/README.md))

- §4.2 wire list: W37, W42, W43, W45, W46 deleted; W47 added with its pin-to-pin table (§11.5).
- §5 pinouts: the PCB-16 pad row removed; PCB-08 rev B connectors added; PCB-12 rows unchanged.
- §6 estimates: the head-rail drop recalculated for wire.
- §7.3 "Head off" rewritten (§3.8 above).
- [csi-chain-tests.md](05-harness/csi-chain-tests.md) marked superseded by the gate in §3.5.

### 6.4 Body

- Body v1 sources stay read-only. In the droid CAD: cassette stator, ribbon reserves and the PCB-08 ribbon-fold reserves removed; body clamp, rotor liner and the body-side camera board with its mount added.
- [02-body/v1/BOM.md](02-body/v1/BOM.md): BO-050, BO-059, BO-062 superseded; BO-069, BO-070 added.

### 6.5 Head

- Head v1 sources stay read-only. In the droid CAD: all D-103, D-104 and D-105 edits removed; the underside opening, collar and clamp, the bore bushing, the lead reserves and the head-side camera board with its mount added.
- [03-head/v1/BOM.md](03-head/v1/BOM.md): HD-017–HD-020 superseded; HD-008, HD-009 and HD-010 restored (the D-051 bearing, solid pin and retainer); HD-021–HD-028 added; the camera row (M005, M006) keeps SC0874 and changes only its cable.
- [Camera candidate study](../01-system/camera-candidate-study.md): the selection is unchanged. Its moving-link section gains B0091 as a record update.
- The head's mass register is hand-kept: the bracket and clamp (19.1 g) go; the collar, bushing and head-side board arrive.

### 6.6 Final CAD ([final/v1/cad](final/v1/README.md))

Edits to `makad-v1.step.py`, all in the droid tables:

| Table | Change |
|---|---|
| `DROID_REMOVES` | Delete the D-104 entries (restores the D-051 pin, bearing, retainer, screws). Add the cassette stator, cassette ribbon labels and the head's `yaw_FFC_x3_*` reserves. Redraw `camera_CSI_exit_and_bend_reserve` for the short ribbon to the head-side board |
| `DROID_INSERTS` | Delete the PCB-16, D-104 and D-105 entries and the four `HARNESS_YAW_FFC_FOLD_*` reserves. Add the bore bushing, the clamp bridge, the body clamp, the rotor liner, the bundle at neutral with its swept-envelope reserve, the lead reserves and both camera-link boards with plugs |
| `DROID_CUTS` | Keep renamed cuts that remove the source-integral PCB-14 posts; delete the PCB-16 pockets, the D-104 leg and boss cuts, the D-105 cover slot and disc pockets. Add the underside opening in the lower skin |
| `DROID_ADDS` | Delete the PCB-14 posts and the D-104 leg fills and boss. Add the collar on the lower skin |
| `DROID_MOVES` | Delete the PCB-14 joiner moves |
| `CUSTOM_PCBS` and `pcb_integration.py` | Drop the PCB-14 and PCB-16 groups; install the PCB-08 rev B STEP |

Other files:

- `head_harness.py` rewritten to draw the bundle and its leads.
- New `check_d107_neck.py` (§8).
- Study scripts, kept: `study_umbilical_geometry.py`, `study_umbilical_span.py`, `study_umbilical_homes.py`.
- Retired, kept in git history: `check_pcb14_fit.py`, `check_pcb16_fit.py`, `check_d104_head_routes.py`, `check_d105_csi_loop.py`, `check_pcb08_zif_envelopes.py`, `check_pcb08_zif_stepped.py`, `check_pcb08_ffc_fold.py`, `ribbon_elastica.py`. The mass-and-tipping block of `check_d105_csi_loop.py` moves into the new check.
- Kept: `check_pcb12_fit.py`, `check_pcb08_servo_plug.py`, `check_yaw_stage.py` (body v1), `study_head_cable_passage.py`.

### 6.7 BOM ([BOM.csv](BOM.csv))

Rows superseded, restored and added as in §4. Other sessions edit the BOM concurrently, so each write re-reads the file first. None of these parts has been ordered.

### 6.8 Print ([04-print](../04-print/README.md), [printguide.md](final/v1/printguide.md))

The lower skin gains an opening and a collar. New small prints: bore bushing, clamp bar, body clamp, rotor liner, two board mounts. One print removed (bracket). The −Y leg returns to its solid form, so its coupon test is no longer needed. Nothing is printed yet.

### 6.9 Software ([firmware-requirements.md](04-software/firmware-requirements.md))

No change: the camera stays on the Pi's native pipeline, and Arducam documents B0091 as needing no configuration; gate C1 confirms it.

### 6.10 Other documents

[README.md](README.md), [TODO.md](TODO.md), [final/v1/README.md](final/v1/README.md), [simplification-plan.md](simplification-plan.md) §2 (board count) and the session memory notes for PCB-14, PCB-12, D-104 and D-105.

---

## 7. Levels of work

| Level | Work | State |
|---|---|---|
| **0. Decide** | D-107 and its amendments | Done |
| **1. Paper** | Camera link facts, wire schedule (§11.4, §11.5) | Done, except K2 and K3 |
| **2. Study** | Route study (§11.2, §11.3) and packaging survey (§11.7) | Done |
| **3. Electrical** | PCB-08 rev B work package below; PCB-12 rev A re-audited against the W47 schedule and K2 | **Done2026-11-14**; final evidence in execution record |
| **4. CAD** | D-107 CAD work package below, including the droid-table edits in §6.6 and `check_d107_neck.py` | **Done2026-11-14** with rev B STEP; physical acceptance open |
| **5. Mass** | Mass and tipping with the bracket gone; Q6 ballast | **Done**: steel retained; current sweep, original register calculation and extra10g camera sensitivity in execution record |
| **6. Records** | BOM, board/harness/subsystem records, READMEs, print guide, TODO; retired checks removed | **Done**; durable execution record replaces session notes |
| **7. First power-up** | Table check C0 when the parts arrive; gates C1–C4 and the tests in §8 on the built robot | Waits for parts and the build |

### Next work package: PCB-08 rev B (Level 3)

1. Start from the un-ordered PCB-08 rev A design. Remove `J8-6` and `J8-7`, their ribbon-only routing and the board extension that carried them. Keep `J8-1`, `J8-4`, `J8-8`, the yaw-power pads and D-100's `GND_SIG`/R1 grounding.
2. Add `J8-9` (Micro-Fit 3.0 2×3) for the three head-power pairs and `J8-10` (JST GH 6) for `GND_SIG`, `C0TX±`, `C2TX±` and `SERVO_DATA`, using the pin-to-pin W47 schedule in §11.5. Audit the ground separation, current path, connector orientation and mating access against the actual head and body runs. The camera link bypasses this board.
3. Finish the schematic, netlist and pin-map audit, layout, ERC/DRC, fab outputs and STEP under the PCB workflow. Update the PCB-08 board record to describe rev B. Do not order the board on the strength of a CAD fit alone; retain its existing release gates and add any new connector or harness checks the revision requires.
4. Fit the rev B STEP in the final assembly and run a targeted check for mounting, service access, `J8-9`/`J8-10` plug envelopes, and the path from the yaw axis to the body clamp. Re-audit PCB-12's interface to W47 without redesigning PCB-12 for unrelated work.

**Level 3 done when:** the rev B electrical files and STEP agree on connector names, pin order and orientation; ERC/DRC and the net-map audit pass; the targeted assembly fit passes; and the remaining release holds are recorded. A fabricated or bench-proven board is a later gate.

### Next work package: D-107 CAD edits (Level 4)

1. In the final droid assembly, remove the obsolete cassette ribbons and stator, PCB-14 and PCB-16 and their mounts and pockets, the D-104 hollow trunnion and leg channel, and the D-105 camera bracket, tubes, rear-cover clamp and long ribbon reserves. Restore the D-051 pitch pivot and solid −Y leg. Keep the yaw bearing, drive, stops and the D-105 copper-ballast amendment until Level 5 resolves the mass.
2. Model the centre route in the droid-owned geometry: the lower-skin opening and collar, yaw-disc bushing, smooth rotor liner, body and head clamps, the W47 loose-wire bundle and its swept reserve, the roll-crossing servo leads, and both B0091 boards with mounts, plugs and short static ribbons. Use §3 and the table in §6.6 as the geometry and ownership specification. Keep the body-v1 and head-v1 source models read-only.
3. Rewrite `head_harness.py` for the new run and add `check_d107_neck.py`. Check the full yaw, pitch and roll hard-stop envelope for clearances, bend and twist allowance, passage through the bore, clamp access, camera-board packaging and removal of old geometry. Use §8 for the pass criteria and targeted existing checks for affected interfaces.
4. Use the PCB-08 rev B STEP once available for the final board-and-plug fit. The CAD model can start with the documented connector envelopes; its Level 4 fit gate waits for the actual rev B STEP. Then perform Level 5 mass and tipping before changing the ballast.

**Level 4 done when:** the final assembly contains one centre-route bundle and the two B0091 boards, none of the superseded head-cable geometry, a passing D-107 neck check and targeted integration checks, and a documented list of geometry assumptions that still need physical validation. Camera signal and cable life remain subject to C0–C4.

**Study re-run:** finished and reconciled with §11 on 2026-11-13. `study_umbilical_span.py --record` reproduced every rear-loop and centre-route figure quoted there; two descriptive figures were corrected (body clearance 11–24 mm; sixteen clamp cases, R 6.5–12.0 mm). No route conclusion changed.

---

## 8. Checks and tests

### CAD check: `check_d107_neck.py`

| Check | Pass |
|---|---|
| Bundle length margin at the longest span | ≥ 10 % |
| Bundle clear of the yaw-, pitch- and roll-carried parts over the pitch × roll grid to the hard stops | ≥ 3 mm |
| Underside opening | Cuts the lower skin only; bundle stays inside it with 2 mm margin over the envelope |
| Collar and clamp bridge | Fused to the lower skin; clear of the pitch frame over roll ±21° |
| Bore passage | Bushing seated in the disc bore; Ø18 clear through hub and rotor liner; cassette stator gone; nothing else within 12 mm of the axis above the Pi |
| Body run | From the axis to the body clamp and PCB-08 rev B's plugs, with plug envelopes, clear of the Pi, cooler and rotor |
| Plugs through the bore | Received full housing/latch/boot fits finishedØ18; unqualified until measured. BareØ21 requires removal/redesign of inserts |
| Camera-link boards | Seated on their mounts with plugs and ribbons; head-side board clear over the envelope |
| Internal leads | Clamp to PCB-12, display and the head-side board; roll-crossing lead clear over the envelope |
| D-051 pivot restored | Pin, bearing and retainer present; leg solid; nothing left in the old channel |
| Mass and tipping | Margin ≥ 1.5 % at the worst yaw |

### At first power-up

| Test | Method | Pass |
|---|---|---|
| Camera gates C1–C4 | §3.5 | §3.5 |
| Head link | C0 and C2 exchange frames while the head runs its full range | No link errors |
| Servo bus | All three servos answer while the head moves | No timeouts |
| Rail at the servos | If a meter is available: head rail at the servo plug under load | ≥ 5.23 V (N2 target) |
| Wear look | After the first hour of motion: look at the bundle at the bushing and the clamp | No abrasion, no broken strand |

---

## 9. Risks

| # | Risk | Likelihood | Response |
|---|---|---|---|
| R1 | The camera picture breaks up through the stripped, flexing section | Unknown: untested | Table check C0 before assembly; gate C4; fallback F1. The cable is a wear part |
| R2 | The camera-link conductors fatigue at R 10 mm | Medium over months | Cheap, plug-in cable; replace when frames drop; fine-strand cable preferred |
| R3 | Wires fatigue at R 10 mm | Low to medium | Fine-strand silicone wire; inspect after the first hour; the bundle is replaceable |
| R4 | The stripped HDMI section is fragile: foil wraps tear, thin conductors break | Medium | Strain-relieve both ends of the stripped section; keep a spare cable; fallback F1 |
| R5 | The bundle rubs at the bore or the opening edge | Medium | Flared bushing and a rounded collar; wear look after the first hour |
| R6 | The bundle snags on a leg or the head's underside at an extreme pose | Low | 3.4 mm worst clearance in the study; the CAD check repeats it with the real parts |
| R7 | The collar on a 1.3 mm skin is weak | Medium | The collar spreads the load; the body clamp, not the head clamp, takes pulls from below |
| R8 | The camera pairs pick up servo noise beside the power wires | Medium | Twist the power pair; keep the camera pairs on the far side of the bundle; gate C4 |
| R9 | Head removal is fiddly: plugs through the bore | Low | Small plugs; documented order in §3.8 |

---

## 10. Fallbacks

- **F1, camera link only:** a longer cable in a loop behind the head. It needs a notch in the rear panel and a hole in the rear cover (both surveyed in §11.1), cut after printing. The twelve wires stay on the centre route.
- **F2, camera link only:** the ribbon cassette and the D-105 loop, as designed before D-107. It brings back PCB-14 and the bracket for the camera alone.
- **F3, kit:** U6248, with its receiver's jack removed and the board in the slot under the compute tray (§11.7).

---

## 11. Level 1 and 2 results (2026-11-13)

Read-only work; no CAD geometry, board or BOM file changed. Scripts: `final/v1/cad/study_umbilical_geometry.py` (head and body surface samples, exit and rear-cover ray profiles; report `study_umbilical_geometry-report.json`) and `final/v1/cad/study_umbilical_span.py` (hose solver: a bending rod of fixed length clamped in position and direction at both ends, own weight, soft contact against the sampled parts; checked against clamped-beam sag and a finite-difference gradient). Every number below is `E`: stiffness and weight are assumed, contact has no friction, the clamps are points. The solver's cases are saved in `study_umbilical_span-report.json` (`rear_record`, `neck`, `neck_clamp_record`) and re-run with `--record` (about 50 min).

### 11.1 Body exit and head entry (survey)

- **Body exit.** At the rear centre the gap between the mushroom bezel (top Z 126.5) and the panel's top edge is 5.5 mm. At Y ±18 to ±24 the rear panel's top band (Z 118–134) has nothing behind it but the shell wall at X −46 and the frame's rear rail from X −36. So exit B (off-centre panel notch) needs a notch in the panel only, and the **−Y side (Y −18)** gives a direct run under the rail to PCB-08 (X −22…10, Y −44…−23, Z 112). Exit C (deck corner) is 2.4 mm of shell over the frame's rear rail. Exit A cuts the shell rim, the frame bar and passes the yaw flange screw at X −24.
- **Head entry.** Behind the rear cover (inner face X −110.9), over roll 0, ±10.5° and ±21°:
  - above the roll servo, Z 72–82 across Y −21…+19: nothing between the cover and the head interior (the cover is 1.6 mm);
  - beside the servo, |Y| 13–21 from Z 26 to 70: a 20 mm deep pocket to the pitch saddle;
  - on the servo's own band (|Y| ≤ 7, Z 26–62): the servo case touches the cover. No entry there.

### 11.2 Rear loop (first selected, now withdrawn): it does not close as estimated

The span from exit A to the rear cover's top entry over the hard-stop envelope is **72–178 mm**, not the 108 ± 30 mm this plan's first estimate implied, and pitch drives it more than yaw: at yaw 0 alone it is 73–165 mm. Mid and low entries shorten the neutral span but widen the range (41–168 and 27–163 mm).

Solved on 60 poses (yaw −61…61, pitch −25…43, roll −21…21), exit A, top entry, hose leaving the cuff straight back:

| Free length | EI (N·mm²) | Smallest bend radius | Neutral loop | Sideways sweep | Highest point | Yaw torque, worst | Rests on the head |
|---|---|---|---|---|---|---|---|
| 205 mm (+15 %) | 3 000 | **10 mm** (yaw 61, pitch 43, roll 21) | 83 mm behind the exit | ±106 mm | Z 325 | 0.23 N·m | yes, at the envelope corners |
| 205 mm | 12 000 | 10 mm | 83 mm | ±106 mm | Z 325 | **1.08 N·m** | yes |
| 235 mm (+30 %) | 3 000 | 23 mm | 88 mm | ±116 mm | Z 330 | 0.08 N·m | yes |
| 235 mm | 12 000 | 23 mm | 87 mm | ±115 mm | Z 330 | 0.31 N·m | yes |

(Body clearance stays 11–24 mm in every case. "Rests on the head" means the contact term held the hose on the rear cover or the pitch parts at some poses. The head's top is about Z 294 at neutral.)

What this means:
1. **Length.** The first draft's rule of 10 % over the longest span is not enough: the hose kinks (R 4–10 mm) and pulls hard at the corner pose. It needs about 30 % slack, about 235 mm.
2. **Stiffness.** Only a soft hose meets the yaw-torque target: at EI 3 000 it is 0.08 N·m against the first draft's 0.05 N·m budget (a sixth of the assumed 0.30 N·m yaw ceiling); at 12 000 it is 0.31 N·m, the whole assumed yaw ceiling. Corrugated conduit (EI likely well over 12 000, `E`) is out; braided sleeve with loose wires is the candidate.
3. **Looks and envelope.** The loop stands 85–90 mm behind the exit at neutral, sweeps ±115 mm sideways at full yaw and rises about 35 mm above the head's top at chin-down. It lies on the head's rear at the envelope corners, so it rubs.
4. **Camera cable.** A 23 mm minimum bend is about 6× a 3.6 mm network cable's diameter: acceptable for occasional bending, short of the 7.5–10× usually asked for continuous flexing (`E`, generic guidance, no datasheet for the chosen cable).

Other cuff set-ups, EI 3 000:

| Set-up | Free length | Smallest bend | Neutral loop | Highest point | Yaw torque | Rests on the head |
|---|---|---|---|---|---|---|
| Top entry, cuff heading 30° up | 205 mm | 18 mm | 73 mm | Z 316 | 0.14 N·m | yes |
| Top entry, cuff heading 30° up | 230 mm | 26 mm | 77 mm | Z 318 | 0.10 N·m | yes |
| Mid entry (Y −16, Z 48), heading 60° up | 190 mm | 21 mm | 60 mm | Z 294 | 0.13 N·m | yes |
| Mid entry, heading 60° up | 215 mm | 24 mm | 67 mm | Z 294 | 0.16 N·m | yes |

The mid entry keeps the loop below the head's top but loads yaw more. No set-up tried met the 0.05 N·m budget, and every one lay on the head somewhere in the envelope. The 90°-up cuff, exits B and C and the full 585-pose grid were not run.

Picture: `final/v1/cad/snapshots/umbilical-loop-A-top-h+0-t0-L235.png` (235 mm, EI 3 000) at neutral, chin up, chin down, yaw 61°, yaw 61° with chin down, and yaw −61° with chin up. At chin-down the cuff end rises above the robot; at yaw −61° with chin up the spare length curls beside the head.

### 11.3 Centre route (selected): compact, but tight bends

The bundle rises from the yaw disc's bore (on the yaw axis), crosses the 34.5 mm neck gap and enters the head through an opening in its underside, clamped in the roll frame at head-local Z 13, just under the pitch frame (Z 16.8). On the yaw axis the lower end neither moves nor turns, so **yaw only twists the bundle**; the span depends on pitch and roll only: **50–73 mm**.

Solved on 45 poses (pitch × roll to the hard stops), 7 mm bundle, clamp 8 mm behind the yaw axis, 95 mm free length; picture `final/v1/cad/snapshots/umbilical-neck-dx-8-L95.png`:

| EI (N·mm²) | Smallest bend radius | Clearance to yaw / pitch / roll parts | Sideways reach | Pitch torque, worst | Yaw torque |
|---|---|---|---|---|---|
| 2 000 | **10 mm** | 5.9 / 5.9 / 3.4 mm | 44 mm | 0.36 N·m | twist only |
| 8 000 | 10 mm | 5.9 / 5.9 / 3.6 mm | 44 mm | 1.49 N·m | twist only |

- **Opening in the head's underside:** the bundle crosses the skin within head-local X −14…+3 of the yaw axis and Y −7…+6, so about **24 × 20 mm** with margin. The skin and the pitch frame's underside are head-owned parts, cut as droid edits.
- **Twist:** ±61° of yaw over 95 mm is about 0.65°/mm. Loose silicone wires take it; a jacketed camera cable twisting ±61° per cycle needs its own test.
- **Bends:** the excess length folds into an S in the neck gap with R about 10 mm at every pose and every length tried (75–95 mm, clamp 8 mm either side of the axis). That is fine for loose AWG22–28 silicone wires and too tight for a network or HDMI cable in continuous flexing.
- **Other clamp arrangements do not help.** Sixteen more cases with the head clamp 20–30 mm forward, aft or to the side of the yaw axis and the bundle entering horizontally gave R 6.5–12.0 mm and wider span ranges (34–91 mm). The tight bend comes from the short neck gap, not from the clamp layout.
- **Below the disc:** the bundle continues down the Ø21 bore through the hub into the body, where it can take the yaw twist over a longer free length. That part is not modelled.
- **Pitch load:** the short, bent bundle pushes on the head. Against the STS3045M's 4.4 N·m stall rating (about 45 kg·cm, `E`), 0.36 N·m at EI 2 000 is 8 %, while 1.49 N·m at EI 8 000 is a third. The bundle must be loose wires, not a jacketed cable or a hose.
- **Visibility:** the bundle shows in the neck gap, under the head; nothing shows behind the robot.

### 11.4 Camera link (Level 1a, from Arducam's documentation and photos)

- **U6248 receiver is a Pi HAT.** Arducam's assembly drawing shows the receiver (UC-892) the size of the Pi, on four M2.5 × 11 spacers over it, with a 2 × 3 socket on the Pi's header pins 1–6 (3.3 V, 5 V, I²C, 5 V, I²C, GND). In Makad that space holds PCB-09 on the header (C0 2 × 20 socket and strip) and the yaw servo above. So the receiver needs a new home off the Pi, with flying leads for power and whatever it takes from pins 1–6. Which of those pins it uses is not documented (`U`).
- **U6248 transmitter.** UC-891: the camera bolts to it on four M2 × 7 spacers, a short ribbon loops from the camera to the board, and the jack is on the top edge. One reseller gives 25 × 38 mm (`U`). It is a stack about 20 mm deep with the camera, behind the crown's camera seat; the crown is 40 mm wide.
- **Arducam's passive HDMI pair (B0091):** two identical 25.20 × 27.83 mm boards, 12.62 mm deep with the HDMI jack (Arducam mechanical drawing, `D`). No power and no software. Arducam lists Raspberry Pi 5 and the Camera Module 3 ("V3") as supported, up to 3–5 m. It keeps SC0874 and the Pi pipeline like U6248, with no HAT to rehome. Its cable would be a slim HDMI lead (standard ones are about 7 mm, `E`). See K1 in §5.
- **Kit prices.** Robu lists a U6248 at ₹4,829–4,899 but one cached page showed it out of stock (stale, `U`); Fab.to.Lab lists it in stock.

### 11.5 W47 wire schedule (Level 1c draft)

Body end on PCB-08 rev B (new `J8-9` Micro-Fit 3.0 2 × 3 for power, new `J8-10` GH6 for signals); head end on pre-made leads in the roll frame.

| # | Net | Wire (`E`) | Body pin | Head end |
|---|---|---|---|---|
| 1 | `+6V3_HEAD_PR` | AWG22 silicone | `J8-9.1` | Servo lead pin 2 (5264: 1 GND, 2 V+, 3 data, as `J8-8`; verify on the received STS3045M) |
| 2 | `+5V_C2` | AWG26 | `J8-9.2` | PCB-12 `J1-6` |
| 3 | `+5V_DISPLAY` | AWG26 | `J8-9.3` | D1 power + |
| 4 | `GND_HEAD` | AWG22 silicone | `J8-9.4` | Servo lead pin 1; branch AWG28 to PCB-12 `J2-1` |
| 5 | `GND_C2` | AWG26 | `J8-9.5` | PCB-12 `J1-7` |
| 6 | `GND_DISPLAY` | AWG26 | `J8-9.6` | D1 power − |
| 7 | `GND_SIG` | AWG28 | `J8-10.1` | PCB-12 `J1-1` |
| 8, 9 | `C0TX+`, `C0TX−` | AWG28 pair | `J8-10.2`, `.3` | PCB-12 `J1-2`, `J1-3` |
| 10, 11 | `C2TX−`, `C2TX+` | AWG28 pair | `J8-10.4`, `.5` | PCB-12 `J1-4`, `J1-5` |
| 12 | `SERVO_DATA` | AWG28 | `J8-10.6` | Servo lead pin 3; branch to PCB-12 `J2-2` (joined in the head, Q4) |
| — | Camera link | per §3.5 | Receiver | Transmitter |

`J8-9` mirrors `J8-1`, so PCB-08 rev B is a straight pass-through for power. `J8-10`'s order follows `J8-4` plus `SERVO_DATA`. Three wires (1, 4, 12) cross the roll joint to the servos on the pitch frame.

**Gaps found, outside the bundle:**
- **PCB-11 status LED has no driver.** Its pads take +3V3, GND and DIN, but PCB-12 rev A assigns no GPIO to it (its table uses GPIO 1, 2, 4–9 only). Either a spare C2 pad or D1 must drive it; a head-internal wire.
- **D1's power input** (connector or pads on the Waveshare ESP32-S3-LCD-4.3) is not recorded anywhere in the build folder.
- **Servo plug pin order** is assumed from `J8-8`; verify on the received servos.

### 11.6 Route decision

The builder chose the centre route for everything on 2026-11-13 ([D-107](decisions.md#d-107), second amendment), with the camera cable stripped to loose pairs in the neck and no bench test before the build. The options weighed were: (a) the rear loop, (b) the centre route, (c) wires by the centre and the camera cable by a rear loop, (d) limiting the envelope's corner in firmware. Option (c) was dropped because a single thin cable in a 235 mm rear loop is too limp to hold a shape and would hang onto the rear panel unless sleeved.

### 11.7 Packaging survey for the centre route

`final/v1/cad/study_umbilical_homes.py`, report `study_umbilical_homes-report.json`. Parts are sampled on their surfaces with their labels; a slab is free when no sample lies in it on a 2 mm grid and it is enclosed by parts on at least five of six sides. Body candidates are then checked with exact booleans. Board sizes for U6248 are estimates from Arducam's photographs (`E`).

- **Yaw-axis column.** Within 14 mm of the yaw axis from Z 90 to 160 the body has three parts: the Pi (top Z 111.1 there), its cooler (Z 108.3) and the cassette stator's floor (Z 120–121, removed by D-107). The hub and rotor are bored through. So the bundle has a clear way down to about Z 112.
- **Axis to PCB-08.** PCB-08 (X −22…10, Y −44…−23, Z 112–113.6) is 23 mm from the axis. Its `J8-4` and `J8-8` plugs stand to Z 121–126 at Y −43…−24; the frame's rail is above Z 126.
- **Head underside.** Round the opening there are two parts: the lower skin (Z 0–1.3) and the pitch frame's underside (Z 16.9–24, 8.7 mm from the clamp point). The opening cuts the lower skin only.
- **Head-side board (roll frame, free over roll ±21° against the pitch parts and over the envelope against the yaw parts).**
  - U6248 transmitter with jack and mated plug, 25 × 62 × 16 mm: 122 positions lying flat under the roof at head-local X −71…−63, Y ±13, Z 73–77, 56–64 mm from the camera, 10–12 mm of clearance at the centre. Also 45 positions on edge at Y −29.
  - With the jack removed (25 × 40 × 6 mm): thousands of positions.
- **Body-side board.**
  - U6248 receiver with jack and mated plug, 65 × 56 × 18 mm: **no position** anywhere in the body or chassis. None at 60 × 56 × 18 or at 65 × 56 × 14 either.
  - At 65 × 56 × 10 mm: 6 positions; with the jack removed (65 × 56 × 7 mm): 30 positions, all in one slot at Z 79–81, X 33–53, Y −13…+3, between the compute tray and the regulator modules. Exact check: no clash with a 1 mm shrink.
  - B0091 board with a straight slim HDMI plug, 26 × 70 × 13 mm: 88 positions, for example at X 53, Y −13, Z 119, 28 mm from the Pi's centre. With a right-angle plug, 26 × 45 × 16 mm: 294 positions, including behind the rear panel at X −33, Y 35, Z 103.
- **Not covered.** The cassette stator is still in the body model, so space it frees is not counted. The rotating hub and rotor are not in either model the survey reads. Cable runs to the boards are not drawn.


## Sources

- [Arducam Ethernet Extension Kit documentation (U6248: Pi 5 and Camera Module 3 support)](https://docs.arducam.com/Camera-Extension-Solution/Ethernet-Extension-Kit/)
- [Arducam U6248 at Fab.to.Lab](https://www.fabtolab.com/arducam-u6248-cable-extension-kit-raspberry-pi-camera-15-meter-extension-compatible)
- [Arducam U6248 at Welectron (kit contents)](https://www.welectron.com/Arducam-U6248-Cable-Extension-Kit-for-Raspberry-Pi-Camera)
- [Arducam IMX708 documentation (B0305 focus range 1.5 m to infinity)](https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/12MP-IMX708/)
- [Arducam 12MP IMX708 USB UVC fixed-focus module](https://www.arducam.com/product/12mp-imx708-usb-uvc-fixed-focus-camera-module-3/)
- [Arducam B0305 at DigiKey (38 × 38 mm)](https://www.digikey.in/en/products/detail/arducam/B0305/19116505)
- [RobotShop listing for the B0305 (24 × 25 mm camera board, 38 × 38 mm adapter)](https://ca.robotshop.com/products/arducam-12mp-imx708-usb-uvc-102-wide-angle-fixed-focus-camera)
- [Arducam IMX708 documentation](https://docs.arducam.com:443/Raspberry-Pi-Camera/Native-camera/12MP-IMX708/)
- [Arducam cable extension kit for Camera Module 3](https://www.arducam.com/product/arducam-cable-extension-kit-for-raspberry-pi-camera-module-3-up-to-10-meter-extension-compatible-with-all-imx708-camera-module/)
- [Arducam cable extension kit at Robu](https://robu.in/product/arducam-cable-extension-kit-for-raspberry-pi-camera-up-to-15-meter-extension-compatible-with-raspberry-pi-camera/)
- [The Pi Hut: Arducam LAN cable extension kit](https://thepihut.com/products/arducam-lan-cable-extension-kit-for-raspberry-pi-camera)
- [Raspberry Pi camera documentation](https://www.raspberrypi.com/documentation/accessories/camera.html)
