# Osiris PDB Rev A — current CAD scope and requested change

The active schematic is `A-P5-DRAFT` in `Osiris_PDB_RevA.kicad_pro`. It is a
two-layer, 1.6 mm, nominal 1 oz copper avionics power-protection board with
INA228 I²C telemetry. The schematic now includes a **provisional, separately
fused J3 four-motor ESC branch**. The PCB placement and routing still represent
the older parallel-output layout and **do not implement the new branch**.

The intended avionics operating envelope is **25 W and 2.5 A simultaneously**
from a 4S battery, with the Jetson in its requested 15 W mode. These are design
targets, not measured ratings. The avionics path is J1 battery input → F1 4 A
MINI fuse → Q3 ideal-diode stage → U1 LTC4368-1 and back-to-back Q1/Q2 MOSFETs
→ R5 5 mΩ Kelvin shunt → J4 protected raw-battery output to Osiris. U3 LT3010
derives the local 3.3 V
telemetry supply from the protected output. D3 is a power Schottky clamp from
ground to the avionics output. J2 carries the Osiris I²C interface with pin 1
unconnected, pin 2 SCL, pin 3 SDA, and pin 4 ground.

The provisional motor path is `VBAT_RAW` → F2 100 A candidate fuse →
`ESC_VBAT` → J3. D5 is a bidirectional 24 V TVS candidate and C17–C19 provide
470 µF / 35 V bulk, 1 µF / 50 V, and 100 nF / 50 V local bypass. J1 and J3
are shown as 125 A terminal candidates. These selections establish schematic
intent only; time-current behavior, breaking capacity, transient energy,
capacitance/ripple, connector fit, wiring, and temperature rise remain open.

The board layout and current BOM supersede the September 15 planning numbers
in older review files. The schematic export has 65 BOM entries, including
seven test pads; the PCB has 64 footprints, including four mounting holes.
The H3 courtyard conflict and MOSFET pin-count discrepancies have been corrected
in CAD. J3/J4 cable polarity and mating, actual mounting fit, protection
transients, fuse/trace coordination, assembly sourcing, and first-article
verification still need closure before release.

For the requested redesign, use the [provisional motor-branch design basis](docs/MOTOR-BRANCH-DESIGN-BASIS-20260928.md):
60 A continuous and 100 A for 30 seconds at J3 until motor/propeller data
supersede these assumptions. Keep the existing board outline. The motor
branch must bypass the avionics 4 A fuse and protection path, with both
positive and return routes sized for motor current. The present XT60
connectors and 1 oz avionics copper do not meet this provisional target.

See [the current manufacturing review](MANUFACTURING_REVIEW_2026-09-28.md) for
the measured CAD checks, remaining blockers, and manufacturing status. The
[output topology note](docs/OUTPUTS-AND-DIODE-20260928.md) documents the
superseded A-P4 parallel-output schematic and the reason for the split. The
[September 15 electrical review](docs/PDB-ELECTRICAL-REVIEW-20260915.md) and
[simulation review](Simulation/combined-20260915/REVIEW.md) remain historical
engineering inputs; their population and board-status statements are stale.
