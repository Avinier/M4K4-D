"""Shared helpers for the final-tree check scripts (D-095 bought-module checks and PCB-09 checks).

Run the check scripts from this folder with the legacy runtime and PYTHONPATH in ../README.md.
`droid_tree()` builds the chassis and body trees with every droid edit (about 40 s) and adds the
"Bought modules" group; the head is not built. Vendor Pi and cooler STEPs are tested as boxes
(pi-step-stalls-clash-checks). Interference is a world-frame BRepAlgoAPI_Common volume; clearance
is BRepExtrema distance, never on vendor leaves.
"""

import importlib.util
import json
import sys
import time
from pathlib import Path

from build123d import Box, Compound, Location, Shape, Solid
from OCP.Bnd import Bnd_Box
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
from OCP.BRepBndLib import BRepBndLib
from OCP.BRepExtrema import BRepExtrema_DistShapeShape
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
from OCP.TopAbs import TopAbs_COMPOUND, TopAbs_SOLID
from OCP.TopoDS import TopoDS

HERE = Path(__file__).resolve().parent
VENDOR = ("C0_RASPBERRY_PI5_EXACT_STEP", "PI5_ACTIVE_COOLER_STEP")
NOT_PARTS = ("RESERVE", "KEEP_OUT", "KEEPOUT", "CORRIDOR", "HARNESS", "OVERLAY", "PHYSICS", "SWEEP", "ENVELOPE_CHECK")
_T0 = time.time()


def log(msg):
    print(f"... {msg} ({time.time() - _T0:.0f} s)", flush=True)


def load_entry(name="makad-v1.step.py", module="makad_v1_entry"):
    spec = importlib.util.spec_from_file_location(module, HERE / name)
    entry = importlib.util.module_from_spec(spec)
    sys.modules[module] = entry
    spec.loader.exec_module(entry)
    return entry


def _box(shape):
    w = shape.wrapped if hasattr(shape, "wrapped") else shape
    if w is None or w.IsNull():
        return (1e9, 1e9, 1e9, -1e9, -1e9, -1e9)   # empty: hits nothing
    b = Bnd_Box()
    BRepBndLib.Add_s(w, b, False)
    return b.Get()


def _hit(a, b, pad=0.0):
    return not (a[3] + pad <= b[0] or b[3] + pad <= a[0] or a[4] + pad <= b[1] or
                b[4] + pad <= a[1] or a[5] + pad <= b[2] or b[5] + pad <= a[2])


def _leaves(node, loc=Location(), path=()):
    here = loc * node.location
    kids = list(node.children) if getattr(node, "children", None) else []
    name = path + (node.label or "?",)
    if not kids or any(v in (node.label or "") for v in VENDOR):
        yield name, node, loc
        return
    for kid in kids:
        yield from _leaves(kid, here, name)


def place(node, loc):
    """The leaf at its world place, sharing its geometry (TopoDS Moved, no copy)."""
    m = node.wrapped.Moved(loc.wrapped)
    if m.ShapeType() == TopAbs_COMPOUND:
        return Compound(TopoDS.Compound_s(m))
    if m.ShapeType() == TopAbs_SOLID:
        return Solid(TopoDS.Solid_s(m))
    return Shape.cast(m)


def blk(b):
    """Box from (x0, x1, y0, y1, z0, z1)."""
    return Box(b[1] - b[0], b[3] - b[2], b[5] - b[4]).moved(Location(((b[0] + b[1]) / 2, (b[2] + b[3]) / 2, (b[4] + b[5]) / 2)))


def bbox_shape(bb):
    """Box from a Bnd_Box tuple (x0, y0, z0, x1, y1, z1)."""
    return blk((bb[0], bb[3], bb[1], bb[4], bb[2], bb[5]))


def volume(shape):
    w = shape.wrapped if hasattr(shape, "wrapped") else shape
    p = GProp_GProps()
    BRepGProp.VolumeProperties_s(w, p)
    return p.Mass()


def common(a, b):
    """World-frame intersection volume, mm3."""
    op = BRepAlgoAPI_Common(a.wrapped if hasattr(a, "wrapped") else a, b.wrapped if hasattr(b, "wrapped") else b)
    assert op.IsDone()
    return volume(op.Shape())


def distance(a, b):
    d = BRepExtrema_DistShapeShape(a.wrapped if hasattr(a, "wrapped") else a, b.wrapped if hasattr(b, "wrapped") else b)
    d.Perform()
    return d.Value() if d.IsDone() else float("nan")


def is_part(path):
    return not any(t in "/".join(path).upper() for t in NOT_PARTS)


class Leaf:
    __slots__ = ("path", "label", "shape", "box", "vendor")

    def __init__(self, path, shape, vendor):
        self.path, self.label, self.shape, self.vendor = path, path[-1], shape, vendor
        self.box = _box(shape)

    @property
    def solid(self):
        """Shape for booleans: the box for vendor STEPs."""
        return bbox_shape(self.box) if self.vendor else self.shape


