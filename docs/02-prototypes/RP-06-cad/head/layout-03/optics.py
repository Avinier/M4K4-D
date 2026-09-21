"""Conservative 102-degree horizontal field, rectangular sensor corner rays.

Pupil X=-8 is an explicitly assumed worst rearward position (lens front X=-2).
Vertical tangent derived from 16:9 image aspect, not independently certified FOV.
3 mm entrance half-size guards pupil uncertainty. All values are layout inputs.
"""
import math
from build123d import Plane,Polygon,loft,Location
PUPIL_X=-8.
HALF_H=math.tan(math.radians(51))
HALF_V=HALF_H*9/16
PUPIL_HALF=3.

def cone(z,xend=28,margin=0):
    sections=[]
    for x in [PUPIL_X,xend]:
        w=PUPIL_HALF+(x-PUPIL_X)*HALF_H+margin
        h=PUPIL_HALF+(x-PUPIL_X)*HALF_V+margin
        sections.append((Plane.YZ*Polygon((-w,z-h),(w,z-h),(w,z+h),(-w,z+h),align=None)).moved(Location((x,0,0))))
    return loft(sections,ruled=True)
