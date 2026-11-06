# Final v1 purchased models

Vendor files for the D-093 bought modules ([D-095](../../../../decisions.md#d-095)), downloaded from Pololu's product resource pages on 2026-11-07. `makad-v1.step.py` loads the STEPs through `VENDOR_STEPS`; each file has the board underside on z 0, and the mounting holes in `VENDOR_HOLES` were read from the STEPs' Ø2.18 bores and match the dimension drawings.

| File | Part | Source |
|---|---|---|
| `5v-step-up-step-down-voltage-regulator-s13v30f5.step`, `-dimensions.pdf`, `reg26a-drill.dxf` | Pololu #4082 S13V30F5 (M4, M5): 22.9 × 22.9 mm, two Ø2.18 holes 18.5 apart on the pin edge | [pololu.com/product/4082/resources](https://www.pololu.com/product/4082/resources) (0J1808, 0J1807, 0J1809) |
| `s18v20x-step-up-step-down-voltage-regulator.step`, `-dimensions.pdf`, `reg14a01-drill.dxf` | Pololu #2572 S18V20ALV (M2, M3): 43.2 × 21.0 mm, four Ø2.18 holes 38.9 × 16.6 | [pololu.com/product/2572/resources](https://www.pololu.com/product/2572/resources) (0J1416, 0J1417, 0J905) |
| `big-pushbutton-power-switch-with-reverse-voltage-protection.step`, `-dimension-diagram.pdf`, `psw03b-drill.dxf` | Pololu #2813 Big Pushbutton Power Switch HP (M1): 20.3 × 25.4 × 4 mm, no mounting holes (the four Ø2.18 holes are the power terminals) | [pololu.com/product/2813/resources](https://www.pololu.com/product/2813/resources) (0J1405, 0J1102, 0J1099) |

SHA-256:

```
6daa3aed7237d86456a1540f35f7e13183961d6601f1a65cde67840c8a0c02dc 5v-step-up-step-down-voltage-regulator-s13v30f5.step
89dceed662b33acde2cf32cef641e73ba3a7763c03d66824b471639f7bcb5de8 big-pushbutton-power-switch-with-reverse-voltage-protection.step
9c23c2bbb85e01bfae0806b770bb04707262cbbd6bab0d21058c2ddee3d59212 s18v20x-step-up-step-down-voltage-regulator.step
```
