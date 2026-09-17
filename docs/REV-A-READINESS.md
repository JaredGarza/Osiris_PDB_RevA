# Osiris PDB Rev A review — 12 September 2026

**Later September 15 update:** the active schematic now has 48 components, F1=5 A and R5=8 mOhm. See [simulation/design review](../Simulation/combined-20260915/REVIEW.md). Earlier numerical population/threshold tables below describe the previous draft.

> Historical audit. The active September 15 A-P2-DRAFT has 42 components and an
> LT3010 local regulator. Use [the current review](PDB-ELECTRICAL-REVIEW-20260915.md)
> and [interface proposal](PDB-INTERFACE-PROPOSAL-20260915.md) for new work.

> September 13 update: the new Osiris Rev B power section and top-facing ports are
> planned and no revised schematic exists yet. The Osiris connections below describe
> the reference implementation, not a verified new Rev B design. See the current
> [parts-planning freeze](../procurement/2026-09-13/FREEZE-NOTE.md).

**Status: schematic candidate; not ready for fabrication or flight.** Fresh ERC and
targeted netlist checks pass. A current PCB, full device-model fault validation,
measured load envelope, firmware integration and hardware qualification are missing.
No hardware was powered or measured in this review.

## Which files are current

Use `Osiris_PDB_RevA.kicad_sch` in this project. It has 39 components and 28 nets.
The September 9 archive has 33 components; Power_Distribution_Boardv1 has 22.
Comparison details are in `revision-audit-20260912/design-checks.json`.
The active design adds C9, D1/D2/D3 and TP6/TP7 relative to the archive, along with
connector, gate-network and component-property revisions. The current `.kicad_pcb`
was already deleted in the pre-review Git working tree. The obsolete layout was
not restored because it does not implement this design.

The workspace has no reliable per-edit author history for the uncommitted changes.
Findings below describe saved files, not an assertion about which assistant wrote them.

## Corrections and remaining design issues

1. **Reverse-battery branch was already repaired in the latest schematic.** U3 IN/EN
   and its C4 input capacitor are on protected PDB_VOUT, not VBAT_FUSED. Keep this.
   D3 clamps negative output excursions, but its real forward voltage and transient
   current must be checked against every downstream pin's negative-voltage rating.
   The generic simulation diode cannot prove compliance with a -0.3 V limit.
2. **Gate network is correctly separated in the current netlist.** C1 is on U1 GATE;
   R4 connects it to both FET gates; D2 provides the discharge bypass. Gate protection,
   actual MOSFET charge and SOA still need device-specific checks.
3. **F1 is already marked provisional in the current schematic.** Retain 4 A as a
   candidate. The old claim that 2.22 A is an established maximum is unsupported.
   This is a rail-budget calculation with assumed loads and efficiency. Moderate
   overloads below the nominal 10 A electronic trip can instead be cleared by F1;
   it is false that the electronic breaker always operates first for every overload.
   Fuse time-current behavior, temperature and available fault current remain open.
4. **Osiris reference variants disagree on the pull-up rail.** Original ZIP-derived
   reference data puts R74/R75 on +3V3. The supplied
   `Kicad/OsirisRevB/Hardware/OSIRIS/OsirisRevA.kicad_pcb` puts them on ST_LINK_T_PWR.
   That PCB also contains 19 duplicated nonempty reference names. These are release
   blockers for that imported implementation, not a reason to blindly rename its nets.
   Establish which Osiris hardware will fly and verify the actual powered bus.
5. **Power connector numbers differ between libraries.** Current PDB J3 is pin 1 GND,
   pin 2 PDB_VOUT. Osiris J16 is pad 1 VBATT_IN, pad 2 GND. Connect positive to positive
   and ground to ground by verified physical contact polarity; do not make a numbered
   1-to-1 power cable from these netlists. J15 is VBATT_OUT, not the input.
