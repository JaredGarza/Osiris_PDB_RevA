# PDB / Osiris interface proposal

**15 September 2026 - proposed requirements, not a released interface.**
Jared confirmed that the Jetson configuration, other loads, board dimensions and
harness constraints are not decided. The limits below give those decisions a
concrete starting point. They are not measured capabilities of the PDB or promises
about an unspecified Jetson configuration. Active schematic: **A-P2-DRAFT**.

## 1. Proposed electrical boundary

The PDB supplies one protected, unregulated 4S avionics branch. Osiris makes its own
regulated rails and controls their startup. Propulsion uses a separate power path.
No power converter for the Jetson has been selected or changed in this task.

| Item | Proposed requirement | Closure evidence |
|---|---|---|
| Normal input | 12.0-16.8 V at J1 | Exact battery and its allowed operating range |
| Continuous Osiris load | At J3, **both <=25 W and <=2.5 A** | Actual rail budget, efficiency and simultaneous-load measurements |
| Transient demand | No additional peak allowance yet; stay within 2.5 A except the controlled capacitive startup below | Measured startup/peak duration and repetition |
| Capacitance during startup | <=220 uF maximum input-equivalent total, including PDB capacitors, harness and Osiris; include positive tolerance | Actual converter topology and capacitance inventory |
| Startup load | Osiris holds high-power loads off until its input and rails are valid; never demand constant power from a near-zero input | Converter enable/UVLO schematic and timing capture |
| Path resistance | <=75 milliohms target for the complete battery-to-Osiris feed and return at operating temperature | Four-wire measurement including holders, connectors, copper and cable |
| Normal drop | <=0.188 V at 2.5 A for that path target | Loaded measurement |
| Local environment | Initial qualification target 0 to +60 C inside the enclosure at the fuse; not just outside-air temperature | Enclosure thermal test; expand range only after rerating |
| Availability | A PDB trip may remove FMU and Jetson power. Continuous operation through a trip is not provided | Team decision on whether a separate FMU supply is required |

Illustrative 25 W load plus 0.1 W PDB housekeeping, with the 75 milliohm path:

| Battery | Estimated input current |
|---|---:|
| 16.8 V | 1.50 A |
| 14.8 V | 1.71 A |
| 12.0 V | 2.12 A |
| 10.175 V illustrative lowest UV corner | 2.51 A |

Thus the 25 W allowance must be reduced near undervoltage to honor the separate
2.5 A limit. The normal envelope starts at 12 V. Neither this table nor the PDB
cutoff defines a safe battery-discharge or landing threshold.

### Load allocation to complete when hardware is selected

| Load | Required inputs still missing |
|---|---|
| Jetson | Exact module, power profile, supply requirement, peak demand and startup sequence |
| FMU and retained avionics | Rail currents, brownout limits, mandatory always-on circuits |
| USB / debug | Which ports may source power, maximum demand and isolation arrangement |
| Sensors / radios / cameras / peripherals | Part list, simultaneous rail demand and startup peaks |
| Osiris converters | Efficiency at low battery, input capacitance, UVLO, soft-start and fault behavior |

Required rail-budget check: sum of each rail's maximum simultaneous output power
divided by its minimum converter efficiency, plus board overhead, must satisfy
both PDB output limits. Do not assign the entire 25 W to the Jetson.

## 2. Contact-level wiring

| PDB connector/contact | Electrical function | Required mating connection |
|---|---|---|
| J1 pin 1 | GND | Battery negative |
| J1 pin 2 | VBAT_RAW | Battery positive, through the correct protected harness |
| J3 pin 1 | GND | Osiris power-entry negative contact |
| J3 pin 2 | PDB_VOUT | Osiris raw-battery positive contact |
| J2 pin 1 | NC | Omit the conductor where practical; never attach a power source |
| J2 pin 2 | SCL | Selected Osiris FMU external I2C SCL |
| J2 pin 3 | SDA | Same FMU bus SDA |
| J2 pin 4 | GND | Osiris signal ground |

