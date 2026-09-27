# RP-06 — Sourced layout CAD

| Field | Value |
|---|---|
| Status | **This folder owns the working CAD.** Phase A packaging is the article. Physical validation is 0%. No gate registered, no mock-up built, no scored run |
| Governing plan | [`risk-prototype-plan.md`](../../01-system/risk-prototype-plan.md) v1.15 §RP-06 |
| Purpose | Working whole-robot packaging for an obtainable, serviceable layout |
| Active models | Head [Layout 04](head/layout-04/README.md). Whole body [Layout 02](body-chassis/layout-02/README.md) |
| Closure instrument | [`TODO.md`](TODO.md); detail in [`checklist.md`](checklist.md) |

RP-01 is an object. RP-02 is states and interfaces. RP-03 is a vehicle plus local safety. **RP-06 is the whole-robot packaging prototype**, and therefore the home of the CAD.

RP-01 and RP-03 keep mechanism, physics, gates and rigs; they link here for geometry.

## Start here

| Document | What it owns |
|---|---|
| [TODO](TODO.md) | Builder remaining-work punch list |
| [Closure checklist](checklist.md) | Remaining G01–G06 work; CAD-done vs physical-open |
| [Head Layout 04](head/layout-04/README.md) | Active 1:1 head. Viewer, verification, mass tree |
| [Body/chassis Layout 02](body-chassis/layout-02/README.md) | Active whole-robot assembly. Live-imports Layout 04 |
| [Head decisions](head/decisions.md) | Head CAD decisions and revisions |
| [Body/chassis CAD-context decisions](decisions.md) | `RP03-CAD-01…12` (CAD-first, not RP-03 safety approval) |
| [Peripheral selection](peripheral-selection.md) | Audio path, mics, speaker/amp, status LED and base IMU working selections (2026-09-26) with evidence |
| [Prototype open items](../openitems.md) | Folder-wide remaining-open index |

## CAD map

```text
RP-06-cad/
├── head/                  Layout 04 active; 03, 02 and 01 preserved
│   ├── layout-04/         1:1 packaging, service, optics, harness overlays
│   ├── layout-02/         preserved previous head
│   ├── layout-01/         first study + purchased catalog STEP
│   ├── decisions.md
│   └── requirements.md
├── body-chassis/
│   ├── layout-02/         active whole-robot model
│   └── layout-01/         previous body; shared purchased/ STEP
├── decisions.md           body CAD-context register
├── TODO.md
└── checklist.md
```

Open Layout 04 in CAD Viewer from [`head/layout-04/README.md`](head/layout-04/README.md). Open the whole robot from [`body-chassis/layout-02/README.md`](body-chassis/layout-02/README.md). Body/chassis composes the head from live Python source — do not redraw it as an AABB.

| Head notes | Body notes |
|---|---|
| [Layout 03 brief](head/layout-03-brief.md) | [Layout 02 brief](body-chassis/layout-02/brief.md) |
| [Layout 03 verification](head/layout-03/review/verification.md) | |
| [Packaging estimates](head/packaging-estimates.md) | [Layout 01 body](body-chassis/layout-01/README.md) (preserved) |
| [Pre-layout brief](head/pre-layout-brief.md) | Purchased Pi 5 / 608ZZ STEP live locally under `body-chassis/layout-01/references/purchased/` (not in Git) |

## Locked inputs RP-06 may not reopen

| Item | Value | Home |
|---|---|---|
| Moving-head load | Layout 04's current hand-kept mass tree is about **588 g**; it is an estimate, not M900 `W`. Layout 03's 499–524 g screening range is historical. Former ~250 g target is inadmissible | [Layout 04](head/layout-04/README.md); [`dimensional-baseline.md`](../../01-system/dimensional-baseline.md) |
| Head envelope | **104 × 150 × 115 mm** crown-inclusive | same |
| Neutral stack | **293.5 mm** (140 body + 49.5 neck + 104 head, head Layout 04 turntable). Meets the 300 mm rounded target with 6.5 mm to spare; closed 2026-09-26 | same |
| Display / camera / C2 / C0 | SKU 30493; SC0874; ESP32-S3-Zero; Pi 5 2 GB + official Active Cooler | component studies; RP-02 |
| Drive topology | Two-wheel + Ø1″ ball + rear skid | baseline v1.12 |

## Owned elsewhere — link, do not copy

| Subject | Home |
|---|---|
| Dimensional / CoM targets | [`dimensional-baseline.md`](../../01-system/dimensional-baseline.md) |
| Mass ledger | [`mass-envelope-ledger.md`](../../01-system/mass-envelope-ledger.md); RP-01 [`payload-mass-capture.md`](../RP-01-head/payload-mass-capture.md) |
| Sourcing / landed cost | [`candidate-sourcing-matrix.md`](../../01-system/candidate-sourcing-matrix.md) |
| Display / camera / harness gates | display study; camera study; [`head-harness-routing-study.md`](../../01-system/head-harness-routing-study.md) |
| Head motion / actuators / scored gates | RP-01 `physics.md`, `gates.md`, `rig.md` |
| Drive physics / scored gates | RP-03 `physics.md`, `gates.md`, `rig.md` |
| Audio `AR-*` / `AP-*` | RP-05 [`audio-requirements.md`](../RP-05-interaction/audio-requirements.md) |
| Thermal trip-wire T-3 | [`power-energy-ledger.md`](../../01-system/power-energy-ledger.md) |

## What to do next

1. Keep editing **this** tree. Fit actual sourced articles into body Layout 02 and head Layout 04.
2. ~~Accept or recover the 304 mm stack~~ — closed: the neck is 49.5 mm, the stack 293.5 mm. **CoM:** [`RP03-CAD-09`](decisions.md) accepted a previous 2,568 g hand-kept register at x +18.77 / h 105.05 mm, retaining the 81.6 g [`RP03-CAD-08`](decisions.md#rp03-cad-08--ballast-bar-ahead-of-the-battery-tub) bar and adding no more. The latest `body-chassis/layout-02/generated/mass-properties.md` reads 2,551.9 g at x +19.46 / h 107.27 mm (a_tip 1.78 m/s²); the physical robot still needs weighing.
3. Do not ballast the head to 250 g.
4. Physical mock-up and G01–G06 registration wait on representative head, electrical, and acoustic evidence.

## Organization record — 2026-09-21

Builder direction: all prototype CAD from RP-01 and RP-03 moves here as `RP-06-cad`. RP-01 `cad/` and RP-03 `cad/` become forwarding stubs.
