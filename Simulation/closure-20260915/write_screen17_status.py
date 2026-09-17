"""Write the current development report from recorded simulator results."""
from pathlib import Path
import json
H=Path(__file__).resolve().parent
suite=json.loads((H/'screen17-results.json').read_text())
fine=json.loads((H/'screen17-fine.json').read_text())
temp=json.loads((H/'screen17-nominal-temperature.json').read_text())
dc=json.loads((H/'screen17-sensor-dc.json').read_text())
rows=suite['results']+[fine['result'],temp['result'],dc]
table='\n'.join('| '+r['deck']+' | '+r['status']+' | '+str(max(map(len,r['measurements'].values()),default=0))+' |' for r in rows)
by={r['deck']:r for r in rows}
nom=by['screen17_nominal.cir']['measurements']
tm=temp['result']['measurements']
fault=by['screen17_faults.cir']['measurements']
fine_m=fine['result']['measurements']
over=by['screen17_temperature.cir']['measurements']
max_delta=max(x['maximum_relative_change'] for x in fine['time_step_comparison'].values())
text=f'''# PDB simulation development status — 2026-09-17

## Decision

The passive blocking-diode candidate passes the recorded voltage and recovery checks, and the planned 7 W Jetson load passes the tested nominal and model-temperature cases. It is **a simulation candidate, not a released schematic**. The added 50% Jetson overload exceeds the existing 2.5 A current target. That failure remains visible; the limit was not relaxed.

The main A-P3 schematic still has the original 60 V MOSFETs and earlier protection circuit (47 component symbols, 45 populated). It does **not** contain this candidate's blocking diode, stronger output clamp or sensor filters. No PDB PCB layout exists. Earlier reports describing48 components/8mΩ/5A are historical, not the current schematic population.

## Recorded tests

| Deck | Result | Cases |
|---|---|---:|
{table}

PASS means the stated screening limits passed, not that every component is qualified. FAIL on corners/temperature comes from overload current. Current and energy measurements without manufacturer pulse/thermal acceptance criteria remain measurements, not passes.

## What changed in the simulation

- Added a100 V series Schottky, upgraded the output clamp, added1Ω/1µF input damping, and evaluated R1=226k to compensate for diode drop. These are in `../combined-20260915/pdb/pdb_screen17.lib` only.
- Added common-mode sensor filters (1µF minimum effective capacitance per input) and a100Ω/100nF VBUS filter.
- Added explicit positive/negative sensor limits, differential input stress, MOSFET/controller limits, diode reverse stress, diode current/energy and resistor energy measurements.
- Corrected the candidate INA228 surrogate: the old10MΩ input resistors implied8.5µA at85 V, inconsistent with the2.5nA active-mode bias specification. The new model uses2.5nA bias and92kΩ typical differential impedance, plus1TΩ numerical shunts (up to85pA additional current). Its dedicated DC tests pass. ADC, protocol, ALERT timing and unpowered leakage remain unmodeled.
- Added a separate nominal-load stimulus: it preserves Osiris hardware and disables only the additional50% Jetson overload step. Original overload decks remain intact.
- Stored source/dependency SHA-256 hashes with the new suite, fine-step and temperature results. Baseline models and newer HV candidate work were preserved.

## Key results

- Nominal load: maximum input current **{max(nom['iin_ss']):.3f} A**; maximum PDB output power **{max(nom['pout_nominal']):.2f} W** at the modeled planning load.
- Nominal load at0/60°C model temperature: maximum input current **{max(tm['iin_ss']):.3f} A**. This does not model board self-heating or all process corners.
- Overload across the0/60°C cases: up to **{max(over['iin_step']):.3f} A**, above2.5 A.
- Blocking-diode loss: up to **{max(nom['d4_power_ss']):.2f} W** nominal at27°C, **{max(tm['d4_power_ss']):.2f} W** across the nominal temperature cases; overload reaches **{max(over['d4_power_step']):.2f} W**. PCB thermal design must support this.
- Fine reversal test: controller VIN minimum **{min(fine_m['u1_vin_min']):.2f} V** against−40 V; added diode reverse stress maximum **{max(fine_m['d4_reverse']):.2f} V** against100 V.
- Reducing reversal maximum step from5µs to1µs changes the six compared voltage/energy metrics by at most **{max_delta*100:.2f}%**. See `screen17-fine.json` for individual comparisons and divider-pin current checks.
- Short test: source peak **{max(fault['sh_ipk']):.1f} A**, integrated source current-squared **{max(fault['sh_i2t']):.4f} A²s**; output clamp peak **{max(fault['d3_ipeak']):.1f} A**. Pulse survivability and fuse clearing are not proven by these numbers.

## Remaining engineering work

1. Decide between the passive candidate's conduction loss and a lower-loss front end. The preserved HVD candidate uses100 V FETs and three parallel TVSs; ideal sharing does not establish real tolerance/current sharing or pulse survivability.
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

The first command intentionally returns a nonzero exit code while the overload exceeds2.5 A. Review `screen17-results.json`, `screen17-fine.json`, `screen17-nominal-temperature.json` and `screen17-sensor-dc.json`. `../combined-20260915/active_decks.json` still represents the earlier schematic-related suite and has not been silently switched to this candidate.

## Sources and limits

Use the locally saved primary datasheets in `../../docs/interface-review-20260915/`: LTC4368 Rev C absolute ratings/Note3; INA228 input ratings and active-mode electrical characteristics. The candidate Schottky fit comes from [ST DS14177](https://www.st.com/resource/en/datasheet/stpst10h100sb.pdf). MOSFET/diode/TVS models are fitted approximations; the Osiris eFuse and converter models are behavioral approximations. No claim of SOA, avalanche, fuse-clearing, thermal or hardware qualification follows from these runs.
'''
for old,new in [('describing48','describing 48'),('a100','a 100'),('added1','added 1'),('a100Ω','a 100 Ω'),('old10','old 10'),('implied8.5','implied 8.5'),('at85','at 85'),('the2.5','the 2.5'),('uses2.5','uses 2.5'),('and92','and 92'),('plus1T','plus 1 T'),('to85','to 85'),('additional50','additional 50'),('at0/60','at 0/60'),('the0/60','the 0/60'),('above2.5','above 2.5'),('at27','at 27'),('from5','from 5'),('to1µs','to 1µs'),('uses100','uses 100'),('exceeds2.5','exceeds 2.5'),('Note3','Note 3'),('1µF','1 µF'),('1Ω','1 Ω'),('100Ω','100 Ω'),('100nF','100 nF'),('50%','50%')]:
 text=text.replace(old,new)
(H/'STATUS.md').write_text(text,encoding='utf-8')
print('Wrote',H/'STATUS.md')
