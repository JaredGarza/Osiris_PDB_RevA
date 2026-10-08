# REV1.1 procurement substitutions

Checked October 8, 2026. Updated 14 fitted components across 11 MPN groups. Values, packages, copper routing and board size are unchanged. Resistors are 0805, 1%, 125 mW, 150 V; 10 ohm parts have 200 ppm/K TCR and the others 100 ppm/K. Capacitors are 0805, X7R, 50 V, 10%. Stock is a reported snapshot, not a guarantee of future availability or JLC assembly stock. Confirm exact parts at order time.

| References | Selected MPN | LCSC | Reported stock |
|---|---|---|---:|
| C2,C18 | CC0805KKX7R9BB105 | [C91185](https://www.lcsc.com/product-detail/C91185.html) | 767,960 |
| C19 | CC0805KRX7R9BB104 | [C49678](https://www.lcsc.com/product-detail/C49678.html) | 8,362,320 |
| R3 | 0805W8F2004T5E | [C26112](https://www.lcsc.com/product-detail/C26112.html) | 17,200 |
| R4 | 0805W8F2202T5E | [C17560](https://www.lcsc.com/product-detail/C17560.html) | 1,226,000 |
| R6 | 0805W8F6803T5E | [C17797](https://www.lcsc.com/product-detail/C17797.html) | 64,300 |
| R7 | 0805W8F2003T5E | [C17539](https://www.lcsc.com/product-detail/C17539.html) | 428,200 |
| R8,R9 | 0805W8F100JT5E | [C17415](https://www.lcsc.com/product-detail/C17415.html) | 4,712,400 |
| R10 | 0805W8F4701T5E | [C17673](https://www.lcsc.com/product-detail/C17673.html) | 1,678,600 |
| R12 | 0805W8F1001T5E | [C17513](https://www.lcsc.com/product-detail/C17513.html) | 24,259,800 |
| R15,R16 | 0805W8F1002T5E | [C17414](https://www.lcsc.com/product-detail/C17414.html) | 48,598,900 |
| R21 | 0805W8F1000T5E | [C17408](https://www.lcsc.com/product-detail/C17408.html) | 6,871,100 |

C17 remains Panasonic EEHZL1H331P: 330 µF, 50 V, 12 mΩ at 100 kHz and 5 A ripple at 125 °C. No verified single-part replacement was found meeting capacitance, voltage, ESR, ripple current and the G16 package. EEH-ZU1H221P is only 220 µF and is not an approved direct replacement. Two parallel parts would require a separate layout and transient validation.

Retained the linear-mode MOSFETs, protection ICs, INA228, Kelvin shunt, high-power resistors, fuses and film capacitors because a sourcing swap must preserve their specific electrical function. Existing KEMET 0603 decouplers already have deep reported stock; the investigated Samsung option had much less reported stock. Precision divider values were retained.

Fresh KiCad DRC: zero violations, zero unconnected items, zero schematic parity issues. ERC: zero violations. Calculation inputs and formulas are unchanged. These CAD checks do not establish hardware transient or thermal qualification.
