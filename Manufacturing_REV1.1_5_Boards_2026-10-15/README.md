# Osiris PDB REV1.1 — five-board manufacturing package

## Files to upload to JLCPCB

Use only the three files in `JLCPCB/`: Gerbers.zip for fabrication, BOM.csv for assembly and Pick_and_Place.csv for component placement. Select **five assembled boards**. BOM quantities are per board. This assembly variant contains **51 JLC-fitted parts per board**.

**C1, F1, R19, U1, F2 and R5 must be left unpopulated by JLC.** They are deliberately excluded from BOTH JLC assembly files; the physical pads and tracks remain on the PCB. Confirm these omissions in the final JLC component list and placement preview. Do not allow automatic matching to add them back.

## Parts to install locally

`Local_Assembly/BOM.csv` and `Pick_and_Place.csv` contain the six deferred parts per board (30 fitted parts across five boards). `Procurement_5_Boards.csv` lists their purchasing quantities, including the existing spare policy. Its price figures are references, excluding freight, taxes and assembly; verify actual distributor stock and checkout prices before purchasing.

Use the exact listed MPNs. U1 remains the 125 C H-grade LTC4368; no I-grade substitution has been made. C1 and R19 can be iron soldered, F1 is a through-hole holder, and U1 needs fine-pitch soldering and inspection. F2 and the four-terminal R5 shunt require an appropriate controlled heating process for the connected copper. Preserve all four Kelvin shunt connections. These boards are incomplete until local installation and inspection. Do not power them beforehand.

F1 is the Keystone 3568 HOLDER. Its blade fuse insert is a separate item listed in the full procurement workbook and is not a JLC placement. Check that the correct fuse is available and installed before operation.

## Reference and design source

`Reference/` contains the full 57-part-per-board BOM/CPL, the two latest single-sheet procurement workbooks, and the latest ERC/DRC reports. These full assembly files include the deferred components and **must not be uploaded for this partial-JLC assembly order**. PnP.xlsx is full-board local procurement, not just the six deferred parts. JLCPCB_BOM_Stock_5_Boards.xlsx is the full-design stock review; remaining stock warnings there describe the full design. Use the dedicated six-part procurement file for local completion of this order.

`Source/` contains the current KiCad design, libraries and datasheets. The schematic keeps all parts populated because this is a manufacturing assembly variant, not a circuit deletion.

The fabrication ZIP contains Gerbers and drills for the current 82.5 x 65 mm four-layer board, 1 oz outer / 0.5 oz inner copper. Latest sourcing changes only affect part metadata; board geometry is unchanged. D1/D4 specify RUILON SMAJ24CA C28092. Final rotations, polarity, through-hole/manual assembly eligibility, and current stock allocation still require JLC order review. ERC, DRC, unconnected-item and schematic-parity checks report zero issues; these checks do not replace electrical, thermal, surge or hardware validation. Existing design validation limitations remain applicable.

`SHA256.json` records package file hashes. Generated 2026-10-15. This package does not assert that every remaining JLC part is currently allocated or that assembly/fabrication service costs are quoted.
