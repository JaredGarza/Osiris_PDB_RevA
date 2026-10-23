# Running procurement replacement tally

Last verified: 2026-10-23 15:58 CDT.

## Scope and current tally

**20 sourcing-substitution groups / 29 fitted reference positions per PCB** differ from the October 23 starting CAD BOM. These are procurement recommendations, not changes already installed on hardware. The schematic, PCB, footprint libraries, firmware and already-submitted manufacturing package have not been changed by this procurement review.

The latest school purchasing workbook is [Osiris_PDB_Procurement_Verified_2026-10-23.xlsx](Osiris_PDB_Procurement_Verified_2026-10-23.xlsx). It covers 10 boards with the supplied spare/quantity policy. It supplements the existing five-board manufacturing documents; it does not instruct the manufacturer to change an order already placed.

The supplier restriction supplied by the user is **no China-based sellers**. Current school purchase sources are DigiKey, Mouser and Newark; country of manufacture is not excluded by that instruction. This records the user's purchasing rule, not a legal or school-policy certification.

## Active replacement register

Each row is one MPN group. The position count is the number of fitted references on one board, not the purchasing quantity. Keep this table current when a sourcing choice changes; add dated decisions below instead of replacing the history.

| References | Positions / PCB | Starting CAD manufacturer / MPN | Purchasing manufacturer / MPN | Differences and compatibility | Status and source |
|---|---:|---|---|---|---|
| C4,C9 | 2 | Samsung Electro-Mechanics `CL31B106KBHNNNE` | TDK `C3216X5R1H106K160AB` | 10 uF / 50 V / 10% / 1206 retained; X7R to X5R, upper temperature 125 C to 85 C. Nominal thickness 1.6 mm. DC-bias/ripple behavior requires review. | CONDITIONAL: temperature, DC bias and ripple verification pending; Chosen during October 23 procurement review. [Product](https://www.mouser.com/en/ProductDetail/TDK/C3216X5R1H106K160AB?qs=NRhsANhppD%252BLHMbxvQzsEQ%3D%3D) |
| C6 | 1 | Samsung Electro-Mechanics `CL21B106KAYQNNE` | TDK `C2012X5R1E106K085AC` | 10 uF / 25 V / 10% / 0805 retained; X7R to X5R, upper temperature 125 C to 85 C; nominal thickness 1.25 mm to 0.85 mm. LT3010 requires effective output C >=1 uF, ESR <=3 ohms. | CONDITIONAL: temperature, effective C and LDO stability pending; Chosen during October 23 procurement review. [Product](https://www.mouser.com/en/ProductDetail/TDK/C2012X5R1E106K085AC?qs=6JAMGB%252BEdkxKBx%252Bl%252BExtPw%3D%3D) |
| C11-C16 | 6 | TDK `B32529C0105J000` | TDK `B32529C0105K000` | 1 uF / 63 V PET, same 7.3 x 4.5 x 9.5 mm body and 5 mm pitch; tolerance relaxes 5% to 10%. Six-part bank nominal 6 uF, tolerance-only range 5.4-6.6 uF. | Recommended sourcing substitution; hardware unqualified; Chosen during October 23 procurement review. [Product](https://www.digikey.com/en/products/detail/tdk/B32529C0105K000/1089750) |
| D1,D4 | 2 | RUILON `SMAJ24CA` | Bourns `SMAJ24CA` | RUILON to Bourns; same SMA / DO-214AC and bidirectional 24 V nominal TVS class; 26.7-29.5 V breakdown, 38.9 V clamp at 10.3 A, 400 W 10/1000 us. Actual surge environment unqualified. | Recommended sourcing substitution; hardware unqualified; Chosen during October 23 procurement review. [Product](https://www.digikey.com/en/products/detail/bourns-inc/SMAJ24CA/2254533) |
| R1 | 1 | FOJAN `FRC0805F2373TS` | YAGEO `RC0805FR-07237KL` | 237 kΩ 0805 resistor; same 0805 pads and nominal resistance. 125 mW, 150 V. 1% tolerance retained. | Nominal/specification comparison checked; Chosen during October 23 procurement review. [Product](https://www.digikey.com/en/products/detail/yageo/RC0805FR-07237KL/727754) |
| R2 | 1 | FOJAN `FRC0805F1182TS` | YAGEO `RC0805FR-0711K8L` | 11.8 kΩ 0805 resistor; same 0805 pads and nominal resistance. 125 mW, 150 V. 1% tolerance retained. | Nominal/specification comparison checked; Chosen during October 23 procurement review. [Product](https://www.digikey.com/en/products/detail/yageo/RC0805FR-0711K8L/727558) |
| R3 | 1 | UNI-ROYAL `0805W8F2004T5E` | YAGEO `RC0805FR-072ML` | 2 MΩ 0805 resistor; same 0805 pads and nominal resistance. 125 mW, 150 V. 1% tolerance retained. | Nominal/specification comparison checked; Chosen during October 23 procurement review. [Product](https://www.digikey.com/en/products/detail/yageo/RC0805FR-072ML/727665) |
| R4 | 1 | UNI-ROYAL `0805W8F2202T5E` | YAGEO `RC0805FR-0722KL` | 22 kΩ 0805 resistor; same 0805 pads and nominal resistance. 125 mW, 150 V. 1% tolerance retained. | Nominal/specification comparison checked; Chosen during October 23 procurement review. [Product](https://www.digikey.com/en/products/detail/yageo/RC0805FR-0722KL/727736) |
| R6 | 1 | UNI-ROYAL `0805W8F6803T5E` | YAGEO `RC0805FR-07680KL` | 680 kΩ 0805 resistor; same 0805 pads and nominal resistance. 125 mW, 150 V. 1% tolerance retained. | Nominal/specification comparison checked; Chosen during October 23 procurement review. [Product](https://www.digikey.com/en/products/detail/yageo/RC0805FR-07680KL/731049) |
| R7 | 1 | UNI-ROYAL `0805W8F2003T5E` | YAGEO `AC0805FR-07200KL` | 200 kΩ 0805 resistor; same 0805 pads and nominal resistance. 125 mW, 150 V. 1% tolerance retained. | Nominal/specification comparison checked; Already present in user-supplied purchasing workbook. [Product](https://www.mouser.com/en/ProductDetail/YAGEO/AC0805FR-07200KL?qs=yhV1fb9g/Kbw5hOmSj8rUw%3D%3D) |
| R8,R9 | 2 | UNI-ROYAL `0805W8F100JT5E` | YAGEO `RC0805FR-0710RL` | 10 Ω 0805 resistor; same 0805 pads and nominal resistance. 125 mW, 150 V. 1% tolerance retained. | Nominal/specification comparison checked; Chosen during October 23 procurement review. [Product](https://www.digikey.com/en/products/detail/yageo/RC0805FR-0710RL/727534) |
| R10 | 1 | UNI-ROYAL `0805W8F4701T5E` | YAGEO `RC0805FR-074K7L` | 4.7 kΩ 0805 resistor; same 0805 pads and nominal resistance. 125 mW, 150 V. 1% tolerance retained. | Nominal/specification comparison checked; Chosen during October 23 procurement review. [Product](https://www.digikey.com/en/products/detail/yageo/RC0805FR-074K7L/727929) |
| R11 | 1 | RESI `PTFR0805B1K58P9` | YAGEO `RT0805BRD071K58L` | 1.58 kΩ 0.1% precision resistor; same 0805 pads and nominal resistance. 125 mW, 150 V. 0.1%, 25 ppm/C; 125 mW replaces 130 mW. | Nominal/specification comparison checked; Already present in user-supplied purchasing workbook. [Product](https://www.digikey.com/en/products/detail/yageo/RT0805BRD071K58L/1075685) |
| R12 | 1 | UNI-ROYAL `0805W8F1001T5E` | YAGEO `RC0805FR-071KL` | 1 kΩ 0805 resistor; same 0805 pads and nominal resistance. 125 mW, 150 V. 1% tolerance retained. | Nominal/specification comparison checked; Chosen during October 23 procurement review. [Product](https://www.digikey.com/en/products/detail/yageo/RC0805FR-071KL/727444) |
| R13 | 1 | UNI-ROYAL `0805W8F5492T5E` | YAGEO `RC0805FR-0754K9L` | 54.9 kΩ 0805 resistor; same 0805 pads and nominal resistance. 125 mW, 150 V. 1% tolerance retained. | Nominal/specification comparison checked; Chosen during October 23 procurement review. [Product](https://www.digikey.com/en/products/detail/yageo/RC0805FR-0754K9L/728029) |
| R14 | 1 | FOJAN `FRG0805J226TS` | YAGEO `RC0805JR-0722ML` | 22 MΩ 0805 resistor; same 0805 pads and nominal resistance. 125 mW, 150 V. 5% tolerance retained. | Nominal/specification comparison checked; Chosen during October 23 procurement review. [Product](https://www.digikey.com/en/products/detail/yageo/RC0805JR-0722ML/5919060) |
| R15,R16 | 2 | UNI-ROYAL `0805W8F1002T5E` | YAGEO `RC0805FR-0710KL` | 10 kΩ 0805 resistor; same 0805 pads and nominal resistance. 125 mW, 150 V. 1% tolerance retained. | Nominal/specification comparison checked; Chosen during October 23 procurement review. [Product](https://www.digikey.com/en/products/detail/yageo/RC0805FR-0710KL/727535) |
| R21 | 1 | UNI-ROYAL `0805W8F1000T5E` | YAGEO `AC0805FR-07100RL` | 100 Ω 0805 resistor; same 0805 pads and nominal resistance. 125 mW, 150 V. 1% tolerance retained. | Nominal/specification comparison checked; Already present in user-supplied purchasing workbook. [Product](https://www.mouser.com/en/ProductDetail/YAGEO/AC0805FR-07100RL?qs=yhV1fb9g/KZPmqCrZLI1lw%3D%3D) |
| U1 | 1 | Analog Devices `LTC4368HMS-1#WTRPBF` | Analog Devices `LTC4368HMS-1#PBF` | Same H-grade LTC4368-1 / MSOP-10 nominal function and pinout. W automotive ordering option replaced by non-W; qualification/traceability is not equivalent by assumption. | Pre-existing sheet choice; nominal match only; Already present in user-supplied purchasing workbook. [Product](https://www.digikey.com/en/products/detail/analog-devices-inc/LTC4368HMS-1-PBF/6820033) |
| U2 | 1 | Texas Instruments `INA238AIDGSR` | Texas Instruments `INA238AQDGSRQ1` | Same INA238 architecture / DGS VSSOP-10 pinout. Q1 device ID 0x2381 is accepted by existing driver mask; same address/calibration scheme. Physical board bring-up pending. | Recommended sourcing substitution; hardware unqualified; Chosen during October 23 procurement review. [Product](https://www.mouser.com/en/ProductDetail/Texas-Instruments/INA238AQDGSRQ1?qs=QNEnbhJQKvZaH3/ajejFPA%3D%3D) |

## Corrections and purchasing arrangements outside the tally

- **C17/C20:** the supplied spreadsheet's `EEH-ZS1H221V` was corrected to `EEH-ZS1H221P`, matching the existing CAD's `EEHZS1H221P`. This is a spreadsheet correction, not a new board substitution. Do not buy the V land-pattern variant for these existing pads.
- **F1:** purchase the Keystone `3568` holder and the separate Littelfuse `029707.5WXNV` 7.5 A insert. Two purchasing lines represent one fuse location, not two PCB placements. Normalizing `3568.0` to `3568` is not a component change.
- **J2:** exact `BM04B-GHS-TBT(LF)(SN)` retained; sourced from Newark `73M9202`, UK inventory with advertised US delivery 4-6 business days. Supplier change only. Do not substitute a side-entry header. Retail metadata saying four rows is inconsistent with the exact MPN/datasheet: this is one row of four contacts.
- **J1/J3/J4:** exact `XT60PW-F` retained. User will supply existing connectors or handle additional sourcing separately. School order quantity is 0 and connector costs are excluded. This does not mean no connectors are needed: three are fitted per PCB; previous purchasing plan allowed 42 including spares. On-hand quantity and exact PCB variant still need counting/confirmation by the user.
- **R17/R18:** DNP in the starting schematic; excluded from purchasing. H1-H4 mounting holes and TP1-TP7 bare test pads require no electronic parts.
- **C2/C18:** exact Yageo `CC0805KKX7R9BB105` retained; US Mouser quote resolved. No component change.

## Final spreadsheet verification

- All **39 school purchase rows** reopened in the user's browser on October 23: correct product MPNs, sufficient reported stock, valid applicable quantity-price breaks. No price differences found in this final check. One additional row is user-supplied XT60s.
- All **57 fitted CAD reference positions** accounted for once, including user-supplied connectors. Separate fuse insert accounted for as an accessory. No R17/R18 DNP purchases added.
- Per-board quantities retained. C4/C9 order restored to 28, C6 to 14 because Mouser permits single-piece multiples. User-handled XT60 school purchase quantity is zero.
- Parts subtotal **USD 735.0196**, displayed as **$735.02**. It includes both conditional capacitor choices and excludes XT60 purchases, assembly, shipping, tax and extra tariffs. Installed purchased-component cost **USD 49.8553 per PCB**, excluding the user-supplied connectors. This is not the total order cost divided by ten; spares and bulk purchasing explain the difference.
- Supplier hyperlinks, native table filters, cached formula totals and saved XLSX package checked. The comparison column now records R7, R11, R21 and U1 as well as the newly chosen changes.
- **Not an unconditional assembly release:** C4/C9 and C6 still need component-temperature/DC-bias checks, and C6 regulator startup/stability confirmation. X5R operating limit is 85 C at the capacitor, including self-heating. Procurement verification cannot establish unmeasured operating temperature or hardware qualification.

## Dated decision history

| Date | Decision |
|---|---|
| 2026-10-23 | Original redesign request canceled. Already ordered board/manufacturing files retained. Scope changed to purchasing links and sourcing substitutions. |
| 2026-10-23 | Replace hard-to-source UNI-ROYAL/FOJAN resistor ordering codes with common Yageo alternatives while preserving nominal resistance and existing pads. |
| 2026-10-23 | Select TDK 10% film variant, TI INA238-Q1 and Bourns TVS sourcing routes. Correct Panasonic P versus V purchasing mismatch. |
| 2026-10-23 | Broader supplier search found stock through a China-based seller; user subsequently prohibited China-based sellers. Those sources and links were removed from the final school workbook. |
| 2026-10-23 | Select stocked TDK X5R capacitor candidates from Mouser, explicitly conditional on 85 C thermal limit and bias/stability checks. Earlier Murata/AVX leads are not additional active purchases. |
| 2026-10-23 | Exact JST header moved to Newark; XT60 sourcing delegated by the user to their own stock/separate purchasing and removed from school totals. |
| 2026-10-23 | Final browser audit: 39/39 school purchase rows matched MPN/stock/price. Added the four previously unrecorded inherited substitutions to this running tally and the workbook. |

## Primary technical references

- [TDK C4/C9 characterization sheet](https://product.tdk.com/system/files/dam/doc/product/capacitor/ceramic/mlcc/charasheet/c3216x5r1h106k160ab.pdf)
- [TDK C6 part-specific data and reference curves](https://www.farnell.com/datasheets/2370672.pdf)
- [TI INA238-Q1 datasheet](https://www.ti.com/lit/ds/symlink/ina238-q1.pdf)
- [ADI LTC4368 datasheet and ordering options](https://www.analog.com/media/en/technical-documentation/data-sheets/LTC4368.pdf)
- [Existing procurement/specification review](PROCUREMENT_REVIEW_2026-10-15.md) (historical five-board route; active school substitutions are listed above)

Future updates should record date, references, original and selected MPN/manufacturer, supplier link, quantity, material rating/package differences and the remaining qualification status. Increment the active tally only when an additional CAD reference group changes; supplier-only changes, packaging normalization and superseded candidates do not add to the active count.
