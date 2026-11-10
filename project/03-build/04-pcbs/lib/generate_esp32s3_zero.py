"""Generate PCB-12's Waveshare ESP32-S3-Zero castellated land pattern.

Pad grid from the two community footprints that agree (jtomka/kicad-esp32-s3-zero
THT, formix-kicad-libraries SMD): 2 x 9 positions at 2.54 mm, rows 15.24 mm apart
on the 18 x 23.5 mm module, USB-C end at local -Y, viewed from the component side
(an SMD module on the carrier's top face is seen from its top). Pad 1 = 5V at the
top left; 1-9 run down the left row (5V, GND, 3V3, GPIO1-6), 10-18 up the right
row (GPIO7-12, then GPIO13/RX/TX, whose order the sources dispute: unused here).
Pads are 3.0 x 1.5 mm across the castellated edge (formix). The module's bottom
pads (GPIO17/18/38-42/45) are not landed; the antenna keep-out follows formix.
Origin at the module centre. Model: Waveshare's v2 STEP, board bottom on the carrier.
"""

from pathlib import Path

NAME = "Waveshare_ESP32-S3-Zero_Castellated"
HERE = Path(__file__).parent
OUT = HERE / "pcb12.pretty" / f"{NAME}.kicad_mod"


def line(x0, y0, x1, y1, layer, width):
    return (f'\t(fp_line (start {x0} {y0}) (end {x1} {y1}) '
            f'(stroke (width {width}) (type solid)) (layer "{layer}"))')


def pad(number, x, y):
    # Multi-line, as KiCad writes pads: kfile.replace_footprint carries nets onto this form.
    return (f'\t(pad "{number}" smd roundrect\n\t\t(at {x} {y})\n\t\t(size 3 1.5)\n'
            f'\t\t(layers "F.Cu" "F.Mask" "F.Paste")\n\t\t(roundrect_rratio 0.15)\n\t)')


items = [
    f'(footprint "{NAME}"', '\t(version 20241229)', '\t(generator "makad-generate_esp32s3_zero")',
    '\t(layer "F.Cu")',
    '\t(descr "Waveshare ESP32-S3-Zero, 18 castellated edge pads at 2.54 mm; USB-C at -Y; bottom pads not landed")',
    '\t(tags "ESP32-S3 Zero Waveshare castellated module")',
    '\t(property "Reference" "REF**"\n\t\t(at 0 -14.5 0)\n\t\t(layer "F.SilkS")\n\t\t(effects (font (size 1 1) (thickness 0.15)))\n\t)',
    f'\t(property "Value" "{NAME}"\n\t\t(at 0 13.2 0)\n\t\t(layer "F.Fab")\n\t\t(effects (font (size 1 1) (thickness 0.15)))\n\t)',
    '\t(attr smd)',
]
for k in range(9):
    y = round(-10.16 + 2.54 * k, 3)
    items.append(pad(k + 1, -8.7, y))
for k in range(9):
    y = round(10.16 - 2.54 * k, 3)
    items.append(pad(k + 10, 8.7, y))
# Module outline and USB-C overhang on Fab; courtyard round the pads and the USB-C.
for seg in [(-9, -11.75, 9, -11.75), (9, -11.75, 9, 11.75), (9, 11.75, -9, 11.75), (-9, 11.75, -9, -11.75),
            (-4.5, -11.75, -4.5, -13.25), (-4.5, -13.25, 4.5, -13.25), (4.5, -13.25, 4.5, -11.75)]:
    items.append(line(*seg, "F.Fab", 0.1))
for seg in [(-10.45, -12.0, -4.75, -12.0), (-4.75, -12.0, -4.75, -13.5), (-4.75, -13.5, 4.75, -13.5),
            (4.75, -13.5, 4.75, -12.0), (4.75, -12.0, 10.45, -12.0), (10.45, -12.0, 10.45, 12.0),
            (10.45, 12.0, -10.45, 12.0), (-10.45, 12.0, -10.45, -12.0)]:
    items.append(line(*seg, "F.CrtYd", 0.05))
items.append(line(-7.0, 12.1, 7.0, 12.1, "F.SilkS", 0.12))
items.append('\t(fp_text user "5V" (at -6.3 -10.16 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))')
items.append('\t(fp_text user "ANT" (at -1.4 10.75 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))')
# Ceramic antenna clearance (formix): no copper on any layer.
items.append('\t(zone (net 0) (net_name "") (layers "F.Cu" "B.Cu") (hatch edge 0.5) (connect_pads (clearance 0)) '
             '(min_thickness 0.25) (keepout (tracks not_allowed) (vias not_allowed) (pads not_allowed) '
             '(copperpour not_allowed) (footprints allowed)) (placement (enabled no) (sheetname "")) '
             '(fill (thermal_gap 0.5) (thermal_bridge_width 0.5)) '
             '(polygon (pts (xy -6.75 9.25) (xy -6.75 12.25) (xy 4 12.25) (xy 4 9.25))))')
items.append(f'\t(model "${{KIPRJMOD}}/../../lib/pcb12.pretty/waveshare_esp32_s3_zero_v2.step" '
             '(offset (xyz -9 -11.75 0.8)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))')
items.append(')')
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("\n".join(items) + "\n")
print(OUT)
