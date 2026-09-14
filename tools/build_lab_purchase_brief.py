"""Build a purchasing discussion brief from the unchanged A-P1 order list."""
from pathlib import Path
import csv
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
rows = list(csv.DictReader((ROOT/'procurement/2026-09-13/PDB-grouped-order-list.csv').open(newline='', encoding='utf-8-sig')))
common = {'C0603C104K4RACTU','C1608X7R1H104K080AA','RC0805FR-0710RL','RC0805FR-0722KL','RC0805FR-074K7L'}
passives = [r for r in rows if r['mpn'].startswith(('C0','C1','C2','C3','RC0805'))]
special = [r for r in rows if r not in passives]
assert len(rows)==27 and sum(int(r['qty']) for r in rows)==33
assert len(passives)==14 and len(special)==13
spec = {
'C0603C104K4RACTU':'100 nF, 16 V, X7R, 10%',
'C1608X7R1H104K080AA':'100 nF, 50 V, X7R, 10%',
'C2012C0G2A562J125AA':'5.6 nF, 100 V, C0G, 5%',
'C2012X7R1A106K125AC':'10 uF, 10 V, X7R, 10%',
'C2012X7R1H105K125AB':'1 uF, 50 V, X7R, 10%',
'C3216X7R1H106K160AC':'10 uF, 50 V, X7R, 10%',
'FC4L64R005FER':'5 milliohm, 4-terminal shunt',
}
def description(r):
    if r['mpn'].startswith('RC0805'): return r['value']+' ohm, 1%, 0.125 W'
    return spec.get(r['mpn'],r['value'])
intro = [
('Purpose', 'Prepare a shared lab stock purchase for the new pick-and-place machine, plus the exact parts needed for PDB Rev A prototypes. Prepared September 14, 2026 for the September 15 discussion. Build quantity, machine model, budget and existing usable stock are not yet known.'),
('Recommendation', 'Inventory Ryan\'s R/C/L books first. Request quotes for small machine-ready reels of the most reusable passives and compare with one factory reel per selected stock item. Buy project-specific ICs, MOSFETs, shunts and connectors in prototype quantities. Do not buy full semiconductor reels just because the order code is a reel variant.'),
('What is confirmed', 'The A-P1 PDB baseline contains 27 unique purchased part codes, 33 physical items per board and 29 SMT placements across 23 SMT part types. Seven bare test pads do not require purchased parts. This list supports procurement planning; final circuit qualification and PCB layout remain open.'),
('Osiris Rev B boundary', 'The new Rev B power path and top-facing ports are planned, not saved as a completed design. Its new regulator, inductor and power-path BOM is unknown. Historical Osiris passives are largely 0402, while this PDB uses 0603/0805/1206. Equal values in different packages cannot share a reel. No new Rev B quantities are included here.'),
]
actions = [
('Ryan\'s books: inventory before buying', 'Record value, EIA package, manufacturer/MPN, tolerance, power or voltage rating, dielectric, quantity and carrier condition. Distinguish loose parts, short tape strips and continuous tape. Count stock toward machine assembly only after feeder compatibility is established. Unidentified parts are not approved substitutions for the PDB.'),
('Shared stock proposal', 'For each of the five A-marked candidates, quote 250 and 1,000 parts on a custom reel, plus the smallest factory reel. These are quote tiers, not committed order quantities. Select one tier after checking other project BOMs, Ryan\'s stock and total cost including reeling. The two 100 nF parts remain separate MPNs; combining them needs a reviewed substitution.'),
('Project-specific quantity rule', 'For each B or C item, order max(0, boards to build x quantity per board + setup losses + repair spares - usable on-hand stock), rounded to supplier pack quantity. Establish setup loss with the machine supplier; do not assume a percentage covers feeder loading. Request continuous cut tape or a custom reel for SMT parts; loose pieces are for supported trays/manual work only.'),
('Machine and assembly purchases', 'Confirm machine model, 0402 capability, feeder widths and pitch, reel diameter, component height limits, nozzle selection, vision support and cut-tape/tray handling. There are 23 SMT part types on the PDB; that is not a guaranteed 23-slot feeder requirement because widths and staging vary. Budget feeders, suitable nozzles, leader/trailer supplies, ESD storage and moisture-control supplies as required by component handling specifications.'),
('Items outside the PCB BOM', 'Budget solder paste compatible with the process, flux/cleaning supplies, stencil and board support, reflow capability and inspection equipment. Quote stencil/panel details after layout is released. Add the PDB-to-Osiris power and I2C harnesses, mating housings/contacts and crimp tooling once connector orientation, wire gauge and length are fixed; they are not included in the 33-item board count.'),
('Hold before production-volume buying', 'Finalize the Rev B power/load budget and interface, then resolve the provisional 4 A fuse rating, MOSFET fault-energy/SOA and clamp validation. Historical overlaps in INA228 and JST/XT60 connectors are candidates only. Do not stock new Rev B regulators or inductors until their electrical and package requirements are selected.'),
('Decisions for the meeting', 'Agree a shared-stock budget, nominate someone to inventory Ryan\'s books, obtain the machine/feeder specification, and choose the initial PDB build quantity. Then request distributor quotes with exact MPN, carrier, pack quantity, lead time, stock and total price. No live prices or stock availability have been quoted in this brief.'),
]
sources = [
('A-P1 source','procurement/2026-09-13/PDB-grouped-order-list.csv; tag pdb-procurement-2026-09-13. Exact electrical specifications are retained in the baseline purchasing workbook and datasheets.'),
('Custom reels','https://forum.digikey.com/t/details-about-digi-reels/1303'),
('Cut tape packaging','https://forum.digikey.com/t/a-closer-look-at-taped-packaging-including-cut-tape-and-tape-and-reels/17211'),
]
def tier(r):
    if r['mpn']=='0297004.WXNV': return 'HOLD rating'
    if r['mpn'] in common: return 'A - stock candidate'
    if r in passives: return 'B - small tape/reel'
    return 'C - prototype SMT' if r['route']=='SMT' else 'C - manual/TH'
