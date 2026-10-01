"""Build body v1 using CADgen's generated assembly package."""

from cadgen import step
from body_v1_model import build_body_assembly


@step(out="body-v1.step")
def body_v1():
    return build_body_assembly()


if __name__ == "__main__":
    body_v1()
