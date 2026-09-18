/* CA-14 C3 board-role header — generated from RP-03 pin map v0.1
 * Source: docs/02-prototypes/RP-03-locomotion/base-control-architecture.md §3
 * Registration: RP03-P4-REG-02 / RP02-P4-REG-02 (2026-09-18)
 *
 * This is the C3 half of the CA-14 config source. It is not a carrier freeze,
 * not a SKU freeze, and not a byte-layout freeze. Soft BASE_LIMITS_SET values
 * may only tighten the compiled maxima below. A hash mismatch blocks arm.
 *
 * Carrier PCB still waits on a frozen map. N8R8 is not a silent substitute.
 */
#ifndef MAKAD_C3_BOARD_ROLE_H
#define MAKAD_C3_BOARD_ROLE_H

#define MAKAD_C3_BOARD_ROLE_REV        1u
#define MAKAD_C3_PINMAP_VERSION        0x0001u
#define MAKAD_C3_BOARD_ID              "ESP32-S3-DevKitC-1-N8"

/* Config identity. Replace the hash at freeze; a mismatch blocks BASE_ENABLE. */
#define MAKAD_C3_CONFIG_SOURCE         "rp03-pinmap-v0.1"
#define MAKAD_C3_CONFIG_HASH_PLACEHOLDER  0x00000000u

/* --- compiled hard maxima (conservative defaults until measured CoM) --- */
/* physics.md RANGE, not the 1.98 m/s² placement target. BC-09. */
#define MAKAD_C3_A_MAX_MM_S2           800     /* 0.80 m/s² */
#define MAKAD_C3_V_FOLLOW_MAX_MM_S     500     /* CON-19; cannot be weakened */
#define MAKAD_C3_V_CLAMP_MM_S          700     /* BD-06 cannot-exceed test limit */
#define MAKAD_C3_W_MAX_MRAD_S          3840    /* 220 °/s = 3.840 rad/s */
#define MAKAD_C3_V_CAL_MM_S            60      /* BM-11 / CC-12C clamp */
#define MAKAD_C3_CMD_TTL_CRUISE_MS     200     /* candidate, unregistered */
#define MAKAD_C3_CMD_TTL_ONESHOT_EXTRA_MS 250  /* plus duration_ms; unregistered */
#define MAKAD_C3_HEARTBEAT_TIMEOUT_MS  150     /* candidate, unregistered */
#define MAKAD_C3_QUEUE_DEPTH           2       /* candidate, unregistered */
#define MAKAD_C3_CC12C_ARM_TTL_MS      5000    /* candidate, unregistered */
#define MAKAD_C3_GEARBOX_TSTOP_C       85      /* stop-on-temperature candidate */

/* --- pin map v0.1: ESP32-S3-DevKitC-1-N8 --- */
/* Strapping GPIO0/45/46: unassigned, no safety OUTPUTS.
 * GPIO3: ESTOP_N input-only exception. GPIO19/20 USB. GPIO43/44 USB-UART.
 * GPIO48: WDI (RGB LED released). Spare safe GPIO: 2, 10, 38 (≥2 required). */

#define MAKAD_C3_GPIO_ENC_L_A          4
#define MAKAD_C3_GPIO_ENC_L_B          5
#define MAKAD_C3_GPIO_ENC_R_A          6
#define MAKAD_C3_GPIO_ENC_R_B          7
#define MAKAD_C3_GPIO_PWM_L            11
#define MAKAD_C3_GPIO_PWM_R            12
#define MAKAD_C3_GPIO_DIR_L            13
#define MAKAD_C3_GPIO_DIR_R            14
#define MAKAD_C3_GPIO_nSLEEP           21  /* fail-safe pull-down to inhibit */
#define MAKAD_C3_GPIO_nFAULT           9
#define MAKAD_C3_GPIO_CLIFF_FL         15
#define MAKAD_C3_GPIO_CLIFF_FR         16
#define MAKAD_C3_GPIO_CLIFF_REAR       8
#define MAKAD_C3_GPIO_OBST_IR          1   /* ADC1; not ToF */
#define MAKAD_C3_GPIO_BUMP             47
#define MAKAD_C3_GPIO_ESTOP_N          3   /* input only; strapping exception */
#define MAKAD_C3_GPIO_ENERGY_OK        39
#define MAKAD_C3_GPIO_MOTOR_PRESENT    40
#define MAKAD_C3_GPIO_IMU_MOSI         35
#define MAKAD_C3_GPIO_IMU_MISO         36
#define MAKAD_C3_GPIO_IMU_SCLK         37
#define MAKAD_C3_GPIO_IMU_CS           41
#define MAKAD_C3_GPIO_IMU_INT          42
#define MAKAD_C3_GPIO_UART1_TX         17
#define MAKAD_C3_GPIO_UART1_RX         18
#define MAKAD_C3_GPIO_WDI              48

#define MAKAD_C3_GPIO_SPARE_0          2
#define MAKAD_C3_GPIO_SPARE_1          10
#define MAKAD_C3_GPIO_SPARE_2          38
#define MAKAD_C3_SPARE_SAFE_COUNT      3

/* ISENSE / IPROPI is not on the MCU in v0.1. A later landing consumes a named
 * spare through change control and re-proves SPARE_SAFE_COUNT >= 2. */

#define MAKAD_C3_GPIO_STRAPPING_UNUSED_0   0
#define MAKAD_C3_GPIO_STRAPPING_UNUSED_45  45
#define MAKAD_C3_GPIO_STRAPPING_UNUSED_46  46

#if (MAKAD_C3_SPARE_SAFE_COUNT) < 2
#error "CA-14 / RP03-P08: C3 pin map must retain >= 2 unassigned safe GPIO"
#endif

#endif /* MAKAD_C3_BOARD_ROLE_H */
