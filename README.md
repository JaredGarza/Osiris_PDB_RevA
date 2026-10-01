# Osiris PDB Rev A

This repository contains the current KiCad 10 power distribution board project.
Open [Osiris_PDB_RevA.kicad_pro](Osiris_PDB_RevA.kicad_pro) to edit the schematic and PCB. The `Libraries` and `Datasheets` directories contain project resources; keep them alongside the project files.

The PCB is the compact layout restored on October 1, 2026: J1 is on the left, J3 is on the right, and the ESC capacitor sits above the central circuitry. The schematic uses the matching connector and net assignments. Local library names and resource paths are configured for this project directory.

This revision is still in progress. Checks on October 1, 2026 reported no schematic electrical-rule violations, no unconnected PCB items, and no schematic parity issues. Six PCB design-rule violations remain; resolve them before manufacturing.

The updated purchasing and cost workbook, with engineering, purchasing, and missing-link previews, is in `outputs/updated-board-20261001`. Component datasheets and local KiCad libraries are kept with the project. Temporary generation scripts, bundled software dependencies, and intermediate inspection files are excluded.

To repeat the checks from this directory:

```sh
kicad-cli sch erc Osiris_PDB_RevA.kicad_sch
kicad-cli pcb drc --schematic-parity Osiris_PDB_RevA.kicad_pcb
```
