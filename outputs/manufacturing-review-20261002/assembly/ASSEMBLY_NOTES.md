# Assembly instructions

The fitted build has 56 component placements, all on the top side. JLCPCB BOM/CPL are quotation inputs pending exact part matching and factory preview.

## Fitting instructions

- F1 placement is the **Keystone 3568 fuse holder**, not the removable blade fuse. Supply one Littelfuse 029707.5WXNV per board separately; insert after soldering, cleaning, and inspection.
- F2: fit SCHURTER **3-140-177**, 100 A / 50 VDC UHS. Do not substitute another family or use the old blade-fuse footprint.
- R17/R18: **do not populate**. The host owns the I2C pull-ups.
- H1–H4 are empty mounting holes. TP1–TP7 are bare copper test pads; no separate parts.
- Q1/Q2: exact Infineon ISC015N06NM5LF2ATMA1. Pins 1–3 source, 4 gate, 5–8 drain; custom pad primitives provide the enlarged source and drain lands. Review stencil deposition and hidden-joint soldering.
- U1: exact **LTC4368HMS-1#TRPBF**. The -2 variant is not an approved substitute.
- D3: both anode leads connect to GND; cathode tab connects to PDB_VOUT. Confirm the package orientation in the matched preview.
- D1/D4/D5 are bidirectional TVS parts. Fit the exact selected manufacturers/MPNs; no generic manufacturer substitutions are approved by this BOM.
- Verify C17/C9 capacitor polarity against copper/net assignments. All IC pin-1 positions must agree with the pad-1 table and assembly drawing.
- Confirm J1/J3's tall screw-terminal insertion and soldering process, mechanical support, and solder fill. Fit the JST and XT60 connectors in the specified orientation.

## Connector continuity table

| Connector | Pin | Connection |
| --- | --- | --- |
| J1 pack input | 1 | GND |
| J1 pack input | 2 | VBAT_RAW positive |
| J3 ESC output | 1 | GND |
| J3 ESC output | 2 | ESC_VBAT positive, after F2 |
| J4 avionics output | 1 | GND |
| J4 avionics output | 2 | PDB_VOUT protected positive |
| J2 host interface | 1 | INA_ALERT; no power feed |
| J2 host interface | 2 | I2C SCL |
| J2 host interface | 3 | I2C SDA |
| J2 host interface | 4 | GND |

Pin numbers are PCB/schematic pad numbers. Verify mating-harness contact numbers and physical polarity; visual connector gender alone is insufficient.

## Placement convention

Coordinates are millimeters, X right / Y up, using the KiCad absolute datum. THT footprints with offset pad-1 origins have been centered on their body/courtyard for insertion; these positions still need factory confirmation. SMT origins are retained. `Placement_Review.csv` records origins, proposed centers and actual pad-1 coordinates. Factory library rotations have not been assumed. Check all matched bodies and polarities in the assembly preview before order release.
