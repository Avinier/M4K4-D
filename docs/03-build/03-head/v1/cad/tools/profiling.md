# Head check profiling (D-048 baseline)

Runtime: Python 3.13, `cadgen==0.4.28`, 10 logical cores and 24 GiB RAM.
These are measurements from this checkout, not D-049 sign-off timings.

| Run | cProfile total | Main finding |
|---|---:|---|
| `check_fasteners.py` (cold cache) | 255.55 s | 2,592 relief intersection results during the first build; 37,644 optimal bounding-box evaluations across build and audit. |
| `check_revision.py --neutral` (warm cache) | 22.92 s | 8,648 optimal bounding-box evaluations, taking 9.97 s inside OCC; import overhead is also visible. |
| `check_fasteners.py` (warm cache, bounds memoized) | 250.72 s wall | Screw station containment tests dominate after the build is removed. Output still matches the golden. |
| `check_layout.py --neutral` (warm cache) | 10.46 s | Import overhead dominates; OCC evaluated 310 bounding boxes. |
| `motion_envelope.py --write` (warm mesh cache) | 10.20 s | Rotation/pose math is now the main computation; imports take about 2.7 s. |

The cache writes 100 BReps for 3.7 MiB total. Reading all 100 took 0.16 s
inside an already started interpreter; a fresh interpreter plus cache read took
6.82 s wall time. The remaining startup time is Python and CAD library import.
With a disjoint-box screen before relief intersections, one cold full-parts
build took 113.84 s wall time while another CAD check was active.
The spawn-based relief sampler completed a direct cold build in about 87 s.
Its mass output matched the golden, and all 100 cached parts matched the
earlier full build in volume (within 0.01 mm³) and solid count.
The full 56-pose revision run with 10 spawn workers took 156.81 s wall time.
The full 56-pose clearance audit took 174.09 s serial while a direct mass
build was active, then 77.17 s with 10 spawn workers. The two JSON files were
byte identical.
Envelope regeneration took 164.57 s with the original full mesh clouds.
After caching all 100 part tessellations and retaining only convex-hull
vertices for extreme-Z queries, the first run took 32.74 s and matched the
envelope golden exactly. A warm rerun took 8.43 s.

The first `check_fasteners.py` run passed and its output matched the checked in
golden exactly. `check_revision.py --neutral` passed; the JSON was byte
identical after memoizing bounds. The full parallel revision result matched
the golden. The D-049 mounts profile is pending its source commit.

The first `run_checks.py --fast` pass took 432.99 s for the available head
checks. Its revision, clearance, integration, envelope, mass and fastener
checks passed. The mount, busy-minute and FEA checks were unavailable in this
D-048 checkout. Body layout passed after copying the ignored purchased STEP
references into this worktree. Yaw stage passed in 924.92 s; it is currently
the dominant full-run cost and has not been accelerated by the head cache.

Profiles were written outside the repository to `/private/tmp/makad-cache-build.prof`
and `/private/tmp/makad-revision-neutral.prof`.
