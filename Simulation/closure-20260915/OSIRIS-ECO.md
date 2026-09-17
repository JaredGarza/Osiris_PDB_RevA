# Osiris eFuse slew-control change

**Required companion change for the A-P3 PDB simulation. Not yet integrated into the original Osiris Altium files.**

The reference Osiris design leaves the LM73100 dVdt pins open. The combined
startup screen fails with that fast slew under some capacitance and supply
conditions. Add these three capacitors:

| New reference | Connection | Part |
|---|---|---|
| C901 | U21 pin 7 (dVdt) to U21 pin 8 (GND) | 3.3 nF, 50 V, C0G, 5%, 0603 |
| C902 | U22 pin 7 (dVdt) to U22 pin 8 (GND) | Same |
| C903 | U4 pin 7 (dVdt) to U4 pin 8 (GND) | Same |

Candidate: **TDK C1608C0G1H332J080AA**. The manufacturer lists this value,
dielectric, tolerance and package. [TDK product specification](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C1608C0G1H332J080AA).

Use the [KiCad change sheet](Osiris_Power_Input_ECO.kicad_sch) as an integration
reference. Its three isolated-pin ERC warnings represent the destinations in the
external design; it is not a complete Osiris schematic. Do not fabricate this
change sheet as a separate board. Confirm unused references when incorporating
the changes, remove the no-connect markers, and keep the capacitor returns short
to each IC's quiet ground. These are **Osiris** U21/U22/U4, not PDB U4.

TI specifies typical slew of 0.61 V/ms and a typical 2.35 ms turn-on delay at
12 V with 3.3 nF. The screening model uses those typical values and sweeps
0.3–2 V/ms and 0.1–5 ms independently. Those sweeps are engineering sensitivity
ranges, not guaranteed process/temperature limits.
[TI LM73100, sections 6.7, 7.3.4.1 and 10.1](https://www.ti.com/lit/ds/symlink/lm7310.pdf).

`osiris/osiris_eco.lib` preserves the reference device network and changes the
surrogate's slew/delay defaults. It does not simulate capacitor leakage, the
internal dVdt circuit, thermal shutdown, buck compensation or real digital loads.
U22 is fitted in the proposal but remains inactive in the battery-only startup
test; alternate-input operation needs its own verification.

On the assembled design, capture PDB current, Osiris input, 5 V and 3.3 V at
12 V and 16.8 V with maximum load and capacitance. Check both primary and alternate
input startup. Do not substitute open dVdt pins and retain the ECO simulation's
startup conclusions.
