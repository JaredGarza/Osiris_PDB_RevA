# Combined PDB + Osiris Rev A — simulation findings

**Date:** 2026-09-15
**Engine:** LTspice 26.0.2 (**not** PSpice — see *Engine* below)
**Scope:** Osiris PDB `A-P2-DRAFT` + Osiris flight computer **Rev A**, joined by an XT60 harness.

> This is a **screening simulation**, not hardware qualification. Several devices
> are datasheet-fitted surrogates. Read `model_manifest.json` before quoting any
> number here. Nothing below certifies SOA, thermal, EMC or fuse-clearing behaviour.

---

## Engine: PSpice was requested but cannot run here

`C:/Cadence/OrCADX_25.1/tools/bin/pspice.exe /r <deck>` launches the **OrCAD X
Standard GUI** and blocks indefinitely — confirmed by process inspection
(`MainWindowTitle = "OrCAD X Standard"`, no `.out` written, no license daemon
configured). There is no batch path on this machine.

LTspice 26.0.2 was used instead. It is the engine that produced every prior
result in `Simulation/`, and the vendor models on disk (`LTC4368-1.sub`,
`LT3010.lib`) are LTspice-format. **The decks use LTspice-only syntax and will
not run under PSpice without translation.**

---

## What was built

| File | Contents |
|---|---|
| `models/pdb_devices.lib` | ISC015N06NM5LF2 VDMOS, SMAJ24CA, MBR0540, INA228 stub, 74AUP1G07 |
| `pdb/pdb_ap2.lib` | `PDB_AP2` — all 42 schematic components, transcribed 1:1 from `final.net.xml` |
| `osiris/osiris_reva.lib` | `OSIRIS_REVA` — input path, both LM73100 eFuses, both AP64501 bucks, protected-5V switch, bootstrap sequencer, aggregated digital loads |
| `combined_*.cir` | Startup, faults, reverse polarity, brownout, UV-stability decks |

PDB connectivity is exact. Osiris connectivity is traced to
`docs/osiris-power-audit/zip-pcb-pad-nets.json` and the Altium-derived JSONs;
per-designator provenance is in the manifest.

### Corrections to earlier project assumptions

Three things in the older notes are **wrong for Rev A** and were corrected here:

- **Osiris has no fuse, no discrete reverse-protection FETs, and no input TVS.**
  All input protection is internal to the LM73100s. The `F1`/`Q1`/`Q2`/`SMAJ24CA`
  parts discussed in `requirements-20260910.md` are **PDB** parts.
- **USB is not a power source.** `+VBUS_IN` reaches only `IC1 74LVC1T45` as a
  1.8 V VBUS-present detect. The real alternate source is the **J17 DC barrel
  jack** into `U22`. Any "USB 5 V input" scenario is not a Rev A behaviour.
- **U21's dV/dt pin is unconnected** — there is no Osiris dV/dt capacitor. The
  5.6 nF in `calculate_power.py` is the PDB's `C1` on the LTC4368 gate.

---

## Verified good

**Cross-validation against the project's own budget.** Simulated steady-state
input current, with no fitting:

| Pack | Simulated | `calculations.json` | Error |
|---|---|---|---|
| 16.8 V | 1.389 A | 1.3816 A | 0.5 % |
| 14.8 V | 1.579 A | 1.5711 A | 0.5 % |
| 12.0 V | 1.957 A | 1.9460 A | 0.6 % |

(Figures are from the final verification re-run. They are an independent check:
the Osiris model was built from CAD connectivity, not fitted to this table.)

**Protection thresholds** — measured vs. hand-calculated from the dividers:

| | Measured | Calculated |
|---|---|---|
| UV rising | 11.16 V | 11.09 V |
| UV dropout | 10.56 V | 10.56 V |
| OV trip | 18.69 V | 18.68 V |
| OV recovery | 17.68 V | 17.74 V |

For a 4S LiPo (12.0–16.8 V) this leaves 2.1 V of headroom below OV and 1.44 V
above UV dropout.

**Startup sequencing** (14.8 V): PDB output at **35.0 ms** (LTC4368 spec
t<sub>D(ON)</sub> = 32 ms typ) → Osiris UVLO crossed at 35.7 ms → +5V0 at
37.9 ms → +5V0_PROT at 87.8 ms → +3V3 at 89.4 ms. Inrush peaks at
**2.90 A** (3.09 A at a full pack), below both the 4 A fuse and the 10 A breaker.

