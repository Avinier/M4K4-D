# RP-02 Decision

| Field | Value |
|---|---|
| Status | **Open — no gate outcome, no ADR closed, no candidate selected** |
| Created | 2026-09-08 |
| Revised | 2026-09-08 |
| Design question | What compute/controller split, internal link, rail and protection topology, and energy source lets Makad run representative head, drive, display, camera, audio and compute loads concurrently — and with what measured margin? |
| Gate question | Does that design sustain every registered state and the registered mixed-duty cycle for at least 20 minutes without unsafe motion, unintended reset, rail excursion, data staleness or thermal violation — and does every injected fault produce a bounded state? |
| Feeds | ADR-03, ADR-06, ADR-12; power/energy, thermal, internal-communication and compute-coexistence budget rows; `subsystem-interfaces.md` |
| Rule | A negative runtime or coexistence result is an `iterate` on the design or a `reject` of a candidate — never a threshold change. CON-10's 20 minutes cannot be weakened; `Defer` is unavailable for Core outcomes. Failed runs stay cited here |

## Inherited locked decisions

Nothing in RP-02 reopens these; RP-02 measures them.

| Decision | Locked input | Source |
|---|---|---|
| CTRL-01…CTRL-06 | ESP32-S3 motion firmware; C2 separate from the display board; C2 = Waveshare ESP32-S3-Zero; bench twin DevKitC-1-N8R8; no runtime head IMU | `../RP-01-head/decision.md` |
| Display | SKU 30493 renders locally; receives semantic face state | display study; MEM-20260902-01 |
| Camera | Camera Module 3 Wide SC0874, CSI to the SBC | camera study |
| Placement | SBC, mics, speaker, battery in the body; battery low and forward of the axle | dimensional baseline v1.9 |
| E-stop | Motor bus, not logic | `workbench.md` |

## Gate outcomes

| Gate | Outcome | Evidence (run IDs) | Notes |
|---|---|---|---|
| RP02-G01 Protection | | | Verification; per rig revision |
| RP02-G02 Peak coexistence | | | Recorded as: invariant verified against ledger v_ for states S__ with loads __; pending states __; re-run due on __ |
| RP02-G03 Runtime | | | Recorded as a rehearsal with margin; SC-14 closes the requirement at integration |
| RP02-G04 Fault containment | | | Verification; zero unbounded outcomes across the campaign |
| RP02-G05 Control feasibility | | | Measurement with margin ratios |
| RP02-G06 Serviceability | | | Verification; timed procedures |

## ADR closure ladder

This is the folder's purpose. Each row closes independently and says what it is waiting on.

| ADR | Half | Closes when | Waiting on | Status |
|---|---|---|---|---|
| **ADR-03** controller backbone | — | G05 with margin on the Zero (or the twin with the pin-map header noted) **and** G04 on the SBC↔C2 link with real servos | RP-01 servo family for the bus; Phase B | Open |
| **ADR-12** internal communication and timebase | — | `link-contract.md` v1.0 implemented at both ends; G05 link and timestamp metrics met; `timebase.md` validated per its §6 | Phase A for loopback and DevKitC-1; Phase B for the flexing-harness CRC measurement | Open |
| **ADR-06** battery, rails, isolation, low-energy policy | **Architecture** | Every `PA-xx` confirmed or superseded; G01 passed on the rig; chemistry chosen from the ledger's envelope; G06 paths credible on the body layout | Servo rail voltage (RP-01); an SBC candidate; RP-06 body layout for G06 reach | Open |
| **ADR-06** | **Sizing** | Ledger `W` rows cover every load group; trip-wire evaluated against the candidate pack; G03 rehearsal margin recorded | RP-03 drive `W` rows; Phase C battery gate | Open — **expected to close after RP-03, not in stage 2**; RP-02 records it as *bounded, not sized* |

## Candidate register

Candidates are recorded so selection happens from evidence. **No row is selected; no purchase is authorized.**

| Decision | Candidates | What is fixed for comparison | What decides it |
|---|---|---|---|
| Main SBC (LG-01) | Raspberry Pi 5 class (5 V / 5 A supply, highest perception headroom); Raspberry Pi 4 class (5 V / 3 A, lower draw); other CSI-capable Linux SBC with equivalent camera stack support | Must drive the selected CM3 Wide over CSI with a supported stack; body-mounted; UART pairs for C2 and display | Perception workload (RP-07 profiling), ledger LG-01 `W` row, thermal, India sourcing; recorded in the sourcing matrix. Not chosen for RP-02's convenience |
| Battery chemistry | Protected 18650 Li-ion in holder (working assumption for rig design, PA-03); LiPo pouch | Placement low and forward; mass row 150–500 g; handling rules in `workbench.md` | Ledger composite peak and energy; G06 charging/removal paths; solo-builder risk |
| Pack configuration | 2S (regulated servo rail or direct for 6–7.4 V servos); 3S (12 V servo class) | Coupled to RP-01 servo family (PA-04) | RP-01 actuator selection, then ledger |
| Servo-rail conversion | Direct from pack; high-current buck on the motor domain | Rig socket accommodates both | Servo voltage window; measured S07 transient with each |
| Compute-rail converter | Buck module rated 5 V / ≥ 5 A with low ripple; two candidates minimum | Own converter, never shared with the motor domain (PA-05) | SBC candidate's requirement; S07 compute-rail minimum |
| Link transport | 3.3 V UART at 921 600 (primary); USB-CDC on native USB (fallback) | Same framing either way | G05 CRC error rate across the flexing harness; flashing-path conflict (CAD-04a) |
| Base/drive MCU | Same family as C2 (ESP32-S3) preferred; on-SBC RT thread rejected by AD-04 unless proven | Added in RP-03 | RP-03; heterogeneity caution in the control study |
| Charging | External via removable pack or exposed connector (default, PA-09); onboard 2S charger board | — | G06 procedure timing and the battery gate |
| Low-energy thresholds | Loaded-voltage thresholds; coulomb counting | Must trigger above any rail's sag point (PA-07) | SC-TBD-10 registration; pack internal resistance `W` |

## Conclusion

*(per ADR: pass / iterate / reject; selected candidates; budget rows updated with measured value, uncertainty and margin; downstream assumptions changed; re-run obligations created)*
