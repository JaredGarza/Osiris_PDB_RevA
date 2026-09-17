from pathlib import Path
import sys,json
S=Path(__file__).resolve().parents[1]/'combined-20260915'
sys.path.insert(0,str(S));import verify_all as v
s=(S/'pdb/pdb_final.lib').read_text()
s=s.replace('RF1  VBAT_RAW VBAT_FUSED {RFUSE}', '''RF1 VBAT_RAW IDEAL_IN {RFUSE}
* Experimental upstream ideal diode; ADI LTC4359 example topology.
MQ3 VBAT_FUSED IDEAL_GATE IDEAL_IN IDEAL_IN ISC015N06NM5LF2
XU5 VBAT_FUSED IDEAL_GATE IDEAL_IN IDEAL_IN IDEAL_SHDN IDEAL_VSS LTC4359
R19 IDEAL_VSS GND 1k
XD4 IDEAL_IN IDEAL_VSS SMAJ24CA
C11 VBAT_FUSED IDEAL_VSS 1.5u Rser=50m
RIN_DAMP IDEAL_IN INPUT_DAMP 1
CIN_DAMP INPUT_DAMP GND 1u Rser=50m''')
(S/'pdb/pdb_ideal.lib').write_text(s)
s=(S/'final_transients.cir').read_text().replace('pdb_final.lib','pdb_ideal.lib')
s=s.replace('.step param',r'.lib C:\Users\jared\AppData\Local\LTspice\lib\sub\LTC4359.sub'+'\n.step param')
s=s.replace('.end','''.meas TRAN U5_IN_MIN MIN V(XPDB:IDEAL_IN,XPDB:IDEAL_VSS)
.meas TRAN U5_OUT_MIN MIN V(XPDB:VBAT_FUSED,XPDB:IDEAL_VSS)
.meas TRAN Q3_VDS MAX ABS(V(XPDB:VBAT_FUSED,XPDB:IDEAL_IN))
.meas TRAN Q3_VGS MAX ABS(V(XPDB:IDEAL_GATE,XPDB:IDEAL_IN))
.save V(XPDB:IDEAL_IN) V(XPDB:IDEAL_VSS) V(XPDB:IDEAL_GATE)
.end''')
(S/'ideal_transients.cir').write_text(s)
r=v.run(S/'ideal_transients.cir',Path(r'C:/Program Files/ADI/LTspice/LTspice.exe'),180)
print(r,flush=True)
(S.parent/'closure-20260915/ideal-input.json').write_text(json.dumps(r,indent=2))
