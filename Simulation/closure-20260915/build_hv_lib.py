"""Build 100 V FET protection candidate libraries.

Variants (all SCREENING models, none is hardware qualification):
  A  100 V FETs + 1x SM8S24CA + input damping + sensor filters
  B  A plus a series-R/Schottky clamp on the LTC4368 VIN pin   [REJECTED]
  C  A with 2x SM8S24CA in parallel (lower dynamic resistance)
  E  C plus a series Schottky blocking diode in the main path

Variant B is retained only to reproduce its failure: clamping VIN breaks the
LTC4368 gate-drive reference, pushing VGS to 22.3 V (abs max 20 V) and letting
the negative bus reach the INA228 pins. Do not use it.

The BSC070N10NS5 VDMOS is datasheet-fitted, not an Infineon model: no
validated SOA, avalanche, thermal or reverse-recovery behaviour.
"""
from pathlib import Path

S = Path(__file__).resolve().parents[1] / 'combined-20260915'

# Infineon BSC070N10NS5 rev 2.3 (Datasheets/BSC070N10NS5.txt):
#   V(BR)DSS 100 V   VGS +/-20 V   VGS(th) 2.2/3.0/3.8 V
#   RDS(on) 6.0 typ / 7.0 max @ VGS=10V, ID=40A      gfs 38 min / 77 typ
#   Ciss 2100p  Coss 340p  Crss 16p @ VDS=50V        RG 1.0/1.5 ohm
#   Qg 30n  Qgs 10n  Qgd 6n        VSD 0.9 typ / 1.1 max @ 40 A
#   EAS 73 mJ  RthJC 0.9/1.5 K/W   ID 80 A @ TC=25C   PG-TDSON-8 (SuperSO8)
# Fit: Rd+Rs hold RDS(on)~6.3 m; Kp=34 gives gm=sqrt(2*Kp*Id)=52 S at 40 A,
# between the 38 S minimum and 77 S typical. Cgd/Cjo approximate Qgd/Qoss.
FET_MODEL = """
* ** FIDELITY WARNING -- SURROGATE, NOT AN INFINEON MODEL **
* Datasheet-fitted VDMOS for screening overvoltage/gate stress only.
* Not valid for SOA, avalanche, reverse-recovery or thermal qualification.
.model BSC070N10NS5 VDMOS(nchan
+ Vto=3.0 Kp=34 lambda=0
+ Rd=1.5m Rs=0.3m Rg=1.5
+ Cgs=2.08n Cgdmax=1n Cgdmin=16p a=0.3 Cjo=1.2n
+ Is=7e-11 N=1.0 Rb=5m
+ BV=100 IBV=250u
+ mtriode=1.0 ksubthres=0.1
+ Tnom=25)
"""

# SM8S24CA-class bidirectional TVS, 24 V standoff. Rs fits the datasheet
# clamping slope; the model has NO pulse-width derating, so peak current must
# be compared against the part's pulse curve by hand.
TVS_MODEL = """
.subckt SM8S24CA_SCREEN A1 A2
DA A1 MID DSM8S_SCREEN
DB A2 MID DSM8S_SCREEN
.ends SM8S24CA_SCREEN
.model DSM8S_SCREEN D(Is=1e-12 N=1 Rs=.02765 Cjo=10n BV=30.5 IBV=1m Tnom=27)
"""

# ST STPST10H100SB-TR, 100 V 10 A DPAK. VF max .605 V @ 5 A, .715 V @ 10 A.
DIODE_MODEL = """
* Datasheet-fitted screening model, not an ST manufacturer model.
.model STPST10H100_SCREEN D(Is=70n N=1.1 Rs=.018 Cjo=2n BV=100 IBV=26u Tnom=25)
"""


def build(variant: str) -> Path:
    s = (S / 'pdb/pdb_filter.lib').read_text()

    # 100 V FETs, same SuperSO8 / PG-TDSON-8 pinout as the 60 V part.
    s = s.replace('ISC015N06NM5LF2', 'BSC070N10NS5')

    # Input TVS: one or two SM8S24CA in parallel. RTVS is a 1 mOhm sense
    # stand-in for the clamp return trace so the deck can measure total TVS
    # current as V(TVS_K)/0.001.
    n_tvs = {'A': 1, 'B': 1, 'C': 2, 'E': 2, 'D': 3, 'F': 2}[variant]
    refs = ['XD1', 'XD6', 'XD7'][:n_tvs]
    tvs = '\n'.join(f'{r}  VBAT_FUSED TVS_K SM8S24CA_SCREEN' for r in refs)
    tvs += '\nRTVS TVS_K GND 1m'
    s = s.replace('XD1  VBAT_FUSED GND SMAJ24CA', tvs)

    # Harness-inductance damping at the input.
    cdamp = '10u' if variant == 'F' else '1u'
    damp = ('R20  VBAT_FUSED INPUT_DAMP 1\n'
            f'C11  INPUT_DAMP GND {cdamp} Rser=50m')
    if variant == 'E':
        # Series blocking Schottky ahead of all protected electronics; the
        # damping network sits on the unblocked side.
        s = s.replace('RF1  VBAT_RAW VBAT_FUSED {RFUSE}',
                      'RF1  VBAT_RAW DIODE_IN {RFUSE}\n'
                      'D4   DIODE_IN VBAT_FUSED STPST10H100_SCREEN\n'
                      'R20  DIODE_IN INPUT_DAMP 1\n'
                      'C11  INPUT_DAMP GND 1u Rser=50m')
        s = s.replace('D3   GND VOUT MBR0540', 'D3   GND VOUT STPST10H100_SCREEN')
    else:
        s = s.replace('RF1  VBAT_RAW VBAT_FUSED {RFUSE}',
                      'RF1  VBAT_RAW VBAT_FUSED {RFUSE}\n' + damp)

    if variant == 'B':
        s = s.replace('XU1  VBAT_FUSED N_UV', 'XU1  VIN_PIN N_UV')
        s = s.replace('R6   VBAT_FUSED SHDN_LTC 680k',
                      'R21  VBAT_FUSED VIN_PIN 470\n'
                      'D5   GND VIN_PIN MBR0540\n'
                      'R6   VBAT_FUSED SHDN_LTC 680k')

    s += FET_MODEL + TVS_MODEL
    if variant == 'E':
        s += DIODE_MODEL
    out = S / f'pdb/pdb_hv{variant.lower()}.lib'
    out.write_text(s)
    return out


if __name__ == '__main__':
    for v in ('A', 'B', 'C', 'E'):
        p = build(v)
        print(p.name, p.stat().st_size)
