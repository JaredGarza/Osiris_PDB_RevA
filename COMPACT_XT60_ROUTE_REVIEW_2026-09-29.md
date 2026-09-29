# Compact three-XT60 route review — 29 September 2026

**Status: connected CAD candidate, not a 60 A / 100 A qualified power board. Do not fabricate or power the ESC from this revision.**

## Connections and layout

| Reference | Connection | PCB part | Pin 1 | Pin 2 |
| --- | --- | --- | --- | --- |
| J1 | 4S battery input | XT60PW-M | GND | VBAT_RAW |
| J3 | Four-motor ESC output | XT60PW-F | GND | ESC_VBAT |
| J4 | Protected Osiris avionics output | XT60PW-F | GND | PDB_VOUT |
| J2 | Osiris I²C data | JST-GH, four pin | NC | SCL (pin 3 SDA, pin 4 GND) |

There are exactly three XT60 power footprints. J1 and J3 replace the two
provisional Phoenix terminal footprints. J2 remains a data connector; it is
not an additional battery or ESC power connection. J3 is the ESC connector
used by the latest schematic branch, and J4 remains the avionics connector.

The board outline is approximately **94.5 × 75.5 mm** at its bounding box,
down from **126.0 × 83.25 mm** for the prior placement study. The bounding
rectangle is about 32% smaller. The irregular outline retains the four
existing mounting holes, but frame and harness fit still need a mechanical
check. F2, C17, D5, C18, and C19 occupy the upper shelf. The existing
avionics circuitry stays in the central and lower portion.

The candidate routes `VBAT_RAW` from J1 to the input of F2 on front copper;
F2 feeds an `ESC_VBAT` front-copper area extending to J3 and the nearby
transient/bypass parts. A back-copper GND plane provides the J3 return toward
the J1 battery return. The protected avionics output remains isolated from
the ESC-positive area and feeds J4. J2 remains on the low-current I²C path.
The earlier J3-to-J4 protected-output spur was removed. A schematic wire
that had joined `ESC_VBAT` to GND was corrected before the board was checked.

## CAD checks

The final KiCad 10.0.5 check should be run with zone refill and
schematic parity after any further edit. On this candidate the checks found
no physical-rule violations and no unconnected items. Schematic ERC and
schematic-to-PCB parity each report two footprint-filter warnings: the
provisional UHS fuse pattern and the polarized C17 capacitor pattern do not
match the generic `Device:Fuse` and `Device:C` symbol filters. These checks verify CAD
connectivity and clearances at the current **0.20 mm** rule; they do not
establish current capacity, thermal rise, or assembly fit. The project is
still set to nominal **1 oz copper**.

## Release blockers

1. **Connector current rating:** The selected AMASS board-mount
   [XT60PW-M](https://www.china-amass.net/xt60pw-m-product/) and
   [XT60PW-F](https://www.china-amass.net/xt60pw-f-product/) are rated 35 A
   at a temperature rise of up to 85 K. J3 must carry
   the requested 60 A continuous / 100 A for 30 s; J1 carries that branch
   plus avionics current. The three-XT60 arrangement therefore does not
   satisfy the requested electrical target. Select and qualify a connector
   architecture rated for the actual harness and duty cycle before release.
2. **Copper and returns:** The front positive areas and back GND plane are
   connectivity routes, not 60 A / 100 A conductors verified by calculation
   or temperature testing. In particular, the fuse pads, XT60 pins,
   narrowed copper near the upper shelf, and any layer transitions need
   current-density, voltage-drop, fault-energy, and temperature-rise work.
   Revisit clearance and fabrication rules if increasing copper weight.
3. **Fuse and transient parts:** F2 uses a provisional
   [Schurter UHS](https://www.schurter.com/en/datasheet/UHS) footprint.
   Confirm its exact 100 A device, land pattern, solder process, time-current
   behavior, DC interrupt rating, and coordination with the battery and PCB.
   Qualify D5 and C17–C19 against ESC ripple, inrush, and transient energy.
4. **Mechanical and manufacturing:** Verify mated connector polarity and
   harness exit, XT60 board-edge seating, fuse access, the four mounting-hole
   locations, and actual enclosure clearance. Regenerate BOM, placement,
   Gerbers, and drill files only after the electrical architecture is fixed.

The preceding [28 September manufacturing review](MANUFACTURING_REVIEW_2026-09-28.md)
and [first ESC placement study](ESC_BRANCH_PLACEMENT_NOTES.md) describe older
board states and must not be used as release evidence for this candidate.
