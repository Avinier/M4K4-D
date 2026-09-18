# RP-02 Phase A reference

This directory is an **exploratory host implementation**, not a scored G04/G05 run or a wire-compatible release. `schema.json` is the one source for the provisional C0 Python and C2 C frame codecs. `python3 generate.py` regenerates `codec.py` and `codec.h`. The type numbers and header layout are marked `EXP_ONLY_NOT_REGISTERED`; the registered Part-4 ICD defines message and recovery semantics, and leaves byte layout open.

The generated codecs implement COBS framing, CRC-16/CCITT-FALSE, little-endian envelope fields, a 16-byte C0 boot UUID and session epoch. Payload bytes are opaque: typed payload layouts, hard-limit tables, C3 drive messages and production protocol compatibility remain open. `runtime.py` exercises C0 authority lease, a fresh C2 boot challenge, two-phase arm, heartbeat timeout, queue flush, command expiry at execution, E-stop no-replay and a four-timestamp time model. It is a reference model, not ESP-IDF firmware or a motor-control loop.

Run host checks from this directory:

```sh
python3 generate.py
python3 -m unittest discover -p 'test_*.py' -v
cc -std=c11 -Wall -Wextra -Werror codec_smoke.c -o /tmp/rp02-codec-smoke
/tmp/rp02-codec-smoke
```

No DevKitC serial device was present during this change. TTL loopback, UART edge stamps, timer capture, ESP-IDF watchdog behavior and G05 timing remain to be implemented and measured on the twin. The host tests demonstrate software behavior only.

## Board-role pin map, before GPIO assignment

| Role | C2 Zero installed | C2 DevKitC-1-N8R8 twin | C3 DevKitC-1-N8 |
|---|---|---|---|
| C0 link UART | Dedicated UART TX/RX to external full-duplex differential transceiver; common reference and power-off isolation | Same logical UART, TTL loopback first; GPIO selection is board header only | Dedicated UART TX/RX to separate differential transceiver |
| Safety inputs | E-stop/motor-present, energy status, servo fault where available: direct inputs with safe pulls | Same logical inputs emulated on bench; do not tie to installed harness blindly | E-stop, `ENERGY_OK`, motor-present: direct inputs, not an expander |
| Safety outputs | Watchdog feed after healthy loop; READY passes external watchdog-good; servo transceiver enable defaults off | Same logical functions with test points and inert load | Watchdog feed, qualified READY and driver inhibit; motor I/O awaits RP-03 |
| Service/reserved | Native USB service; GPIO21 LED excluded; GPIO0/3/45/46 strapping excluded for safety | Native USB and USB-UART reserved; RGB LED pin varies by board revision | GPIO19/20 native USB, 43/44 USB-UART reserved; 0/3/45/46 strapping excluded; 35–37 available on N8 |

This is a role map and reservation, **not a carrier pinout**. Physical GPIO assignments for C3 exist as pin map v0.1 and the generated `c3_board_role.h` (`RP03-P4-REG-02`); the carrier PCB still waits on a frozen map. C2 physical GPIO still requires the exact board revision. Preserve at least two unassigned safe GPIO after the map.

## Logging record for exploratory timing

Each append-only event record carries `run_id`, `source`, `event`, `boot_uuid`, `epoch`, `seq`, `raw_local_us` (nullable for C0), `converted_master_us` (nullable while unsynchronized), `receipt_master_us` (nullable), `model_ref_local_us`, `offset_at_ref_us`, `rate_ppb`, `uncertainty_us`, `model_valid`, `firmware_hash`, `config_hash`, `health` and `detail`. Keep raw and converted stamps together; never replace a missing stamp with zero. `CLOCK_MONOTONIC` drives C0 stamps. UTC belongs once in the run metadata. The immutable ring format and pre-run write check still need implementation before scored work.

## Next hardware execution

1. Freeze a board revision and assign safe GPIO in one board-role header, then flash the same C2 target to the Zero and DevKitC twin.
2. On the twin, run TTL loopback using these exploratory frames; capture first-byte RX and pre-FIFO TX edge stamps and export the logging record above.
3. Fit the time model from at least three valid exchanges, inject stale frames, CRC damage, link removal and reset; record behavior without scoring.
4. After the byte layout and numeric G04/G05 thresholds are registered, repeat on the differential breakout and representative harness as scored runs.
