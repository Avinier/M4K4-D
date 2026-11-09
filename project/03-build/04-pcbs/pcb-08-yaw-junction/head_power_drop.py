"""Reproduce PCB-08/14 head FFC drop screen (estimate, not cable test).

Four FH34SRJ interfaces are counted in series. The maker's 0.1-ohm maximum
includes 8 mm of FFC bulk at each interface; adding it to the whole cable
length is a deliberately conservative small double count.
"""

COPPER_OHM_MM2_PER_M = 0.01724
CONDUCTOR_WIDTH_MM = 0.3
TOTAL_CABLE_M = 0.3  # 200 mm cassette + assumed 100 mm head lead
CONTACTS_IN_SERIES = 4
CONTACT_OHM_MAX = 0.1
HEAD_CURRENT_A = 2.8
HEAD_TERMINAL_TARGET_V = 5.23
SELECTED_SETPOINT_V = 6.3
PROTECTED_HEAD_CURRENT_A = 2.4
# Conservative pre-pour PCB-08 trunk estimate at 27 um copper. Filled
# copper lowers it, but the J5 throat prevents claiming an 8 mm path.
PCB08_DROP_UPPER_EST_V = 0.10


def loop_ohm(thickness_mm: float, positive: int, returns: int) -> float:
    one_path = (
        COPPER_OHM_MM2_PER_M * TOTAL_CABLE_M / (CONDUCTOR_WIDTH_MM * thickness_mm)
        + CONTACTS_IN_SERIES * CONTACT_OHM_MAX
    )
    return one_path / positive + one_path / returns


def main() -> None:
    print("copper_mm  positive  returns  loop_ohm  drop_2.8V  min_setpoint_V")
    for thickness in (0.035, 0.027):
        for count in (7, 13):
            resistance = loop_ohm(thickness, count, count)
            drop = HEAD_CURRENT_A * resistance
            print(
                f"{thickness:9.3f}  {count:8d}  {count:7d}  "
                f"{resistance:8.3f}  {drop:9.3f}  {HEAD_TERMINAL_TARGET_V + drop:14.3f}"
            )
    thin = loop_ohm(0.027, 7, 7)
    terminal = SELECTED_SETPOINT_V - PROTECTED_HEAD_CURRENT_A * thin - PCB08_DROP_UPPER_EST_V
    print(f"D-100 amended: {SELECTED_SETPOINT_V:.1f} V, {PROTECTED_HEAD_CURRENT_A:.1f} A, "
          f"thin FFC and pre-pour PCB upper estimate -> {terminal:.3f} V at head "
          f"(target {HEAD_TERMINAL_TARGET_V:.2f} V; excludes regulator droop and other leads)")


if __name__ == "__main__":
    main()
