"""STS3045M mass sensitivity with unchanged head structure and A0 datums.

Uses the existing mass-placement rows as a baseline, replacing only the two
XC330 servo rows. Servo CoMs and intrinsic inertia use a uniform 36x15x29.2
case approximation; tabs, horn, cable and redesigned mounts are not included.
Never writes mass-placement.json or axes.json.
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
source = json.loads((HERE / "mass-placement.json").read_text())
MASS_G = 34.8
ROLL_CENTER = [-97.4, source["axes"]["roll_y"], source["axes"]["roll_z"]-6]
PITCH_CENTER = [source["axes"]["pitch_x"]-6, 30.6,
                source["axes"]["pitch_z"]]


def box_inertia(size):
    return [MASS_G*(size[1]**2+size[2]**2)/12,
            MASS_G*(size[0]**2+size[2]**2)/12,
            MASS_G*(size[0]**2+size[1]**2)/12]


rows = []
for original in source["rows"]:
    row = dict(original)
    if "XC330-M288-T roll" in row["name"]:
        row.update(name="STS3045M roll what-if, tabs vertical",
                   mass_g=MASS_G, center_mm=ROLL_CENTER,
                   intrinsic_diagonal_g_mm2=box_inertia((29.2, 15, 36)),
                   basis="E: drawing case box and nominal mass; mounts/horn/cable unchanged")
    elif "XC330-M288-T pitch" in row["name"]:
        row.update(name="STS3045M pitch what-if, tabs rearward",
                   mass_g=MASS_G, center_mm=PITCH_CENTER,
                   intrinsic_diagonal_g_mm2=box_inertia((36, 29.2, 15)),
                   basis="E: drawing case box and nominal mass; mounts/horn/cable unchanged")
    rows.append(row)


def group(frames, axis, origin):
    members = [r for r in rows if r["frame"] in frames]
    mass = sum(r["mass_g"] for r in members)
    centre = [sum(r["mass_g"]*r["center_mm"][i] for r in members)/mass
              for i in range(3)]
    inertia = sum(
        r["intrinsic_diagonal_g_mm2"][axis] +
        r["mass_g"]*sum((r["center_mm"][i]-origin[i])**2
                         for i in range(3) if i != axis)
        for r in members) * 1e-9
    return {"mass_g": mass, "center_mm": centre,
            "estimated_inertia_kg_m2_at_old_axis": inertia}


axes = source["axes"]
working = {
    "roll": group("R", 0, (0, axes["roll_y"], axes["roll_z"])),
    "pitch": group("RP", 1, (axes["pitch_x"], 0, axes["pitch_z"])),
    "yaw": group("RPY", 2, (axes["pitch_x"], 0, -49.5)),
}
result = {
    "basis": "E sensitivity; only servo mass/box replaced, old structural geometry, axes and mounts retained",
    "source": "mass-placement.json",
    "working": working,
    "baseline": source["working"],
    "nominal_servo_placements_mm": {"roll": ROLL_CENTER, "pitch": PITCH_CENTER},
    "open": ["new mount and horn mass", "measured servo CoM and tensor",
             "A0 re-solve", "head structure/clearance/FEA", "motion §11.3"],
}
out = HERE / "generated/feetech-mass-whatif.json"
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({name: {"mass_g": round(data["mass_g"], 2),
                         "inertia_kg_m2": round(data["estimated_inertia_kg_m2_at_old_axis"], 9)}
                  for name, data in working.items()}, indent=2))
