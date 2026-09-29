# Single-battery power-path foundation — 29 September 2026

**Design study; no fabrication or flight release.** This note replaces the
assumption that a green terminal alone qualifies the motor power path. The
active KiCad schematic and routed PCB still represent the three-XT60
candidate described in `COMPACT_XT60_ROUTE_REVIEW_2026-09-29.md`. A separate
[green-terminal placement board](../design-studies/phoenix-through-pdb/Osiris_PDB_RevA.kicad_pcb)
implements the requested through-PDB power path as an unrouted study.

## Loads and electrical boundary

One 4S battery supplies the AERO SELFIE 45 A four-in-one ESC and the Osiris
avionics. The ESC's 45 A continuous rating is **per motor channel**; it is not
a measured common battery current. The provisional design target remains
60 A continuous / 100 A for 30 s for propulsion until the actual motors,
propellers, and battery-current measurements establish another requirement.
The avionics design target is 25 W and 2.5 A from the 4S input, protected by
the existing 4 A F1 branch fuse.

## Selected layout foundation: ESC power through the PDB

```text
one 4S pack XT60
        │ full propulsion current; exact pack plug rating unknown
        ▼
short XT60-to-wire adapter
        ▼
J1 green input ──► raw-battery split ──► F2 ──► J3 green output ──► ESC
                            │                  │                   └─► motors
                            │                  └─► transient/bypass parts
                            └─► F1 ──► avionics protection ──► J4 Osiris
                                                            └─► J2 I²C
```

Both green blocks are Phoenix Contact MKDSP 25/2-15.00 / 1932588 candidates.
The battery's XT60 stays on the pack and mates to the adapter. The ESC input
wires terminate at J3; its stock XT60 pigtail cannot remain in this path if
the intent is to remove the second XT60 bottleneck. The exact battery
connector is still a separate constraint. The placement study puts J1 and
J3 on one upper cable edge with their positive pad groups facing F2 in the
middle. The front positive corridor can run directly across the gap. The
ground return needs a broad, uninterrupted path, not a handful of vias.
The ESC bypass parts occupy the row above J3. Avionics remain in the lower
region with J4/J2 at the Osiris cable exit.

The study has a 94.55 × 98.55 mm bounding box, with the four existing
mounting holes preserved. It is narrower than the historical 126.05 ×
83.30 mm Phoenix placement, but taller and larger than the current routed
three-XT60 PCB. Its Phoenix land pattern and F2 pattern are provisional.
KiCad reports zero physical-rule violations and 25 expected unconnected
items. There is no high-current copper route or current-capacity claim.

## Alternative: one short main feed, one fused avionics tap

```text
4S pack with XT60
        │  full propulsion current; connector qualification pending
        ▼
short, restrained battery/ESC cable ───────────► ESC BAT+ / BAT− ─► motors
        │                                         local ESC bulk capacitor
        └─► branch fuse near the tap ─► PDB J1 ─► existing avionics
                                                  protection + telemetry
                                             └─► J4 Osiris power, J2 I²C
```

The tap takes raw battery **positive and return** ahead of the ESC's
switching circuitry. The branch fuse protects the small tap wire as close to
the split as practical; F1 and its coordination with that fuse remain to be
reviewed. The ESC keeps its manufacturer's required local input capacitor.
The PDB carries avionics current, not the four-motor current. Its INA228/R5
then continues to measure the protected avionics branch, **not** total
battery or motor current.

The compact PDB layout can start with J1 near F1, then Q3, U1/Q1/Q2 and R5
in power-flow order, and J4/J2 together at the Osiris harness edge. Remove
the ESC-only J3/F2/D5/C17–C19 shelf from that board variant only after the
ESC capacitor and any required motor-branch protection are specified in the
external harness. Keep the four mounting holes or revise their positions
against the actual frame; no smaller outline dimension is asserted yet.

This remains the lighter, smaller alternative if ESC power is later allowed
to bypass the PDB. The [Phoenix Contact 1932588](https://www.phoenixcontact.com/en-ca/products/printed-circuit-board-terminal-mkdsp-25-2-1500-1932588)
green terminal is 30 × 31 mm on the PCB and approximately 43.56 g per part.
It is not needed to carry a roughly 2.5 A avionics branch. Its 125 A nominal
rating is tied to specified conductors and mounting; two such terminals
would add roughly 87 g without increasing the battery XT60's rating.

For the selected through-PDB layout, the present 1 oz two-layer copper,
provisional F2 footprint and solder joints have not been shown to carry
60/100 A. Connector, wire, fuse, copper, assembly, temperature rise and
mechanical retention all require validation.

## Unresolved battery XT60 limit

The [AMASS XT60PW-M](https://www.china-amass.net/xt60pw-m-product/) used on
the current PCB and the manufacturer's
[XT60H-F](https://www.china-amass.net/xt60h-f-product/) cable connector are
published at 35 A under a temperature-rise condition of up to 85 K. The
exact plug on the battery is unknown. Neither direct ESC feed nor a green
terminal raises the rating of a connector retained at the battery. The
previous 4S flight proves that the combination operated on that mission;
it does not establish 60 A continuous / 100 A for 30 s margin. Confirm the
pack connector and cable, log actual battery current over the intended
flight profile, and inspect temperature rise before setting a flight limit.
If 60/100 A is truly required, select a battery interface and entire path
qualified for that duty.

## Implementation gate

Confirm the exact battery connector and cable, the battery current under the
actual motors and propellers, and whether the pack connector can be upgraded
if 60/100 A is required. Verify the Phoenix footprint against its controlled
drawing and select a high-current PCB stackup and fabrication process. Then
update the active schematic and board together, route both high-current
conductors, refit the outline and harness exits, rerun ERC and DRC, and
keep the revision marked unqualified until temperature and fault testing
are complete.
