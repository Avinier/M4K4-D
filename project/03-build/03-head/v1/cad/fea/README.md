# Head v1 stiffness FEA (D-049)

Linear-elastic screen of the head v1 pitch frame (`connected_pitch_frame_roll_servo_saddle`, P) and the +Y yoke leg (`yaw_yoke_leg_55`, Y) for the D-049 STS3045M installation. The method is the RP-06 Layout 04 one ([its README](../../../../../02-prototypes/RP-06-cad/head/layout-04/fea/README.md)): gmsh tetrahedra, scikit-fem P2 elasticity, PLA E = 3.5 GPa (2.3 GPa low case), ν = 0.35, a 1 N·m pure couple centred on the loaded faces, and `k = M/θ` with θ the least-squares rigid rotation of those faces. Results are in [`results.json`](results.json). This is an `E` structural screen, not a modal test or RP-01 P07 evidence on its own.

## Load cases

D-049 moved the pitch actuator onto the pitch frame: its horn is screwed to the +Y yoke leg, so the pitch reaction runs servo case → ear seats → frame, and output → horn → +Y leg → disc.

- **Pitch:** the four pitch-servo ear seats on the collar are clamped; the couple about +Y acts on the cartridge seat (slab top face under the cartridge). The −Y trunnion gives no torque restraint and is left free.
- **Roll:** the −Y trunnion bore and the pitch-servo ear seats (the two pitch-axis supports) are clamped; the couple about +X acts on the four roll-servo ear seats on the mount plate.
- **Leg:** the +Y leg is clamped on its foot (the disc top); the couple about +Y acts on the horn pocket floor (the horn's clamp face). The old 41 Hz frame result never included this leg, although the XC330 adapter also hung the pitch reaction on it.

The frame and leg are springs in series. Frequencies are `f = √(k/J)/2π` with `J` the D-049 mass tree's pitch (R+P) or roll (R) inertia about the solved axes.

## Reproduce

```bash
uv venv fea-venv --python 3.12 && uv pip install --python fea-venv/bin/python gmsh scikit-fem meshio scipy numpy
~/.codex/runtimes/text-to-cad/0.4.28/venv/bin/python fea/export_parts.py /tmp/head   # writes /tmp/head_frame.step, _leg.step, .json
fea-venv/bin/python fea/frame_fea.py /tmp/head pitch 3500 1.4
fea-venv/bin/python fea/frame_fea.py /tmp/head roll 3500 1.4
fea-venv/bin/python fea/frame_fea.py /tmp/head leg 3500 1.4
```

## Not included

The bolted cartridge (conservative), screw and insert compliance, print anisotropy and infill, the servo gear train, horn/spline and coupler lash and compliance, the yaw disc and its body bearing. These are in series and may govern the real mode; bench test B6 measures it.
