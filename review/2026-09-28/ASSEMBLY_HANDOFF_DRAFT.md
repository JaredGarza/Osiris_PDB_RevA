# JLCPCB assembly handoff — draft, not for order

The current board passes schematic ERC and PCB DRC, with zero unconnected pads
and zero schematic-to-board parity issues. Electrical fault qualification, final
load definition, physical fit, and JLCPCB part matching remain open. See
`../../MANUFACTURING_REVIEW_2026-09-28.md` before making a release ZIP.

## Board and files

- Board: two-layer FR-4, 1.6 mm, 1 oz outer copper, solder mask, assembly
  finish to be selected with JLCPCB.
- `assembly-bom-draft.csv`: 51 placed parts. Every JLCPCB Part # cell is blank
  until the exact MPN has been matched and confirmed in JLCPCB's order review.
- `assembly-cpl-draft.csv`: 51 positions, in millimetres, with board-positive Y.
  Compare every location and rotation against JLCPCB's placement preview.
- `assembly-extra-parts-draft.csv`: the separate 4 A blade fuse inserted into
  the installed holder.
- `schematic-bom-current.csv`: source-of-truth schematic population, including
  DNP and bare test pads. R17/R18 are DNP; TP1–TP7 are bare PCB pads.
- Gerbers and separate PTH/NPTH drills currently exist only in a temporary
  review folder. No manufacturing ZIP has been released.

## Assembly details to confirm

- F1 is a **Keystone 3568 fuse holder** at the PCB footprint. The fuse is a
  separate **Littelfuse 0297004.WXNV**, 4 A MINI blade. Confirm JLCPCB will
  source, solder, and insert both parts. The holder MPN is the placed F1 BOM
  row; the blade fuse is in the extra-parts file.
- J1 is XT60PW-M battery input; J3/J4 are XT60PW-F protected outputs. J1 pin
  2 is battery positive, J3/J4 pin 2 is protected positive, and pin 1 is GND.
  Confirm board/contact orientation and the actual mating harness.
- Confirm through-hole assembly for the XT60 connectors, holder, and C11–C16,
  and verify the six 0.6 mm plated slots in the production preview.
- Check the Infineon Q1/Q2 and Q3 solder-paste apertures against the exact
  supplied packages before accepting the stencil preview.

JLCPCB states that only BOM parts matched to its library will be populated;
its order review allows unmatched parts to be selected. Through-hole assembly
is offered for supported parts, including connectors. See its
[assembly FAQ](https://jlcpcb.com/help/article/pcb-assembly-faqs) and
[KiCad 10 BOM/CPL guide](https://jlcpcb.com/help/article/how-to-generate-the-bom-and-centroid-file-from-kicad).
