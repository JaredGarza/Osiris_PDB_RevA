# BSC070N10NS5 Q3

The user-supplied 100 V archive contains the exact device, including an LTspice-specific library at `OptiMOS5/OptiMOS5_100V_LTSpice.lib` (version 240725). Original archive files are retained unchanged.

The release circuit uses `BSC070N10NS5_L1`, drain/gate/source, with original package parasitics and typical parameter settings. The L1 model follows simulator temperature; it does not establish self-heating, SOA or avalanche survival. The five-pin electrothermal version was not substituted without a justified thermal boundary.

See `../../combined-20260915/Q3-MODEL-VERIFICATION.md` for measured standalone results and the unresolved combined-circuit initialization test. Prior fitted-Q3 results are not current evidence.
