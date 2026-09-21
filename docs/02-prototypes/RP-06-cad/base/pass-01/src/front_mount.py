from cadgen import step
from lib.parts import front_mount as _front_mount


@step(out="../STEP/front_mount.step")
def front_mount():
    return _front_mount()


if __name__ == "__main__":
    front_mount()
