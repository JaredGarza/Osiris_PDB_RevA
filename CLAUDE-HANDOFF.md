# PDB engineering handoff — 2026-09-16

## User instruction

Continue the PDB schematic and SPICE review, correct every substantiated issue, and deliver clean, readable engineering files. Schematic edits are authorized. Preserve unrelated work. There is **no PDB PCB layout yet**. Retain the existing Osiris hardware and its planned 7 W Jetson mode; do not require an Osiris board modification. Verify changes with real SPICE runs, connectivity checks, ERC and visual inspection. Do not describe a converged simulation as hardware qualification.

## Workspace and tools

- Project: `C:/Users/jared/Desktop/PCB/Kicad/Osiris_PDB_RevA` (many existing uncommitted changes).
- Schematic: `Osiris_PDB_RevA.kicad_sch`, A-P3-DRAFT.
- LTspice: `C:/Program Files/ADI/LTspice/LTspice.exe` v26.
- KiCad CLI: `C:/Program Files/KiCad/10.0/bin/kicad-cli.exe`.
- Python: `C:/Python314/python.exe`.
- Current simulation directory: `Simulation/combined-20260915` (S below).
- Working review directory: `Simulation/closure-20260915` (H below).
- `S/verify_all.py` runs LTspice and checks fresh completed logs, finite measurements, step counts and specified limits. PASS requires defined electrical limits; RUN_OK only means a completed run. It overwrites `S/audit/verification.json` each invocation. `S/audit/test_runner.py` has eight failure-injection checks, previously passing.

## Changes already in the MAIN schematic

- Correct LTC4368 gate topology: GATE directly drives Q1/Q2; R4 22k and C1 22n form a **series branch** to ground. D2 removed. Old wiring slowed fault turnoff incorrectly.
- C1 `C2012C0G2A223J125AC`, 22nF, 100V, C0G, 5%.
- R5 `FC4L64R005FER`, 5mΩ, 1%, four-terminal 2W. Nominal breaker 10A, normal min/max approximately 7.92–12.12A. F1 remains 4A `0297004.WXNV`; conductor/fuse coordination is still open.
- UV divider R1 237k, R2 11k8, gate feedback R14 22M 5%. See `H/divider-bounds.json` for tolerance assumptions and bounds. Nominal cold UV-on 11.075V; assumed worst cold-on 11.793V.
- R17/R18 I²C pulls DNP; host owns pulls to switched 3.3V. Calibration SHUNT_CAL=3277 at 50µA/LSB, ADCRANGE=0, address0x40.
- Actual Osiris R74/R75 are **12k** to 3V3. The schematic note now states 100kHz and <=90pF total capacitance, replacing erroneous 200pF. `H/i2c.json` RC timing passed (worst rise ~0.968µs). Protocol/unpowered leakage not modeled.
- J2 pin1 NC, pin2 SCL, pin3 SDA, pin4 GND. Osiris J28 pin1 is +5V0_PROT: leave disconnected at PDB. Do not connect it to PDB power.
- R16–R18 grid/overlap corrections previously applied. Last ERC before the latest note change was zero warnings/errors. Need fresh render/ERC after final edits.
- Current main schematic has 47 physical symbols, 45 populated. `S/pdb/pdb_final.lib` matches this population. **All new transient-protection candidates below are simulation-only.**

## Existing successful screening

`H/core-initial.json` preserves initial final-suite results. Later individual runs are in H JSON files. `S/audit/verification.json` is not a complete consolidated result.

- final_corners: 8 startup/load cases passed; final_lowtrip: 8 passed; final_temperature: 16 passed at model 0/60C.
- final_faults passed startup, UV/OV and short recovery; fine rerun passed. Short peak ~172.17A, I²t~0.152766A²s. Fine test stop shortened to1.12s with1µs max timestep, preserving entire short window; coarse3s test covers recovery.
- final_reverse and final_reverse25 passed **slow** reversal/recovery tests.
- Actual Osiris model `S/osiris/osiris_reva.lib` retained: eFuse dVdt pins open. Do not use `osiris_eco.lib` as final hardware configuration.
- Load planning: Jetson7W included within 5V-domain2.5A, 3V3-domain2A, assumed85% efficiency, ~23.07W total input estimate. 600ms stress adds50% Jetson load: this is an overload sensitivity, not continuous7W operation.
- final_weak_source shows UV cycling with high source resistances500–900mΩ. It is exploratory RUN_OK, not acceptable normal operation. Source/harness normal assumption is much lower (~75mΩ). Do not claim weak-source cycling fixed.

## Critical defects found in deeper tests

1. `final_transients.cir`: fast charged-output reversal (+16.8 to−25V in10µs), source inductance0.2/2/20µH, sourceR20mΩ, output220µF/6.72Ω. Original model times out from ringing. Adding1Ω+1µF series input damping converges but exposes VIN down to−62.49V and Q2 VDS~61.85V. LTC4368 VIN abs min−40V; Q1/Q2 rating60V. Bigger TVS alone did not solve all corners. SMCJ24CA and SM8S24CA candidates are **not approved fixes**.
2. `H/sensor-fault.json` / `S/sensor_fault.cir`: fine short test revealed INA228 IN+ −7.31V, IN− −7.70V, VBUS −7.65V. Limit−0.3V. Existing MBR0540 clamp insufficient. Earlier recovery-only PASS missed pin stress.
3. `H/filter-fault.json`: adding1µF **minimum effective** from each INA input to ground (existing10Ω series resistors retained), plus100Ω/100nF VBUS filter, reduces all three sensor minima to roughly−22µV. Candidate in `S/pdb/pdb_filter.lib`. Not yet applied to CAD. Need real capacitance with bias/tolerance, measurement accuracy/settling analysis and stronger power freewheel diode.

