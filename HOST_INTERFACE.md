# PDB REV1.1 to Osiris Rev B

Verified from the current OsirisRevA schematic/netlist, October 8, 2026. Host is STM32H743IIK6 U10; use I2C1, PB8 (SCL) / PB9 (SDA), initially 100 kHz. The PDB INA228 address is **0x40 (7 bit)**. Osiris's onboard INA228 IC11 is a different device on I2C4, address 0x4F; do not apply this PDB's 5 mOhm calibration to IC11.

| PDB J2 | Cable connection | Osiris J28 |
|---|---|---|
| Pin 1: INA_ALERT, open-drain | **No connection; omit this conductor** | Pin 1 is +5V0_PROT; leave unused |
| Pin 2: SCL | Connect | Pin 2: FMU_I2C1_SCL |
| Pin 3: SDA | Connect | Pin 3: FMU_I2C1_SDA |
| Pin 4: GND | Connect | Pin 4: GND |

**A straight four-wire cable is incompatible.** It applies host 5 V to PDB ALERT. Use a three-conductor cable in the four-position keyed housings, with cavity 1 empty at both ends. Poll the PDB instead of using ALERT in this connection. Inspect cavity numbering against both board footprints and perform cable continuity checks before connection. No 5 V supply is carried in this data cable.

PDB R17/R18 remain DNP. Osiris I2C1 R74/R75 were changed in the current host schematic and PCB from 12 kOhm to **4.7 kOhm**, 0402, Yageo RC0402FR-074K7L. They connect to the host's switched +3V3 rail. No other host I2C bus resistors were changed. Host production outputs were not regenerated as part of the PDB package; use Osiris_Host_Pullup_Changes.csv when rebuilding its BOM. Check that no connected peripheral adds an excessive parallel pull-up.

For 4.7 kOhm and the historical 90 pF assumption, tr = 0.8473 R C = 358.4 ns. At 100 kHz, the 1000 ns rise-time criterion implies about 251 pF total capacitance, before resistor tolerance and design margin. At 400 kHz, the 300 ns criterion implies about 75 pF, so **do not switch this harness to 400 kHz based on the 90 pF estimate**. Measure SCL/SDA rise time, low voltage and ringing on the installed harness. Keep the ground conductor alongside the data conductors.

The PDB ALERT buffer is not used by this polling cable. Do not connect host power to it. Verify the host-off/PDB-on and PDB-off/host-on cases on the assembled system. The INA228 SCL/SDA absolute rating is independent of VS, unlike its ALERT rating; this alone does not qualify the entire powered-off bus.

Power cable: **PDB J4 pin 2 (+PDB_VOUT) -> Osiris J17 pin 1 (+VBATT_OUT); PDB J4 pin 1 GND -> Osiris J17 pin 2 GND**. This supplies protected, unregulated 4S battery voltage. Connector pin numbers differ; never connect by pin number alone.

Firmware source is provided in `source_snapshot/Firmware`. It is a transport-independent driver, not a flashed or integrated Osiris application. Configure the actual STM32 clock-dependent timing value through the existing firmware project and connect finite-timeout read/write callbacks to I2C1. No runnable firmware project was found in the local Hardware/Osiris repositories.
