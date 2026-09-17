from pathlib import Path
import json,re
import develop_protection as d
s=(d.S/'pdb/pdb_release.lib').read_text().replace('.ends PDB_CURRENT','C17 IDEAL_GATE IDEAL_IN 10n Rser=50m\n.ends PDB_CURRENT')
(d.S/'pdb/pdb_gate_hold.lib').write_text(s)
t=(d.S/'release_transients.cir').read_text().replace('pdb_release.lib','pdb_gate_hold.lib').replace('.step param LH list 200n 2u 20u','.step param LH list 200n 20u')
p=d.S/'gate_hold_transients.cir';p.write_text(t)
d.v.limits=lambda name:dict(u5_gs_min=(-.3,15),u5_gs_max=(-.3,15),u5_in_min=(-40,100),q3_vds=(0,100),vout_final=(16,16.8),inp_min=(-.3,85))
r=d.v.run(p,Path(r'C:/Program Files/ADI/LTspice/LTspice.exe'),180)
(d.H/'gate-hold.json').write_text(json.dumps(r,indent=2));print(r['status'],r['errors'],r['measurements'],flush=True)
