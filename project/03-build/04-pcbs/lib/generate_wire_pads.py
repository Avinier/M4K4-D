"""Generate PCB-16's bare-copper wire-pad rows (SMD, solder the wire across the pad).

WirePads_1x07_P1.5mm / 1x02_P1.5mm: 1.0 x 2.5 mm pads for AWG28 (pre-crimped GH lead
cut ends). WirePads_Power_1x02_P3.5mm: 2.2 x 3.5 mm for AWG20 head power (2.4 A); the GND pad also takes
PCB-12's AWG28 GND_HEAD reference wire.
Pad 1 at the left (-X); the wire leaves toward local -Y. Written in KiCad's
multi-line form so kfile.replace_footprint carries nets onto the pads.
"""

from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "pcb16.pretty"
SPECS = {
    "WirePads_1x07_P1.5mm": (7, 1.5, 1.0, 2.5),
    "WirePads_1x02_P1.5mm": (2, 1.5, 1.0, 2.5),
    "WirePads_Power_1x02_P3.5mm": (2, 3.5, 2.2, 3.5),
}


def prop(name, value, y, layer):
    return (f'\t(property "{name}" "{value}"\n\t\t(at 0 {y} 0)\n\t\t(layer "{layer}")\n'
            f'\t\t(effects (font (size 0.8 0.8) (thickness 0.12)))\n\t)')


for name, (n, pitch, w, h) in SPECS.items():
    x0 = -(n - 1) * pitch / 2
    items = [f'(footprint "{name}"', '\t(version 20241229)', '\t(generator "makad-generate_wire_pads")',
             '\t(layer "F.Cu")', f'\t(descr "{n} bare SMD wire pads, {pitch} mm pitch, {w} x {h} mm; wire leaves toward -Y")',
             '\t(tags "wire pad solder")', prop("Reference", "REF**", -(h / 2 + 1.0), "F.Fab"),
             prop("Value", name, h / 2 + 1.0, "F.Fab"), '\t(attr smd exclude_from_pos_files exclude_from_bom)']
    for k in range(n):
        items.append(f'\t(pad "{k + 1}" smd rect\n\t\t(at {x0 + k * pitch:.3f} 0)\n\t\t(size {w} {h})\n'
                     f'\t\t(layers "F.Cu" "F.Mask")\n\t)')
    cx, cy = -x0 + w / 2 + 0.25, h / 2 + 0.25
    for a, b in [((-cx, -cy), (cx, -cy)), ((cx, -cy), (cx, cy)), ((cx, cy), (-cx, cy)), ((-cx, cy), (-cx, -cy))]:
        items.append(f'\t(fp_line (start {a[0]:.3f} {a[1]:.3f}) (end {b[0]:.3f} {b[1]:.3f}) (stroke (width 0.05) (type solid)) (layer "F.CrtYd"))')
    items.append(f'\t(fp_text user "1" (at {x0:.3f} {-(h / 2 + 0.6):.3f} 0) (layer "F.Fab") (effects (font (size 0.6 0.6) (thickness 0.1))))')
    items.append(')')
    OUT.mkdir(exist_ok=True)
    (OUT / f"{name}.kicad_mod").write_text("\n".join(items) + "\n")
    print(name)
