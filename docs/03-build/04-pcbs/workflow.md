# PCB workflow — design, procure, integrate

Each custom board goes through three stages, one board at a time: **design** it, **procure** its parts and the assembled board, then **integrate** the real board into the final CAD. A board starts a stage only after it has finished the stage before. Each board has a folder in `04-pcbs/`. Its README records where the board is in this workflow.

PCB-01 has no folder. It is the bought TIFPS0629 ([D-019](../decisions.md#d-019)), and its acceptance stays in [power-boards.md §3](power-boards.md#3-pcb-01--tifps0629-acceptance-before-cells-are-connected).

## Board folders

| Folder | Board | BOM | Design | Procure | Integrate |
|---|---|---|---|---|---|
| [pcb-02-charger](pcb-02-charger/README.md) | Charger, latch and pack sense | CH-041 | Not started | — | — |
| [pcb-03-motor-gate](pcb-03-motor-gate/README.md) | Motor gate and head 5 V rail | CH-042 | Not started | — | — |
| [pcb-04-branch-converters](pcb-04-branch-converters/README.md) | Five branch converters | CH-043 | Not started | — | — |
| [pcb-05-audio-front-end](pcb-05-audio-front-end/README.md) | Audio front end | BO-002 | Not started | — | — |
| [pcb-06-pdm-mic](pcb-06-pdm-mic/README.md) | PDM microphone board ×4 | BO-005 | Not started | — | — |
| [pcb-07-base-imu](pcb-07-base-imu/README.md) | Base IMU | CH-021 | Not started | — | — |
| [pcb-08-yaw-junction](pcb-08-yaw-junction/README.md) | Yaw junction | CH-083 | Not started | — | — |
| [pcb-09-c0-link-adapter](pcb-09-c0-link-adapter/README.md) | C0 link adapter | CH-084 | Not started | — | — |
| [pcb-10-c3-carrier](pcb-10-c3-carrier/README.md) | C3 controller carrier | CH-044 | Not started | — | — |
| [pcb-11-status-led](pcb-11-status-led/README.md) | Status LED carrier | CH-085 | Not started | — | — |
| [pcb-12-c2-head-carrier](pcb-12-c2-head-carrier/README.md) | C2 head carrier | CH-086 | Not started | — | — |
| [pcb-13-charge-inlet](pcb-13-charge-inlet/README.md) | Charge inlet | BO-015 | Not started | — | — |
| [pcb-14-yaw-rotor-joiner](pcb-14-yaw-rotor-joiner/README.md) | Yaw rotor joiner ×3 | BO-062 | Not started | — | — |
| [pcb-15-nose-hall](pcb-15-nose-hall/README.md) | Nose Hall carrier | CH-064 | In progress | — | — |

Update this table and the board's README together. The [board register](README.md#board-register) keeps the board's specification status and the work it still needs.

## Folder layout

Each board folder starts with only its README. The other entries appear when the stage that produces them starts.

```text
pcb-NN-name/
  README.md     identity, inputs, stage status, log
  design/       KiCad project: .kicad_pro/.kicad_sch/.kicad_pcb (stage 1)
  fab/<rev>/    Gerbers, drill, pick-and-place, fab BOM (stage 1)
  bom.csv       component BOM for one board             (stage 2)
  cad/          board STEP exported from the layout     (stage 1, used in stage 3)
```

Material that spans several boards stays at the top of `04-pcbs/`: [power-boards.md](power-boards.md), [charge-path.md](charge-path.md), [feetech-link-contract.md](feetech-link-contract.md) and [open-items.md](open-items.md). Board folders link to it rather than copy it.

The tools are KiCad 10.99 nightly with KiPy, `kicad-cli` and JLCPCB ([D-058](../decisions.md#d-058), [D-060](../decisions.md#d-060); paths in the [README](README.md#tools)). No autorouter.

## Stage 1 — Design

**Starts when** the board's specification is clear enough to draw: its function, connectors and pinout, supply and protection, and its CAD envelope. Any spec gaps are listed in the board README under *Inputs*.

1. **Freeze the inputs.** In the README, list the spec sources, the connector pinout and the envelope the CAD placeholder gives: outline, mounting holes, connector positions, tallest part.
2. **Schematic.** Draw it from the spec. Check it against the spec row by row, and record that check.
3. **Layout.** Follow the [layout rules](README.md#layout-rules): no autorouter, placement in small groups, octolinear buses, current-sized tracks. Keep the board inside the CAD envelope. Export a board STEP early and check it in the droid CAD ([final/v1/cad](../final/v1/cad/)). If the board must grow or a connector must move, raise a decision first.
4. **Checks and DFM.** Run `kicad-cli` ERC on the schematic, and DRC with `--schematic-parity` on the board. Both must come back with 0 errors. Then run JLCPCB's design-rule and assembly checks.
5. **Release outputs.** Commit the schematic, layout, fab outputs and board STEP under a revision letter (rev A, rev B…).

**Done when** a revision is committed with schematic, layout, fab outputs and board STEP, and any change to the envelope or interface has its decision.

## Stage 2 — Procure

**Starts when** the board has a committed design revision.

1. **Component BOM.** `bom.csv` lists one board's parts: reference, value, MPN, manufacturer, quantity, supplier and its part number, unit price, and the date stock was checked. It also says whether each part is assembled by the fab house or fitted by hand.
2. **Sourcing in India.** Confirm each part can be bought: fab-house stock, LCSC, element14 India, Evelta, Mouser/DigiKey India. A part that can't be sourced sends the board back to stage 1.
3. **Order.** Order the bare board or PCBA, with spares for one rework. Boards that share a fab house can go on one order.
4. **Project BOM.** Update the board's line in [BOM.csv](../BOM.csv): `status`, `supplier_candidate`, `procurement`.
5. **Receive.** Inspect the boards. Measure outline, thickness, tallest part and mass, and record them in the BOM line's `received_measurements`. Then run the board's bring-up and bench tests from its spec.

**Done when** the boards are in hand and measured, and the project BOM line is up to date. A failed bench test is raised as a decision. It may send the board back to stage 1 for a new revision.

## Stage 3 — Integrate

**Starts when** the board has a design revision and a board STEP. Received measurements are better where they exist.

1. **Replace the placeholder.** KiCad's STEP has Y flipped and the board solid starting at Z 0, so place it with a measured transform ([D-058](../decisions.md#d-058)). Droid CAD changes are made only in [final/v1/cad](../final/v1/cad/) ([rules](README.md#rules)). Load the board STEP in `makad-v1.step.py` in place of the block placeholder from the subsystem tree. Keep the label the final CAD matches: `CUSTOM_PCBS` in [makad-v1.step.py](../final/v1/cad/makad-v1.step.py). If the label must change, change the pattern too.
2. **Mounting.** Model the standoffs, inserts, slots or tabs the layout's holes need.
3. **Mass.** Update the board's row in the subsystem's hand-kept mass table. Geometry changes do not update it, so mass checks pass on stale numbers until someone does.
4. **Checks.** The subsystem checks don't see changes made in `final/v1/cad`. Add or run a targeted check script there for that area: clash, fit, assembly path, harness.
5. **Final CAD.** Rebuild `makad-v1.step.py` and `makad-v1-presentation.step.py` (see [final/v1](../final/v1/README.md)). Check the board in the `Custom PCBs` group in the viewer and save a snapshot.

**Done when** the final CAD shows the real board at its installed position, the subsystem checks pass, and the register row and this table are updated.

## Before release

A board is released only after all three stages and the record the [README rules](README.md#rules) require: exact revision, schematic, BOM, layout, pinout, protection and enable behaviour, mounting, fab outputs and measured electrical results.
