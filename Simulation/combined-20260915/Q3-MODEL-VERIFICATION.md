# Exact Q3 model integration

Source: user-supplied `infineon-optimos-power-mosfet-spice-100-v-n-channel-simulationmodels-en.zip`.

Selected library: `../vendor-models/infineon-100v/OptiMOS5/OptiMOS5_100V_LTSpice.lib`, version 240725. SHA-256: `775c1b18bdbf61ae6f1662fa42aaaa86eb34b4977896d3c979abadf3edfb91b3`.

Q3 now uses the exact `BSC070N10NS5_L1` three-pin drain/gate/source subcircuit. Manufacturer parameters and package inductances are unchanged. This is a fixed-temperature electrical model, not a self-heating or SOA qualification. The library also contains an electrothermal version, but it requires a justified thermal boundary.

The live schematic connectivity check passes, including Q3 drain/gate/source mapping. No schematic electrical changes were made. Earlier passing simulations used a different Q3 model and are historical; their consolidated report is preserved in `audit/verification-before-q3.json` and their PDB model in `audit/pdb_release-before-q3.txt`.

## Results

- Standalone Q3 test (`infineon_q3_device_check.cir`): completed without tolerance-relaxation warnings. At 25 °C, 10 V gate drive and 40 A, typical on-resistance is 6.0861 mΩ; dRdson=1 gives 7.0080 mΩ. This is a model spot check, not full datasheet qualification.
- Live connectivity and all nine runner self-tests pass.
- Combined 20 µH transient test: did not complete within 240 seconds. DC initialization exhausted direct Newton, Gmin and source-stepping attempts; no valid final measurements were produced. Evidence: `audit/verification-q3-first-transient.json`. This is a numerical failure, not a demonstrated hardware limit violation.
- Other combined-board regression tests have not yet been rerun with the new Q3. The previous 10/11 count does not apply to this model revision.

Next: diagnose combined-circuit initialization with the three vendor MOSFET models, then rerun the full release suite. Keep electrical tolerances and acceptance limits intact; do not accept an incomplete or tolerance-relaxed run. No physical component change is justified by this timeout alone.

Remaining fidelity gaps include the Bourns TVS approximation, Osiris behavioral surrogate, thermal/SOA and fuse-clearing behavior. Simulation success would support prototype preparation, not guarantee that both physical boards will work.
