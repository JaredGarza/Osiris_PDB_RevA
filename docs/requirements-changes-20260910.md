> HISTORICAL SNAPSHOT — superseded for readiness decisions by `docs/REV-A-READINESS.md`
> (project-relative path). Includes unvalidated claims about maximum load, fuse coordination,
> clamp margin and/or earlier wiring. Use the current schematic and fresh audit results.

# Applied schematic changes — 10 September 2026 (requirements pass)

Source: the user's saved `Osiris_PDB_RevA.kicad_sch` after the fuse/connector pass.
Pre-edit backup in `requirements-backup-20260910/`. Reasoning and derivations are in
[requirements-20260910.md](osiris-power-audit/requirements-20260910.md); this file
records only what changed in the schematic.

Applied by `apply_requirements_edits.py`, checked by `verify_requirements_edits.py`.
Both are re-runnable: the apply script refuses to overwrite an existing backup and uses
deterministic UUIDs, so restoring the backup and re-running reproduces the same file.

## D1 — F1 finalised at 4 A

`5A MINI` / `0297005.WXNV` → **`4A MINI` / `0297004.WXNV`**. The PROVISIONAL marking is
gone; the design maximum of 2.22 A is now established, giving 3.00 A of continuous
capability at the 75% convention (1.35× margin) and reducing fault let-through from
25 to 17 A²s. Datasheet now points at the locally archived
`Datasheets/Littelfuse_297_MINI.pdf`, whose ratings table is the source for those
figures.

## D2 — gate network moved to LTC4368 Figure 11

Previously the GATE pin tied straight to both MOSFET gates, with R4 + C1 forming a
series RC to ground. R4 was therefore not in the position the datasheet specifies, so
its documented reverse-hot-plug function was absent.

The net names now separate the two halves of the network:

| Net | Nodes |
|---|---|
| `GATE_PIN` | U1.10 (GATE), C1.1, R4.2, D2.1 (cathode) |
| `GATE_FET` | Q1.4, Q2.4, R4.1, D2.2 (anode) |

- **C1** (5n6) is now CGATE, directly on the GATE pin. It still sets the 6.25 kV/s
  turn-on ramp, so inrush is unchanged at ≈ 0.82 A.
- **R4** (22 k) is now RGATE, in series between the GATE pin and the MOSFET gates.
- **D2 — new part**, MBR0540T1G in SOD-123, across R4 with its cathode on the GATE-pin
  side. **This diode is not optional.** Without it the fast pull-down has to discharge
  2 × 6.9 nF of Ciss through 22 kΩ, degrading fault turn-off from 8 µs to ≈ 300 µs and
  defeating the breaker.

No wires moved. The change is entirely in the net labels plus the new diode, which is
why the existing gate wiring is byte-identical to before.

`CHOTSWAP` was evaluated and **deliberately not fitted** — with Crss ≤ 96 pF against
5.6 nF on the gate node, a 16.8 V hot-plug couples only 0.28 V, eight times below the
2.25 V minimum gate threshold.

## D3 — J2 re-pinned to mate with Osiris J28

The old 6-way pinout could not connect to anything: Osiris's own INA228 bus (FMU_I2C4)
never reaches a connector, and no Osiris GH connector exposes a spare GPIO or +3V3 for
the two status lines.

`BM06B-GHS-TBT` 6-way → **`BM04B-GHS-TBT` 4-way**, footprint
`Connector_JST:JST_GH_BM04B-GHS-TBT_1x04-1MP_P1.25mm_Vertical`, mating housing
`GHR-04V-S`. Value changed `OSIRIS_CTRL` → `OSIRIS_I2C`.

| Pin | Was | Now | Osiris J28 |
|---|---|---|---|
| 1 | GND | no-connect | +5V0_PROT |
| 2 | SDA | `PDB_I2C_SCL` | FMU_I2C1_SCL |
| 3 | SCL | `PDB_I2C_SDA` | FMU_I2C1_SDA |
| 4 | INA_ALERT_N | GND | GND |
| 5 | PDB_FAULT_N | — | — |
| 6 | NC | — | — |

This is a straight 1:1 map to Osiris J28, so a stock 4-way GH-to-GH cable works and the
custom-cable requirement is retired. Pin 1 faces the Osiris +5V0_PROT contact and is
intentionally left open.

`INA_ALERT_N` and `PDB_FAULT_N` now terminate on **TP6** and **TP7** (new test points)
instead of the connector. U4 and R10 are retained so a later Osiris revision can pick
the signals up without a respin.

## D4 — U3 supply moved ahead of the MOSFETs

U3's IN (pin 8) and EN (pin 5) moved from `PDB_VOUT` to `VBAT_FUSED`, carrying **C4**
(10 µF/50 V) with them — which is exactly the 10 µF from IN to GND that the TPS7A16
datasheet recommends. Costs ≈ 0.65 mA of standing battery drain.

Be precise about the benefit: Osiris is powered only through PDB_VOUT, so it also dies
on a trip and cannot read the monitor during one. What this actually buys is that the
INA228 retains its configuration and accumulated charge/energy registers across the
550 ms retry cycle rather than resetting, and that PDB_3V3 is live for bench probing
with the output off.

**C9 — new part**, 10 µF/50 V 1206 (same MPN as C4), added on `PDB_VOUT` to keep local
bulk at the output connector and hold total load capacitance at the 131 µF used in the
inrush calculation.

## D5 — bidirectional input clamp

**D1 — new part**, SMAJ24CA in SMA, from `VBAT_FUSED` to GND.

