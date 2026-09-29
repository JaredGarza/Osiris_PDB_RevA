# Osiris PDB Rev A

**Current layout: [29 September compact XT60 routing candidate](COMPACT_XT60_ROUTE_REVIEW_2026-09-29.md). The 60 A continuous / 100 A for 30 s target is not qualified; do not order this board.** The [28 September manufacturing review](MANUFACTURING_REVIEW_2026-09-28.md) describes the preceding layout.

The current `A-P5-DRAFT` schematic and compact PCB candidate have three XT60
power connections: J1 battery input, J3 ESC output, and J4 avionics output.
J2 is the four-pin I²C data connector. Earlier simulation, purchasing, and
assembly exports describe older populations. The root `BOM.csv` and
`BOM_purchasing.csv` are historical exports.
Open `Osiris_PDB_RevA.kicad_pro` in KiCad 10. Project libraries use `${KIPRJMOD}`.
This folder and its `origin` remote are the **power distribution board only**.
The active Osiris Rev B main-board project is in the separate
[Hardware repository's Osiris Rev B branch](https://github.com/modifly-technologies/Hardware/tree/codex/osiris-revb-power-route/OSIRIS_RevB), at
`OSIRIS_RevB/OsirisRevB.kicad_pro`.

**Current electrical draft:** U3 is LT3010 with R11/R12/C10.
See the [earlier electrical review](docs/PDB-ELECTRICAL-REVIEW-20260915.md) and
[proposed interface](docs/PDB-INTERFACE-PROPOSAL-20260915.md). Actual loads and
mechanical constraints remain undecided; negative-input protection and fault
qualification remain open. The previous parts baseline is historical.

**Historical parts-planning baseline: 13 September 2026.** See the
[freeze note](procurement/2026-09-13/FREEZE-NOTE.md) and
[parts workbook](outputs/procurement-20260913/PDB-RevA-Parts-Planning.xlsx).
This is a historical PDB parts-planning baseline. Current Osiris Rev B power
path work lives in the separate Hardware repository above.

See the [PDB and Osiris completion plan](docs/PDB-AND-OSIRIS-COMPLETION-PLAN.md)
for achieved milestones, remaining review gates, interface decisions and proposed dates.

**Not flight-ready. Electrical and JLCPCB assembly checks remain open.** Start with
[Rev A readiness and completion plan](docs/REV-A-READINESS.md) and
[current scope](DESIGN-SPEC.md).

Older competing PDB projects and local backup directories are preserved in an
external dated archive on the original workstation; they are not required to open
this repository. Consult that archive's move manifest to restore local copies.
Historical apply scripts and review documents record earlier revisions and must not
be treated as instructions to regenerate the current design.

## Repository contents and checks

The current schematic, PCB, project-local libraries, engineering and purchasing
BOMs, datasheets, simulation sources and review evidence are versioned together.
Full Osiris board imports, editor state and LTspice binary outputs are kept out
of Git. The current PCB is a draft under manufacturing review.

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
