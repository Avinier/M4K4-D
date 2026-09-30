# Drive gearmotor interface sheet (CH-014)

**Status:** parked reference sheet; no motor is currently on hand and no measurement task is active. The chassis design may proceed using the clearly labeled CAD/supplier assumptions in this sheet and a replaceable motor interface. If the selected **6V230RPM** units become available, record actual values here rather than copying the CAD assumptions. The [axle stack proposal](axle-stack.md) identifies the fit-critical rows with ★.

Tools: digital caliper (0.01 mm), M3 screw or tap to check thread, small hex key or pin gauge to test hole depth, scale (0.1 g), phone photo of each face with a ruler in shot.

## Datum

Take the **output faceplate** as Y = 0, with + toward the shaft tip. The **flat** on the shaft marks the angular datum: 0° is the direction the flat faces. Measure hole angles from there when looking at the face.

## Face and pilot

| # | Feature | CAD assumption | 230RPM #1 | 230RPM #2 | Notes |
|---|---|---|---|---|---|
| ★F1 | Number of tapped face holes | 2 | | | Photo of face |
| ★F2 | Hole thread (M3? M2.5?) | M3 | | | Try an M3 screw by hand |
| ★F3 | Hole spacing, centre to centre (measure outside-to-outside and subtract one hole Ø) | 17.0 (R 8.5) | | | If there are more than 2 holes, give the pattern |
| ★F4 | Hole angle from the flat datum | 90° / 270° (holes on the axle-height line) | | | |
| ★F5 | Usable thread depth (bottom a screw gently; measure how far it went in) | 5.0 | | | The limiting value for screw length |
| ★F6 | Pilot (bushing boss) diameter | 7.0 | | | |
| ★F7 | Pilot height above faceplate | 2.5 | | | |
| F8 | Faceplate diameter / square size | Ø25 | | | |
| F9 | Face flatness: any raised rim, rivet heads or screw heads proud of the face? | none | | | Anything proud stops the face bearing flat on the plate |

## Output shaft

| # | Feature | CAD assumption | 230RPM #1 | 230RPM #2 | Notes |
|---|---|---|---|---|---|
| ★S1 | Shaft diameter (round part) | 4.00 | | | Measure in two directions |
| ★S2 | Across the flat (flat to opposite round) | 3.50 | | | |
| ★S3 | Shaft length, faceplate to tip | 12.0 | | | Some JGA25 listings say 11.5 |
| ★S4 | Flat start and end, from the faceplate | 4.0 to 12.0 | | | |
| S5 | Shaft end play (push/pull by hand, dial or caliper depth) | — | | | |
| S6 | Shaft radial play at the tip (wiggle, dial if available) | — | | | Informs how much the motor bushing can locate |

## Body and connector

| # | Feature | CAD assumption | 230RPM #1 | 230RPM #2 | Notes |
|---|---|---|---|---|---|
| ★B1 | Gearbox diameter | 25.0 | | | |
| ★B2 | Gearbox length, faceplate to can joint | 21.0 | | | Varies with ratio |
| B3 | Can diameter | 24.4 | | | |
| B4 | Faceplate to encoder board rear face | 61.0 | | | |
| B5 | Faceplate to rear of mated plug / cable exit | ~65 | | | Include the plug in the mated state |
| B6 | Connector position: angle from the flat datum, and radial reach | rearward, 6-pin | | | Photo |
| B7 | Lead length and wire gauge | — | | | |
| B8 | Mass with the supplied lead | 110 g | | | Scale reading |

## Performance (230RPM units only; bench test from [D-003](../../decisions.md#d-003))

| # | Test | 230RPM #1 | 230RPM #2 |
|---|---|---|---|
| P1 | No-load rpm and current at 6.0 V | | |
| P2 | No-load rpm and current at 5.3 V | | |
| P3 | Encoder counts per output revolution | | |
| P4 | Speed at 0.063 N·m and 0.110 N·m | | |
| P5 | Current-limited brief stall: current and torque | | |

If physical-fit work later fills the ★ rows, update `MOTOR_*` in [`cad/body_chassis_model.py`](cad/body_chassis_model.py) and log the change in the [build ledger](../../decisions.md). This is a future verification record, not an active checklist item.
