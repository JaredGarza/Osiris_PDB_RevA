> HISTORICAL SNAPSHOT — superseded for readiness decisions by `docs/REV-A-READINESS.md`
> (project-relative path). Includes unvalidated claims about maximum load, fuse coordination,
> clamp margin and/or earlier wiring. Use the current schematic and fresh audit results.

# Osiris PDB Rev A — derived requirements

Date: 10 September 2026. Continues `calculate_power.py` / `calculations.json`.

Sources: the user's saved `Osiris_PDB_RevA.kicad_sch`, the supplied `OsirisRevA (1).zip`
Altium archive (SHA-256 manifest recorded in `calculations.json`), and the manufacturer
datasheets in `Datasheets/`. Every number below is either measured off those files or
cited to a datasheet page. Assumption-derived numbers are labelled as such.

This document records requirements only. It does not change the schematic.

> HISTORICAL / SUPERSEDED: several conclusions below are incorrect or conditional.
> See [September 15 review](../PDB-ELECTRICAL-REVIEW-20260915.md): WXNV is package
> quantity, interrupt rating is 1000 A, current fuse data lists 31 A2s for 4 A,
> moderate overloads can be cleared by the fuse, and neither 2.22 A nor the
> nominal inrush estimate is a measured maximum. Gate drive and hot-swap
> assumptions below must not be reused as current approval.

---

## 1. Load requirement

The Osiris board is the only load. Its converted input power is built from rail
ceilings, not measurements:

| Quantity | Value | Basis |
|---|---|---|
| +5V0 rail | 5.164 V nominal | Osiris feedback divider 12 k / 2.2 k |
| +3V3 rail | 3.307 V nominal | Osiris feedback divider 47 k / 15 k |
| Rail load ceiling | 2.5 A on +5V0, 2.0 A on +3V3 | **Assumption** — conditional ceiling, not measured |
| Rail power | 19.52 W | computed |
| Conversion efficiency | 85% | **Assumption** |
| PDB housekeeping | 0.10 W | **Assumption** (U2 + U3 + U4) |
| Converted input power | 23.07 W | computed |

Battery-side current, including the 75 mΩ aggregate path resistance assumption
(wire + XT60 contacts + board):

| Battery voltage | Input current | Path drop | Path loss |
|---|---|---|---|
| 16.8 V (full) | 1.38 A | 104 mV | 0.14 W |
| 14.8 V (nominal) | 1.57 A | 118 mV | 0.19 W |
| 12.0 V (3.0 V/cell) | 1.95 A | 146 mV | 0.28 W |
| 10.56 V (PDB UV trip) | **2.22 A** | 166 mV | 0.37 W |

**R1 — Design maximum continuous input current is 2.22 A**, occurring at the
undervoltage trip point. Everything downstream is sized against this figure.

Of the 7 W Orin Nano profile, only 1.36 A of the 2.5 A +5V0 ceiling is the module
itself; the remainder is Osiris electronics and peripherals.

---

## 2. Voltage window and coordination with Osiris

| Threshold | PDB (this board) | Osiris LM73100 |
|---|---|---|
| Undervoltage | 10.56 V nominal (10.21 – 10.93 V) | 7.91 V on / 7.19 V off |
| Overvoltage | 18.68 V nominal (18.04 – 19.33 V) | 27.70 V off / 25.16 V recover |

PDB tolerance band is the ±1% resistor corner sweep on R1/R2/R3 combined with the
LTC4368's 492.5 – 507.5 mV comparator spec.

**R2 — The PDB window sits strictly inside the Osiris window in both directions, so
the PDB always trips first.** Even at the worst corner, PDB OV (19.33 V) is 5.8 V below
Osiris OV (25.16 V recover), and PDB UV (10.21 V) is 2.3 V above Osiris UV (7.91 V).
Coordination is correct; no threshold change is required.

**R3 — The PDB undervoltage trip is not battery protection.** 10.56 V is 2.64 V/cell,
below the 3.0 V/cell LiPo limit. This is deliberate: a propulsion current sag must not
drop the flight controller. Cell protection is PX4's responsibility.

---

