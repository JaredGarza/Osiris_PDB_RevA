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

Two sockets on one bus are acceptable in principle for ordinary loads that
share the same supply, provided their **combined** normal, startup, and fault
currents fit the entire path and neither attached device can back-power the
other through a second source. The current PDB design target is **25 W and
2.5 A together** for the avionics branch. The 4 A fuse is not a 4 A operating
allowance and is not sized for a four-motor ESC feed.

Before assigning J3/J4 to loads, identify what plugs into each connector,
the maximum simultaneous demand (including startup), whether either load has
another power source, the actual 4S battery's fault-current capability, and
the mating-harness polarity. If an ESC uses either connector, redesign the
power route from battery through connector, protection, fuse, copper, and
return conductors for its specified current. If separate fault containment
is required for two avionics loads, add independent branch protection rather
than treating D3 as branch isolation.

Sources: [ADI LTC4359 ideal-diode behavior](https://www.analog.com/media/en/technical-documentation/data-sheets/ltc4359.pdf),
[TI INA228 absolute limits](https://www.ti.com/lit/ds/symlink/ina228.pdf),
[ST STPST10H100SB datasheet](https://www.st.com/resource/en/datasheet/stpst10h100sb.pdf),
[Littelfuse MINI fuse datasheet](https://www.littelfuse.com/assetdocs/littelfuse-datasheet-297-mini32v?assetguid=42c9dd21-a88e-4328-8e67-2f832444faf1).
