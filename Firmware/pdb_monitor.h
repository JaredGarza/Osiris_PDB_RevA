#ifndef PDB_MONITOR_H
#define PDB_MONITOR_H
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
/* Transport callbacks use 7-bit addresses, MSB-first data and finite timeouts. */
typedef bool (*pdb_read_fn)(void *,uint8_t,uint8_t,uint8_t *,size_t);
typedef bool (*pdb_write_fn)(void *,uint8_t,uint8_t,const uint8_t *,size_t);
typedef enum { PDB_OK, PDB_IO_ERROR, PDB_WRONG_DEVICE, PDB_CONFIG_LOST,
               PDB_NOT_READY, PDB_SENSOR_FAULT, PDB_BAD_ARGUMENT } pdb_status;
typedef struct { bool valid; double current_a,bus_v,shunt_v; uint16_t diagnostic; } pdb_sample;
#endif
