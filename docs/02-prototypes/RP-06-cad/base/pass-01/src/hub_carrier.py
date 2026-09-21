from cadgen import step
from lib.parts import hub_carrier as _hub_carrier


@step(out="../STEP/hub_carrier.step")
def hub_carrier():
    return _hub_carrier()


if __name__ == "__main__":
    hub_carrier()
