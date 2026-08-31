# Makad Workbench

| Field | Value |
|---|---|
| Status | Approved |
| Version | 1.0 |
| Owner | Project builder |
| Last reviewed | 2026-08-20 |
| Decision authority | Project builder |

Bench setup and test-readiness gate for Makad prototypes. The current dimensional target is defined by `dimensional-baseline.md`; total mass remains underived (CON-14; CON-TBD-06 allows "moderate weight"; the mass/envelope ledger produces the real number). The scale class remains a droid that one person places on a large tabletop for demonstrations (SCOPE-11), "compact enough to remain approachable" without size minimization (vision), operating in a single household room with following capped at 0.5 m/s (CON-19). That means table-liftable — heavier than a toy, lighter than anything that needs two hands and a plan. At that scale the hazard energy is low: a prototype fault damages the robot, not a person. Revisit the hazard notes if the ledger or drive envelope grows materially beyond that picture. This doc covers only the physical bench; sourcing matrices, the mass/envelope ledger, and the monotonic timebase are engineering deliverables in `risk-prototype-plan.md`; run identity and evidence storage are defined in `run-record-convention.md`.

Current starting equipment: one Elegoo kit. Everything else below must be bought or built.

## On-hand bench instruments (not robot hardware)

| Item | Current role | Explicit exclusion |
|---|---|---|
| Arduino Nano 33 BLE Sense | Bench instrument for optional IMU resonance/backlash measurement, APDS-9960 auto-brightness/proximity-startle experiments, and early PDM-mic DOA work toward the 13° target | Not installed in RP-01, not a motion controller, not in the head mass ledger or BOM. Its nRF52840 offers BLE, not Wi-Fi. |

These are candidate-feature experiments, not purchase triggers or V1 commitments. Do not buy a XIAO or SPI IMU now.

## Buy list (Mumbai)

| Item | Spec | ₹ approx | When |
|---|---|---|---|
| Soldering station | Temp-controlled (Hakko FX-888D clone or decent Chinese station), not a pencil iron | 2,500–5,000 | Now — **✅ selected, see below** |
| Bench PSU | 30 V / 5 A **with current limit** (Korad KA3005D class) | 3,000–6,000 | Now — highest-value item on this list — **✅ selected, see below** |
| Multimeter | With a fast continuity beeper | 800–3,000 | Now |
| Logic analyzer | 8-ch clone + sigrok/PulseView; Saleae later if earned | 800–1,500 | Now |
| E-stop parts | Latching mushroom switch + XT60 in the motor rail | ~300 | Before first motion rig |
| Calipers, helping hands, ESD mat | — | ~1,500 | Now |
| Solder, breadboards, jumpers, wire, connectors, component stock | — | 1,500–3,000 | Now |
| Oscilloscope | Budget 2-ch DSO (Fnirsi 1014D / Hantek) | 4,500–9,000 | **Defer** until an analog problem appears (motor noise on a rail, brownout) |
| LiPo bag + balance charger | — | 500–1,500 | **Defer** until a battery pack exists |

Realistic total to start: **₹10,000–18,000** (scope pushes it to ~25,000). Sources: Robu.in, Zbotic, and Lamington Road — walk it once; local availability beats 3-day shipping for iteration latency.

Standing PSU rule: before first power-up of any new circuit, set the current limit to expected draw plus margin (~200 mA for logic-only boards). A miswire then hits the limit and the circuit survives.

### Finalized sourcing (first purchases, 2026-08-20)

