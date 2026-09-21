from cadgen import step
from lib.parts import adapter_ball as _adapter_ball


@step(out="../STEP/adapter_ball.step")
def adapter_ball():
    return _adapter_ball()


if __name__ == "__main__":
    adapter_ball()
