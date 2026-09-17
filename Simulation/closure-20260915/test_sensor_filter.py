from pathlib import Path
import sys,json
S=Path(__file__).resolve().parents[1]/'combined-20260915'
sys.path.insert(0,str(S));import verify_all as v
s=(S/'pdb/pdb_final.lib').read_text().replace('XU2  INA_IN_P INA_IN_N VOUT', 'XU2  INA_IN_P INA_IN_N INA_VBUS')
s=s.replace('C7   INA_IN_P INA_IN_N 100n Rser=30m','''C7 INA_IN_P INA_IN_N 100n Rser=30m
* Candidate common-mode filters; values below are minimum effective capacitance.
C12 INA_IN_P GND 1u Rser=30m
C13 INA_IN_N GND 1u Rser=30m
R19 VOUT INA_VBUS 100
C14 INA_VBUS GND 100n Rser=30m''')
(S/'pdb/pdb_filter.lib').write_text(s)
s=(S/'sensor_fault.cir').read_text().replace('pdb_final.lib','pdb_filter.lib').replace('VBUS_MIN MIN V(PDBOUT)','VBUS_MIN MIN V(XPDB:INA_VBUS)')
s=s.replace('.end','.save V(XPDB:INA_VBUS)\n.end')
(S/'filter_fault.cir').write_text(s)
r=v.run(S/'filter_fault.cir',Path(r'C:/Program Files/ADI/LTspice/LTspice.exe'),180)
print(r,flush=True)
(S.parent/'closure-20260915/filter-fault.json').write_text(json.dumps(r,indent=2))
