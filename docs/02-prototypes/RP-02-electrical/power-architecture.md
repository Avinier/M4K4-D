# RP-02 Power Architecture — Candidate Rail, Protection and Energy Topology

| Field | Value |
|---|---|
| Status | **Candidate design, evidence class `E`.** Nothing here is selected, sized or purchased. It is the ADR-06 *architecture* input; ADR-06 *sizing* waits on the ledger |
| Owner | Project builder |
| Created | 2026-09-08 |
| Inputs | `../../01-system/power-energy-ledger.md` (planning envelopes); `../../01-system/workbench.md` (E-stop, PSU, battery rules); `../../01-system/dimensional-baseline.md` (battery low and forward of axle; body-mounted SBC); `../../01-system/head-harness-routing-study.md` (branch partition; yaw boundary); `state-register.md` |
| Feeds | ADR-06; `gates.md` G01 and G06; `rig.md`; sourcing matrix power rows |
| Method | `../../intuition.md` §5.1 step 3 electrical toolkit; each numbered choice below is a `PA-xx` proposal with its reason and its reopen condition |

This document answers *what shape* the electrical tree has, so that G01 has something to review and the rig has something to build. It does not answer *how big* — conductor gauge, regulator rating and pack capacity are the ledger's outputs and arrive as `W` rows accumulate.

## 1. Two-domain topology

```mermaid
flowchart TB
    PACK["Battery pack<br/>chemistry, S-count open (PA-03/04)"] --> PROT["Pack protection<br/>BMS/PCM + main fuse"]
    PROT --> ISO["Main isolation<br/>physically yankable XT60"]
    ISO --> LOGIC["LOGIC DOMAIN<br/>never cut by E-stop"]
    ISO --> ESTOP["E-STOP<br/>latching mushroom, in series"]
    ESTOP --> MOTOR["MOTOR DOMAIN<br/>every hazardous output"]

    LOGIC --> BK1["Buck A — 5 V compute rail<br/>SBC + camera + mics"]
    LOGIC --> BK2["Buck B — 5 V head-logic rail<br/>display board + C2 + status light"]
    LOGIC --> BK3["Buck/LDO — audio rail<br/>amplifier (hazard-free, but noisy)"]
    LOGIC --> BMCU["Base MCU / safety sensing<br/>(when RP-03 adds it)"]

    MOTOR --> SRV["Servo rail<br/>voltage set by RP-01 servo family (PA-04)"]
    MOTOR --> DRV["Drive rail<br/>motor driver (RP-03)"]
    SRV --> FY["fuse Y"] --> SY["yaw servo"]
    SRV --> FP["fuse P"] --> SP["pitch servo"]
    SRV --> FR["fuse R"] --> SR["roll servo"]
    DRV --> FD["fuse D"] --> MD["L / R motors"]

    BK2 -. "5 V + UART link, across yaw boundary<br/>demateable connector (CAD-05)" .-> HEAD["Head: display ESP32-S3, C2, light"]
    SRV -. "servo power + bus, across yaw boundary" .-> HEAD
    BK1 -. "camera CSI, own controlled route" .-> HEAD
```

### PA-01 — Logic and motor domains are electrically distinct, and only the motor domain passes through the E-stop

**Choice.** The E-stop is in series with everything that can move or push: servo rail and drive rail. Compute, controllers, display, camera, audio and sensing stay powered through a stop.

**Why.** `workbench.md`: killing the MCU mid-motion while servos hold torque is a worse failure than the one being prevented. A stopped robot that can still report health, show a face and log the event is diagnosable (AD-11) and recoverable from current intent (SDB failure priority 6). CON-P02 asks for a cutoff of *hazardous outputs*, not of the robot.

**Consequence.** C2 must detect the motor-domain loss (a sense line or servo-bus silence) and treat it as `unsafe`/`inhibited`, never as "servos will reappear so keep the trajectory queued." That is fault case F-12/F-13.

**Reopen if.** A hazardous output is ever found on the logic domain (a heater, a high-current LED, an actuator added later) — it moves to the motor domain or gets its own switched branch.

### PA-02 — Protection is layered: pack, main, per-branch

| Layer | Protects against | Candidate device class |
|---|---|---|
| Pack BMS/PCM | Cell over-discharge, over-charge, cell-level short | Integral to pack choice (PA-03); protected 18650s carry their own PCM |
| Main fuse at the pack | Wiring short between pack and distribution | Blade fuse or resettable at ~1.25–1.5× the ledger's registered composite peak — value from ledger, not from here |
| Per-branch fuse/polyfuse | One load's fault taking the tree down; the specific case is one servo shorting during S07 while the other two are mid-slew | Polyfuse per servo branch and per drive channel; fast fuse on the compute buck input |
| Regulator current limit and thermal shutdown | Sustained overload on a rail | Module-native; verify it exists and what it does on trip (latch versus hiccup) |

**Why per-servo.** The three head axes are listed as *separately observable* load groups in the plan for a reason: a fault on one must be attributable and containable. Shared servo fusing turns a roll-servo short into a three-axis inhibit with no diagnosis.

