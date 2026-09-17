"""Selected A-P4 circuit: low-loss reverse blocking and defined filter parts."""
from pathlib import Path
H=Path(__file__).resolve().parent;S=H.parent/'combined-20260915'
s=(S/'pdb/pdb_selected.lib').read_text()
s=s.replace('* Experimental upstream ideal diode; ADI LTC4359 example topology.','* LTC4359 upstream ideal diode; 100 V Q3. A-P4 selected circuit.')
s=s.replace('C11 VBAT_FUSED IDEAL_VSS 1.5u Rser=50m','C11 VBAT_FUSED IDEAL_VSS {1u*CFILM} Rser=50m\nC15 VBAT_FUSED IDEAL_VSS {1u*CFILM} Rser=50m')
s=s.replace('RIN_DAMP IDEAL_IN INPUT_DAMP 1','R20 IDEAL_IN INPUT_DAMP 1')
s=s.replace('CIN_DAMP INPUT_DAMP GND 1u Rser=50m','C16 INPUT_DAMP GND {1u*CFILM} Rser=50m')
s=s.replace('C12 INA_IN_P GND 1u Rser=30m','C12 INA_IN_P GND {1u*CFILM*CMISMATCH} Rser=50m')
s=s.replace('C13 INA_IN_N GND 1u Rser=30m','C13 INA_IN_N GND {1u*CFILM/CMISMATCH} Rser=50m')
s=s.replace('C14 INA_VBUS GND 100n Rser=30m','C14 INA_VBUS GND {1u*CFILM} Rser=50m')
s=s.replace('RHV_VOUT=1G','CFILM=0.9 CMISMATCH=1 RHV_VOUT=1G')
s=s.replace('A-P3-DRAFT ECO:','A-P4-DRAFT:')
(S/'pdb/pdb_release.lib').write_text(s)
print('Wrote selected circuit with film-capacitance tolerance parameters.')
