# Osiris PDB Rev A — current CAD scope and requested change

The active design is `A-P4-DRAFT` in `Osiris_PDB_RevA.kicad_pro`. It is a
two-layer, 1.6 mm, nominal 1 oz copper avionics power-protection board with
INA228 I²C telemetry. The user now requires J4 to power the four-motor ESC
from this PDB. The active CAD **does not yet implement that requirement**.

The intended operating envelope is **25 W and 2.5 A simultaneously** from a
4S battery. These are design targets, not measured ratings. The active power
path is J1 battery input → F1 4 A MINI fuse → Q3 ideal-diode stage → U1
LTC4368-1 and back-to-back Q1/Q2 MOSFETs → R5 5 mΩ Kelvin shunt → J3/J4
protected raw-battery outputs. U3 LT3010 derives the local 3.3 V telemetry
supply from the protected output. D3 is a power Schottky clamp from ground to
the output. J3 and J4 are parallel contacts on the same `PDB_VOUT` bus, with
no protection between them; D3 does not isolate the outputs. J2 carries I²C
with pin 1 unconnected, pin 2 SCL, pin 3 SDA, and pin 4 ground.

The board layout and current BOM supersede the September 15 planning numbers
in older review files. The schematic export has 60 BOM entries, including
seven test pads; the PCB has 64 footprints, including four mounting holes.
The H3 courtyard conflict and MOSFET pin-count discrepancies have been corrected
in CAD. J3/J4 cable polarity and mating, actual mounting fit, protection
transients, fuse/trace coordination, assembly sourcing, and first-article
verification still need closure before release.

For the requested redesign, use the [provisional motor-branch design basis](docs/MOTOR-BRANCH-DESIGN-BASIS-20260928.md):
60 A continuous and 100 A for 30 seconds at J4 until motor/propeller data
supersede these assumptions. Keep the existing board outline. The motor
branch must bypass the avionics 4 A fuse and protection path, with both
positive and return routes sized for motor current. The present XT60
connectors and 1 oz avionics copper do not meet this provisional target.

See [the current manufacturing review](MANUFACTURING_REVIEW_2026-09-28.md) for
the measured CAD checks, remaining blockers, and manufacturing status. The
[output topology note](docs/OUTPUTS-AND-DIODE-20260928.md) explains J3/J4 and
D3. The [September 15 electrical review](docs/PDB-ELECTRICAL-REVIEW-20260915.md) and
[simulation review](Simulation/combined-20260915/REVIEW.md) remain historical
engineering inputs; their population and board-status statements are stale.