6. **Documentation corrected.** The old frozen specification described an 80 A
   four-ESC distributor. It has been superseded by the present avionics-only scope.
   Historical requirement/simulation claims are not release approval.

## How power reaches Osiris

4S battery → J1 → F1 → LTC4368-controlled back-to-back Q1/Q2 → 5 mΩ R5 →
J3 → verified power harness → Osiris J16 VBATT_IN → Osiris input protection U21
(LM73100) → Osiris converters → local 5 V and 3.3 V rails.

U3 supplies the PDB's 3.3 V monitoring electronics from the protected output.
This PDB supplies **protected, unregulated battery voltage**. It does not generate
a regulated 12 V, 5 V or 3.3 V power feed for Osiris. ESC/motor current must use a
separate appropriately designed power path.

Nominal divider thresholds are approximately 10.56 V UV and 18.68 V OV; the
electronic forward breaker is nominally 10 A with the 5 mΩ shunt. These are protection
settings, not a 10 A continuous load rating. An undervoltage or overcurrent trip can
remove the flight controller's power. Automatic retry does not preserve flight control:
Osiris and the PDB monitor may reset and must restart/reconfigure. Battery warning and
landing must happen before that state; pack voltage alone does not protect each cell.

## How data reaches Osiris

U2 INA228 measures this avionics branch's shunt current and output bus voltage and
can accumulate power, energy and charge. It does not measure total propulsion current.
Osiris's FMU acts as the I²C master and polls U2 at 7-bit address **0x40**. There is
no PDB processor, CAN transmitter, radio or autonomous packet stream.

| PDB J2 contact | Signal | Osiris J28 contact |
|---|---|---|
| 1 | Intentionally unconnected; do not import +5 V | 1, +5V0_PROT |
| 2 | SCL, 3.3 V logic | 2, FMU_I2C1_SCL |
| 3 | SDA, 3.3 V logic | 3, FMU_I2C1_SDA |
| 4 | GND | 4, GND |

Verify actual harness continuity; a connector family name alone does not prove cable
pin mapping. Alert/fault signals terminate at TP6/TP7, not at J28.
Firmware must enable the correct external bus, identify INA228, program conversion
and averaging settings and shunt calibration for 5 mΩ, handle timeouts and resets,
and publish this as an avionics monitor rather than total aircraft battery current.
ADCRANGE=1 clips above approximately 8.192 A with this shunt, below the nominal breaker;
use the wider range if recording higher pre-trip current is required. Firmware support
and other devices' addresses on the selected external bus have not been validated.

With the reference 12 kΩ pull-ups, tr≈0.8473·R·C: 100 pF gives about 1.02 µs.
This is already near the 1 µs Standard-mode limit; Fast-mode's 300 ns corresponds
to only about 29.5 pF. Start integration at 100 kHz, measure rise time at both ends,
then select total pull-up resistance against bus capacitance and sink-current limits.
Do not assume that omitting PDB pull-ups guarantees a reliable cable interface.

## How clean is the delivered power?

**Ripple and transient cleanliness are not established.** The protection controller
disconnects faults; it is not an active ripple filter. Local ceramic capacitance helps
at some frequencies, but no intentional series-inductor filter is present. Battery
ripple, motor-induced droop, harness ringing and ground offsets can reach Osiris.
Osiris's converters then regulate their own rails; their output quality needs separate
measurement under actual load.

For scale only, 23.48 mΩ cold fuse + 5 mΩ shunt + 3.1 mΩ FET pair gives 31.58 mΩ:
at the assumed 2.22 A this is about 70 mV drop and 0.156 W. This excludes PCB,
holder, connector and cable resistance and assumes the FET datasheet resistance
test conditions; gate voltage and temperature change it. The earlier 75 mΩ complete
path assumption predicts 167 mV and 0.370 W at 2.22 A. Neither is a measured result.

