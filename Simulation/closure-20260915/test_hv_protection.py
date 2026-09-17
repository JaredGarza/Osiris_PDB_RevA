"""Compare 100 V FET protection variants under the fast-reversal transient.

Instruments EVERY LTC4368 absolute-maximum pin rating, including VOUT/SENSE
and the VIN-to-VOUT differential that earlier reviews never measured, plus
FET VDS and VGS. Limits come from LTC4368 Rev C page 4 and BSC070N10NS5
rev 2.3 -- they are abs-max ratings, not deratings, and not a hardware
qualification.
"""
from pathlib import Path
import sys, json

H = Path(__file__).resolve().parent
S = H.parents[0] / 'combined-20260915'
sys.path.insert(0, str(S))
import verify_all as v
import build_hv_lib

LTSPICE = Path(r'C:/Program Files/ADI/LTspice/LTspice.exe')

# Same stimulus as final_transients/passive_transients so results compare
# directly: charged-output reversal, 3 harness inductances, 20 mOhm source.
DECK = """* 100 V FET protection candidate, variant {V}. Screening only.
* Reversed hot-plug, charged-output reversal, loss of input, and restart.
* 0.2/2/20 uH source/harness inductance sensitivity; 20 mOhm source.
.lib C:\\Users\\jared\\AppData\\Local\\LTspice\\lib\\sub\\LTC4368-1.sub
.lib C:\\Users\\jared\\AppData\\Local\\LTspice\\lib\\sub\\LT3010.lib
.inc models\\pdb_devices.lib
.inc pdb\\pdb_hv{v}.lib
.step param LH list 200n 2u 20u
VBAT SRC 0 PWL(0 0 10u -25 50m -25 50.01m 16.8 150m 16.8 150.01m -25 250m -25 250.01m 16.8 350m 16.8 350.01m 0 400m 0 400.01m 16.8 600m 16.8)
RSRC SRC L_IN 20m
LSRC L_IN VIN {{LH}} Rser=1m
XPDB VIN VOUT V3V3 GP GF COMMON FAULT ALERT SCL SDA 0 PDB_CURRENT
RLOAD VOUT 0 6.72
CLOAD VOUT 0 220u Rser=20m
.tran 0 600m 0 5u
.options method=gear reltol=0.003 cshunt=10p
* --- INA228 analog pin stress (abs max -0.3 V) ---
.meas TRAN INP_MIN MIN V(XPDB:INA_IN_P)
.meas TRAN INN_MIN MIN V(XPDB:INA_IN_N)
.meas TRAN VBUS_MIN MIN V(XPDB:INA_VBUS)
* --- LTC4368 pin stress (Rev C p.4 absolute maximum ratings) ---
.meas TRAN U1_VIN_MIN  MIN V({PIN})
.meas TRAN U1_VIN_MAX  MAX V({PIN})
.meas TRAN U1_VOUT_MIN MIN V(XPDB:SHUNT_LO)
.meas TRAN U1_VOUT_MAX MAX V(XPDB:SHUNT_LO)
.meas TRAN U1_SENSE_MIN MIN V(XPDB:SHUNT_HI)
.meas TRAN U1_SENSE_MAX MAX V(XPDB:SHUNT_HI)
.meas TRAN U1_VOUT_SENSE_ABS MAX ABS(V(XPDB:SHUNT_LO,XPDB:SHUNT_HI))
.meas TRAN U1_VIN_VOUT_MIN MIN V({PIN},XPDB:SHUNT_LO)
.meas TRAN U1_VIN_VOUT_MAX MAX V({PIN},XPDB:SHUNT_LO)
.meas TRAN U1_GATE_MIN MIN V(GP)
.meas TRAN U1_GATE_VIN_MAX MAX V(GP,{PIN})
.meas TRAN U1_RETRY_MIN MIN V(XPDB:N_RETRY)
.meas TRAN U1_RETRY_MAX MAX V(XPDB:N_RETRY)
* --- divider pins: below -0.3 V is allowed if pin current stays under 1 mA ---
.meas TRAN U1_UV_MIN  MIN V(XPDB:N_UV)
.meas TRAN U1_OV_MIN  MIN V(XPDB:N_OV)
.meas TRAN U1_OV_MAX  MAX V(XPDB:N_OV)
.meas TRAN U1_SHDN_MIN MIN V(XPDB:SHDN_LTC)
.meas TRAN BUS_MIN MIN V(XPDB:VBAT_FUSED)
* --- MOSFET stress ---
.meas TRAN Q1_VDS MAX ABS(V(XPDB:VBAT_FUSED,COMMON))
.meas TRAN Q2_VDS MAX ABS(V(XPDB:PDB_PROTECTED,COMMON))
.meas TRAN VGS_MAX MAX ABS(V(GF,COMMON))
* --- rail integrity ---
.meas TRAN TVS_IPK MAX ABS(V(XPDB:TVS_K)/1m)
.meas TRAN TVS_I2T INTEG (V(XPDB:TVS_K)*V(XPDB:TVS_K)*1e6)
.meas TRAN V3V3_MAX MAX V(V3V3)
.meas TRAN VOUT_FINAL AVG V(VOUT) FROM 550m TO 595m
.save V(XPDB:INA_IN_P) V(XPDB:INA_IN_N) V(XPDB:INA_VBUS) V(VOUT) V(V3V3)
.save V(XPDB:VBAT_FUSED) V({PIN}) V(COMMON) V(XPDB:PDB_PROTECTED) V(GF) V(GP)
.save V(XPDB:SHUNT_HI) V(XPDB:SHUNT_LO) V(XPDB:N_UV) V(XPDB:N_OV)
.save V(XPDB:N_RETRY) V(XPDB:SHDN_LTC) V(XPDB:TVS_K)
.end
"""


VARIANTS = tuple(sys.argv[1:]) or ('A', 'B')


def main():
    results = []
    for variant in VARIANTS:
        build_hv_lib.build(variant)
        pin = 'XPDB:VIN_PIN' if variant == 'B' else 'XPDB:VBAT_FUSED'
        name = f'hv{variant.lower()}_transients'
        (S / f'{name}.cir').write_text(
            DECK.format(V=variant, v=variant.lower(), PIN=pin))
        r = v.run(S / f'{name}.cir', LTSPICE, 300)
        results.append(r)
        print(name, r['status'], r['seconds'], flush=True)
        for e in r['errors'][:12]:
            print('   ', e, flush=True)
        (H / 'hv-protection.json').write_text(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
