# PDB manufacturing review — 28 September 2026

**Status: CAD checks pass; assembled-board release remains on hold.** The active
project is `Osiris_PDB_RevA.kicad_pro`, revision `A-P4-DRAFT`. The temporary
Gerbers are a review export, not an order package.

## Current CAD result

| Check | Result |
| --- | --- |
| KiCad 10.0.5 schematic ERC | 0 violations; footprint-filter checking enabled |
| PCB DRC after zone refill | 0 violations |
| PCB connectivity | 0 unconnected items |
| Schematic-to-PCB parity | 0 issues |
| Board | 2 copper layers, 1.6 mm nominal, 35 µm nominal copper per layer; 64 footprints |
| Assembly inventory | 51 placed parts, 7 bare test pads, 4 mounting holes, 2 DNP resistors; the 4 A blade fuse is an additional inserted part |
| Drill test | Separate PTH and NPTH files export; 223 plated and 4 non-plated holes, including six 0.6 mm plated slots |

Reports, a fresh BOM, and **draft** JLCPCB-format BOM and placement CSVs are in
`review/2026-09-28/`. The JLCPCB part-number column is blank because exact stock
parts have not been matched. Do not upload the draft BOM as a complete assembly
order: JLCPCB says only matched parts are populated.

KiCad ERC still ignores three project categories: single-use global labels,
four-way junctions, and SPICE model issues. PCB DRC ignores only tuning-profile
geometry. The board-wide minimum clearance is **0.20 mm**, so any order using
more than **1 oz copper** needs a fresh rules and DRC review.

## Fixes completed in this pass

- Moved H3 from `(90.5, 58.75)` to `(90.5, 59.5)` mm after the hole pattern was
  confirmed movable. The H3/J4 courtyard overlap is gone. Verify the new hole
  against the actual frame and screw head.
- Replaced Q1/Q2's altered three-pad board footprints with the project-local
  eight-pad Infineon footprint, restored the full solder-paste pattern, assigned
  pins 1–3 to source and 5–8 to drain, and used direct zone connections on the
  power pads. Corrected an extraneous line in the library courtyard.
- Gave Q3's existing copper pad three additional numbered, copper-only pad
  regions for pins 6–8. These lie inside its already connected drain pad, so
  copper, mask, and paste shapes are unchanged. Saved it as a project footprint
  and linked the schematic to it. The ordered part is the Infineon
  `BSC070N10NS5ATMA1` SuperSO8.
- Matched the selected footprints to project-local symbol filters for D3, J2,
  U1, and U4. Corrected the stale F1 schematic description from 5 A to 4 A.

