from cadgen import step
from lib.parts import swivel_caster as _swivel_caster


@step(out="../STEP/swivel_caster.step")
def swivel_caster():
    return _swivel_caster()


if __name__ == "__main__":
    swivel_caster()
