"""Review assembly for the provisional original-height Feetech yaw package."""
from pathlib import Path
from build123d import Axis, Compound, Location, import_step
import body_v1_model as b
from feetech_yaw_cradle import parts as cradle_parts

HERE=Path(__file__).parent


def gen_step():
    servo=import_step(HERE/'purchased/waveshare_feetech_st3215_hs_servo.step')
    servo=servo.rotate(Axis.X,-90)
    servo=servo.translate((b.BODY_AXIS_X+b.YAW_PINION_CENTER[0],
        b.YAW_PINION_CENTER[1],b.YAW_SERVO_TOP_Z-servo.bounding_box().max.Z))
    servo.label='ST3215_HS_PURCHASED_STEP'
    mount=cradle_parts()
    pi=b.raspberry_pi5().moved(Location((0,-6,0)))
    pi.label='PI5_SHIFT_MINUS_Y_6MM'
    tray=b.compute_tray_print(pi_y_shift=-6)
    tray.label='COMPUTE_TRAY_SHIFTED_PI_BOSSES'
    cooler=b._purchased_step('Heatsink+fan RPi-5.STEP','PI5_ACTIVE_COOLER_STEP',[(Axis.X,90.0)])
    posts=sorted((s for s in cooler.solids() if 100<s.volume<140),key=lambda s:s.bounding_box().center().X)
    post_a=posts[0].bounding_box().center()
    plate_z0=max(cooler.solids(),key=lambda s:s.volume).bounding_box().min.Z
    cooler=cooler.moved(Location((b.PI_COOLER_HOLE_A[0]-post_a.X,
        b.PI_COOLER_HOLE_A[1]-6-post_a.Y,b.PI_SOC_TOP_Z-plate_z0)))
    cooler.label='ACTIVE_COOLER_SHIFT_MINUS_Y_6MM'
    pcb=b._c0_link_adapter(main_x_shift=6).moved(Location((0,-6,0)))
    pcb.label='PCB09_SHIFT_MINUS_Y_6MM_MAIN_PLUS_X_6MM'
    housing=b._yaw_housing();housing.label='YAW_CARTRIDGE_HOUSING_CURRENT'
    cassette=b._yaw_cassette_stator();cassette.label='YAW_CASSETTE_STATOR_CURRENT'
    return Compound(label='FEETECH_YAW_CANDIDATE_NOT_RELEASED',children=[
        servo,mount['cradle'],mount['strap'],tray,pi,cooler,pcb,housing,cassette])
