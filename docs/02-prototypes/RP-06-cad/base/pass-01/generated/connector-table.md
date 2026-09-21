# Connector table (keep-out class, family is RP-02)

| Source | Destination | Family | Mate dir | Disconnect order |
|---|---|---|---|---|
| MOTOR_L pigtail | DRIVER_L | PH2.0 6-pin class | inboard then up | 3 after arm-off |
| MOTOR_R pigtail | DRIVER_R | PH2.0 6-pin class | inboard then up | 4 |
| DRIVER_L/R logic | C3 | Dupont forbidden; keyed | body cavity | 2 |
| CLIFF_* | C3 GPIO | native GPIO, no expander | harness_sense | 5 |
| IR_FRONT | C3 ADC | analog + divider | +x at contact | 6 |
| IMU_BASE | C3 SPI | SPI+INT1 | rigid base | 7 |
| Neck trunk | body demate | keyed, both-face strain relief | +z at F_NECK | 1 last-on first-off |
