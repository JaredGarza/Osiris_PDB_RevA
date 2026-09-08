# Osiris PDB Rev A — Frozen Prototype Specification

## Purpose

A 4S quadcopter power-distribution board that powers four external ESCs and
supplies a separately fused raw-4S branch to Osiris J15.

## Frozen assumptions

- Battery: 4S LiPo, 12.0 V to 16.8 V.
- Expected propulsion baseline: four approximately 15 A motors.
- ESC branch design target: 20 A continuous, 30 A short burst each.
- Complete motor-bus prototype target: 60 A expected, 80 A design target.
- Board: 55 mm x 55 mm, 30.5 mm square M3 mounting pattern.
- Stackup: four copper layers; specify 2 oz copper on every layer for the
  prototype quote.
- Battery and ESC connections: soldered pigtails, not rigid board-mounted XT60s.
- Battery pigtail: genuine XT60 and 12 AWG wire.
- ESC pigtails: 14 AWG wire or sized to the selected ESC.
- Osiris pigtail: XT60 male and 16/18 AWG wire.

These current ratings remain prototype targets until verified thermally with
the selected battery, ESCs, motors, propellers, airflow, and wire lengths.

## Power tree

```text
4S BATTERY_IN
    |
    +-- main VBAT/GND planes
            +-- ESC1_OUT
            +-- ESC2_OUT
            +-- ESC3_OUT
            +-- ESC4_OUT
            +-- F1 --> OSIRIS_FUSED --> OSIRIS_OUT --> Osiris J15

Across main bus: D1 SMCJ17CA + C1 1000 uF/35 V + C2 100 nF/50 V
Across Osiris branch: D2 SMCJ17CA + C3 1 uF/50 V + C4 100 nF/50 V
Optional branch bulk: C5 100 uF/35 V, DNP until transient testing
```

## Intentional omissions

- No onboard charger or cell balancer.
- No LibreSolar BMS MOSFET bank.
- No 5 V or 3.3 V converter; Osiris already contains them.
- No duplicate LM73100; Osiris already contains one at J15.
- No onboard ESC switching in Rev A; the four outputs feed external ESCs.
- No total-current sensor in Rev A. It will be selected after propulsion
  current is known, preferably as a Hall sensor or correctly rated 4-terminal
  shunt in the combined revision.
- No PCB main fuse. Use an appropriately rated external inline fuse during
  prototype testing; final aircraft main protection follows the propulsion
  current budget.

## Acceptance gates

1. Connector polarity, wire exit, and mounting geometry verified physically.
2. Schematic and every land pattern independently reviewed.
3. ERC/DRC clean with no unconnected copper.
4. Dummy-load tests pass before Osiris is connected.
5. Osiris branch current stays below 5.5 A.
6. Bus and connector temperature rise is acceptable at staged loads.
7. Oscilloscope confirms J15 transients remain below the agreed margin to the
   LM73100 28 V absolute maximum.
8. Motor testing is performed without propellers first.

