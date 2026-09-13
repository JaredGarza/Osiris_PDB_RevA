# Osiris PDB Rev A

Active 39-component 4S avionics power protection and I2C telemetry schematic.
Open `Osiris_PDB_RevA.kicad_pro` in KiCad 10. Project libraries use `${KIPRJMOD}`.

**Not flight-ready. No current PDB PCB layout exists.** Start with
[Rev A readiness and completion plan](docs/REV-A-READINESS.md) and
[current scope](DESIGN-SPEC.md).

Older competing PDB projects and local backup directories are preserved in an
external dated archive on the original workstation; they are not required to open
this repository. Consult that archive's move manifest to restore local copies.
Historical apply scripts and review documents record earlier revisions and must not
be treated as instructions to regenerate the current design.

## Repository contents and checks

The schematic, project-local libraries, engineering and purchasing BOMs, datasheets,
simulation sources and review evidence are versioned together. Full Osiris board
imports, editor state and LTspice binary outputs are kept out of Git. Git history
retains the obsolete PCB; it is not a layout for the current circuit.

Install KiCad 10 and run from the repository root:

```sh
kicad-cli sch erc -o erc-current.rpt Osiris_PDB_RevA.kicad_sch
kicad-cli sch export netlist --format kicadxml -o docs/revision-audit-20260912/current.net.xml Osiris_PDB_RevA.kicad_sch
python docs/revision-audit-20260912/check_design.py
```

The Python checker uses the standard library. Set `KICAD_FOOTPRINT_DIR` if system
footprints are not at the default Windows or Linux location. Historical comparison
inputs are committed XML snapshots; regenerate the current input after electrical edits.

LTspice screening uses `Simulation/Osiris_PDB_RevB_Cascade.cir` (historical filename).
It requires LTspice's LTC4368-1 model and SiR870ADP entry in `standard.mos`; adjust the
deck's absolute `standard.mos` path for your installation. U21_SCREEN is an engineering
surrogate. Audit simulation logs under `docs` are retained as evidence; routine output
is ignored. See the readiness report for model limitations. Historical source-audit
scripts also require original Osiris files from the author's workstation.