| Item | Model | Vendor | ₹ | Notes |
|---|---|---|---|---|
| Bench PSU | **Korad KA3005D** (30 V / 5 A, linear, CV/CC) | mtools.co.in | ~4,500 | Plain **D** (no USB/PC control) is sufficient; do not pay extra for the "S"/"P" programmable variants. |
| Power leads | **4 mm banana → alligator/crocodile, 1 m, 15 A** — red + black pair | Robu.in | ~150 ea (~300/pair) | Buy one red + one black. 15 A rating is ample (PSU maxes at 5 A). |
| Soldering station | **Yihua 948DB+-II** (T12 cartridge, 75 W, PID, digital) | Robu.in / ElectronicsComp | ~2,650 (₹2,249 + 18% GST) | Iron-only, no hot air (SMD rework not in scope). Ships with stand + 3 T12 tips + cord. Chosen for **T12 thermal recovery**, the spec that matters for servo-lead/XT60/JST joints. |
| Multimeter | **ANENG** TRMS, 9999-count, auto-range, NCV | Amazon.in / Robu.in | ~1,200–1,800 | **Buy the rotary-dial variant with a dedicated continuity (·))) ) position — not the dial-less "Smart" auto-detect body.** Do short-hunting from the manual continuity position, never Smart mode (its auto-detect adds beeper latency and can guess the wrong function). TRMS/NCV are nice-to-have, not why it was chosen; the **fast continuity beeper** is. |
| Logic analyzer | **FX2LA 8-ch, 24 MHz USB clone** ("24M 8CH, Saleae-compatible") | Amazon.in / Robu.in | ~800–1,500 | Drive it with **free sigrok/PulseView** (loads `fx2lafw` firmware + protocol decoders) — the "Saleae-compatible" label just means it enumerates; you won't use Saleae's software. **Logic-level only: probe ≤5 V signals, never the motor rail or anything >~5 V (no input protection).** 24 MHz is ample for Makad's I²C/UART/servo PWM; only genuinely fast SPI would ever earn an upgrade. Pick the cheapest listing with dupont test clips included. |
| Calipers | **Birud 150 mm stainless-steel digital caliper**, ±0.01 mm | Amazon.in | ~700–1,100 | The one spec that matters is **stainless measuring surfaces + ±0.01 mm accuracy** — this unit has both. "Plastic, Stainless Steel" = steel jaws/beam, plastic LCD housing (normal). **Reject carbon-fibre/composite units and anything quoting ±0.1–0.2 mm** (e.g. the KD Royale carbon-fibre ±0.2 mm — 10× worse, feeds garbage into the mass/envelope ledger). Keep spare LR44 batteries. |
| Helping hands | **Inditrust 3-arm flexible-gooseneck, table-clamp base** | Amazon.in | ~300–500 | Clamp base chosen over a weighted base for **stability under pressure** when feeding wire into a joint. Holds *small parts/wires*, not a full PCB — a dedicated PCB vise is a later if-earned add. Alternative if grab-and-go placement is preferred: a **5-arm weighted-base** unit, but only if the base is genuinely heavy (a light one slides — worst of both worlds). |
| ESD mat + wrist strap | **SCHOFIC 2-layer anti-static rubber mat, 18×36", w/ wrist strap** | Amazon.in | ~600–1,000 | The **grounded board-handling surface** for the SBC + bare sensors. Rubber (durable, flat) > PVC. **Only works if grounded: mat corner-snap → grounding cord → a verified earth pin** (multimeter-check the socket earth first — Indian home earth is often dead). Confirm the box includes the **mat grounding cord**, not just the wrist strap. **Not heat-rated — never rest the iron on it.** |
| Cutting mat | **A2 self-healing, 18×24" (457 × 610 mm), green** | Amazon.in | ~400–700 | Aesthetic/general **base layer** + knife-safe surface for wire/heatshrink/standoff trimming. Electrically inert (insulating PVC) — does **not** ground the ESD mat sitting on top, and its "anti-static" label (if any) is not relied on. **Also not heat-rated — no iron on it.** Bench stack: cutting mat (base) → ESD mat (grounded island) → *hot-iron zone TBD*. |

Vendor/price notes: mtools is a real, established tools vendor but a mobile-repair shop with a sloppy web store and undefined online-return terms — so pay by card/UPI (dispute recourse), not bank transfer. ₹4,500 is the genuine Indian street price (₹4,000–4,800 range); it is **not** suspiciously cheap. Amazon.in lists only a grey-imported unit at ~₹35,000 — ignore it. Prices/stock re-check rule (below) still applies before purchase.

