# RP-06 TODO

| Field | Value |
|---|---|
| Status | **Open.** Working CAD is Layout 03 + body/chassis Layout 02. Physical validation 0% |
| Home | [`README.md`](README.md) |
| Detail | [`checklist.md`](checklist.md) |

Checking a box here does not freeze a SKU, promote `E` to `W`, or register a gate.

- [ ] Decide whether to accept the 304 mm neutral stack or recover 4 mm to meet the rounded 300 mm target.

- [ ] Resolve inherited RP-01 blockers:
  - [ ] two screw collisions
  - [ ] pitch-frame stiffness
  - [ ] roll-saddle stiffness
  - [ ] hard-stop margin
  - [ ] bearing SKU
  - [ ] balance trim
  - [ ] CAD/firmware sign mapping
  - [ ] actuator family
  - [ ] production camera interconnect

- [ ] Replace remaining CAD envelopes with exact vendor or measured geometry:
  - [ ] motors and gearboxes
  - [ ] wheels and hubs
  - [ ] ball-transfer article
  - [ ] battery
  - [ ] power modules
  - [ ] motor drivers
  - [ ] sensors
  - [ ] audio hardware
  - [ ] connectors and cable exits

- [ ] Resolve the RP-03 CAD-versus-safety issue:
  - the controller/safety design expects multiple direct stop-path sensors
  - current Layout 02 only packages one guarded rear TCRT channel and explicitly makes no full forward/lateral cliff-protection claim
  - this must be reconciled before physical layout closure

- [ ] Select the status LED and diffuser/optic.

- [ ] Select microphone front end, microphone boards, speaker, and amplifier.

- [ ] Select battery and enough of the power hardware to verify actual packaging.

- [ ] Obtain or fabricate representative articles and measure:
  - [ ] every relevant mass
  - [ ] complete robot CoM
  - [ ] head installed mass/CoM
  - [ ] service clearances
  - [ ] cable bend and demate volumes
  - [ ] airflow and temperatures

- [ ] Perform the physical display tests:
  - [ ] smoked window
  - [ ] viewing angle
  - [ ] distance
  - [ ] lighting
  - [ ] frame rate and tearing

- [ ] Perform camera tests:
  - [ ] FOV and occlusion
  - [ ] calibration
  - [ ] focus lock
  - [ ] motion smear
  - [ ] LED/display contamination
  - [ ] live CSI endurance

- [ ] Perform audio tests:
  - [ ] speaker level and vibration
  - [ ] microphone contamination
  - [ ] cooler and mechanism noise
  - [ ] playback-while-listening behaviour

- [ ] Demonstrate replacement of a named high-risk module and record time/tools.

- [ ] Verify current suppliers, landed costs, and substitutes.

- [ ] Register and execute RP06-G01…G06.
