#ifndef PDB_INA238_H
#define PDB_INA238_H
#include "pdb_monitor.h"
/* Callbacks use a 7-bit address (0x40), MSB-first data and a finite timeout.
 * STM32 HAL adapters must shift the address left once at the HAL boundary.
 * Host: STM32H743 I2C1, PB8=SCL / PB9=SDA, 100 kHz. */
typedef struct { void *context; pdb_read_fn read; pdb_write_fn write; double shunt_ohms; bool configured; } pdb_ina238;
pdb_status pdb_ina238_init(pdb_ina238 *device);
pdb_status pdb_ina238_sample(pdb_ina238 *device,pdb_sample *sample);
/* Register-domain current resolution after integer calibration, not an
 * assumed nominal CURRENT_LSB. Range 0; CAL=4096; nominal 5 mOhm => 1 mA. */
double pdb_ina238_current_lsb(const pdb_ina238 *device);
#endif
