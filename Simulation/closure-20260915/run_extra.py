from pathlib import Path
import sys,json
S=Path(__file__).resolve().parents[1]/'combined-20260915'
sys.path.insert(0,str(S));import verify_all as v
s=(S/'eco_reverse.cir').read_text().replace('.step param VREV list -14.8 -16.8','.param VREV=-25')
(S/'eco_reverse25.cir').write_text(s)
s=(S/'eco_lowtrip.cir').read_text().replace('RSHUNT=12.625m','RSHUNT=16.833333m')
s='* Emulate 30 mV zero-output minimum using nominal 50 mV model and increased sense resistor.\n'+s
(S/'eco_zeroout.cir').write_text(s)
s=(S/'eco_corners.cir').read_text().replace('.step param CASE list 1 2 3 4 5 6 7 8','.step param CASE list 1 2 3 4 5 6 7 8\n.step temp list 0 60')
(S/'eco_temperature.cir').write_text(s)
results=[]
for name in ('eco_reverse25','eco_zeroout','eco_temperature'):
 r=v.run(S/(name+'.cir'),Path(r'C:/Program Files/ADI/LTspice/LTspice.exe'),180)
 results.append(r);print(name,r['status'],r['errors'],r['measurements'],flush=True)
 (S.parent/'closure-20260915/extra.json').write_text(json.dumps(results,indent=2))
