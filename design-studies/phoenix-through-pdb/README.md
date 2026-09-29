# Phoenix through-PDB placement study

**Layout only. Do not fabricate or power the ESC from this board.**

This KiCad PCB shows the single-battery distribution layout requested after
the three-XT60 routed candidate. The 4S pack retains its XT60 and uses a
short XT60-to-wire adapter at J1. J1 and J3 are provisional Phoenix Contact
MKDSP 25/2-15.00 green terminals. J3 connects to the AERO SELFIE ESC battery
input wires. J4 remains the protected Osiris avionics XT60 output, and J2
remains I²C.

J1 positive faces F2 input, and J3 positive faces F2 output. The parts are
positioned for a short, straight positive corridor with a broad return
path. The ESC capacitor and transient parts are in a row above J3. The
existing four mounting-hole centers and lower avionics placement were kept.
Bounding rectangle: **94.55 × 98.55 mm**.

The Phoenix body is about 43.5 mm high. Check the aircraft frame and cable
bend space. F2 sits in the gap between two tall terminal bodies; its solder
process, inspection and replacement access need a real assembly review.

The board is **not routed**. The saved DRC report has zero physical-rule
violations and 25 unconnected items. The green-terminal and F2 footprints
are provisional. No schematic has been synchronized with this study; the
root project remains the active three-XT60 candidate. The pack's XT60,
adapter wires, green terminals, fuse, solder joints, PCB copper and ESC
input wires all need current and thermal qualification. Refer to the
[power-path foundation](../../docs/SINGLE_BATTERY_POWER_PATH_FOUNDATION_2026-09-29.md)
for the circuit boundary and unresolved ratings.

Regenerate the PCB from the project root with KiCad 10's Python:

```powershell
& 'C:\Program Files\KiCad\10.0\bin\python.exe' 'docs\build_phoenix_pdb_foundation.py'
```
