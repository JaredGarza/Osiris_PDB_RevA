# PDB Rev A and Osiris Rev B completion plan

> September 15 update: A-P2-DRAFT implements the U3 regulator correction and has
> 42 components. M1 is proposed; M2 remains open. Current details are in the
> [electrical review](PDB-ELECTRICAL-REVIEW-20260915.md) and
> [interface proposal](PDB-INTERFACE-PROPOSAL-20260915.md). Dates and counts below
> describe the September 13 plan, not current completion commitments.

Planning date: 13 September 2026. Targets below are proposed working dates, not
verified delivery commitments. Current procurement baseline: A-P1, Git tag
`pdb-procurement-2026-09-13`, commit `e780c08`.

## Where we are now

The PDB is at the end of its initial schematic/parts-planning phase and before PCB
implementation. Its current topology is one protected, monitored, unregulated 4S
avionics supply. It does not distribute motor current. The schematic has 39 components,
including seven bare test pads; purchasing requires 33 physical items including the
separate fuse holder. There are 27 order codes, 23 of them SMT, for 29 SMT placements.

The current PDB passes ERC under the existing project rules and the targeted
connectivity/BOM checks. Eight screening simulation cases completed. Neither of
these establishes fault survival, power cleanliness, hardware reliability or flight
readiness. There is no current PDB layout, completed first article or measured test
record available in this workspace.

Osiris Rev B's replacement power section is planned, not saved or designed yet.
Treat that subsystem as a new design. The older Osiris files remain references for
loads, pin requirements and retained circuitry; their regulators, input switch and
connector designators are not automatically the new Rev B solution. Retained
FMU/Jetson/peripheral circuits still need conversion and integration review.

**A-P1 is a procurement baseline, not unconditional functional schematic approval.**
The final PDB load envelope, fuse rating and new Rev B interface remain open. Any
resulting change gets a new revision; the existing tag stays unchanged.

## Milestones achieved

| When | Achievement | Evidence and limits |
|---|---|---|
| Before September 12 | Protected avionics-feed architecture implemented | LTC4368-1, back-to-back MOSFETs, four-terminal shunt and INA228 in the saved schematic; old 80 A motor-distribution specification retired |
| September 9–10 saved revisions | Protection and interface changes implemented | Gate resistor/diode network, input TVS, negative-output clamp, output capacitance, four-pin I2C and status test points; subsequent audit confirmed connectivity |
| September 12 audit | Latest versions compared; current project identified | Current 39-part schematic compared with 33-part archive and 22-part older project; uncommitted edits cannot reliably be assigned to a particular author |
| September 12 audit | U3 supply and critical nets checked | U3 is already on protected PDB_VOUT; gate network and Kelvin taps checked; earlier reverse-input supply mistake is absent in the latest schematic |
| September 12 audit | ERC and screening simulation completed | Zero ERC violations under configured rules; eight simulation cases completed; real device SOA/clamp/fuse behavior still unqualified |
| September 12–13 | Workspace and GitHub consolidated | One active PDB project, separate recoverable archive, private GitHub synchronized; vendor file handling corrected |
| September 13 | A-P1 procurement baseline recorded | Missing resistor order codes completed; full MOSFET and controller reel codes selected; grouped BOM, workbook, schematic PDF and SHA-256 manifest committed and tagged |

The September 13 layout target in the meeting slides has **not** been achieved.
Today's parts baseline is useful progress, but it must not be reported as completed
layout. The slides' later dates remain planning references, not completed milestones.

## Major changes to understand

| Change | Why it matters now |
|---|---|
| Scope changed from the obsolete multi-ESC distributor to an avionics feed | The PDB current budget covers Osiris and its peripherals, not propulsion. The aircraft still needs an appropriate motor power path. |
| U3 runs from protected output | It is no longer directly exposed to reversed battery voltage through its supply branch. The monitor can lose power/reset when the output trips. |
| R4 is in series with the FET gates and D2 bypasses it for discharge | Startup and turn-off depend on this network. Retain the complete network while checking the real FET behavior. |
| D1, D3 and C9 were added in the later schematic | Input surge clamping, negative-output clamping and local bulk are present; their existence does not prove transient margin. |
| J2 changed to four-pin I2C; fault/alert went to TP6/TP7 | Current cable carries SCL, SDA and ground; it does not report a separate fault interrupt to Osiris. |
| F1 is a provisional 4 A MINI fuse | A new Rev B load/startup budget can change this selection. The nominal 10 A electronic threshold is not a continuous-current rating. |
| A-P1 adds resistor MPNs and complete semiconductor order codes | Purchasing can identify parts and supply packaging. The latest freeze did not change electrical values, footprints or connectivity. |
| New Rev B power and top-facing ports are now explicit planned work | Old J16/J28 connections and matching part counts are references only. Shared reels cannot be committed on that basis. |

## The connection between the two boards

Proposed division of work, subject to the interface milestone:

