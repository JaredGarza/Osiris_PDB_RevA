# Osiris PDB Rev A — current CAD scope

**New layout study:** [single-battery through-PDB power foundation](docs/SINGLE_BATTERY_POWER_PATH_FOUNDATION_2026-09-29.md)
and its [two-Phoenix-terminal placement board](design-studies/phoenix-through-pdb/Osiris_PDB_RevA.kicad_pcb)
show the proposed battery XT60 adapter → PDB → AERO SELFIE ESC path. This
study is not routed or synchronized with the active schematic. The active
root PCB described below remains the three-XT60 candidate. Neither design
is qualified for the provisional 60/100 A propulsion target.

The active schematic is `A-P5-DRAFT` in `Osiris_PDB_RevA.kicad_pro`. It is a
two-layer, 1.6 mm, nominal 1 oz copper avionics power-protection board with
INA228 I²C telemetry. The PCB is now a compact, routed **candidate** for the
separately fused J3 four-motor ESC branch. See the
[29 September layout review](COMPACT_XT60_ROUTE_REVIEW_2026-09-29.md) for its
dimensions, checks, and unresolved current-capacity limits.

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
470 µF / 35 V bulk, 1 µF / 50 V, and 100 nF / 50 V local bypass. J1, J3, and J4
have XT60 board-mount footprints. The earlier two provisional 125 A terminal
footprints were removed. These selections establish layout intent only;
time-current behavior, breaking capacity, transient energy,
capacitance/ripple, connector fit, wiring, and temperature rise remain open.

The board layout supersedes the September 15 planning numbers in older review
files. Earlier BOM and assembly exports must be regenerated for this candidate.
The H3 courtyard conflict and MOSFET pin-count discrepancies have been corrected
in CAD. J3/J4 cable polarity and mating, actual mounting fit, protection
transients, fuse/trace coordination, assembly sourcing, and first-article
verification still need closure before release.

The [provisional motor-branch design basis](docs/MOTOR-BRANCH-DESIGN-BASIS-20260928.md)
sets 60 A continuous and 100 A for 30 seconds at J3 until motor/propeller data
supersede these assumptions. The user's later compact-board request superseded
the earlier instruction to keep the outline. The motor branch bypasses the
avionics 4 A fuse and protection path. Its positive and return copper, the
XT60 connectors, and the provisional fuse land pattern remain unqualified for
this current target.

The reported ESC is the AERO SELFIE `4IN1-ESC-LDO`, rated in its
[manufacturer manual](https://cdn.shopify.com/s/files/1/0728/7321/4171/files/45A_4IN1-ESC_Manual_Book_EN-CN.pdf?v=1745301381)
at **45 A continuous and 55 A peak per motor channel**, four channels total.
These are channel ratings, not a measured common battery-input current. See
the [representative 4S current estimate](docs/AERO_SELFIE_ESC_INPUT_ESTIMATE_2026-09-29.md)
before treating the provisional 60/100 A PDB target as an operating limit.

See [the 29 September layout review](COMPACT_XT60_ROUTE_REVIEW_2026-09-29.md) for
the current CAD checks, remaining blockers, and manufacturing status. The
[28 September manufacturing review](MANUFACTURING_REVIEW_2026-09-28.md) is
historical for this new board. The
[output topology note](docs/OUTPUTS-AND-DIODE-20260928.md) documents the
superseded A-P4 parallel-output schematic and the reason for the split. The
[September 15 electrical review](docs/PDB-ELECTRICAL-REVIEW-20260915.md) and
[simulation review](Simulation/combined-20260915/REVIEW.md) remain historical
engineering inputs; their population and board-status statements are stale.
