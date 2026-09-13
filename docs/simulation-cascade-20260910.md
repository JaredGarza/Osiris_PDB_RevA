> HISTORICAL SNAPSHOT — superseded for readiness decisions by `docs/REV-A-READINESS.md`
> (project-relative path). Includes unvalidated claims about maximum load, fuse coordination,
> clamp margin and/or earlier wiring. Use the current schematic and fresh audit results.

# Cascade simulation results — 10 September 2026

Screening simulation of the PDB feeding Osiris, run after the requirements-pass schematic
changes. **This is screening, not hardware qualification** — see Limitations before
quoting any number here.

- Netlist: `Simulation/Osiris_PDB_RevB_Cascade.cir`
- Log: `Simulation/Osiris_PDB_RevB_Cascade.log`
- LTspice 26.0.2, Gear method, `reltol=.003`, 2.3 s transient, 23.7 s wall clock
- All 8 cases found an operating point and ran to completion

## Cases

| # | Condition | VBAT | R source | C scale | U21 dV/dt cap |
|---|---|---|---|---|---|
| 1 | Nominal | 14.8 V | 20 mΩ + 6 mΩ | 1.0 | 0 (fast) |
| 2 | Slower U21 ramp | 14.8 V | 20 mΩ + 6 mΩ | 1.0 | 1.8 nF |
| 3 | Slowest U21 ramp | 14.8 V | 20 mΩ + 6 mΩ | 1.0 | 3.3 nF |
| 4 | Low battery | 12 V | 20 mΩ + 6 mΩ | 1.0 | 0 |
| 5 | Full pack | 16.8 V | 20 mΩ + 6 mΩ | 1.0 | 0 |
| 6 | High source impedance | 12 V | 200 mΩ + 50 mΩ | 1.0 | 0 |
| 7 | Low capacitance corner | 16.8 V | 20 mΩ + 6 mΩ | 0.5 | 0 |
| 8 | High capacitance corner | 16.8 V | 20 mΩ + 6 mΩ | 1.2 | 0 |

The stimulus sequence is: reverse pack 0–20 ms, off to 50 ms, normal 51–400 ms,
overvoltage 19.5 V at 410–500 ms, recovery, undervoltage 9 V at 810–900 ms, recovery,
output short at 1.2 s for 100 ms, then recovery to 2.3 s.

## Results

Voltages in V, currents in A, I²t in A²s.

| # | V reverse | I pk start | V steady | nEN | V off (OV) | V post-OV | V off (UV) | V post-UV | I pk short | Fuse I²t | V recovered |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | −0.052 | 4.21 | 14.65 | 1.00 | ~0 | 14.65 | ~0 | 14.65 | 134 | 0.111 | 14.65 |
| 2 | −0.052 | 1.57 | 14.65 | 1.00 | ~0 | 14.65 | ~0 | 14.65 | 134 | 0.111 | 14.65 |
| 3 | −0.052 | 1.57 | 14.65 | 1.00 | ~0 | 14.65 | ~0 | 14.65 | 134 | 0.111 | 14.65 |
| 4 | −0.052 | 3.71 | 11.82 | 1.00 | ~0 | 11.82 | ~0 | 11.82 | 108 | 0.066 | 11.82 |
| 5 | −0.052 | 4.40 | 16.67 | 1.00 | ~0 | 16.67 | ~0 | 16.67 | 154 | 0.186 | 16.67 |
| 6 | −0.052 | 3.50 | 11.35 | 1.00 | ~0 | 11.36 | ~0 | 11.35 | 41 | 0.015 | 11.35 |
| 7 | −0.052 | 2.12 | 16.67 | 1.00 | ~0 | 16.67 | ~0 | 16.67 | 155 | 0.171 | 16.67 |
| 8 | −0.052 | 4.82 | 16.67 | 1.00 | ~0 | 16.67 | ~0 | 16.67 | 154 | 0.190 | 16.67 |

"~0" is 10⁻¹³ to 10⁻⁸ V — the rail is genuinely off, not merely low.

## What the numbers say

**Reverse-battery protection holds.** `PDB_VOUT` sits at −0.052 V with the pack
reversed, against the −0.3 V absolute maximum on U3's IN pin. This is the result of the
D3 clamp added in the requirements pass; before it, the node reached about −0.8 V, which
would have exceeded U3's rating. See the caveat on the D3 model below.

**Overvoltage and undervoltage both disconnect and both recover.** The downstream rail
collapses to zero during the 19.5 V and 9 V excursions in every case, and returns to its
pre-fault value afterwards. `V post-OV` and `V post-UV` match `V steady` to within a
millivolt throughout.

**Inrush stays modest.** Peak start current is 1.6–4.8 A across the corners, worst at
case 8 (full pack into the high capacitance corner) — as expected, since that is the most
charge to move at the highest voltage. The slow-ramp cases 2 and 3 halve the peak,
confirming the U21 dV/dt cap does what it is there for.

**Fuse and electronic breaker are correctly coordinated.** This was the open question
flagged on the schematic as "fault coordination pending", and it resolves cleanly:

| | Value |
|---|---|
| Worst-case let-through during output short (case 8) | 0.190 A²s |
| Littelfuse 0297004 melting I²t (4 A MINI) | 17 A²s |
| Margin | ~89× |

The fuse is nowhere near opening on an output short — the LTC4368 clears the fault and
the board recovers by itself, which is the behaviour you want. F1 stays a protection
device for wiring faults rather than something that trips on a recoverable event. The
datasheet's cold resistance for this part, 23.48 mΩ, matches the value used in the model
exactly, so the fuse model is at least consistent with the part selected.

**The short-circuit current peak is brief.** Peak current through R5 reaches 134–155 A,
which looks alarming in isolation, but the let-through energy bounds its duration: 0.190
A²s spread over the 100 ms window is only ~1.4 A RMS, so a 154 A spike can persist no
more than roughly 8 µs. That is consistent with the ~8 µs fault turn-off the D2 gate
bypass provides. Without D2 the turn-off degrades to about 300 µs, which would raise the
energy by a large factor — so this result is also indirect support for the D2 change.
It does **not** establish that the MOSFETs survive the pulse; see below.

## Limitations

These matter, and none of them are resolved by this run:

1. **The MOSFET model is a stand-in.** The simulation uses `SiR870ADP`; the schematic
   specifies `ISC015N06NM5LF2`. The 134–155 A peaks are therefore not an SOA verdict on
   the fitted part. Checking that pulse against the real device's SOA curve is still open,
   and it is the most significant outstanding item here.
2. **D3 is modelled with a generic diode**, the same `DBYP` behavioural model used for the
   D2 gate bypass (`Is=1u N=1.1 Rs=.15`), not an extracted MBR0540. A real Schottky drops
   more at the same current, so −0.052 V is optimistic. The margin to −0.3 V is large,
   but confirm on hardware.
3. **The fuse cannot open in this model** — only its cold resistance is present. That is
   harmless for this conclusion, since the let-through never approaches melting I²t
   anyway, but the model would not show a nuisance trip if one existed.
4. **The TVS is a piecewise behavioural model**, not a device model.
5. **The load is a planning allowance**, 22.97 W, not a measured Jetson profile.
6. **The short is a single 100 ms event.** Repeated retries into a sustained short would
   accumulate thermal energy that this run does not capture.

## Reproducing

```
& 'C:\Program Files\ADI\LTspice\LTspice.exe' -b -Run `
  '<repo>\Simulation\Osiris_PDB_RevB_Cascade.cir'
```

Measurements land in `Osiris_PDB_RevB_Cascade.log` under `Measurement:` headings.
