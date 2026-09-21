from cadgen import step
from lib.parts import axle_frame as _axle_frame


@step(out="../STEP/axle_frame.step")
def axle_frame():
    return _axle_frame()


if __name__ == "__main__":
    axle_frame()