Genuine-Korad acceptance test — run within the return window, before the unit is trusted for any scored test:
1. Display shows **no pink/magenta tint when output is OFF** (a known counterfeit tell).
2. Set 5 V, current limit 0.2 A, output on, briefly short the leads → display must snap to **CC**, current pinned ~0.20 A, voltage collapsing toward 0, no spark. This proves the current limiter — the reason this unit was chosen — actually works.
3. Reject SMPS-labelled units: genuine KA3005D is **linear, made in China**. Any listing/unit marked "SMPS" or "Made in India" is a clone and defeats the low-noise purpose.
4. Fail either → raise the return immediately while inside the window.

Multimeter acceptance test — run on arrival, within the return window:
1. Dial to the dedicated continuity (·))) ) position, touch the two probes together → beep must be **instant and latch**, not delayed by a beat.
2. Drag one probe quickly across two touching points → the beep must keep up with the movement.
3. Noticeable lag before the beep = the laggy-beeper failure this row exists to avoid → return within the window.
4. Sanity-check accuracy against the Korad: set the PSU to 5.00 V, measure → meter should read within a few counts.

Why the **T12** class over the alternatives: in a traditional 936-style station the heater and sensor sit in the handle, behind the tip, so recovery is slow when the tip dumps heat into a thick servo lead or a ground plane. A T12 cartridge puts heater **and** sensor in the tip itself, millimetres from the joint — it recovers in ~1 s where a 936 sulks for ~10. Thermal recovery, not max temperature, is what separates a clean joint from a cold blob, and Makad's work (22–26 AWG servo leads, JST/XT60 connectors) hits that case constantly. Iron-only is deliberate: hot-air combos (Yihua 862D class) exist for SMD rework Makad isn't doing yet, and the combo compromises the iron to hit the price. Genuine Hakko FX-888D (~₹10–12k) uses older T18 tips, not cartridges, and counterfeit Hakko tips are rife in India — bad value here specifically. The 948DB+-II being ~₹2,650 is **not** suspiciously cheap: a T12 base unit is commodity electronics (the intelligence lives in the replaceable tip), and iron-only skips the expensive hot-air/high-wattage hardware. The money in this category buys tip quality, power headroom, and build QC — none of which Makad's soldering needs yet.

Soldering-station acceptance test — run before first use:
1. **Grounding / ESD-safe check** (the one real catch on cheap T12 units, KSGER-class included): unit unplugged, check **continuity from the iron tip to the earth pin of the mains plug** → must read near-0 Ω. Open circuit = not ESD-safe and mildly unsafe; note it or return.
2. Heat-up: set 300 °C from cold → tip should reach temp in ~7–10 s (confirms genuine T12 behaviour, not a mislabelled slow heater).
3. Confirm at least one bundled tip is a **chisel (D-series)** — the 95%-of-work tip. A fine conical alone transfers heat poorly. **Note: this model uses proprietary Yihua "T12-TYPE-x" cartridges, NOT universal Hakko T12** — a Hakko T12-D24 will not fit. Replacement chisel is the Yihua **T12-TYPE-2.4D**. Real cartridge recovery, but mild tip-supply lock-in.

### Finalized consumables & sub-items (2026-08-21)

Split across two storefronts by deliberate choice: generic commodities (solder, cutters, desolder kit) from Amazon India where third-party pricing wins; station-specific and fluxing items from Robu.in (1–2 day Mumbai delivery). This relaxes the earlier "Robu only" preference on purpose — only for parts where vendor doesn't matter.

| Item | Spec | Store | Notes |
|---|---|---|---|
| Solder wire | **63/37 eutectic, 2.0% rosin core, 0.8 mm** (~183 °C, no plastic phase) | Amazon | Primary solder; eutectic = clean liquid→solid snap, forgiving for learning. 0.8 mm suits servo leads / connector pins / general PCB; 1.0 mm only for heavy joints. |
| Flush cutter | Narrow micro-jaw side cutter | Amazon | For snipping component legs flush to the board. |
| Desolder kit | **Tabiger 3-in-1** — vacuum pump + 2× copper braid wick (2.5 mm) | Amazon | Dual-action mistake correction: bulk extraction (pump) + fine bridge cleanup (wick). |
| Flux paste | **Noel White flux paste, 10 g** | Robu | Low-smoke, low-residue rosin activator. |
| Iron holder + cleaner | **Yihua X-4** — holder w/ dry brass wool + tip-storage slots | Robu | Brass wool (not wet sponge — no thermal shock to tip); side slots store spare cartridges. |

