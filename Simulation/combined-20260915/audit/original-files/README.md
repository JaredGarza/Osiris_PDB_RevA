# Combined PDB + Osiris Rev A simulation

Start with **[FINDINGS.md](FINDINGS.md)** for results on the **as-built** board,
**[REVB-PROPOSAL.md](REVB-PROPOSAL.md)** for the proposed fixes, and
**[model_manifest.json](model_manifest.json)** for what is a real vendor model
versus a surrogate. Do not quote a number from here without checking the manifest.

> **The KiCad schematic has NOT been modified.** `REVB-PROPOSAL.md` is a
> simulated, verified proposal awaiting sign-off. The as-built model
> (`pdb/pdb_ap2.lib`) is left untouched so the two can be compared.

**Engine is LTspice 26.0.2, not PSpice.** PSpice is installed but is GUI-only and
unlicensed on this machine. Decks use LTspice-only syntax and will not run under
PSpice without translation. Details in `FINDINGS.md`.

## Layout

```
models/pdb_devices.lib      MOSFET, TVS, Schottky, INA228 stub, 74AUP1G07
pdb/pdb_ap2.lib             PDB_AP2 subckt  (all 42 components, as-built)
pdb/pdb_ap2_revb.lib        PDB_AP2_REVB    (proposed changes, not built)
pdb/component_map.csv       per-designator traceability
osiris/osiris_reva.lib      OSIRIS_REVA subckt + BUCK_AVG / LDO / DIGILOAD
osiris/component_map.csv    per-designator traceability
combined_*.cir              as-built simulations
revb_*.cir                  Rev-B candidate simulations
verify_all.sh               re-runs every deck, reports pass/fail
```

## Running

```sh
bash verify_all.sh                      # everything
"C:/Program Files/ADI/LTspice/LTspice.exe" -b -Run combined_startup.cir
```

Results land in the matching `.log` (`.meas` output) and `.raw` (waveforms).

## The decks

| Deck | Question it answers |
|---|---|
| `pdb/pdb_smoke.cir` | Does the PDB subckt parse and bias up? |
| `pdb/pdb_thresholds.cir` | Where are the UV/OV trip points and their hysteresis? |
| `pdb/pdb_overcurrent.cir` | Fault-resistance sweep — what trips, what doesn't |
| `osiris/osiris_smoke.cir` | Does the Osiris bootstrap chain come up? |
| `combined_startup.cir` | Sequencing, inrush, steady state at 3 pack voltages + degraded harness |
| `combined_faults.cir` | OV excursion, UV sag, hard short, and recovery from each |
| `combined_reverse.cir` | Reverse battery at −14.8 / −16.8 / −25 V |
| `combined_brownout.cir` | Constant-power collapse as the pack sags, by pack impedance |
| `combined_uvchatter.cir` | Is there a pack-voltage window that causes a restart loop? |
| `combined_uvstate.cir` | Single-case probe: is that loop sustained or transient? |
| `revb_thresholds.cir` | Do the Rev-B UV/OV thresholds land where designed? Any OV chatter? |
| `revb_fbnode.cir` | Which hysteresis feedback node actually works? |
| `revb_fbsweep.cir` | Each feedback variant probed across its own window |
| `revb_overcurrent.cir` | Does the 8 mΩ / 5 A pairing close the gap without nuisance trips? |
| `revb_regression.cir` | Does everything that worked before still work? |

## Caveats you must carry

- The **fuse never opens** — it is a fixed cold resistance. 17 A²s is *melting*
  I²t, not clearing.
- **No SOA / thermal / avalanche validity.** Q1/Q2 are datasheet-fitted VDMOS.
- **No buck loop stability or ripple** — AP64501 is an averaged surrogate.
- **No digital or firmware behaviour** on either board.
- Osiris `J24`/`J25` tap raw VIN; external module draw is unbounded and unmodelled.
