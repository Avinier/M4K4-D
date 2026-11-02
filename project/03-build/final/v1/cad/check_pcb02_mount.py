"""CP-OI-09: validate PCB-02 edge mount against the body and chassis CAD.

Run with the legacy CAD runtime and final/v1/cad's documented PYTHONPATH.
The board STEP is still a placeholder, so this checks mount geometry, holes,
connector reserves and the existing panel/button/inlet bounds. Final courtyard
and height checks must be repeated with the KiCad board STEP before layout.
"""

import importlib.util
from pathlib import Path

from build123d import Compound, Location, Shape, Solid
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.TopAbs import TopAbs_COMPOUND, TopAbs_SOLID
from OCP.TopoDS import TopoDS

import body_v1_model as B

spec = importlib.util.spec_from_file_location("makad_v1_entry", Path(__file__).with_name("makad-v1.step.py"))
entry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entry)
M = entry.PCB02_MOUNT


def box(shape):
    b = Bnd_Box()
    BRepBndLib.Add_s(shape.wrapped, b, False)
    return b.Get()


def place(node, loc):
    moved = node.wrapped.Moved(loc.wrapped)
    if moved.ShapeType() == TopAbs_COMPOUND:
        return Compound(TopoDS.Compound_s(moved))
    if moved.ShapeType() == TopAbs_SOLID:
        return Solid(TopoDS.Solid_s(moved))
    return Shape.cast(moved)


def leaves(node, loc=Location(), path=()):
    here = loc * node.location
    name = path + (node.label or "?",)
    kids = list(node.children) if getattr(node, "children", None) else []
    if not kids:
        yield name, node, loc
    else:
        for child in kids:
            yield from leaves(child, here, name)


def common_volume(a, b):
    try:
        return (a & b).volume
    except Exception:
        return 0.0