def droid_tree(entry=None, with_modules=True):
    """(entry, tree, leaves) for the chassis + body trees with all droid edits and the bought modules."""
    entry = entry or load_entry()
    import body_v1_model as B
    tree = entry._apply_droid_cuts(Compound(children=[B.build_body_assembly(), B.chassis_v1_reference()]), strict=False)
    if with_modules:
        tree = Compound(children=[tree, entry.bought_modules()])
    log("droid tree built")
    leaves = [Leaf(p, place(n, l), any(v in p[-1] for v in VENDOR)) for p, n, l in _leaves(tree)]
    return entry, tree, leaves


def find(leaves, label):
    hits = [lf for lf in leaves if lf.label == label]
    assert len(hits) == 1, (label, len(hits))
    return hits[0]


def clashes(subject, leaves, skip=(), pad=0.0, min_vol=1e-4, parts_only=True):
    """[(label, volume)] of leaves intersecting `subject` (a shape), boxes pre-filtered."""
    sb = _box(subject)
    out = []
    for lf in leaves:
        if (parts_only and not is_part(lf.path)) or any(s in "/".join(lf.path) for s in skip):
            continue
        if not _hit(sb, lf.box, pad):
            continue
        v = common(subject, lf.solid)
        if v > min_vol:
            out.append((lf.label, round(v, 4)))
    return out


def min_gap(subject, leaves, skip=(), reach=3.0, parts_only=True):
    """(gap, label) to the nearest leaf within `reach`; vendor leaves as boxes."""
    sb = _box(subject)
    best = (reach, None)
    for lf in leaves:
        if (parts_only and not is_part(lf.path)) or any(s in "/".join(lf.path) for s in skip):
            continue
        if not _hit(sb, lf.box, best[0]):
            continue
        d = distance(subject, lf.solid)
        if d < best[0]:
            best = (d, lf.label)
    return best


class Report:
    """Named pass/fail rows with measured values; writes JSON beside the script and exits non-zero on failure."""

    def __init__(self, name):
        self.name, self.rows = name, []

    def check(self, key, ok, **values):
        self.rows.append(dict(check=key, ok=bool(ok), **{k: _jsonable(v) for k, v in values.items()}))
        print(f"{'PASS' if ok else 'FAIL'}  {key}  " + "  ".join(f"{k}={_short(v)}" for k, v in values.items()), flush=True)
        return ok

    def finish(self):
        passed = sum(r["ok"] for r in self.rows)
        out = HERE / f"{self.name}-report.json"
        out.write_text(json.dumps(dict(script=self.name, passed=passed, total=len(self.rows), rows=self.rows), indent=1) + "\n")
        print(f"\n{self.name}: {passed}/{len(self.rows)} pass -> {out.name}")
        sys.exit(0 if passed == len(self.rows) else 1)


def _jsonable(v):
    if isinstance(v, float):
        return round(v, 4)
    if isinstance(v, (list, tuple)):
        return [_jsonable(x) for x in v]
    if isinstance(v, dict):
        return {k: _jsonable(x) for k, x in v.items()}
    return v


def _short(v):
    s = json.dumps(_jsonable(v))
    return s if len(s) < 160 else s[:157] + "..."


def moved(shape, v):
    """A copy of a world shape translated by v, sharing geometry."""
    return place(shape, Location(tuple(v)))


def frac_inside(tool, solid):
    """Share of `tool`'s volume inside `solid` (1.0: fully embedded)."""
    v = volume(tool)
    return common(tool, solid) / v if v > 0 else 0.0


def point_in(solid, xyz):
    from OCP.BRepClass3d import BRepClass3d_SolidClassifier
    from OCP.TopAbs import TopAbs_IN
    from OCP.gp import gp_Pnt
    c = BRepClass3d_SolidClassifier(solid.wrapped if hasattr(solid, "wrapped") else solid, gp_Pnt(*xyz), 1e-6)
    return c.State() == TopAbs_IN


def ray(solid, origin, direction):
    """Material intervals [(t0, t1)] of `solid` along origin + t * direction (unit vector)."""
    from OCP.IntCurvesFace import IntCurvesFace_ShapeIntersector
    from OCP.gp import gp_Dir, gp_Lin, gp_Pnt
    hit = IntCurvesFace_ShapeIntersector()
    hit.Load(solid.wrapped if hasattr(solid, "wrapped") else solid, 1e-6)
    hit.Perform(gp_Lin(gp_Pnt(*origin), gp_Dir(*direction)), -1e9, 1e9)
    ws = sorted(hit.WParameter(i) for i in range(1, hit.NbPnt() + 1))
    ws = [w for k, w in enumerate(ws) if k == 0 or w - ws[k - 1] > 1e-4]
    return list(zip(ws[0::2], ws[1::2]))


def sweep(subjects, leaves, direction, distances, skip=(), parts_only=True):
    """First (distance, subject label, leaf label, volume) where a translated subject meets a leaf, or None.

    subjects: [(label, shape)]. Each subject is tested at every offset in `distances` along `direction`.
    """
    for d in distances:
        v = tuple(d * c for c in direction)
        for label, shape in subjects:
            hits = clashes(moved(shape, v), leaves, skip=skip, parts_only=parts_only)
            if hits:
                return (d, label, *hits[0])
    return None


def own(leaves, *tokens):
    """Leaves whose path contains any of `tokens`."""
    return [lf for lf in leaves if any(t in "/".join(lf.path) for t in tokens)]
