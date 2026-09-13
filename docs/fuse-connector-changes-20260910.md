# Applied schematic changes — 10 September 2026

Source: the user's saved Osiris_PDB_RevA.kicad_sch. A pre-edit backup is in fuse-connector-backup-20260910.

- F1: Littelfuse 0297005.WXNV, 5 A MINI blade fuse; Keystone 3568 holder footprint and holder sourcing fields. The fuse rating is explicitly provisional pending load, inrush, temperature and fault coordination checks.
- J1: AMASS XT60PW-M, pin 1 GND, pin 2 VBAT_RAW.
- J2: JST BM06B-GHS-TBT(LF)(SN), six-pin vertical GH connector. Mating housing and contact fields added. Pinout remains 1 GND, 2 SDA, 3 SCL, 4 INA_ALERT_N, 5 PDB_FAULT_N, 6 NC; a custom Osiris cable still needs endpoint verification.
- J3: AMASS XT60PW-F, dedicated project symbol with pin 1 GND and pin 2 PDB_VOUT. The user's latest saved wires already placed ground and output on the desired physical contact positions; the final symbol matches those wires. Exported netlist verification confirms the polarity. Cable documentation targets Osiris J16 VBATT_IN based on the supplied Osiris archive.
- Manufacturer and MPN fields added for the selected connectors, fuse, shunt and ICs. U4's datasheet now matches Nexperia. Local datasheet links are used where PDFs downloaded successfully; online sources remain where hosts blocked download.
- Existing wires, threshold resistors and the shunt footprint are preserved. The older PCB is not modified by this schematic edit.

Validation: zero ERC errors/warnings; explicit netlist assertions for J1/J3 polarity and J2 pinout; all 33 board symbols have resolving footprints; local datasheet paths resolve; rendered schematic visually checked.

BOM.csv is KiCad's native symbol export, including the holder sourcing fields. BOM_purchasing.csv expands this to 34 rows so the separate fuse holder is purchased. The holder row belongs to the F1 assembly and is not an additional physical PCB footprint. Bare test pads need no purchased part. Ordinary resistor MPNs remain open.

Datasheets/README.md indexes nine new downloaded PDFs, the existing regulator-controller/MOSFET PDFs, and links for unavailable downloads. The original selection proposal records the reasoning; this file records the final implementation.
