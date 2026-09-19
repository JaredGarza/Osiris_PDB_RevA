# PDB and Osiris power simulation

Q3 model update: the supplied Infineon 100 V archive has now replaced the fitted Q3 with `BSC070N10NS5_L1`. Earlier 10/11 results below are historical and must not be applied to this changed model. See `Q3-MODEL-VERIFICATION.md` for the new run status.

Latest manufacturer-model verification: [2026-09-18 status](MODEL-VERIFICATION-20260918.md). The previous 9/9 report used fitted Q1/Q2 models and is historical.

Historical pre-Q3 consolidated evidence: `audit/verification-before-q3.json` — 10/11 independent decks passed with the fitted Q3. The three independent transient decks replace one stepped deck, retaining its original cases and limits. Current Q3-model status is in `Q3-MODEL-VERIFICATION.md`; `audit/verification.json` contains only the latest individual invocation.

The active A-P4 KiCad schematic has **59 component symbols, 57 populated**,
a 5 mOhm shunt, a 4 A fuse, an LTC4359/BSC070N10NS5 reverse-current stage,
filtered INA228 inputs and an STPST10H100SB output clamp. The default
`release_*` decks match that population through `pdb/pdb_release.lib`.
The older `screen17_*`, `current_*` and `final_*` decks are preserved design
history and are not the default verification target.
The original [REVIEW.md](REVIEW.md) is a historical review; its population
and values do not describe the current schematic.

## Run

From this directory in PowerShell:

```powershell
python verify_all.py
```

Requires LTspice (default `C:/Program Files/ADI/LTspice/LTspice.exe`) and its
LTC4368-1, LTC4359 and LT3010 models. Pass `--engine` or set `LTSPICE_EXE` to change the executable.
Vendor includes currently use this workstation's installed model paths.
The shell wrapper is optional. These are LTspice decks, not portable PSpice decks.

- `release_*.cir`: live A-P4 KiCad population, using `pdb/pdb_release.lib`.
- `final_*.cir` and `current_*.cir`: earlier A-P3 populations retained for comparison.
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