## 3. Overcurrent protection chain

Three elements act in sequence. Their separation is what matters.

**Element 1 — LTC4368 electronic breaker.** 50 mV forward sense threshold across
R5 = 5 mΩ gives a **10 A forward trip**; the LTC4368-**1** option gives −50 mV reverse,
so also 10 A reverse. Fault propagation delay is 8 µs typical. This is 4.5× the 2.22 A
design maximum.

**Element 2 — auto-retry.** C3 = 100 nF on RETRY at 5.5 ms/nF gives a **550 ms
cool-down**, during which the internal timer charges/discharges C3 31 times. RETRY is
not grounded, so the part auto-retries rather than latching off.

**Element 3 — F1 blade fuse.** Backup only. From the Littelfuse 297 time-current
curves, at 10 A a 4 A MINI opens in roughly 0.4 – 1 s and a 5 A MINI in roughly
1 – 3 s. Both are more than 50,000× slower than the 8 µs breaker.

**R4 — The fuse can never be the primary overcurrent element.** For any fault the
MOSFETs can interrupt, the breaker acts first by five orders of magnitude. F1 only ever
operates when the MOSFETs *cannot* interrupt: a shorted-FET failure, or a short on
VBAT_FUSED upstream of Q1. Its rating must therefore be chosen to protect the battery
wiring and the board, not the load.

Verified Littelfuse 297 data (datasheet page 2, `Datasheets/Littelfuse_297_MINI.pdf`):

| Part | Rating | Typ. voltage drop | Cold resistance | I²t |
|---|---|---|---|---|
| 0297003 | 3 A | 153 mV | 33.75 mΩ | 9.4 A²s |
| 0297004 | 4 A | 121 mV | 23.48 mΩ | 17 A²s |
| 0297005 | 5 A | 129 mV | 17.75 mΩ | 25 A²s |

Note: an earlier web summary quoted 37 A²s for the 5 A part. The datasheet says
**25 A²s**. Use the datasheet.

Temperature rerating (datasheet page 2 curve): 100% of rating at ≈ +20 °C, ≈ 110% at
−40 °C, ≈ 85% at +125 °C. The manufacturer's *continuous-duty* derating guidance lives
in the separate fuse selection guide, which is behind a 403 and could not be archived;
the widely applied convention is 75% of rating for continuous load.

Sizing against R1 (2.22 A) using the 75% convention:

| Option | 75% continuous | Margin over 2.22 A | Verdict |
|---|---|---|---|
| 3 A | 2.25 A | 1.01× | **Reject** — no margin |
| 4 A | 3.00 A | 1.35× | Valid; tighter wire protection, 17 A²s let-through |
| 5 A | 3.75 A | 1.69× | Valid; more nuisance margin, 25 A²s let-through |

**R5 — 3 A is rejected. Both 4 A and 5 A satisfy every constraint.** The choice is a
tradeoff between fault let-through energy and nuisance margin, and is recorded as
decision D1 in §8.

**R6 — Interrupting rating is adequate.** The `.WXNV` suffix on the specified MPN is
the 3000 A interrupting version, which covers the prospective short-circuit current of
a 4S LiPo.

---

## 4. Inrush and turn-on

The LTC4368 ramps the MOSFET gates with a 35 µA charge pump. Source-follower action
bootstraps Cgs out of the ramp, and Cgd is 96 pF max, so the ramp rate is set by C1:

- Gate ramp = 35 µA / 5.6 nF = **6.25 kV/s**
- Ramp time = 16.8 V / 6.25 kV/s = **2.7 ms**
- Load capacitance = Osiris 120 µF + C4 10 µF + C2 1 µF = **131 µF** (nominal, not
  DC-bias derated)
- Inrush = 131 µF × 6.25 kV/s = **0.82 A**, on top of load current

**R7 — Inrush is a non-event.** 0.82 A is below the 2.22 A design load, 12× below the
breaker, and its I²t of ≈ 0.0018 A²s is four orders of magnitude below the fuse's
17 A²s. No nuisance opening, no SOA concern during the 2.7 ms ramp.

