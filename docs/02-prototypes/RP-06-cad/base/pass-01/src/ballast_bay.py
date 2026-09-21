from cadgen import step
from lib.parts import ballast_bay as _ballast_bay


@step(out="../STEP/ballast_bay.step")
def ballast_bay():
    return _ballast_bay()


if __name__ == "__main__":
    ballast_bay()
