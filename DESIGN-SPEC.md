# Osiris PDB Rev A — current scope

Current simulation/design audit: [review](Simulation/combined-20260915/REVIEW.md). This supersedes earlier population and simulation claims.

Status: schematic candidate, not fabrication- or flight-qualified.

**September 15 update: A-P2-DRAFT, 48 components.** U3 is LT3010 with the
R11/R12/C10 feedback network. See the current
[electrical review](docs/PDB-ELECTRICAL-REVIEW-20260915.md) and
[interface proposal](docs/PDB-INTERFACE-PROPOSAL-20260915.md).
The proposed 25 W AND 2.5 A load limits, 220 uF startup capacitance budget and
mechanical envelope await selection of the actual loads/airframe. They are not
measured ratings. F1 remains provisional and the INA228 negative-input protection
and fault-survival validation remain open.

This board provides one fused, protected raw-4S avionics feed to Osiris and INA228
I2C telemetry. It does not distribute ESC/motor power and has no high-current
propulsion-bus rating. The old four-ESC/80 A specification is retired and preserved
in the external workspace archive.

Power: J1 → provisional 5 A F1 → LTC4368-1 / back-to-back MOSFETs → 5 mΩ shunt
→ J3 → Osiris raw-battery input (new Rev B connector to be defined; old reference J16).
U3 runs from protected PDB_VOUT.
Gate-feedback UV thresholds require corner validation; nominal OV is about 18.7 V. Nominal electronic breaker: 6.25 A.
These thresholds do not establish a continuous current rating or battery cell protection.

Data: J2 4-way GH, 1 NC / 2 SCL / 3 SDA / 4 GND. Old Osiris reference: J28;
the new Rev B connector and bus mapping remain to be defined.
U2 INA228 address: 0x40. Verify Osiris pull-up rail and bus timing before integration.
The 2.22 A planning case is an assumption-derived scenario, not a measured maximum.
Mechanical dimensions, copper stackup and layout must be established for this design;
there is no current PDB PCB file.

See [Rev A readiness and completion plan](docs/REV-A-READINESS.md) for the power/data
explanation, review findings, evidence, limitations and ordered acceptance gates.
