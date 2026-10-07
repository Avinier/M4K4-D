# Head v1

The head v1 CAD is in [cad/](cad/README.md). It is based on the latest RP-06
Layout 04, with its source and purchased geometry moved into the build tree.
The head now shares body v1's yaw datum and has modeled M3 disc fixings to
its three hub inserts. [The integrated export](cad/head-v1-integrated.step.py)
builds the head on the latest body v1 and chassis v1 source; the standalone
[head export](cad/head-v1.step.py) supports head-only review.

The integrated CAD is a geometry and packaging handoff. The purchased fits,
print process and tolerances, cable flex, and measured balance remain physical
build checks before fabrication release.
