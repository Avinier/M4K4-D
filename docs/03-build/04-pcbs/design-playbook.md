# Board design playbook (stage 1)

How one custom board goes from spec to a committed revision. The steps were worked out on [PCB-15](pcb-15-nose-hall/README.md) and refined on [PCB-11](pcb-11-status-led/README.md) and [PCB-06](pcb-06-pdm-mic/README.md); PCB-15 was designed 2026-10-14 to 10-25 in the Claude Code session `makad-a2`. They follow [workflow.md](workflow.md) stage 1, the [layout rules](README.md#layout-rules) ([D-060](../decisions.md#d-060)) and the [fab-neutral design rules](README.md#fab-neutral-design-rules) ([D-062](../decisions.md#d-062)). Boards are designed one at a time and procured together afterwards ([D-064](../decisions.md#d-064)).

**Teaching.** The builder is new to PCB design and learns as each board is made. Explain each step from first principles before doing it, one lesson per step. Say why each part and each rule exists, and stop at the steps where the builder must act or decide. PCB-15 went in six lessons: what a PCB is, the circuit, the envelope, the schematic, the layout, and the checks and outputs. Later boards can skip what is already taught and spend the time on what is new to that board.

## 1. Freeze the inputs

- Read the board's spec, its register row in [README.md](README.md#board-register), the decisions it cites, and the CAD placeholder in its subsystem source.
- **Measure the envelope in CAD, not just the spec.** Take the placeholder's world box, and the openings around it on every face where parts must fit. PCB-15's spec put three parts against solid seat wall, because the CAD drew the board as a plain block ([D-059](../decisions.md#d-059)).
- Check every pinout against the datasheet (TI's PDFs download with a browser user agent).
- Write the inputs into the board README: sources, circuit table, interface, supply and protection, envelope, and gaps. An envelope change needs a decision before layout. Droid CAD changes go in `final/v1/cad` only: `DROID_CUTS`, `DROID_ADDS` and `DROID_MOVES` in `makad-v1.step.py`, each with a check script.

## 2. Schematic

- Project in the board's `design/`: `<board>.kicad_pro`, `.kicad_sch`, a project `fp-lib-table`, and project footprints in `<short>.pretty/`. Use the KiCad 10.99 nightly; its files may not open in 10.0.6.
- Use stock KiCad symbols where they exist. For a derived symbol, embed the base symbol's body with the derived symbol's own properties, or ERC reports a library mismatch.
- Name every net. Put `PWR_FLAG` on each power net that enters through a connector or pad, so ERC knows it is driven.
- Mark bare-copper pads (wire pads, test pads) "not in BOM". Their footprints must also be left out of position files: see the F8 trap below.
- `kicad-cli sch erc --severity-all` must give **0 errors and 0 warnings**. Export the netlist, check it against the spec row by row, and record the check in the README.

## 3. Board set-up (before any part is placed)

- Outline on `Edge.Cuts` with a simple mapping from KiCad to board-local coordinates. Put the aux and grid origins at local (0, 0).
- Stackup and thickness from the spec. Rules: copy [PCB-15's `.kicad_dru`](pcb-15-nose-hall/design/pcb-15-nose-hall.kicad_dru), which holds the fab-neutral minimums (vias 0.67/0.35 mm, gap 0.16, edge 0.3).
- **Mechanical envelope as rule areas.** Add footprint keep-outs wherever the enclosure leaves no room, and draw the openings on user layers. DRC then checks the fit on every run.
- Make a custom footprint when the stock one doesn't fit the envelope, and record why. PCB-15's SOT-23 toes were trimmed to fit a notch.

## 4. Layout

- The builder opens the project in the **nightly**, opens the PCB editor, presses **F8** (Update PCB from Schematic) and saves. KiPy cannot open files or press F8.
- Drive the open board with [`tools/kp.py`](tools/kp.py) from the KiPy venv: `place()`, `track()` (octolinear only), `via()`, `refs_to_fab()`, `exclude_from_pos()`, `audit()`, `save()`, `drc()`.
- Place parts one at a time or in functional groups, reading the pad positions back after each. Run DRC after placement, before routing.
- Route the fan-out first (short stubs and vias), then each net. Size tracks for the current: 0.2 mm is plenty at a few mA, and power paths are sized and routed by hand first. Nudging placement during routing is fine. No autorouter.
- DRC with `--schematic-parity` must give **0 errors and 0 unconnected**. Explain every warning that remains.

## 5. Checks and outputs

- `audit()`: every footprint has its library 3D models, and bare-copper footprints are left out of position files.
- Export the board STEP to `cad/<board>-revX.step`, and check it lists the parts (`grep PRODUCT`). A 0.04 s export means no models.
- **Fit check in the robot.** Place the STEP in its subsystem with a script in `final/v1/cad`, as [`check_pcb15_fit.py`](../final/v1/cad/check_pcb15_fit.py) does. It checks against the enclosure and against anything that moves near the board. KiCad's STEP puts the core at Z 0–(thickness − copper), flips Y, and sets components about 0.085 mm off the core. Use real part heights and tolerances for the margins, not only the CAD placeholder: PCB-15's fit check found the magnet could hit the sensor ([D-063](../decisions.md#d-063)).
- Fab outputs to `fab/revX/`: Gerbers (`F/B.Cu`, `Mask`, `Paste`, `Silkscreen`, `Edge.Cuts`), Excellon drill in mm, the position file in CSV (plus JLCPCB's CPL columns), the BOM, a zip, and a README with the order parameters and the open stage-2 items.
- Update the board README (stage table, layout, checks, log), the [workflow.md](workflow.md) tracker and the register row. Commit the revision when the builder asks.

## Traps found on PCB-15

| Trap | What happens | Handling |
|---|---|---|
| KiPy `flip_items()` | Strips the footprint's 3D models. The STEP has no parts, and DRC shows `lib_footprint_mismatch` | `kp.place()` restores models from the library; check with `audit()` |
| F8 (Update PCB from Schematic) | Resets footprint attributes from the symbol, dropping "exclude from position files" | `kp.exclude_from_pos(...)` after every F8 |
| Rotated footprints | About 1 nm of round-off in fab and courtyard lines leaves a cosmetic `lib_footprint_mismatch` | Explain it in the README; pads and models still match |
| Silkscreen on small boards | JLCPCB's minimum text is 1.0 mm | `kp.refs_to_fab()` |
| `.kicad_pro` while KiCad is open | KiCad may rewrite it | Edit project rules only with KiCad closed; board rules live in the `.kicad_dru` |
| CAD placeholder heights | The placeholder had a 1.0 mm block; the real part is up to 1.12 mm, and KiCad's model 1.2 mm | Fit check with datasheet maximums and board thickness tolerance |

## Traps found on PCB-11

| Trap | What happens | Handling |
|---|---|---|
| Envelope checked by part height only | PCB-11's 0402s fitted the socket cavity by height, but their courtyards did not fit beside the centred LED. The parts moved to the back at layout (D-065 amended) | When freezing an envelope, check footprint areas (courtyards) as well as heights against every face that carries parts |
| Stock footprint without its 3D model | KiCad's `LED_WS2812B-2020_PLCC4_2.0x2.0mm` names a model the library doesn't ship, so the board STEP has no LED | Copy the footprint into the project library with a project model built from the datasheet; check the STEP's `PRODUCT` list |
| Placement file and Gerbers in different frames | With the aux origin at board-local (0, 0), `pcb export pos --use-drill-file-origin` is local, but the Gerbers and drill default to absolute, so the fab's preview misplaces parts | Export the Gerbers with `--use-drill-file-origin` and the drill with `--drill-origin plot`, so all files share one origin |

## Traps found on PCB-06

| Trap | What happens | Handling |
|---|---|---|
| Rules file on a scratch copy | KiCad loads only the `.kicad_dru` named after the board. A scratch `test.kicad_pcb` beside `<board>.kicad_dru` runs DRC with **no custom rules, silently** | Copy the `.kicad_pro` and `.kicad_dru` under the scratch board's name, and make one test that only a custom rule can catch |
| One design in mirrored positions | Four boards, left and right of the body, with the lead side toward the centre: two mount turned over, so an obstacle above the board at one position is below it at another | Measure every position in lesson 1 and lay out against the envelope folded about the board's axis. The fit check places each orientation from one plane (lead direction, inboard normal) and lets the third axis follow |
| Datasheet land pattern vs fab-neutral rules | Infineon's GND seal ring sits 0.18 mm from the Ø0.8 non-plated sound hole: under JLCPCB's 0.2 mm and the fab-neutral 0.31 mm | Put each new footprint on a scratch board with the rules file before placing. A scoped exception (one footprint's own hole) is a decision, recorded with the fabs' published limits |
| Track ending on a custom pad's shape | A track started on the seal ring's copper (a custom pad's circle primitive), not on its anchor, reads as dangling and unconnected | Start and end tracks on the pad's anchor point |
| No-via zone round a feature | Vias banned within 3.8 mm of the port forced every net out of the mic on F.Cu, which fixed the pin escape order. At a 1.4 mm wire-pad pitch, two nets had to cross at the middle pads | Plan the routing before fixing a connector's pad pitch. Here the pads went to 2.2 mm, so a via fits in each gap |
| Fit-check columns | A lowering sweep built from each part's own bounding box can only find clashes; the clearance to what passes above reads "none" | Build the column from the board face outward (n 0 to a few mm) over the part's footprint, and compare datasheet maximum heights with the nearest obstacle |

## Traps found on PCB-05

| Trap | What happens | Handling |
|---|---|---|
| Envelope checked against CAD placeholder bodies | The lesson-1 spacer check passed against the CAD's GH header boxes, but the real footprints' pads run 1.1 mm further inboard, so the spacers' rings landed on signal pads; the Micro-Fit block was 2.4 mm narrower than the part. Found only at placement, after the CAD fixing was committed (D-067 amended) | When freezing the inputs, place the fixed parts' real footprints (connectors, mounting) on a scratch board and DRC them before committing CAD that depends on their positions |
| Stock land patterns that fail fab rules | KiCad's Würth WA-SMSI spacer footprints put their solder ring at their own NPTH's edge (0 mm) | DRC every stock footprint on the scratch board at set-up; copy and fix it in the project library (PCB-05 plated the hole) |
| Through-hole parts over something close below | THT tails stick out about 1.6 mm under a 1.6 mm board | A B.Cu rule area with pads not allowed over the low-clearance zone; notch it only for parts with a recorded decision |
| One-line `(model …)` in a project footprint | `kp.library_models()` parsed only the multi-line form, so `place()` never restored the ADAU7002's model and U1/U2 had none; the board STEP would have lost both chips | Fixed in `kp.py` (balances parentheses); run `audit()` before the fit check, and expect n/n for every project part |
| The fab-neutral via rule is via copper to other copper | 0.31 mm from the via's ring, not its hole: two vias can't sit between In2 rows 1.25 mm apart, and five vias failed by 0.01–0.12 mm | Plan via sites at ≥ 0.31 + 0.335 + half the track width from neighbours; leave via room when spacing parallel rows |
| Signal layer next to the plane you think is the reference | On a 1.6 mm 4-layer board, B.Cu is 0.21 mm from In2 and 1.3 mm from In1, so tracks on In2 slot the return path of a B.Cu bus where they cross under it | Keep the layer next to a fast bus free of crossings, or stitch GND vias beside each slot |
| Test-pad courtyards | `TestPoint_Pad_D1.0mm` has a Ø2 courtyard, twice the pad, so test pads crowd small parts | Place test pads last, at ≥ 1 mm courtyard radius from everything |
| Stock models that don't ship, again | PCB-11's trap hit twice: `TQFN-16-1EP_3x3mm_P0.5mm_EP1.23x1.23mm` names a model the library lacks (only EP1.6 ships), and KiCad has no Micro-Fit models at all. `audit()` passed, because it compares the board with the library's *names*; only the STEP export's "File not found" and its `PRODUCT` list showed the gap | At set-up, check every footprint's model file exists on disk, not just that one is named. `audit()` now flags a named model whose file is missing. Fix with a project footprint copy: a stock model of the same body, or one built from the drawing |

KiCad keeps local history in `design/.history/` (git-ignored). `git log` there shows which save changed what.
