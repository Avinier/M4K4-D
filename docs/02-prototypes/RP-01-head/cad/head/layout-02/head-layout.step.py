"""RP-01 Layout 02, mm, +X face, +Y left, +Z up. See brief.md."""
from layout_model import assembly

def gen_step():
    return {'shape': assembly(), 'params': 'head-layout.params.js'}
