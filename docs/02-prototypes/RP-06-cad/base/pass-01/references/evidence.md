# Purchased-part evidence index — CAD pass 1

Leads, not freezes. Capture class W/D/E/U. Official STEPs from step.parts were hits for GP2Y, TCRT5000, and 608ZZ; this pass uses **class envelopes** for placement control (optical/contact datums) and keeps vendor URLs here. Do not treat any row as the purchased article.

| Item | Identity | Capture | Official geometry used | step.parts | Notes |
|---|---|---|---|---|---|
| R-MTR | JGA25-370 / GM25-370 class | D / U face | Ø25 GB, 4 mm D-shaft 10–12, keep-out Ø28×90 | MISS | Stall 900 mA vs ≤3 A, not averaged |
| R-WHL | Family C Ø84×24 PU 608 | D OD/mass | 84×24, 90 g | MISS | A/B retained uncomposed |
| R-HUB | 608ZZ ×2 per wheel | D | 8×22×7, 12.1 g | HIT `bearing_608zz` | Printed carrier |
| R-BALL | Pololu 2691 class | D | H 29, Ø34, 3-hole span 12.2, 16.5 g | MISS | Not Robu 15.9 mm steel |
| R-CAS | 33×38 Ø30 plate class | D plate; U trail | H 38, holes 30×23 | MISS | Trail displayed 14 U |
| R-DRV | Pololu 4035 class | D | 15.2×17.8, installed 20×20×12 | MISS (Pololu STEP exists) | Body, not tub |
| R-C3 | ESP32-S3-DevKitC-1 | D outline | 62.74×25.40; USB U | MISS | Not ~69 |
| R-IR | GP2Y0A41SK0F | D | 29.5×13×13.5; OA 4.5+19.7 / 7.2 | HIT | Envelope + OA child |
| R-CLF | TCRT5000 | D | 10.2×5.8×7, peak 2.5 | HIT | Bare component |
| R-IMU | ICM-42688-P breakout | U module | Reserve 25×25×5 | MISS | Silicon is not the module |

Sources: Pololu 2691/4035 pages; Sharp GP2Y datasheet; Vishay 83760; Espressif DevKitC-1 DXF; SKF 608-2Z; NFP-GM25-370-EN / Oz Aslong 176 RPM. Dated 2026-09-19.
