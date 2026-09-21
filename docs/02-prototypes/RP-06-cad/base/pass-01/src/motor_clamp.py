from cadgen import step
from lib.parts import motor_clamp as _motor_clamp


@step(out="../STEP/motor_clamp.step")
def motor_clamp():
    return _motor_clamp()


if __name__ == "__main__":
    motor_clamp()
