#ifndef PDB_INA228_H
#define PDB_INA228_H
#include "pdb_monitor.h"
/* Callbacks use a 7-bit address (0x40), MSB-first data and a finite timeout.
 * STM32 HAL adapters must shift the address left once at the HAL boundary.
 * Host: STM32H743 I2C1, PB8=SCL / PB9=SDA, 100 kHz. */
typedef struct { void *context; pdb_read_fn read; pdb_write_fn write; double shunt_ohms; bool configured; } pdb_ina228;
pdb_status pdb_ina228_init(pdb_ina228 *device);
pdb_status pdb_ina228_sample(pdb_ina228 *device,pdb_sample *sample);
/* Register-domain current resolution after integer calibration, not an
 * assumed nominal CURRENT_LSB. Range 0; CAL=4096; nominal 5 mOhm => 62.5 uA. */
double pdb_ina228_current_lsb(const pdb_ina228 *device);
#endif