The PDB netlist mapping is verified. New Osiris connector references and physical
contact views remain unassigned. Old Osiris J16 numbers differ from the PDB power
connector numbers; verify physical polarity instead of wiring by equal numbers.
J2 does not carry alert/fault wires; TP6/TP7 remain bench access only.

**Proposed harness:** each power lead pair <=300 mm, initially 18 AWG copper;
I2C cable <=300 mm. These are packaging proposals, not ampacity certification.
Confirm insulation temperature, strain relief, routing and contact retention.
Keep positive and return together; provide a real power-return conductor so the
I2C ground is not the intended load return. Fit and continuity tests are mandatory.

## 3. I2C and telemetry

- Start at 100 kHz. Current PDB R17/R18 provide 4.7 kilohm pull-ups to PDB_3V3.
  Account for existing Osiris pull-ups and mixed-power backfeed before connection;
  do not add the formerly proposed host 2.2 kilohm pair without recalculation.
- Proposed total bus capacitance <=200 pF, including both boards and cable.
  Estimated rise time is 0.804 us at the high resistor corner; estimated sink
  demand is 0.69 mA with a 3.6 V pull-up rail and 0.4 V low level.
- Measure at both ends; require rise <=1 us and low <=0.4 V. Cable length alone
  does not establish capacitance. [NXP I2C specification](https://www.nxp.com/docs/en/user-guide/UM10204.pdf).
- INA228 address 0x40; use ADCRANGE=0. Proposed CURRENT_LSB=50 uA and SHUNT_CAL=5243
  for nominal 8 milliohms. Program and read back calibration after every reset.
- Begin with continuous bus/shunt conversions, 1.052 ms each and 16 averages;
  publish at 10 Hz with timestamps. Temperature sampling can be enabled separately.
- Label readings **avionics branch**. Handle NACKs, stuck bus, missing updates and
  power cycles. Mark data invalid after three missed 10 Hz updates; never use a
  missing reading as zero consumption. Confirm the address against the final bus.
  [TI INA228 datasheet](https://www.ti.com/lit/ds/symlink/ina228.pdf).

## 4. Source and fault states required of new Osiris

| State | Required behavior / decision |
|---|---|
| Battery valid, other sources absent | Controlled startup; remain inside load and capacitance budgets |
| USB/debug only | No backfeed into J3 or J2 pin 1; FMU-only operation depends on explicit Osiris power routing |
| Battery plus USB/debug | Defined source priority/isolation; no supply contention |
| PDB UV/OV/overcurrent trip | Treat FMU/Jetson loss and restart as possible; record telemetry gap |
| Retry after fault | Reinitialize rails and INA228; do not assume configuration survived |
| Peripheral fault | Osiris must isolate it if continued FMU operation is required |
| PDB powered while FMU off, and vice versa | Verify pin limits, bus recovery and absence of back-powering |

The PDB's reverse-current breaker has a large current threshold. It does not by
itself provide the low-current USB/debug backfeed isolation required above.
Battery warning/landing and any redundant-power architecture remain system
decisions, not automatically resolved by keeping the existing UV divider.

## 5. Mechanical proposal

Start placement feasibility with **80 x 50 mm**, four **3.2 mm** mounting holes at
(5,5), (75,5), (5,45), (75,45) mm from the lower-left board corner; allow 25 mm
above-board space initially. Leave connector mating, wire bends and fuse removal
accessible. These dimensions have **not** been checked against the aircraft or a
component placement and are not frozen. Keep copper/components clear of the
actual screw-head/washer envelopes on both sides.

## 6. What finishes step 1

Accept or revise these proposed bounds; select the actual loads and source states;
complete the two-ended harness drawing; verify the mounting envelope against the
airframe. Until then M1 is **proposed**, not final. Preliminary placement can use
this proposal, with possible mechanical and electrical rework.
