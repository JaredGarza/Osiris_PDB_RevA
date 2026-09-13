# Osiris PDB Rev A — current scope

Status: schematic candidate, not fabrication- or flight-qualified.

This board provides one fused, protected raw-4S avionics feed to Osiris and INA228
I2C telemetry. It does not distribute ESC/motor power and has no high-current
propulsion-bus rating. The old four-ESC/80 A specification is retired and preserved
in the external workspace archive.

Power: J1 → provisional 4 A F1 → LTC4368-1 / back-to-back MOSFETs → 5 mΩ shunt
→ J3 → Osiris raw-battery input (new Rev B connector to be defined; old reference J16).
U3 runs from protected PDB_VOUT.
Nominal UV/OV thresholds: 10.56/18.68 V. Nominal electronic breaker: 10 A.
These thresholds do not establish a continuous current rating or battery cell protection.

Data: J2 4-way GH, 1 NC / 2 SCL / 3 SDA / 4 GND. Old Osiris reference: J28;
the new Rev B connector and bus mapping remain to be defined.
U2 INA228 address: 0x40. Verify Osiris pull-up rail and bus timing before integration.
The 2.22 A planning case is an assumption-derived scenario, not a measured maximum.
Mechanical dimensions, copper stackup and layout must be established for this design;
there is no current PDB PCB file.

See [Rev A readiness and completion plan](docs/REV-A-READINESS.md) for the power/data
explanation, review findings, evidence, limitations and ordered acceptance gates.
