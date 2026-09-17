# Simulation and schematic review - 15 September 2026

## Decision

**Nominal power-path screening passes. The design is not ready for fabrication release.**
The expanded startup sweep exposes inadequate margin to the minimum electronic
breaker threshold. This is a modeled risk, not a measured hardware failure.

The schematic already contained the 5 A fuse, 8 mOhm shunt and gate-feedback
changes when this review began. This review repaired the remaining grid defects,
preserved every component pin-to-net connection, corrected misleading model
behavior and documentation, and reconciled the BOMs. No electrical component
value was changed in the schematic during this review.

## Verified changes

- **Schematic:** corrected R16-R18 wire/label endpoints to the existing snapped
  symbol row. Final ERC: **0 errors, 0 warnings**. Existing ignored categories
  are unchanged and listed in `audit/erc.rpt`. The rendered sheet was visually
  inspected: the relocated resistors clear the annotation text and title block.
- **Source consistency:** 48 components; every CAD pin/net preserved relative to
  the review-entry export. Both BOMs match all schematic values, footprints and
  order-code fields. Purchasing BOM also retains the separate fuse-holder entry.
  Matching an order-code field does not confirm that part is available or qualified.
- **Current model:** `pdb/pdb_current.lib` uses the actual R1/R2/R3/R13/R14 and
  R15-R18 designators, without experimental feedback resistors that are absent
  from CAD. Passive nodes/values, shunt and controller/LDO mappings are checked.
