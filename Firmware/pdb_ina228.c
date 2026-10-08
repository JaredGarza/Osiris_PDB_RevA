#include "pdb_ina228.h"
#include <math.h>
#define PDB_ADDRESS 0x40u
#define SHUNT_CAL 4096u
#define ADC_CONFIG 0xFB6Au /* continuous V/I/T, 1052 us each, 16 averages */
static bool read16(pdb_ina228 *d,uint8_t reg,uint16_t *v){
 uint8_t b[2];if(!d->read(d->context,PDB_ADDRESS,reg,b,2))return false;
 *v=(uint16_t)(((uint16_t)b[0]<<8)|b[1]);return true;
}
static bool write16(pdb_ina228 *d,uint8_t reg,uint16_t v){
 uint8_t b[2]={(uint8_t)(v>>8),(uint8_t)v};return d->write(d->context,PDB_ADDRESS,reg,b,2);
}
static bool read20(pdb_ina228 *d,uint8_t reg,bool sign,int32_t *v){
 uint8_t b[3];uint32_t raw;
 if(!d->read(d->context,PDB_ADDRESS,reg,b,3))return false;
 raw=((uint32_t)b[0]<<16)|((uint32_t)b[1]<<8)|b[2];raw>>=4;
 *v=(sign && (raw&0x80000u))?(int32_t)raw-1048576:(int32_t)raw;return true;
}
static pdb_status configuration(pdb_ina228 *d){
 uint16_t c,a,s;
 if(!read16(d,0,&c)||!read16(d,1,&a)||!read16(d,2,&s)){d->configured=false;return PDB_IO_ERROR;}
 if(c!=0||a!=ADC_CONFIG||s!=SHUNT_CAL){d->configured=false;return PDB_CONFIG_LOST;}
 return PDB_OK;
}
double pdb_ina228_current_lsb(const pdb_ina228 *d){
 return d && isfinite(d->shunt_ohms) && d->shunt_ohms>0 ? SHUNT_CAL/(13107200000.0*d->shunt_ohms):NAN;
}
pdb_status pdb_ina228_init(pdb_ina228 *d){
 uint16_t manufacturer,id;
 if(!d||!d->read||!d->write||!isfinite(d->shunt_ohms)||d->shunt_ohms<=0)return PDB_BAD_ARGUMENT;
 d->configured=false;
 if(!read16(d,0x3E,&manufacturer)||!read16(d,0x3F,&id))return PDB_IO_ERROR;
 if(manufacturer!=0x5449u||(id&0xFFF0u)!=0x2280u)return PDB_WRONG_DEVICE;
 /* Stop conversions while programming; never use ADCRANGE=1 on this board. */
 if(!write16(d,1,0)||!write16(d,0,0)||!write16(d,2,SHUNT_CAL)||!write16(d,1,ADC_CONFIG))return PDB_IO_ERROR;
 {pdb_status status=configuration(d);if(status!=PDB_OK)return status;}
 d->configured=true;return PDB_OK;
}
pdb_status pdb_ina228_sample(pdb_ina228 *d,pdb_sample *s){
 uint16_t flags;int32_t current,bus,shunt;pdb_status status;
 if(!s)return PDB_BAD_ARGUMENT;
 s->valid=false;s->current_a=NAN;s->bus_v=NAN;s->shunt_v=NAN;s->diagnostic=0;
 if(!d||!d->read||!d->configured)return PDB_CONFIG_LOST;
 if(!isfinite(d->shunt_ohms)||d->shunt_ohms<=0){d->configured=false;return PDB_BAD_ARGUMENT;}
 status=configuration(d);if(status!=PDB_OK)return status;
 if(!read16(d,0x0B,&flags))return PDB_IO_ERROR;
 s->diagnostic=flags;
 if(!(flags&1u)||(flags&0x200u))return PDB_SENSOR_FAULT; /* MEMSTAT / MATHOF */
 if(!(flags&2u))return PDB_NOT_READY;
 if(!read20(d,7,true,&current)||!read20(d,5,false,&bus)||!read20(d,4,true,&shunt))return PDB_IO_ERROR;
 /* Reject clipping rather than silently presenting it as a real current. */
 if(current==524287||current==-524288||shunt==524287||shunt==-524288||bus==1048575)return PDB_SENSOR_FAULT;
 status=configuration(d);if(status!=PDB_OK)return status;
 s->current_a=current*pdb_ina228_current_lsb(d);s->bus_v=bus*0.0001953125;s->shunt_v=shunt*0.0000003125;s->valid=true;return PDB_OK;
}
