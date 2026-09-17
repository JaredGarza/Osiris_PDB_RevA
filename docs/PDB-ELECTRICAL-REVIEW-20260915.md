# PDB electrical review and A-P2 draft change

**Later September 15 update:** the active schematic now has 48 components, F1=5 A and R5=8 mOhm. See [simulation/design review](../Simulation/combined-20260915/REVIEW.md). Earlier numerical population/threshold tables below describe the previous draft.

**15 September 2026. M2 remains open. No fabrication or flight release.**

The current schematic is **A-P2-DRAFT: 42 components, 28 nets**. This review
implements one electrical correction and reconciles component metadata. It also
identifies remaining issues that cannot be closed by declaring the design final.
The companion [interface proposal](PDB-INTERFACE-PROPOSAL-20260915.md) uses bounds
proposed after Jared confirmed the loads and mechanical constraints are undecided.

## Implemented: reverse-current-protected local regulator

U3 changed from TPS7A1633DGNR to **LT3010EMS8E#TRPBF**. The former device's
OUT-IN absolute maximum is +0.3 V; charged output capacitance during an input
collapse created an unaddressed stress. [TI TPS7A16 datasheet](https://www.ti.com/lit/ds/symlink/tps7a16.pdf).

The LT3010 provides reverse-input and reverse-current protection. Added R11=1.58k,
R12=1k and C10=100n across R11, giving nominal 3.2896 V. C10 satisfies the
manufacturer's compensation topology; its impedance at 10 kHz is about 177 ohms
at 90 nF versus the 1k lower resistor. Keep C6 effective capacitance >=1 uF and
ESR <=3 ohms over voltage/temperature; verify the selected ceramic's bias curve.
The divider draws at least about 1.22 mA at the initial tolerance corner.
Reference/resistor corner calculation gives 3.153-3.430 V before additional drift
and transient allowance. Proposed assembled acceptance is 3.10-3.50 V steady,
with overshoot remaining below the 3.6 V operating ceiling of U4.

At a deliberately conservative 5 mA local output and 0.7 mA ground-current
allowance, estimated dissipation at 16.8 V is 80 mW. This is not a measured thermal
result. Pin mapping: 1 OUT, 2 ADJ, 3/6/7 NC, 4/9 GND, 5 SHDN, 8 IN. IN and SHDN
remain on PDB_VOUT. The MS8E 0.65 mm pitch and 1.68 x 1.88 mm exposed pad match the
assigned KiCad MSOP footprint; solder pad 9 to ground. Startup and stability remain
bench checks. [ADI LT3010 datasheet, pin table, Figure 2 and package drawing](https://www.analog.com/media/en/technical-documentation/data-sheets/lt3010-3010-5.pdf).

This change addresses U3's identified reverse-bias mechanism. It does **not**
qualify negative transients at the separate INA228 inputs. New resistor order
codes: R11 RC0805FR-071K58L, R12 RC0805FR-071KL. C10 reuses the existing KEMET
C0603C104K4RACTU. R11's individual manufacturer specsheet could not be retrieved;
confirm it before purchasing. [YAGEO R12 specification](https://yageogroup.com/component-documentation/download/specsheet/RC0805FR-071KL).

## Protection calculations and corrections

Calculations are reproduced by [check_review.py](interface-review-20260915/check_review.py)
and saved in [calculations.json](interface-review-20260915/calculations.json).
Threshold bounds include 1% initial resistor tolerance, comparator tolerance and
independent +/-10 nA divider-pin leakage corners. They exclude resistor temperature
drift, aging and layout/noise. They are desk-review bounds, not final test tolerances.

| Quantity | Result / interpretation |
|---|---|
| UV falling | 10.175-10.957 V |
| UV recovery | 10.589-11.646 V |
| OV rising | 18.003-19.372 V |
| OV recovery | 16.831-18.610 V |
| Forward trip, normal specified conditions | 7.92-12.12 A with 1% shunt |
| Forward trip, datasheet zero-output condition | 5.94-14.14 A; not a hard ceiling on fault overshoot |
| Reverse trip magnitude | 8.32-11.72 A |
| Gate ramp estimate, C1 tolerance and charge current | 3.40-11.28 kV/s |
| Estimated ramp to 16.8 V | 1.49-4.94 ms, before real FET/load dynamics |
| 220 uF estimated capacitive inrush | 0.75-2.48 A; plus 2.5 A load gives about 4.98 A |
| Stored energy, 220 uF at 16.8 V | 31 mJ |

The controller specifies 3-18 us overcurrent propagation under a particular 2.2 nF
test condition; this populated 5.6 nF network is different. Its 10-13.1 V gate-drive
range at 12-60 V input corrects the old use of the 5 V-input specification. Do not
carry either specification unchanged into ringing/short-circuit waveforms.
[ADI LTC4368 datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/ltc4368.pdf).

**Startup is a screening calculation only.** A live downstream converter can
change the ramp. Account for local-regulator charging current as well. Use the
actual input-equivalent capacitance and startup sequence before signing this off.
The old claim that a simple capacitive divider proves no gate-source hot-swap
capacitor is needed is withdrawn: C1 is separated from the FET gates by R4, and
FET capacitance depends on voltage. Reserve a gate-source capacitor footprint in
layout feasibility; determine stuffing from real transient analysis and testing.

### F1: correct manufacturer data

Retain 4 A as a **conditional prototype selection** for the proposed load envelope.
The September 2024 manufacturer datasheet states **1000 A at 32 VDC** interrupting
rating. WXNV denotes **3000-piece packaging**, not 3000 A interruption. Its 4 A
typical I2t is **31 A2s**, versus 17 in the older archived copy. That is typical
pre-arcing data, not a guaranteed total-clearing energy limit.

Manufacturer typical allowed-current guidance gives 2.9 A at 60 C for the 4 A fuse;
the 2.5 A proposal has only 0.4 A margin before application-specific effects.
At 8 A, opening can take 0.15-5 seconds; at 5.4 A it can take up to 600 seconds.
The electronic breaker need not trip at those currents. Wiring, holder and copper
must survive the applicable interval.

An idealized 16.8 V / 1000 A calculation yields 16.8 milliohms. Establish the actual
minimum fault-loop impedance and interrupting duty, including faults upstream of
the MOSFETs; do not count resistance absent from that fault path. The exact pack
is still unknown. [Littelfuse current MINI datasheet](https://www.littelfuse.com/assetdocs/littelfuse-datasheet-297-mini32v?assetguid=42c9dd21-a88e-4328-8e67-2f832444faf1).

### Q1/Q2, shunt and transient energy

The selected FET is 60 V with +/-20 V gate limits. Its hot-case SOA graph was
visually reviewed; the broad current rating alone is not a fault qualification.
Normal startup appears plausible under the proposed envelope, but real per-FET
VDS/current/time trajectories and repeated-retry heating remain unbounded.
Keep each trajectory inside the appropriate temperature/pulse curve, with an
explicit design margin and measured case temperature. Do not divide fault energy
equally between back-to-back FETs without a circuit argument.
[Infineon device datasheet, diagrams 3-5](https://www.infineon.com/assets/row/public/documents/24/49/infineon-isc015n06nm5lf2-datasheet-en.pdf).

R5 steady dissipation at 2.5 A and high resistance is about 32 mW. At the 14.14 A
corner it is about 1.01 W, excluding any overshoot. Its 2 W label does not establish
pulse survival at battery-limited short current; obtain pulse/thermal evidence and
retain true Kelvin routing.

D1's 38.9 V clamp applies at the specified pulse current/waveform, not arbitrary
surges. Source/harness inductance and pulse repetition determine energy. Check
positive and negative input, including a reversed input while output capacitance
is charged. A 38.9 V negative excursion opposed by a 16.8 V charged output suggests
55.7 V differential stress before other drops/ringing: too close to a 60 V device
to call qualified without the actual waveform.
Also check the controller's -40 V input limit: a -38.9 V nominal specified clamp
leaves only 1.1 V for additional undershoot. A lower-standoff bidirectional TVS
may improve this margin, but its cold breakdown must still clear the worst OV
window and its energy rating must fit the final source.
[Bourns SMAJ datasheet](https://www.bourns.com/docs/product-datasheets/smaj.pdf).

## Remaining design blocker: negative INA228 input voltage

D3 is an MBR0540, whose 25 C forward-voltage limits include 0.51 V at 0.5 A and
0.62 V at 1 A. It does not guarantee a -0.3 V clamp. The INA228 IN+, IN- and VBUS
limits therefore remain unproven. VBUS is connected directly to PDB_VOUT; a
resistor-only argument for the sense inputs would not protect that pin.
[onsemi MBR0540 datasheet](https://www.onsemi.com/pdf/datasheet/mbr0540t1-d.pdf),
[TI INA228 datasheet](https://www.ti.com/lit/ds/symlink/ina228.pdf).

Required closure: define the worst negative waveform and source impedance; design
and verify protection at all three pins or select a monitor with suitable negative
common-mode tolerance. Include clamp leakage/measurement error and temperature.
Do not assume an arbitrary Schottky or a series resistor alone satisfies both
voltage and current limits. No speculative clamp substitution was applied.

## Specific release gates

| Gate | Status | Evidence still required |
|---|---|---|
| Source/load/data/mechanical interface | Proposed | Actual selected hardware satisfies the companion limits; physical mating/mounts verified |
| U3 reverse-bias correction | Implemented in draft | Confirm C6 effective capacitance; measure startup, collapse/recovery and local rail limits |
| INA228 negative-input protection | Open design issue | Complete protected input network or qualified alternate monitor |
| Fuse interruption and overload protection | Open system/layout issue | Pack fault-current bound; cable/holder/copper thermal coordination |
| FET/TVS survival and retry | Open validation issue | Actual models/trajectories, parasitics, worst temperature and repeated-fault energy |
| All footprints | Partially checked | U3 package checked; remaining land patterns/contact polarity independently checked |
| Documentation/BOM consistency | Passed for current source | Repeat after further ECOs; old procurement workbook/freeze remains historical |

## Bench acceptance worksheet to execute after design closure

Use a current-limited source and dummy load first. Record equipment, temperature,
source settings, probe locations/bandwidth, screenshots and pass/fail for every row.
Do not substitute a bench supply's current limit for the eventual battery fault duty.

| Test | Required observation |
|---|---|
| Inspection and continuity | No unintended shorts; correct connector polarity and populated parts |
| 12 / 14.8 / 16.8 V startup, minimum and maximum capacitance | Repeatable startup; measured load/inrush inside approved budget |
| Local rail at light/heavy housekeeping load | 3.10-3.50 V steady; no unstable oscillation or >3.6 V overshoot |
| Collapse U3 input with charged local output | Safe LT3010 recovery and no abnormal reverse current; reset handled |
| 0.5 / 1 / 2 / 2.5 A load and thermal soak | Resistance <=75 milliohm target for full path; temperatures inside selected limits |
| UV/OV sweep and recovery | Compare to a finalized tolerance model, including TCR; no unexplained cycling |
| Moderate overload and controlled short | Measured clearing behavior, per-FET stress and conductor temperatures acceptable |
| Sustained fault/retry | Observe to thermal equilibrium; no ratcheting temperature or unbounded energy |
| Positive/reverse hot-plug, charged/discharged output | Every monitored pin inside absolute limits with design margin |
| Telemetry calibration and mixed power states | Correct signed readings, calibration persistence/reinitialization, no backfeed or stuck bus |

No hardware tests or new full-device fault simulation were run in this task.
The previous surrogate cascade simulation predates this ECO and does not validate it.

## Verification and file control

- Fresh KiCad ERC: **0 errors, 0 warnings**, with existing ignored categories unchanged.
- Exact netlist comparison: only U3 pin-function/feedback changes plus R11/R12/C10;
  all other original pin-to-net connections preserved.
- All 42 component values, order codes and footprint assignments match BOM.csv;
  footprint files resolve. Missing resistor MPN fields and semiconductor packaging
  drift were corrected in the schematic using the curated purchasing BOM.
- Schematic rendered and visually reviewed. Existing C6/D3 text interference cleaned up.
- Backups are in `interface-review-20260915/before-metadata` and `before-u3-eco`.
- A-P1 procurement tag/manifest is unchanged. A-P2-DRAFT is an engineering change,
  not a new purchasing release. Refresh quotations/workbooks after further changes
  and final approval of the build revision.

Manufacturer PDFs were read through web access where local downloads failed.
The old local fuse PDF is retained as historical evidence, not the current rating
source. No purchase, upload to a board house, commit or flight approval was made.
