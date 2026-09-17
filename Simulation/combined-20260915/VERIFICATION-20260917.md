# A-P4 PDB + Osiris power-path verification — 2026-09-17

## Result

The current A-P4 PDB schematic passes the recorded LTspice screening suite: **9 of 9 active decks passed**. KiCad ERC reports **0 violations**. The live schematic, both BOMs and the A-P4 SPICE population pass the connectivity/value check.

This is a circuit-screening result, not fabrication or flight qualification. The Osiris circuit is still a Rev A behavioral surrogate because a current Rev B power schematic and measured load profile are not present in the workspace.

## Verified source

- PDB schematic: 59 symbols, 57 populated; R17/R18 are DNP.
- PDB model: `pdb/pdb_release.lib`.
- Combined model: PDB A-P4 feeding the Osiris Rev A behavioral power/load model.
- Simulator: LTspice 26.0.2.
- Evidence: `audit/verification.json`, `audit/connectivity.json`, and `../../docs/erc-latest.rpt`.

## Active deck results

| Deck | Result | Purpose |
|---|---|---|
| `release_corners.cir` | PASS | 12/16.8 V startup, source/harness and slew cases |
| `release_lowtrip.cir` | PASS | conservative breaker/startup margin |
| `release_temperature.cir` | PASS | 0/60 °C model sweep |
| `release_faults.cir` | PASS | OV, UV, short and recovery |
| `release_faults_fine.cir` | PASS | short result at finer timestep |
| `release_reverse.cir` | PASS | −14.8/−16.8 V reverse input and recovery |
| `release_reverse25.cir` | PASS | −25 V reverse input and recovery |
| `release_transients.cir` | PASS | 0.2/2/20 µH hot-plug/reversal sensitivity |
| `model_sanity.cir` | PASS | unpowered and boot-ramp invariants |

## Notable worst-case measurements

- Steady rails: 5.161–5.162 V, 3.3047–3.3054 V; PDB local rail 3.2793–3.2829 V.
- Startup source-current peak: 5.57 A maximum in the selected corner sweep.
- Modeled load-step current: 2.43 A maximum.
- Short recovery: 3.3 V returned at 1.537 s; short I²t was approximately 0.12 A²s.
- INA228 short-event differential: 313.7 mV. This exceeds its ADC range and temporarily saturates telemetry, but remains far below the ±40 V absolute differential rating.
- Q3 transient VDS: 63.22 V maximum against the 100 V rating.
- Q3 transient VGS: 12.50 V maximum against the ±20 V rating.
- LTC4359 IN relative to VSS: −35.21 V minimum against the −40 V absolute limit. This is the narrowest recorded voltage margin and needs real parasitic/harness validation.
- Filter-capacitor stress: C11 32.92 V maximum; C16 46.86 V maximum against 63 V nominal parts.
- INA228 IN+/IN−/VBUS negative excursions remained within the −0.3 V absolute limit in the tested cases.

## Corrections made during this verification

- Switched the default suite from the stale A-P3 `final_*` decks to the live A-P4 `release_*` decks.
- Updated the connectivity checker to export and verify the live 59-symbol KiCad schematic against `pdb_release.lib`.
- Reconciled both BOMs with C11–C16, D4, Q3, R19–R21, U5 and the current D3 clamp.
- Corrected the INA228 differential damage limit from an unsupported 0.3 V assumption to the datasheet ±40 V absolute rating; ADC saturation remains reported.
- Fixed runner timeout handling so a timed-out LTspice child cannot remain active indefinitely; default timeout is now 300 s.
- Runner failure-injection tests pass 8 of 8.

## Open qualification items

- Q1/Q2/Q3 MOSFET SOA, avalanche, thermal impedance and repeated-fault survival are not represented by the fitted models.
- D1/D3/D4 pulse energy, temperature and production tolerance need vendor models plus bench correlation.
- The fuse is modeled as resistance only; opening, arcing and interrupt capability are not simulated.
- The Osiris LM73100, AP64501 converters and digital loads are behavioral models. A current Rev B schematic and measured startup/steady/transient load profile are required for combined-system signoff.
- PCB parasitics, thermal design, EMI, firmware sequencing, I2C operation and physical connector polarity require layout/bench tests.
