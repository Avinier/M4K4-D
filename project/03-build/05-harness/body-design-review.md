# Body harness design review — 2026-11-15/16 (updated after the open items)

CAD disposition of the body harness after [D-109](../decisions.md#d-109), following [body-harness-plan.md](../body-harness-plan.md) Levels 0–6. `E` means an assumed envelope, length or mass; nothing here is a measured part, a crimp, or a physical fit.

## Completed

| Level | Result | Evidence |
|---|---|---|
| 0 Cleanup | Stale Layout-02 reserves dropped from the droid tree: W40 leads to the deleted PCB-02 J2-9, the Pi pigtail drop to the deleted PCB-04 J4-1, and all three old −Y head-riser boxes (one sat inside the moved J8-1 plug). Every body-harness endpoint now resolves from the live tree with an exit direction | `body_harness_endpoints.py`; [check_body_endpoints](../final/v1/cad/check_body_endpoints-report.json) **47/47** |
| 1 Decisions | B-01…B-10 recorded as D-109 | [decisions](../decisions.md#d-109) |
| 2 Placements | Eight envelopes: − charge splice; shared-5 V ± splices and the potted SS34 under the tray; the J6 rear break (Micro-Fit 3.0 1×6) above M6; audio hub v2 (18.5 × 23, four 2×3 latching mic headers, cradle + VHB, no screws); W28 speaker break. The button-buffer reserve moved out of the mushroom keep-out | `d109_body_parts.py`; [check_d109_placements](../final/v1/cad/check_d109_placements-report.json) **8/8**; rear bay 23/23, tray 24/24, amp mount 10/10, D-106 134/134, chassis harness 15/15 unchanged |
| 3 Route reserves | 64 boxes, 31 chains, endpoint to endpoint, clear of every printed part, module, vendor STEP and the **rev B** PCB-08 plugs | `d109_routes.py`; [check_d109_routes](../final/v1/cad/check_d109_routes-report.json) **95/95** |
| 4 Visible wires | `Harness → Body wires` (31 envelopes in six groups) beside head and chassis wires; focused `body-harness.step.py` | [iso](../final/v1/cad/snapshots/body-harness-iso_20261115T191424Z.png), [top](../final/v1/cad/snapshots/body-harness-top_20261115T191440Z.png) |
| 5 Neutral checks | Each wire clear of the assembly (endpoint parts allowed), no segment reversal > 120°, B-09 ≥ 5 mm signal/audio-to-power except shared corridors, same-module ends and one named crossing (W40 control tail beside W05 at the M1 face, 3.5 mm) | [check_body_harness](../final/v1/cad/check_body_harness-report.json) **77/77** |
| 5 Head harness | Body wires vs the D-107 W47 run, stripped HDMI and Pi camera FPC (visible-harness solids): no overlap, ≥ 0.5 mm nominal gap. W24 lowered under the HDMI pairs (0.71 mm, signal beside signal, tied); W25 moved outboard of the FPC (1.64 mm) | [check_body_vs_head](../final/v1/cad/check_body_vs_head-report.json) **31/31** |
| 5 Service | Tray slide (front, 90 mm, 2 mm lift) meets only W10 and the four PCB-09 leads (unplugged first) and W28 (off with the speaker); rear-panel withdrawal: W04 98 mm vs 53 mm needed, W40 mushroom lead via a 2-way header at the buffer; body-lift slack ≥ 40 mm on all five body-lift chains; PCB-08 removal: W17 227 mm vs 111 mm needed. **Shell lift fails** (F2) | [check_d109_service](../final/v1/cad/check_d109_service-report.json) **10/13** |
| B-05 Tie lugs | Two fused 4 × 4 × 3 lugs with 3 × 1.5 tie tunnels on `BODY_FRAME_MAIN_PRINT` (+Y mic runs). A riser lug was rejected: it blocked the J8-1 pull and PCB-08 removal. Other runs tie to each other and to module cradles | `study_d109_tie_lugs.py` → `d109-tie-lugs.json`; D-107 body 31/31, body wires 77/77 with lugs |
| Cut list | Chassis + W47 + head fan-out + body from CAD centrelines: 83 rows, 3.1 / 3.0 / 0.4 / 3.6 m `E` | [harness-cut-list.csv](../final/v1/cad/harness-cut-list.csv) |
| 6 Mass | Routed body harness **50.7 g** `E` (38.6 g conductors + 3 g ties + 9.1 g breaks/splices) replaces that share of the 95 g `HARNESS_AND_FASTENERS` allowance; 44.3 g stays for fasteners/clips | [check_d109_mass](../final/v1/cad/check_d109_mass-report.json) 3/3 |

## Findings

| # | Finding | Disposition |
|---|---|---|
| F1 | **Tipping margin.** Moving 50.7 g from the allowance centroid (20, 0, 88) to the routed positions shifts the CoM 0.42 mm rearward. The full 1,068,120-pose sweep (`MAKAD_D109_MASS=1 check_d107_mass.py`) gives worst-pose margin **steel 2.15 %**, **copper 3.72 %** (was steel 4.59 %). Steel is above the 1.5 % operating minimum but below the 3 % release buffer, so the D-107 rule selects **copper ballast** again. The original-register all-10 g-in-head case falls to −0.03 % | Copper ballast (C110) retained as the release configuration; [report](../final/v1/cad/check_d107_mass_d109-report.json). Weigh the real harness and re-run; the allowance centroid was itself `E` |
| F2 | **Shell lift: OPEN.** The W27 plug must be drawn back along its route as the shell lifts. FR and RR pass 2.5–3.7 mm passages (around PCB-10's +X end and outboard of its uprights); RL passes 3.5 × 5.5 mm under the fan web roots. A 2×3 plug (5.6 × 8.1 `E`) does not fit. A mic-end break was screened and rejected: anything riding with the shell inboard of \|Y\| 70.3 hits the upper side rail while lowering | Resolve in the D-037 shell mock-up: a smaller plug (≤ 2.4 mm section is unlikely), re-routing the three leads through wider passages, or a local frame relief. Do not print the shell first |
| F3 | **J10-1 exit blocked.** The C3 J10-1 right-angle plug's rear (+X, X 68) faces the `C3_CARRIER_EDGE_CONNECTOR_J101_RESERVE`. W11 is drawn turning straight down at the plug | Measure the received Molex plug and J101 use; reroute or flip the header if the wires cannot turn within the plug's strain-relief length |
| F4 | **PCB-08 rev A parts remain in the droid tree** (`YAW_JUNCTION_J8_*`); rev B comes in through `pcb_integration`. Body checks ignore the rev A shapes and test against rev B positions copied from `check_d107_body` | Remove the rev A connector shapes from the droid tree in a later cleanup |
| F5 | **W17 pads.** Rev B's J6 pads sit at about world (−6, −43.4) on the board top (layout_pcb08.py), not at the −Y edge; W17 drops onto them. W17 leaves with PCB-08 after `J-S18-Y` is unplugged (60 mm service allowance) | Sweep the PCB-08 removal path with W17 attached (Level 5 remainder) |
| F6 | **B-03 resolved: keep roles.** Swapping M4/M5 saves about 35 mm in total and moves the shared node away from its two −Y loads (C3, J8-1). W10 crosses under the tray at X 5.5–10 and drops through the old Pi pigtail passage | Recorded in D-109 |
| F7 | **`check_pcb09_*` failed at import** since D-107 (`KeyError: 'makad_v1_entry'`) | **Fixed**: the three checks register the entry module; fit now uses the D-109 J6 route: fit 8/8, mount 7/7, inputs survey runs |
| F8 | The routed body wires are ~40–70 % shorter than the old whole-run `E` cut allowances for their body portions | 05-harness §4.4 now lists CAD-derived body cuts |

## Still open

| Item | Why it matters |
|---|---|
| F2 shell-lift plug passage | Blocks a shell print; physical mock-up decides |
| F3 J10-1 lead exit | Needs the received plug |
| F4 rev A PCB-08 shapes in the droid tree | Cleanup; checks already use rev B |
| Whole-robot STEP | Rebuilt 2026-11-16 with D-109 (see final/v1 README); presentation STEP not rebuilt |
