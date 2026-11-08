# PCB-09 rev B: draft fabrication outputs

**Do not order yet.** This branch's routed board passes KiCad Nightly DRC with 0 violations, 0 unconnected items and 0 schematic parity issues. The exported STEP passes final-v1 fit 8/8, mount 7/7 and static integration with no collisions. The received #2813 measurements, actual Pi image checks and populated continuity, power and pull tests remain release gates.

`layout_pcb09.py --export` generated these Gerber, drill, position, CPL and BOM files after the CAD fit. All use the same bottom-left board origin. The outline is 89 × 22.7 mm overall with a stepped +X extension; the 3.3 V-side service interface uses J6 GH6, pins 1–6: 3V3, SDA, SCL, GND, BTN_SENSE, PWR_OFF. C5 is DNP and is absent from the assembly BOM and CPL.

J6 must be mated before the tray goes in. The checked 3 mm lead corridor shifts to world Y 20, runs rearward at Z 118, and reaches the buffer reserve beside M1; add physical strain relief and pull-test the populated lead. The cable check is a static CAD reserve, not a wire bend or motion test.
