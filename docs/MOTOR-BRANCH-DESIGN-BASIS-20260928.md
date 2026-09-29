# PDB motor branch: provisional design basis — 28 September 2026

**Historical basis.** The user later identified the AERO SELFIE
`4IN1-ESC-LDO`; its confirmed per-channel ratings and a representative 4S
input-current scenario are in the
[29 September estimate](AERO_SELFIE_ESC_INPUT_ESTIMATE_2026-09-29.md).
The older board-state and connector selections below are superseded by the
[compact layout review](../COMPACT_XT60_ROUTE_REVIEW_2026-09-29.md).

## Load assumption for layout work

The user requires this PDB to power a 4S, four-motor ESC at J3 and asked for
a conservative normal-use estimate until motor and propeller data are
available. Use **15 A per motor simultaneously (60 A continuous at J3)** and
**25 A per motor simultaneously (100 A for a 30-second burst at J3)** as
provisional *design targets*. Reserve at least **5 A additional avionics
input current for J4** when rating any common battery entry; this is a
preliminary allowance pending the Osiris load and fuse review. These are engineering
assumptions, not motor measurements or confirmed operating limits.

The reported AERO SELFIE 45 A four-in-one ESC is described as 45 A *per
channel* in its [stack listing](https://aeroselfie.myshopify.com/products/aero-selfie-h743-flight-controller-stack-30-x-30-stack-with-45a).
Its [standalone listing](https://aeroselfie.myshopify.com/products/45a-4-in-1-esc-brushless-motor-speed-controller)
uses ambiguous “across 4 channels” wording. If the installed motors can use
all four channels at that rating simultaneously, the battery branch might
have to support substantially more than this 60/100 A assumption. Do not
release a board on this assumption without confirming the installed ESC,
motor/propeller current, and battery capability.

## Required electrical split

```text
4S battery, common input rated for both loads
  ├─ ESC branch: separately rated fault protection → heavy positive and return paths → J3
  └─ avionics branch: F1 → Q3/U5 → Q1/Q2/U1 → R5 → J4 → Osiris power input
```

J3 must leave `/PDB_VOUT`; the motor branch must not cross F1, Q3, Q1/Q2,
or R5. Maintain separate copper nets for raw battery, protected avionics,
and motor output. Ground is electrically common, but the ESC's return current
needs its own low-impedance route to the battery entry rather than sharing
the INA228 sense or avionics return bottlenecks. Select motor protection to
coordinate with the wire gauge, connector, PCB copper, and battery's available
short-circuit current. The existing 4 A F1 remains an avionics-only part and
must be requalified for the Jetson's 25 W case and other Osiris loads.

## A-P5 schematic candidates

| Reference | Provisional choice | Purpose / remaining qualification |
| --- | --- | --- |
| J1, J3 | Phoenix Contact 1932588 / MKDSP 25/2-15,00, 125 A nominal with specified conductor | Battery input and ESC output candidates; footprint, cable access, torque, assembly method, polarity and temperature rise remain open |
| F2 | SCHURTER UHS 100 A, 3-140-177 | Dedicated ESC branch fuse candidate; verify 60 A continuous heating, 100 A for 30 s, time-current curve, pack fault current and breaking capacity |
| D5 | SMBJ24CA | Bidirectional 24 V local connector TVS candidate; validate actual harness ringing, pulse energy and clamp voltage |
| C17 | 470 µF / 35 V low-ESR | Provisional local ESC bulk capacitance; coordinate ESR, ripple current, inrush and minimum ESC-vendor capacitance |
| C18, C19 | 1 µF / 50 V X7R and 100 nF / 50 V X7R | Local high-frequency bypass at J3 |

These are schematic design-basis parts, not a released order BOM. The current
PCB has not been updated with their footprints or high-current copper.

## Existing-board feasibility check

- Current outline: approximately **94.55 × 51.8 mm**. The user wants to keep
  this size. The lower edge has the J3/J4 outputs, J2, test pads, and two mounting holes;
  the central area carries the avionics protection and telemetry components.
- Current stack: **two layers, nominal 1 oz copper**. The existing `/PDB_VOUT`
  traces include **0.3–3.0 mm** widths and were designed for avionics, not
  the motor target.
- The A-P4 J1/J3/J4 footprints are XT60PW-M/F. AMASS lists the
  [M30](https://www.china-amass.net/xt60pw-m-product/) and
  [F30](https://www.china-amass.net/xt60pw-f-product/) variants at **35 A
  with up to 85 K rise**. They cannot be treated as 60 A continuous or
  100 A burst connectors without a separate qualification. Simply swapping
  to an XT90PW is insufficient: AMASS lists the
  [XT90PW-M30](https://www.china-amass.net/xt90pw-m-product/) at **45 A
  with up to 85 K rise**.
- As a preliminary *single external conductor* check using the IPC-2221
  empirical formula with 20 °C allowed rise, 60 A needs approximately
  **56 mm of 1 oz copper**, **22.4 mm of 2.5 oz copper**, or
  **12.5 mm of 4.5 oz copper** for each polarity on a single outer layer.
  Parallel top/bottom pours could share current only after connection and
  current division are checked. The calculation
  excludes connector pads, neckdowns, vias, solder joints, airflow,
  enclosure temperature, and the matching return conductor, so it is a
  feasibility screen rather than a qualified trace width. Both polarities
  need comparable capacity. JLCPCB lists [4.5 oz on two-layer FR4](https://jlcpcb.com/help/article/jlcpcb-copper-weight)
  with **0.30 mm minimum trace/space**, requiring a fresh whole-board
  fabrication-rule check and substantial placement/routing changes. A
  temporary copy of the current PCB checked with 0.30 mm minimum clearance
  and track width produced **235 clearance and 29 track-width violations**
  (plus seven missing local-footprint references caused by copying it outside
  the project). The active CAD was not changed for this check.
  JLCPCB's 2.5 oz option keeps the published 0.20 mm minimum trace/space,
  matching the current project minimum, but needs much wider positive and
  return pours and substantial rearrangement of the existing components.

**Conclusion:** the 60/100 A provisional branch is a board redesign within
the existing outline. The active 1 oz PCB is not a usable starting motor
route. Choose a battery-entry/J3 connection method rated for at least the
provisional currents and compatible with JLCPCB assembly, then draw the
separate branch in the schematic and route both polarities with thermal,
voltage-drop, fault, and DRC review. The present release status remains hold.

One connector candidate for a footprint/fit study is the
[Phoenix Contact MKDSP 25/2-15,00, order code 1932588](https://www.phoenixcontact.com/en-de/products/pcb-terminal-block-mkdsp-25-2-1500-1932588):
two poles, 125 A nominal with the specified conductor, 30 mm wide, and
wave-soldered. Two would replace the battery and ESC XT60s; J4 would remain
an avionics connector. This is **not a selected BOM part**: the terminal's
large body and cable access must fit the fixed board outline, the chosen
battery/ESC wires must meet the intended currents, and JLCPCB must confirm
it can source and assemble the exact part. A compact motor-fuse candidate
for a later thermal/fault study is the [SCHURTER UHS 100 A SMT,
order code 3-140-177](https://www.schurter.com/en/datasheet/UHS). Its
published breaking-capacity tests use a **22 mm, 210 µm copper** test-board
conductor, which is substantially heavier than the active board's 1 oz
copper. Confirm its time-current behavior, 4S pack fault current, board
thermal path, JLCPCB stock, and first-article heating before selecting it.
These two component examples are footprint-study candidates, not an order BOM.
