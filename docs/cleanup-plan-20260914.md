# Osiris PDB Rev A — schematic cleanup, 2026-09-14

**Status: applied and verified.** Documentation, title block and field presentation only.
No symbol, pin, wire, label, footprint or net was changed.

## Verification summary

| Check | Result |
|---|---|
| ERC (`kicad-cli sch erc`) | 0 violations |
| Netlist nets | 28 before, 28 after, connectivity byte-identical |
| Component references | 47, unchanged |
| Wires / junctions / no-connects | 62 / 17 / 6, unchanged |
| Pins, footprints, lib_ids | unchanged |
| UUIDs | all 333 unchanged (no re-annotation) |
| Netlist component values | 1 intended change (R5), 38 unchanged |
| File encoding | still pure ASCII, still CRLF |
| Plotted text outside A4 frame | none |

Backups: `Osiris_PDB_RevA.kicad_sch.pre-cleanup.bak`, `BOM.csv.pre-cleanup.bak`,
`BOM_purchasing.csv.pre-cleanup.bak`.

## Baseline established before editing

Compared the uncommitted working tree against `HEAD` (722d665). The 2,195-insertion /
2,209-deletion diff was almost entirely KiCad re-sorting the cached `lib_symbols` block.
Only two substantive differences existed, neither of them mine:

1. The `title_block` had been **deleted** — invisible to ERC and to the netlist.
2. One added wire segment `(55.88 40.64) -> (55.88 36.83)`, a stub carrying `VBAT_FUSED`
   off the fuse pin to its label. Correct as drawn; kept.

`Osiris_PDB_RevA.kicad_pro` differed only by a reordered `used_designators` string.
**No ERC rule was disabled or downgraded**, so the clean ERC result is meaningful.

## Edits applied

### 1. Restored the deleted title block

```
(title "Osiris PDB - procurement baseline")
(date "2026-09-14")
(rev "A-P1")
(comment 1 "Parts planning only; new Osiris Rev B power interface pending")
(comment 2 "Design review draft - see DESIGN-SPEC.md for open validation items")
```

Plots at the bottom-right with 3.67 mm clearance above the drawing.

### 2. Reworded over-claimed component notes

Each stated a verified result where only an assumption or an intent existed.

- **D2** — dropped "without it fault turn-off degrades from 8 us to about 300 us". The
  LTC4368 datasheet supports the bypass-diode arrangement but does not yield those two
  numbers, and nothing in `Simulation/` produces them. Now: "Fast turn-off diode across
  R4, per the LTC4368 Figure 11 gate network. Turn-off timing not yet measured or
  simulated."
- **C9** — was claiming the inrush calculation still held. Now states it must be re-run
  against the final load capacitance before release.
- **J2** — was claiming a verified mate with a stock cable. Now scoped to the Osiris
  **Rev A** J28 pinout, with cable and mating called out as unverified.
- **J2 sheet note** — first line said "mates 1:1", contradicting the title-block comment
  that the Rev B interface is pending. Now "pinned 1:1 to Osiris Rev A J28 … Unverified
  against Rev B."

### 3. R5 value presentation

R5 was the only passive whose `Value` was a manufacturer part number, so the
current-sense shunt rendered on the drawing as `FC4L64R005FER`.

- `Value`: `FC4L64R005FER` -> `5m` (consistent with `5n6`, `22k`, `4k7`, …)
- `Description`: `""` -> `5 mOhm 1% 2W`, made visible

Plots as a clean `R5` / `5m` / `5 mOhm 1% 2W` stack at 2.4 mm spacing, nearest unrelated
text 8.7 mm away. ASCII `mOhm` deliberately — the file contains no non-ASCII characters
and should stay that way.

### 4. Tightened the two sheet notes

Both mixed live constraints with historical rationale. Regrouped so unresolved work sits
under explicit `OPEN:` markers at the end of each note rather than buried mid-prose.

## Corrections made during the work

Two mistakes caught before they shipped, recorded so they are not repeated:

- I first added a new `Specification` property to R5. **Wrong** — the BOM's
  `Specification` column maps to the schematic's `Description` property. The invented
  field would never have reached the BOM. Removed and redone as `Description`.
- I was about to regenerate `BOM.csv` with `kicad-cli sch export bom`. **That would have
  destroyed hand-curated procurement data** — see below.

## BOM handling

`BOM.csv` and `BOM_purchasing.csv` are **not** raw KiCad exports. A fresh export differs
from the committed file in ways that lose real information:

| Field | Committed | Raw re-export |
|---|---|---|
| Q1/Q2 `MPN` | `ISC015N06NM5LF2ATMA1` | `ISC015N06NM5LF2` |
| Q1/Q2 `Selection Status` | tape-and-reel note | *(empty)* |
| R1–R10 / TP1–TP7 `Specification` | blank | `Resistor` / `test point` |

The Q1/Q2 tape-and-reel order code exists only in the CSV. Both files were therefore
patched at the single R5 line; every other byte is unchanged, and the R5 **MPN is
unchanged**, so nothing procurable moved.

## Procurement freeze status — needs a decision

`procurement/2026-09-13/freeze-manifest.json` SHA-256s the design files. Current state:

| File | vs. frozen A-P1 |
|---|---|
| `Osiris_PDB_RevA.kicad_sch` | differs — **already did before this cleanup** (title-block deletion) |
| `Osiris_PDB_RevA.kicad_pro` | differs — pre-existing designator reorder |
| `BOM.csv` | differs — R5 row, this cleanup |
| `BOM_purchasing.csv` | differs — R5 row, this cleanup |
| all libraries, footprints, 3D models | match |

The A-P1 freeze is superseded. Re-freezing is a procurement decision and was left alone;
the manifest has **not** been regenerated.

## Deliverables

- `outputs/review-20260914/Osiris_PDB_RevA-schematic.pdf`
- `docs/erc-post-cleanup.rpt` — 0 violations

## Deliberately NOT changed

- **C1's "sets the 6.25 kV/s turn-on ramp."** Unlike the D2 claim this is a real
  derivation: 35 uA into 5.6 nF is exactly 6.25 kV/s. Confirm the LTC4368 GATE pull-up
  current against the datasheet and it stands on its own.
- The `VBAT_FUSED` wire stub — correct as drawn.
- The provisional/pending `Selection_Status` strings on F1, D1, D3 and the MOSFETs. They
  already read as open items, which is accurate.

## Still open — engineering, not documentation

1. **U3 reverse-bias during an output short.** Input can collapse while the 3V3 output
   cap stays charged; TI limits OUT above IN to 0.3 V. D3 clamps output-to-ground and
   does not address this.
2. **Protection coordination.** Provisional 4 A fuse, 10 A nominal electronic trip, TVS
   clamp and MOSFET fault survival are not verified as a coordinated set.
3. **Footprint dimensions.** Consistent and assigned; not checked against physical parts.
4. **Q1/Q2 MPN drift.** The schematic carries `ISC015N06NM5LF2`, the BOM
   `ISC015N06NM5LF2ATMA1`. Deliberate per the BOM note, but worth stating out loud if a
   reviewer asks why they disagree.
