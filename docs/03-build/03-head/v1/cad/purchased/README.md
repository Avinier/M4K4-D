# Head v1 purchased CAD references

These files are copied byte for byte from
`docs/02-prototypes/RP-06-cad/head/layout-01/parts/` so head v1 can build
from its own CAD folder. The RP-06 [parts register](../../../../../02-prototypes/RP-06-cad/head/layout-01/parts/README.md)
records the original vendors, files, and modeling limits.

- `camera-module-3-wide.step`: Raspberry Pi Camera Module 3 Wide.
- `waveshare_esp32_s3_touch_lcd_4_3.stp`: conservative touch-board outline
  used for the selected non-touch 4.3 inch display.
- `waveshare_esp32_s3_zero_v2.step`: C2 board envelope.
- `xc330.stp`: ROBOTIS XC330 servo geometry.
- `sts3045m_reference.step.py` / `.step`: locally authored STS3045M
  packaging reference from the [Evelta Feetech datasheet drawing, p. 6](https://evelta.com/content/datasheets/501-STS3045M.pdf)
  and the three supplied product photographs. The body envelope (36 × 15 ×
  29.2 mm), total ear span (48.8 mm), four open Ø4.2 slots, 7.5 mm row pitch,
  output offset (6 mm), and Ø5.9/25T shaft are drawing-based. Boss profile,
  cable stub, tab roots, screw thread, and spline teeth are simplified or
  estimated. This is **not** an exact manufacturer STEP or a production
  mounting authority; confirm slot centres and horn engagement on the sample.
  Its local origin is the output axis at the case bottom, +Z along the shaft.

The original purchased files are 1:1 packaging references; the new STS3045M
file is a drawing-based envelope. Fits and production variants still need
physical confirmation. Keep `xc330.stp` for the unrefitted legacy head assembly.
