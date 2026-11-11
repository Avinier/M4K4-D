"""Planar elastica for a flat cable loop: the shape of a strip of fixed length clamped at both ends.

The strip is split into n equal segments with headings theta_i (rad, from +x towards
+z, unwrapped). Bending energy plus the strip's own weight,
    E / EI = sum((theta_{i+1} - theta_i)^2) / (2 ds) + (q / EI) * ds * sum(z_i),
is minimised subject to the end position and the two clamp headings (an inextensible
strip, gravity along -z). q / EI is the weight per length over the bending stiffness
(1/mm^3); 0 gives the weightless shape. Used by check_d105_csi_loop.py (D-105).
"""

import math

import numpy as np
from scipy.optimize import minimize


def solve(p0, a0, p1, a1, length, n=80, guess=None, q_over_ei=0.0):
    """Strip from p0 leaving at heading a0 to p1 arriving at heading a1, both (x, z).

    Returns (points (n+1, 2), headings (n,), max curvature 1/mm, converged).
    """
    ds = length / n
    dx, dz = p1[0] - p0[0], p1[1] - p0[1]
    after = np.arange(n, 0, -1, dtype=float)     # points beyond segment j (z of each depends on theta_j)

    def pts(t):
        return np.vstack([[0.0, 0.0], np.cumsum(np.c_[np.cos(t), np.sin(t)] * ds, axis=0)]) + p0

    def energy(t):
        full = np.r_[a0, t, a1]
        z = np.cumsum(np.sin(t)) * ds
        return np.sum(np.diff(full) ** 2) / (2 * ds) + q_over_ei * ds * np.sum(z)

    def grad(t):
        full = np.r_[a0, t, a1]
        d = np.diff(full)
        return (d[:-1] - d[1:]) / ds + q_over_ei * ds * ds * np.cos(t) * after

    cons = [
        {"type": "eq", "fun": lambda t: np.sum(np.cos(t)) * ds - dx,
         "jac": lambda t: -np.sin(t) * ds},
        {"type": "eq", "fun": lambda t: np.sum(np.sin(t)) * ds - dz,
         "jac": lambda t: np.cos(t) * ds},
    ]
    t0 = np.linspace(a0, a1, n) if guess is None else np.asarray(guess)
    res = minimize(energy, t0, jac=grad, constraints=cons, method="SLSQP",
                   options={"maxiter": 800, "ftol": 1e-12})
    t = res.x
    full = np.r_[a0, t, a1]
    kappa = np.max(np.abs(np.diff(full))) / ds
    p = pts(t)
    closed = math.hypot(p[-1, 0] - p1[0], p[-1, 1] - p1[1]) < 0.05
    return p, t, kappa, bool(res.success and closed)
