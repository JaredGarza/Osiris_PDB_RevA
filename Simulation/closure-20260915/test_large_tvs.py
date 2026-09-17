from pathlib import Path
import sys,json
S=Path(__file__).resolve().parents[1]/'combined-20260915'
sys.path.insert(0,str(S));import verify_all as v
s=(S/'pdb/pdb_tvs.lib').read_text().replace('SMCJ24CA_SCREEN','SM8S24CA_SCREEN').replace('Rs=.122 Cjo=2n BV=29.5','Rs=.02765 Cjo=10n BV=30.5')
s=s.replace('0.244 ohm total series slope','0.0553 ohm total slope; 30.5 V BV emulates hot upper corner')
(S/'pdb/pdb_large_tvs.lib').write_text(s)
s=(S/'tvs_transients.cir').read_text().replace('pdb_tvs.lib','pdb_large_tvs.lib')
(S/'large_tvs_transients.cir').write_text(s)
s=(S/'tvs_faults.cir').read_text().replace('pdb_tvs.lib','pdb_large_tvs.lib').replace('I(XPDB:D3)','I(D:XPDB:D3)')
s=s.replace('.end','.save V(OSIN) V(V5) V(V3) V(PDB3V3) V(VBIN) V(PDBOUT) V(V5PROT) I(RBATT) V(XPDB:INA_IN_P) V(XPDB:INA_IN_N) I(D:XPDB:D3)\n.end')
(S/'large_tvs_faults.cir').write_text(s)
results=[]
for name in ('large_tvs_transients','large_tvs_faults'):
 r=v.run(S/(name+'.cir'),Path(r'C:/Program Files/ADI/LTspice/LTspice.exe'),180)
 results.append(r);print(name,r['status'],r['errors'],r['measurements'],flush=True)
 (S.parent/'closure-20260915/large-tvs.json').write_text(json.dumps(results,indent=2))