**Housekeeping rail:** 3.2825 V → 3.2793 V across a 12 → 16.8 V input swing.
Note this is **3.28 V, not 3.30 V** (R11/R12 = 1k58/1k0). Within spec for both
the INA228 (2.7–5.5 V) and the 74AUP1G07 (0.8–3.6 V) — not a defect, but the
silkscreen/docs should not claim 3.3 V.

**Reverse battery** (−14.8 / −16.8 / −25 V): Osiris sees **−47 to −61 mV**,
total draw **< 1 mA**, gate held at −0.13 V, and all rails come up normally once
polarity is corrected. The TVS does not conduct below its 26.7 V breakdown, so
the FETs take the full reverse voltage — fine against their 60 V rating.

**Hard short at the Osiris input:** breaker trips essentially instantly
(I²t = 8.3 × 10⁻⁹ A²s, versus the fuse's 17 A²s melting energy) and the system
**self-recovers in ~400 ms** with no intervention — PDB back at 1.452 s after
the short cleared at 1.100 s, all rails nominal by 1.504 s.

**OV and UV excursions:** clean disconnect and clean recovery in both directions.

**Brownout is stable.** The Osiris bucks are constant-power loads, so current
rises as the pack sags — but the loop does not run away. Current climbs
monotonically to ~2.6 A and the PDB cuts cleanly at the UV threshold.

---

## Findings

### 1. Sustained non-recoverable retry loop with a high-impedance pack — most significant

With a **500 mΩ** pack whose open-circuit voltage sits in roughly the
**11.2 – 11.8 V** window, the system enters a restart loop that **never exits**:

- unloaded, VBIN sits at 11.6 V — above the 11.16 V UV **rising** threshold, so
  the LTC4368 begins to turn on
- after the **32 ms** gate turn-on delay the output rises to ~9.2 V and the
  Osiris bucks begin drawing (peak **2.32 A**)
- the 500 mΩ pack sags **1.16 V** → VBIN = 10.44 V, below the 10.56 V UV
  **falling** threshold → gate collapses, rail drops to ~0.90 V
- load disappears, VBIN springs back to 11.6 V, and the cycle repeats
- **+5V0 never exceeds 1.81 V, so the Jetson never boots**
- average draw is only **5.2 mA**, so nothing overheats — the aircraft is
  silently bricked rather than either running or cleanly off

**Mechanism:** this is a UV-threshold relaxation oscillation paced by the
LTC4368's gate turn-on delay — measured period **34 ms** against the datasheet
t<sub>D(ON)</sub> of 32 ms typ. It is *not* the overcurrent retry timer, which
would be ~545 ms with C3 = 100 nF.

Confirmed over four **disjoint** windows (3–4 s, 6–7 s, 9–10 s, 11–12 s) of a
12 s run, all bit-for-bit identical, with restart attempts still firing at 11.98 s.

**Condition:** the window opens when `I_trip × R_pack` exceeds the UV
hysteresis (≈600 mV input-referred). At ~2.3 A that needs **R_pack ≳ 260 mΩ**.
Healthy packs (20–50 mΩ) are unaffected — verified stable. 200 mΩ is just inside
the safe side. The risk is a cold, aged, or badly-connected pack, or added
harness/connector resistance.

**Worth considering:** more UV hysteresis, or a latch-off-after-N-retries policy
so the failure is loud rather than silent.

### 2. Overcurrent coverage gap between ~4 A and ~10 A

The fuse is 4 A; the LTC4368 breaker trips at 50 mV / 5 mΩ = **10 A**.
Sweeping fault resistance:

| Fault R | Input peak | I²t | Result |
|---|---|---|---|
| 10 mΩ | 234 A | 0.006 A²s | breaker trips |
| 100 mΩ | 97 A | 0.009 A²s | breaker trips |
| 500 mΩ | 28 A | 0.059 A²s | breaker trips |
| 1 Ω | 15.5 A | 0.082 A²s | breaker trips |
| **2 Ω** | **8.7 A** | **67.8 A²s** | **never trips** |

At 2 Ω the total is 8.8 A → only **44 mV** across the shunt, under the 50 mV
typical threshold. Nothing trips electronically and the fuse absorbs **4× its
melting energy** slowly (seconds). Against a 1.55 A nominal load, any fault
drawing 5–9 A lands in this gap.

This sits inside the LTC4368's own tolerance band (40–60 mV ⇒ 8–12 A), so a
worst-case-low part *would* trip at 8 A and a worst-case-high part would not —
genuinely marginal, not a clean margin.

### 3. Pack impedance eats usable capacity

Brownout dropout, by pack internal resistance:

| R<sub>pack</sub> | Drops out at (open-circuit) |
|---|---|
| 20 mΩ | 10.68 V |
| 200 mΩ | 11.15 V |
| 500 mΩ | 11.93 V |

A 500 mΩ pack browns out with 11.93 V still on the cells.

### 4. Worst-case current exceeds the documented figure

`requirements-20260910.md` R1 states *"Design maximum continuous input current
is 2.22 A, occurring at the undervoltage trip point."* With a +50 % Jetson
compute transient at the trip point this reaches **2.62–2.70 A** — 18–22 %
higher. Still only ~65 % of the 4 A fuse, but the margin is thinner than
documented. The 2.22 A figure assumes static rail ceilings with no transient.

### 5. Minor / informational

- **PDB 3V3 rail is 3.28 V**, not 3.30 V (see above).
- **U4 `74AUP1G07` output (`/INA_ALERT_N`) goes only to TP6** — open-drain with
  no pull-up and no connector pin. As drawn, the buffered ALERT is unusable.
- **`/PDB_FAULT_N` has no pull-up** — open-drain LTC4368 FAULT floats to TP7.
- **`J2` pin 1 is unconnected**, and there are **no I²C pull-ups on the PDB** —
  the bus depends entirely on the host side.
- MLCC DC-bias derating is significant and is parameterised (`CDERATE`), not
  ignored: C4/C9 are 50 V 1206 X7R at 12–16.8 V bias, C6 is a 10 V part on 3.28 V.

---

## Two bugs found in my own models during verification

Recorded because they affected intermediate results before being fixed:

1. **`DIGILOAD` guard ordering.** The rail-collapse guard was applied before the
   25 ms load ramp, so a dead rail kept being sunk at ~0.46 A and went to
   **−349 V**, making the U4 pass element attempt ~12 kA. Caught by a physically
   impossible recovery voltage. Guard now multiplies the final current.
2. **Hard comparators.** `if()`/`>` in the enable and sequencer logic chattered
   when rails decayed through threshold, collapsing the timestep to ~1e-15 and
   hanging the OV case (5817 tolerance warnings). Smoothed with `tanh`.
   Startup results are unchanged after the fix — verified by re-run.

Also: `.meas INTEG ABS(ddt(...))` edge counting reported **zero** while the
circuit was demonstrably oscillating, and a 1.5 s fault window could not
distinguish "does not recover" from "has not recovered yet". Both were replaced
with direct measurements over disjoint windows.

---

## What this does **not** establish

- The **fuse never opens** in this model. The 17 A²s figure is pre-arcing
  (melting) I²t, not total clearing I²t. No arc energy, clearing time, or
  interrupt behaviour is modelled. Interrupt rating is 1000 A, not 3000 A.
- **No SOA, avalanche or thermal validity.** The 178.7 A short-circuit peak is
  not an SOA demonstration; the MOSFET is a datasheet-fitted surrogate whose
  gm is ~2× high.
- **No buck loop stability / ripple / phase margin** — the AP64501 model is an
  averaged surrogate and the COMP networks are not modelled. AP64501 switching
  frequency and FB reference are unverified; L1/L2 inductance is ambiguous in
  the source CAD (MPN implies 3.3 µH, Altium field says 47 µH).
- **No digital behaviour** on either board — no ADC, I²C, firmware, or the U11
  sequencer's actual program. `TSEQ = 50 ms` is assumed.
- **LM73100 slew rate is unverified** (TI's model is PSpice-encrypted). The
  ~3.4 A Osiris inrush figure rests on the surrogate's `SR = 28100 V/s` default.
- **No tolerance-corner analysis** beyond the parameters explicitly swept.
- Osiris `J24`/`J25` Module Hub pins tap **raw VIN**; external modules can draw
  unbudgeted current that none of this bounds.
