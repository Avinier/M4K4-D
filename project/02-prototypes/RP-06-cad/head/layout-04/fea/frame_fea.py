"""Linear-elastic FEA of the head pitch frame (P frame) for its pitch and roll
torsional stiffness. Quadratic tetrahedra (P2 displacement on a linear-geometry
gmsh mesh). Units mm, N, MPa. argv: prefix (reads prefix.step/.json), case.

pitch: +Y trunnion bore clamped (servo horn side); a unit moment about the
       pitch axis is applied as a rotational traction on the cartridge seat
       (slab top face), where the rolling assembly's mass is carried. The
       passive -Y trunnion is left free: it gives no torque restraint.
roll:  both trunnion bores clamped; a unit moment about the roll axis is
       applied on the servo-case interfaces (saddle wall inner faces, plus the
       two case-screw bores when present).
Stiffness k = M / theta, theta the least-squares rigid rotation of the loaded
faces about the loading axis.
"""
import sys, json, math
import numpy as np
import gmsh
from skfem import (MeshTet, Basis, FacetBasis, ElementVector, ElementTetP2, asm, solve,
                   condense, LinearForm, BilinearForm)
from skfem.models.elasticity import linear_elasticity, lame_parameters
from skfem.helpers import dot

prefix, case = sys.argv[1], sys.argv[2]
E = float(sys.argv[3]) if len(sys.argv) > 3 else 3500.0
H = float(sys.argv[4]) if len(sys.argv) > 4 else 1.6
meta = json.load(open(prefix + '.json'))
px, pz, ry, rz = meta['pitch_x'], meta['pitch_z'], meta['roll_y'], meta['roll_z']

gmsh.initialize(); gmsh.option.setNumber('General.Terminal', 0)
gmsh.model.occ.importShapes(prefix + '.step'); gmsh.model.occ.synchronize()
gmsh.option.setNumber('Mesh.Algorithm', 6); gmsh.option.setNumber('Mesh.Algorithm3D', 1)
gmsh.option.setNumber('Mesh.MeshSizeMax', H); gmsh.option.setNumber('Mesh.MeshSizeMin', H / 4)
gmsh.model.mesh.generate(3)
nodes, coords, _ = gmsh.model.mesh.getNodes()
X = coords.reshape(-1, 3); idx = {int(t): i for i, t in enumerate(nodes)}
types, _, conn = gmsh.model.mesh.getElements(3)
tets = np.array([idx[int(t)] for t in conn[list(types).index(4)]]).reshape(-1, 4)
gmsh.finalize()
vol = np.abs(np.einsum('ij,ij->i', np.cross(X[tets[:, 1]] - X[tets[:, 0]], X[tets[:, 2]] - X[tets[:, 0]]), X[tets[:, 3]] - X[tets[:, 0]])) / 6
tets = tets[vol > 1e-4]
print('dropped degenerate tets', int((vol <= 1e-4).sum()), 'volume kept', float(vol[vol > 1e-4].sum()), flush=True)
used = np.unique(tets); remap = -np.ones(len(X), int); remap[used] = np.arange(len(used))
mesh = MeshTet(X[used].T, remap[tets].T)
print('mesh', mesh.nelements, 'tets', mesh.nvertices, 'vertices', flush=True)

e = ElementVector(ElementTetP2()); ib = Basis(mesh, e)
lam, mu = lame_parameters(E, 0.35)
K = asm(linear_elasticity(lam, mu), ib)

def near_bore(x, y0, y1):
    r = np.hypot(x[0] - px, x[2] - pz)
    return (np.abs(r - 4.2) < 0.35) & (x[1] > y0 - 0.1) & (x[1] < y1 + 0.1)

if case == 'pitch':
    fixed = mesh.facets_satisfying(lambda x: near_bore(x, 44.5, 53.5))
    axis_pt, axis_dir = np.array([px, 0, pz]), np.array([0., 1., 0.])
    zc = rz - 12.0
    loaded = mesh.facets_satisfying(lambda x: (np.abs(x[2] - zc) < 0.05) & (x[0] > -69.1) & (x[0] < -38.9) & (np.abs(x[1] - ry) < 12.1))