**Reopen if.** The selected servo family's own protection (Dynamixel-class units report overcurrent and shut down) proves sufficient and per-branch polyfuses add drop that costs servo performance at peak — measured on the rig, not assumed.

### PA-03 — Chemistry: protected Li-ion 18650 in a holder is the working assumption; LiPo pouch is the alternative

**Choice.** Not made. This records the comparison so the decision can be taken from evidence rather than habit.

| Criterion | Protected 18650 in holder | LiPo pouch |
|---|---|---|
| Peak current | 2S2P of ordinary 2.5 Ah cells gives ~10–20 A continuous — ample against the ledger's `E` composite peak of 5.5–9.5 A at 7.4 V | Effectively unlimited for this scale |
| Solo-builder handling risk | Cells swap, holders are non-destructive, cylindrical cells tolerate abuse better; PCM per cell | Puncture/swelling risk; bag and balance-charger discipline mandatory (`workbench.md`) |
| Mass (ledger row 150–500 g) | ~45–50 g per cell + holder; 2S2P ≈ 220–260 g | Lower for the same Wh, typically 60–70 % |
| Volume and placement | Cylinders pack awkwardly but a 4-cell holder is flat enough for "low and forward of the axle" | Flexible shape |
| Charging path (G06) | Cells removable → external charger; or onboard 2S charger board | Balance lead → external charger; onboard charging adds a board |
| Service (SC-17) | Cell replacement without tools if the holder is accessible | Pack replacement requires connector access and care |
| Cost / sourcing (India) | Common; genuine-cell risk is real (reject unbranded "9800 mAh" cells) | Common |

`workbench.md` already notes that Makad's draw does not need LiPo discharge rates and that 18650s are meaningfully more forgiving. **Working assumption for rig design: 2S protected 18650, cell count P decided by the ledger.** This is not a purchase.

**Reopen if.** The ledger's composite peak or the servo family's rail voltage forces 3S/4S (see PA-04) and the resulting holder no longer fits low-and-forward; or the mass row cannot absorb the holder penalty after the head grows.

### PA-04 — Pack voltage is coupled to the RP-01 servo selection, and the rig must accommodate both outcomes

| Servo class (examples, none selected) | Rail | Pack implication |
|---|---|---|
| 5 V class (XC330 reference: 3.7–6.0 V) | Servo rail = regulated 5–6 V | 2S pack + high-current buck on the motor domain; buck must survive S07 transient; **direct 2S is out of the servo's window** |
| 6–7.4 V class (many bus servos) | Servo rail = 2S direct | 2S pack, no conversion loss on the largest load; rail sags with cell voltage — trajectory feel changes over discharge unless the servo compensates |
| 12 V class (XL430/XM-class) | Servo rail = 3S direct | 3S pack; compute buck sees 12.6 V in; more headroom, more mass |

**Choice.** Design the rig with a servo-rail regulator socket so both "regulated from 2S" and "direct from pack" can be measured. Do not pre-empt RP-01's actuator selection from the power side — the same error `control-topology-options.md` §6.3 avoided when it rejected controller boards that "silently decide the actuator family."

**Reopen if.** RP-01 selects; then this collapses to one row and the ledger's servo rail gets a voltage.

### PA-05 — The compute rail has its own converter and never shares one with anything that moves

**Choice.** Buck A feeds the SBC (and, through the SBC, the camera) alone, rated for the SBC candidate's published supply requirement — 5 V at 3 A (Pi 4 class) to 5 A (Pi 5 class) — with the ledger deciding.

**Why.** The failure G02 is hunting is a motion-induced dip resetting compute. An SBC's undervoltage detector trips in the tens-of-milliseconds range; a servo launch transient is exactly that length. Sharing a converter between compute and anything on the motor domain guarantees coupling through the converter's output impedance. Separate converters share only the pack, whose impedance is low.

**Consequence.** Bulk capacitance sits at the *servo rail*, not the compute rail — the servo rail is where the transient originates. The rig measures the compute rail's minimum during S07 with and without added servo-rail bulk (`rig.md` measurement plan).

### PA-06 — The head is fed by three separately owned branches across the yaw boundary

Per the harness study's partition, and preserved here because conductor sizing differs per branch:

| Branch | Carries | Sized for | Owner |
|---|---|---|---|
| Servo power + servo bus | Servo rail at composite three-axis peak; half-duplex TTL or RS-485 pair | S07 transient with registered drop limit; noise separation from CSI | Motor domain |
| Head-logic power + semantic link | 5 V for display board, C2, status light; UART TX/RX (+ optional USB) | Display board peak + C2 peak; link signal integrity across flex | Logic domain (Buck B) |
| Camera CSI | 2-lane MIPI, 3.3 V from SBC connector | Signal integrity, not current | Logic domain via SBC |

All three cross the **demateable boundary at yaw** required by CAD-05 so M020 and M900 can be weighed. The connector choice is a G06 item (service) and a G01 item (a connector that can mate reversed is an unbounded energy path).

