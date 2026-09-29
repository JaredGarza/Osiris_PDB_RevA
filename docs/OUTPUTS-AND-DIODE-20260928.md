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

The reported ESC is an **AERO SELFIE 45 A four-in-one, Oneshot-capable model**
(reported identifier `X004186FZF`). The matching
[manufacturer listing](https://aeroselfie.myshopify.com/products/45a-4-in-1-esc-brushless-motor-speed-controller)
states 2S–6S input, 45 A continuous and 55 A bursts for up to 30 seconds.
Its separate [45 A stack listing](https://aeroselfie.myshopify.com/products/aero-selfie-h743-flight-controller-stack-30-x-30-stack-with-45a)
explicitly says **45 A per motor channel**. This is an ESC channel rating,
not a measured combined battery-input current; four motors may demand far
more than 4 A at the battery. Confirm the exact item from its label or
purchase record before sizing the motor-power branch.

The user requires **J4 to remain on the PDB as the ESC supply**. The required
architecture is a new, separately protected **motor-power branch** from a
battery input rated for the combined loads to J4. The existing F1, Q3,
Q1/Q2, R5, and their narrow avionics copper should feed **J3/Osiris only**.
J4 needs its own correctly rated positive path and return path, and its own
fault protection. If one battery connector J1 remains, its contacts, solder
joints, wire, and upstream fuse must carry the sum of both branches. The
present two-layer, 1 oz, avionics-sized layout cannot be approved for that
motor branch by renaming J4's net or fitting a larger F1.

The schematic calls out `XT60PW-M` at J1 and `XT60PW-F` at J4 without a
fully specified manufacturer variant. AMASS lists its [XT60PW-M30](https://www.china-amass.net/xt60pw-m-product/)
and [XT60PW-F30](https://www.china-amass.net/xt60pw-f-product/) at **35 A with
up to 85 K temperature rise**. That does not establish an acceptable rating
for this assembly, and the shared J1 input would carry both branches. Confirm
the exact connector variant and mating cable, then select connectors against
the measured or specified combined battery current and permitted heating.

```text
4S battery → rated PDB input ┬→ dedicated ESC protection and heavy power/return path → J4 → ESC
                             └→ F1 → Q3 → Q1/Q2 → R5 → J3 → Osiris J16
```

The ESC model, continuous and peak input currents, battery fault-current
capability, and mating-harness polarity are still required to size either
motor-power implementation. Motor average current is not a substitute for
peak, startup, or fault-current requirements.

Sources: [ADI LTC4359 ideal-diode behavior](https://www.analog.com/media/en/technical-documentation/data-sheets/ltc4359.pdf),
[TI INA228 absolute limits](https://www.ti.com/lit/ds/symlink/ina228.pdf),
[ST STPST10H100SB datasheet](https://www.st.com/resource/en/datasheet/stpst10h100sb.pdf),
[Littelfuse MINI fuse datasheet](https://www.littelfuse.com/assetdocs/littelfuse-datasheet-297-mini32v?assetguid=42c9dd21-a88e-4328-8e67-2f832444faf1).
