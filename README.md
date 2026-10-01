# Osiris PDB Rev A

This repository contains the current KiCad 10 power distribution board project.
Open [Osiris_PDB_RevA.kicad_pro](Osiris_PDB_RevA.kicad_pro) to edit the schematic and PCB. The `Libraries` and `Datasheets` directories contain project resources; keep them alongside the project files.

The PCB is the compact layout restored on October 1, 2026: J1 is on the left, J3 is on the right, and the ESC capacitor sits above the central circuitry. The schematic uses the matching connector and net assignments. Local library names and resource paths are configured for this project directory.

This revision is still in progress. KiCad reports board rule violations and incomplete connections; run the checks below before manufacturing.

To repeat the checks from this directory:

```sh
kicad-cli sch erc Osiris_PDB_RevA.kicad_sch
kicad-cli pcb drc --schematic-parity Osiris_PDB_RevA.kicad_pcb
```
