"""RP-03 pass 1 required swap: swivel caster on the same mount and contact x."""

from cadgen import step

from lib.assemble import build_base


@step(out="../STEP/assembly_caster.step")
def assembly_caster():
    return build_base("caster")


if __name__ == "__main__":
    assembly_caster()
