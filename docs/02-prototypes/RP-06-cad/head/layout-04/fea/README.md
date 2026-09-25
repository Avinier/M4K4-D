# Pitch-frame stiffness FEA

Linear-elastic screen of the P-frame part `connected_pitch_frame_roll_servo_saddle` for its pitch and roll torsional stiffness. The results are in [`results.json`](results.json). This is an `E`-grade structural screen: a single PLA part, isotropic, fully dense, bonded, and without the bolted cartridge. It is not a modal test and not RP-01 P07 evidence on its own.

## Method

- **Geometry:** `export_frame.py` builds the layout with `catalog=False` and exports only the frame solid, plus the A0 datums, to STEP and JSON.
- **Mesh:** gmsh 4.15. Frontal-Delaunay surface mesh, Delaunay volume mesh, maximum element size 1.4 mm (1.0 mm to check convergence). Zero-volume sliver tets from boolean seams are dropped (at most 2 per mesh).
- **Solver:** scikit-fem 12, quadratic tetrahedra (P2 displacement). PLA at E = 3.5 GPa, ν = 0.35; 2.3 GPa for the low-modulus case. Units are mm, N and MPa.
- **Pitch case:** the +Y trunnion bore is clamped (the servo horn). The passive −Y trunnion is left free, since it gives no pitch restraint. A 1 N·m **pure couple** about +Y is applied as a rotational traction on the cartridge seat, the slab top face that carries the rolling assembly's mass.
- **Roll case:** both trunnion bores are clamped. A 1 N·m pure couple about +X is applied on the roll-servo case interfaces: the saddle wall inner faces, plus the two case-screw bores when present.
- **Pure couple:** each traction is centred on its loaded faces' own centroid. A rotational traction centred anywhere else also carries a net force; an early run centred on the pitch axis bent the frame and understated the new design by 10×. A0 puts the head CoM on the axes, so the real inertial load on the frame is a couple.
- **Stiffness:** `k = M / θ`, where θ is the least-squares rigid rotation of the loaded faces. The pitch run also prints the rotation reached at stations along the load path (arm, web, box, slab) as fractions of θ. That breakdown is how the box-to-slab joint was found and replaced by the keel.

## Reproduce

```bash
uv venv fea --python 3.12 && uv pip install --python fea/bin/python gmsh scikit-fem meshio scipy numpy
# the frame export uses the RP-06 legacy CAD runtime
~/.codex/runtimes/text-to-cad/0.4.28/venv/bin/python fea/export_frame.py . /tmp/frame_new
fea/bin/python fea/frame_fea.py /tmp/frame_new pitch 3500 1.4
fea/bin/python fea/frame_fea.py /tmp/frame_new roll 3500 1.4
```

For the old frame, run the same commands on `git archive` of the parent commit's `layout-04` folder.

## Not included

- The bolted bearing cartridge. It would stiffen the slab region, so leaving it out is conservative.
- Screw and insert compliance.
- Print anisotropy and infill.
- Bearing and trunnion clearance.
- The servo's own gear train, horn and case compliance, and the coupling. These are `U`, and in series they may govern the real mode. That is what bench tap test B6 is for.