## Latest promising candidate — CHECK FIRST

Script `H/test_passive_protection.py` was running when handoff began (Python PID5968, LTspice PID26288 at last check; verify before doing anything with processes). It writes `H/passive-protection.json` after each of two tests.

`S/pdb/pdb_passive.lib` starts with the sensor filters, then:

- Adds series100V10A Schottky D4 after fuse and before existing protected electronics.
- Adds R20=1Ω plus C11=1µF series damping from D4 input to ground.
- Replaces D3 with the same stronger power Schottky.
- Changes candidate R1 to226k to account for input diode forward drop.
- Uses a **datasheet-fitted, non-vendor** `STPST10H100_SCREEN` model: Is70n,N1.1,Rs.018,Cjo2n,BV100,IBV26u,Tnom25. VF fitted to ST max25C points. Recovery/leakage/avalanche/thermal behavior NOT validated.
- Intended real part candidate: ST `STPST10H100SB-TR`, active DPAK100V10A. Has two anode terminals that must both connect. Verify symbol/footprint mapping from datasheet before CAD use.

Latest `passive_transients` completed14.4s RUN_OK, all three inductances: sensor minima only~−44µV; U1 VIN min−18.84V/max32.35V; Q1 VDSmax33.44V; Q2 VDSmax18.41V; gate-source max13.55V; local3V3max3.288V; finaloutput16.143V. **No electrical limits were attached yet**, and newly added diode stress/current/energy still must be measured. `passive_fault` was running next. Continue by inspecting its result, then test candidate combined startup/min-trip/temp/reversal, input diode dissipation, source and UV margins, and fine transient convergence. The diode likely dissipates~1–1.5W at2.5A; layout/thermal plan required. Do not apply candidate blindly because one test converged.

Rejected/unfinished alternative: `H/test_ideal_input.py` / `S/pdb/pdb_ideal.lib` added LTC4359 upstream with60V Q3,1k VSS return,1.5µF OUT-to-VSS and SMAJ24CA IN-to-VSS following ADI example. Timed out180s at third inductance. No CAD change. If revisiting, use an adequately rated MOSFET and all pin-stress checks. Avoid dumping encrypted model binary into logs.

## Finish requirements

1. Resolve candidate protection design, with explicit pass/fail pin and component stress limits. Add new monitoring requirements to default active suite. Current `S/active_decks.json` still points at old final models including failing transient test.
2. Apply only validated engineering changes to main schematic; maintain readable horizontal text and grid alignment. Export netlist and verify exact pin connectivity vs SPICE. Update `H/check_eco.py` (currently expects47symbols and only five gate-network pin changes) for new parts/nets deliberately.
3. Reconcile both BOMs using existing `S/audit/reconcile_bom.mjs`; regenerate `S/audit/components.json` from final schematic first. Node `C:/Users/jared/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe`; audit/node_modules junction exists. This builder was already run after the90pF note change.
4. Rerun ERC, inspect full rendered schematic and crowded regions. Do not equate ERC clean with electrically safe.
5. Write **H/STATUS.md**, currently missing despite a schematic reference. Consolidate active results with hashes and clearly separate model limitations, solved defects, remaining PCB/bench release requirements.
6. Reconcile stale root README, DESIGN-SPEC, `docs/PDB-INTERFACE-PROPOSAL-20260915.md`, S/README, model_manifest and REVIEW. Old reports can be explicitly marked historical/superseded. They currently disagree about values/populations/calibration. Preserve useful evidence.
7. `H/OSIRIS-ECO.md` and `H/Osiris_Power_Input_ECO.kicad_sch` are a rejected earlier alternative adding dVdt caps to Osiris. Mark clearly retired/not required; user confirmed existing Osiris hardware should remain.
8. There is no PDB layout: do not claim DRC, thermal layout, EMI, FET SOA, fuse clearing or hardware qualification complete. Fuse model is a cold resistor; its17A²s number is typical PRE-ARCING, not clearing or a safety acceptance limit. INA digital behavior and eFuse surrogate limitations remain.

## Primary references

- https://www.analog.com/media/en/technical-documentation/data-sheets/ltc4368.pdf — gate topology Fig7, thresholds, pin limits.
- https://www.ti.com/lit/ds/symlink/ina228.pdf — sensor pin limits/filter guidance.
- https://www.ti.com/lit/ds/symlink/lm7310.pdf — actual Osiris eFuse open dVdt behavior; current model is an engineering surrogate.
- https://www.st.com/resource/en/datasheet/stpst10h100sb.pdf — candidate D3/D4. VFmax.605V@5A/.715V@10A25C;210A10ms single surge; thermal and reverse leakage require evaluation.
- https://www.analog.com/media/en/technical-documentation/data-sheets/ltc4359.pdf — alternative ideal diode and reverse transient protection.
- https://www.infineon.com/assets/row/public/documents/24/49/infineon-isc015n06nm5lf2-datasheet-en.pdf — Q1/Q2. Current fitted VDMOS is not suitable for SOA/avalanche/thermal qualification.

The user requested switching to Claude API to conserve Codex usage. Claude Code executable is installed at `C:/Users/jared/.local/bin/claude.exe`, but `claude auth status` reports loggedIn=false and this process has no ANTHROPIC_API_KEY. Authenticate before sending this task; never paste credentials into this file or logs.
