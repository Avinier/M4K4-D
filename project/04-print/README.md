# 04-print — making Makad's printed parts

`03-build` designs Makad. `04-print` turns the designed parts into printed
parts. It holds only the raw STL files exported from the CAD, and the READMEs
and logs around them: part cards, print logs and measured results. It starts
where a `03-build` part is marked `DESIGN` and ends when the part is printed,
inspected and weighed.

| File | What it holds |
|---|---|
| [lab.md](lab.md) | The lab: rules, machines, rates, cost estimate and open permissions |
| [workflow.md](workflow.md) | The steps every part goes through, the part card, file names and what "print-ready" means |
| [01-chassis/](01-chassis/README.md) | Chassis v1 prints |
| `02-body/` | Body v1 prints (not started) |
| `03-head/` | Head v1 prints (not started) |
| `05-finish/` | Primer, paint and weathering (not started) |

## Rules

1. **No geometry is edited here.** This folder holds STL files exported from
   the CAD and the documents around them, nothing else. An STL is never edited,
   repaired into a different shape or modelled over; a copy of geometry kept
   here would drift from the CAD.
2. **Every geometry change is made in `03-build/final/v1` only.** When a print
   shows a problem (a tight fit, a thin wall, a missing chamfer), the fix is an
   entry in `DROID_CUTS`, `DROID_ADDS` or `DROID_MOVES` in
   [`final/v1/cad/makad-v1.step.py`](../03-build/final/v1/cad/makad-v1.step.py),
   with a decision in [decisions.md](../03-build/decisions.md) and a targeted
   check in `final/v1/cad`. The subsystem folders (`01-chassis/v1`,
   `02-body/v1`, `03-head/v1`) are **not** edited for print fixes. Then the part
   is exported again and its old STL replaced.
3. **STLs are exported from the final assembly, never from a subsystem model.**
   The droid edits in `final/v1` change printed parts that the subsystem models
   do not know about; for example, `DROID_ADDS` fuses the PCB-05 bosses into the
   body frame print (D-067). An STL exported from a subsystem model alone would
   miss them. The export builds the subsystem tree and applies
   `_apply_droid_cuts(tree, strict=False)` from the final entry first.
4. **One decision ledger.** Material, process and fit decisions are recorded
   in [03-build/decisions.md](../03-build/decisions.md). This folder cites
   them. Print settings, results and measurements stay here.
5. **No separate test prints.** Small real parts go first and are the test:
   their holes, bearing seats and insert bosses show whether the fits are
   right before the big parts are printed. A wrong fit is corrected in the
   slicer (XY hole compensation) if it is a printer offset, or in the CAD
   under rule 2 if it is a design error. A part whose fit depends on a
   purchased part waits until that part is in hand and measured.
6. **Measure and weigh every print.** A part's mass and key dimensions go in
   its subsystem log. The mass registers in `03-build` are hand-kept tables, so
   a measured mass reaches them only when someone updates them.
7. **Material and colour come from the [print guide](../03-build/final/v1/printguide.md).**
   A part's material is not chosen again here.

## Plan

Structure is printed before skins and cheap materials before expensive ones.
Each phase ends with a fit or bench test, so a design problem shows up before
the parts that depend on it are printed.

| Phase | What | Printers | Ends with | Status |
|---|---|---|---|---|
| 0. Access | Lab sign-off, faculty sponsor, spools bought and dried; open questions in [lab.md](lab.md#still-open) answered | — | Permission for ASA on the X1E and PA-CF on the X-CF Pro | Open |
| 1. Chassis | [Frame, axle stack, wheels, nose and keel](01-chassis/README.md), about 20 parts, mostly PETG. Small parts and one tyre first | A1, Guider II; A1 for TPU | The rolling-chassis tests in [chassis testsystem.md](../03-build/01-chassis/v1/testsystem.md) | Not started |
| 2. Body structure | Body frame and foot cassette, compute tray, yaw stage and gears (PETG) | A1, Guider II | Frame on the chassis; the yaw stage bench test (D-044) | Not started |
| 3. Body skins | Shell, service panels, wheel-arch pods, trims (ASA, ivory and taupe) | X1E | The shell lowered over the frame; panels and mics fitted | Not started |
| 4. Head | PLA frames, PA-CF yoke legs (after a stiffness test bar, D-049), ASA skins, two-tone ears | X1E, X-CF Pro, A1 | Head assembled on the yaw disc; the D-053 assembly paths tried | Not started |
| 5. Finish | Primer, paint, clear coat, weathering | — | The finished look in the print guide §3 | Not started |

Phases 2 and 4 can overlap with phase 1 once the chassis small parts have shown
the fits are right, but skins wait until the structure under them fits: a
structure change usually changes a skin.

**Budget:** about 1.5 kg of filament per complete set and 1.5–2 sets in all.
See [lab.md § Cost](lab.md#cost).
