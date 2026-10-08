# Osiris PDB REV1.1 protection corrections

October 8, 2026. Revision stays 1.1; outline and copper build stay 82.5 x 65 mm, four layers, 1 oz outer / 0.5 oz inner. These are engineering corrections, not a full electrical qualification or flight release.

| Item | Implemented correction | Remaining evidence |
|---|---|---|
| TVS / capacitor voltage coordination | D5 SMBJ24CA -> SMBJ18CA. C17 470 uF / 35 V EEHZS1V471P -> 330 uF / 50 V EEHZL1H331P. Same SMB/G16 footprints and pads. | Installed ESC/harness overshoot, regeneration, TVS pulse energy, temperature and capacitor ripple/bulk requirement. |
| Startup / MOSFET SOA | Corrected component identification and added startup, inrush and single-FET stress equations to workbook. Existing Q1/Q2 are linear-mode-rated ISC015N06NM5LF2, not the ordinary ISC015N06NM5. | Actual host startup waveform, connected peripheral capacitance, hot-case SOA trajectory and repeated-retry thermal test. No SOA pass claimed. |
| Retry calculation | C3 is 100 nF on U1 RETRY: nominal delay 550 ms. C1 is 22 nF in series with R4=22 kOhm in the gate-ramp branch. | C3 tolerance/DC bias and IC timing variation; fault/recovery scope test. |
| Host bus / cable | Found 5 V-to-ALERT cable conflict; specified three-conductor J2-to-J28 harness. Changed host R74/R75 to 4.7 kOhm. PDB pull-ups remain DNP. | Physical cable checks, rise-time and independent power-state test. |
| Firmware | Added tested, portable INA228 driver: correct address/range/calibration/sign/diagnostics/configuration-loss handling. | Integrate into the actual STM32 firmware project; compile for target, flash and compare against calibrated instruments. No application firmware was found locally. |
| Pack fault interruption | Verified F2's actual voltage-specific interruption figures and recovered 4S/AERO SELFIE 45 A 4-in-one context from earlier discussion. Added a concrete external-fuse proposal below. | Pack/harness minimum resistance and inductance, guaranteed total clearing data, physical protective-device installation and current envelope. Not closed. |

## Transient component correction

At 16.8 V full-charge input, SMBJ18CA has 18 V standoff. Bourns specifies 29.2 V maximum clamp at 20.6 A (10/1000 us) and 38.0 V at 103 A (8/20 us), at 25 C. These are 20.8 V and 12.0 V below the new 50 V capacitor rating at those stated pulse conditions. They are not maximum system voltages for arbitrary pulse currents or temperature. C17's nominal energy at 16.8 V is 0.04657 J. The new ZL G16 part is 330 uF +/-20%, 12 mOhm ESR at 100 kHz/20 C, 5 Arms at 100 kHz/125 C. The reduced capacitance must not replace the ESC manufacturer's required capacitor at the ESC terminals. Supply is explicitly 4S; this TVS selection is not for 6S use.