else:
    fixed = np.concatenate([mesh.facets_satisfying(lambda x: near_bore(x, 44.5, 53.5)),
                            mesh.facets_satisfying(lambda x: near_bore(x, -53.5, -44.5))])
    axis_pt, axis_dir = np.array([0, ry, rz]), np.array([1., 0., 0.])
    def iface(x):
        wall = (np.abs(np.abs(x[1] - ry) - 10.2) < 0.05) & (x[0] > -107.1) & (x[0] < -74) & (x[2] > rz - 26.1) & (x[2] < rz - 11.9)
        screw = np.zeros_like(wall)
        for dy in (-8.0, 8.0):
            screw |= (np.abs(np.hypot(x[1] - ry - dy, x[2] - rz + 22.5) - 1.15) < 0.1) & (x[0] > -80.6) & (x[0] < -78.4)
        return wall | screw
    loaded = mesh.facets_satisfying(iface)
print('fixed facets', len(fixed), 'loaded facets', len(loaded), flush=True)
assert len(fixed) and len(loaded)

fb = FacetBasis(mesh, e, facets=loaded)
# Pure couple: centre the rotational traction on the loaded faces' centroid
# (an off-centroid rotational traction also carries a net force). The head's
# CoM is on its axes (A0), so its inertial load on the frame is a couple.
from skfem import Functional
_sb = FacetBasis(mesh, ElementTetP2(), facets=loaded)
_A = Functional(lambda w: 1.0 + 0 * w.x[0]).assemble(_sb)
axis_pt = np.array([Functional(lambda w, i=i: w.x[i]).assemble(_sb) / _A for i in range(3)])
print('load centroid', axis_pt.round(2), flush=True)

def rperp(x):
    d = np.stack([x[i] - axis_pt[i] for i in range(3)])
    along = sum(d[i] * axis_dir[i] for i in range(3))
    return np.stack([d[i] - along * axis_dir[i] for i in range(3)])

@LinearForm
def unit_rot(v, w):
    r = rperp(w.x)
    t = np.stack([axis_dir[1] * r[2] - axis_dir[2] * r[1], axis_dir[2] * r[0] - axis_dir[0] * r[2], axis_dir[0] * r[1] - axis_dir[1] * r[0]])
    return dot(t, v)

# Traction t = c (axis x r); its moment is c * integral |r|^2 dA, set to 1 N*m.
I2 = Functional(lambda w: sum(rperp(w.x)[i] ** 2 for i in range(3))).assemble(FacetBasis(mesh, ElementTetP2(), facets=loaded))
M = 1000.0  # N*mm
f = asm(unit_rot, fb) * (M / I2)
D = ib.get_dofs(fixed).all()
u = solve(*condense(K, f, D=D))
# theta: least squares rigid rotation of the loaded faces = integral (r x u).a dA / integral |r|^2 dA
theta = (asm(unit_rot, fb) @ u) / I2
k = M / theta / 1000.0  # N*m/rad
if case == 'pitch':
    ux, uz = u[ib.nodal_dofs[0]], u[ib.nodal_dofs[2]]
    P = mesh.p
    def rot_at(mask):
        dx, dz = P[0, mask] - P[0, mask].mean(), P[2, mask] - P[2, mask].mean()
        r2s = dx ** 2 + dz ** 2
        # rotation about +Y: u = theta * (dz, -dx) in (x, z)
        uxm, uzm = ux[mask] - ux[mask].mean(), uz[mask] - uz[mask].mean()
        return float(np.sum(uxm * dz - uzm * dx) / np.sum(r2s))
    stations = {
        'arm_top_y49': (np.abs(P[1] - 49) < 2) & (P[2] > pz - 6) & (np.abs(P[0] - px) < 6),
        'web_front_y49_x-50': (np.abs(P[1] - 49) < 2) & (np.abs(P[0] + 50) < 1.5),
        'web_rear_y49_x-72': (np.abs(P[1] - 49) < 2) & (np.abs(P[0] + 72) < 1.5),
        'box_y25': (np.abs(P[1] - 25) < 1.5) & (P[0] < -68) & (P[0] > -80.5),
        'box_y0': (np.abs(P[1] - ry) < 1.5) & (P[0] < -68) & (P[0] > -80.5),
        'slab_x-60': (np.abs(P[0] + 60) < 1.5) & (np.abs(P[1] - ry) < 12) & (np.abs(P[2] - (rz - 14)) < 2.5),
        'slab_x-45': (np.abs(P[0] + 45) < 1.5) & (np.abs(P[1] - ry) < 12) & (np.abs(P[2] - (rz - 14)) < 2.5),
    }
    print(json.dumps({k: (round(rot_at(v) / theta, 3) if v.any() else None) for k, v in stations.items()}), flush=True)
print(json.dumps(dict(case=case, E_MPa=E, mesh_h=H, tets=int(mesh.nelements), moment_Nmm=M, theta_rad=theta, k_Nm_per_rad=k)), flush=True)
