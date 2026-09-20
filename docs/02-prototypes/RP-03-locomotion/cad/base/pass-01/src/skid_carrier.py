from cadgen import step
from lib.parts import skid_carrier as _skid_carrier


@step(out="../STEP/skid_carrier.step")
def skid_carrier():
    return _skid_carrier()


if __name__ == "__main__":
    skid_carrier()
