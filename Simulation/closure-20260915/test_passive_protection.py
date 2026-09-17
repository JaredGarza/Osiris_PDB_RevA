from pathlib import Path
import sys,json
S=Path(__file__).resolve().parents[1]/'combined-20260915'
sys.path.insert(0,str(S));import verify_all as v
s=(S/'pdb/pdb_filter.lib').read_text().replace('R1V=237k','R1V=226k')
s=s.replace('RF1  VBAT_RAW VBAT_FUSED {RFUSE}', '''RF1 VBAT_RAW DIODE_IN {RFUSE}
D4 DIODE_IN VBAT_FUSED STPST10H100_SCREEN
R20 DIODE_IN INPUT_DAMP 1
C11 INPUT_DAMP GND 1u Rser=50m''')
s=s.replace('D3   GND VOUT MBR0540','D3 GND VOUT STPST10H100_SCREEN')
s+='''
* Datasheet-fitted screening model, not an ST manufacturer model.
* ST DS14177 rev2: 25 C VF max .605 V at 5 A, .715 V at 10 A.
* Is/N/Rs fit those two points; Cjo approximates typical Fig6.
* No validated recovery, leakage, avalanche, or self-heating model.
.model STPST10H100_SCREEN D(Is=70n N=1.1 Rs=.018 Cjo=2n BV=100 IBV=26u Tnom=25)
'''
(S/'pdb/pdb_passive.lib').write_text(s)
results=[]
for base,name in [('final_transients','passive_transients'),('sensor_fault','passive_fault')]:
 s=(S/(base+'.cir')).read_text().replace('pdb_final.lib','pdb_passive.lib')
 s=s.replace('VBUS_MIN MIN V(VOUT)','VBUS_MIN MIN V(XPDB:INA_VBUS)').replace('VBUS_MIN MIN V(PDBOUT)','VBUS_MIN MIN V(XPDB:INA_VBUS)')
 s=s.replace('.end','.save V(XPDB:INA_VBUS)\n.end')
 (S/(name+'.cir')).write_text(s)
 r=v.run(S/(name+'.cir'),Path(r'C:/Program Files/ADI/LTspice/LTspice.exe'),180)
 results.append(r);print(name,r,flush=True)
 (S.parent/'closure-20260915/passive-protection.json').write_text(json.dumps(results,indent=2))
