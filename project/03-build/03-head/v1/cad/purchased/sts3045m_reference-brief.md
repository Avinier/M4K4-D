# STS3045M reference STEP brief

Purpose: a dimensioned packaging reference for pitch/roll fit work, not a
machining drawing. Units: millimetres. The output axis is the local Z axis;
the origin is its intersection with the bottom case plane.

The [supplied STS3045M PDF](https://evelta.com/content/datasheets/501-STS3045M.pdf),
page 6, is the dimensional source. The three user-supplied product photographs
establish the general case split, two mounting tabs, upper boss and lead exit.
The drawing controls a 36 × 15 × 29.2 mm case, 48.8 mm total mounting span,
four open-ended Ø4.2 mounting slots in two rows 7.5 mm apart, output shaft offset 6 mm
along the case, and Ø5.9, 25T output. The local body interval is X −12…24;
tabs extend X −18.4…30.4 at Z 19.7…21.7; slot centres sit at X −15.3 and
+27.3 (±21.3 from the case centre, X +6); spline reaches Z 33.1.

Scaled from the same drawing (D-049 step 0, 2026-10-08; anisotropic raster,
dimensioned features reproduce to ≤ 0.2 mm): slot necks 2.4 mm wide; output
boss Ø10.4 × 0.3; the lead exits the **shaft-end face (−X), centred in Y**,
as a 1.4 mm flange (6.0 wide, Z 0.9…4.9) plus a 2.1 mm nozzle (5.1 wide,
Z 1.7…4.2), 3.5 mm proud. The earlier model put the lead stub beside the
case at Y −9.5…−7.5, cut 4.2 mm slot entrances and used a Ø9.5 boss; all
three were corrected. Tab root shape, M3 thread depth and tooth form remain
unmeasured.

Validation targets (measured on the regenerated STEP): five closed valid
solids; overall bounds X −18.4…30.4, Y −7.5…7.5, Z 0…33.1; each slot empty
at r 2.05 and solid at r 2.25 about its centre; necks open over |Y−row| ≤ 1.2.
The 150 mm flexible lead leaves the nozzle tip along −X and requires routed
clearance. The 25T tooth profile, M3 internal thread, horn
engagement, mounting-hole centre tolerance and case fillets are not defined.
