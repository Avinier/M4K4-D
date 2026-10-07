# STS3045M trial fit in the live head source

`check_feetech_head_envelopes.py` locates the drawing-based STS3045M STEP at
the current A0 pitch/roll axes. `check_feetech_head_fit.py --exact` then builds
the current 100-entry `layout_model.py` head and checks four neutral-pose
clockings against all named part boxes and selected solid pairs. Results:
[`feetech-head-envelopes.json`](generated/feetech-head-envelopes.json),
[`feetech-head-fit.json`](generated/feetech-head-fit.json), and the independent
[`feetech-mass-whatif.json`](generated/feetech-mass-whatif.json).

| Trial orientation | Solid overlaps with non-XC330 parts, mm³ | Consequence |
|---|---|---|
| Roll tabs vertical | rear cover 56.2; pitch frame saddle 49.9; servo strap 160.5; rear trim stack 806.5 | Requires saddle, strap, cover and trim relocation. |
| Roll tabs lateral | rear cover 56.2; servo strap 530.6; rear trim stack 806.5 | Better frame clearance, but cover, strap and trim still need redesign. |
| Pitch tabs forward | display module 248.1; connector/service reserve 977.0; rolling cradle 390.0; +Y trunnion 135.0; old adapter 352.8 | Fails the display/service space at this datum. |
| Pitch tabs rearward | rolling cradle 7.7; +Y trunnion 135.0; old adapter 910.0 | Preferred trial clocking; requires a new adapter and changed trunnion/cradle interface. |

These are intersections of the reference solid with each named existing
part; the volumes are **not additive**, and a small intersection is not a
tolerance allowance. The old XC330 housings and their screws are intentionally
excluded from the solid list because they are replacements. The current
helmet skin did not intersect either candidate solid at neutral, but pose
sweeps, shell wall clearance, tool access, cable exit and horns were not
checked. The STEP omits spline teeth and uses estimated boss/lead details.
The existing saddle/adapter were designed for XC330 tapped-face screws; an
STS3045M tab-mounted design must use its four open Ø4.2 slots and establish a new
25T horn connection. Do not update `axes.json` or `mass-placement.json` from
these neutral-pose placements. Rebuild the supports, then rerun the complete
pose and fastener checks, mass solve and P07 FEA.
