"""One-time metadata reconciliation; no electrical or graphical edits."""
from pathlib import Path
import csv, io, json, re, shutil

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sch=ROOT/'Osiris_PDB_RevA.kicad_sch'
assert not list(ROOT.glob('*.lck')), 'Close KiCad before modifying saved source'
backup=HERE/'before-metadata'
assert not backup.exists(), 'Already applied; inspect backups instead of re-running'
backup.mkdir()
for name in ('Osiris_PDB_RevA.kicad_sch','BOM.csv','BOM_purchasing.csv'):
    shutil.copy2(ROOT/name,backup/name)
rows={r['Reference']:r for r in csv.DictReader((ROOT/'BOM.csv').open(encoding='utf-8-sig'))}
updates={
 'C1':{'Selection_Status':'Nominal gate-ramp estimate 6.25 kV/s; 20-60 uA and 5% C1 give 3.40-11.28 kV/s before MOSFET dynamics. See September 15 review.'},
 'C9':{'Selection_Status':'Output bulk capacitor; final total downstream capacitance and startup load must meet the proposed September 15 envelope. Inrush not qualified.'},
 'D1':{'Selection_Status':'Bidirectional 24 V TVS candidate; 38.9 V specified clamp is pulse-condition dependent. Source energy, ringing and downstream peak voltage remain open.'},
 'D2':{'Selection_Status':'Gate discharge bypass across R4, cathode at U1 GATE. Actual populated-circuit turn-off and hot-plug response require validation.'},
 'D3':{'Selection_Status':'OPEN: MBR0540 does not guarantee a -0.3 V clamp. Review INA228 IN+/IN-/VBUS and U3 IN/EN during negative transients; see September 15 review.'},
 'F1':{'Selection_Status':'PROVISIONAL 4 A for proposed 2.5 A continuous envelope. 1000 A interrupt rating; WXNV means 3000-piece packaging. Final source fault current and thermal coordination pending.'},
 'J2':{'Description':'JST GH 4-way I2C: 1 NC, 2 SCL, 3 SDA, 4 GND. New Osiris interface and cable continuity require verification.',
       'Selection_Status':'PDB pinout fixed; proposed Osiris 3.3 V pull-ups, 100 kHz, <=200 pF bus. No power on pin 1. Physical cable mating and new Rev B mapping unverified.'},
 'J3':{'Description':'Protected raw-4S power output: pin 1 GND, pin 2 PDB_VOUT; map physical contacts to new Osiris power entry.',
       'Selection_Status':'PDB polarity fixed. Verify physical cable contacts and board-edge clearance; old Osiris J16 numbering is not the new Rev B interface.'},
 'U3':{'Selection_Status':'OPEN: TPS7A16 OUT-IN absolute maximum +0.3 V can be exceeded when PDB_VOUT collapses. Reverse-current-protected replacement proposed in September 15 review; not applied.'}
}

def quote(s):
    return '"'+s.replace('\\','\\\\').replace('"','\\"').replace('\n','\\n')+'"'

def prop(block,key,value):
    pat=r'(\(property '+re.escape(quote(key))+r' )"(?:\\.|[^"\\])*"'
    if re.search(pat,block):
        return re.sub(pat,lambda m:m[1]+quote(value),block,count=1)
    at=re.search(r'\(at ([\d.-]+) ([\d.-]+)',block)
    field=(f'\n\t\t(property {quote(key)} {quote(value)}\n'
           f'\t\t\t(at {at[1]} {at[2]} 0)\n\t\t\t(hide yes)\n'
           '\t\t\t(effects (font (size 1.27 1.27)))\n\t\t)')
    return block[:-3]+field+'\n\t)'

raw=sch.read_bytes()
text=raw.decode('utf-8').replace('\r\n','\n')
changed=[]
def edit(m):
    block=m[0]
    match=re.search(r'\(property "Reference" "([^"]+)"',block)
    if not match or match[1] not in rows:
        return block
    ref=match[1]
    fields=dict(updates.get(ref,{}))
    if rows[ref]['MPN']:
        fields['MPN']=rows[ref]['MPN']
        fields['Manufacturer']=rows[ref]['Manufacturer']
    before=block
    for k,v in fields.items():
        block=prop(block,k,v)
    if before!=block:
        changed.append(ref)
    return block
text=re.sub(r'^\t\(symbol\n.*?^\t\)',edit,text,flags=re.M|re.S)
assert changed
sch.write_bytes(text.replace('\n','\r\n').encode('utf-8'))

# Re-serialize changed CSV rows only; retain every other byte, including order codes.
for name in ('BOM.csv','BOM_purchasing.csv'):
    path=ROOT/name
    data=path.read_bytes()
    bom=data.startswith(b'\xef\xbb\xbf')
    lines=data.decode('utf-8-sig').splitlines(keepends=True)
    header=next(csv.reader([lines[0]]))
    out=[lines[0]]
    for line in lines[1:]:
        values=next(csv.reader([line]))
        row=dict(zip(header,values))
        ref=row['Reference']
        if ref in updates:
            for key,value in updates[ref].items():
                column={'Selection_Status':'Selection Status','Description':'Specification'}[key]
                row[column]=value
            buf=io.StringIO(newline='')
            csv.writer(buf,lineterminator='\r\n').writerow([row[k] for k in header])
            out.append(buf.getvalue())
        else:
            out.append(line)
    path.write_bytes((b'\xef\xbb\xbf' if bom else b'')+''.join(out).encode('utf-8'))
(HERE/'metadata-changes.json').write_text(json.dumps({'schematic_refs':changed,'field_changes':updates,'MPNs':'Reconciled all active schematic MPNs to curated BOM; values, footprints, pins and wiring unchanged.'},indent=2)+'\n')
print('Updated metadata for',', '.join(changed))
