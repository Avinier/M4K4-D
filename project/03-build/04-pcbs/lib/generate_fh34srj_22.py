"""Generate the shared FH34SRJ-22S-0.5SH(99) KiCad footprint.

Dimensions follow Hirose FH34 series catalog, recommended PCB mounting pattern,
22 positions (2026-04-01), and the part's 13 x 3.8 mm body. Local +Y is the
FFC insertion direction; contact 1 is at local +X. The signal paste
apertures follow Hirose's 0.1 mm stencil recommendation. The final stencil
still needs assembly-process review.
"""

from pathlib import Path

NAME = "Hirose_FH34SRJ-22S-0.5SH_1x22_P0.50mm"
OUT = Path(__file__).parent / "fh34.pretty" / f"{NAME}.kicad_mod"


def line(x0, y0, x1, y1, layer, width):
    return (f'\t(fp_line (start {x0} {y0}) (end {x1} {y1}) '
            f'(stroke (width {width}) (type solid)) (layer "{layer}"))')


def pad(number, x, y, sx, sy, layers):
    return (f'\t(pad "{number}" smd rect (at {x:.3f} {y:.3f}) '
            f'(size {sx:.3f} {sy:.3f}) (layers {layers}))')


items = [
    f'(footprint "{NAME}"',
    '\t(version 20241229)',
    '\t(generator "makad-generate_fh34srj_22")',
    '\t(layer "F.Cu")',
    '\t(descr "Hirose FH34SRJ-22S-0.5SH(99); local +Y = FFC entry; catalog land pattern, 2026-04-01")',
    '\t(tags "FFC FPC 0.5mm FH34SRJ")',
    '\t(property "Reference" "REF**" (at 0 -3.2 0) (layer "F.SilkS") '
    '(effects (font (size 0.8 0.8) (thickness 0.12))))',
    f'\t(property "Value" "{NAME}" (at 0 3.2 0) (layer "F.Fab") '
    '(effects (font (size 0.8 0.8) (thickness 0.12))))',
    '\t(attr smd)',
]

# Hirose B=10.5 mm between end contact centres, pitch 0.5 mm. The 22 copper
# contacts are 0.3 x 0.8 mm; two 0.4 x 0.8 mm mechanical solder tabs have
# inner/outer X limits E/2=6.05 and F/2=6.45 mm. Row separation is 3.3 mm.
for number in range(1, 23):
    x = 5.25 - (number - 1) * 0.5
    items.append(pad(number, x, -1.65, 0.3, 0.8, '"F.Cu" "F.Mask"'))
    # Hirose recommended 0.1 mm stencil: 0.25 x 0.65 mm signal aperture.
    items.append(pad("", x, -1.65, 0.25, 0.65, '"F.Paste"'))
for x in (-6.25, 6.25):
    items.append(pad("", x, 1.65, 0.4, 0.8, '"F.Cu" "F.Paste" "F.Mask"'))

# The 13 x 3.8 mm closed housing and 0.25 mm assembly clearance.
for x0, y0, x1, y1 in [
    (-6.5, -1.9, 6.5, -1.9), (6.5, -1.9, 6.5, 1.9),
    (6.5, 1.9, -6.5, 1.9), (-6.5, 1.9, -6.5, -1.9),
]:
    items.append(line(x0, y0, x1, y1, "F.Fab", 0.1))
for x0, y0, x1, y1 in [
    (-6.75, -2.30, 6.75, -2.30), (6.75, -2.30, 6.75, 2.30),
    (6.75, 2.30, -6.75, 2.30), (-6.75, 2.30, -6.75, -2.30),
]:
    items.append(line(x0, y0, x1, y1, "F.CrtYd", 0.05))
items.append(line(-5.8, 2.05, 5.8, 2.05, "F.SilkS", 0.12))
items.append(line(5.7, -2.3, 6.2, -2.3, "F.SilkS", 0.12))
items.append(line(6.2, -2.3, 6.2, -2.15, "F.SilkS", 0.12))
items.append('\t(fp_text user "FFC ENTRY" (at 0 1.0 0) (layer "F.Fab") '
             '(effects (font (size 0.5 0.5) (thickness 0.08))))')
items.append(')')
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("\n".join(items) + "\n")
print(OUT)
