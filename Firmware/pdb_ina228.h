#ifndef PDB_INA228_H
#define PDB_INA228_H
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
/* Callbacks use a 7-bit address (0x40), MSB-first data and a finite timeout.
 * STM32 HAL adapters must shift the address left once at the HAL boundary.
 * Host: STM32H743 I2C1, PB8=SCL / PB9=SDA, 100 kHz. */
typedef bool (*pdb_read_fn)(void *,uint8_t,uint8_t,uint8_t *,size_t);
typedef bool (*pdb_write_fn)(void *,uint8_t,uint8_t,const uint8_t *,size_t);
typedef struct { void *context; pdb_read_fn read; pdb_write_fn write; double shunt_ohms; bool configured; } pdb_ina228;
typedef enum { PDB_OK, PDB_IO_ERROR, PDB_WRONG_DEVICE, PDB_CONFIG_LOST,
               PDB_NOT_READY, PDB_SENSOR_FAULT, PDB_BAD_ARGUMENT } pdb_status;
typedef struct { bool valid; double current_a,bus_v,shunt_v; uint16_t diagnostic; } pdb_sample;
pdb_status pdb_ina228_init(pdb_ina228 *device);
pdb_status pdb_ina228_sample(pdb_ina228 *device,pdb_sample *sample);
/* Register-domain current resolution after integer calibration, not an
 * assumed nominal CURRENT_LSB. Range 0; CAL=4096; nominal 5 mOhm => 62.5 uA. */
double pdb_ina228_current_lsb(const pdb_ina228 *device);
#endif
