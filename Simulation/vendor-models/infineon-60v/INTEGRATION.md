# Infineon Q1/Q2 model integration

2026-09-18 status: see `../../combined-20260915/MODEL-VERIFICATION-20260918.md`. Ten of eleven independent release decks pass. The original stepped transient run failed initialization in its second case; independent 0.2 µH and 2 µH cases pass, but 20 µH remains unresolved. No tolerance-relaxed result is accepted.

Source: user-supplied infineon-optimos-powermosfet-pspice-60v-n-channel-simulationmodels-en.zip.
Selected library: 03_OptiMOS_OptiMOS5/OptiMOS_OptiMOS5_60V_LTSpice.lib, version 030726.
SHA-256: 6309f9b70959f636ee3cea927251da7f6cc7f5d73b444a1a3c4b2489e470917e.

The release PDB now instantiates ISC015N06NM5LF2_L1 for Q1/Q2 with drain/gate/source order. All original manufacturer model parameters and package parasitics are retained. L1 follows the deck temperature without modeling self-heating. The five-pin electrothermal model is available in the same library; its case-temperature or heatsink boundary must be defined before interpreting thermal results.

The first combined startup run reached an iteration limit in case 5. Raising the transient Newton iteration allowance to 1000 allowed all eight startup corners to complete and pass with unchanged accuracy tolerances and electrical acceptance limits. This numerical setting does not change the physical circuit.

The normal-solver temperature sweep subsequently exceeded 300 seconds and the fault run emitted a tolerance-relaxation warning. These are not accepted as passes. The release model now selects LTspice's alternate solver while retaining the same tolerances; the startup corner deck also passes with that solver. Solver guidance: [Analog Devices LTspice troubleshooting](https://github.com/analogdevicesinc/ltspice-reference/blob/main/ai_ref/TROUBLESHOOTING-GUIDE.md). See audit/verification.json for completed-suite status rather than assuming that a successful startup test closes the remaining tests.

Q3 remains a fitted BSC070N10NS5 model: the separately supplied BSC070N10NS5 archive contains only BSC070N10NS5.SchLib and INF-PG-TDSON-8-1_N.PcbLib. Obtain the Infineon 100 V power MOSFET simulation library containing the exact BSC070N10NS5 subcircuit.

The supplied Taiwan Semiconductor SMAJ24CA model remains a different-manufacturer comparison candidate for the Bourns TVSs. Its original parameter continuation lines start with '+'. Its subcircuit is named SMAJ24A even though the header says SMAJ24CA; two opposing diodes implement bidirectional behavior.
