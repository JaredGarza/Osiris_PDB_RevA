"""Reduce saved data and focus timestep comparison on the unchanged fault event."""
from pathlib import Path
import re,shutil
H=Path(__file__).resolve().parent;S=H.parent/'combined-20260915'
if not (H/'core-initial.json').exists():shutil.copy2(S/'audit/verification.json',H/'core-initial.json')
p=S/'final_faults_fine.cir';s=p.read_text()
s=s.replace('.tran 0 3.0 0 1u','.tran 0 1.12 0 1u')
s=re.sub(r'^\.meas TRAN (?:T_REC_V3|REC_\w+)\s+.*\n','',s,flags=re.M)
if '.save ' not in s:s=s.replace('.end','.save V(OSIN) V(V5) V(V3) V(V5PROT) V(PDB3V3) V(VBIN) V(PDBOUT) I(RBATT)\n.end')
p.write_text(s)
p=S/'final_transients.cir';s=p.read_text()
if '.save ' not in s:s=s.replace('.end','.save V(XPDB:INA_IN_P) V(XPDB:INA_IN_N) V(VOUT) V(XPDB:VBAT_FUSED) V(COMMON) V(XPDB:PDB_PROTECTED) V(GF) V(V3V3)\n.end')
p.write_text(s)
