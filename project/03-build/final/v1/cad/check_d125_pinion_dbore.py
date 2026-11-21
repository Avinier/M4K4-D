"""D-125: aluminium fixed pinion half on BO-047's D-flat, with the pre-wind peg, through
the droid entry.

Builds the chassis + body droid tree (module_checks.droid_tree) and checks:
- the shaft carries the stock's full-length flat (2.0 from the axis);
- the droid's fixed half is the fab half (d125_pinion_dbore.metal_half_local) plus
  the pressed Ø2 x 4 peg, in place;
- no interference between the half and the shaft at the nominal flat and at the
  stock's thickest flat (4.55 across), and the key engages (shaft turned ±3 deg);
- the peg: clear of the sprung half at neutral, stops the spring's +θ turn on the
  slot's end after about 1.2 deg, and lets the half wind about 12.9 deg the other way;
  clear of every other part; the slot leaves PETG ligaments to the bore and the root;
- sprung half and hub unchanged against the shaft;
- key bearing stress (`E`): 0.22 N.m preload + demand (0.22 paper peak, 0.30 proposed
  ceiling) on the 3.0 x 2.0 mm flat, uniform and triangular pressure; screened
  against 6061-T6 yield (240 MPa; 7075-T6 is about 500) and recorded for PETG (why);
- mass rows for check_d107_mass: half PETG -> aluminium, plus the steel peg.

Run from this folder with the legacy runtime, PYTHONPATH ../../../02-body/v1/cad:.
(about 1 min). Writes check_d125_pinion_dbore-report.json.
"""
import math

from build123d import Axis, Cylinder, Location

import module_checks as C
import d125_pinion_dbore as D
import body_v1_model as B

PRELOAD, PAPER_PEAK, CEILING = B.YAW_SCISSOR_PRELOAD_NM, 0.22, B.YAW_SERVO_TORQUE_LIMIT_NM
AL_YIELD, PETG_SUSTAINED = 240.0, 15.0


def segment(r, d):
    return r * r * math.acos(d / r) - d * math.sqrt(r * r - d * d)


def turned(shape, deg):
    return shape.moved(Location((-D.PX, -D.PY, 0))).rotate(Axis.Z, deg).moved(Location((D.PX, D.PY, 0)))


def symdiff(a, b):
    return a.volume + b.volume - 2 * C.common(a, b)


