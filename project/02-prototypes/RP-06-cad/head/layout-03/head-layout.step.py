"""RP-01 Layout 03, mm, +X face, +Y left, +Z up. See brief.md."""
from layout_model import assembly
import inspection_scene, details, mass_layout, harness, optics, write_dimensions

def gen_step():
    return {'shape': assembly(), 'params': 'head-layout.params.js'}