Chisel tip not bought separately — relying on the 3 bundled T12 tips for now; replacements are Yihua-proprietary (see acceptance test note above).

Prototyping stock — starting equipment is the **Elegoo EL-KIT-003 UNO Super Starter Kit** (UNO R3, 1× 830-pt breadboard, M-M jumper bundle, starter passives/LEDs/transistors/diodes, potentiometer, 74HC595, SG90 servo, ULN2003 stepper, LCD1602, IR remote). Added on top:

| Item | Spec | Store | Notes |
|---|---|---|---|
| Breadboards | 2× 830-point (→ 3 total with the kit's one) | Amazon | Spares let one rig stay wired while experimenting on another. |

Deferred as **as-needed, not blind-stocked** (they pair with components not yet chosen): mixed **M-F / F-F jumper set** (~₹150, when wiring sensors/servos), **22 AWG solid-core hookup wire**, **power connectors** (XT60/JST/screw terminals + Dupont crimp kit — chosen once battery/motor-driver are picked), **heatshrink tubing**.

## Hazard notes

1. **Unexpected motion** — real. A firmware bug slews the neck at full speed with head mass attached. Damages the robot, not people. Mitigate with firmware velocity/torque/angle caps and the E-stop.
2. **Fall from desk/table** — the #1 hardware-loss risk. Differential drive on a desk can drive itself off the edge. Test on the floor, or use a tabletop lip/catch.
3. **Short circuit** — mitigated by the current-limited PSU rule above.
4. **Unstable fixture** — real during neck bring-up. Clamp the rig; never blu-tack a moving mass to a desk.
5. **Pinch** — marginal. A hobby servo hurts a finger, doesn't injure it. Matters only if a child or pet is around during tests.
6. **Hot surfaces** — marginal. Soldering iron; stalled servos get warm.
7. **Projectile** — not applicable; nothing spins fast enough.
8. **Battery** — not applicable until a pack exists; see below.

No exclusion zones, spotters, tethers, or marked floor geometry — those exist for machines that can break a wrist.

## E-stop

Fit one to every motion rig. It must cut **motor bus power, not logic power** — killing the MCU mid-motion while motors hold position is a different, worse failure. A latching mushroom switch in the motor rail plus an XT60 you can physically yank covers it.

## Scored-test gate

No test whose result gets recorded against a registered gate (`RP*-G*`) starts until:

1. the E-stop is **verified working this session** — checked, not just installed;
2. current, velocity, torque, and joint-angle limits are set **for this specific test**;
3. the rig is clamped or the robot physically cannot leave the test surface;
4. the firmware/software commit, configuration, and rig revision are recorded;
5. logging is **confirmed writing** before the run, not discovered empty after;
6. an instrument on the bench can actually resolve the gate's threshold (a 200 ms settling gate needs something that measures 200 ms).

Exploratory bench poking is outside this gate. The dominant solo-builder failure is not injury — it is getting a number you can't trust or reproduce; items 4–6 are what prevent that.

## Battery (deferred, then respected)

Battery-pack fabrication or charging does not begin without a **written, dated procedure produced before first use and not edited during the session**, plus the LiPo bag and balance charger. Rules when there: charge in the bag, never unattended, correct cell count and rate, non-flammable surface (tile/metal/concrete, not a wooden desk or carpet), store at 40–60% (3.7–3.85 V/cell).

Worth evaluating in ADR-06: protected 18650 cells in a holder are meaningfully more forgiving than LiPo pouches, and Makad's draw (small servos + SBC-class compute) doesn't need LiPo discharge rates. That is a spec decision, not a shopping decision.

## Approval note

Approved by the project builder on 2026-08-17 as the initial workbench sourcing and powered-test-readiness baseline. Prices, stock, and local availability are planning estimates and must be checked again immediately before purchase. Approval does not select final Makad components, battery chemistry, pack design, or system architecture.
