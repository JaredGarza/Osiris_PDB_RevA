Superseded for U2/C17 by [implemented INA238 and capacitor-bank update](INA238_CAPACITOR_BANK_2026-10-15.md). Use PnP.xlsx and the updated one-sheet JLC workbook for purchasing. The prior U2/C17 shortages below describe the earlier selections.

# Osiris PDB five-board procurement — October 15, 2026

Two alternatives are provided: JLCPCB assembly, and local boss/PnP procurement. Do not purchase both as separate five-board builds unless ten boards are intended.

## Files

- JLCPCB_BOM_Stock_5_Boards.xlsx: first sheet is the per-PCB upload BOM; second sheet reviews JLC inventory for five assembled boards, including catalog loss estimates. Set assembled quantity to five in JLCPCB checkout.
- Boss_PnP_Procurement_5_Boards.xlsx: grouped purchasing quantities for five boards. Passives use max(100, 10 times fitted need); ICs and other parts use 20% extra rounded up. Supplier multiples round up and an optional larger-quantity override is available.
- BOM.csv and Pick_and_Place.csv match the latest PDB CAD. The placement file is unchanged because placement, footprint pads and wiring did not change.
- The 7.5 A MINI blade fuse insert is listed separately in the boss file; it is not a PCB placement.

## Current stock result

JLCPCB: 29 board BOM groups have sufficient reported assembly stock against the catalog-loss planning estimate. Five board groups have short stock and five have unconfirmed exact catalog matches. The complete order cannot be released as all-in-stock.

| References | Selected manufacturer/MPN | JLC stock | Next step |
|---|---|---:|---|
| C1 | TDK C2012C0G2A223J125AC | 0 | Confirm exact global sourcing/consignment and receipt before assembly. |
| C17 | Panasonic EEHZL1H331P | Unconfirmed | No purchasable exact part or fully matching single-part replacement verified; sourcing/engineering remains open. |
| D1,D4 | Bourns SMAJ24CA | 0 | Confirm exact global sourcing/consignment and receipt before assembly. |
| D5 | Bourns SMBJ18CA | Unconfirmed | Confirm exact global sourcing/consignment and receipt before assembly. |
| F1 | Keystone 3568 | 0 | Confirm exact global sourcing/consignment and receipt before assembly. |
| F2 | SCHURTER 3-140-177 | Unconfirmed | Confirm exact global sourcing/consignment and receipt before assembly. |
| R5 | Ohmite FC4L64R005FER | Unconfirmed | Confirm exact global sourcing/consignment and receipt before assembly. |
| R19 | Vishay CRCW25121K00FKEGHP | Unconfirmed | Confirm exact global sourcing/consignment and receipt before assembly. |
| U1 | Analog Devices LTC4368HMS-1#WTRPBF | 0 | Confirm exact global sourcing/consignment and receipt before assembly. |
| U2 | Texas Instruments INA228AIDGSR | 0 | No stock verified at JLC, DigiKey, Mouser or TI. Retained INA228; no available drop-in approved. |

Boss/local procurement: all rows have sufficient reported supplier stock for the policy quantities except U2 (zero) and C17 (unconfirmed). Prices combine observed references with older estimates; the subtotal excludes the unquoted C17 and all assembly/freight/tax/tariff/reel charges. Full reels are not assumed.

## Substitutions and footprint verification

All final MPNs match the schematic, PCB, CSV BOM and both workbooks. Byte comparison against the starting schematic/PCB, excluding only Manufacturer/MPN/Datasheet property values, confirms that footprint identifiers, copper, pads, hole sizes, pin numbering, nets, zones, outline and placement are unchanged. Fresh KiCad DRC: zero violations, zero unconnected items, zero schematic parity issues. ERC: zero violations.