Sources: [Bourns SMBJ](https://www.bourns.com/docs/product-datasheets/smbj.pdf), [Panasonic ZL](https://industrial.panasonic.com/cdbs/www-data/pdf/RDD0000/ast-ind-303928.pdf). D5's old sourcing record and C17's old price/stock no longer apply; the procurement workbook marks both replacements unquoted. Its total is a quoted-items subtotal until these are priced.

## Startup calculation and disposition

The actual gate network follows the LTC4368 application circuit: GATE directly drives Q1/Q2, with R4=22 kOhm and C1=22 nF to ground. C2=1 uF is on the output/sense node; it is not the gate-ramp capacitor. C3=100 nF is the retry capacitor.

Use dV/dt = Igate/Cgate, Icapacitive = Cload Igate/Cgate, and tcharge = Cgate Vin/Igate as first-order screening equations. The controller's 12 V test condition gives 20/35/60 uA gate pull-up magnitudes. C1 is +/-5%. At 16.8 V, nominal ramp is 10.56 ms; the slow screening corner is 19.404 ms. These ignore intrinsic gate charge and load behavior, and are not guaranteed timing across the full operating range.

The current Osiris netlist has 1 uF on VBATT_OUT and 49.2 uF nominal on VIN (six 4.7 uF plus 1 uF plus two 10 uF). The main-board LM73100 intervenes, and converter output capacitance and external peripherals are not directly equivalent to this sum. The workbook uses a conservative **110 uF screening assumption for known PDB/host input capacitance**, not a measured upper bound for the installed system. Fast-corner inrush is 0.316 A. Adding the 5 A constant-current example gives 5.316 A, below the 7.921 A breaker lower corner, but a converter can draw constant power and behave differently during startup.

A rectangular mixed-corner single-FET energy screen is about 1.733 J. Compare the actual VDS(t), ID(t) and starting case temperature against Infineon's SOA curves at 25 C and 125 C, including repeated retries. Do not divide stress equally between back-to-back FETs or equate avalanche energy with startup SOA. The high-drain-voltage FET can take almost all the linear stress. No startup component change is justified solely by the assumed 110 uF number; measure input/output/gate/shunt waveforms with Osiris and its intended peripherals before selecting a different C1 or retry policy.

Sources: [LTC4368 Rev. C](https://www.analog.com/media/en/technical-documentation/data-sheets/ltc4368.pdf), [ISC015N06NM5LF2](https://www.infineon.com/assets/row/public/documents/24/49/infineon-isc015n06nm5lf2-datasheet-en.pdf).

## Pack protection proposal — not installed or qualified

The earlier discussions identify the AERO SELFIE 45 A four-in-one ESC and explicitly used nominal motor/load examples; they do not provide a measured pack ESR or specific battery capacity/C rating. A four-channel ESC's 45 A rating is not its combined battery-input current. The 60 A continuous / 100 A for 30 s target remains incompatible with the selected 45 A XT60PW-F common input. The connector's momentary 60 A duration is unspecified. Software telemetry on J4 cannot measure or enforce ESC current on J3.

F2 remains SCHURTER 3-140-177, 100 A. Published breaking capacity is 600 A at 50 VDC, 1000 A at 32 VDC, 1300 A at 24 VDC, 2000 A at 16 VDC. Full 4S is **16.8 V**, so do not automatically use the 16 V rating or interpolate a rating. The datasheet's time-current tests use 22 mm wide, 210 um copper, unlike this PCB. Its 3200 A²s figure is typical melting I²t at 10x current, not a guaranteed total-clearing rating for the installed battery circuit. It is not protection for sustained overload of a 45 A connector.

For a deliberately lower-current bench/prototype harness, a concrete source-side candidate is **Littelfuse JLLN030.T, 30 A Class T**, with a matching enclosed LFT30-series holder and verified wire/terminal ampacity, installed close to the pack positive terminal **before J1**. Littelfuse publishes 160 VDC / 50 kA DC interruption for 1–30 A JLLN. This is a proposed external system component; it is not in the PCB BOM and is not installed by a PCB factory. It changes the allowable operating envelope and cannot support the previous 60/100 A goal. Check the exact holder, curve, temperature, expected motor current/inrush, harness withstand and total clearing let-through before adoption. A 30 A fuse is not an electronic 30 A limiter.

Required measured inputs: maximum pack voltage; minimum pack+lead+contact resistance over temperature and state of charge; loop inductance; wire gauge/length and insulation limits; fuse/holder temperature; maximum actual motor/prop current; clearing-time and total-I²t envelopes. Isc = V/R is only a DC screening model, not an inductive battery-fault test. Do not short a pack to measure it. Until coordinated, use a current-limited bench supply for bring-up and leave propulsion disconnected.

Sources: [SCHURTER UHS](https://www.schurter.com/en/datasheet/typ_UHS.pdf), [Littelfuse JLLN](https://www.littelfuse.com/assetdocs/jlln-datasheet?assetguid=3a7bc9bf-d932-4401-bdc7-b39f302195cf).