def main():
    r = C.Report("check_d125_pinion_dbore")
    entry, _, leaves = C.droid_tree(with_modules=False, revb_pcb08=False)
    shaft = C.find(leaves, "YAW_PINION_SHAFT_D5_STEEL").shape
    fixed = C.find(leaves, "YAW_DRIVE_SCISSOR_PINION_FIXED_HALF").shape
    sprung = C.find(leaves, "YAW_DRIVE_SCISSOR_PINION_SPRUNG_HALF").shape
    hub = C.find(leaves, "YAW_DRIVE_HUB_ON_ST3215_HS_HORN").shape
    R, L = D.R, D.Z1 - D.Z0
    z0, z1 = D.FIXED_Z

    # --- Shaft -------------------------------------------------------------
    sb = shaft.bounding_box()
    want = math.pi * R * R * L - segment(R, D.SHAFT_FLAT) * L
    r.check("shaft_flat_full_length", abs(shaft.volume - want) < 1e-3 and abs(sb.min.Y - (D.PY - D.SHAFT_FLAT)) < 1e-6,
            volume=shaft.volume, expected=want, across_flat=R + D.SHAFT_FLAT)

    # --- Fixed half = fab half + peg ---------------------------------------
    made = D.metal_half_local().moved(Location((D.PX, D.PY, z0)))
    peg = D.peg_pin()
    d = symdiff(fixed, made + peg)
    r.check("droid_half_is_fab_half_plus_peg", d < 1e-2, symdiff_mm3=d, half_volume=made.volume, peg_volume=peg.volume)

    v = C.common(shaft, fixed)
    thick = Cylinder(R, L).moved(Location((D.PX, D.PY, (D.Z0 + D.Z1) / 2))) - D._minus_y_slab(D.BORE_FLAT, D.Z0 - 1, D.Z1 + 1, R + 1)
    v_thick = C.common(thick, fixed)
    r.check("shaft_clears_fixed_half", v < 1e-4 and v_thick < 1e-4, nominal_mm3=v, thickest_stock_flat_mm3=v_thick,
            clearance_nominal=D.BORE_FLAT - D.SHAFT_FLAT)
    play = math.degrees(math.atan2(math.sqrt(R * R - D.SHAFT_FLAT ** 2), D.SHAFT_FLAT) - math.acos(D.BORE_FLAT / R))
    hits = {deg: C.common(turned(shaft, deg), fixed) for deg in (-3.0, 3.0)}
    r.check("key_engages", all(h > 1e-3 for h in hits.values()), turned_3deg_mm3=hits, play_each_way_deg=play,
            note="play cannot open as lash while demand < preload: the preload loads the key one way")

    # --- Peg and slot ------------------------------------------------------
    at = {deg: C.common(turned(sprung, deg), peg) for deg in (0.0, 0.8, 1.6, -12.4, -13.4)}
    r.check("peg_stop_and_travel", at[0.0] < 1e-4 and at[0.8] < 1e-4 and at[1.6] > 1e-4 and at[-12.4] < 1e-4 and at[-13.4] > 1e-4,
            peg_vs_sprung_mm3_by_turn_deg=at,
            note="+deg = the spring's direction: stops on the slot end after ~1.2 deg (0.39 mm at the pitch circle); winds ~12.9 deg the other way")
    others = [lf for lf in leaves if lf.label not in ("YAW_DRIVE_SCISSOR_PINION_FIXED_HALF",)]
    cl = C.clashes(peg, others)
    pb = peg.bounding_box()
    r.check("peg_clear_of_other_parts", not cl and pb.min.Z > D.SPRUNG_Z[0] + 0.1, clashes=cl,
            peg_bottom_above_sprung_bottom_mm=pb.min.Z - D.SPRUNG_Z[0])
    root_r = B.YAW_GEAR_MODULE * (B.YAW_GEAR_TEETH / 2 - 1.25)
    inner = D.PEG["r"] - D.SLOT["width"] / 2 - (R + 0.1)
    outer = root_r - (D.PEG["r"] + D.SLOT["width"] / 2)
    r.check("slot_ligaments_mm", inner >= 3.0 and outer >= 3.0, to_bore=inner, to_root=outer)

    r.check("sprung_half_and_hub_unchanged", C.common(shaft, sprung) < 1e-4 and C.common(shaft, hub) < 1e-4,
            sprung_mm3=C.common(shaft, sprung), hub_mm3=C.common(shaft, hub),
            note="hub bore stays round; the shaft is bonded in it")

    # --- Key bearing stress (E) --------------------------------------------
    w, hl = 2 * math.sqrt(R * R - D.SHAFT_FLAT ** 2), z1 - z0

    def p(t_nm):
        t = t_nm * 1000.0
        return round(4 * t / (hl * w * w), 1), round(6 * t / (hl * w * w), 1)
    sustained, peak, ceiling = p(PRELOAD), p(PRELOAD + PAPER_PEAK), p(PRELOAD + CEILING)
    r.check("fixed_half_key_bearing_stress", ceiling[1] <= AL_YIELD,
            flat_width=w, key_length=hl, preload_only_MPa=sustained, preload_plus_paper_peak_MPa=peak,
            preload_plus_ceiling_MPa=ceiling, aluminium_6061_yield_MPa=AL_YIELD,
            petg_sustained_screen_MPa=PETG_SUSTAINED, petg_fails=sustained[0] > PETG_SUSTAINED,
            note="E; the steel shaft side is far below its yield")

    # --- Mass rows for check_d107_mass --------------------------------------
    t = B.YAW_SCISSOR_HALF_FACE
    petg = B._involute_gear(B.YAW_GEAR_TEETH, B.YAW_GEAR_MODULE, 0.0, t, 0.0, 0.0, D.PHASE) - \
        Cylinder(R, t + 2).moved(Location((0, 0, t / 2)))
    c_half = (D.PX, D.PY, (z0 + z1) / 2)
    pc = pb.center()
    rows = [("fixed pinion half PETG removed", round(-petg.volume * D.DENSITY["petg"], 3), c_half),
            ("fixed pinion half 7075-T6", round(D.metal_half_local().volume * D.DENSITY["al7075"], 3), c_half),
            ("pre-wind peg ISO 8734 2x4", round(peg.volume * D.DENSITY["steel"], 3), (pc.X, pc.Y, pc.Z))]
    r.check("mass rows", True, rows=rows, net_g=round(sum(g for _, g, _ in rows), 3))
    r.finish()


if __name__ == "__main__":
    main()
