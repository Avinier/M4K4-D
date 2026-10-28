"""Same authored assembly, exterior removed; translucent volumes are reserves."""
from layout_model import assembly

def gen_step():
    return assembly(internals=True)
