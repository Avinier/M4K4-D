from cadgen import step
from lib.parts import head_lump as _head_lump


@step(out="../STEP/head_lump.step")
def head_lump():
    return _head_lump()


if __name__ == "__main__":
    head_lump()