```text
4S battery
  ├── Separate propulsion power path → ESCs/motors
  └── PDB input → fuse → switched protection → current shunt → protected raw 4S
                                                               │
                                                        power harness
                                                               │
                                              new Osiris Rev B power entry
                                                               │
                                      local conversion / isolation / sequencing
                                                               │
                                        FMU, Jetson, USB and peripheral rails

PDB INA228 ⇄ SCL / SDA / common ground ⇄ Osiris FMU I2C controller
```

Keeping local conversion on Osiris preserves the present PDB's basic function. It
also makes Osiris responsible for regulation and rail sequencing close to its loads.
Moving the converters onto the PDB is a different architecture and requires reopening
the PDB schematic and procurement baseline.

Freeze an interface document covering these seven items before treating either
board's connections as final:

| Interface item | Agreement required | Completion evidence |
|---|---|---|
| Power envelope | Battery range, delivered voltage range, continuous/peak current, peak duration, startup capacitance and allowable harness drop | Rail budget and worst-case input-current calculation accepted by both board designers |
| Startup | Regulator enables, Jetson/FMU startup order as required by selected devices, capacitance charging and load ramp | Timing diagram and reviewed startup/inrush calculation; later bench capture |
| Fault behavior | What trips, what stays powered, retry/latch policy and recovery after a brownout | Fault-state table for battery, USB, debug and peripheral faults |
| Power harness | Positive/ground contacts, wire size/length, current rating, connector gender/orientation, retention and return path | Contact-level drawing and mechanical fit check; later continuity test |
| Data harness | Pin mapping, common ground, I2C master/bus, logic voltage, pull-up ownership and cable length | Two-ended pin table; timing calculation followed by measured rise time |
| Telemetry | INA228 at 0x40, 5 mΩ calibration, sampling, reset/recovery, whether a second Osiris monitor is useful | Firmware interface specification and later calibrated readings |
| Status | Polling only versus physical alert/fault wires | Explicit decision. Current J2 has no alert/fault connection; adding one changes the interface/BOM. |

Current PDB J2 is 1 NC, 2 SCL, 3 SDA, 4 GND. Its NC contact must not be assumed to
provide or accept power. Current PDB J3 is 1 GND, 2 protected output. Those numbers
must be mapped to the actual new Osiris connector contacts, not copied blindly from
the old connector library. Rev B's connector names can change without changing the
electrical agreement, provided the harness drawing remains correct.

The INA228 measures the avionics branch, not total aircraft battery consumption.
It is polled over I2C; it is not an autonomous transmitter. Telemetry and firmware
cannot keep a flight controller operating after its only power supply is disconnected.
Decide whether USB, a peripheral fault or propulsion sag can reset the FMU, and whether
the intended aircraft requires additional isolation or another power source. This is
a system decision to close before approving the protection settings.

## Remaining milestones and proposed schedule

Dates assume prompt team decisions, available CAD source and parallel work by the
PDB and Osiris contributors. The ownership column is a proposed allocation aligned
with the meeting slides; it does not assign work to anyone externally.

| ID / proposed target | Deliverable and proposed owner | Exit criteria | Dependency |
|---|---|---|---|
| M1 — September 14–15 | Joint power/data/mechanical interface; Jared + Ryan | The seven interface items above are recorded; rail loads, Jetson configuration and fault behavior have explicit bounds; no connector or voltage ambiguity | A-P1 and retained Osiris load requirements |
| M2 — September 16–19 | PDB functional schematic release; Jared | Fuse and protection thresholds reviewed against M1; actual FET/diode/shunt/TVS margins checked; exact land patterns checked; critical simulations updated; no unresolved design-stopping issue; ERC and BOM agree | M1 |
| M3 — September 16–19 | New Rev B power schematic; Jared, coordinated with Ryan | Converters and passives selected from real rail requirements; battery/USB/ST-LINK power states, backfeed prevention and sequencing defined; top-facing connectors and I2C mapped; new schematic saved and reviewed | M1 and verified retained load pins |
| M4 — September 19–22 | PDB PCB layout; Jared | Board outline/mounts/height approved; power loops, Kelvin routes and thermal copper implemented; real connector clearances checked; DRC and schematic-to-PCB parity reviewed with no unexplained unconnected nets | M2; preliminary placement may start sooner at rework risk |
| M5 — September 20–24 | Rev B power-section validation and layout integration; Jared + Ryan | Power schematic checks pass; layout follows selected regulator requirements; noise/return paths and USB/ST-LINK integration reviewed; conversion net mismatches and duplicate refs resolved or explicitly justified | M3 and available complete Rev B CAD |
| M6 — September 24 target | PDB fabrication/assembly review package; Jared + lab operator | Controlled BOM, Gerbers/drills, stackup, stencil, positions, assembly drawings, harness drawing and bring-up procedure all match one revision; parts/carriers fit the actual machine | M4, verified parts availability and machine constraints |
| M7 — October 2 target | Complete Rev B manufacturing review; team | Retained circuitry and new power/ports/ST-LINK reviewed together; complete board DRC/net parity, power budget, mechanical fit and assembly package accepted | M5 plus other Rev B workstreams; not achieved by PDB completion alone |
| M8 — After boards and parts arrive | PDB first-article bench acceptance; Jared | Inspect and check shorts first; staged dummy-load tests verify voltage drop, startup, UV/OV, fault response/retry, negative clamp, telemetry and temperature against written limits | M6, assembly and equipment; schedule follows confirmed lead times |
| M9 — After Rev B assembly | Combined PDB + Rev B acceptance; team | Start every required power-source combination; verify rails, USB/debug backfeed behavior, peak loads, telemetry and fault recovery; no unexplained reset or exceeded limit | M7 and M8; may begin earlier with a representative validated load fixture |
| M10 — After combined bench pass | Aircraft ground/flight release; team | Representative propulsion load/EMI, low-battery, harness vibration/retention and controlled ground tests passed; approved flight progression and recorded results | M9 and aircraft integration |