| References | Final selected part | Compatibility evidence |
|---|---|---|
| C3,C5,C8,C10,C7 | CC0603KRX7R9BB104 | YAGEO 100 nF 50 V X7R +/-10%, 1.6 x 0.8 mm 0603. C3/C5/C8/C10 rise from 16 V to 50 V; C7 remains 50 V. Existing 0603 pads retained. |
| C4,C9 | CL31B106KBHNNNE | Samsung 10 uF 50 V X7R +/-10%, 3.2 x 1.6 mm 1206. Existing pads +/-1.475 mm, 1.15 x 1.8 mm. |
| C6 | CL21B106KAYQNNE | Samsung 10 uF 25 V X7R +/-10%, 2.0 x 1.25 mm 0805. Rating increases from 10 V; existing pads +/-0.95 mm, 1 x 1.45 mm. Prior effective-capacitance/stability verification requirement remains. |
| C11,C12,C13,C14,C15,C16 | B32529C0105J000 | Same TDK B32529C0105J electrical specification. 000 is untaped, 189 is reel. 7.3 x 4.5 x 9.5 mm max body, 5 mm pitch, 0.5 +/-0.05 mm leads; existing 0.75 mm holes and 7.7 x 5 mm courtyard. Manual insertion/lead trimming. |
| R1 | FRC0805F2373TS | 237 kOhm +/-1%, 125 mW, 150 V, 0805. Existing two-pad footprint. |
| R2 | FRC0805F1182TS | 11.8 kOhm +/-1%, 125 mW, 150 V, 0805. Existing two-pad footprint. |
| R11 | PTFR0805B1K58P9 | 1.58 kOhm +/-0.1% thin film, 130 mW, 150 V, 25 ppm/C, 0805. Improves divider tolerance/TCR and retains nominal resistance; -55 to 125 C part rating. Existing pads retained. |
| R13 | 0805W8F5492T5E | 54.9 kOhm +/-1%, 125 mW, 150 V, 0805. Existing two-pad footprint. |
| R14 | FRG0805J226TS | 22 MOhm +/-5%, 125 mW, 150 V, 0805. Existing two-pad footprint. |
| R19 | CRCW25121K00FKEGHP | Normalize ordering code to CRCW25121K00FKEGHP, same intended 1 kOhm +/-1%, 1.5 W pulse-rated CRCW-HP in 2512. |
| U1 | LTC4368HMS-1#WTRPBF | Automotive W order option of LTC4368HMS-1, retaining H grade -40 to 125 C, -1 threshold and 10-pin MSOP pinout. Direct supplier has ten listed; JLC has zero and requires sourcing/consignment. |

Nominal compatibility and CAD consistency were checked. DC-bias curves for replacement MLCCs, assembled regulator stability, startup/SOA, transients, temperature and system fault protection have not been newly qualified by this procurement work. Existing engineering limits remain documented in PDB/PROTECTION_FIX_STATUS.md.

## Pasted automatic matches corrected

- U3: use adjustable LT3010EMS8E#TRPBF, JLC C579990. Do not use fixed 5 V C579991.
- R11: use 1.58 kOhm PTFR0805B1K58P9, JLC C2692700. Do not use 1.5 kOhm C4310.
- C1: retain 22 nF, 100 V, C0G +/-5%; do not accept pasted X7R +/-10% C1729 as an equivalent gate-timing part.
- R19: retain specified pulse-rated 1.5 W +/-1% Vishay part; do not accept the pasted generic 1 W +/-5% part.
- U4: use Nexperia C477991, not the unreviewed TECH PUBLIC match C49230940. Nexperia GW is SOT353/SC70-5; the catalog calls it TSSOP-5.
- D1/D4: pasted C609818 is Slkor, while the design specifies Bourns. Exact Bourns catalog C3719750 currently has zero stock.
- D5: pasted C2938922 is RUILON, while prior clamp coordination uses Bourns curves. Retain Bourns pending a separate manufacturer-specific substitution review.

## Sources

- Supplied ODS procurement workbook, five-board quantities and spare-parts policy; no claim of recalling the separate email.
- Exact supplier links, stock check date and price basis are present beside each input in the boss workbook.
- Exact JLC stock endpoint, catalog part number, loss allowance, process and check date are present beside each input in the JLC stock review.
- [TDK B32529 dimensions and packaging codes](https://product.tdk.com/en/system/files/dam/doc/product/capacitor/film/mkt/data_sheet/20/20/db/fc_2009/b32520_529.pdf).
- [ADI LTC4368 ordering table and pinout](https://www.analog.com/media/en/technical-documentation/data-sheets/LTC4368.pdf).
- [ADI LT3010 adjustable versus fixed-5 V variants](https://www.analog.com/en/products/LT3010.html).
- [Nexperia 74AUP1G07 package and pinout](https://assets.nexperia.com/documents/data-sheet/74AUP1G07.pdf).

No order, payment, consignment shipment or supplier message was submitted.
