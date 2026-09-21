# RP-05 audio path families

| Field | Value |
|---|---|
| Status | Comparison only. **No family selected.** Product names are class examples already used in RP-02, not buys |
| Created | 2026-09-21 |
| Rule | Score a family against [`audio-requirements.md`](audio-requirements.md). Do not add a fifth family to avoid a miss. Do not treat a kit that “works on the bench” as ADR-11 |

RP-02 already named two unselected leads: an AC108-class I²S TDM codec HAT, and an XMOS-class USB array. This file adds the playback-binding axis those leads left implicit, and records how each binding sits against `AR-*`.

## 1. Families

| ID | Capture host interface | Playback host interface | What it is |
|---|---|---|---|
| `AP-TDM` | Pi I²S/TDM on GPIO18–21 into a multi-channel codec; discrete PDM (or codec-native) capsules on the body | Same codec DAC, or a sibling I²S DAC on the same clock tree, into a class-D amp and the reserved 50 mm speaker | One hardware audio timebase on C0's I²S reservation |
| `AP-USB` | USB microphone array (onboard DSP possible) | Separate analog/I²S amp, or a second USB playback device | Capture clock lives on the USB device; playback may not |
| `AP-USB-IO` | One USB audio device that exposes both capture and playback | Same device into the body amp/speaker or its own transducer | Shared USB clock; still USB scheduling |
| `AP-SPLIT` | Codec/TDM capture as in `AP-TDM` | Unrelated USB or analog dongle for playback | Explicitly splits the clocks; included as a **negative** comparison |

`AP-SPLIT` exists so a convenient “USB speaker now, codec later” kit cannot quietly become the architecture.

HAT vs USB power attribution follows the ledger: codec-class peak `E` on `PB-AUDIO-IN`; USB-array class moves ~0.5–1 W onto `PB-COMPUTE` and must declare no-back-power.

## 2. Fit against requirements

`Y` = can meet if designed to; `?` = must be proven, historically the weak point; `N` = structurally poor for that `AR`.

| Requirement | `AP-TDM` | `AP-USB` | `AP-USB-IO` | `AP-SPLIT` |
|---|---|---|---|---|
| `AR-01` four body mics | Y | Y if the array is four-ch and body-mounted, not a head-set | Y same | Y |
| `AR-02` not in head/ears | Y | N if the SKU is a bar/headset; Y if capsules are still body-port | Y if body-mounted | Y |
| `AR-03` synchronized channels | Y | Y onboard; host-side USB jitter is a timestamp problem | Y onboard | Y on capture only |
| `AR-05` Pi 5 has no 4-ch PDM | Y — this is the native answer | Y — avoids Pi PDM | Y | Y |
| `AR-06` GPIO18–21, no UART steal | Y, and it **uses** the reservation | Y — leaves GPIO18–21 free for something else; must not then claim them | Y | Y |
| `AR-07` no back-power / safety coupling | ? HAT 3V3/5V path | ? USB VBUS when C0 is off | ? same | ? both |
| `AR-10` always-on listen | Y low | ? USB DSP idle power, enumeration | ? | Y capture / ? play |
| `AR-13`/`F-21` missing device | Y ALSA/device node | Y USB disconnect | Y | two failure surfaces |
| `AR-50` simultaneous duplex | Y | ? unless playback clock is locked to capture | Y | N for AEC-quality duplex |
| `AR-51` recoverable play↔cap time | Y if one clock tree | ? two domains | Y if the device exposes both | N |
| `AR-53` self-playback ≠ wake | Y with echo ref | ? if no echo reference to C0 | Y if the device exposes a ref or loopback | N honest AEC |
| `AR-60` speaker–mic coupling | Y — uses reserved cavity | ? if the USB array brings its own speaker | ? own transducer vs reserved 50 mm | Y speaker / Y mics, uncoupled clocks |
| `AR-61` cooler noise | independent of family; packaging | independent | independent | independent |
| `AR-64` rigid body geometry | Y discrete capsules on a subframe | ? commercial bars have their own geometry | ? | Y |
| CAND-01 DOA (not Core) | later software | often onboard; must not force Core to depend on it | same | later software |
| Kernel/driver risk on Pi 5 | named in RP-02 (AC108-class) | typically UAC, lower kernel risk | UAC | both |

Leaving GPIO18–21 unused (`AP-USB`) is allowed. Using them for a non-audio function still needs a `CA-06` change request.

## 3. What would reject a family later

These are selection **rules**, not a selection.

1. Cannot mount four capsules on the Layout 02 body ports (`AR-01`/`AR-02`/`AR-04`).
2. Cannot listen in quiet sleep without spinning the camera or a cloud session (`AR-10`/`AR-20`).
3. Mute-to-play or mute-to-listen (`AR-50`).
4. No recoverable relationship between speaker samples and mic samples when both are active (`AR-51`), unless a later measured echo/false-wake test shows the family still meets `AR-53` without it — that exception must be written before the test, not after.
5. UART collision, USB back-power into an off SBC, or speaker current through a safety return (`AR-06`/`AR-07`/`AR-32`).
6. Character playback that is English TTS (`AR-34`).
7. A kit speaker that abandons the reserved cavity without an RP-06 envelope revision (`AR-31`).

Onboard USB DOA is **not** a reason to prefer `AP-USB` for Core. It is a reason that family remains interesting for ADR-13, which this slice does not open.

## 4. Stand-in vs path

| Thing | Proves | Does not prove |
|---|---|---|
| RP-04 virtual `AudioPlay` callback | Identity, stop, stale epoch, underrun deny | Any `AR-01`–`AR-07` or `AR-50`–`AR-65` |
| GPIO / host beep | IR-06 scheduling | Enclosure, SPL, echo, contamination |
| Laptop mic + phone speaker | NLU software can be developed | Body array, Pi 5 interface, ADR-11 |
| One family on a bench, cooler off, no drive | Exploratory `E` | Scored contamination or G01 |

## 5. Disposition

No `AP-*` is selected. No purchase is implied. RP-02's candidate register stays unselected. A later slice may pick a family by applying §3 to measured or datasheet evidence; this file will then record the pick in [`decision.md`](decision.md), not by rewriting the table into a winner.
