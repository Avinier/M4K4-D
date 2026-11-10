"""D-064 batch (D-100 to D-103): mass and tipping margin after the PCB-08/12/14/16 drafts.

Run from this folder with the legacy runtime, PYTHONPATH 03-head/v1/cad first; about 2 min.
The register is hand-kept (rp06-mass-register-is-manual). This script starts from the
D-095 state recorded by check_d095_mass.py (MASS_ROWS minus its removed rows plus its added
rows, read from check_d095_mass-report.json) and adds the batch's rows:

- PCB-08 rev A: measured core (FR4 1.85 g/cm3) + parts (E) in place of the 4.0 g row less
  D-095's 1 g J8-3/J8-5 removal and its J8-8 header block;
- PCB-14 rev A x3: measured cores + six FH34SRJ (E) in place of D-052's 3 x 0.51 + 6 x 0.4 g
  inside BODY_YAW_STAGE;
- the D-101 rotor posts: rotor volume with the droid edit minus without, PETG 1.20;
- PCB-16 rev A: measured core + two FH34SRJ + two M2 x 4 screws and inserts (new row);
- PCB-12 rev A: reported against the head's M008 C2 allowance (20 g E), which stays in the
  head mass tree unchanged (the A0 solve is head-owned).

Then CoM and a_tip at the neutral and worst head pose with check_d095_mass.tip(), against
1.582 m/s2. Component masses are estimates (E), not weighed.
"""

import json
from pathlib import Path

from build123d import Compound
from cadgen.step_scene import import_step

import module_checks as C
import check_d095_mass as D

ROOT = Path(__file__).resolve().parents[3]
FR4 = 1.85
PARTS_E = {  # g, evidence
    "FH34SRJ": (0.10, "E Hirose FH34SRJ-22S, 13 x 3.8 x 1.0 mm LCP"),
    "MICROFIT_43045_0621": (1.5, "E Molex 43045-0621 2x3 right angle with clips"),
    "GH_BM06B": (0.25, "E JST BM06B-GHS-TBT"),
    "SPOX_5267_03A": (0.4, "E Molex 22-03-5035"),
    "M2X4_BUTTON": (0.15, "E ISO 7380 M2 x 4 steel"),
    "M2_INSERT": (0.10, "E M2 x 3 brass heat-set insert"),
}


def core_mass(name, rev="revA"):
    scene = import_step(str(ROOT / "04-pcbs" / name / "cad" / f"{name}-{rev}.step"))
    kids = [c for c in scene.children if c.solids()]
    core = next(c for c in kids if not c.children)   # as pcb_integration.raw_parts: only the core is not an assembly
    v, _ = D.centroid(core)
    return v * FR4 / 1000.0, v


