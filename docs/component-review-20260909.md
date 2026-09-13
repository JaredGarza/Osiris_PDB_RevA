# PDB component review — 9 September 2026

The saved Osiris_PDB_RevA schematic is the source of truth for this review. The older DESIGN-SPEC.md and previous BOM describe a different circuit and must not be used to size this circuit's fuse or connectors.

## Applied

- C4 already specified 10 uF, 50 V, X7R; C3 and C8 already specified 100 nF, 16 V, X7R. Preserved these specifications.
- Repaired the 2.54 mm gap between C8 pin 2 and its existing PDB_3V3 wire. ERC changed from one error and one warning to zero errors and zero warnings.
- Added the requested external I2C and alert/fault pull-up note beneath the Osiris connectors.
- Assigned all eight capacitor footprints and manufacturer part numbers, nine ordinary resistor footprints (0805), and five bare test-pad footprints (1.5 mm).
- Preserved R5 and its custom four-terminal footprint exactly.
- Exported BOM.csv from KiCad with reference, value, specification, footprint, manufacturer, MPN, selection status, and datasheet fields.
- Verified every assigned footprint resolves to an installed or project-local footprint file. Visually inspected the rendered schematic.
- Saved the previous schematic and BOM in component-review-backup-20260909.

## Capacitor selections

| References | MPN | Package | Nominal specification | Manufacturer source |
|---|---|---|---|---|
| C1 | C2012C0G2A562J125AA | 0805 | 5.6 nF, 100 V, C0G, 5% | [TDK](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C2012C0G2A562J125AA) |
| C2 | C2012X7R1H105K125AB | 0805 | 1 uF, 50 V, X7R, 10% | [TDK](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C2012X7R1H105K125AB) |
| C3, C5, C8 | C0603C104K4RACTU | 0603 | 100 nF, 16 V, X7R, 10% | [KEMET](https://search.kemet.com/component-documentation/download/specsheet/C0603C104K4RACTU) |
| C4 | C3216X7R1H106K160AC | 1206 | 10 uF, 50 V, X7R, 10% | [TDK](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C3216X7R1H106K160AC) |
| C6 | C2012X7R1A106K125AC | 0805 | 10 uF, 10 V, X7R, 10% | [TDK](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C2012X7R1A106K125AC) |
| C7 | C1608X7R1H104K080AA | 0603 | 100 nF, 50 V, X7R, 10% | [TDK](https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C1608X7R1H104K080AA) |

These selections settle nominal specifications and package sizes. Effective capacitance under DC bias, tolerances, temperature, regulator stability and procurement availability still require validation. TDK's C4 page did not provide inventory information during this review.

## Still open before layout release

1. F1, J1, J2 and J3 have no assigned footprint. Current budget, peak/inrush duration, battery range, mating parts, polarity and mechanical orientation must establish these selections. J1's value only says XT60; it does not identify PCB mounting versus a wired pigtail, gender or orientation.
2. Ordinary resistor MPNs and power/tolerance ratings remain open. Existing 1% fields are preserved. The 0805 assignments are package choices, not power qualification.
3. Existing semiconductor and shunt part identifiers remain in their Value fields; their dedicated MPN fields have not been independently completed. U4's 74AUP1G07GW value and TI sn74aup1g07 datasheet link need manufacturer/order-code reconciliation.
4. Confirm actual Osiris-side pull-ups and cable pinout, including whether any pull-ups already exist and the intended grounds. The schematic note is an interface requirement, not verification of the Osiris board.
5. Validate shunt dissipation/current limits, MOSFET heating and protection thresholds, fuse time-current behavior, connector/wire ratings, and TPS7A1633 thermal margin against the real loads.
6. This change does not update or validate the existing PCB layout. ERC does not establish power or layout readiness.

Reports: erc-before-component-review.rpt and erc-after-component-review.rpt. Visual check: review-render/after.png.