A 32 ms turn-on debounce (t_D(ON)) precedes every connection, plus an 800 µs startup
delay out of shutdown.

---

## 5. Hot-plug: CHOTSWAP is not required

The LTC4368 datasheet offers an optional 4.4 – 6.8 nF CHOTSWAP across the MOSFET
gate–source terminals to stop drain-gate coupling from enhancing the FETs during a hot
insertion. Checking whether this design needs it:

- ISC015N06NM5LF2 Crss = 55 pF typical, **96 pF maximum**
- Gate node holds C1 = 5.6 nF
- A 16.8 V hot-plug step couples 16.8 V × 96 pF / (96 pF + 5600 pF) = **0.28 V**
- VGS(th) = 2.25 V minimum, 3.0 V typical

**R8 — No CHOTSWAP is needed.** The coupled 0.28 V is 8× below the minimum gate
threshold. The datasheet's recommendation is aimed at parts with far higher Crss than
this one, at far higher bus voltages. Do not add the part.

---

## 6. Gate network deviates from datasheet Figure 11

Datasheet Figure 11 topology: LTC4368 GATE pin → CGATE to GND, then RGATE 22 k in
series to the MOSFET gates, with an optional MBR0540 across RGATE (cathode to the CGATE
side).

As built: the GATE pin ties **directly** to both MOSFET gates, and R4 (22 k) + C1
(5.6 nF) form a series RC from that node to GND.

Consequences:

- Turn-on ramp rate and turn-off speed are both correct as built. The 60 mA fast
  pull-down acts directly on the FET gates.
- **R9 — RGATE is not performing its documented function.** The datasheet states
  "to avoid large currents when the reverse voltage is hot plugged, set RGATE to 22k".
  With R4 out of the series path there is no series impedance between the GATE pin and
  the FET gates during a reverse insertion. GATE absolute maximum is −40 V, and
  datasheet Figure 12 shows a −20 V insertion ringing significantly past −20 V from
  wire inductance alone. At 4S the nominal reverse case is −16.8 V, so margin exists but
  the documented mitigation is absent.
- Moving R4 into the series position **requires** adding the MBR0540. Without it the
  fault turn-off degrades from 8 µs to 22 kΩ × 13.8 nF ≈ **300 µs**, which would defeat
  the breaker. This is a three-part change or none at all.

Recorded as decision D2 in §8.

---

## 7. Thermal and voltage-drop budget at 2.22 A

| Element | Resistance | Drop | Loss | Margin |
|---|---|---|---|---|
| F1, 4 A option | 23.48 mΩ | 52 mV | 116 mW | — |
| F1, 5 A option | 17.75 mΩ | 39 mV | 87 mW | — |
| Q1 + Q2 | 2 × 1.55 mΩ max | 7 mV | 15 mW | — |
| R5 shunt | 5 mΩ ±1% | 11 mV | 25 mW | 2 W part, **81×** |
| **PDB total (5 A fuse)** | **≈ 28 mΩ** | **≈ 57 mV** | **≈ 127 mW** | — |

**R10 — The 75 mΩ path resistance assumption is self-consistent.** The board accounts
for only ≈ 28 mΩ of it; the balance is wire and XT60 contact resistance, which is
plausible for the specified pigtails.

**R11 — Gate enhancement is below the RDS(on) test condition but immaterial.** The
LTC4368 delivers 7.2 V minimum / 8.7 V typical of GATE−VOUT at VIN ≥ 12 V, whereas
RDS(on) ≤ 1.55 mΩ is specified at VGS = 10 V. Even at 3× the specified resistance the
conduction loss at 2.22 A stays under 50 mW. No action.

**R12 — R5 Kelvin wiring is verified correct.** Footprint `OH_FC4L64_OHM` places pads
1/4 as the 5.4 mm current electrodes and pads 2/3 as the 0.71 mm sense electrodes,
matching the FC4L64 (6432 metric, 2 W) drawing. The netlist puts the current path on
1→4 and takes SENSE from the upstream pad 2 and VOUT from the downstream pad 3, giving
the correct forward sense polarity.

---

## 8. Telemetry and digital interface

### 8.1 I²C address — resolved, no clash