def main():
    import body_v1_model as M
    r = C.Report("check_batch_mass")
    rep = json.loads((Path(__file__).parent / "check_d095_mass-report.json").read_text())
    rows95 = {x["check"]: x for x in rep["rows"]}
    removed = {n for n, _ in rows95["removed_rows"]["rows"]}
    rows = [(n, g, tuple(c)) for n, g, c, _ in M.MASS_ROWS if n not in removed]
    rows += [(n, g, tuple(c)) for n, g, c, _ in rows95["added_rows"]["rows"]]
    before = D.tip(rows, M)
    r.check("d095_state_reproduced", abs(before["a_tip"] - rows95["neutral_a_tip_above_minimum"]["a_tip"]) < 2e-3,
            mass_g=before["mass_g"], a_tip=before["a_tip"], worst_pose_a_tip=before["worst_pose_a_tip"])

    delta = []
    ho = M.HEAD_ORIGIN_IN_CHASSIS
    # PCB-08: the register row (4.0 g) less D-095's -1 g, and D-095's measured J8-8 header block.
    m08, v08 = core_mass("pcb-08-yaw-junction")
    parts08 = PARTS_E["MICROFIT_43045_0621"][0] + PARTS_E["GH_BM06B"][0] + PARTS_E["SPOX_5267_03A"][0] + 2 * PARTS_E["FH34SRJ"][0]
    j88 = sum(g for n, g, _, _ in rows95["added_rows"]["rows"] if n == "YAW_JUNCTION_J8_8_FEETECH_5264_3P_HEADER")
    delta.append(("PCB-08 rev A replaces its estimate", m08 + parts08 - 3.0 - j88, (-3.4, -33.5, 113.0),
                  f"core {v08:.0f} mm3 x {FR4} = {m08:.2f} g + parts {parts08:.2f} g (E); less 3.0 g row and {j88:.2f} g J8-8 block"))
    # PCB-14 x3 inside BODY_YAW_STAGE.
    m14, v14 = core_mass("pcb-14-yaw-rotor-joiner")
    new14 = 3 * m14 + 6 * PARTS_E["FH34SRJ"][0]
    delta.append(("PCB-14 rev A x3 replaces D-052's estimate", new14 - (3 * 0.51 + 6 * 0.4), (16.0, -1.0, 142.3),
                  f"3 x core {v14:.0f} mm3 x {FR4} + 6 FH34SRJ (E) = {new14:.2f} g; was 3.93 g"))
    # D-101 rotor posts.
    entry = C.load_entry()
    rotor = next(p for p in M.yaw_drive_moving_parts() if p.label == "YAW_ROTOR_CLAMP_DRUM_AND_STOP_DOG")
    edited = entry._apply_droid_cuts(Compound(children=[rotor]), strict=False)
    after = edited.children[0]
    va, ca = D.centroid(after)
    vb, cb = D.centroid(rotor)
    dv = va - vb
    cpost = tuple((va * ca[i] - vb * cb[i]) / dv for i in range(3)) if abs(dv) > 1e-3 else cb
    delta.append(("YAW_ROTOR D-101 posts", dv * D.PETG_BODY / 1000.0, cpost, f"measured {dv:+.1f} mm3 x {D.PETG_BODY}"))
    # PCB-16 on the yaw disc (yaw-carried; the yaw stage carries it with the head).
    m16, v16 = core_mass("pcb-16-head-junction")
    hw16 = 2 * (PARTS_E["FH34SRJ"][0] + PARTS_E["M2X4_BUTTON"][0] + PARTS_E["M2_INSERT"][0])
    delta.append(("PCB16_HEAD_JUNCTION", m16 + hw16, (-44.2 + ho[0], 44.7 + ho[1], -33.9 + ho[2]),
                  f"core {v16:.0f} mm3 x {FR4} = {m16:.2f} g + ZIFs, screws and inserts {hw16:.2f} g (E); wires in the head harness allowance"))
    # PCB-12 against M008.
    m12, v12 = core_mass("pcb-12-c2-head-carrier")
    zero_g, ics_g = 2.0, 1.2
    hw12 = 2 * (PARTS_E["M2X4_BUTTON"][0] + PARTS_E["M2_INSERT"][0])
    pcb12 = m12 + zero_g + ics_g + hw12
    r.check("pcb12_within_head_c2_allowance", pcb12 <= 20.0, assembly_g_E=round(pcb12, 2), allowance_g=20.0,
            breakdown=dict(core=round(m12, 2), zero_E=zero_g, ics_connectors_passives_E=ics_g, screws_inserts_E=round(hw12, 2)),
            note="M008 'C2 installed allowance' 20 g (E) in 03-head mass_layout.py stays; the printed tray (removed) was owned by M008 too")

    rows += [(n, g, c) for n, g, c, _ in delta]
    now = D.tip(rows, M)
    r.check("batch_rows", True, total_g=round(sum(d[1] for d in delta), 3),
            rows=[(n, round(g, 3), [round(v, 1) for v in c], why) for n, g, c, why in delta])
    r.check("neutral_a_tip_above_minimum", now["a_tip"] >= D.A_TIP_MIN, a_tip=now["a_tip"], before=before["a_tip"],
            minimum=D.A_TIP_MIN, mass_g=now["mass_g"], mass_before_g=before["mass_g"], com_mm=now["com_mm"])
    r.check("worst_head_pose_a_tip_above_minimum", now["worst_pose_a_tip"] >= D.A_TIP_MIN,
            worst_pose_a_tip=now["worst_pose_a_tip"], before=before["worst_pose_a_tip"], minimum=D.A_TIP_MIN)
    r.finish()


if __name__ == "__main__":
    main()