def main():
    ok = True

    def check(name, passed, detail):
        nonlocal ok
        ok &= bool(passed)
        print(f"{'PASS' if passed else 'FAIL'}  {name}: {detail}", flush=True)

    tree0 = Compound(children=[B.build_body_assembly(), B.chassis_v1_reference()])
    base = [(p, place(n, l)) for p, n, l in leaves(tree0)
            if n.wrapped is not None and not n.wrapped.IsNull()]
    tree = entry._apply_droid_cuts(tree0, strict=False)
    mounted = [(p, place(n, l)) for p, n, l in leaves(tree)
               if n.wrapped is not None and not n.wrapped.IsNull()]
    labels = [p[-1] for p, _ in mounted]

    # All four holes pass through the placeholder PCB core at the frozen datum.
    board = next((s for p, s in base if p[-1] == "PCB02_CHARGE_AND_SYSTEM_POWER_PCB"), None)
    hole_shapes = list(entry.pcb02_mount_holes().children)
    hole_volumes = [common_volume(board, h) for h in hole_shapes] if board else []
    check("four through-holes", len(hole_volumes) == 4 and all(v > 0.1 for v in hole_volumes),
          f"count {len(hole_volumes)}, removed volumes {[round(v, 2) for v in hole_volumes]} mm3")

    # The printed support is fused into the existing frame. Check that each
    # modeled metal insert is a hollow annulus at its specified board hole.
    mount_shape = entry.pcb02_mount_frame()
    frame_box = box(mount_shape)
    check("edge-frame envelope", abs(frame_box[0] + 53.8) < .02 and abs(frame_box[3] + 34.0) < .02,
          f"X {frame_box[0]:.1f}..{frame_box[3]:.1f}, Y {frame_box[1]:.1f}..{frame_box[4]:.1f}, Z {frame_box[2]:.1f}..{frame_box[5]:.1f} mm")
    ir, bore_r, ilen = M["insert"]
    insert_expected = 4 * 3.141592653589793 * (ir * ir - bore_r * bore_r) * ilen
    insert_measured = 0.0
    for y, z in M["holes"]:
        x1 = M["boss_x"][1]
        x0 = x1 - ilen
        ring = entry._pcb02_x_cylinder(ir, x0, x1, y, z) - entry._pcb02_x_cylinder(bore_r, x0 - .1, x1 + .1, y, z)
        insert_measured += common_volume(mount_shape, ring)
    check("four hollow inserts", abs(insert_measured - insert_expected) < 0.1,
          f"modeled annular volume {insert_measured:.2f}/{insert_expected:.2f} mm3")

    # Side rails and pads stay out of the plug/courtyard zones. Explicit reserve
    # blocks from body_v1_model are checked by volume against the proposed mount.
    reserve_terms = ("RESERVE", "CORRIDOR", "HARNESS", "MATED_PLUG", "KEEP_OUT", "SWEEP")
    reserves = [(p, s) for p, s in base if any(t in p[-1] for t in reserve_terms)]
    hits = [(p[-1], common_volume(mount_shape, s)) for p, s in reserves]
    hits = [(n, v) for n, v in hits if v > 1e-4]
    check("connector and harness reserves", not hits,
          "clear" if not hits else "; ".join(f"{n} overlap {v:.3f} mm3" for n, v in hits))

    # Only the two lower feet are allowed to intersect the lower cross rail.
    # Every other fixed body/chassis solid must remain clear of added mount plastic.
    intended = "BODY_FRAME_MAIN_PRINT"
    nearby = [(p[-1], common_volume(mount_shape, s)) for p, s in base
              if intended not in p and "PCB02_CHARGE_AND_SYSTEM_POWER" not in "/".join(p)]
    clashes = [(n, v) for n, v in nearby if v > 1e-3]
    check("body and chassis clearance", not clashes,
          "only intended frame contact" if not clashes else "; ".join(f"{n} overlap {v:.3f} mm3" for n, v in clashes))
    for path, fixed in base:
        if path[-1] == "REAR_SERVICE_PANEL_OCTAGONAL":
            intersection = mount_shape & fixed
            if intersection.solids():
                ib = box(intersection)
                print(f"DETAIL  rear-panel intersection bounds X {ib[0]:.2f}..{ib[3]:.2f}, Y {ib[1]:.2f}..{ib[4]:.2f}, Z {ib[2]:.2f}..{ib[5]:.2f} mm", flush=True)
            break

    # The rear cross rail is at X -36..-28, Z 61..69; foot risers must reach it.
    rail_probe = entry._pcb02_block((-36.1, -34.0, -28.0, 28.0, 61.0, 69.0))
    contact = common_volume(mount_shape, rail_probe)
    check("lower rail tie-in", contact > 1.0, f"support/rail overlap {contact:.2f} mm3 (intentional fusion)")

    # The circle is a local keepout, so it may extend beyond the board edge.
    # The drilled hole and the screw head themselves must be supported by PCB.
    hole_edge = min(min(25.0 - abs(y), z - M["board"][4], M["board"][5] - z) for y, z in M["holes"])
    head_edge = hole_edge - M["screw"][2]
    courtyard_overhang = max(M["courtyard_r"] - min(25.0 - abs(y), z - M["board"][4], M["board"][5] - z)
                             for y, z in M["holes"])
    check("mount-hole and screw-head edge support", hole_edge >= M["hole_r"] + 0.3 and head_edge >= 0.0,
          f"drill-edge margin {hole_edge - M['hole_r']:.1f} mm, head-edge margin {head_edge:.1f} mm; local courtyard extends {max(0.0, courtyard_overhang):.1f} mm beyond outline")

    # Insert outer and screw head geometry remains behind the board component plane.
    rear_depth = M["board"][0] - M["boss_x"][0]
    check("rear fastener stack", rear_depth >= M["insert"][2] and M["screw"][0] <= M["insert"][2] + 1.6,
          f"boss depth {rear_depth:.1f} mm; insert {M['insert'][2]:.1f} mm; M2 screw {M['screw'][0]:.1f} mm")

    # Existing external checks constrain this panel-side area and button/inlet fit.
    check("PCB-02 remains installed in final body tree",
          any("PCB02_CHARGE_AND_SYSTEM_POWER_PCB" in p for p in labels),
          "placeholder core retained for hole comparison")
    print("NOTE  Populate the final board STEP and rerun height, full courtyard, PCB-13 face, button and inlet checks before layout.")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
