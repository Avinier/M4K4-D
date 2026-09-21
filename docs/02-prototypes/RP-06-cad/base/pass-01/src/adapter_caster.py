from cadgen import step
from lib.parts import adapter_caster as _adapter_caster


@step(out="../STEP/adapter_caster.step")
def adapter_caster():
    return _adapter_caster()


if __name__ == "__main__":
    adapter_caster()
