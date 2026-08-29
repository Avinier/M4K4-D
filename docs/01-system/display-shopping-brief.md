# Makad IPS Face-Display Shopping Brief

| Field | Value |
|---|---|
| Status | **Procurement brief for locked display SKU** |
| Version | 0.3 |
| Last reviewed | 2026-08-29 |
| Governs | Ecommerce searches, Lamington Road calls/visits and supplier checks for the moving-head face display |

## Buy this exact module

> **Waveshare ESP32-S3-LCD-4.3, no-touch version, SKU 30493** — not the capacitive-touch version and not a 480×272 SPI display.

The module is selected and locked for Makad V1. The remaining shopping task is to verify the exact variant, obtain one genuine unit and document its price, revision and delivery—not to continue comparing screens.

## Exact-SKU verification criteria

| Criterion | Accept | Reject / question |
|---|---|---|
| Panel | **IPS**, full colour, 4.3-inch class | TN when IPS is claimed only in the title; monochrome OLED; character LCD |
| Resolution | **800×480 native** | 480×272 unless deliberately accepted as a visual downgrade; interpolated resolution |
| Active area | About **93–101 W × 52–57 H mm** in landscape | Seller gives only diagonal and no drawing |
| Module body | Prefer **≤107 W × 68 H mm**; up to ~122×74 mm only for a proven smart-display fallback | Dimensions exclude PCB, connector or FPC tail |
| Interface | Best: integrated **ESP32-S3 + LVGL**. Next: 15-pin Pi DSI. UART smart HMI is acceptable. | Raw 40/45-pin RGB without a named controller plan; HDMI for the final moving head |
| Touch | **No touch preferred** | Do not pay weight/cost for touch unless it is the only stocked exact module |
| Brightness | **≥300 nit**, with ≥400 preferred | No brightness figure; marketing terms such as “high brightness” only |
| Frame rate | 50–60 fps target or a demonstrated fluid eye animation | “Fast refresh” without timing/example evidence |
| Colour | 65K is adequate for stylized eyes; 262K/16.7M welcome | Do not trade controller reliability for colour depth the artwork does not need |
| Power | Input voltage and typical/worst consumption stated | “5 V” with no current figure or inaccessible power connector |
| Mass | Actual module mass or permission to weigh sample | Shipping weight presented as installed mass |
| Evidence | Exact manufacturer SKU, invoice, live stock, datasheet/wiki and return/DOA policy | Generic title/photo, substituted revision, marketplace seller cannot identify controller |

## Procurement source and contingency references

| Role | Exact item | Seller evidence checked 2026-08-29 | Action |
|---:|---|---|---|
| **Selected source** | Waveshare ESP32-S3-LCD-4.3 **no touch**, SKU 30493 | [Hubtronics](https://hubtronics.in/development-boards/microcontroller-development-boards/esp32-s3-lcd-4.3): ₹3,065 incl. GST, two shown in stock | Confirm SKU 30493, no-touch, unopened stock and shipping time; obtain one unit after confirmation |
| Contingency only | Waveshare 43H-800480-IPS **no touch**, SKU 24159 | [Zbotic product family](https://zbotic.in/product/waveshare-4-3inch-dsi-display/) around ₹3.3k; exact selected variant/live quantity ambiguous | Do not purchase unless selection change control is triggered by a documented hard failure |
| Contingency only | DWIN DMG80480T043_09WN **no touch** | [RoboticsDNA](https://roboticsdna.in/product/4-3inch-800x480-ips-industrial-hmi-uart-lcd-display-without-touch-2/): ₹4,576.01 incl. GST, shown in stock | Do not purchase unless selection change control is triggered by a documented hard failure |

Stock and price are snapshots, not procurement guarantees. Recheck immediately before payment.

## Questions for an ecommerce seller or Lamington Road shop

1. What is the exact manufacturer and complete part number? Please send a photo of the label.
2. Is it IPS, and is 800×480 the native resolution?
3. Is this the no-touch version? If touch is fitted, what is the total module mass?
4. What are the active-area and complete PCB/module dimensions in landscape?
5. Which controller is included: ESP32-S3, DSI adapter, HDMI board, UART HMI or none?
6. Can it play locally stored animations without streaming HDMI video?
7. What input voltage and current does the complete module require at full brightness?
8. What is the module's actual net weight, excluding box and cable?
9. How many identical units are physically in stock, and can the same revision be supplied later?
10. Is there a datasheet/wiki, pinout, example code and dead-on-arrival replacement policy?

## Red flags

- The listing switches among IPS, TFT, OLED and AMOLED as if they are synonyms.
- “4.3-inch” is the only dimensional information.
- The photo shows a Raspberry Pi DSI connector but the description says generic HDMI or SPI.
- The price changes after selecting the required no-touch/800×480 variant.
- The panel is raw RGB and the seller cannot name a compatible controller board.
- The quoted weight is visibly the packed shipment weight.
- The seller will not confirm the exact suffix or sends a different touch version “as equivalent.”

## Reusable procurement-verification prompt for other agents

```text
Find an India-orderable source for this exact locked display module:

- Waveshare ESP32-S3-LCD-4.3
- no-touch version
- official SKU 30493

Do not recommend alternative screens. Reject the capacitive-touch variant, 480×272 products, raw panels, HDMI modules, and listings that cannot prove the exact manufacturer SKU.

For every source report: seller URL, exact SKU/variant evidence, live-stock timestamp, GST-inclusive price, Mumbai delivery estimate, return/DOA policy, and whether the seller can provide a label photo. Also record any manufacturer-declared revision, net mass, power documentation and official documentation links. Separate verified facts from inference.
```

## Purchase gate

Do not buy several speculative panels. Confirm the exact SKU with the seller, obtain **one** selected-module sample, and run the acceptance test in `display-candidate-study.md`. A second unit is justified only after that sample passes geometry, mass, animation, optical, power and availability checks.

## Change log

| Date | Version | Change |
|---|---|---|
| 2026-08-29 | 0.1 | Created the earlier AMOLED sourcing and RFQ brief. |
| 2026-08-29 | 0.2 | Replaced the AMOLED requirement with an India-focused IPS brief, exact first-purchase candidate, seller questions and reusable search prompt. |
| 2026-08-29 | 0.3 | Converted the brief from comparative sourcing to exact-SKU procurement after the project builder locked Waveshare no-touch SKU 30493. |
