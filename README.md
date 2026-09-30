# Osiris PDB Rev A

This repository contains the current KiCad 10 power distribution board project.
Open [Osiris_PDB_RevA.kicad_pro](Osiris_PDB_RevA.kicad_pro) to edit the schematic and PCB. The `Libraries` and `Datasheets` directories contain project resources; keep them alongside the project files.

The PCB is the latest local revision saved on September 29, 2026. The schematic and PCB are still engineering work in progress. KiCad 10.0.5 reports no PCB rule violations or unconnected items, with two footprint-filter warnings that also appear in the schematic ERC. Those checks do not establish manufacturing readiness.

To repeat the checks from this directory:

```sh
kicad-cli sch erc Osiris_PDB_RevA.kicad_sch
kicad-cli pcb drc --schematic-parity Osiris_PDB_RevA.kicad_pcb
```
