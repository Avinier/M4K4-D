# Body harness plan: the last harness segment, from wire list to checked CAD

| Field | Value |
|---|---|
| Status | **Levels 0–8 done 2026-11-16** except one open finding ([design review](05-harness/body-design-review.md)): endpoints 47/47, placements 8/8, routes 95/95, wires 77/77, vs head 31/31, service 10/13, mass 3/3; tie lugs, combined cut list and inspection STEP done. **Open:** W27 shell-lift plug passage (D-037 mock-up), J10-1 exit, rev A PCB-08 shapes, presentation STEP |
| Scope | Every installed wire whose run lies **inside the body**, above the J13 lift plane: rear bay, compute tray, the −Y riser to PCB-08, compute signals, audio, rear panel, and the body halves of the four body-lift plugs (§2) |
| Out of scope | D-108 (2026-11-15) lifted the D-096 electrical HOLD; its W02P, R010 and M1-heat conditions stay. Chassis runs (done: [D-106](decisions.md#d-106), `chassis_harness.py`), W47 neck and head fan-out (done: [D-107](decisions.md#d-107), `head_harness.py`). Both are **fixed obstacles** here. The D-096 electrical HOLD, CH-103 and the CH-099 shunt stay where they are tracked ([05-harness §9](05-harness/README.md#9-open-and-acceptance)) |
| Basis | [05-harness README](05-harness/README.md) §1–§7 (wire list and pinouts), [chassis design review](05-harness/chassis-design-review.md), [head-umbilical-plan.md](head-umbilical-plan.md), [d107-execution.md](final/v1/d107-execution.md), [d107-camera-verification.md](final/v1/d107-camera-verification.md), `final/v1/cad/makad-v1.step.py` |
| Evidence marks | `D` documented, `E` estimate, `U` verify on receipt, `W` measured. Every coordinate below is read from the current CAD sources (`D` as CAD); every length is `E` |

---

## 1. How the first two harnesses were done, and what this plan copies

Both finished harnesses followed the same five steps. The body harness should follow them too, so the three can be reviewed the same way.

| Step | Chassis (D-106, 2026-11-13/15) | Head (D-107, 2026-11-13/14) | Body (this plan) |
|---|---|---|---|
| 1. Concept and wire list | 05-harness §4.1/§4.2 rows (D-096 topology) | `head-umbilical-plan.md`: route study, W47 schedule, decision | Rows already exist in 05-harness §4; this plan adds the missing body-side parts and decisions (§3, §4) |
| 2. Route reserves | `D106_ROUTES` boxes and `D106_CHAINS` in `makad-v1.step.py`, print fixes (deck slot, tunnels, tie lugs); `check_d106_harness.py` 134/134 | `d107_umbilical.py`, `study_umbilical_*`, collar/clamp/liner prints; `check_d107_neck/body/seating` | `D109_ROUTES` / `D109_CHAINS` boxes and body-print tie features; `check_d109_routes.py` (Level 3) |
| 3. Visible wires | `chassis_harness.py` → `Harness → Chassis wires`, 34 cables + 2 splice envelopes; `chassis-harness.step.py` | `head_harness.py` → `Harness → Head wires`, 12 wires + HDMI + fan-out leads | `body_harness.py` → `Harness → Body wires`; `body-harness.step.py` (Level 4) |
| 4. Checks | `check_chassis_harness.py` 15/15: wire vs assembly, signal vs power, splice vs wires | neck 13/13 over 45 poses, body 31/31, service removal, mass | Neutral clash, segregation, **service sweeps** for shell, tray, panel, body lift, PCB-08 (Level 5) |
| 5. Review record | `chassis-design-review.md`: done vs open, P0/P1 | `d107-execution.md`, `d107-corrections.md`, camera verification | `05-harness/body-design-review.md` + 05-harness §4 update (Level 8) |

**Two lessons are carried forward.**

- **Chassis lesson: lengths stayed `E`.** The chassis visible wires were drawn but their centreline lengths were never extracted, so 05-harness §4 still carries hand estimates. The body harness should compute each wire's CAD centreline length and write it to a report from the start. The three harnesses can then give one cut list (Level 7).
- **Head lesson: clearance is not buildability.** The camera chain passed 72/72 clearance checks and still failed review (plug approached from below, ribbon as slabs, 65 mm of FPC surplus not drawn). Body checks must include **approach direction at each plug, surplus-length dress and service motion**, not only "no intersection".

---

## 2. Inventory: what the body harness contains

All rows already exist in [05-harness §4](05-harness/README.md#4-wire-list); this table only regroups them by body corridor and names their CAD endpoints. "Body-lift half" means the body side of a D-096 plug, which stays with the body when it lifts.

### 2.1 Rear-bay power (H-01 to H-03)

| ID | Body-side run | Conductors | CAD endpoints (labels) |
|---|---|---|---|
| `W03r` | `J-BAT` body half → rear +/− charge splice | 2×AWG16, `E` 60 | `J_BAT_*_RECEPTACLE_HALF` (X −19.5..−8.5, Y −31..−22.7, Z 57–67), exit reserve `HARNESS_D106_J_BAT_BODY_EXIT` → `CHARGE_SPLICE_HEATSHRUNK_AWG16` axis (−45.6, −34), Z 62–88. One splice is modelled; H-01 needs **two**, + and − (B-07) |
| `W04` | Charge splices → rear-panel XT30 female | 2×AWG16, `E` 100 | `M12_XT30U_FEMALE_CHARGE_PORT` at Y −8, Z 64, cups toward +X. Panel-withdrawal screen already done (47.6 mm at 40 mm withdrawal) |
| `W05` | +splice → M1 VIN; M1 VOUT → M6 IN+; M6 IN− → +STAR; −splice → M1 GND / −STAR | AWG16, `E` 40/80/60/100 | M1 `#2813` on rear plate face X −46.1, Y −27..−1.6, Z 72–92.5, terminals +Y; M6 at Y 1–26.5, Z 72–92.5; stars `SWITCHED_STAR_POS/NEG` at X −31.75 / −25.25, Y −12..12, Z 74.25 |
| `W05c` body half | ± STAR → `J-CHASSIS` body half | 2×AWG16 | `J_CHASSIS_*` Y 22.7..31, exit reserve `..._J_CHASSIS_BODY_EXIT` |
| `W05b` | ± STAR → M4 and M5 VIN/GND | 2×AWG18 per module, `E` 180 each | M4 under tray at origin (−19, 21.66), M5 at (3.86, −35.16), board top Z 79.5, components down |
| `W02B` tail | Already drawn by the chassis harness up to `M12_JST_XHP_3_BALANCE_PORT_PLUG` (Y 8.5, Z 64) | — | Only the park/unpark motion at panel removal is body scope |

### 2.2 Tray 5 V branches

| ID | Run | Conductors | Endpoints |
|---|---|---|---|
| `W10` | M4 VOUT → Pi 5 right-angle USB-C | 2×AWG18, `E` 100 | `PI5_POWER_USBC_RIGHT_ANGLE_PLUG_RESERVE` on the Pi's **−Y** edge, cable exits down. **M4 is on the +Y side** (see B-03) |
| `W05s` | M5 VOUT → shared-5 V ± distribution | 2×AWG18, `E` 60 | **No CAD envelope exists** for the distribution splice (B-02) |
| `W11` | Shared 5 V → SS34 (potted) → C3 `J10-1` | 2×AWG22, `E` 110 | `C3_J10_1_MICROFIT3_2P_MATED_PLUG` (X 46–56, Y −56.8..−49.8, Z 78.6–88). **No envelope for the potted SS34** |
| `W12` | Shared 5 V → M8 amp VIN/GND | 2×AWG22, `E` 160 | Amp bracket on front +Y post, board Y 40.6–58.4, Z 102–121.4 |
| `W14` | Shared 5 V → `J8-1.2/.5` and `.3/.6` | 4×AWG22, `E` 140 | `D107_PCB08_J8_1_MATED_PLUG_E` X −32.4..−24.4, Y −42.1..−28.9, Z 114–121, **mouth −X** |

### 2.3 −Y riser: head and yaw supply inside the body

| ID | Run | Conductors | Endpoints |
|---|---|---|---|
| `W13` body half | `J-S18-H` body half → `J8-1.1/.4` | 2×AWG20 | `J_S18_H_*` (X −3..16, Y −45.5..−38.5, Z 59.4–69.4), exit reserve `JS18_BODY_LEADS` → J8-1 (same plug as W14: 6 contacts in one housing) |
| `W17` body half | `J-S18-Y` body half → PCB-08 **J6 solder pads** (1 +11V1_YAW, 2 GND_SIG) | 2×AWG20 | `J_S18_Y_*` (Y −38..−31) → PCB-08 board X −22..12, Y −46..−21, Z 112–113.6. Soldered (B-06) |
| `W15` | PCB-08 `J8-8` → ST3215-HS yaw servo | Vendor 3-wire, 120 target | `D107_PCB08_J8_8_MATED_PLUG_E` X −20..−12, Y −25.9..−20.9, Z 119.6–126.6 |

### 2.4 Compute signals

| ID | Run | Build | Endpoints |
|---|---|---|---|
| `W24` | PCB-09 `J9-1` ↔ PCB-08 `J8-4` | GH6 1:1, `E` 170 | J8-4 top entry, X −8.7..0, Y −26.9..−22.7, Z 117.9–124.9 |
| `W25` | PCB-09 `J9-2` ↔ C3 `J10-2` | GH6 1:1, `E` 200 | J10-2 in PCB-10's Z 86 row, −Y wall |
| `W41` | Fan → PCB-09 `J9-4` | GH2 (schematic: BM02B-GHS-TBT) | Fan axis X 17.5, Z 110 on the +Y web. Body model's `J9_4_FAN_HEADER_RESERVE` says XH: stale (§3) |
| J6 lead | PCB-09 `J6` GH6 → **rear service break** → W44 (M6 SDA/SCL/VCC/GND) + W40 (BTN_SENSE, PWR_OFF) | GH6 pre-crimp + 6-way break, then 4×AWG28 + 2×AWG28 | Checked corridor: J6 rise (70.5–73.5, 29.5–32.5, 115.5–119.5) → Y 20, Z 118 → `M1_REAR_BUTTON_BUFFER_CAD_RESERVE` (−41..−34, −20..−8, 94–100). **Break connector unselected, not in CAD** (B-04) |
| `W40` | Mushroom NO → M1 ON/GND; buffer → BTN_SENSE | 2 + 2 wires | Mushroom on rear panel; old `POWER_BUTTON_W40_LEAD_RESERVE_1..4` still end at **deleted PCB-02 J2-9** (§3) |

### 2.5 Audio

| ID | Run | Build | Endpoints |
|---|---|---|---|
| `W26` | PCB-09 `J9-3` GH10 → audio hub | GH10 pre-crimp, solder at hub, `E` 160 | `M13_AUDIO_HUB_PERFBOARD` (18.5 × 22, on the bracket's −X face, Y 40–58.5, Z 100.5–122.5) |
| `W27` ×4 | Hub → INMP441 FL/FR/RL/RR | 6×AWG28 each, `E` 250 front / 190 rear | Mic boards in **shell** bosses at (54, ±70, 118) front and (−22, ±70, 108) rear; `M9_*_PIGTAIL_RESERVE` stubs. **Shell-mounted: needs a break** (B-01) |
| `W28` | Amp screw terminal → speaker | Twisted 2×AWG22, `E` 100 | Speaker at (90.5, 0, 99), removed with the front panel (D-037 assembly note) |

### 2.6 Camera body segment (coordination only)

The body HDMI cable, B0091 body board and HD-027 Pi FPC are D-107 parts and stay under its camera HOLD. They share the body corridors with W24, the J6 lead and W41, so the body route reserves must **leave room for** the 65.035 mm FPC surplus dress that the [camera verification](final/v1/d107-camera-verification.md) found missing. Drawing that dress is a D-107 camera fix, not a body-harness deliverable (B-10).

**Count:** about **25 runs and 95 conductors** (`E`), in 6 corridors, with 4 body-lift halves, 5 PCB-08 plugs/pads, 7 PCB-09/PCB-10 connectors, and 3 breaks/plugs that are not yet designed.

---

## 3. Gaps found while preparing this plan

These are concrete defects or missing pieces in the current sources. Each one must be closed before the body wires can be drawn honestly.

| # | Gap | Evidence | Effect |
|---|---|---|---|
| G1 | **Mic leads have no disconnect.** D-037 mounts the INMP441 boards on the shell and requires their leads to be unplugged at the board end before the shell lifts. D-093 replaced PCB-05 (which had the GH sockets) with a **perfboard hub** that only lists solder pads. GH is 1.25 mm pitch and does not fit 2.54 mm perfboard | decisions.md D-037 assembly note; 05-harness §4.2 W27 "solder at hub" | The shell cannot come off without cutting wires. The hub board must change (B-01) |
| G2 | **Shared-5 V distribution has no envelope.** W05s → W11/W12/W14 meets at "rated multiwire splices", but nothing is placed, unlike HN-006 in the chassis | 05-harness §4.1 W05s; no label in `bought_modules()` | Under-tray space between Z 69.9 (motor cable keep-out, D-072) and 79.5 is tight; this must be placed first |
| G3 | **M4 sits on the opposite side from the Pi's USB-C.** M4 (Pi supply) is at Y +21.7; the Pi USB-C plug and pigtail drop are on the −Y edge, beside **M5**. M4 and M5 are identical S13V30F5 modules | `TRAY_BAY` modules; `PI_POWER_PLUG_RESERVE` / `PI_POWER_PIGTAIL_DROP` | W10 at `E` 100 mm probably cannot reach; swapping the two roles may shorten W10, W11 and W14 (B-03) |
| G4 | **Only one charge splice is modelled.** H-01 needs an unswitched + splice and a − splice | `CHARGE_SPLICE` (one cylinder at −45.6, −34) | W03r/W04/W05 negative path has no physical node |
| G5 | **Stale Layout-02 body reserves still in the tree.** `HARNESS_SIGNAL_TRUNK`, `HARNESS_SENSOR_TRUNK`, `POWER_BUTTON_W40_LEAD_RESERVE_1..4` (to PCB-02 J2-9), `PI_POWER_PIGTAIL_DROP` (to PCB-04 J4-1), `J9_4_FAN_HEADER_RESERVE` (XH, schematic is GH2), `HARNESS_HEAD_RISER_UPPER_TO_J1` (X −29..−23, Z 110–120, now **inside** the moved J8-1 mated-plug envelope X −32.4..−24.4, Z 114–121) | `body_v1_model.py` 1145–1158, 4179–4192; `makad-v1.step.py` 1623–1626 | They show routes to deleted boards and can hide clashes. Retire or re-point each one (Level 0) |
| G6 | **W17 is soldered to PCB-08.** D-107's checked PCB-08 removal is "unplug all five; tilt 15°, +Y 6, −X 60". J6's solder pads are a sixth connection that cannot be unplugged at the board | `check_d107_body` `pcb08_service_removal`; PCB-08 README J6 | Either W17 follows the board out to `J-S18-Y` on the deck, or it needs a break (B-06) |
| G7 | **Rear service break (J6 → W40/W44) is unselected and not in CAD.** PCB-09 rev B checked only the lead corridor and buffer volume | 05-harness §4.2 note under W44 | Needed before W40/W44 can be routed and before the tray slide sequence can be checked |
| G8 | **No body-side slack for the body-lift plugs.** H-08 requires ≥40 mm withdrawable slack, and D-106 drew the plugs "40 mm inward to unmate", but nothing models where the body-half slack is stored | `BODYLIFT`, `D106_ROUTES` body exits end at Z 72 | Must be a drawn service loop, not an assumption |
| G9 | **Mass allowance is a placeholder.** The body register carries `HARNESS_AND_FASTENERS` 95 g at (20, 0, 88); 05-harness §6 gives ~87 g `E` with exclusions. D-107's tipping margin is tight (2.38 % in the original register against a 3 % buffer) | `body_v1_model.py` 1420; d107-execution.md | Real routed masses and centroid should replace the allowance and the tipping check must be re-run |

---

## 4. Decisions needed from the builder (become D-109)

Each has a recommendation. The option chosen changes what Level 2 builds.

| ID | Question | Options | Recommendation |
|---|---|---|---|
| **B-01** | How do the four mic leads disconnect for shell removal? (G1) | (a) Four 6-way **2.54 mm locking headers on a larger hub**, plugged through the front aperture as D-037 intended; (b) an inline 6-way break in each W27 near the hub; (c) a small custom hub PCB with four GH6 sockets | **(a)**, e.g. Molex KK 254 or a 2.54 mm-pitch equivalent that fits perfboard (family `U` until a sample mates). Grow the hub board and re-check the amp bracket bosses. (c) is cleaner but adds a seventh custom board |
| **B-02** | Where does the shared-5 V distribution sit, and in what form? (G2) | (a) Two insulated splice envelopes under the tray beside M5 (copy HN-006); (b) a small screw/lever terminal block on the tray underside | **(a)** first, placed in CAD to prove space; (b) only if one rated four-wire joint per polarity cannot be found |
| **B-03** | Keep or swap M4/M5 roles? (G3) | (a) Keep: M4 (+Y) feeds the Pi; (b) Swap: the −Y module feeds the Pi, the +Y module feeds shared 5 V | **Decide from CAD lengths.** Draw both in Level 4 and compare W10 + W11 + W12 + W14. (b) shortens W10 and W12 but lengthens W11 and W14, which go to the −Y wall and riser. No hardware or print change: both modules and mounts are identical; only labels and setpoints move |
| **B-04** | Rear service break family for the J6 lead (G7) | (a) Micro-Fit 3.0 1×6 inline pair with AWG26–28 contacts (reuses H-04 family and tool); (b) Molex PicoBlade wire-to-wire 6-way; (c) a soldered, sleeved joint (no service break) | **(a)** if a Micro-Fit contact for AWG26–28 exists in the chosen series (`U`); otherwise (b). (c) breaks the tray-removal procedure in 05-harness §4.2 |
| **B-05** | Wire dress method in the body | (a) Tie lugs fused into body prints (copy D-106 J15B-style lugs: 3 mm tall, 3 × 1.5 tunnel, 2.5 mm tie); (b) adhesive tie mounts; (c) printed clips | **(a)** on `BODY_FRAME_MAIN_PRINT` and the rear-bay plate, as droid adds in `makad-v1.step.py`. Proven on the chassis, no extra parts |
| **B-06** | W17 at PCB-08 removal (G6) | (a) W17 stays soldered; PCB-08 removal also unplugs `J-S18-Y` on the deck and W17 travels with the board; (b) add an inline 2-way MF3 break near PCB-08 | **(a)**, if the Level 5 sweep shows the W17 pigtail follows the 15°/+Y/−X path without snagging. Otherwise (b); no PCB change, because W17 still lands on the J6 pads |
| **B-07** | Second charge splice (G4) | Place a − splice beside the + splice on the rear plate, or a single two-cavity sleeve | Separate − splice, mirrored at Y −30..−38 band, with its own insulation |
| **B-08** | Speaker and front-panel removal | (a) Unscrew W28 at the amp terminal; (b) a 2-way JST PH/XH inline break | **(b)**. A screw terminal is not a service connector; the D-037 order removes the front panel and speaker before the mic plugs |
| **B-09** | Signal segregation rule for the body | Rules to enforce in the checks | I²S (W26/W27), RS-422 (W24/W25) and the J6 I²C lead keep **≥ 5 mm** from AWG16/18/20 power (W03r/W05/W05b/W10/W13/W17) and cross power only near 90°; W15 servo lead may run with W17. The 5 mm figure is `E`, chosen to be checkable |
| **B-10** | Camera body segment | Include the FPC dress in this work, or leave it to the D-107 camera fix | **Leave it to D-107**, but reserve a fold volume for the 65 mm surplus in `D109_ROUTES` so body wires do not take that space |

---

## 5. Levels of work

The levels follow the chassis and head work. Each ends with a check that must pass before the next starts. All CAD work goes in `final/v1/cad` (droid-owned edits only; subsystem sources stay untouched) and uses the legacy 0.4.28 runtime documented in [final/v1 README](final/v1/README.md).

### Level 0 — Clean the ground (half a day)

1. Retire or re-point every stale reserve in G5. Prefer adding labels to the droid's drop list in `makad-v1.step.py` (as done for PCB-02–07 and D-104/105 labels) over editing `body_v1_model.py`.
2. Fix the J9-4 envelope to the GH2 plug that PCB-09 rev B actually carries.
3. Re-validate `HARNESS_HEAD_RISER_UPPER_RISE` against the D-107 PCB-08 cradle and J8-1 position; delete `..._UPPER_TO_J1` if it duplicates the plug envelope.
4. Write `body_harness_endpoints.py`: one function that returns every body-harness endpoint (label, face point, **approach direction**) from the live tree. Every later script reads endpoints from here, never from copied numbers.

**Exit:** `check_body_endpoints.py` finds every label in §2 in the tree and reports its mouth point and approach vector. Stale labels gone from a fresh build.

### Level 1 — Decide (builder session)

Take B-01 to B-10. Record D-109 in `decisions.md` with the chosen options. Update 05-harness §1 with any new H-rows (expected: mic break, shared-5 V node, rear service break, speaker break, M4/M5 roles).

**Exit:** D-109 recorded; no open option blocks Level 2.

### Level 2 — Place the missing parts (1–2 days)

Add tagged envelopes, all `E` and labelled `UNMEASURED` where the part is unbought:

| Part | Placement target | Check |
|---|---|---|
| Second (−) charge splice (B-07) | Rear plate −Y edge beside the existing splice | `check_bay_rear.py` extended |
| Shared-5 V ± splices (B-02) | Under the tray beside M5, above Z 69.9 | `check_bay_tray.py` extended: clear of motor reserves, standoffs, Pi pigtail |
| SS34 potted joint (W11) | On W11, within 20 mm of M5, sleeve Ø6 × 18 `E` | Same |
| Rear service break, mated (B-04) | Inside or beside `M1_REAR_BUTTON_BUFFER_CAD_RESERVE` on a rear-plate tie lug | `check_bay_rear.py`: hand access with rear panel off |
| Enlarged audio hub with four mic headers + speaker break (B-01, B-08) | Same bracket; grow toward −Z or −X | `check_amp_mount.py` extended: header mouths face the front service aperture |
| Body tie lugs (B-05) | Rear plate, tray underside, −Y riser, +Y post | Print check on the affected body prints |

**Exit:** all new envelopes clear the printed body, modules and the drawn chassis/head wires at neutral; module checks unchanged.

### Level 3 — Route reserves: `D109_ROUTES` (2–3 days)

Copy the D-106 method exactly: world boxes `(x0, x1, y0, y1, z0, z1)` drawn round each bundle with bend room, and chains whose consecutive boxes must overlap.

Six trunks, proposed (all `E` until drawn):

| Trunk | Carries | Path |
|---|---|---|
| **T1 rear bay** | W03r, W05, W05c body half, W04 | J-BAT / J-CHASSIS body exits (X −27.5..−19.5, up to Z 72) → aft over the rear cross rail → stars at Z 74.25 → M1/M6 terminals on the plate face → splices → XT30 cups |
| **T2 tray feed** | W05b to M4/M5 | Stars → forward under the tray at Z 70–79 along the ±Y edges (above the D-072 keep-out) |
| **T3 −Y riser** | W13, W17, W14, W15 | J-S18 body exits and M5/shared node → up the −Y side → J8-1 (enter from −X) and PCB-08 J6 pads; W15 from J8-8 to the servo |
| **T4 compute** | W24, W25, W41, J6 lead | PCB-09 connectors → J8-4 (top), J10-2 (−Y wall, Z 86 row), fan (+Y web), J6 corridor to the rear break |
| **T5 audio** | W26, W27 ×4, W12, W28 | J9-3 → hub; hub → front mics direct; hub → rear mics along the shell inner side at |Y| ≈ 60–66 below the fan web; W12 from the shared node to the amp |
| **T6 rear panel** | W40, W04 loop, XHP-3 park | Mushroom → M1 ON/GND and buffer; the panel-withdrawal loop volumes |

Plus two **slack volumes**: body-lift withdrawal loops for the four body halves (G8), and the camera FPC surplus fold (B-10).

Write `check_d109_routes.py` on the `check_d106_harness.py` pattern: every box out of every printed part and module; every chain connected; every chain end meets its endpoint mouth from §Level 0 **from the correct side**; lead room ≥ 6 mm straight at each Micro-Fit and ≥ 3 mm at each GH.

**Exit:** `check_d109_routes.py` all pass; D-106 and D-107 checks still pass (`check_d106_harness.py`, `check_d107_body.py`, `check_pcb09_fit.py`).

### Level 4 — Visible wires: `body_harness.py` (2 days)

1. New `final/v1/cad/body_harness.py`, built like `chassis_harness.py`: `_through_boxes()` turns each chain into a centreline; pairs are offset by insulation OD; signal bundles are single outer envelopes (GH6 Ø2.6, GH10 Ø3.2, W27 six-core Ø2.4, all `E` until measured).
2. Groups under `Harness → Body wires`: *Rear-bay power*, *Tray 5 V*, *Riser to PCB-08*, *Compute signals*, *Audio*, *Rear panel*.
3. Add it to `build_robot()` next to the head and chassis wires; add `body-harness.step.py` as the focused review entry.
4. **New over the chassis work:** each wire records its centreline length plus a termination/service allowance, written to `body-harness-lengths.json`. Do the same retroactively for `chassis_harness.py` and `head_harness.py` so one script gives all three (Level 7).
5. For B-03, build both M4/M5 role variants once and record the four wire lengths in the report.

**Exit:** focused STEP opens in the 0.4.28 viewer; snapshots `body-harness-iso`, `-rear-bay`, `-riser`, `-audio` reviewed by eye for crossed folds, plug approach and bunching.

### Level 5 — Checks (2–3 days, run targeted)

`check_body_harness.py`, with one row per item:

| Check | Pass condition |
|---|---|
| Wires vs assembly | No intersection > 0.05 mm³ except intended plug-entry contacts (allow-list per wire, as `check_chassis_harness.py`) |
| Segregation (B-09) | Each signal/audio envelope ≥ 5 mm from each power envelope, except named crossings |
| Plug approach | The last segment of each wire enters its plug's rear face along the plug axis (± 20°), with straight lead ≥ 6 mm (MF+/MF3) or ≥ 3 mm (GH). This is the check the camera chain lacked |
| Bend radius | No centreline bend tighter than 3 × OD for power, 5 × OD for W27/GH bundles (`E`) |
| Bundle fill | Every reserve box holds its wires' total cross-section at ≤ 60 % fill |
| **Shell removal** | With W27 unplugged (B-01) and W28 broken (B-08), lower/lift the shell along its D-037 path: no wire touches it. Mic tails ride with the shell inside their pigtail reserves |
| **Tray slide** | J6 pre-mated; the tray assembly travels its path; the J6 lead follows the PCB-09 corridor without crossing W10, W24 or W25 |
| **Rear-panel withdrawal** | 40 mm rearward + lay-down; W04, W40 and the parked XHP-3 stay within their loops; no load on cups (distance screen extends the chassis W04 study) |
| **Body lift** | Each body-lift half withdraws 40 mm inward without pulling its body-side run tight (G8) |
| **PCB-08 removal** | The D-107 15° / +Y 6 / −X 60 path, with W17 handled per B-06 |
| Chassis/head unchanged | `check_chassis_harness.py` 15/15, `check_d107_body.py` 31/31, `check_d107_neck.py` 13/13 still pass |

Do **not** run the 40-minute `check_layout`; the targeted set above covers every touched interface.

### Level 6 — Mass and tipping (half a day)

1. From `body-harness-lengths.json`, compute conductor mass per wire (g/m by gauge, `E`: AWG16 UL1061 ≈ 14, AWG18 ≈ 9, AWG20 ≈ 6, AWG22 ≈ 4, AWG28 ≈ 1.2) plus connector/splice masses, with centroids from the CAD paths.
2. Replace the body's 95 g `HARNESS_AND_FASTENERS` allowance by the routed harness rows plus a smaller fastener allowance. Keep the chassis and W47 rows separate so nothing is counted twice (the D-095 balance/charge rows are already separate).
3. Re-run `check_d107_mass.py` (moving-frame sweep and original register). If the original-register margin falls further below 3 %, report it; do not change ballast silently.

**Exit:** mass report written; tipping margins recorded with method named.

### Level 7 — Cut list, connector counts and BOM (1 day)

1. One script, `harness_cut_list.py`, reads the three length reports and writes the cut list: CAD centreline + termination allowance + service loop, per wire, flagged `E`.
2. Update 05-harness §4 tables: replace hand `E` lengths with the CAD-derived ones (still `E`; they become `W` only after string-routing the built robot).
3. Count contacts, housings, splices and sleeve by family, including the new mic headers, rear service break, speaker break and shared-5 V splices.
4. Per the Level 6 BOM practice, log any article the builder orders, then write the BOM in one pass at the end.

### Level 8 — Record and release (half a day)

1. `05-harness/body-design-review.md`: done vs open, P0/P1, on the chassis review's format.
2. 05-harness README: title and scope become "chassis, body and D-107 head"; §4 adds the CAD view note for `Harness → Body wires`; §7 service procedures gain shell-off (mic and speaker breaks), tray-out (rear break) and PCB-08-out (W17) steps.
3. `final/v1/README.md` check table rows; `TODO.md` order items for the new connectors.
4. Rebuild `makad-v1.step` and the presentation STEP with `--force`, then snapshot. The chassis-harness commit already advanced the source past the D-107 export baseline, so a fresh whole-robot export is due anyway.

---

## 6. Physical gates after the CAD

The CAD can only screen. Release of the body harness also needs:

- **Receipt measurements:** M6, M8 and M9 outlines (still `UNMEASURED`), the #2813 terminal holes, S13V30F5 pad positions, chosen mic-header and rear-break samples, GH lead bundle ODs.
- **Mock-up before printing the shell and hub:** plug the four mic leads through the front aperture with the shell lowered (D-037 order) and unplug them for lift-off.
- **First build:** string-route every body run on the assembled robot and record `W` lengths; photograph every pad termination; pull-test three samples per wire/contact combination; prove the tray slide with J6 pre-mated; prove 40 mm slack at all 11 body-lift plugs.
- **Bench, unchanged from 05-harness §9:** N1 (switch heat), N2/N3 (head and yaw rails), N8 (Schottky back-feed on W11), N9/N11 (audio and mic timing, with W27 at final length and routing), N10 (IMU), N12 (Pi input voltage over W10). N9/N11 are the real test of the B-09 segregation rule.

---

## 7. Risks

| Risk | Why it matters | Mitigation |
|---|---|---|
| Hub growth collides with the amp bracket or speaker cup | B-01 adds four headers to an 18.5 × 22 board | Place in Level 2 before routing; move the hub to its own bracket face if needed |
| Under-tray congestion (M4, M5, shared node, SS34, W05b, W10, W11, W14) | One 9.6 mm band between the D-072 keep-out and the module undersides | Place G2/SS34 first; B-03 swap may relieve it |
| −Y riser congestion (W13, W14, W17, W15, the W47 body run, the camera FPC, W25 to J10-2) | Every head and yaw supply rises on the same side as the camera FPC and PCB-10 | Draw T3 before T4; keep the FPC surplus volume reserved (B-10) |
| I²S noise from servo/drive currents | W27 is 190–250 mm of unshielded AWG28 | B-09 rule enforced in CAD; N9/N11 at final routing; fall back to twisting SCK/WS with GND |
| PCB-08 removal now needs a deck unplug | B-06 (a) adds a step | Write it into 05-harness §7.3; switch to (b) only if the sweep fails |
| Another session edits `makad-v1.step.py` or 05-harness at the same time | Has happened before (parallel-session memory) | Re-read before each write; stage own edits only |

---

## 8. Recommended order and effort

| Order | Work | Effort (`E`) | Depends on |
|---|---|---|---|
| 1 | Level 0 cleanup + endpoint module | 0.5 day | — |
| 2 | Level 1 decisions (B-01…B-10) → D-109 | 1 session | Level 0 findings |
| 3 | Level 2 placements | 1–2 days | D-109 |
| 4 | Level 3 route reserves + `check_d109_routes.py` | 2–3 days | Level 2 |
| 5 | Level 4 visible wires + lengths (all three harnesses) | 2 days | Level 3 |
| 6 | Level 5 checks incl. service sweeps | 2–3 days | Level 4 |
| 7 | Level 6 mass/tipping | 0.5 day | Level 4 |
| 8 | Level 7 cut list/BOM, Level 8 records + rebuild | 1.5 days | Levels 5–6 |

About **10–13 working days** of CAD and documentation, then the physical gates in §6. Start with T1 (rear bay) and T3 (−Y riser): they carry all the power and are the most crowded.
