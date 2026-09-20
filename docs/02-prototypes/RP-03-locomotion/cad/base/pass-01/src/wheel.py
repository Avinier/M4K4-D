from cadgen import step
from lib.parts import wheel_family_c


@step(out="../STEP/wheel.step")
def wheel():
    return wheel_family_c()


if __name__ == "__main__":
    wheel()
