# PDB J3/J4 output topology — 28 September 2026

The active schematic and PCB netlist show **one protected output bus with two
connectors**, not two separately protected power paths:

`J1 battery → F1 4 A fuse → Q3/U5 ideal diode → Q1/Q2/U1 protection → R5 5 mΩ shunt → PDB_VOUT → J3 and J4`

J3 pin 2 and J4 pin 2 are both `PDB_VOUT`; both pin 1 contacts are GND. The
sum of both load currents flows through F1, Q3, Q1/Q2, and R5. A short or
overload at either output can shut off both. There is no branch fuse, current
limit, or isolation diode between J3 and J4.

D3 is a Schottky diode from GND (anode) to `PDB_VOUT` (cathode). It can conduct
when the shared output swings negative; it does not carry normal load current
and cannot prevent J3 from feeding J4 or vice versa. Its forward voltage is
not proven to keep the INA228 sense and VBUS pins above the device's −0.3 V
absolute minimum during an actual negative transient. The U5/Q3 ideal-diode
stage blocks reverse current toward the battery input; it is also upstream
of both connectors and does not isolate them from each other.

The intended loads are now confirmed: **J3 feeds Osiris J16; J4 feeds the
four-motor ESC**. As drawn, ESC startup and motor current pass through the
same 4 A fuse and avionics protection path as Osiris. A fault at either
connector can remove power from both. The current PDB was designed around
**25 W and 2.5 A together** for avionics; even that target must be revised
for the Jetson's new 25 W design case. The J4 ESC connection is therefore a
**release blocker**, not a second usable motor-power branch.

Recommended architecture if the ESC can use a separate battery harness:
split the 4S battery feed into separately rated and protected avionics and
ESC branches. Keep `battery → PDB J1 → J3 → Osiris J16` for avionics, and feed
the ESC from its own branch with wire, connectors, fuse/protection, and return
conductors sized to the ESC's actual maximum and startup current. Remove J4
from this avionics PCB when that architecture is selected. If J4 must stay
on the PCB, create a genuinely separate motor-current path and qualify J1,
J4, copper on both layers, return current, protection, and heating for the
ESC's specified current. Merely moving J4 to the raw battery net or fitting
a larger F1 is not a qualified fix.

The ESC model, continuous and peak input currents, battery fault-current
capability, and mating-harness polarity are still required to size either
motor-power implementation. Motor average current is not a substitute for
peak, startup, or fault-current requirements.

Sources: [ADI LTC4359 ideal-diode behavior](https://www.analog.com/media/en/technical-documentation/data-sheets/ltc4359.pdf),
[TI INA228 absolute limits](https://www.ti.com/lit/ds/symlink/ina228.pdf),
[ST STPST10H100SB datasheet](https://www.st.com/resource/en/datasheet/stpst10h100sb.pdf),
[Littelfuse MINI fuse datasheet](https://www.littelfuse.com/assetdocs/littelfuse-datasheet-297-mini32v?assetguid=42c9dd21-a88e-4328-8e67-2f832444faf1).
