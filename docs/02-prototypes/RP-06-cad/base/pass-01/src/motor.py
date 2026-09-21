from cadgen import step
from lib.parts import motor_keepout


@step(out="../STEP/motor.step")
def motor():
    return motor_keepout()


if __name__ == "__main__":
    motor()
