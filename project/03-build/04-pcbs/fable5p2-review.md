# PCB-08 rev B — design review (Fable 5.2, 2026-11-17)

Review of [pcb-08-yaw-junction](pcb-08-yaw-junction/README.md) rev B as saved at commit `c9d567dc` (board file SHA-256 `f486017c…ad6618`). Nothing in the board folder was changed; all work was done on a scratch copy.

## 1. Verdict

**The board is electrically correct and its evidence reproduces, but it is not the best design for its job, and six things should change before it is ordered.**

- **Correct:** every net goes where the harness tables say. ERC, DRC, the four audits and the fab package all reproduce exactly.
- **Not optimal:** half of the board (the two Micro-Fit headers and both inner layers) carries power straight through without doing anything to it. The four-layer stack and the special inner-copper order exist only to untangle a wire crossing that the connector arrangement creates. See [§5](#5-is-it-the-best-design-for-its-goal).
- **Should fix before ordering** ([§4](#4-findings)):
  1. The yaw tracks run under J1's metal clips, where Molex forbids copper, and sit 0.18 mm from J1's pins on the side that gets soldered by hand.
  2. The board has no silkscreen at all, so the hand-soldered 11.1 V pads have no polarity mark.
  3. The inner-copper requirement cannot be met as written and the board's own numbers do not need it.
  4. The C2 and display tracks are thin and were sized without a display current.
  5. The W17 solder joints land on the cradle's support ledge, and W17 has no strain relief.
  6. One track sits at exactly the minimum distance from the board edge for 20 mm.

None of these is a wrong connection. Items 1, 2 and 5 are the ones that could damage a part or stop the board seating.

## 2. What I ran

| Check | Tool | Result |
|---|---|---|
| ERC, all severities | Nightly `kicad-cli` 10.99 | 0 violations |
| DRC with schematic parity, as saved and again after a zone refill | Nightly `kicad-cli` | 0 errors, 0 unconnected, 0 parity; the same six `lib_footprint_mismatch` warnings. The refill left the file byte-identical, so the saved fills are current |
| `audit_netlist`, `audit_w47`, `audit_pads`, `audit_power_copper` | Project `.venv` | All pass; three of the four JSON reports are byte-identical to the committed ones (the pad audit differs only in the library path) |
| Gerbers and drills regenerated and compared with `fab/revB` | Nightly `kicad-cli` | Identical apart from creation dates. The fab package matches the board |
| Board read back through KiCad's own model | **KiPy 0.8.0** against the Nightly PCB editor | 87 track segments, 12 vias, 9 footprints, 41 pads, 2 filled zones, 4 edge lines, no board text. Matches the file |
| Copper analysis on the KiPy data | Own scripts (shapely, scipy) | Track resistances, plane resistance, narrowest plane channels, every different-net gap, edge distances, Molex keep-out overlap |
| 3D render and four-layer plot | `kicad-cli pcb render`, matplotlib | Used to read placement and routing |
| Molex drawing SD-43045-008 for 43045-0621 | Web | Source for the clip keep-out note |

KiPy note: the standalone Nightly PCB editor, opened on the scratch board, did answer KiPy. The earlier "no handler available" result for standalone windows did not repeat.

**Not checked:** the whole-robot CAD checks (`check_d107_body.py`, `check_pcb_integration.py`), anything physical, and India stock for any part.

## 3. What holds up

- **Pin maps.** J1 and J3 carry the same six nets on the same pin numbers. J4's order is J2's plus `SERVO_DATA`. PCB-12's J1/J2 and its three ground links agree with W47.
- **Wrong-plug safety.** J1 and J3 are identical and wired identically, so swapping their plugs changes nothing. Swapping the two GH6 plugs is also harmless: `SERVO_DATA` lands on an unconnected pin (PCB-09 `J9-1` pin 6 is unconnected too) and the head simply loses the servo bus.
- **Head rail copper.** My own solver gives 3.54 and 4.79 squares for the two fills, against the audit's 3.53 and 4.75. ("Squares" is the resistance of a copper shape counted in units of one square of that copper; multiply by the sheet resistance to get ohms.) At 2.4 A that is about 11 mV and 27 mW in total. The audit's method is sound.
- **Yaw copper.** 1.5 mm outer tracks, 8.6 mΩ out and 11.6 mΩ back. At the 2.4 A yaw screen figure that is 48 mV and under 0.12 W. IPC-2221 puts a 1.5 mm, 35 µm outer track at about 3.2 A for a 10 °C rise.
- **Routing discipline.** Every segment is octolinear. The yaw supply and return run on top of each other on opposite faces, which keeps their loop small. No autorouter traces.
- **Fab rules.** Vias are 0.67/0.35 mm, tracks ≥ 0.2 mm, all inside the fab-neutral set.

## 4. Findings

Coordinates are KiCad mm (world X = x − 100, world Y = 100 − y).

### 4.1 Yaw tracks under J1's clips and tight against its pins — fix

The channel between J1's clip holes and its first pin row is 1.87 mm wide. The layout puts a 1.5 mm track through it on both faces: `GND_SIG` on the top, `+11V1_YAW` on the bottom.

| Problem | Measured |
|---|---|
| Molex note 8: "Metal tab may be flush with PCB. No exposed traces or vias allowed near these areas." The footprint draws these two 2.45 × 1.60 mm areas per header on `Dwgs.User`, so DRC cannot see them | Top `GND_SIG` track covers 3.2–3.6 mm² of each of J1's two areas (each is 3.9 mm²). Top `SERVO_DATA` track crosses one of J3's areas (0.32 mm²) |
| Gap from the bottom `+11V1_YAW` track to J1 pins 1, 2, 3 (`+6V3_HEAD_PR`, `+5V_C2`, `+5V_DISPLAY`) and to the clip pad | 0.183–0.186 mm, against the 0.16 mm rule |
| Gap from the top `GND_SIG` track to the same pads and to J6 pad 1 (`+11V1_YAW`) | 0.175–0.186 mm |

Why it matters:
- The tracks are under solder mask, so they are not literally "exposed". But a metal tab resting on a masked track is how mask gets worn through. The clips have no net, so one contact shorts nothing; it is still against the maker's layout note.
- The bottom is where J1's pins and clips are soldered by hand. A solder bridge across a 0.18 mm mask strip would put 11.1 V on a 5 V rail, which would destroy the C2 module or the display.

Fix: route the yaw pair down the free channel at x ≈ 89.3–91.9 (between J1's courtyard and J4's mounting pads), where it can keep ≥ 0.5 mm from everything, or move J5 and J6 next to each other. Move the `SERVO_DATA` test branch to the bottom face, clear of J3's clip. Add the four keep-out boxes to the footprint as real rule areas so DRC enforces them.

### 4.2 No silkscreen — fix

`layout_pcb08.py` moves every silkscreen item to the Fab layer; both silkscreen Gerbers are empty.

- **J6** is two bare pads soldered by hand: pad 1 `+11V1_YAW`, pad 2 `GND_SIG`. The only cue is that pad 1 is square. Reversed, the yaw servo gets −11.1 V.
- J1/J3 and J2/J4 are identical pairs with no names. Swapping is harmless (§3), but nothing tells the assembler which is which, and pin 1 is unmarked on all five connectors.
- There is no board name or revision on the copper or silk. Rev A and rev B outlines differ, but a label costs nothing.

Fix: add `+11V1` and `GND` at J6, the harness names (`J8-1`, `J8-9`, `J8-4`, `J8-10`, `J8-8`), pin-1 marks, `TP` names and `PCB-08 B`. The fab-neutral rule allows text at 1.0 mm high with 0.16 mm lines, and the board has room. Restoring the library silk should also clear the DRC warnings that come from the silk move.

### 4.3 The inner-copper requirement — reword

The README and fab note demand "at least 35 µm **finished** copper on every layer", with written fab confirmation, and call 17.5 µm unacceptable.

- **It cannot be met by a 1 oz order.** 1 oz foil is 35 µm nominal before processing. IPC-6012 allows an inner 1 oz layer to finish at 24.9 µm, and a 0.5 oz layer at 11.4 µm (figures from the standard as I recall them; confirm on the fab's stack-up sheet). A fab can only promise ≥ 35 µm finished by using heavier foil. As written, this gate stalls the order.
- **The head rail does not need it.** Both fills together:

| Inner copper | Drop at 2.4 A | Loss |
|---|---|---|
| 35 µm (nominal 1 oz) | 11.3 mV | 27 mW |
| 24.9 µm (IPC minimum for 1 oz) | 16.0 mV | 38 mW |
| 17.5 µm (nominal 0.5 oz) | 22.8 mV | 54 mW |
| 11.4 µm (IPC minimum for 0.5 oz) | 35.0 mV | 84 mW |

Even the worst row is under half of the 80 mV the W47 wires lose, and tens of milliwatts will not warm an 850 mm² board measurably. One Micro-Fit contact at 10 mΩ dissipates 58 mW, more than both planes.

- **The parts that do care are the thin tracks** (§4.4), not the planes.

Fix: specify "1 oz (35 µm nominal) inner foil, IPC-6012 Class 2" as a preference, add the 24.9 µm row to `audit_power_copper.py`, and drop the written-confirmation gate. Keep N2(b)'s terminal-voltage measurement; the PCB-temperature measurement can go.

### 4.4 C2 and display tracks — widen

`+5V_C2`, `GND_C2`, `+5V_DISPLAY` and `GND_DISPLAY` are 0.5 mm tracks, 24–28 mm long, on the inner layers.

| Branch | Loop resistance, 35 µm at 20 °C | At IPC-minimum 1 oz, 60 °C |
|---|---|---|
| C2 | 51 mΩ | 83 mΩ |
| Display | 52 mΩ | 84 mΩ |

- That is about as much as the 0.35 m of AWG26 in W47 (94 mΩ loop). The board nearly doubles each branch's wiring loss.
- IPC-2221 gives a 0.5 mm inner track about 0.55–0.7 A for a 10 °C rise. The display's current is not recorded anywhere (K3 is open), so the width was chosen without a number.
- These four tracks are also what cut slots in the two head-rail fills. The top and bottom faces are almost empty.

Fix: move the four tracks to the outer faces at 1.5 mm or wider. Loop resistance falls to about 17 mΩ, the answer no longer depends on inner copper, and both fills become unbroken.

### 4.5 W17 at J6: ledge clash and no strain relief — fix

- The cradle's support ledge covers the bottom of the board from the rear edge to world Y −44.8 (`d107_umbilical.py`, `block(-26,16,-48,-44.8,110.5,112)`), touching the board at Z 112. J6's bottom pads reach world Y −45.08, so each pad overlaps the ledge by 0.28 mm, and the hole edge is 0.23 mm from it. The solder fillet and wire stub of W17 will sit on the ledge and stop the board seating flat. The board STEP has no solder or wire, so the CAD checks cannot see this.
- The README says "strain relieve before pads", but the board has no feature for it. W17 is AWG20, stays soldered, and leaves with the board at every removal (D-109 B-06). Stranded wire breaks where the solder ends.

Fix: move J6 at least 1.5 mm inboard (or notch the ledge over world X −10…−2), and add a slot or two Ø2.5 holes beside it for a cable tie. A tie slot is not a mounting hole, so it does not break the "no unreviewed mounting holes" rule.

Also check: an AWG20 stranded conductor is about 0.95–1.0 mm across and the hole is 1.15 mm. It fits, with about 0.1 mm to spare; try the bought wire.

### 4.6 `GND_SIG` track on the edge limit — move

The bottom `GND_SIG` track from R1 to TP2 runs at x = 111.55 for 20 mm. Its copper is exactly 0.300 mm from the board edge, which is the rule with no margin for the fab's outline tolerance. Its lower end is beside the cradle's +X side stop. It is squeezed there by J3's clip pad.

Fix: R1's `GND_SIG` end can reach the net at J4 pin 1 or J6 pad 2 through the board interior once §4.1 and §4.4 free the faces.

### 4.7 Smaller points

| Item | Note |
|---|---|
| J4 access | J4 (the W47 signal plug, pulled at every head removal) sits in a slot 11.5 mm wide between the backs of J1 and J3. Those headers are 9.9 mm tall; a mated GH plug is 7.3 mm, so it sits below their tops. Courtyard gaps are 1.45 mm to J1 and 3.45 mm to J3. Try it with real parts before fixing the placement; the open strip beside J2 is the alternative |
| Assembly order | J4's solder tails face J3's rear wall about 4 mm away. Solder J2, J4 and R1 before any Micro-Fit, or J4 cannot be reworked |
| Vias | Eight of the twelve vias carry the four RS-422 lines to the bottom and back. J2's and J4's pin orders nest, so all four can stay on the top face once the `SERVO_DATA` test branch moves. Fewer vias also widens the `GND_HEAD` fill's narrowest channel (1.25 mm, between a via and J3's pins) |
| Test pads | TP1 and TP2 are 1.0 mm pads. A 1.5–2 mm pad or a wire loop is easier to hold a probe on |
| Head-rail pins | J1/J3 pins 1 and 4 join the fills solidly. Right for current; they need more heat when soldered by hand |
| Panel | Lion Circuits' MII service needs a 50 × 100 mm panel. The fab note does not say so |
| Stale text | `build_schematic.py` still names `J8-6`/`J8-7` and says the PCB editor is driven by KiPy and F8; the layout is now `kfile`-based |

## 5. Is it the best design for its goal?

The README states the goal: a stationary junction where the body harness meets the head bundle W47. Split by what each part of the board actually does:

| Function | Parts | Does the board add anything? |
|---|---|---|
| Three power pairs, J8-1 → J8-9 | J1, J3, both inner layers | **No.** Six wires in, the same six wires out |
| Head link, W24 → W47 | J2, J4 | Yes: it adds `SERVO_DATA` and swaps the ground pin to `GND_SIG` |
| Yaw servo plug and W17 landing | J5, J6 | Yes: it joins the servo's power, ground and data |
| Ground option | R1 | Yes |
| Bench access | TP1, TP2 | Yes |

### 5.1 The power pass-through is the expensive half and does no work

- It puts 12 mated contacts and 12 solder joints in series with the head's power, where a single inline pair would put 6 and none.
- It is the only reason the board has four layers. J3 is J1 turned 180°, and both use the same pin numbers, so all six nets must swap sides between the two headers. Two layers cannot do that cleanly; four can.
- It sets the board's size: the two Micro-Fit courtyards cover about 40 % of the 34 × 25 mm area and fix its 34 mm length.

**Alternative A — inline connector.** Join the body harness to W47 with one wire-to-wire Micro-Fit 2 × 3 pair (the project already uses inline Micro-Fit breaks at `J-S18-H` and the J6 rear break), held in a printed clip on the same cradle. PCB-08 shrinks to J2, J4, J5, J6 and R1: two layers, roughly half the area (`E`), ordinary copper, no inner-copper question at all.
- Cost: the head-removal step becomes "unplug one inline pair and one GH plug" and the clip needs designing and checking in CAD.
- This is the better design on parts, loss, cost and risk. It is a route change, so it is the builder's decision.

**Alternative B — keep the board, use the layers properly.** If a fixed power socket on the board is wanted (it is easier to find and mate than a loose inline pair), four layers is a fair price for a clean crossing. Then apply §4.3 and §4.4: fills on the inner layers with nothing else there, C2 and display wide on the outer faces, ordinary 1 oz or even 0.5 oz inner copper. That is rev B with the findings fixed.

### 5.2 "Separate returns" are separate only on this board

PCB-08 keeps `GND_HEAD`, `GND_C2`, `GND_DISPLAY` and `GND_SIG` apart. PCB-12 joins all of them in the head through three 0 Ω links (R1, R7, R10), and they also meet at the supply star. Bonded at both ends, the four returns are simply four wires in parallel, and the head servos' return current divides between them by resistance.

Rough estimate from the wire schedule (`E`: AWG22 53 mΩ/m, AWG26 134, AWG28 213; contacts 5–10 mΩ each): about 0.35–0.45 of the servo return current leaves through PCB-12 rather than the `GND_HEAD` wire. At the 2.4 A allowance that is roughly 0.9–1.1 A through the AWG28 `GND_HEAD_REF` branch and PCB-12's J2 pin 1, a GH contact rated 1 A.

- This is a stall-only figure and I have not measured anything; the lengths and contact values are assumed.
- It does not make PCB-08 wrong. It means the separation here buys no isolation, and that the thin reference wires carry servo current.
- It belongs to PCB-12 and W47: fit R7 as a resistor (10 Ω keeps the `SERVO_DATA` reference and blocks the share), or accept it and size the branch for 1 A. Worth deciding before PCB-12 is ordered.

### 5.3 Two population choices

- **R1 value.** 0 Ω ties the Pi's ground to the yaw servo's ground through W24's AWG28 wire, in parallel with the star. D-100 accepted that loop and kept this footprint as the fallback. Since both grounds already meet at the star, the usual RS-422 practice of about 100 Ω in the ground wire would keep the reference and stop servo current sharing through the Pi. With no bench equipment to measure the loop, 100 Ω is the safer first fit; the footprint takes either.
- **Yaw rail capacitor.** The yaw servo is fed by a regulator that cannot absorb current, through 257 mm of wire, and the board has no capacitor. A footprint for a 100–470 µF, 25 V part across J5 pins 2 and 1 costs nothing and can be left empty. This is a judgement call, not a defect; D-093's minimal-safety scope may rule it out.

## 6. Suggested order of work

1. Decide §5.1: inline power pair (A) or fixed sockets (B).
2. If B: re-route the yaw pair and the `SERVO_DATA` branch (§4.1), move C2/display to the outer faces (§4.4), move the edge track (§4.6), move J6 inboard and add the tie slot (§4.5).
3. Restore silkscreen and add the labels (§4.2).
4. Reword the copper requirement and add the 24.9 µm row to the audit (§4.3).
5. Add Molex's four keep-out areas to the footprint as rule areas, then re-run DRC, the four audits and the export.
6. Re-run `check_d107_body.py` and `check_pcb_integration.py` with the new STEP, and add a J6-fillet envelope to the cradle check.
7. Raise §5.2 against PCB-12 before either board is ordered.
8. With received parts: J4 plug access (§4.7) and the AWG20 fit in J6.

---

# PCB-09 rev B — design review (Fable 5.2, 2026-11-17)

Review of [pcb-09-c0-link-adapter](pcb-09-c0-link-adapter/README.md) rev B as saved at commit `65d1db5c` (board file SHA-256 `079e63da…b68989`). Nothing in the board folder was changed; KiCad work was on a scratch copy.

## P1. Verdict

**PCB-09 rev B is a sound design and close to the best its envelope allows. I found no wrong connection. Four things should change before it is ordered, and one pin choice is worth reconsidering.**

- **Correct, as far as this review went:** the circuit reads correctly from the manifest, and the copper is adequate for every current on the board.
- **Near-optimal:** the four layers and the two-sided assembly are both forced by the space, not chosen for comfort ([§P5](#p5-is-it-the-best-design-for-its-goal)).
- **Should fix before ordering** ([§P4](#p4-findings)):
  1. Three of J6's six pins leave the board with no protection, toward pack-voltage hardware.
  2. The board has no labels, and two decisions (D-073, D-098) require them.
  3. Thirteen socket pads sit 0.17 mm from another net's track on the side that gets soldered.
  4. R7 assumes a rear-bay circuit that has not been designed yet.
- **Reconsider:** the battery monitor can have a hardware I²C bus on the pins rev B gives to the button and OFF ([§P5.2](#p52-the-battery-monitor-can-have-a-hardware-bus)).

## P2. What I ran

ERC, DRC, the netlist audit and the fab export were **not** re-run, at the builder's request. The committed `layout-drc.json` (0 / 0 / 0, 2026-11-08) is taken as given.

| Check | Tool | Result |
|---|---|---|
| Board read back through KiCad's own model | KiPy 0.8.0 against the Nightly PCB editor, scratch copy | 209 track segments, 46 vias (all 0.67/0.35 mm), 35 footprints, 143 pads, 4 copper fills, 3 rule areas, 12 edge lines, no board text. Outline 89 × 22.7 mm, 1,180 mm² |
| Stack-up stored in the board | KiPy | Outer copper 35 µm, **inner copper 15.2 µm** (half-ounce class) |
| Resistance of the 3.3 V, 5 V and ground copper | Own solver on the KiPy geometry: all four layers, vias as shorts | Table in §P3 |
| Every different-net gap and edge distance, per layer | Own script (shapely) | Minimum gap 0.16 mm on every layer; nearest copper to the edge 0.30 mm (fills), tracks 0.32 mm or more |
| Top-face space for the underside parts | Own script on the pad outlines | §P5.1 |
| Silkscreen content | Board file and the `fab/revB` Gerbers | §P4.2 |
| Circuit and far ends | `circuit-manifest.json`, `layout_pcb09.py`, README, D-096, D-098, harness W40/W44, BOM BO-067 | Basis for §P4 and §P5 |
| Pi 5 I²C overlay options | Raspberry Pi `rpi-6.12.y` overlay README (the README's source U) | §P5.2 |

## P3. What holds up

| Path | Resistance | At the expected load |
|---|---|---|
| 3.3 V, Pi pins 1/17 → U1 pin 1 | 174 mΩ | 12 mV drop with both transceivers driving, the mics and the pull-ups (about 69 mA) |
| 3.3 V → U2 pin 1 | 210 mΩ | 13 mV |
| 3.3 V → J4 pin 1 (audio hub) / J6 pin 1 | 183 / 189 mΩ | 12 mV |
| 5 V, Pi pins 2/4 → J5 pin 1 (fan) | 161 mΩ | 24 mV at 0.15 A (`E`: the fan current is still unmeasured) |
| Ground, any bay part → the Pi's ground pins | 2.5–5.3 mΩ | Negligible |

- **These figures already use the thin 15.2 µm inner copper.** The board needs no special copper order.
- **3.3 V is one connected net.** The In2 fill is in three pieces (621, 100 and 14 mm²), but vias and tracks join them. Almost all of the 174 mΩ is one track: 0.3 mm wide, 43.9 mm long, on In1 (166 mΩ). It is adequate for 70 mA.
- **Circuit.** THVD1451 pin use, receiver-only 120 Ω termination, the TX pull-ups, the fan switch with its diode the right way round, and the fan capacitor on the supply side of the switch all read correctly.
- **Audio clocks.** PCB-09 has no series resistors on BCLK, LRCLK or SDO0, and does not need them: the audio hub (BOM BO-067) carries a 33–100 Ω resistor in each clock branch.
- **Rule discipline.** Every via is the fab-neutral size and nothing is under 0.16 mm.

## P4. Findings

### P4.1 Three of J6's six pins have no protection — add series resistors

J6's lead runs to the rear-bay plate, where the INA226 module sits in the pack's positive line and the power switch carries pack voltage.

| J6 pin | Net | Between the pin and the Pi |
|---|---|---|
| 1 | Pi 3.3 V rail | Nothing |
| 2, 3 | GPIO16 (SDA), GPIO26 (SCL) | Nothing |
| 5 | `BTN_SENSE` | 2.2 kΩ (R8) |
| 6 | `PWR_OFF` | 1 kΩ (R9) |

- A chafed wire, or a solder bridge on the INA226 module, puts the fault straight onto the Pi's rail or pins.
- The INA226 draws about 0.3 mA, so resistance in its supply costs nothing.

Fix, three 0603 parts:
- 100 Ω in series with J6 pin 1. It drops 30 mV at 0.3 mA. A short to ground then draws 33 mA instead of pulling the Pi's rail down.
- 220–330 Ω in series with SDA and SCL, on the connector side of the pull-ups. With 4.7 kΩ pull-ups the low level rises to about 0.2 V, which is still a valid low.

These limit fault current to tens of milliamps. They do not make the pins safe against pack voltage held on them.

### P4.2 No labels on the board — add them

The silkscreen Gerbers hold part outlines only (54 strokes on top, 70 on the bottom). There is no text on any layer, and every reference name was moved to the Fab layer, which is not printed.

- D-073 selected "labelled SDA, SCL and GND service pads". TP1, TP2 and TP3 are unmarked.
- D-098 says to "label the four service nets so 3.3 V cannot be mistaken for Pi 5 V". J6 is unmarked.
- J3 and J6 are the same six-way header, about 12 mm apart. Swapping their plugs connects the base RS-422 cable to the service nets.
- TP5 (3.3 V) and TP6 (5 V) are identical 1 mm pads.

Fix: print the harness name and pin 1 at each connector (`J9-1`, `J9-2`, `J9-3`, `J9-4`, `J6 SERVICE 3V3`), the net at each test pad, and `PCB-09 B`. The fab-neutral rule allows 1.0 mm text.

### P4.3 Socket pads 0.17 mm from other tracks on the soldered side — shrink the pads

J1's body is on the bottom, so its 40 pins are soldered on the top face. The stock footprint's pads are 1.7 mm across with a 1.0 mm hole.

- 13 of those pads have the `HEAD_TX` track 0.174 mm away on the top face, where it runs between the two pin rows.
- The mask opening equals the pad (`pad_to_mask_clearance 0`), so that 0.17 mm of solder mask is all that separates a solder joint from the track. A fab's mask can sit 0.05–0.075 mm off (`E`, typical figure).

Fix: use a project copy of the socket footprint with 1.5 mm pads. The copper ring round the hole is still 0.25 mm, above the 0.16 mm rule, and the gap grows to about 0.27 mm. The strip's two middle lanes could then also carry 0.2 mm tracks.

### P4.4 R7 assumes a far-end circuit that does not exist yet — decide with the buffer

R7 pulls `BTN_SENSE` up to the Pi's 3.3 V through 10 kΩ. The far end is still "a high-impedance divider/buffer" to be measured and chosen (W40, D-098).

- With an open-collector buffer (a transistor that only pulls the line low), R7 is correct.
- With a plain divider from the switch's ON node, R7 fights the divider and the Pi reads a wrong level. With the Pi off, the divider would also feed current into the dead 3.3 V rail through R7, which D-098 forbids.

Fix: none on the copper. Record that R7 is fitted only for an open-collector buffer, and mark it "do not fit" in the BOM until the buffer is chosen.

### P4.5 Smaller points

| Item | Note |
|---|---|
| Rev B tracks on In2 | Five service tracks run 30–34 mm across the bay on the 3.3 V layer and cut the fill into ribbons. It still works (§P3). U2's supply now arrives by a 0.16 mm bottom-face track, 8 mm long (the extra 35 mΩ in the table) |
| Ground pins | 47 % of any bay return current uses header pin 34 and 51 % pin 39; the other six ground pins carry almost none. They are simply the nearest. Fine for the fan plus 70 mA |
| Minimum-width tracks | 104 of 209 segments are 0.16 mm wide. The strip needs that; the bay does not. Bay tracks can be 0.2 mm for a better yield at no cost |
| TP4 | On the underside, so unreachable once the board is on the Pi. It is the isolated spare, so nothing depends on it |
| Mating J6 | J6 is 18.6 mm beyond the last supported edge. A 10 N push (`E`) bends the bay about 0.2 mm there. Support the bay with a finger when plugging; the plan already mates J6 on the bench |
| Stale text | README line 3 says rev B is on branch `pcb-09-revB`; it is on `main`. The Layout section's totals (142 segments, 27 vias) are rev A's; rev B has 209 and 46. `layout_pcb09.py` says "U1 stays on B" but moves U1 to the top |

## P5. Is it the best design for its goal?

The goal: connect the Pi's header to two RS-422 links, the audio hub, the enclosure fan and (rev B) the rear service lead, in a 6.1 mm strip over the header plus a small bay.

| Function | Parts | Does the board add anything? |
|---|---|---|
| Two RS-422 links | U1, U2, R1–R4, C1, C2, J2, J3 | Yes: level conversion, termination, idle bias |
| Audio | J4 | Wires only, but needed: the socket covers the whole header |
| Enclosure fan | Q1, D1, R5, R6, C3, C4, J5 | Yes. The Pi's own fan header is taken by the Active Cooler |
| Rear service | J6, R7–R12, C5 | Yes: series parts and pull-ups (see §P4.1, §P4.4) |

### P5.1 The expensive choices are forced

- **Four layers.** The strip gives four track lanes per layer. Ten nets run its length and seven more leave it at the bay end. Two layers cannot carry them.
- **Parts on both faces.** The top of the bay is 57 % covered by connectors and their keep-clear margins. The underside parts need about 184 mm²; the top has 285 mm² free, but in fragments: one 6 × 5 mm space and nothing 8 × 6 mm, which U2 needs. One-sided assembly would need a larger bay, and the bay is already at the body frame.
- **Shape.** Set by the Pi, the cooler and the frame; checked in CAD by the project (not re-run here).

### P5.2 The battery monitor can have a hardware bus

Rev B reads the INA226 over `i2c-gpio`, a bus the Pi's processor toggles in software, on GPIO16 and GPIO26. D-098 chose it because I²C1's pins are at the far end of the strip and could not be routed.

The Pi 5 has a second hardware bus within reach: the overlay `i2c2-pi5` has a `pins_12_13` option. GPIO12 and GPIO13 are header pins 32 and 33, the pins rev B gives to the button and OFF. All four pins sit in the same four header columns.

| | Rev B now | Swap |
|---|---|---|
| Header 32 / GPIO12 | Button sense | I²C2 data |
| Header 33 / GPIO13 | M1 OFF | I²C2 clock |
| Header 36 / GPIO16 | Software I²C data | Button sense |
| Header 37 / GPIO26 | Software I²C clock | M1 OFF |

- Gain: a standard hardware bus with proper timing, instead of a bit-banged one. For one sensor read a few times a second the software bus will also work, so the gain is modest.
- Cost: re-route the four short runs in the bay, and change D-096, D-098, the 40-row table and the firmware notes. GPIO16 and GPIO26 have the same reset state as GPIO12 and GPIO13 (weak pull-down), so the OFF line's safe state is unchanged.
- Confirm which of GPIO12/13 is data and which is clock in the RP1 table before changing the schematic; I checked only that the overlay option exists.

This is the builder's decision. If rev B is being re-routed for §P4 anyway, it is cheap to do then.

### P5.3 What I would leave alone

- The 3.3 V feed. Feeding from pin 17 as well would halve its resistance, but it would cut the ground between the socket rows, and 12 mV does not need fixing.
- The In2 service tracks. Every other layer in the bay is busier.
- The transceiver, fan switch and connector choices.

## P6. Suggested order of work

1. Decide §P5.2 (hardware I²C swap) first, because it changes the same nets as step 2.
2. Add the three series resistors at J6 (§P4.1).
3. Make the project socket footprint with 1.5 mm pads (§P4.3) and widen bay tracks to 0.2 mm where they fit (§P4.5).
4. Add the labels (§P4.2).
5. Mark R7 "do not fit" until the button buffer is chosen (§P4.4).
6. Correct the stale text (§P4.5).
7. Re-run ERC, DRC, the netlist audit, the export, `check_pcb09_fit.py`, `check_pcb09_mount.py` and `check_pcb_integration.py`.

## P7. Not checked

- ERC, DRC, the netlist audit and fab regeneration (skipped on request).
- The CAD fit, mount and integration checks; I read that they pass but did not re-run them.
- Anything physical: socket seating, plug access, fan current, boot behaviour of GPIO13 or GPIO26.
- India stock for any part.

---

# PCB-12 rev A and PCB-11 rev A — head electronics review (2026-11-17)

The saved PCB-12 board is `c527eb17…7fc4b31c` (SHA-256; last changed by `74c222a3`, 2026-11-10). PCB-11 is `c833de8d…a1b3aa6` (SHA-256). This review changes neither design nor fab output.

## H1. Verdict

**PCB-12's copper matches its schematic and the D-107 W47 connector map, but the head electronics are not ready to order.** K2 (status LED driver) and K3 (display power inlet) are still open. The 0 Ω servo-reference link also needs a deliberate return-current choice. PCB-11's tiny circuit checks out; its driver ownership and wire termination remain the practical issues.

## H2. Evidence checked

| Check | Result |
|---|---|
| KiCad 10.99.0 Nightly ERC, all severities | 0 violations on each schematic |
| KiCad 10.99.0 Nightly DRC with schematic parity, all severities | PCB-12: 0 violations, 0 unconnected, 0 parity. PCB-11: 2 `lib_footprint_mismatch` warnings (C1/R1), 0 unconnected, 0 parity |
| Fresh schematic netlist exports; PCB-12 `audit_netlist.py` | Fresh exports confirm PCB-12 J1/J2/J3/R7 and PCB-11 LED/P1–P3 pin maps. The saved PCB-12 audit passes 13/13 checks on 76 connected pins. `audit_w47.py`'s saved output passes all five PCB-08/12 interface checks, but explicitly leaves K2/K3 open |
| Cross-check | D-102 and D-107, W47 table in `05-harness/README.md` §4.3, both board READMEs, circuit manifest, PCB-11 fab notes, earlier PCB-08 review §5.2 |

These checks prove board/schematic parity and the recorded pin map. They do not prove the external head wiring, servo return currents, received Zero footprint or the fitted display inlet. Fab outputs and physical fit were not regenerated in this pass.

## H3. Findings

### H3.1 K2: choose one status LED source before PCB-12 release

PCB-11 needs `+3V3`, GND and DIN. PCB-12 rev A uses GPIO1, 2, 4–9 and has no LED wire pad or connector. The D-107 plan says a spare C2 pad on PCB-12 should drive the LED, yet the older PCB-11 README assigns its three wires to D1's `Sensor AD` J6 (3V3, GND, GPIO6). Those are competing interface descriptions. The KiCad checks cannot resolve the missing connection.

The simpler candidate is the existing D1 J6 path, **if the received display actually has that header, GPIO6 is free, and its 3.3 V output can supply the V6 LED**. It keeps PCB-12 unchanged and gives data and LED power the same source. Record the D1 connector/cavity map, a head-local three-wire route and firmware ownership. If that path fails the received-board check, assign an agreed C2 GPIO, add a PCB-12 wire landing with strain relief, and revise its schematic, layout, audit and fab files. Do not use GPIO3 casually; D-102 deliberately left that strapping pin unused.

### H3.2 K3: D1 power remains a harness gap

W47 provides `+5V_DISPLAY` and `GND_DISPLAY` directly to D1, while PCB-12 J3 carries only RS-485 B/A and a ground reference. The actual display power connector or pads and their polarity are absent from the build record. Identify them on the received D1 or its exact schematic, then add the cavity/pad map to W47 and the bring-up check. This needs no PCB-12 copper change if the current signals-only architecture is retained.

### H3.3 R7 can put servo return current through a GH reference pin

PCB-12 J2.1 reaches C2 GND through R7, a fitted 0 Ω 0603, on a 0.3 mm top track. `GND_HEAD` and the other returns also join at the supply star. The earlier PCB-08 review §5.2 estimates roughly 0.9–1.1 A through the parallel thin reference branch at the 2.4 A servo allowance; that is an estimate, not a measurement, and is at or above the cited 1 A GH contact rating. Recheck the actual W47 lengths/contacts and measure J2.1 current at servo load. Decide whether to fit a DC resistor at R7 to limit sharing, while checking servo-bus voltage levels, or intentionally size the branch and contact for the measured current. A ferrite does not limit DC sharing. Keep R1/R10 in the same return-path calculation.

### H3.4 Assembly and physical acceptance

The 20 mm lower carrier extension is estimated to deflect 0.7 mm under a 5 N mating force. Support its back while mating J1–J3 and check the printed bosses with real plugs. PCB-11 has three 0.8 × 1.2 mm back pads only 0.3 mm apart, without silkscreen names; use a keyed assembly drawing showing P1 `+3V3`, P2 GND, P3 DIN, solder the AWG30 wires before installing the board, and anchor the cable at the socket so pulls do not peel the pads. Confirm the V6 part number `C52917434`, since the earlier LED is not rated for the selected 3.3 V supply.

### H3.5 PCB-12's order note still describes the old FFC route

The board README's historical Inputs section and `fab/revA/README.md`'s "Before ordering" list still call for a W42/W43 FFC-to-wire break and PCB-14 gates. D-107 replaced that route with W47, and PCB-14/16 are removed. Update the active order instructions to K2, K3, W47 connector/branch dress and the actual head fit checks so an assembler does not follow superseded wiring. Keep the history clearly dated.

## H4. Release sequence

1. Resolve K2 with the received D1 header check; revise PCB-12 only if D1 cannot drive PCB-11.
2. Resolve K3 from the received D1 power inlet, including polarity and the display's 5 V current.
3. Decide R7's population from a return-current calculation and bench measurement; confirm the servo-bus levels.
4. Replace the superseded FFC/PCB-14 instructions in the active fab note. Re-run the PCB-12/W47 netlist audit, ERC, parity DRC, fab export and head fit for any changed board. Verify PCB-11 pad wiring, V6 part and two-sided assembly preview.

---

# PCB-10 rev A — C3 carrier review (2026-11-17)

Saved board `c2dac029…7746` (SHA-256), last changed by `1a1ddbe8` on 2026-10-28. D-093 and D-106 came later. No board or fab files were changed in this review.

## C1. Verdict and checks

**The board still satisfies its own electrical design, but the D-093 supply change added an apparently redundant external diode, and the board is poorly marked for assembly and service.** Four layers remain justified by the unchanged DevKitC pin fences and signal count; D-093 removed the external permit chain, not the retained watchdog, sleep gate, ten connector footprints or most of their routing.

KiCad 10.99.0 Nightly ERC found 0 violations. Parity DRC found 0 errors, 0 unconnected and 0 parity issues. Its 61 warnings are the 57 recorded footprint-copy mismatches and four J1 silkscreen segments clipped at the edge; none is a copper clearance hit. The exported schematic netlist confirms D1 pin 2/anode on `+5V_IN` (J10-1.1), pin 1/cathode on `+5V_DK` (DevKitC 5 V pin). The saved fab notes and the schematic agree on the diode and on J10-12 being fitted. I did not regenerate the Gerbers or re-run the whole-robot CAD.

## C2. Findings

### C2.1 W11's added SS34 duplicates the on-board back-feed block

D-093 added an SS34 in W11 to stop service USB feeding the shared buck. PCB-10 already has B5819W D1 in series from J10-1 to the DevKitC 5 V pin, with its cathode toward the DevKitC. That diode blocks the direct USB-to-J10-1 path on the saved schematic and board. W11's SS34 is therefore redundant for the stated fault path and adds another forward drop during normal running. N8 requires **at least 4.5 V at the DevKitC 5 V pin** under load; two diodes from a nominal 5 V module leave little margin.

Recommended harness correction: test N8 with the **on-board D1 only**, measuring J10-1, the DevKitC 5 V pin, M5 output and switched bus in both loaded and USB-service/off states. If the off-state bus stays at 0 V, remove the W11 SS34 and update its harness/BOM records. If another back-feed path appears, keep protection but solve it from measured voltages, not the assumed direct path. This is a harness/assembly decision; the PCB-10 copper need not change.

### C2.2 J10-12 is still populated although D-093 retired it

The GH4 J12 is on the board and in the rev A fab BOM/CPL, but W39 is deleted and the header is unmated. GPIO17's `MOTOR_PRESENT` is pulled low through R43, and `C3_READY` still serves the on-board U4 gate. Firmware requirement FW-B2 already says low is normal. Mark J12 **do not fit** in the assembly data and remove it from the fab BOM/CPL, unless a defined service use is wanted; keep R42/R43 and the internal READY circuit. This saves an unused part and removes an attractive wrong-plug destination without a PCB re-spin.

### C2.3 No usable board labels

The fab silkscreen is footprint outlines only; references are on Fab, which is not printed. Ten GH headers, a two-way power header and eight test pads therefore have no harness, pin-1, polarity or signal labels. Several GH sizes repeat. Add labels to the board before ordering, at least `J10-1 +5V/GND`, the J10 harness names, `J10-12 UNUSED` if fitted, TP rail names, and `PCB-10 A`. The J1 clipped outline warnings can be cleared while editing silk. This is a board revision and requires re-export and DRC.

### C2.4 D-106 motor-inline overlap was a harness placement fault

D-106 found the right motor's original inline pair overlapping PCB-10/J10-1 and moved that pair on top of the motor-driver board. Its saved route check reports 134/134; the current chassis-harness report in the working tree reports 80/80. That resolves the recorded clash in CAD without changing PCB-10. Confirm the physical inline pair and wire bend against the real J10-1 plug during assembly; the original 2026-10-28 PCB-10 fit did not include the D-106 pair.

### C2.5 Fab notes still name PCB-04 as J10-1's source

The PCB-10 README's connector table still says J10-1 mates PCB-04 `J4-4`; the active supply is the bought M5 through W11. Its fab notes correctly describe the saved copper but do not record D-093's external diode and J10-12 retirement. Refresh the active order and assembly instructions after C2.1/C2.2 are decided so the ready-looking rev A package cannot be ordered to the old connection plan.

## C3. Order work

1. Settle the single-diode W11 arrangement with N8 and correct harness/BOM text.
2. Mark J12 DNP in the PCBA data, while retaining its pull-down and firmware rule.
3. Add the board labels and update the PCB-04-era order notes; rerun ERC/parity DRC, regenerate Gerbers/BOM/CPL, and check the fab preview.
4. Recheck the D-106 right motor plug against the assembled PCB-10/J10-1 envelope.

---

# PCB-15 rev A — nose Hall quick review (2026-11-17)

Saved board `da5333ea…9157` (SHA-256). KiCad 10.99.0 Nightly ERC: 0 violations; parity DRC: 0 errors, 0 unconnected, 0 parity, four recorded footprint-copy warnings. A fresh schematic netlist export confirms P1 `+3V3`, P2 GND and P3 `HALL_OUT`; the harness maps them to J10-8.4/.2/.5. D-106 routes the same W34 nose cable and reports the tunnel/bore clear.

The three back pads are each **0.8 × 1.2 mm**, 1.1 mm centre to centre (0.3 mm copper gap), at the top lead groove. The board has no printed polarity or pad labels; its fab silk has only 0402 body marks. Put a back-face P1/P2/P3 diagram in the W34 build sheet, check the actual received pre-crimp conductor diameter and insulation against these pads and the groove, then solder and glue/strain-relieve the leads before the board is seated. The repository records W34 as an existing 220 mm GH5 lead but does not record its conductor gauge, so wire fit cannot be certified from files alone. The 0.8 mm board still needs a panel and a two-sided assembly quote as its fab note says. No circuit or board change is indicated by this quick review.
