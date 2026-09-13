# PDB parts-planning freeze — 13 September 2026

Baseline ID: **PDB-PROCUREMENT-2026-09-13**.

The current PDB schematic, nominal values, footprints and order codes are fixed as
this dated procurement baseline. This supports prototype parts planning before the
PCB is routed. **Final functional schematic approval for the new Osiris Rev B power
system is still pending its interface and load budget.** This is not fabrication or
flight release, and it does not guarantee that no engineering change will be needed.

## What is ready today

- 39 schematic components: 32 purchased components plus 7 bare test pads.
- The separately purchased fuse holder makes **33 physical purchased items per PDB**.
- **27 distinct order codes**, including **23 SMT types / 29 SMT placements**.
- Through-hole/hand assembly: J1, J3 and the F1 holder. F1 is inserted manually.
- Nine formerly unspecified ordinary resistors now have YAGEO RC0805 1%, 0.125 W
  order codes. Values and 0805 footprints were retained.
- Q1/Q2 use full ordering code ISC015N06NM5LF2ATMA1 for the existing device.
- U1 uses LTC4368IMS-1#TRPBF, the tape-and-reel version of the existing MSOP -1 device.
- No electrical value, footprint, pin assignment or net changed in this pass.
- Fresh ERC: 0 errors, 0 warnings under the existing project settings. Connectivity
  is identical to the reviewed September 12 export. The BOM was regenerated from KiCad.

The workbook is `outputs/procurement-20260913/PDB-RevA-Parts-Planning.xlsx` in the
repository. The grouped CSV beside this note is a per-board list, not a purchase order.
Enter actual board count, feeder setup loss and stock before calculating quantities.
The workbook's initial 10% spare allowance is an editable planning assumption.
Stock, supplier price, lead time and received inventory have not been established.

## Order boundary

Use the listed identifiers to check lab stock, request quotes and buy modest prototype
quantities. Do not commit production volumes for D1/D3, Q1/Q2 or F1 on the strength of
the screening simulation. F1's 4 A rating remains a candidate; the existing holder
choice does not make the final fuse rating settled. Check retention and access before
ordering bulk holders/connectors.

Resistor ratings are nominal family selections, not a completed abnormal-fault/pulse
review. High-voltage divider and low-power sense networks retain their previous values.
Datasheet voltage limits and power limits both apply; a 150 V resistor rating does
not mean that every resistance can dissipate 150 V continuously. Manufacturer RC
specifications and normal-operating network calculations must be used together.

For SMT supply, order an appropriate reel or continuous tape with sufficient leaders
for the lab machine. Cut-tape fragments, bulk bags and tube packaging may require
different feeding. Tape width/pitch, nozzle, carrier orientation, feeder slot and
moisture/reflow handling need the actual supplier packaging and machine details.
MSOP/VSSOP/exposed-pad parts and the large JST connector also need pickup/vision checks.

There is no centroid/XY/rotation file yet: coordinates, side and rotation come from
the routed PCB. The later assembly release also needs verified footprints, stencil,
fiducials, panel rails, board origin, BOM-to-placement reconciliation and first-article
orientation checks. Freezing parts today lets you prepare stock and feeders; it does
not create a runnable machine job today.

## Rev B design boundary

Jared clarified that the power-section removal/replacement and top-facing ports are
**planned**, with no updated schematic saved yet. The local folder named OsirisRevB
still contains the older imported power implementation. Treat it as reference only.

The four matches in `RevB-common-part-candidates.csv` are candidates, not confirmed
new Rev B demand:

| Part | PDB quantity | Existing Osiris reference | New Rev B status |
|---|---:|---|---|
| INA228AIDGSR | 1 | IC11 | Decide whether a second monitor is needed |
| BM04B-GHS-TBT(LF)(SN) | 1 | J27/J28/J29/J30/J37 | Confirm retained connectors and quantities |
| XT60PW-M | 1 | J16 | Existing horizontal connector; top-facing design may change it |
| XT60PW-F | 1 | J15 | Existing horizontal connector; may be removed/replaced |

The PDB's 0603/0805/1206 passives are not reel-equivalent to Osiris 0402 parts just
because the resistance or capacitance is the same. Do not standardize onto smaller
packages without checking voltage, power, effective capacitance and footprint.

**Proposed interface to preserve this PDB baseline:** protected unregulated 4S on the
PDB power output; new Osiris regulators generate its local rails. No new Rev B regulator
MPNs have been selected or silently added to this order list. If the team instead
moves those converters onto the PDB, this baseline requires an engineering revision.

The new Osiris power schematic needs to define:

1. Jetson module and permitted power modes; FMU, USB/ST-LINK and peripheral rail loads,
   startup peaks, rail accuracy, sequencing and peak/continuous limits.
2. Rail conversion from the PDB's actual input range; current and thermal headroom,
   regulator compensation and verified capacitor/inductor selections.
3. USB/debug versus battery power selection, backfeed prevention, fault isolation and
   the desired behavior when the avionics supply trips. Do not rely on the removed U21.
4. Top-facing connector types, power polarity, retention and cable current rating.
5. I2C pin mapping, local pull-up supply and firmware ownership. The old J16/J28
   designators and old ST_LINK_T_PWR routing are not requirements for the new board.

## Deadline alignment

The supplied USL meeting slides, pages 4 and 6–7, record a September 13 PDB-layout
target and Osiris conversion milestone, September 19 Osiris power-schematic work,
September 24 layout/simulation/BOM review and October 2 Rev B manufacturing review.
Those are historical plan dates, not evidence the work is complete. Jared's current
request brings this parts-planning freeze forward to today. This package does not
claim the still-missing PDB layout or planned Rev B power section is complete.

## Change control

After this baseline, changes to MPN, package, value, connector orientation, pinout or
power architecture require a new dated BOM revision and a check against already
ordered stock. Do not move or overwrite the Git tag for this baseline. Layout can
continue in the active project; the tag and SHA-256 manifest identify what purchasing
used. Keep final fuse selection and new Rev B commonality on the open-items list.

## Selection references

- [YAGEO RC0805 43.2 kΩ specification](https://yageogroup.com/component-documentation/download/specsheet/RC0805FR-0743K2L)
- [YAGEO RC0805 56.2 kΩ specification](https://yageogroup.com/component-documentation/download/specsheet/RC0805FR-0756K2L)
- [YAGEO RC0805 22 kΩ specification](https://yageogroup.com/component-documentation/download/specsheet/RC0805FR-0722KL)
- [YAGEO RC0805 200 kΩ specification](https://yageogroup.com/component-documentation/download/specsheet/RC0805FR-07200KL)
- [YAGEO RC0805 10 Ω specification](https://yageogroup.com/component-documentation/download/specsheet/RC0805FR-0710RL)
- [YAGEO RC0805 4.7 kΩ specification](https://yageogroup.com/component-documentation/download/specsheet/RC0805FR-074K7L)
- [Infineon device and ordering code](https://www.infineon.com/part/ISC015N06NM5LF2)
- [ADI LTC4368 ordering options](https://www.analog.com/en/products/ltc4368.html)

The 2 MΩ and 680 kΩ selections use the same RC0805 ordering family; their direct
manufacturer specsheet fetches were unavailable in this pass. Confirm their exact
supplier datasheets on the purchase quote. No substitute MPN is preapproved.