Searched all 434 footprints in the Osiris archive:

- PDB U2 INA228: A0 = A1 = GND → address **0x40**
- Osiris IC11 INA228: A0 = A1 = +3V3 → address **0x45**, and it sits on FMU_I2C4

**R13 — No address conflict exists**, and the question is moot anyway because FMU_I2C4
never leaves the Osiris board (see §8.3).

### 8.2 INA228 configuration

**R14 — Use ADCRANGE = 1 (±40.96 mV).** With R5 = 5 mΩ this gives 8.19 A full scale and
a 15.6 µA current LSB. Full scale sits below the 10 A breaker, so a trip event reads as
saturated — acceptable, since the breaker handles the fault and the exact peak is not
needed.

**R15 — The monitor does not survive a trip.** U3's input is PDB_VOUT, downstream of
the FETs, so PDB_3V3, U2 and U4 all lose power when the breaker opens. The LTC4368's own
FAULT output is powered from VBAT_FUSED and does survive. U4 is a 74AUP part with
power-down (Ioff) protection, so its output will not load an external pull-up while
unpowered. Feeding U3 from VBAT_FUSED instead would keep telemetry alive through a trip
at the cost of ≈ 0.65 mA of permanent battery drain; recorded as decision D4.

**R15a — What D4 actually buys, stated precisely.** Osiris is powered only through
PDB_VOUT, so it also loses power on a trip and cannot read the INA228 during one. The
real benefit is narrower than "telemetry survives": with U3 on VBAT_FUSED the INA228
keeps its configuration and its accumulated charge/energy registers across the 550 ms
retry cycle instead of resetting to defaults, so Osiris does not have to reconfigure the
monitor and lose the accumulators on every retry. It also means PDB_3V3 is live whenever
a battery is connected, which is what makes bench probing of the monitor possible with
the output off.

### 8.3 J2 cannot connect to Osiris Rev A as drawn

This is the most significant finding. Searching every Osiris connector:

- **FMU_I2C4** — Osiris's own INA228 bus — is internal only. It reaches U10 (STM32H743)
  and IC11 and nothing else. It is not available to the PDB.
- Exactly two external I²C buses exist, both with 12 kΩ pull-ups to Osiris **+3V3**
  (R74/R75, R76/R77):

| Osiris connector | Part | Pinout |
|---|---|---|
| **J28** | BM04B-GHS-TBT (4-way) | 1 +5V0_PROT, 2 FMU_I2C1_SCL, 3 FMU_I2C1_SDA, 4 GND |
| **J35** | BM06B-GHS-TBT (6-way) | 1 +5V0_PROT, 2 FMU_UART8_TX, 3 FMU_UART8_RX, 4 FMU_I2C2_SCL, 5 FMU_I2C2_SDA, 6 GND |

- **No GH connector on Osiris exposes +3V3 or a spare GPIO.**

Consequences:

**R16 — The PDB correctly omits I²C pull-ups**, and its 3.3 V I²C levels are compatible
with Osiris's 3.3 V bus. The existing schematic note is right on this point.

**R17 — The existing schematic note is wrong about the status lines.** It says
"INA_ALERT_N and PDB_FAULT_N each require a 10 kΩ pull-up to Osiris +3V3". No cable to
Osiris Rev A can deliver +3V3, and neither signal has a GPIO to land on. As drawn, these
two open-drain outputs have no destination.

**R18 — The current J2 pinout (1 GND, 2 SDA, 3 SCL, 4 ALERT, 5 FAULT, 6 NC) matches
neither Osiris connector**, so it mandates a custom cable and still leaves two signals
unterminated. Options are recorded as decision D3.

---

## 9. Decisions required

