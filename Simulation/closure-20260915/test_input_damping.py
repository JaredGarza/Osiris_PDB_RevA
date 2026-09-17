from pathlib import Path
import sys,json
S=Path(__file__).resolve().parents[1]/'combined-20260915'
sys.path.insert(0,str(S));import verify_all as v
s=(S/'pdb/pdb_final.lib').read_text().replace('XD1  VBAT_FUSED GND SMAJ24CA','XD1  VBAT_FUSED GND SMAJ24CA\nRIN_DAMP VBAT_FUSED INPUT_DAMP 1\nCIN_DAMP INPUT_DAMP GND 1u Rser=50m')
(S/'pdb/pdb_damped.lib').write_text(s)
s=(S/'final_transients.cir').read_text().replace('pdb_final.lib','pdb_damped.lib')
(S/'damped_transients.cir').write_text(s)
r=v.run(S/'damped_transients.cir',Path(r'C:/Program Files/ADI/LTspice/LTspice.exe'),180)
print(r['status'],r['errors'],r['measurements'],flush=True)
(S.parent/'closure-20260915/damping.json').write_text(json.dumps(r,indent=2))
