"""Centralized RP-03 pass-1 parameters. Ranges stay ranges. Leads are not freezes.

Units: millimetres, grams, seconds. Chassis frame is axle-origin (see frames.py).
"""

from __future__ import annotations

# --- identity ----------------------------------------------------------------
LAYOUT_ID = "RP03_BASE_PASS1"
LAYOUT_REV = "pass-01.0"
WHEEL_FAMILY_DISPLAYED = "C"  # skate Ø84×24 + 608. A and B exist as alternate models.
SKU_FROZEN = False
FRONT_SUPPORT_V1 = "ball"  # displayed assembly. Caster is the required swap assembly.

# --- coordinate / ride -------------------------------------------------------
H_AXLE = 42.0
TRACK = 170.0  # wheel centre-to-centre
WHEEL_Y_L = TRACK / 2.0
WHEEL_Y_R = -TRACK / 2.0
LOADED_RADIUS = 42.0  # assumption; squash U. Distinct from nominal OD/2.
NOMINAL_RIDE_HEIGHT = 0.0  # ground plane at z=0

# --- CON-14 / clearance ------------------------------------------------------
CON14_H = 300.0
CON14_W = 205.0
CON14_D = 180.0
GROUND_CLEARANCE_MIN = 25.0
GROUND_CLEARANCE_MAX = 35.0
SHELL_CLEARANCE = 30.0  # displayed deck underside target, inside the band

# --- wheel families (A/B retained, C displayed) ------------------------------
WHEEL_A_OD, WHEEL_A_W, WHEEL_A_MASS = 83.0, 35.0, 54.0
WHEEL_B_OD, WHEEL_B_W, WHEEL_B_MASS = 80.0, 10.0, 23.0  # mass D for 80×10 incl. tyre
WHEEL_C_OD, WHEEL_C_W, WHEEL_C_MASS = 84.0, 24.0, 90.0
WHEEL_OD = WHEEL_C_OD
WHEEL_WIDTH = WHEEL_C_W
WHEEL_MASS = WHEEL_C_MASS
HUB_BORE = 22.0  # 608 OD
HUB_THICK = 12.0
SHAFT_D = 4.0
SHAFT_LEN = 11.0  # mid of 10–12
SHAFT_FLAT = 8.0
BEARING_ID, BEARING_OD, BEARING_B = 8.0, 22.0, 7.0

# --- motor keep-out (class envelope, not a winding freeze) -------------------
MOTOR_KEEPOUT_D = 28.0
MOTOR_KEEPOUT_L = 90.0  # includes pigtail
MOTOR_GB_D = 25.0
MOTOR_GB_L = 21.0
MOTOR_CAN_D = 30.8
MOTOR_CAN_L = 32.0
MOTOR_ENC_L = 12.0
MOTOR_FACE_M3 = 19.0  # E until article
MOTOR_MASS = 110.0  # with encoder; do not use 85
# Stall conflict — cite both, do not average
MOTOR_STALL_OZ = (900.0, 0.490)  # mA, N·m
MOTOR_STALL_NFP = (3000.0, 0.441)
MOTOR_PIGTAIL_L = 25.0

# --- front support -----------------------------------------------------------
FRONT_CONTACT_X = 110.0  # displayed; adjustable 105–115
FRONT_CONTACT_X_MIN = 105.0
FRONT_CONTACT_X_MAX = 115.0
SHIM_MIN = 0.0
SHIM_MAX = 15.0
BALL_NATIVE_H = 29.0
BALL_HOUSING_D = 34.0
BALL_D = 25.4
BALL_HOLE_SPAN = 12.2  # adjacent C–C
BALL_PCD = 14.0
BALL_MASS = 16.5  # #2691 rollers; #2692 is 18.5
BALL_SHIM = H_AXLE - BALL_NATIVE_H  # 13 mm at loaded radius = 42
CASTER_NATIVE_H = 38.0
CASTER_PLATE = (33.0, 38.0)
CASTER_HOLES = (30.0, 23.0)
CASTER_WHEEL_D = 30.0
CASTER_WHEEL_W = 13.0
CASTER_SHIM = H_AXLE - CASTER_NATIVE_H  # 4 mm
CASTER_TRAIL_MIN = 10.0
CASTER_TRAIL_MAX = 18.0
CASTER_TRAIL_DISPLAY = 14.0  # U, mid of target band, not a measurement
CASTER_MASS = 32.0  # 25 mm variant D; 30 mm listing mass U — labelled estimate

