"""Evaluate PDB-only gate timing with the unchanged Osiris reference model."""
from pathlib import Path
import sys,json
S=Path(__file__).resolve().parents[1]/'combined-20260915'
sys.path.insert(0,str(S));import verify_all as v
base=(S/'pdb/pdb_eco.lib').read_text()
results=[]
for cap in ('220n','470n','1u'):
 model=base.replace('C1   GATE_RC GND 22n','C1   GATE_RC GND '+cap)
 (S/('pdb/pdb_only_'+cap+'.lib')).write_text(model)
 s=(S/'eco_corners.cir').read_text().replace('pdb_eco.lib','pdb_only_'+cap+'.lib').replace('osiris_eco.lib','osiris_reva.lib')
 s=s.replace('1,300,2,300,3,610,4,610,5,1200,6,1200,7,2000,8,2000','1,12140,2,12140,3,28100,4,28100,5,44780,6,44780,7,60000,8,60000')
 s=s.replace('FROM 400m TO 500m','FROM 750m TO 850m')
 deck=S/('pdb_only_'+cap+'.cir');deck.write_text(s)
 r=v.run(deck,Path(r'C:/Program Files/ADI/LTspice/LTspice.exe'),180)
 results.append(r)
 print(cap,r['status'],r['errors'],{k:vals for k,vals in r['measurements'].items() if k in ('v5_ss','v3_ss','iin_peak','iin_step','t_3v3')},flush=True)
 (S.parent/'closure-20260915/pdb-only-candidates.json').write_text(json.dumps(results,indent=2))