| ID | Decision | Recommendation |
|---|---|---|
| **D1** | F1 final rating: 4 A or 5 A (§3) | **4 A** (0297004.WXNV) — 1.35× over the 2.22 A ceiling, still 10⁴× above inrush I²t, and reduces fault let-through from 25 to 17 A²s |
| **D2** | Gate network: rework to datasheet Fig. 11 (R4 in series + MBR0540 across it), or leave as built (§6) | **Rework** — restores the documented reverse-insertion mitigation; must include the diode |
| **D3** | J2 interface (§8.3) | **Re-pin to a 4-way BM04B-GHS-TBT matching Osiris J28 1:1** (1 = NC, 2 = SCL, 3 = SDA, 4 = GND) — yields a stock cable with no firmware constraint |
| **D4** | Feed U3 from VBAT_FUSED so telemetry survives a trip (§8.2) | Optional; costs ≈ 0.65 mA standing battery drain |
| **D5** | Input transient clamp on VBAT_FUSED | Optional. Must be **bidirectional** — see below. **SMAJ24CA**: 24 V standoff, 26.7 – 29.5 V breakdown, 38.9 V clamp at 10.3 A, 400 W |

### D5 must be bidirectional

A unidirectional part (SMAJ24**A**) would forward-conduct the instant the battery is
connected backwards, shorting the pack through F1 and destroying the reverse-battery
tolerance that the LTC4368 and the back-to-back MOSFETs exist to provide. The clamp
must block in both directions.

SMAJ24**CA** satisfies every constraint:

- 26.7 V minimum breakdown is above the 19.33 V worst-case OV corner, so it never
  conducts in normal operation or at the OV trip point
- 38.9 V clamping voltage is well below the 60 V V(BR)DSS of Q1/Q2 and the LTC4368's
  100 V VIN rating
- 24 V standoff in the reverse direction blocks a −16.8 V reversed pack

The **SMCJ17CA** named in `DESIGN-SPEC.md` is bidirectional but the wrong voltage: its
18.9 – 20.9 V breakdown overlaps the 18.04 – 19.33 V OV corner, so it would conduct at
the very threshold the OV comparator is set to.

D3 alternatives, for completeness:

- **Keep 6-way, re-pin to match Osiris J35 1:1** (1 NC, 2 ALERT, 3 FAULT, 4 SCL,
  5 SDA, 6 GND). Stock 6-wire cable, but pins 2/3 land on UART8_TX/RX. Safe only while
  PX4 leaves UART8 unconfigured; if UART8_TX is ever enabled it drives against the PDB's
  open-drain outputs. Requires a firmware lock.
- **Keep the current pinout and accept a custom cable** carrying only GND/SDA/SCL,
  leaving ALERT/FAULT for a future Osiris revision.

If D3 drops the status lines from the connector, U4 and R10 no longer drive anything
external. Keeping them wired to a test point costs two parts and preserves the option
for a later Osiris revision.

---

## 10. Housekeeping finding

**`DESIGN-SPEC.md` no longer describes this board.** It specifies a four-output ESC
distribution board with an 80 A motor bus, D1/D2 SMCJ17CA clamps, a 1000 µF bulk
capacitor and no LTC4368. The built schematic is a single protected 2.2 A feed to
Osiris with an LTC4368 breaker and INA228 telemetry. The two documents conflict on
current rating, topology, part selection and connector count. It should be rewritten
against this document or explicitly retired, otherwise it will keep being cited as a
requirement — as its SMCJ17CA selection already was in D5.

---

## 11. Verification plan

Nothing above substitutes for bench measurement. Before Osiris is connected:

1. Confirm the actual Orin Nano nvpmodel profile in use, and measure real +5V0 and
   +3V3 rail currents. Replace the §1 ceilings with measured values.
2. Measure the PDB input current at 16.8 V, 14.8 V and 12.0 V into a dummy load and
   confirm it tracks the §1 table.
3. Scope PDB_VOUT on turn-on and confirm the 2.7 ms ramp and ≤ 0.82 A inrush.
4. Trip the breaker into a dummy short; confirm the 8 µs turn-off, the 550 ms retry
   period, and that F1 survives.
5. Confirm UV and OV trip points against §2 with a bench supply sweep.
6. Verify polarity end-to-end on the physical J1 and J3 pigtails before any Osiris
   connection.
7. Measure the board's series resistance and confirm it against the ≈ 28 mΩ of §7.
8. Confirm the INA228 answers at 0x40 and that its readings agree with a reference
   meter at 0.5 A, 1 A and 2 A.