# --- skid (not frozen 14/70) -------------------------------------------------
SKID_REACH_MIN = 60.0
SKID_REACH_MAX = 80.0
SKID_H_MIN = 8.0
SKID_H_MAX = 16.0
SKID_REACH = 72.0  # displayed pose inside the band, not 70 frozen
SKID_HEIGHT = 12.0  # displayed pose inside the band, not 14 frozen
SKID_PAD = (22.0, 22.0, 4.0)

# --- sensing -----------------------------------------------------------------
CLIFF_BODY = (10.2, 5.8, 7.0)
CLIFF_STANDOFF = 4.0  # adjustable 2–8; peak 2.5 is optical, not a freeze
CLIFF_STANDOFF_MIN = 2.0
CLIFF_STANDOFF_MAX = 8.0
CLIFF_F_LEAD = 40.0  # ahead of ball contact
IR_BODY = (30.0, 14.0, 14.0)  # 29.5×13×13.5 plus capacitor/keep-out
IR_OA_FROM_LEFT = 4.5 + 19.7  # detector lens centre from body L (D, Sharp)
IR_OA_SIDE = 7.2  # side-view lens axis (D)
IR_LOOKAHEAD_050 = 179.0
BUMPER_SPAN = 205.0
BUMPER_BAR = (8.0, 205.0, 12.0)
SWITCH_BODY = (20.0, 6.0, 10.0)
IMU_BODY = (25.0, 25.0, 5.0)  # module U

# --- electronics keep-outs ---------------------------------------------------
C3_BOARD = (62.74, 25.40, 12.0)  # official outline D; USB stick-out U
C3_USB_KEEP = 8.0
DRV_INSTALLED = (20.0, 20.0, 12.0)  # PCB 15.2×17.8 plus headers/bend
DRV_MASS = 0.9
BATTERY_BODY = (68.0, 40.0, 22.0)  # dummy; must sit entirely x>0
BATTERY_X = 65.0  # pack CoM band +50…+80
BATTERY_Z = 25.0  # band 18–32
BATTERY_MASS = 280.0  # band 150–500
BATTERY_X_MIN = 50.0
BATTERY_X_MAX = 80.0

# --- ballast bay -------------------------------------------------------------
BAY_X_MIN = 20.0
BAY_X_MAX = 95.0
BAY_Z_MIN = 12.0
BAY_Z_MAX = 40.0
BALLAST_X = 70.0
BALLAST_Z = 22.0
BALLAST_BODY = (40.0, 36.0, 16.0)
BALLAST_MASS = 350.0

# --- head lump (Layout 03, not re-authored) ----------------------------------
HEAD_MASS_NOM = 509.04
HEAD_MASS_LO = 499.04
HEAD_MASS_HI = 524.04
HEAD_LOCAL_COM = (-39.55188359184538, 0.7458558252366899, 40.295971393290785)
HEAD_ORIGIN_IN_CHASSIS = (37.9645316623177, 0.0, 200.0)
F_NECK = (0.0, 0.0, 140.0)
PITCH_LEVER = 52.0  # RP-03 lumped E, not Layout 03 CAD arm
HEAD_BBOX = (115.0, 150.0, 164.0)  # includes 60 mm neck
BODY_H = 140.0

# --- frame / print -----------------------------------------------------------
RAIL_T = 8.0
DECK_Z = 32.0
PLA_DENSITY = 0.00124  # g/mm^3
PRINT_MASS_FRAME = 95.0
PRINT_MASS_CLAMP = 18.0
PRINT_MASS_HUB = 12.0
PRINT_MASS_MOUNT = 22.0
PRINT_MASS_ADP = 8.0
PRINT_MASS_SKID = 16.0
PRINT_MASS_BAY = 28.0
PRINT_MASS_BUMPER = 14.0
PRINT_MASS_CARRIER = 4.0

# --- motion (paper, not a gate) ----------------------------------------------
V_FOLLOW = 0.50
A_PEAK = (0.80, 1.00)
G = 9810.0  # mm/s^2 for a_tip in mm then convert; use 9.81 m/s^2 in mass.py
DRIVE_MASS_MIN = 200.0
DRIVE_MASS_MAX = 600.0
