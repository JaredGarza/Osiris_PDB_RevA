# Osiris PDB Rev A

Current simulation/design audit: [review](Simulation/combined-20260915/REVIEW.md). This supersedes earlier population and simulation claims.

Active 48-component A-P2-DRAFT 4S avionics power protection and I2C telemetry schematic.
Open `Osiris_PDB_RevA.kicad_pro` in KiCad 10. Project libraries use `${KIPRJMOD}`.

**September 15 engineering draft:** U3 is now LT3010 with R11/R12/C10.
See the [electrical review](docs/PDB-ELECTRICAL-REVIEW-20260915.md) and
[proposed interface](docs/PDB-INTERFACE-PROPOSAL-20260915.md). Actual loads and
mechanical constraints remain undecided; negative-input protection and fault
qualification remain open. The previous parts baseline is historical.

**Historical parts-planning baseline: 13 September 2026.** See the
[freeze note](procurement/2026-09-13/FREEZE-NOTE.md) and
[parts workbook](outputs/procurement-20260913/PDB-RevA-Parts-Planning.xlsx).
New Osiris Rev B power and top-facing ports are planned, not yet drawn; shared-part
counts from the old imported PCB remain candidates.

See the [PDB and Osiris completion plan](docs/PDB-AND-OSIRIS-COMPLETION-PLAN.md)
for achieved milestones, remaining review gates, interface decisions and proposed dates.

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

Install KiCad 10 and run from this project's root. Current draft checks:

```sh
kicad-cli sch erc -o docs/interface-review-20260915/erc-final.rpt Osiris_PDB_RevA.kicad_sch
kicad-cli sch export netlist --format kicadxml -o docs/interface-review-20260915/final.net.xml Osiris_PDB_RevA.kicad_sch
python docs/interface-review-20260915/check_review.py
```

The September 12 audit procedure below is historical; do not overwrite its saved
evidence when checking A-P2-DRAFT:

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
