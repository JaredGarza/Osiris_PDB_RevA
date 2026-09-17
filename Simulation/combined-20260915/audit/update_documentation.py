from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
p=root/'model_manifest.json';m=json.loads(p.read_text())
m['scope']='Current 48-component A-P2-DRAFT and historical 42-component PDB, each feeding the Osiris Rev A surrogate.'
m['review']='2026-09-15 independent model and schematic audit; see REVIEW.md and audit/verification.json.'
m['current_schematic_model']='pdb/pdb_current.lib; exact populated resistor names, no experimental 1 GOhm feedback branches.'
for model in m['models']:
 if 'LT3010' in model['device']:
  model['limits']='Vendor model, nominal reference 1.275 V. Out-of-range behavior remains unqualified. Phantom external current sinks were removed; do not infer hardware reverse or transient protection from this model alone.'
 if 'F1' in model['device']:
  model['device']='Historical F1 0297004.WXNV 4 A; current F1 0297005.WXNV 5 A'
  model['limits']='Cold resistor only (23.48/17.75 mOhm assumptions carried from older source). No heating/opening/arcing/clearing. Old 17/25 A^2s figures are not acceptance limits. Use current manufacturer time-current data and temperature derating for coordination.'
 if 'LM73100' in model['device']:
  model['limits']='Engineering surrogate, no thermal/fast-trip model. TI SNOSDC0A table 6.7 supports typical open-pin SR=28.1 V/ms and TD=0.1 ms at 12 V; slew varies with input (12.14 V/ms at 2.7 V, 44.78 V/ms at 23 V). A fixed 12 V typical is not a guaranteed bound.'
  model['source']='https://www.ti.com/lit/ds/symlink/lm7310.pdf'
 if 'AP64501' in model['device']:
  model['provenance']='Behavioral average; AP64501 DS41980 Rev 5-2 reviewed.'
  model['limits']='0.8 V reference and 570 kHz verified in manufacturer datasheet. 100 nF soft-start maps to 18.868 ms using Eq.7, replacing 2 ms. IQ/EFF/ILIM/smoothed UVLO and bandwidth remain assumptions. No switching, compensation, peak-current or thermal qualification. Output delivery now requires enable and input headroom.'
  model['source']='https://www.diodes.com/datasheet/download/AP64501.pdf'
 if 'digital consumers' in model['device']:
  model['limits']='Planning loads, not independent measured budgets. Boot ramp now starts after rail rise and resets on collapse. The 50% Jetson step at 600 ms is an arbitrary stress stimulus. Sequencer firmware and actual module demands remain unknown.'
m['review_fixes']=['No supply-independent INA228/buffer/AMS1117 quiescent sinks at zero power.', 'Correct AP64501 capacitor-derived soft start.', 'Buck cannot source through disabled/absent input in the averaged model.', 'Digital-load ramp follows rail validity.', 'Short I^2t includes switch edge at 899.96 ms.', 'Removed unreliable ddt-based edge counter; stable cases no longer require nonexistent retry crossings.', 'Native Windows runner checks completion, return codes, fresh logs, finite measurements and explicit electrical bounds.']
p.write_text(json.dumps(m,indent=2))
(root/'README.md').write_text('''# PDB and Osiris power simulation

Start with [REVIEW.md](REVIEW.md) for the reviewed results and remaining issues.
The active KiCad schematic has **48 components** and already includes the
8 mOhm shunt, 5 A fuse, separate UV/OV dividers and gate-to-UV feedback.

## Run

From this directory in PowerShell:

```powershell
python verify_all.py
```

Requires LTspice (default `C:/Program Files/ADI/LTspice/LTspice.exe`) and its
LTC4368-1/LT3010 models. Pass `--engine` or set `LTSPICE_EXE` to change the executable.
Vendor includes currently use this workstation's installed model paths.
The shell wrapper is optional. These are LTspice decks, not portable PSpice decks.

- `current_*.cir`: current KiCad population, using `pdb/pdb_current.lib`.
- `combined_*.cir`, `pdb/pdb_ap2.lib`: historical 42-component population, with reviewed shared models.
- `revb_*.cir`: experimental feedback/population comparisons; alternative feedback paths are not the active schematic.
- `model_sanity.cir`: supply-off and boot-ramp model invariants.
- `audit/verification.json`: measurements, source hashes and check outcomes.
- `audit/check_connectivity.py`: verifies the exported CAD, both BOMs and model mapping.
- `model_manifest.json`: device provenance and model limitations.

`PASS` means stated electrical screening bounds passed. `RUN_OK` means an
exploratory deck completed with finite measurements; its behavior still needs
engineering interpretation. Missing/failed measurements, timeouts and numerical
warnings fail the runner. Absence of an explicitly tested extra threshold crossing
is the sole intentional missing-measurement exception.

Original files are preserved in `audit/original-files`. Earlier logs/numbers do
not validate the corrected model. Fuses do not open in these models; FET SOA,
thermal behavior, buck control-loop stability and firmware are not qualified.
''')
(root/'FINDINGS.md').write_text('''# Historical 42-component simulation

The original findings have been superseded by [REVIEW.md](REVIEW.md).
The source population remains available in `pdb/pdb_ap2.lib`; the active
schematic is modeled by `pdb/pdb_current.lib`.

The old report used a 2 ms buck soft-start instead of the capacitor-derived
18.868 ms, started short-circuit energy integration after the initial fault
pulse, and included supply-independent current sinks. Its precise timing,
energy, low-voltage behavior and thermal conclusions must not be reused.
The original text is retained in `audit/original-files/FINDINGS.md` for traceability.

The budget comparison was an arithmetic consistency check using shared assumed
loads, not an independent validation against hardware measurements. The weak-pack
retry mechanism remains visible in corrected historical-population simulations.
''')
(root/'REVB-PROPOSAL.md').write_text('''# Gate-feedback candidate: current implementation status

The proposed circuit was already present in KiCad when this review started.
The active schematic uses these actual designators:

| Function | Current population |
|---|---|
| UV divider | R1 1M0 from VBAT_FUSED to LTC_UV; R2 47k to GND |
| OV divider | R3 2M0 from VBAT_FUSED to LTC_OV; R13 54k9 to GND |
| Hysteresis | R14 20M from GATE_PIN to LTC_UV |
| Breaker shunt | R5 8 mOhm |
| Fuse | F1 5 A, 0297005.WXNV, provisional |
| Testpoint pull-ups | R15/R16 10k to PDB_3V3 |
| I2C pull-ups | R17/R18 4.7k to PDB_3V3 |

See [REVIEW.md](REVIEW.md) for results and unresolved electrical limits.
Lowering the electronic trip and raising fuse rating does not establish fuse,
cable or MOSFET coordination. A nominal sweep does not qualify the leakage-
sensitive 20 MOhm feedback network. The circuit does not contain a UV latch;
a settled off state can restart when source voltage changes.

Experimental `revb_*.cir` decks retain alternate feedback branches for comparison.
Use `current_*.cir` for the exact present resistor population.
Original proposal text is retained in `audit/original-files/REVB-PROPOSAL.md`.
''')
