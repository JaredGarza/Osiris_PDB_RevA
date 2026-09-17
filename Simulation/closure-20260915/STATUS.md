# PDB simulation development status — 2026-09-17

## Decision

The passive blocking-diode candidate passes the recorded voltage and recovery checks, and the planned 7 W Jetson load passes the tested nominal and model-temperature cases. It is **a simulation candidate, not a released schematic**. The added 50% Jetson overload exceeds the existing 2.5 A current target. That failure remains visible; the limit was not relaxed.

The main A-P3 schematic still has the original 60 V MOSFETs and earlier protection circuit (47 component symbols, 45 populated). It does **not** contain this candidate's blocking diode, stronger output clamp or sensor filters. No PDB PCB layout exists. Earlier reports describing 48 components/8mΩ/5A are historical, not the current schematic population.

## Recorded tests

| Deck | Result | Cases |
|---|---|---:|
| screen17_nominal.cir | PASS | 8 |
| screen17_transients.cir | PASS | 3 |
| screen17_corners.cir | FAIL | 8 |
| screen17_faults.cir | PASS | 1 |
| screen17_reverse25.cir | PASS | 1 |
| screen17_temperature.cir | FAIL | 16 |
| screen17_transients_fine.cir | PASS | 3 |
| screen17_nominal_temperature.cir | PASS | 16 |
| screen17_sensor_dc.cir | PASS | 3 |

PASS means the stated screening limits passed, not that every component is qualified. FAIL on corners/temperature comes from overload current. Current and energy measurements without manufacturer pulse/thermal acceptance criteria remain measurements, not passes.

## What changed in the simulation

- Added a 100 V series Schottky, upgraded the output clamp, added 1 Ω/1 µF input damping, and evaluated R1=226k to compensate for diode drop. These are in `../combined-20260915/pdb/pdb_screen17.lib` only.
- Added common-mode sensor filters (1 µF minimum effective capacitance per input) and a 100 Ω/100 nF VBUS filter.
- Added explicit positive/negative sensor limits, differential input stress, MOSFET/controller limits, diode reverse stress, diode current/energy and resistor energy measurements.
- Corrected the candidate INA228 surrogate: the old 10MΩ input resistors implied 8.5µA at 85 V, inconsistent with the 2.5nA active-mode bias specification. The new model uses 2.5nA bias and 92kΩ typical differential impedance, plus 1 TΩ numerical shunts (up to 85pA additional current). Its dedicated DC tests pass. ADC, protocol, ALERT timing and unpowered leakage remain unmodeled.
- Added a separate nominal-load stimulus: it preserves Osiris hardware and disables only the additional 50% Jetson overload step. Original overload decks remain intact.
- Stored source/dependency SHA-256 hashes with the new suite, fine-step and temperature results. Baseline models and newer HV candidate work were preserved.

## Key results

- Nominal load: maximum input current **2.137 A**; maximum PDB output power **23.45 W** at the modeled planning load.
- Nominal load at 0/60°C model temperature: maximum input current **2.151 A**. This does not model board self-heating or all process corners.
- Overload across the 0/60°C cases: up to **2.565 A**, above 2.5 A.
- Blocking-diode loss: up to **1.11 W** nominal at 27°C, **1.26 W** across the nominal temperature cases; overload reaches **1.53 W**. PCB thermal design must support this.
- Fine reversal test: controller VIN minimum **-18.89 V** against−40 V; added diode reverse stress maximum **67.89 V** against100 V.
- Reducing reversal maximum step from 5µs to 1µs changes the six compared voltage/energy metrics by at most **0.22%**. See `screen17-fine.json` for individual comparisons and divider-pin current checks.
- Short test: source peak **141.7 A**, integrated source current-squared **0.0958 A²s**; output clamp peak **94.1 A**. Pulse survivability and fuse clearing are not proven by these numbers.

## Remaining engineering work

1. Decide between the passive candidate's conduction loss and a lower-loss front end. The preserved HVD candidate uses 100 V FETs and three parallel TVSs; ideal sharing does not establish real tolerance/current sharing or pulse survivability.
2. Select and validate effective capacitor values, diode pulse/thermal behavior, damping-resistor pulse rating, connector/harness limits and fuse coordination. Fit sensor accuracy/settling requirements to its added filters.
3. Extend source/edge/parasitic and component-tolerance sweeps, including sensor-filter mismatch. These tests cover selected cases, not every possible battery/harness.
4. Apply the accepted circuit to CAD, reconcile BOM/netlist/model, run ERC and visually inspect the schematic. Continue PCB thermal, routing, EMI and bench validation once a layout exists.
5. Keep the known weak-source UV cycling visible. Do not claim a high-resistance source meets the normal operating envelope.

## Reproduce

Run from the project root:

```powershell
python Simulation/closure-20260915/develop_protection.py
python Simulation/closure-20260915/refine_screen17.py
python Simulation/closure-20260915/check_nominal_temperature.py
python Simulation/closure-20260915/check_sensor_model.py
python Simulation/closure-20260915/write_screen17_status.py
```

The first command intentionally returns a nonzero exit code while the overload exceeds 2.5 A. Review `screen17-results.json`, `screen17-fine.json`, `screen17-nominal-temperature.json` and `screen17-sensor-dc.json`. `../combined-20260915/active_decks.json` still represents the earlier schematic-related suite and has not been silently switched to this candidate.

## Sources and limits

Use the locally saved primary datasheets in `../../docs/interface-review-20260915/`: LTC4368 Rev C absolute ratings/Note 3; INA228 input ratings and active-mode electrical characteristics. The candidate Schottky fit comes from [ST DS14177](https://www.st.com/resource/en/datasheet/stpst10h100sb.pdf). MOSFET/diode/TVS models are fitted approximations; the Osiris eFuse and converter models are behavioral approximations. No claim of SOA, avalanche, fuse-clearing, thermal or hardware qualification follows from these runs.
