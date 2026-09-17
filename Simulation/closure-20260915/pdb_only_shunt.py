"""PDB-only startup coordination; unchanged Osiris open-pin eFuse slew."""
from pathlib import Path
import sys,json
S=Path(__file__).resolve().parents[1]/'combined-20260915'
sys.path.insert(0,str(S));import verify_all as v
model=(S/'pdb/pdb_eco.lib').read_text().replace('RSHUNT=10m','RSHUNT=5m')
(S/'pdb/pdb_only_5m.lib').write_text(model)
results=[]
for name,rsh in [('pdb5_corners','5.05m'),('pdb5_lowtrip','6.3125m')]:
 s=(S/'eco_corners.cir').read_text().replace('pdb_eco.lib','pdb_only_5m.lib').replace('osiris_eco.lib','osiris_reva.lib')
 s=s.replace('RSHUNT=10.1m','RSHUNT='+rsh)
 s=s.replace('1,300,2,300,3,610,4,610,5,1200,6,1200,7,2000,8,2000','1,12140,2,12140,3,28100,4,28100,5,44780,6,44780,7,60000,8,60000')
 s=s.replace('.end','.meas TRAN IIN_LOWV MAX if(V(PDBOUT)<2,abs(I(RBATT)),0)\n.end')
 deck=S/(name+'.cir');deck.write_text(s)
 r=v.run(deck,Path(r'C:/Program Files/ADI/LTspice/LTspice.exe'),180)
 results.append(r)
 print(name,r['status'],r['errors'],{k:vals for k,vals in r['measurements'].items() if k in ('v5_ss','v3_ss','iin_peak','iin_step','t_3v3','iin_lowv')},flush=True)
 (S.parent/'closure-20260915/pdb-only-shunt.json').write_text(json.dumps(results,indent=2))
