from pathlib import Path
import sys,json
S=Path(__file__).resolve().parents[1]/'combined-20260915'
sys.path.insert(0,str(S));import verify_all as v
s=(S/'pdb/pdb_damped.lib').read_text().replace('XD1  VBAT_FUSED GND SMAJ24CA','XD1  VBAT_FUSED GND SMCJ24CA_SCREEN')
s+='\n* Conservative datasheet-fit screening model, not manufacturer SPICE.\n* 29.5 V upper breakdown plus forward junction; 0.244 ohm total series slope.\n.subckt SMCJ24CA_SCREEN A1 A2\nDA MID A1 DSMCJ_SCREEN\nDB MID A2 DSMCJ_SCREEN\n.model DSMCJ_SCREEN D(Is=1e-12 N=1 Rs=.122 Cjo=2n BV=29.5 IBV=1m Tnom=27)\n.ends SMCJ24CA_SCREEN\n'
(S/'pdb/pdb_tvs.lib').write_text(s)
s=(S/'final_transients.cir').read_text().replace('pdb_final.lib','pdb_tvs.lib')
(S/'tvs_transients.cir').write_text(s)
s=(S/'final_faults.cir').read_text().replace('pdb_final.lib','pdb_tvs.lib')
s=s.replace('.end','.meas TRAN INP_MIN MIN V(XPDB:INA_IN_P) FROM 899.9m TO 1.1\n.meas TRAN INN_MIN MIN V(XPDB:INA_IN_N) FROM 899.9m TO 1.1\n.meas TRAN VBUS_MIN MIN V(PDBOUT) FROM 899.9m TO 1.1\n.meas TRAN D3_IPK MAX ABS(I(XPDB:D3)) FROM 899.9m TO 1.1\n.end')
(S/'tvs_faults.cir').write_text(s)
results=[]
for name in ('tvs_transients','tvs_faults'):
 r=v.run(S/(name+'.cir'),Path(r'C:/Program Files/ADI/LTspice/LTspice.exe'),180)
 results.append(r);print(name,r['status'],r['errors'],r['measurements'],flush=True)
 (S.parent/'closure-20260915/tvs.json').write_text(json.dumps(results,indent=2))