Measure at J16 with the final harness and at the sensitive regulated rails. Record
DC minimum, peak-to-peak ripple, hot-plug overshoot, startup, load steps, motor ramp
and low-battery sag. Use a short-ground differential/appropriate probe setup and
record bandwidth. Set acceptance limits from the actual Osiris load/converter limits
and guaranteed ratings, with margin. A TVS's advertised clamp value or zero ERC
errors does not establish safe downstream transient voltage.

## Checks and evidence

- Fresh KiCad 10.0.5 ERC: **0 errors, 0 warnings**. Project settings ignore four
  check categories, including SPICE models and footprint filters; see the report.
- Fresh XML checks: power polarity by net, Kelvin taps, gate diode orientation,
  U3 protected supply, J2 mapping, INA228 address straps and provisional fuse status pass.
- All 39 BOM reference/value/MPN/footprint entries match the export; footprint files
  resolve. This does not independently certify every land pattern or component rating.
- SVG export succeeds. No current PDB PCB exists, so PDB DRC, routing, copper-current,
  thermal layout and schematic-to-PCB parity cannot pass yet.
- Eight-case LTspice screening rerun recorded separately in
  `revision-audit-20260912/simulation-rerun.log`. This uses the existing source deck,
  not independently validated replacement device models. No hardware qualification.

The deck uses substitute MOSFETs, a generic Schottky, a behavioral TVS, a simplified
LM73100, and a resistor-only fuse. Its single 100 ms short does not validate sustained
retry heating. It omits realistic motor interference, actual load sequencing and
worst-case device tolerances. Small modeled I²t is evidence for that model only;
it does not certify fuse coordination, real diode voltage or FET survival.

## Rev A completion plan, in order

1. **Freeze interfaces and loads.** Select the exact Osiris revision, Jetson power
   mode, peripherals, harness length, battery range and environmental limits. Measure
   startup/steady/peak demand. Resolve J16 physical polarity and the J28 pull-up rail.
2. **Close electrical margins.** Review real MOSFET SOA, VGS and reverse hot-plug;
   D3 negative clamp under actual current; TVS energy and downstream overshoot; shunt
   pulse rating; fuse opening/interrupt capability and holder retention. Test moderate
   overload as well as hard short. Include tolerances, source impedance and temperature.
3. **Complete the PDB PCB.** Agree mounting/enclosure constraints, place protection
   and capacitors close to their loops, route the shunt as true Kelvin connections,
   keep high-current return away from sensing, and provide test access. Check every
   footprint against its current manufacturer drawing; then run ERC, DRC and net parity.
4. **Build bench prototypes.** Inspect/continuity-check first, then current-limited
   dummy-load startup and voltage sweeps; staged loads, thermal soak, reverse input,
   transient injection and appropriately controlled faults. Validate sustained retry
   behavior and verify safe fault energy before connecting expensive Osiris hardware.
5. **Integrate firmware and Osiris.** Confirm 0x40 discovery, calibrated current/voltage,
   rise times, bus recovery, reconnect and power-cycle handling. Test startup with all
   intended loads, UV/OV transitions and telemetry logging.
6. **Qualify the assembled aircraft.** Measure power during representative propulsion
   load changes, check EMI, vibration, harness retention and brownout behavior. Progress
   through controlled ground/tethered tests before flight release. Keep measured records
   and release only with no unexplained resets or violated electrical/thermal limits.

The architecture is a plausible avionics feed for the assumed roughly 23 W case.
It is not yet demonstrated sufficient for normal flight, and it is not a motor PDB.

## Primary references

- [ADI LTC4368](https://www.analog.com/en/products/ltc4368.html)
- [TI INA228 datasheet](https://www.ti.com/lit/ds/symlink/ina228.pdf)
- [TI LM73100 datasheet](https://www.ti.com/lit/ds/symlink/lm7310.pdf)
- [TI TPS7A16 datasheet](https://www.ti.com/lit/ds/symlink/tps7a16.pdf)
- [NXP I²C specification](https://www.nxp.com/docs/en/user-guide/UM10204.pdf)