**Candidate drop limit (not registered):** ≤ 3 % of servo rail at the registered S07 peak, measured at the servo connector, not at the distribution board. This is a proposal for the G02 invariant's rail-excursion definition and must be registered before scored use.

### PA-07 — Brownout ordering is designed, not discovered

Under a deep pack sag the order in which rails give up matters:

1. **Servo and drive rails may sag first** — the consequence is weak motion, which the C2 sees as tracking error and reports;
2. **Head-logic rail** must outlast the servo rail — C2 must be alive to command `BRAKE` and report;
3. **Compute rail** must outlast both, or must at least *restart cleanly* into an inhibited state (fault case F-02).

Implementation is buck-input undervoltage-lockout thresholds plus bulk capacitance placement; the rig verifies the order by ramping the supply down under S13 load (`rig.md` procedure). The energy states `low` → `critical` in `state-register.md` S14/S16 must trigger **above** the point where any rail begins to sag, with the pack's internal resistance at end-of-life taken into account — i.e. the low-energy threshold is a *loaded* voltage or a coulomb-count, not an open-circuit number.

### PA-08 — Measurement points are part of the architecture

Every branch in §1 has a series measurement point on the rig (shunt or INA-class monitor) and a voltage test point at the load end, not only at the distribution board. On the robot these collapse to what health telemetry needs — pack voltage, pack current, servo rail voltage, and per-servo current from the servos' own telemetry — but the *positions* are decided now so G06 can show a credible measurement path and G02 can attribute an excursion.

### PA-09 — Charging: external by default; onboard only if G06 evidence prefers it

External charging through a removable pack or an exposed balance/charge connector is the default because it removes charging electronics from the enclosure and keeps `workbench.md`'s "charge in the bag, never unattended" rule literally possible. Onboard charging is admissible if the service procedure for pack removal proves worse than the added board. Decided in ADR-06 with the G06 record.

### PA-10 — Low-energy policy hooks are electrical requirements

SDB §6 needs the energy dimension `normal · low · critical · charging`. That requires pack voltage and current telemetry to reach the health responsibility, and a threshold policy registered under SC-TBD-10. The architecture reserves: a pack monitor on the logic domain (coulomb counter or voltage + current), a health message field in `link-contract.md`, and the S14/S16 behaviours in the state register. The *values* are not chosen here.

## 2. Paper physics — the calculations the ledger must be able to run

From `intuition.md` §5.1 step 3, restated so every ledger row has a consumer.

| Calculation | Inputs | Output | Where used |
|---|---|---|---|
| **Brownout** — `V_load = V_pack(SoC, I) − I_peak · R_path` per rail | Composite peak current per state (ledger §4), pack internal resistance (`D` then `W`), conductor and connector resistance | Minimum rail voltage per state; margin to each component's undervoltage limit | G02 invariant; PA-06 drop limit; conductor gauge |
| **Energy** — `E_MD01 = Σ_states P_state · t_state`, then `E_pack ≥ E_MD01 / (usable DoD · η_conv) · (1 + reserve)` | State power (ledger §4), `MD-01` durations, conversion efficiency, reserve fraction (SC-TBD-10) | Required pack Wh; margin | G03 rehearsal; ADR-06 sizing |
| **Regulator thermal** — `P_loss = P_out · (1/η − 1)` steady state; linear stages `(V_in − V_out) · I` | Efficiency at the operating point (`D` then `W`), state duration | Case temperature trajectory; margin to SC-TBD-12 | G02 thermal term; enclosure airflow input to RP-06 |
| **Conductor thermal** — `I²R` over the S11 sustained average and the S13 peak | Gauge, length, ambient inside the head/neck | Temperature rise; derating across the flexing neck | Harness selection; CON-P05 |
| **Fuse coordination** — branch fuse trips before main fuse before pack PCM under a branch short; no fuse trips under S13 | Peak per branch, fuse I²t curves | Fuse values | G01 |

## 3. What this document will look like when it closes

ADR-06 architecture closes when every `PA-xx` above is either confirmed by a G01 review plus rig measurement or replaced by a superseding `PA-xx.v2` with its reason. ADR-06 sizing closes later, in `decision.md`'s ladder, when the ledger's `W` rows cover every load group and the trip-wire has been evaluated against a candidate pack.

## 4. Open items

- [ ] Servo family (RP-01) → collapse PA-04 to one row; give the ledger a servo-rail voltage.
- [ ] SBC candidate → Buck A rating; camera current on the same rail.
- [ ] Pack internal resistance `D` value for the working-assumption cells; replace with `W` on the rig.
- [ ] Register the rail-excursion definition (PA-06 candidate ≤3 %) and the undervoltage limits per component before any scored G02 rehearsal.
- [ ] Decide whether per-servo polyfuses stay after measuring their drop at S07 peak.
- [ ] G06 paths: pack removal, charge connector position, main XT60 reach, E-stop reach — coordinate with the body layout in RP-06.
