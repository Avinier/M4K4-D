"""RP-03 pass 1 root: ball-transfer V1 installed. Not a SKU freeze."""

from cadgen import step

from lib.assemble import build_base


@step(out="../STEP/assembly.step")
def assembly():
    return build_base("ball")


if __name__ == "__main__":
    assembly()