md=['# Lab stock and PDB purchasing brief','', '## Purchase strategy','']
for title,body in intro: md += ['### '+title,'',body,'']
for title,group in [('Passives',passives),('Specialized and mechanical parts',special)]:
    md += ['## '+title,'','| Exact MPN | References | Per PDB | Description | Package | Purchase class |','|---|---|---:|---|---|---|']
    for r in group: md += ['| '+' | '.join([r['mpn'],r['refs'],r['qty'],description(r),r['package'],tier(r)])+' |']
    md += ['']
for title,body in actions: md += ['## '+title,'',body,'']
md += ['## Sources','']+[f'- {a}: {b}' for a,b in sources]
outmd=ROOT/'docs/LAB-STOCK-PURCHASING-BRIEF.md'
outmd.write_text('\n'.join(md)+'\n',encoding='utf-8')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodySmall',fontName='Helvetica',fontSize=9,leading=12,spaceAfter=8))
styles.add(ParagraphStyle(name='CellSmall',fontName='Helvetica',fontSize=8,leading=10))
styles['Title'].textColor=colors.HexColor('#123850')
styles['Heading2'].textColor=colors.HexColor('#123850')
story=[]
def para(text,sty='BodySmall'): return Paragraph(escape(text),styles[sty])
def section(title,body): story.extend([para(title,'Heading2'),para(body)])
def table(group):
    data=[[para(t,'CellSmall') for t in ['Exact MPN / specification','Refs','Qty / PDB','Package','Buying class']]]
    for r in group:
        data.append([Paragraph(escape(r['mpn'])+'<br/><font color="#52616c">'+escape(description(r))+'</font>',styles['CellSmall']),para(r['refs'],'CellSmall'),para(r['qty'],'CellSmall'),para(r['package'],'CellSmall'),para(tier(r),'CellSmall')])
    t=Table(data,colWidths=[205,62,43,91,115],repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dceaf2')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f3f6f8')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
    story.append(t)
story.append(para('Lab stock + PDB purchasing brief','Title'))
for title,body in intro: section(title,body)
section('Three purchasing buckets','A: reusable passive stock candidates, pending cross-project demand. B: less-used or specification-sensitive passives in small machine-ready quantities. C: specialized components and manual-assembly parts for the selected prototype batch. HOLD: provisional fuse rating.')
section('What to ask for tomorrow','A budget for shared reel stock and a separate prototype-parts allowance, plus machine feeder details and an inventory of Ryan\'s books. The following pages provide every exact PDB order code without assuming a build count.')
story.append(PageBreak())
story.append(para('1 / Passive stock candidates','Title'))
story.append(para('All package sizes below are EIA. A-marked parts are candidates for lab stock, not confirmed common parts on the redesigned Osiris Rev B. Quote 250 / 1,000 custom-reel quantities versus one factory reel.'))
table(passives)
story.append(Spacer(1,10))
story.append(para('B-marked parts: purchase to the prototype batch formula. Do not replace precision divider values, timing dielectric, voltage ratings or package sizes to match an assortment book. Confirm complete manufacturer specifications at quotation, including the 2 M and 680 k resistor order codes.'))
story.append(PageBreak())
story.append(para('2 / Specialized PDB components','Title'))
story.append(para('Purchase in small quantities based on the agreed build count. For SMT, ask for continuous tape or a custom reel compatible with the machine. Through-hole connectors and holder require a separate assembly operation.'))
table(special)
story.append(Spacer(1,10))
story.append(para('The fuse holder is a separate purchased item. The 4 A fuse is a provisional selection: hold the final rating until the new Osiris load budget is approved. Protect the LTC4368 -1 variant, exact packages and specified manufacturer identities when quoting.'))
story.append(PageBreak())
story.append(para('3 / Turn the list into an order','Title'))
for title,body in actions: section(title,body)
story.append(para('Evidence and packaging references','Heading2'))
for title,body in sources: story.append(para(title+': '+body,'CellSmall'))
out=ROOT/'output/pdf/Lab-Stock-and-PDB-Purchasing-Brief.pdf'
out.parent.mkdir(parents=True,exist_ok=True)
def footer(c,d):
    c.setFont('Helvetica',8);c.setFillColor(colors.HexColor('#52616c'))
    c.drawString(48,25,'Osiris PDB | Purchasing discussion | 14 September 2026')
    c.drawRightString(564,25,str(d.page))
SimpleDocTemplate(str(out),pagesize=(612,792),rightMargin=48,leftMargin=48,topMargin=35,bottomMargin=42).build(story,onFirstPage=footer,onLaterPages=footer)
reader=PdfReader(out)
text='\n'.join(p.extract_text() for p in reader.pages)
for r in rows: assert r['mpn'] in text, r['mpn']
print(f'{len(reader.pages)} pages; all 27 exact MPNs present; 33 items/PDB. {out}')
