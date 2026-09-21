from cadgen import step
from lib.parts import ball_transfer as _ball_transfer


@step(out="../STEP/ball_transfer.step")
def ball_transfer():
    return _ball_transfer()


if __name__ == "__main__":
    ball_transfer()
