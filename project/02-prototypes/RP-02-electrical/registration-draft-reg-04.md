# RP02-P2-REG-04 — Draft supersession record

| Field | Value |
|---|---|
| Status | **DRAFT. Not registered.** No registered text has been edited. This record takes effect only when the builder approves it in the block in §5 and the edits in §4 are made |
| Prepared | 2026-09-25 |
| Source | `board-specs.md` v0.18 §1.1 (builder acceptances `BA-01`, `BA-02`, and the cross-board requirements from the 2026-09-25 reviews) |
| Amends | `power-implementation-basis.md` (`RP02-P2-REG-02`), `power-architecture.md` (`RP02-P2-REG-01`), and by consequence `power-branch-contracts.md` |
| Does not amend | `brownout-restart-contract.md` (`RP02-P2-REG-03`): its thresholds stay evidence-gated |
| Rule applied | `power-architecture.md` §8: "A new energy route, merged safety/application failure branch, changed charging permission, changed E-stop/motor-arm authority or changed return topology requires explicit supersession and downstream ledger/rig/gate review." R4-3 touches E-stop/motor-arm authority, so it is drafted with a downstream-review list |

The builder accepted the recommendations on 2026-09-25 as **working decisions**. Accepting a working decision is not the same as registering a change to a registered baseline, so this draft exists for the builder to approve, edit or reject each item separately.

## 1. Proposed registered changes

### R4-1 — `PB-COMPUTE` nominal output voltage

| | Registered today | Proposed |
|---|---|---|
| Text | `power-implementation-basis.md` §2.2 `PB-COMPUTE`: "**5.1 V nominal registered** for selected Raspberry Pi 5 2 GB"; §5.4: ≤ 100 mV steady and ≤ 200 mV transient total drop "from regulated 5.1 V output to board terminal" | **5.15 V nominal** at the converter output (`LTC3119`, 619 kΩ / 113 kΩ), same 100 mV steady and 200 mV transient allowances, same "> 4.8 V reliable operation" guidance |
| Why | 5.10 V has a worst-case converter low of 4.989 V; minus the 200 mV transient allowance that is 4.789 V, below the 4.8 V guidance (`board-specs.md` §5.4.2) | 5.15 V has a worst-case range of 5.038–5.262 V; minus 200 mV the low is 4.838 V, above 4.8 V |

**Precondition, not yet met.** The Raspberry Pi 5's published upper operating input voltage was not found. The USB `vSafe5V` range is 4.75–5.5 V, the USB PD source tolerance is ±5% (4.75–5.25 V), and the Pi 4 datasheet gives 6.0 V absolute maximum. The proposed worst-case top of 5.262 V is 12 mV above the PD ±5% figure and well inside `vSafe5V`. **Builder choice:**

| Option | Worst-case range | Low after the 200 mV transient | Note |
|---|---|---|---|
| **A (accepted as `BA-01`): 5.15 V** | 5.038–5.262 V | 4.838 V | Exceeds the PD ±5% top by 12 mV; inside `vSafe5V` |
| B: 5.13 V | 5.018–5.241 V | 4.818 V | Inside PD ±5%; margin to 4.8 V is 18 mV |

Either needs confirming against the Raspberry Pi's own statement of the input range when one is published.

### R4-2 — `OFF` configuration (`PA-14`)

| | Registered today | Proposed |
|---|---|---|
| `PA-14` `OFF` row | Permitted source/routes: "Pack protection/BMS quiescent path only; no RP-02 logic/application/motor rail". Required behavior: "No back-power from data/programming ports; user can isolate/remove pack" | **`OFF` powers only: pack protection (`PCB-01`), the charger's battery-only quiescent draw, the system-power latch's nano-power circuit, and the motor-gate controller with its `UV`/`OV` divider. No logic, application or motor rail. The combined pack draw is a candidate bound of about 43 µA typical and 100 µA maximum (`E`, `board-specs.md` §4.2), to be measured at 3.7 V and 8.4 V.** Required behavior unchanged |
| Why | The charger (17–24 µA with its ADC off, `D`), the latch (6 µA) and the gate controller with its divider (about 11 µA typical, 48 µA maximum) are always connected to the pack in the chosen design | The draw is about 1.2–2.8% of the 2.5 Ah pack per month, of the same order as cell self-discharge at the typical figure |

The fallback if the builder does not approve: add a battery-disconnect switch that closes only with an adapter present, at the cost of a high-side switch and a start-up race with the adapter's `VBUS` detect.