The [Infineon Q1/Q2 datasheet](https://www.infineon.com/assets/row/public/documents/24/49/infineon-isc015n06nm5lf2-datasheet-en.pdf)
identifies pins 1–3 as source, 4 as gate, and 5–8 as drain. Its package drawing
and the [Infineon Q3 datasheet](https://www.infineon.com/dgdl/Infineon-BSC070N10NS5-DataSheet-v02_02-EN.pdf?fileId=5546d4624a0bf290014a0fc62d9d6b3c)
are the package references for the PCB assembly review. KiCad's clean DRC does
not certify stencil volume or first-article solder joints.

## Open release gates

1. **Load path and fuse rating.** This layout was designed as a 4S **avionics**
   branch for up to 25 W and 2.5 A simultaneously. Its 4 A MINI fuse and power
   copper are not a qualified four-motor ESC feed. The intended use is now
   confirmed as **J3 to Osiris and J4 to the ESC**; this is a release blocker
   until the motor path is separated or completely redesigned. J3 and J4 are
   parallel connections to the **same**
   `PDB_VOUT` and GND nets; the two load currents add through the common fuse,
   MOSFETs, and shunt. D3 is a ground-to-output clamp and does not isolate the
   connectors. See the [output topology note](docs/OUTPUTS-AND-DIODE-20260928.md).
   The user requires the ESC to remain on J4, so redesign the PCB with a
   **separate motor-current branch** and a battery input, J4, protection,
   copper, and return path rated for that branch plus the avionics load.
   The reported ESC is an AERO SELFIE 45 A four-in-one; the manufacturer's
   [45 A stack listing](https://aeroselfie.myshopify.com/products/aero-selfie-h743-flight-controller-stack-30-x-30-stack-with-45a)
   calls the 45 A rating **per channel**. The actual four-motor battery-input
   maximum still requires motor/propeller data or measurement; motor averages
   are insufficient. The called-out XT60PW connectors also need requalification:
   AMASS lists the [M30](https://www.china-amass.net/xt60pw-m-product/) and
   [F30](https://www.china-amass.net/xt60pw-f-product/) variants at 35 A with
   up to 85 K rise; J1 would carry both motor and avionics current. With
   separate ESC and Osiris branches, the [Osiris Rev B power review](https://github.com/modifly-technologies/Hardware/blob/codex/osiris-revb-power-route/OSIRIS_RevB/REV_B_POWER_REVIEW.md)
   now uses 25 W as the module design case within the requested 15–25 W
   operating range. A 25 W Jetson mode alone exceeds this branch's 25 W
   input budget after conversion loss. The installed module, every concurrent
   avionics load, and the ESC's continuous/peak input requirements remain to
   be confirmed before resizing F1 or releasing the board. For layout work,
   the user asked for a conservative normal-use estimate; the provisional
   design targets are **60 A continuous and 100 A for 30 seconds at J4**,
   with the current outline retained. The
   [motor-branch design basis](docs/MOTOR-BRANCH-DESIGN-BASIS-20260928.md)
   records why the present XT60s and 1 oz layout cannot implement it directly.
2. **Electrical fault behavior.** Demonstrate that the INA228 IN+, IN−, and
   VBUS pins remain within their −0.3 V minimum during reverse input, output
   collapse, and harness transients. Qualify TVS clamp energy and peak voltage,
   LTC4368/Q1/Q2 fault/retry stress, the 4 A fuse's interrupting duty, and
   fuse/holder/copper/cable thermal coordination against the selected 4S pack.
   The [TI INA228 limits](https://www.ti.com/lit/ds/symlink/ina228.pdf) and the
   [earlier electrical review](docs/PDB-ELECTRICAL-REVIEW-20260915.md) explain
   the remaining mechanisms. Older review numbers for F1 and R5 are stale;
   current values are **4 A** and **5 mΩ**.
3. **Actual fit and wiring.** Verify the shifted H3 hole, mounting hardware,
   J1/J3/J4 mating and polarity, cable exit, fuse access, and output polarity
   against the airframe and harness. J1 pin 2 is battery positive; J3/J4 pin 2
   is protected positive; pin 1 on each XT60 is ground.
4. **JLCPCB sourcing and assembly.** Match every fitted BOM MPN to an available
   JLCPCB/LCSC part or approved global-sourcing item. The F1 footprint is the
   **Keystone 3568 holder**; it also needs a separate **Littelfuse
   0297004.WXNV 4 A MINI fuse** inserted after soldering. Confirm JLCPCB will
   supply and install both, plus XT60 and other through-hole parts. Verify the
   placement preview, rotations, first-article soldering, and the six plated
   slots. [JLCPCB assembly FAQ](https://jlcpcb.com/help/article/pcb-assembly-faqs)
   says only matched parts are populated and through-hole assembly is available.
5. **First-article test.** Current, temperature, startup, hot-plug, reverse
   polarity, short, and telemetry behavior need hardware measurements before
   the board is called electrically qualified. A CAD-clean prototype can be
   fabricated before those tests only as an engineering build with these
   risks recorded.

## Fabrication-file state

The latest **temporary** export contains front/back copper, mask, paste,
silkscreen, board outline, and separate plated/non-plated drill files. It is at
`%LOCALAPPDATA%/Temp/pdb-release-review-20260928/cad-clean-gerbers`; it has not
been designated as a release ZIP or uploaded to JLCPCB. The draft assembly CSVs
are for reconciliation and must be checked in JLCPCB's placement and parts
matching preview before any order.

Assumed board order: 2-layer FR-4, 1.6 mm, **1 oz outer copper**, solder mask,
and a finish appropriate for the selected assembly process. JLCPCB lists 0.10 mm
minimum trace/space for its 2-layer 1 oz process and 0.5 mm minimum plated-slot
width; the actual design rules are more conservative at 0.20 mm copper clearance.
See [JLCPCB capabilities](https://jlcpcb.com/capabilities/Capab) and its
[copper-weight guide](https://jlcpcb.com/help/article/jlcpcb-copper-weight).
