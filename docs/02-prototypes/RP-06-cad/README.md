# RP-06 — Sourced layout CAD

| Field | Value |
|---|---|
| Status | **This folder owns the working CAD.** Phase A packaging is the article. Physical validation is 0%. No gate registered, no mock-up built, no scored run |
| Governing plan | [`risk-prototype-plan.md`](../../01-system/risk-prototype-plan.md) v1.15 §RP-06 |
| Purpose | Close **ADR-01**, **ADR-08** and **ADR-11** provisionally from an obtainable, serviceable layout; export binding envelopes to `physical-architecture.md` |
| Active models | Head [Layout 03](head/layout-03/README.md). Whole body [Layout 02](body-chassis/layout-02/README.md) |
| Closure instrument | [`TODO.md`](TODO.md); detail in [`checklist.md`](checklist.md) |

RP-01 is an object. RP-02 is states and interfaces. RP-03 is a vehicle plus local safety. **RP-06 is the whole-robot packaging prototype**, and therefore the home of the CAD.

Root `cad/` stays empty until stage-7 integrated freeze. RP-01 and RP-03 keep mechanism, physics, gates and rigs; they link here for geometry.

## Start here

| Document | What it owns |
|---|---|
| [TODO](TODO.md) | Builder remaining-work punch list |
| [Closure checklist](checklist.md) | Remaining G01–G06 work; CAD-done vs physical-open |
| [Head Layout 03](head/layout-03/README.md) | Active 1:1 head. Viewer, verification, mass tree |
| [Body/chassis Layout 02](body-chassis/layout-02/README.md) | Active whole-robot assembly. Live-imports Layout 03 |
| [Head decisions](head/decisions.md) | `HEAD-CAD-01…10` |
| [Body/chassis CAD-context decisions](decisions.md) | `RP03-CAD-01…03` (CAD-first, not RP-03 safety approval) |
| [Body/chassis closure plan](body-chassis-plan.md) | Packaging acceptance checklist for the integrated model |
| [Prototype open items](../openitems.md) | Folder-wide remaining-open index |
| `runs/` | Run records per [`run-record-convention.md`](../../01-system/run-record-convention.md) |

## CAD map

```text
RP-06-cad/
├── head/                  Layout 03 active; 02 and 01 preserved
│   ├── layout-03/         1:1 packaging, service, optics, harness overlays
│   ├── layout-02/         preserved previous head
│   ├── layout-01/         first study + purchased catalog STEP
│   ├── decisions.md
│   └── requirements.md
├── body-chassis/
│   ├── layout-02/         active whole-robot model
│   └── layout-01/         previous body; shared purchased/ STEP
├── base/pass-01/          historical ugly envelope (head lump, caster swap)
├── decisions.md           body CAD-context register
├── body-chassis-plan.md
├── TODO.md
└── checklist.md
```

Open Layout 03 in CAD Viewer from [`head/layout-03/README.md`](head/layout-03/README.md). Open the whole robot from [`body-chassis/layout-02/README.md`](body-chassis/layout-02/README.md). Body/chassis composes the head from live Python source — do not redraw it as an AABB.

| Head notes | Body notes |
|---|---|
| [Layout 03 brief](head/layout-03-brief.md) | [Layout 02 brief](body-chassis/layout-02/brief.md) |
| [Layout 03 verification](head/layout-03/review/verification.md) | Historical envelope: [`base/pass-01/`](base/pass-01/) |
| [Packaging estimates](head/packaging-estimates.md) | [Layout 01 body](body-chassis/layout-01/README.md) (preserved) |
| [Pre-layout brief](head/pre-layout-brief.md) | Purchased Pi 5 / 608ZZ STEP live under `body-chassis/layout-01/references/purchased/` |

## Locked inputs RP-06 may not reopen

| Item | Value | Home |
|---|---|---|
| Moving-head load | Layout 03 D/E **~499–524 g complete, nominal 509 g at M008=20 g**. Former ~250 g target is inadmissible | [`dimensional-baseline.md`](../../01-system/dimensional-baseline.md) |
| Head envelope | **104 × 150 × 115 mm** crown-inclusive | same |
| Neutral stack | **304 mm**. 300 mm is a rounded target. Accept or recover 4 mm | same |
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

1. Keep editing **this** tree. Fit actual sourced articles into Layout 02 / Layout 03.
2. **Accept or recover** the 304 mm stack. **Hit or revise** the +25 / 124 mm CoM target — Layout 02 currently reports ~+10 / ~108 mm.
3. Do not ballast the head to 250 g.
4. Physical mock-up and G01–G06 registration wait on representative head, electrical, and acoustic evidence.

## Organization record — 2026-09-21

Builder direction: all prototype CAD from RP-01 and RP-03 moves here as `RP-06-cad`. RP-01 `cad/` and RP-03 `cad/` become forwarding stubs. Root `cad/` remains reserved for stage 7.
