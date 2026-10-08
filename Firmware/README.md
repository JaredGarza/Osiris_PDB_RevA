# PDB INA228 driver

This driver targets the PDB INA228 at 0x40, using its 5 mOhm avionics-only shunt. It does not measure ESC or whole-pack current. It is suitable for integration into Osiris STM32H743 I2C1; host wiring and resistors are documented in the package's HOST_INTERFACE.md. It is not an entire flight-controller firmware image, and has not been flashed or tested on physical hardware.

Supply callbacks with a finite timeout. At an STM32 HAL boundary, shift the 7-bit address left once. Register data is MSB first. Use 100 kHz initially; do not automatically fall back to a different bus or INA228 address.

Initialize `pdb_ina228` with the context, callbacks and measured shunt resistance, or nominal 0.005 Ohm for initial bring-up. Call `pdb_ina228_init` after the PDB local rail is present. It validates manufacturer/device IDs, selects ADCRANGE=0, programs SHUNT_CAL=4096, selects 16 averages and 1052 us V/I/temperature conversion times, and checks readback. Nominal CURRENT_LSB is 62.5 uA/count, with a signed positive span one count below 32.768 A. The analog high range is also 32.768 A nominal; the low 8.192 A range is inappropriate for the possible 12.12 A breaker corner. Readback after power loss is mandatory.

Poll roughly every 100 ms. `pdb_ina228_sample` returns a status and a `valid` flag. Never use a failed/not-ready sample as a zero-current reading. Invalid values are NaN. The driver detects I/O failures, changed/reset configuration, memory faults, arithmetic overflow and clipping. It performs signed 20-bit conversion and uses the integer calibration to calculate the actual LSB. Check the sample age in the application, and publish communication faults separately from electrical current. Power/energy/charge accumulation and an interrupt-based alert path are not implemented. Sequential reads are not an atomic multi-register snapshot.

After a configuration-loss/I/O failure, mark telemetry unavailable and retry initialization with a bounded application retry policy. A firmware reboot alone does not constitute a battery disconnect. This driver has no authority over motor throttles or power switches and cannot make the 60/100 A target compatible with the XT60 connectors. Automatic disarming or propulsion interruption requires integration with the existing flight application's safety behavior.

The supplied C unit test was compiled with MSVC `/W4 /WX /std:c11`; it checks positive/negative readings, clipping, sensor fault flags, wrong device, configuration loss, I/O failure and invalid shunt inputs. Physical bring-up and integration remain required.

Source: Texas Instruments [INA228 datasheet](https://www.ti.com/lit/ds/symlink/ina228.pdf), register map and calibration equations. Nominal board identity and connections come from the current PDB netlist.