- **Soft start:** replaced the arbitrary 2 ms buck ramp with 18.868 ms for the
  documented 100 nF capacitors, using AP64501 Equation 7. The 0.8 V reference
  and 570 kHz frequency are also documented by the manufacturer. The averaged
  model still does not represent switching or compensation.
  [Diodes AP64501, DS41980 Rev 5-2](https://www.diodes.com/datasheet/download/AP64501.pdf).
- **Unpowered behavior:** removed constant quiescent-current sinks at zero
  supply; gated buck delivery by enable and available input voltage; made digital
  boot ramps follow rail validity and reset after collapse. Dedicated model
  invariant tests pass. This removes phantom loading, not real-device uncertainty.
- **Measurements:** short-circuit I-squared-time now starts at 899.9 ms, before
  the switch closes at approximately 899.96 ms. The prior 900 ms start missed
  the initial fault pulse. Removed the unreliable derivative edge counter and
  retry-crossing requirements that failed on legitimately stable cases.
- **Verification:** Windows-compatible Python runner rejects stale/incomplete
  logs, nonzero exits, timeouts, missing measurements, numerical warnings and
  values outside explicit limits. Exploratory decks report `RUN_OK`, not an
  electrical pass. Failure-injection tests verify these checks.
- **Documentation:** removed claims of independent measured-load validation,
  guaranteed thermal safety, latch-off and completed qualification. Corrected
  5 A/8 mOhm annotations and the proposed INA228 calibration to SHUNT_CAL=5243
  for CURRENT_LSB=50 uA and ADCRANGE=0. Firmware was not present or changed.

## Results for the current schematic population

These are nominal/surrogate results, not production tolerances.

| Test | Observed result |
|---|---|
| Startup, 12 / 14.8 / 16.8 V and degraded harness | All four reach nominal rails |
| Steady rails | About 5.161 V and 3.305 V; local PDB rail about 3.28 V |
| Startup source-current peaks | 2.33-3.05 A across the four nominal cases |
| Nominal 14.8 V startup | PDB about 35 ms; 5 V about 54 ms; 3.3 V about 117 ms |
| OV/UV excursions and short removal | Rails recover; UV recovery is slower than the old report implied |
| Short recovery | 3.3 V crosses 3.1 V at about 1.533 s after a short removed at 1.100 s |
| Short I-squared-time | 0.2949 A²s at 20 us maximum timestep; 0.2974 A²s at 2 us and tighter tolerance (0.85% change) |
| Short peak source current | About 184 A; surrogate result, not a FET survival rating |
| Reverse input -14.8 / -16.8 / -25 V | Output isolation/recovery screening bounds pass |
| 500 mOhm source, stepped down after startup | Four tested cases settle; 11.2/11.4 V turn off, 11.6/11.8 V remain on |
| 700/900 mOhm source | Some tested cases still retry cyclically |

The 500 mOhm result is history-dependent: these decks first start at 14.8 V.
It does not imply cold startup at 11.6 V. UV gate-feedback hysteresis is not
a latch and does not establish a battery discharge/landing limit.

## Open issue: startup current margin

`current_corners.cir` uses an 8.08 mOhm shunt (+1%), capacitance at 120% of
nameplate (no assumed DC-bias reduction), and eFuse slew sensitivities of
12.14, 28.1, 44.78 and 60 V/ms. The last is an assumed stress case; the
manufacturer's typical slew depends on input voltage and is not a guaranteed
temperature/process maximum. Cross-combining typical slew values with other
input voltages is deliberately a sensitivity test, not a vendor tolerance corner.
[TI LM73100, table 6.7](https://www.ti.com/lit/ds/symlink/lm7310.pdf).

**Two of eight cases fail to boot:** 12 V with the two fastest slews. The highest
peak is about 7.02 A. Several other cases boot with peaks above the conservative
4.9 A screen, near the 4.95 A normal-condition minimum trip calculated from
40 mV / 8.08 mOhm. The encrypted controller is nominal; these tests do not
instantiate every controller threshold/propagation-delay corner.
[ADI LTC4368 datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/ltc4368.pdf).

A **simulation-only C1=22 nF** alternative (`slowgate_corners.cir`) restores
booting in all eight cases but still peaks at 5.46 A. It therefore fails the
same conservative current-margin check and was **not applied to the schematic**.
Increasing a gate capacitor also changes fault turn-off energy; startup alone
cannot justify that substitution.

Closure requires coordinated Osiris eFuse slew control/enable sequencing and PDB
breaker selection using guaranteed limits, then fault-energy and bench validation.
Do not raise the fuse rating or bypass the breaker merely to force these cases
to pass. The default verification command intentionally returns failure while
the current startup stress test remains outside its limits.

## Other unresolved hardware limits

1. **INA228 negative inputs:** the existing Schottky does not guarantee the
   required negative-voltage limit at IN+, IN- and VBUS. The analog stub has
   no accurate clamp/damage model. No speculative diode substitution was made.
2. **Fuse/FET/TVS coordination:** fuse models never open. Short-pulse I²t is
   not fuse clearing energy, and integrating normal current for seconds cannot
   be compared with adiabatic fuse I²t to predict melting. MOSFET safe operating
   area, avalanche, temperature, source fault duty and repeated-retry heating
   require actual component and assembly evidence.
3. **Gate feedback:** 20 MOhm resistor availability/tolerance, contamination
   leakage, temperature drift, controller leakage and gate-drive corners remain
   unqualified. The nominal trip-point sweep cannot close these items.
4. **I2C:** R17/R18 now pull to the local PDB rail. Account for host pull-ups,
   bus capacitance and mixed-power backfeed before mating boards. FAULT/ALERT
   remain testpoint-only; no firmware alert transport was added.
5. **Osiris abstraction:** load budgets, efficiency, current ceilings and
   sequencer delay remain assumptions; the inductor value conflict and converter
   loop compensation are not resolved by an average model. Actual module/port
   loads and power sequencing must be defined.

## Reproduction and evidence

Run `python verify_all.py` in this directory. Expected outcome is nominal checks
passing and the startup stress cases failing until the electrical issue is fixed.
Run `python audit/test_runner.py` for failure-injection checks and
`python audit/check_connectivity.py` after exporting the final KiCad XML netlist.

See `audit/verification.json`, `audit/connectivity.json`, `audit/erc.rpt` and
`audit/render/schematic.png`. Backups preserve the review-entry schematic,
BOMs and original simulation files. No PCB layout, fabricated board or bench
test was available; this review is not manufacturing or flight approval.
