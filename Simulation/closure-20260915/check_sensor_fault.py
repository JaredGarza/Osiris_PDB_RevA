from pathlib import Path
import sys,json
S=Path(__file__).resolve().parents[1]/'combined-20260915'
sys.path.insert(0,str(S));import verify_all as v
s=(S/'final_faults_fine.cir').read_text().replace('.end','''.meas TRAN INP_MIN MIN V(XPDB:INA_IN_P) FROM 899.9m TO 1.1
.meas TRAN INN_MIN MIN V(XPDB:INA_IN_N) FROM 899.9m TO 1.1
.meas TRAN VBUS_MIN MIN V(PDBOUT) FROM 899.9m TO 1.1
.save V(XPDB:INA_IN_P) V(XPDB:INA_IN_N)
.end''')
(S/'sensor_fault.cir').write_text(s)
r=v.run(S/'sensor_fault.cir',Path(r'C:/Program Files/ADI/LTspice/LTspice.exe'),180)
print(r,flush=True)
(S.parent/'closure-20260915/sensor-fault.json').write_text(json.dumps(r,indent=2))