September 24 and October 2 are **review targets**. If M1 slips, M2/M3 and their layouts
slip. Do not make up the lost time by removing electrical review or first-article
testing. Fabrication, shipping, component delivery and a possible respin are outside
these design dates and must be added once quotes are confirmed.

## What can happen in parallel

Once M1 bounds the PDB load and interface, the PDB does not need to wait for every
Rev B trace or connector placement. It can be routed, manufactured and tested with
an electronic load and representative input capacitance while the new Osiris power
section is completed. Passing that test does not replace later testing with the real
regulators, firmware and harness.

While schematic work proceeds, the lab can check inventory against the 27 PDB order
codes, confirm machine/carrier/nozzle requirements, obtain quotes, and arrange bench
equipment. Confirm the two resistor specsheet gaps called out in A-P1. Start modest
prototype procurement of stable selections; keep F1 and fault-sensitive parts visibly
conditional and avoid treating provisional Rev B common counts as demand.

Parts sharing should follow verified MPN, package and specifications. The four
current matches are potential savings only: INA228, four-pin JST-GH and both XT60
genders. The new power topology could eliminate the second INA228; top-facing ports
could replace the horizontal XT60 parts. Do not redesign the PDB passives into 0402
merely to match old Osiris values without a separate rating and assembly review.

## How close are we?

| Finish line | Honest assessment on September 13 |
|---|---|
| Know the PDB's nominal parts | Achieved for the A-P1 procurement baseline; final fuse and interface-dependent changes remain possible |
| Functionally frozen PDB schematic | Close to review, but M1 and M2 are still real engineering work; clean ERC is not the exit criterion by itself |
| Order a PDB PCB | Not yet: layout, mechanical definition and the manufacturing review package are missing |
| Run the pick-and-place machine | Not yet: stock/carrier setup and final PCB position/rotation/stencil data are missing |
| Complete new Rev B power design | At requirements/architecture stage; no saved replacement schematic exists |
| Fly the assembled system | Hardware validation has not started; fabrication, assembly and both levels of test remain |

A single percentage would hide the main risk: the PDB schematic is comparatively
mature, but the combined power system is not. The September 24 PDB manufacturing-review
target is plausible only if the interface closes quickly and the protection review
does not force a redesign. October 2 is an aggressive Rev B manufacturing-review
target with a new power subsystem, not a defensible flight-ready date.

## Immediate next actions

1. Create M1's load/rail table and source-state table: Jetson configuration, FMU,
   USB, ST-LINK and all intended peripherals, including startup and simultaneous loads.
2. Agree that the PDB supplies protected raw 4S and that Rev B makes its local rails,
   or explicitly reopen A-P1 if the team wants a different boundary.
3. Review that load against the 4 A fuse candidate, nominal 10 A breaker and UV
   behavior. Determine acceptable reset/fault behavior before selecting regulators.
4. Select new Rev B power-entry and regulation circuits, document converter/capacitor/
   inductor margins, and save the actual schematic. Keep retained load nets traceable.
5. Close PDB footprint/mechanical checks and start its layout; in parallel complete
   the machine/inventory fields in the existing workbook.

## Status reporting for the next meeting

“PDB A-P1 schematic and procurement baseline are recorded in GitHub. ERC and critical
net/BOM checks pass; eight limited screening simulations completed. The current PDB
layout is not done. Osiris Rev B power replacement and top-facing ports remain planned.
Next gates are the shared power/interface budget, final PDB protection review and the
new Rev B power schematic. September 24/October 2 are proposed review targets, with
fabrication and hardware validation afterward.”

Sources: current project files and A-P1 freeze note; September 12 audit reports;
September 13 user clarification that Rev B power changes are planned, not saved;
USL Meeting 9-9-26 Slides, pages 4 and 6–7, used only for the original milestone dates
and proposed work split. No new bench tests or electrical design changes were made
while preparing this plan.