Note the substitution: the part discussed was SMAJ24**A**, but a unidirectional TVS
would forward-conduct on a reversed pack, shorting the battery through F1 and destroying
the reverse-battery tolerance the LTC4368 and back-to-back MOSFETs exist to provide.
SMAJ24**CA** is the bidirectional version — same 24 V standoff, 26.7 V minimum
breakdown (clear of the 19.33 V worst-case OV corner) and 38.9 V clamp (well under the
60 V MOSFET rating), but it blocks in both directions.

## D6 — output negative-voltage clamp

**D3 — new part**, MBR0540 in SOD-123, cathode to `PDB_VOUT`, anode to GND.

This one came out of the cascade simulation rather than the requirements document.
With a reversed pack on the input, the modelled `PDB_VOUT` node was driven to roughly
−0.8 V. That did not matter while U3 hung off the unprotected side, but D4 moved U3's
supply onto `PDB_VOUT`, and the TPS7A1633 IN pin has a −0.3 V absolute maximum. The
clamp shunts the negative excursion to GND before it reaches U3.

After adding it, `MIN(V(PDBOUT))` over the reverse-input window is −0.052 V in all
eight cases — inside the −0.3 V limit.

**Treat that margin as provisional.** The simulation models D3 with the same generic
`DBYP` behavioural diode used for the D2 gate bypass (`Is=1u N=1.1 Rs=.15`), not an
extracted MBR0540 model. A real Schottky drops more at the same current, so −0.052 V is
optimistic. The part's `Selection_Status` field carries the same caveat: worst-case
forward voltage and pulse current need confirming on hardware.

Note a naming collision worth fixing before this document is circulated: the decision
IDs in these headings (D1–D6) and the diode reference designators (D1, D2, D3) are
different things that happen to share names. "D3 — J2 re-pinned" is a decision;
"**D3 — new part**" here is a diode.

## Unchanged, and asserted so

Protection thresholds were left alone as requested, and the verification script asserts
it rather than assuming it: R1/R2/R3 UV and OV dividers, the R6/R7 SHDN divider, the
R5 Kelvin taps and their forward-positive sense polarity, the C2 ≥ 1 µF on the LTC4368
VOUT pin, and J1/J3 polarity. All wire and junction geometry is unchanged.

## Validation

- ERC: 0 errors, 0 warnings (`erc-requirements.rpt`)
- Netlist assertions on every changed and every deliberately-unchanged net
  (`verify_requirements_edits.py` against `requirements.net.xml`)
- 39 BOM rows, every footprint resolves in its library, every `${KIPRJMOD}` datasheet
  path resolves on disk
- Rendered to `review-render/requirements.pdf` and `review-render/Osiris_PDB_RevA.svg`,
  both regenerated after D3 was placed. D3 sits at (111.76, 153.67); nearest neighbouring
  symbol is C6, 19 mm away, so nothing overlaps, though D3's value text and C6's landed
  about 2 mm apart and could stand tidying.
- `review-render/requirements.png` is **stale** — it predates D3 and does not show it.
  No rasteriser is installed on this machine (no ImageMagick, poppler or Inkscape), so
  it could not be regenerated here. Use the PDF or SVG.

## Parts added

| Ref | Value | MPN | Footprint |
|---|---|---|---|
| C9 | 10u 50V X7R | C3216X7R1H106K160AC | Capacitor_SMD:C_1206_3216Metric |
| D1 | SMAJ24CA | SMAJ24CA | Diode_SMD:D_SMA |
| D2 | MBR0540 | MBR0540T1G | Diode_SMD:D_SOD-123 |
| D3 | MBR0540 | MBR0540T1G | Diode_SMD:D_SOD-123 |
| TP6 | TestPoint | — | TestPoint:TestPoint_Pad_D1.5mm |
| TP7 | TestPoint | — | TestPoint:TestPoint_Pad_D1.5mm |

## Datasheets added

Four PDFs that previously failed to download are now archived locally. `origin` in
`Datasheets/sources.json` records manufacturer-direct versus distributor mirror for each.

| File | Origin |
|---|---|
| `Littelfuse_297_MINI.pdf` | mirror (ficcorp.com) — ratings, I²t, derating curve |
| `Ohmite_FC4L.pdf` | mirror (tti.com) — confirms FC4L64 is the 2 W 6432 part |
| `Bourns_SMAJ_TVS.pdf` | manufacturer (bourns.com) — SMAJ24CA row |
| `onsemi_MBR0540.pdf` | mirror (reichelt) |

TDK characteristic sheets remain 403-blocked; those capacitors keep manufacturer product
pages in the schematic.

## Still open

Cascade simulation results for these changes are in
[`simulation-cascade-20260910.md`](simulation-cascade-20260910.md). Two items from it
bear on this pass:

- **Fault coordination is resolved.** Worst-case let-through on an output short is
  0.190 A²s against the 0297004's 17 A²s melting I²t — about 89× margin. The schematic
  note still reads "fault coordination pending" and can be updated.
- **MOSFET SOA is not.** The simulation substitutes a `SiR870ADP` for the fitted
  `ISC015N06NM5LF2`, so the 134–155 A short-circuit peak is not an SOA verdict on the
  actual part. This is the largest remaining unknown.

`DESIGN-SPEC.md` describes a different board — a four-output ESC distributor with an
80 A motor bus, 1000 µF bulk and no LTC4368. It contradicts the built schematic on
topology, current rating and part selection, and its SMCJ17CA choice is electrically
incompatible with the OV threshold. It needs rewriting against the requirements document
or explicit retirement.
