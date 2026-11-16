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
| 5 Head harness | Body wires vs the D-107 W47 run, stripped HDMI and Pi camera FPC (visible-harness solids): no overlap, ≥ 0.5 mm nominal gap. W24 lowered under the HDMI pairs (0.71 mm, signal beside signal, tied); W25 moved outboard of the FPC (1.64 mm) | [check_body_vs_head](../final/v1/cad/check_body_vs_head-report.json) **35/35** (incl. the shell-dressed runs) |
| 5 Shell-dressed W27 | Each mic lead leaves its mic down the board's inboard face in a notch cut in the boss, then is clipped to the shell skin (front leads Z 103, −Y rear Z 106 under the front bosses, +Y rear over the fan collar at Z 126.6 then Z 106) to the open front at X 77.5. Leads and clip envelopes clear skin and mic parts and ride the shell through 0–140 mm of lift. Free tails: open front → over the hub bracket → headers, every box ≥ 5.6 × 8.1 | `study_d109_mic_leads.py` → `d109-mic-leads.json`; [check_d109_mic_leads](../final/v1/cad/check_d109_mic_leads-report.json) **16/16**; mic bosses 64/64 |
| 5 Service | Tray slide (front, 90 mm, 2 mm lift) meets only W10 and the four PCB-09 leads (unplugged first) and W28 (off with the speaker); rear-panel withdrawal: W04 98 mm vs 53 mm needed, W40 mushroom lead via a 2-way header at the buffer; body-lift slack ≥ 40 mm on all five body-lift chains; PCB-08 removal: W17 227 mm vs 111 mm needed. shell-lift tail passages pass | [check_d109_service](../final/v1/cad/check_d109_service-report.json) **13/13** |
| B-05 Tie lugs | None fused: the two earlier lugs served W27 runs that are now shell-dressed; a riser lug blocked the J8-1 pull and PCB-08 removal. Frame runs tie to each other and to module cradles; shell runs use adhesive cable clips | `study_d109_tie_lugs.py` (no qualifying position) |
| Cut list | Chassis + W47 + head fan-out + body from CAD centrelines: 83 rows, 3.1 / 3.0 / 0.4 / 3.6 m `E` | [harness-cut-list.csv](../final/v1/cad/harness-cut-list.csv) |
| 6 Mass | Routed body harness `E` (conductors + ties + breaks/splices, see report) replaces that share of the 95 g `HARNESS_AND_FASTENERS` allowance; 44.3 g stays for fasteners/clips | [check_d109_mass](../final/v1/cad/check_d109_mass-report.json) 3/3 |

## Findings

| # | Finding | Disposition |
|---|---|---|
| F1 | **Tipping margin.** The routed body harness (now with shell-dressed W27) gives a worst-pose margin of **steel 2.79 %**, **copper 4.36 %** (D-107 baseline steel 4.59 %); the original-register all-10 g-in-head case is 1.68 %. Steel is below the 3 % release buffer, so the D-107 rule selects **copper ballast** | Copper ballast (C110) retained; [report](../final/v1/cad/check_d107_mass_d109-report.json). Weigh the real harness and re-run |
| F2 | **Shell lift: resolved in CAD.** Hub-end plugs could not be drawn back through the 2.5–3.7 mm frame passages, and a mic-end break hit the upper side rail. The leads are now clipped to the shell skin in the band outboard of the frame (where the mic boards already pass) and only free tails reach the hub | Physical: confirm clip adhesion on PETG and the shell mock-up (D-037) before printing |
| F3 | **J10-1 exit: false alarm, resolved.** The "J101" box is `C3_POWER_PLUG_RESERVE`, J10-1's own plug/lead reserve moved down with the real Micro-Fit. W11 leaves the plug rear into it and turns down | Endpoint now includes the reserve |
| F4 | **PCB-08 rev A in the droid tree: resolved.** `module_checks.droid_tree()` now swaps in the rev B board and plugs the way the full build does; the D-107 checks that install rev B themselves opt out (`revb_pcb08=False`) | All checks re-run on the new tree |
| F5 | **W17 pads.** Rev B's J6 pads sit at about world (−6, −43.4) on the board top (layout_pcb08.py), not at the −Y edge; W17 drops onto them. W17 leaves with PCB-08 after `J-S18-Y` is unplugged (60 mm service allowance) | Sweep the PCB-08 removal path with W17 attached (Level 5 remainder) |
| F6 | **B-03 resolved: keep roles.** Swapping M4/M5 saves about 35 mm in total and moves the shared node away from its two −Y loads (C3, J8-1). W10 crosses under the tray at X 5.5–10 and drops through the old Pi pigtail passage | Recorded in D-109 |
| F7 | **`check_pcb09_*` failed at import** since D-107 (`KeyError: 'makad_v1_entry'`) | **Fixed**: the three checks register the entry module; fit now uses the D-109 J6 route: fit 8/8, mount 7/7, inputs survey runs |
| F8 | The routed body wires are ~40–70 % shorter than the old whole-run `E` cut allowances for their body portions | 05-harness §4.4 now lists CAD-derived body cuts |

## Still open (physical only)

| Item | Gate |
|---|---|
| Shell-dressed W27 | Adhesive cable clips on the PETG skin and lead dress, in the D-037 shell mock-up before printing |
| Copper ballast | Weigh the built harness, re-run `MAKAD_D109_MASS=1 check_d107_mass.py`; steel only if ≥ 3 % |
| Received parts | C-Grid III 2×3, Micro-Fit 3.0 1×6 AWG26–28, 2-way speaker and buffer breaks, J10-1 plug lead exit; measured cut lengths (`W`) |
