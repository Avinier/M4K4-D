# 04 — PCBs

This folder holds the schematic, layout, fabrication and electrical-validation work for the robot's custom boards. It is a work area, not a fabrication release. Part records stay in the [project BOM](../BOM.csv); every selection and change goes in the [build decisions](../decisions.md). It replaces the former `04-custom-pcb/` folder ([D-038](../decisions.md#d-038)).

Each custom board is designed, procured and integrated into the final CAD one at a time, in its own `pcb-NN-name/` folder. [workflow.md](workflow.md) describes the three stages and tracks each board's progress.

## Tools

Chosen in [D-058](../decisions.md#d-058); layout tool and routing changed by [D-060](../decisions.md#d-060).

| Tool | Used for | Where |
|---|---|---|
| KiCad 10.99 (nightly) + KiPy | Schematic and layout, driven through KiPy and computer-use tools; the GUI for review | `/Applications/KiCad-nightly` (build 20261024, `de08734017`), side by side with 10.0.6 in `/Applications/KiCad`. KiPy (`kicad-python` 0.8.0) in `~/.local/share/kipy/venv`; it talks to the running GUI, and the nightly has no bundled `pcbnew` Python. Each board's project is in its folder's `design/` |
| `kicad-cli` (same install as the layout) | ERC, DRC with the schematic-to-board check, Gerbers, drill, pick-and-place, BOM, board STEP, renders | `/Applications/KiCad-nightly/KiCad.app/Contents/MacOS/kicad-cli` (10.99). The 10.0.6 CLI in `/Applications/KiCad` may not read files the nightly saved |
| [`tools/kp.py`](tools/kp.py) | KiPy layout helpers: place (restores 3D models after a flip), octolinear tracks, vias, audit, DRC. Steps in [design-playbook.md](design-playbook.md) | Run with `~/.local/share/kipy/venv/bin/python` against the open PCB editor |
| JLCPCB (default), PCBWay, Lion Circuits (MII service) | PCB fabrication and assembly (PCBA). These three only. Layouts follow the [fab-neutral rules](#fab-neutral-design-rules), and the fab is chosen by quote ([D-062](../decisions.md#d-062)) | — |
| text-to-cad (cadgen) | Stage 3: the board STEP placed in the robot CAD | Project runtime 0.4.28 (see [final/v1](../final/v1/README.md)) |

## Layout rules

These rules take priority over D-058 ([D-060](../decisions.md#d-060); builder, 2026-10-14). They come from someone else's experience of LLM-driven KiCad layout. When an LLM lays out a board, it must:

1. use KiCad 10.99 (the nightly build, which adds scripting features) and drive it through KiPy and computer-use tools;
2. not use an autorouter such as Freerouting;
3. place components one at a time or in small functional groups;
4. adjust placement after routing where that helps;
5. route with octolinear traces, organised into buses of parallel, equally spaced tracks. Plan fanouts first. Keep detours and roundabout routes to a minimum, especially on signal nets. Size track widths and pours for each net's current. Optionally, write reusable scripts that check these properties and use them to check the work.

## Fab-neutral design rules

Only three fabs make Makad boards: **JLCPCB** (China, the default), **PCBWay** (China) and **Lion Circuits** (Bengaluru), on its **MII** (Make in India) service ([D-062](../decisions.md#d-062), builder, 2026-10-25). Every board is laid out so that any of the three can make it on its standard service, with no layout change. The rule set is the strictest standard 2-layer, 1 oz limit of the three. Each board carries it as a KiCad custom rules file, `design/<board>.kicad_dru`, copied from [PCB-15's](pcb-15-nose-hall/design/pcb-15-nose-hall.kicad_dru). The fab is chosen by quote at procure.

| Rule | Fab-neutral minimum | JLCPCB | PCBWay | Lion Circuits MII |
|---|---|---|---|---|
| Track width and copper gap | **0.16 mm** | 0.10 | 0.10 | 0.152 (6 mil) |
| Via | **0.35 mm hole, 0.67 mm pad** (ring 0.16) | hole 0.15, pad 0.25 | hole 0.15, ring 0.15 | drill 0.35, ring 0.152 |
| Via to other copper | **0.31 mm**, from the via's copper and from its hole | — | — | 12 mil (0.305), via to trace |
| Hole to hole | **0.31 mm** | — | — | 12 mil between vias |
| Copper to routed edge | **0.3 mm** | 0.2 | 0.25 | 0.3 |
| Solder-mask web between pads | **0.16 mm** | 0.10 | not stated; confirm | 0.152 |
| Silkscreen text | **1.0 mm high, 0.16 mm line**, or leave silkscreen off | 1.0 | 0.8 | 0.58, line 0.152 |
| Board thickness tolerance | **State it on the order** when the mounting needs it | ±10 % | ±10 % at 1.0 mm and thicker; confirm below | ±10 % |
| Assembly, minimum board | **Panelise** small boards | 10 × 10 mm | quote; 0402 parts get an engineering review | 50 × 100 mm |

Lion's page lists three services. **MII** is the target. **Custom** is looser (0.25 mm drill, 10 mil via spacing), so an MII layout also suits it. **Rush** is tighter (0.4 mm drill, 8 mil tracks, 14 mil via spacing) and is not a target. A board that needs Rush is checked against it first.

Sources, read 2026-10-25: [JLCPCB](https://jlcpcb.com/capabilities/pcb-capabilities), [PCBWay](https://www.pcbway.com/capabilities.html), [Lion Circuits](https://lioncircuits.com/pcb-manufacturing-capabilities). Read the pages again before each order. If a fab tightens a limit, tighten the rule here first.

## Board register

**[D-093](../decisions.md#d-093) (2026-11-06):** PCB-02, 03, 04, 05, 06 and 07 are replaced by bought modules and PCB-13 is deleted. The custom boards are PCB-08, 09, 10, 11, 12, 14 and 15. The superseded rows are kept as the record. The change map is in [simplification-plan.md](../simplification-plan.md).

| ID | Board | Location | BOM | Status | Work still required |
|---|---|---|---|---|---|
| PCB-01 | 2S pack protection | Chassis tub, on the pack | CH-023 | **Bought:** Robocraze TIFPS0629 ([D-019](../decisions.md#d-019)); the RP-02 custom design is reference only | Bench acceptance before cells: [power-boards.md §3](power-boards.md#3-pcb-01--tifps0629-acceptance-before-cells-are-connected) |
| PCB-02 | Charger (BQ25798), on/off latch, pack sense, `ENERGY_OK` | Body, behind the rear panel (vertical) | CH-041 | **Superseded by [D-093](../decisions.md#d-093): bought.** A pushbutton power switch module and an INA226/219 voltage/current monitor; no charger (the pack is charged outside the robot). Rev A routing archived in the [board folder](pcb-02-charger/README.md) | Module selection and India stock ([plan level 3](../simplification-plan.md#7-levels-of-work)) |
| PCB-03 | Motor gate, permit chain, head 5 V rail, drive feeds | Body, above the tub | CH-042 | **Superseded by [D-093](../decisions.md#d-093): bought.** Two buck-boost modules: head pitch/roll 5.5 V and yaw 11.1 V. Drive feeds come straight from the switched bus with the SMBJ8.5A and bulk at each `VM`; the yaw servo plug moves to PCB-08 | Module selection and India stock |
| PCB-04 | Five branch converters (C2, base, Pi, display, audio) | Body, under the compute tray | CH-043 | **Superseded by [D-093](../decisions.md#d-093): bought.** Two Pololu S13V30F5 5 V buck-boost modules ([D-094](../decisions.md#d-094)): one for the Pi, one shared by C3, amp, C2 and display | Module selection and India stock; series Schottky in `W11` (C3 USB back-feed) |
| PCB-05 | Audio front end (MAX98357A, 2 × ADAU7002) | Body, above the Pi, hung from the frame on three M2 SMT spacers ([D-067](../decisions.md#d-067)) | BO-002 | **Superseded by [D-093](../decisions.md#d-093): bought.** MAX98357A breakout (BO-007, promoted from bench) and an audio hub. Rev A archived in the [board folder](pcb-05-audio-front-end/README.md) | Amp mount in CAD; four-mic I²S overlay on the bench |
| PCB-06 ×4 | PDM microphone board | Body shell bosses | BO-005 | **Superseded by [D-093](../decisions.md#d-093): bought.** Four I²S mic breakouts with an L/R pin (INMP441 class), two per lane on SDI0/SDI1. Rev A archived in the [board folder](pcb-06-pdm-mic/README.md) | Boss redesign for the breakout outline; overlay bench test before the shell is printed |
| PCB-07 | Base IMU (ICM-42688-P) | Chassis | CH-021 | **Superseded by [D-093](../decisions.md#d-093): bought.** SPI 6-axis IMU breakout on the existing `J10-7` pinout, on a printed adapter on the J15A holes | Breakout selection; adapter in CAD |
| PCB-08 | Yaw junction (clock-spring stationary end) | Body, under the yaw adapter plate | CH-083 | **Rescoped by [D-093](../decisions.md#d-093):** drops the `W23a`/`W23b` permit and status sideband and `ARM_REQ`; gains the yaw servo plug (`+11V1_YAW`, GND, `SERVO_DATA`, was PCB-03 `J3-5`). Spec; grows +X to X 20 for two 22-pin 0.5 mm ZIFs, `J8-6` power and `J8-7` sideband, taking the cassette FFCs ([D-044](../decisions.md#d-044)) | Schematic; FFC pin order (power on 7 + 7 conductors for the pitch/roll pair, 2 + 2 each for C2 and display). Body-side pinout and the mating rule: [05-harness](../05-harness/README.md) (D-039) |
| PCB-14 | Yaw rotor joiner boards ([D-052](../decisions.md#d-052); replaces the D-044 Ø35 ring): three identical vertical 0.8 mm boards, each a straight 1:1 22-pin 0.5 mm FFC joiner with a down-facing side-entry ZIF for its cassette FFC (`W37`/`W42`/`W43`) and an up-facing one for the head FFC, both on the +Y face, 16.8 mm apart; tabs seat in the rotor posts | Body, inside the rotating yaw hub (Z 133.9–150.7) | BO-062 (×3) | HOLD | Select a ZIF ≤ 2.0 mm tall and ≤ 5.2 mm deep with its actuator; lay out the 1:1 joiner (power pins wide enough for the paralleled `W42` conductors); CSI signal check through two ZIF pairs |
| PCB-09 | C0 link adapter (2 × RS-422, audio pass-through, enclosure-fan switch `J9-4`) | Body, on the Pi header, on two M2.5 × 11 standoffs at Pi holes 3/4 | CH-084 | **Rev A designed; rev B schematic draft on `pcb-09-revB`, layout required before fabrication** ([D-092](../decisions.md#d-092), [D-098 amendment](../decisions.md#d-098)): preserve the Samtec SSW-120-01-T-D socket, 4 layers, existing connector pinouts and mounting; add a qualified six-net button/OFF/INA226 `i2c-gpio` service interface; [board folder](pcb-09-c0-link-adapter/README.md). Final CAD still carries rev A geometry | Rev B DRC and populated fit pending. Do not order rev A fab. Then procure two-sided assembly, SSW-120, THVD1451DR and standoffs; CR-02 boot/overlay and fan current, socket seating and contact check on bench; harness dressing at stage 3 |
| PCB-10 | C3 controller carrier (watchdog, READY, sleep gate, Hall and TCRT circuits) | Body, −Y side wall | CH-044 | **Inputs frozen** ([D-068](../decisions.md#d-068), [board folder](pcb-10-c3-carrier/README.md)): two screws and two printed edge hooks, Espressif DevKitC-1 v1.1 only, TPS3436CCCBG from Mouser India, GPIO map v0.2, `J10-2` named by direction ; [KiCad geometry installed in final CAD](../final/v1/README.md#pcb-geometry-in-the-whole-robot-assembly) | **Design done, rev A** (four layers; DRC clean; `check_pcb10_fit.py` 7/7; [fab outputs](pcb-10-c3-carrier/fab/revA/README.md)); GPIO map v0.3, `J10-2` in U2's order; U2/U3 from Mouser India, consigned; nose, TCRT and head-riser harness re-routes at stage 3; [D-093](../decisions.md#d-093): `J10-12` is unused (PCB-03 is gone) and `W11` gets a series Schottky against USB back-feed; no re-spin |
| PCB-11 | Status LED carrier (WS2812B-2020-V6, 100 nF, 330 Ω in DIN) | Head crown, in the socket fused inside the crown ([D-065](../decisions.md#d-065)) | CH-085 | **Rev A designed** ([D-065](../decisions.md#d-065)); [board folder](pcb-11-status-led/README.md) ; [KiCad geometry installed in final CAD](../final/v1/README.md#pcb-geometry-in-the-whole-robot-assembly) | Procure: panel (with PCB-15), two-sided assembly quote, passive MPNs, V6 from the fab (C52917434) or an RFQ to Hubtronics; brightness, stray-light and light-bleed bench (G03) |
| PCB-12 | C2 head carrier (ESP32-S3-Zero, servo bus, head-link and display transceivers) | Head | CH-086 | **Rescoped by [D-093](../decisions.md#d-093):** no TPS3436 watchdog, no `ARM_REQ`, no READY pair. The Waveshare ESP32 Servo Driver does not fit the C2 bay (65 × 30 mm against 18 × 23.5 mm, [D-094](../decisions.md#d-094)), so this stays a simplified custom carrier | Schematic; head pocket fit |
| PCB-15 | Nose Hall carrier (DRV5055A3, decoupling, output filter, three wire pads); numbered by [D-057](../decisions.md#d-057), formerly listed by its BOM ID | Chassis nose, in the pod-seat slot | CH-064 | **Rev A designed** ([D-013](../decisions.md#d-013), [D-059](../decisions.md#d-059), [D-063](../decisions.md#d-063)); [nose-hall-board.md](../01-chassis/v1/research/nose-hall-board.md); [board folder](pcb-15-nose-hall/README.md) ; [KiCad geometry installed in final CAD](../final/v1/README.md#pcb-geometry-in-the-whole-robot-assembly) | Procure: panel, two-sided assembly quote, passive MPNs; cap trip and wire-break fault bench |
| PCB-13 | Charge inlet: GCT USB4140, TVS2200, ESDA25W, STUSB4500, input P-FET | Body, rear-panel pad (comes off with the panel) | BO-015 | **Deleted by [D-093](../decisions.md#d-093).** The pack is charged outside the robot through rear-panel charge and balance ports. Rev A archived in the [board folder](pcb-13-charge-inlet/README.md) | — |

Power-board specification (superseded by [D-093](../decisions.md#d-093) except the DRV8833 facts, the `VM` TVS and the TIFPS0629 acceptance): the RP-02 [board-specs.md](../../02-prototypes/RP-02-electrical/board-specs.md) is the read-only reference, and [power-boards.md](power-boards.md) holds what the build changes. The charge path, from the USB-C inlet to the pack entry, is in [charge-path.md](charge-path.md). Open board work without another home is tracked in [open-items.md](open-items.md).

## Rules

The board outlines in CAD are packaging assumptions. They imply no Gerbers, completed schematic or passed board test.

Basic chassis fit and controlled motor tests can use a regulated bench supply, a development controller, driver boards and a temporary harness. Hall and bare-TCRT circuits can be prototyped separately. Full custom-board fabrication is not a prerequisite for those tests. Battery-powered and integrated sensor/control tests keep their protection, interface and validation requirements.

Before releasing any board, record:

- its exact revision, schematic, BOM and layout;
- connector pinout, protection and enable behaviour;
- mounting dimensions and fabrication/assembly outputs;
- measured electrical results.

When an interface changes, update the affected CAD and the canonical BOM.

**Droid CAD changes go in [final/v1/cad](../final/v1/cad/) only** (builder, 2026-10-14). Envelope fixes, board STEPs that replace placeholders, and the mounting features they need are made in `makad-v1.step.py`. For example, `DROID_CUTS` cuts material from printed parts, `DROID_ADDS` adds it and `DROID_MOVES` shifts parts ([D-063](../decisions.md#d-063)). They are not made in the chassis, body or head sources. The subsystem checks don't see these changes, so each one gets its own targeted check script in `final/v1/cad` (for example `check_pcb15_relief.py`, [D-059](../decisions.md#d-059)).
