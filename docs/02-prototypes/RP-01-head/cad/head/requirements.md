# Head CAD requirements

Relocated: **2026-09-07**, from section 4 of the [RP-01 material/finish/mass decision](../../material-finish-mass-decision.md#4-cad-requirements). These are the existing requirements with their original IDs and wording preserved. The move does not reopen or supersede D-01…D-08.

## Inherited requirements

| ID | Requirement |
|---|---|
| CAD-01 | Model adjacent panels at 0.3–0.5 mm relative height offsets. |
| CAD-02 | Provide correctly sized wells and bosses for each real visible M2 fastener. |
| CAD-03 | Make the rear-surface window mask opaque across the full 110–115 mm width. |
| CAD-04 | Provide display flashing access or a defined wire-flashing path in the sealed head. |
| CAD-05 | Provide a demateable connector or a defined separable cut plane at the yaw boundary so M020 and M900 can be weighed without cutting conductors. |
| CAD-06 | Use panel lines at least 0.6–0.8 mm wide × 0.5 mm deep, raised rivets at least 2 mm diameter × 0.5 mm proud, recessed fastener wells at least 3 mm diameter and real panel gaps at least 0.8 mm. |

Only rear/bottom access and pod-cap seams should be real unless another split is justified by assembly or service. Cosmetic panel lines and rivets should remain integral features.

The removable front carrier in [HEAD-CAD-01](decisions.md#head-cad-01--construction-and-repeated-disassembly) is a service-justified split under that existing rule. Detail it for repeatable reassembly rather than introduce further cosmetic joints.

## Added requirement

| ID | Requirement |
|---|---|
| CAD-04a | Provide a C2 flashing and recovery path in the sealed head, in addition to the CAD-04 display path. The selected Waveshare ESP32-S3-Zero has **no USB-to-UART bridge**: flashing requires native USB with the BOOT strapping pin (GPIO0) held, so the head needs either accessible USB-C and BOOT/RESET actuation, or a defined wire-flashing break-out to the CAD-05 separable boundary. |

**Added 2026-09-07**, following the C2 module selection recorded in CTRL-04 and [`control-topology-options.md` §6.3](../../../../01-system/control-topology-options.md). CAD-04a extends CAD-04 rather than superseding it; both paths must exist. A sealed head with no C2 recovery path is a build failure, not a service inconvenience.

## Other governing inputs

The [dimensional baseline](../../../../01-system/dimensional-baseline.md) owns the head envelope and component placement. The [material/finish/mass decision](../../material-finish-mass-decision.md) owns PLA, real visible fasteners and the finish process. The [head decision register](decisions.md) owns first-layout connection and fitting choices. Their scope and evidence status remain distinct.

Changes to CAD-01…CAD-06 and CAD-04a must retain traceability to the material decision and propagate to the layout, mass capture and applicable prototype checks.
