# Osiris PDB Rev A

This repository contains the current KiCad 10 power distribution board project.
Open [Osiris_PDB_RevA.kicad_pro](Osiris_PDB_RevA.kicad_pro) to edit the schematic and PCB. The `Libraries` and `Datasheets` directories contain project resources; keep them alongside the project files.

The PCB is the compact layout restored on October 1, 2026: J1 is on the left, J3 is on the right, and the ESC capacitor sits above the central circuitry. The schematic uses the matching connector and net assignments. Local library names and resource paths are configured for this project directory.

This revision is a prototype. Manufacturing preparation on October 2, 2026 resolved the redundant output-copper zone, improved J4 mounting-slot annular rings, filled missing part selections, and tightened silkscreen checks. Final checks report no schematic electrical-rule violations, no PCB design-rule violations, no unconnected PCB items, and no schematic parity issues.

The JLCPCB prototype quotation package and [release review](outputs/manufacturing-review-20261002/RELEASE_REVIEW.md) are in `outputs/manufacturing-review-20261002`. Exact JLCPCB parts matching, assembly-preview approval, and stackup/panel confirmation remain necessary before ordering. The 60 A continuous / 100 A for 30 seconds ESC targets still require physical qualification. Use the new manufacturing BOM for this design; the older cost workbook does not include every current selection.

The updated purchasing and cost workbook, with engineering, purchasing, and missing-link previews, is in `outputs/updated-board-20261001`. Component datasheets and local KiCad libraries are kept with the project. Temporary generation scripts, bundled software dependencies, and intermediate inspection files are excluded.

To repeat the checks from this directory:

```sh
kicad-cli sch erc Osiris_PDB_RevA.kicad_sch
kicad-cli pcb drc --schematic-parity Osiris_PDB_RevA.kicad_pcb
```
