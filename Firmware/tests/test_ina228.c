#include "../pdb_ina228.h"
#include <assert.h>
#include <math.h>
#include <stdio.h>
#include <string.h>
static unsigned char regs[64][3];static bool fail;
static bool rd(void *p,uint8_t a,uint8_t r,uint8_t *b,size_t n){(void)p;assert(a==0x40);if(fail)return false;memcpy(b,regs[r],n);return true;}
static bool wr(void *p,uint8_t a,uint8_t r,const uint8_t *b,size_t n){(void)p;assert(a==0x40);if(fail)return false;memcpy(regs[r],b,n);return true;}
static void put16(int r,unsigned int v){regs[r][0]=(unsigned char)(v>>8);regs[r][1]=(unsigned char)v;}
static void put20(int r,int v){unsigned int x=((unsigned int)v&0xFFFFFu)<<4;regs[r][0]=(unsigned char)(x>>16);regs[r][1]=(unsigned char)(x>>8);regs[r][2]=(unsigned char)x;}
int main(void){
 pdb_ina228 d={NULL,rd,wr,0.005,false};pdb_sample s;
 put16(0x3E,0x5449);put16(0x3F,0x2281);assert(pdb_ina228_init(&d)==PDB_OK);assert(regs[2][0]==0x10&&regs[2][1]==0);
 put16(0x0B,3);put20(7,80000);put20(4,80000);put20(5,86016);
 assert(pdb_ina228_sample(&d,&s)==PDB_OK&&s.valid);assert(fabs(s.current_a-5)<1e-9&&fabs(s.bus_v-16.8)<1e-9&&fabs(s.shunt_v-.025)<1e-9);
 put20(7,-80000);put20(4,-80000);assert(pdb_ina228_sample(&d,&s)==PDB_OK&&s.current_a==-5&&s.shunt_v==-.025);
 put20(7,524287);assert(pdb_ina228_sample(&d,&s)==PDB_SENSOR_FAULT&&!s.valid);put20(7,0);
 put16(0x0B,0x203);assert(pdb_ina228_sample(&d,&s)==PDB_SENSOR_FAULT&&!s.valid);
 put16(0x0B,0);assert(pdb_ina228_sample(&d,&s)==PDB_SENSOR_FAULT);put16(0x0B,1);assert(pdb_ina228_sample(&d,&s)==PDB_NOT_READY);put16(0x0B,3);
 put16(2,1000);assert(pdb_ina228_sample(&d,&s)==PDB_CONFIG_LOST&&!s.valid);assert(pdb_ina228_init(&d)==PDB_OK);
 put16(0,0x10);assert(pdb_ina228_sample(&d,&s)==PDB_CONFIG_LOST);assert(pdb_ina228_init(&d)==PDB_OK);
 fail=true;assert(pdb_ina228_sample(&d,&s)==PDB_IO_ERROR&&!s.valid&&isnan(s.current_a));fail=false;
 put16(0x3F,0x2381);assert(pdb_ina228_init(&d)==PDB_WRONG_DEVICE);
 d.shunt_ohms=0;assert(pdb_ina228_init(&d)==PDB_BAD_ARGUMENT);
 puts("INA228 tests passed: scaling, negative current, clipping, POR/config loss, bus errors, identity and flags.");return 0;
}
