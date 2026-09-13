# F1 and J1–J3 selection proposal

Working source: the user's current Osiris_PDB_RevA.kicad_sch. This proposal does not change the schematic or the protection thresholds. The older generated PCB and design specification are not requirements for this proposal.

## Operating assumption

Target a supported low-power Orin Nano profile, provisionally 7 W. NVIDIA documents 7 W profiles for standard Orin Nano configurations; available profiles depend on the module and flashed software. Inspect the installed nvpmodel configuration before selecting a mode ID. No Jetson software has been changed.

Software power management reduces module demand; the complete input budget must include Osiris electronics, attached peripherals, conversion losses, startup, and transient loads. Do not treat the software profile as a hard fuse-sizing limit.

[NVIDIA power management documentation](https://docs.nvidia.com/jetson/archives/r36.5/DeveloperGuide/SD/PlatformPowerAndPerformance/JetsonOrinNanoSeriesJetsonOrinNxSeriesAndJetsonAgxOrinSeries.html)

## Proposed parts

| Reference | Proposed part | KiCad footprint | Status |
|---|---|---|---|
| F1 | Littelfuse 0297005.WXNV, 5 A MINI blade fuse, in Keystone 3568 holder | Fuse:Fuseholder_Blade_Mini_Keystone_3568 | Prototype candidate only; final current rating requires load, temperature, inrush and fault-current checks |
| J1 battery input | AMASS XT60PW-M | Connector_AMASS:AMASS_XT60PW-M_1x02_P7.20mm_Horizontal | Candidate for PCB-mounted input; verify battery cable mating and board-edge clearance |
| J2 Osiris control | JST BM06B-GHS-TBT(LF)(SN), with GHR-06V-S cable housing and appropriate GH contacts | Connector_JST:JST_GH_BM06B-GHS-TBT_1x06-1MP_P1.25mm_Vertical | Candidate; custom cable pinout required |
| J3 Osiris power output | AMASS XT60PW-F | Connector_AMASS:AMASS_XT60PW-F_1x02_P7.20mm_Horizontal | Candidate; reconcile schematic pin numbering before assignment |

The fuse and holder are separate purchased parts and require separate BOM entries. The 3568 manufacturer specifies compatibility with Littelfuse 297-series MINI fuses and a 30 A holder rating. This rating does not set the protected circuit's allowable current. The replaceable holder also needs retention, access and vibration review for aircraft use.

[Littelfuse 297-series catalog](https://m.littelfuse.com/technical-resources/online-tools/~/media/files/littelfuse/technical%20resources/documents/product%20catalogs/eumea-sea_automotive-aftermarket_052008.pdf), [0297005.WXNV manufacturer identification](https://www.littelfuse.com/assetdocs/reach-svhc-declaration-0297005?assetguid=0ff51c38-af71-4687-bf05-0c3a2d32d226), [Keystone 3568](https://www.keyelco.com/product.cfm/product_id/306), [JST GH](https://www.jst-mfg.com/product/index.php?lang=2&series=105), [AMASS input drawing](https://www.tme.eu/Document/b13629717d44ae038681dba08d18c0b6/XT60PW-M.pdf), [AMASS output drawing](https://www.tme.eu/Document/1191bc2fa3aee3c446e5a895fd8f7983/XT60PW-F.pdf).

## Wiring findings that must guide implementation

- In the supplied OsirisRevA ZIP, OS_PowerInput.SchDoc places J16 (XT60PW-M) on VBATT_IN and J15 (XT60PW-F) on VBATT_OUT. Earlier references to J15 as the intended input should not be carried forward. Confirm the populated board and cable polarity against these records.
- The installed KiCad XT60PW-M and XT60PW-F footprints both mark pad 1 negative and pad 2 positive. Current PDB J1 agrees (1 GND, 2 VBAT_RAW). Current PDB J3 is reversed (1 PDB_VOUT, 2 GND). Directly assigning the standard J3 footprint would therefore map positive power to its negative-marked contact. Change the J3 symbol pin mapping or use an explicitly documented remapped project footprint, then verify end-to-end polarity.
- Current J2 is 1 GND, 2 SDA, 3 SCL, 4 INA_ALERT_N, 5 PDB_FAULT_N, 6 NC. Matching the JST GH family does not make this pinout compatible with an arbitrary Osiris GH socket. Identify the actual I2C and GPIO endpoints and document the cable. Osiris contains another INA228, so verify address uniqueness if sharing its bus.

## Thresholds and fuse qualification

Keep the present nominal 10.56 V UV, 18.68 V OV, and 10 A electronic overcurrent thresholds as requested. This preserves the user's targets; it is not a validation of those targets against the battery or all loads.

A 5 A fuse is a candidate below the 10 A electronic breaker setting, not an instantaneous 5 A limiter. Accept it only after normal input current and temperature derating, startup I²t, time-current curves, prospective battery short-circuit current and interrupt rating are checked. Check MOSFET safe operating area and wiring protection during faults. Do not increase the fuse solely to accommodate nuisance trips without finding their cause.

For scale only: 7 W at 5 V is 1.4 A for the module. At a hypothetical 90% conversion efficiency and 12 V battery input, that contribution is about 0.65 A at the PDB; other loads are additional. This is not a measured whole-board budget.
