"""Labeled envelope primitives. Colour lives on leaves."""

from __future__ import annotations

from cadgen import build123d as bd
from cadgen import srgb
from cadgen.assembly import label_shape


def _paint(shape, name: str, color: str, alpha: float = 1.0):
    shape = label_shape(shape, name)
    shape.color = srgb(color, alpha)
    return shape


def box(dx, dy, dz, name, color, center=(0, 0, 0), alpha=1.0):
    s = bd.Pos(*center) * bd.Box(dx, dy, dz)
    return _paint(s, name, color, alpha)


def cyl(r, h, name, color, center=(0, 0, 0), axis="z", alpha=1.0):
    c = bd.Cylinder(r, h)
    if axis == "x":
        c = bd.Rot(0, 90, 0) * c
    elif axis == "y":
        c = bd.Rot(90, 0, 0) * c
    s = bd.Pos(*center) * c
    return _paint(s, name, color, alpha)


def sphere(r, name, color, center=(0, 0, 0), alpha=1.0):
    s = bd.Pos(*center) * bd.Sphere(r)
    return _paint(s, name, color, alpha)


def triad(origin, name_prefix, scale=12.0):
    """RGB axis triad at a named frame. Inspection geometry, not structure."""
    ox, oy, oz = origin
    x = cyl(0.6, scale, f"{name_prefix}_x", "#E11D48", (ox + scale / 2, oy, oz), "x")
    y = cyl(0.6, scale, f"{name_prefix}_y", "#16A34A", (ox, oy + scale / 2, oz), "y")
    z = cyl(0.6, scale, f"{name_prefix}_z", "#2563EB", (ox, oy, oz + scale / 2), "z")
    hub = sphere(1.4, f"{name_prefix}_o", "#111827", origin)
    return bd.Compound(children=[x, y, z, hub])
