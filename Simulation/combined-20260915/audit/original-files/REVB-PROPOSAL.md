# PDB Rev-B candidate — proposed changes, simulated and verified

**Status: SIMULATION ONLY. The KiCad schematic has NOT been touched.**
This is a proposal for sign-off. As-built model (`pdb/pdb_ap2.lib`) is unchanged
so the two can be compared directly.

Candidate model: `pdb/pdb_ap2_revb.lib`. Engine LTspice 26.0.2.

---

## Bill of changes

| Ref | As-built | Rev-B | Why |
|---|---|---|---|
| `R1` | 2M0 | **1M0** | UV divider top, rescaled for the new hysteresis network |
| `R2` | 43k2 (UV→OV) | **2M0, REWIRED to VIN→OV** | OV gets its own divider |
| `R3` | 56k2 | **54k9** | OV divider bottom, keeps the 18.7 V trip |
| `R5` | 5 mΩ | **8 mΩ** | Lowers breaker from 10 A typ to 6.25 A typ |
| `F1` | 4 A (0297004) | **5 A (0297005)** | Re-coordinates fuse against the new breaker |
| — | — | **+`RUVB` 47k**, UV→GND | New UV divider bottom |
| — | — | **+`RH` 20M**, GP→UV | UV hysteresis feedback |
| — | — | **+`RPUF`/`RPUA` 10k** to 3V3 | Pull-ups for FAULT and ALERT |
| — | — | **+`RPUC`/`RPUD` 4k7** to 3V3 | I²C pull-ups |

Net: 3 value changes, 1 rewire, 6 added resistors.

---

## Fix 1 — UV hysteresis (the restart loop)

Hysteresis goes **0.66 V → 1.68 V**, closing the oscillation window for pack
impedance up to **~620 mΩ** (as-built: 260 mΩ).

| | V<sub>on</sub> | V<sub>off</sub> | Hysteresis |
|---|---|---|---|
| As-built | 11.16 V | 10.56 V | 0.60 V |
| Rev-B | 11.78 V | 10.10 V | **1.68 V** |

Verified: `VBIN_PP = 0` at 11.6 / 11.9 / 12.2 / 12.5 / 12.8 V with a 500 mΩ
pack — the band that left the as-built board buzzing at 34 ms with +5V0 stuck
at 1.81 V. Rev-B either runs at 5.16 V or latches cleanly off.

### The feedback node was chosen by measurement, not by argument

I got this wrong twice before landing it, and the reasons matter for review:

- **`PDB_VOUT` (first attempt) — rejected.** Nominally 1.64 V of hysteresis, but
  it *still oscillated* at 11.4 V / 500 mΩ. VOUT does not collapse cleanly when
  the switch opens; the downstream bulk caps hold it at an intermediate voltage,
  so injected feedback current depends on decay state and the threshold goes
  metastable.
- **`V3V3` — rejected.** Measured 2.03 V hysteresis, the best of the three — but
  that number is **inflated by a model bug**. The LT3010 vendor model drives its
  output to −1.02 V when unpowered (outside its ≥3 V spec), over-driving the
  feedback. Real hardware would sit near 0 V, giving ~1.6 V. Calibrating a design
  against a model artifact is not acceptable.
- **`GP` (LTC4368 GATE) — selected.** 1.68 V of *genuine* hysteresis, actively
  driven by the LTC4368 itself, no dependence on out-of-range vendor behaviour.

**Cost:** 20 MΩ on GP draws ~1.3 µA against the LTC4368's 35 µA charge pump
(~4%). Measured turn-on 35.1 ms vs 35.0 ms as-built — no meaningful slowdown.

## Fix 2 — Split the OV divider (required, not optional)

As built, UV and OV are two taps on one string. Feeding hysteresis into the UV
node would drag the OV tap with it and **trade a UV oscillation for an OV
oscillation** (~18.5–19.5 V). So OV gets its own divider off VIN.

Verified: OV trip 18.722 V and recovery 17.715 V are **identical across all
three feedback variants**, and the "extra crossing" probe found none — the OV
path is fully decoupled.

## Fix 3 — Shunt / fuse re-coordination (the 4–10 A gap)

| Fault R | Peak | As-built | Rev-B |
|---|---|---|---|
| 0.5 Ω | 26.7 A | trips | trips |
| 1.0 Ω | 14.0 A | trips | trips |
| **2.0 Ω** | **7.49 A** | **never trips** | **trips** |
| 3.0 Ω | 6.70 A | — | marginal (new boundary) |
| 5.0 Ω | 4.82 A | — | holds |
| no fault | 1.88 A | runs | runs |

Uncovered band narrows from **~4–10 A** to **~4.8–6.25 A**.

**Nuisance-trip check passed** — this was the real risk, since inrush (2.9 A)
now sits much closer to the worst-case-low trip (5.0 A). Across all six runs
inrush stayed 2.88–2.95 A and +5V0 reached 5.16 V every time.

---

## Regression — nothing else moved

| Metric | As-built | Rev-B |
|---|---|---|
| PDB on / +5V0 / +3V3 | 35.0 / 37.9 / 89.4 ms | 35.1 / 38.0 / 88.8 ms |
| Inrush / steady current | 2.90 / 1.578 A | 2.90 / 1.578 A |
| +5V0 / +3V3 | 5.161 / 3.305 V | 5.163 / 3.305 V |
| PDB 3V3 rail | 3.281 V | 3.281 V |
| PDB internal drop | 50.8 mV | **46.6 mV** |
| OV disconnect → recovery | 3.65 V → 5.161 V | 3.52 V → 5.161 V |
| UV disconnect → recovery | 0.878 V → 5.167 V | 0.876 V → 5.177 V |
| Short recovery (+3V3 back) | 1.504 s | 1.504 s |

Zero convergence warnings. Conduction loss **improved** — the 5 A fuse is
17.75 mΩ vs the 4 A part's 23.48 mΩ, which more than offsets the larger shunt.

---

## What to weigh before approving

1. **Turn-on moves 11.16 V → 11.78 V.** The board will refuse to start on a pack
   below ~2.95 V/cell. Arguably desirable, but it *is* a behaviour change — a
   depleted pack that used to boot now will not.
2. **Dropout moves 10.56 V → 10.10 V** (2.53 V/cell). Permits slightly deeper
   discharge. The Osiris LM73100 UVLO at 7.91 V remains the next backstop.
3. **20 MΩ is leakage-sensitive.** Board contamination or humidity across a
   20 MΩ path will shift the UV thresholds. Wants conformal coating and a clean
   assembly, or a guard trace.
4. **620 mΩ is not infinite.** A window reopens at 700–900 mΩ. No protection
   circuit fixes a pack that cannot supply the load — this buys margin for cold
   and aged packs, it does not eliminate the failure mode.
5. **Short-circuit peak rises slightly**, 178.7 A → 184.3 A, because the fuse
   resistance dropped. Still *not* an SOA claim — Q1/Q2 remain a datasheet-fitted
   surrogate with no SOA validity.
6. **`R2` is rewired, not just revalued.** This is a netlist change, not a BOM
   swap — the layout changes.

All the caveats in `FINDINGS.md` still apply: the fuse never opens in this model,
no thermal/SOA/loop-stability validity, no digital behaviour, and the LM73100
slew rate remains unverified.