### R4-3 — Motor-arm latch clears on any permit-term loss

| | Registered today | Proposed |
|---|---|---|
| Text | `power-implementation-basis.md` §8.3: "E-stop assertion also clears the system motor-arm latch. Physical E-stop release alone cannot restore `PB-MOTOR`; a fresh local arm action is required." (`F-13`) | **Additionally, the `SYSTEM_ARM` latch clears on the loss of any other `MOTOR_PERMIT` term (`CHARGE_ABSENT`, `ENERGY_OK`, `C2_READY`, `BASE_READY`), not only on E-stop assertion. A return of that term never re-arms without a fresh local arm action.** |
| Why | The `LTC4368` undervoltage fault recovers by itself 32 ms after it clears, with no re-arm; the watchdog reset and brownout must not resume an old arm (`board-specs.md` §5.1, §7) | Keeps `BR-05` fail-inactive and fresh-intent recovery intact |

Downstream review needed (`power-architecture.md` §8): `F-12`/`F-13` fault rows, `brownout-restart-contract.md` `BR-05`/`BR-06` wording (the permit expression is unchanged; the latch behavior is stated), and the rig procedures for `G01`.

### R4-4 — Requirement handed to RP-03 (not an RP-02 registration)

The cells' maximum charge current is 4 A (Samsung 25R, `D`). The motor gate's reverse trip (14.0–19.3 A) and the pack's charge-overcurrent trip (16.8–26.5 A) are far above it. **RP-03's drive stage must hold regeneration into the motor bus at or below 3 A, and to zero below 0 °C**, through the DRV8874 current limit and the C3 braking policy. RP-02 records the requirement in `board-specs.md` §5.3 and `../openitems.md`; it becomes an RP-03 requirement only by RP-03's own decision.

## 2. Explicitly not registered

Part selections and values in `board-specs.md` (converters, protectors, FETs, shunts, thermal cutoff, charger straps, watchdog part and timing); board sizes and placement; the brownout proposals in §8.1 (`V_SRC_SAFE` 4.6 V, `ENERGY_OK` 5.7/6.4 V, `UV` 4.9 V, hold-up, discharge candidates); the servo family (RP-01 owns the freeze; XC330 is a working assumption, `BA-03`); the drive-motor SKU; the audio amplifier; any purchase; any gate outcome.

## 3. What the working design already does

`board-specs.md` implements R4-1 to R4-3 as the working design, so approving them changes registered text but not the design. Rejecting one changes the design: R4-1 to 5.10 V (accept the transient shortfall or add remote sense), R4-2 to a battery-disconnect switch, R4-3 to a narrower arm-clear (E-stop only) with the `UV` self-recovery documented as an accepted behavior.

## 4. Edits to make on approval (none made)

| File | Edit |
|---|---|
| `power-implementation-basis.md` | §2.2 `PB-COMPUTE` row (5.1 V → approved value); §5.4 `PB-COMPUTE` row wording; §8.3 arm-clear sentence; §9 registration record: add `RP02-P2-REG-04` |
| `power-architecture.md` | `PA-14` `OFF` row and the §7 registered-topology note if it repeats the wording; §8 registration record: add `RP02-P2-REG-04`; change log |
| `power-branch-contracts.md` | `PB-COMPUTE` numeric fields if they quote 5.1 V; `PB-SAFE-C2`/`PB-MOTOR` state text for R4-3 |
| `power-calculation-ledger.md` | Compute-branch drop and converter-loss rows that use 5.1 V (recompute at the approved value) |
| `decision.md` | Registered-decision line for `RP02-P2-REG-04`; candidate register `PB-COMPUTE` row |
| `board-specs.md` | §1.1: mark `BA-01`, `BA-02` as registered by `RP02-P2-REG-04`; header note |
| `README.md`, `../openitems.md` | Pointer rows |

## 5. Approval block

| Item | Builder decision |
|---|---|
| R4-1 (option A 5.15 V, option B 5.13 V, or reject) | *not yet decided* |
| R4-2 | *not yet decided* |
| R4-3 | *not yet decided* |
| R4-4 (hand to RP-03) | *not yet decided* |

**Builder approval:** *pending.* Enter the exact approving statement and date here when given, as for `RP02-P2-REG-01` ("yes to all"). Until then this file registers nothing.

## 6. Reopen rule

A change to the `LTC3119` setpoint, any new always-connected load in `OFF`, or any change to which terms clear the arm latch requires a new supersession record and the downstream review in R4-3.
