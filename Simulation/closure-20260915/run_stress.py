from pathlib import Path
import sys,json,re
S=Path(__file__).resolve().parents[1]/'combined-20260915'
sys.path.insert(0,str(S));import verify_all as v
s=(S/'protection_transients.cir').read_text().replace('pdb_coordinated.lib','pdb_eco.lib')
s=s.replace('RCIN VIN CIN 1\nCCIN CIN 0 1u\n','')
(S/'eco_transients.cir').write_text(s)
s=(S/'eco_reverse.cir').read_text().replace('.step param VREV list -14.8 -16.8','.param VREV=-25')
(S/'eco_reverse25.cir').write_text(s)
s=(S/'current_uvstate.cir').read_text()
s=s[s.index('.lib '):].replace('pdb_current.lib','pdb_eco.lib').replace('osiris_reva.lib','osiris_eco.lib')
(S/'eco_weak_source.cir').write_text('* Source-impedance sensitivity; includes operation outside the proposed normal envelope.\n'+s)
results=[]
for name in ('eco_reverse25','eco_transients','eco_weak_source'):
 r=v.run(S/(name+'.cir'),Path(r'C:/Program Files/ADI/LTspice/LTspice.exe'),180)
 results.append(r);print(name,r['status'],r['errors'],r['measurements'],flush=True)
 (S.parent/'closure-20260915/stress.json').write_text(json.dumps(results,indent=2))
