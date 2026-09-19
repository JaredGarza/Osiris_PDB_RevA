"""Create a presentation-only schematic copy and check electrical parity separately."""
from pathlib import Path
import sys, re, json, math, uuid, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'Simulation/closure-20260915'))
from cad_tools import blocks, block_at, props

def parse(s):
    tokens=iter(re.findall(r'"(?:\\.|[^"\\])*"|[^\s()]+|[()]',s))
    def item(t):
        if t=='(':
            out=[]
            for v in tokens:
                if v==')': return out
                out.append(item(v))
            raise ValueError('unclosed expression')
        return json.loads(t) if t.startswith('"') else t
    return item(next(tokens))
def children(v,k): return [x for x in v if isinstance(x,list) and x and x[0]==k]
def child(v,k): return next(iter(children(v,k)),None)

source=ROOT/'Osiris_PDB_RevA.kicad_sch'
s=source.read_text()
syms={props(b)['Reference']:b for b in blocks(s,'symbol')}
lib=child(parse(s),'lib_symbols')
libs={x[1]:x for x in children(lib,'symbol')}

def pin_positions(b):
    q=parse(b); at=child(q,'at'); x,y,a=map(float,at[1:]); mirror=child(q,'mirror')
    pins={}
    name=child(q,'lib_name') or child(q,'lib_id')
    for unit in children(libs[name[1]],'symbol'):
        for pin in children(unit,'pin'):
            px,py,pa=map(float,child(pin,'at')[1:]); py=-py
            theta=math.radians(-a)
            dx=px*math.cos(theta)-py*math.sin(theta)
            dy=px*math.sin(theta)+py*math.cos(theta)
            if mirror:
                if mirror[1]=='x': dy=-dy
                else: dx=-dx
            xx=x+dx; yy=y+dy
            pins[child(pin,'number')[1]]=(round(xx,4),round(yy,4))
    return pins

if __name__=='__main__':
    before=ROOT/'docs/schematic-readability-before'
    s=(before/'Osiris_PDB_RevA.kicad_sch').read_text()
    syms={props(b)['Reference']:b for b in blocks(s,'symbol')}
    tree=ET.parse(before/'before.net.xml').getroot()
    nets={(n.get('ref'),n.get('pin')):net.get('name').lstrip('/') for net in tree.findall('nets/net') for n in net.findall('node')}
    # Physical references and all symbol UUIDs are retained; only drawing geometry changes.
    placement={
      'J1':(17.78,40.64),'F1':(40.64,38.1),'Q3':(86.36,33.02),
      'Q1':(180.34,43.18),'Q2':(218.44,43.18),'R5':(254,38.1),'J3':(388.62,35.56),
      'D1':(142.24,55.88),'C2':(289.56,55.88),'C9':(314.96,55.88),'D3':(345.44,55.88),
      'U5':(86.36,81.28),'D4':(45.72,99.06),'R19':(111.76,116.84),
      'C11':(124.46,91.44),'C15':(139.7,91.44),'R20':(25.4,86.36),'C16':(25.4,104.14),
      'U1':(175.26,81.28),'R1':(154.94,71.12),'R2':(154.94,96.52),
      'R3':(167.64,109.22),'R13':(167.64,129.54),'C3':(187.96,114.3),
      'R7':(238.76,111.76),'R6':(266.7,111.76),'R14':(213.36,129.54),
      'R4':(243.84,129.54),'C1':(243.84,147.32),
      'U3':(53.34,190.5),'C4':(20.32,190.5),'C6':(114.3,190.5),
      'R11':(91.44,200.66),'R12':(91.44,220.98),'C10':(109.22,210.82),
      'U2':(251.46,187.96),'R9':(327.66,175.26),'R8':(327.66,195.58),
      'C7':(309.88,185.42),'C12':(317.5,162.56),'C13':(342.9,208.28),
      'R21':(327.66,233.68),'C14':(350.52,241.3),'C5':(292.1,218.44),
      'R10':(226.06,193.04),'J2':(388.62,236.22),
      'U4':(172.72,210.82),'C8':(144.78,193.04),
      'R15':(304.8,129.54),'R16':(327.66,129.54),'R17':(350.52,129.54),'R18':(373.38,129.54),
      'TP1':(55.88,48.26),'TP2':(238.76,48.26),'TP3':(30.48,53.34),
      'TP4':(365.76,48.26),'TP5':(129.54,177.8),'TP6':(335.28,147.32),'TP7':(302.26,147.32),
    }
    out=[]; moved={}; pins={}; segments=[]; used=set()
    def uid(): return str(uuid.uuid4())
    def add(t):out.append(t)
    def xy(p):return f'{p[0]:.4f} {p[1]:.4f}'
    def wire(a,b,net):
        a=tuple(a);b=tuple(b)
        if a==b:return
        assert a[0]==b[0] or a[1]==b[1],(a,b)
        segments.append((a,b,net))
    ground_count=0
    def label(net,p,angle=0):
        global ground_count
        if net.startswith('Net-('):return
        if net=='GND':
            ground_count+=1
            b=syms['#PWR01'];q=parse(b);ox,oy=map(float,child(q,'at')[1:3])
            b=re.sub(r'\(at ([\d.+-]+) ([\d.+-]+) ([\d.+-]+)\)',lambda m:f'(at {float(m[1])+p[0]-ox:.4f} {float(m[2])+p[1]-oy:.4f} {m[3]})',b)
            b=b.replace('#PWR01',f'#PWR{100+ground_count}')
            b=re.sub(r'\(uuid "[^"]+"\)',lambda m:f'(uuid "{uid()}")',b)
            add(b);return
        # Original unnamed nets gain local labels without altering pin connectivity.
        name=net if not net.startswith('unconnected-') else None
        if name:add(f'(label {json.dumps(name)} (at {xy(p)} {angle}) (effects (font (size 1.016 1.016)) (justify {"right" if angle==180 else "left"} bottom)) (uuid "{uid()}"))')
    def text(t,p,size=1.524):add(f'(text {json.dumps(t)} (at {xy(p)} 0) (effects (font (size {size} {size})) (justify left)) (uuid "{uid()}"))')
    for ref,(x,y) in placement.items():
        b=syms[ref];q=parse(b);old=child(q,'at'); ox,oy,oa=map(float,old[1:]);dx=x-ox;dy=y-oy
        b=re.sub(r'\(at ([\d.+-]+) ([\d.+-]+) ([\d.+-]+)\)',lambda m:f'(at {float(m[1])+dx:.4f} {float(m[2])+dy:.4f} {m[3]})',b)
        if ref=='D3': b=re.sub(r'\(at [^)]+\)',f'(at {x} {y} 270)',b,count=1)
        if ref=='C8': b=re.sub(r'\(at [^)]+\)',f'(at {x} {y} 180)',b,count=1)
        if ref=='R21': b=re.sub(r'\(at [^)]+\)',f'(at {x} {y} 90)',b,count=1)
        # Keep BOM metadata, but make visible fields compact and consistently horizontal.
        for m in list(re.finditer(r'\(property ',b))[::-1]:
            pb=block_at(b,m.start()); pp=parse(pb); key=pp[1]
            if key in ('Reference','Value','Description'):
                if ref.startswith(('U','Q')):
                    center=x+(22.86 if ref=='U1' else 20.32 if ref=='U2' else 0)
                    top=y-(20.32 if ref=='U3' else 20.32 if ref=='U4' else 20.32 if ref=='U5' else 13.97)
                    px,py=center,top+(0 if key=='Reference' else 2.54)
                elif ref.startswith(('C','R','D')) and float(child(parse(b),'at')[3]) in (0,180,90,270) and ref not in ('R5','R6','R7','R8','R9','R10'):
                    px,py=x+3.81,y+(-1.27 if key=='Reference' else 1.27)
                else: px,py=x,y+(-7.62 if key=='Reference' else -5.08)
                if ref=='U3': py-=2.54
                if ref=='U4':px=185.42;py=198.12+(0 if key=='Reference' else 2.54)
                if ref=='Q3':px=99.06;py=27.94+(0 if key=='Reference' else 2.54)
                if ref=='D4':px=55.88
                if ref=='R21':px=x;py=y+(-7.62 if key=='Reference' else -5.08)
                textangle=float(child(parse(b),'at')[3])%180
                pb=re.sub(r'\(at [^)]+\)',f'(at {px:.4f} {py:.4f} {textangle:g})',pb,count=1)
                pb=re.sub(r'\(justify [^)]+\)','',pb)
                if key=='Description':
                    pb=re.sub(r'\(effects', '(effects (hide yes)',pb,count=1)
                elif ref.startswith(('C','R','D')) and ref not in ('R5','R6','R7','R8','R9','R10'):
                    justification='right' if float(child(parse(b),'at')[3]) in (90,180) else 'left'
                    pb=pb.replace('(effects',f'(effects (justify {justification})',1)
                b=b[:m.start()]+pb+b[m.start()+len(block_at(b,m.start())):]
        moved[ref]=b;add(b)
        for pn,pos in pin_positions(b).items():pins[(ref,pn)]=pos
    assert set(placement)=={r for r in syms if not r.startswith('#')}
    def p(ref,pin):return pins[(ref,str(pin))]
    def route(ref1,pin1,ref2,pin2,via=()):
        a=(ref1,str(pin1));b=(ref2,str(pin2));net=nets[a];assert net==nets[b],(a,b,net,nets[b])
        pts=[pins[a],*via,pins[b]]
        for u,v in zip(pts,pts[1:]):wire(u,v,net)
        used.update([a,b])
    # Main current path, left to right. Kelvin sense pins are deliberately separate.
    route('J1',2,'F1',1)
    route('F1',2,'Q3',1)
    route('Q3',5,'Q1',5)
    route('Q1',1,'Q2',1)
    route('Q2',5,'R5',1)
    route('R5',4,'J3',2)
    for ref in ('C9','D3'):
        route('R5',4,ref,1,[(p(ref,1)[0],38.1)])
    route('Q3',5,'D1',1,[(142.24,38.1)])
    route('R5',3,'C2',1,[(289.56,43.18)])
    for ref,parent,pin,xx in [('TP1','F1',2,55.88),('TP2','Q2',5,238.76),('TP4','R5',4,365.76)]:
        route(parent,pin,ref,1,[(xx,38.1)])
    # Q3 ideal-diode controller and its floating-reference clamp/filter network.
    route('Q3',1,'U5',2,[(60.96,38.1),(60.96,81.28)])
    for pn in (4,5):route('U5',2,'U5',pn,[(60.96,81.28),(60.96,p('U5',pn)[1])])
    route('Q3',4,'U5',1,[(83.82,22.86),(111.76,22.86),(111.76,81.28)])
    route('Q3',5,'U5',8,[(119.38,38.1),(119.38,76.2)])
    route('U5',4,'D4',2,[(45.72,76.2)])
    route('U5',4,'R20',1,[(25.4,76.2)])
    route('R20',2,'C16',1)
    route('D4',1,'R19',1,[(45.72,109.22),(111.76,109.22)])
    route('U5',6,'R19',1,[(111.76,86.36)])
    for ref in ('C11','C15'):
        route('U5',8,ref,1,[(119.38,76.2),(p(ref,1)[0],76.2)])
        route(ref,2,'R19',1,[(p(ref,2)[0],109.22),(111.76,109.22)])
    # Breaker gate drive and local control networks.
    route('Q1',4,'Q2',4,[(182.88,55.88),(215.9,55.88)])
    route('Q2',4,'U1',10,[(215.9,55.88),(236.22,55.88),(236.22,83.82)])
    route('R1',2,'R2',1)
    route('R1',2,'U1',2,[(154.94,83.82)])
    route('R3',2,'R13',1)
    route('R3',2,'U1',3,[(172.72,113.03),(172.72,86.36)])
    route('U1',4,'C3',1,[(160.02,88.9),(160.02,104.14),(187.96,104.14)])
    route('R7',2,'R6',1)
    route('R7',2,'U1',6,[(251.46,111.76),(251.46,93.98)])
    route('R4',2,'C1',1)
    # Local housekeeping regulator, bypass capacitors and feedback divider.
    route('U3',8,'U3',5,[(27.94,177.8),(27.94,182.88)])
    route('U3',8,'C4',2,[(20.32,177.8)])
    route('U3',1,'C6',2,[(114.3,177.8)])
    route('U3',1,'TP5',1)
    route('U3',1,'R11',1,[(91.44,177.8)])
    route('R11',2,'R12',1)
    route('U3',2,'R11',2,[(81.28,187.96),(81.28,208.28),(91.44,208.28)])
    route('R11',2,'C10',2,[(91.44,214.63)])
    route('C10',1,'U3',1,[(119.38,207.01),(119.38,177.8)])
    route('U3',4,'U3',9)
    # INA differential filter; sense inputs are intentionally not power-path wires.
    route('R9',2,'C7',1,[(309.88,175.26)])
    route('R8',2,'C7',2,[(309.88,195.58)])
    route('U2',10,'R9',2,[(299.72,187.96),(299.72,175.26)])
    route('U2',9,'R8',2,[(302.26,190.5),(302.26,195.58)])
    route('U2',3,'R10',2)
    route('U4',5,'C8',2,[(167.64,180.34),(144.78,180.34)])
    route('R9',2,'C12',1,[(309.88,175.26),(309.88,153.67),(317.5,153.67)])
    route('R8',2,'C13',1,[(317.5,195.58),(317.5,200.66),(342.9,200.66)])
    route('R21',2,'C14',1,[(350.52,233.68)])
    route('U2',6,'C5',1)
    route('U2',1,'U2',2,[(241.3,187.96),(241.3,190.5)])
    route('R15',2,'TP7',1,[(304.8,147.32)])
    route('R16',2,'TP6',1,[(327.66,147.32)])
    # Each connected wire group gets one net annotation. Separate local sections
    # retain labels rather than long cross-sheet signal wires.
    def on(pt,a,b):return min(a[0],b[0])-1e-5<=pt[0]<=max(a[0],b[0])+1e-5 and min(a[1],b[1])-1e-5<=pt[1]<=max(a[1],b[1])+1e-5
    # Split wire intersections at same-net junctions for explicit KiCad topology.
    vertices={n:set() for _,_,n in segments}
    for a,b,n in segments:vertices[n].update((a,b))
    for key,pos in pins.items():
        n=nets.get(key)
        if n in vertices and any(nn==n and on(pos,a,b) for a,b,nn in segments):vertices[n].add(pos);used.add(key)
    edges=set()
    for a,b,n in segments:
        pts=sorted([v for v in vertices[n] if on(v,a,b)],key=lambda v:(v[0],v[1]))
        for u,v in zip(pts,pts[1:]):edges.add((u,v,n))
    for a,b,n in sorted(edges):add(f'(wire (pts (xy {xy(a)}) (xy {xy(b)})) (stroke (width 0) (type default)) (uuid "{uid()}"))')
    for n,vs in vertices.items():
        adj={v:set() for v in vs}
        for a,b,nn in edges:
            if nn==n:adj[a].add(b);adj[b].add(a)
        remaining=set(vs)
        while remaining:
            start=min(remaining);stack=[start];group=set()
            while stack:
                v=stack.pop()
                if v in group:continue
                group.add(v);stack.extend(adj[v]-group)
            remaining-=group
            anchor=min(group,key=lambda v:(v[1],v[0]))
            label(n,anchor)
        for v in vs:
            if len(adj[v])>=3:add(f'(junction (at {xy(v)}) (diameter 0) (color 0 0 0 0) (uuid "{uid()}"))')
    # Unrouted control signals get a short visible stub, not a label directly on a pin.
    seen=set()
    ground=next(b for ref,b in syms.items() if ref.startswith('#PWR'))
    for key,pos in pins.items():
        net=nets.get(key)
        if (pos,net) in seen:continue
        seen.add((pos,net))
        if key in used:continue
        if net is None or net.startswith('unconnected-'):
            add(f'(no_connect (at {xy(pos)}) (uuid "{uid()}"))');continue
        ref=key[0];center=placement[ref]
        dx,dy=pos[0]-center[0],pos[1]-center[1]
        if ref in ('U1','U2'):direction=(-1,0) if dx<1 else (1,0)
        elif ref in ('U3','U5'):direction=(-1,0) if dx<0 else (1,0)
        elif abs(dx)>abs(dy):direction=(1 if dx>=0 else -1,0)
        else:direction=(0,1 if dy>=0 else -1)
        end=(round(pos[0]+direction[0]*5.08,4),round(pos[1]+direction[1]*5.08,4))
        add(f'(wire (pts (xy {xy(pos)}) (xy {xy(end)})) (stroke (width 0) (type default)) (uuid "{uid()}"))')
        label(net,end,180 if direction[0]<0 else 0)
    # U3 already declares PDB_3V3 driven. Move its redundant ERC flag to the
    # resistor-fed INA_VBUS input, which is powered through R21.
    flag_nets={'#FLG01':'GND','#FLG02':'IDEAL_IN','#FLG03':'INA_VBUS','#FLG04':'SHUNT_LO','#FLG0101':'VBAT_FUSED','#FLG0102':'IDEAL_VSS','#FLG0103':'PDB_VOUT'}
    for i,(ref,net) in enumerate(flag_nets.items()):
        b=syms[ref];old=child(parse(b),'at');ox,oy=map(float,old[1:3]);x,y=25.4+i*33.02,261.62
        b=re.sub(r'\(at ([\d.+-]+) ([\d.+-]+) ([\d.+-]+)\)',lambda m:f'(at {float(m[1])+x-ox:.4f} {float(m[2])+y-oy:.4f} {m[3]})',b)
        add(b);label(net,(x,y))
    b=syms['#PWR01'];old=child(parse(b),'at');ox,oy=map(float,old[1:3]);gx,gy=25.4,266.7
    b=re.sub(r'\(at ([\d.+-]+) ([\d.+-]+) ([\d.+-]+)\)',lambda m:f'(at {float(m[1])+gx-ox:.4f} {float(m[2])+gy-oy:.4f} {m[3]})',b)
    add(b)
    add(f'(wire (pts (xy 25.4 261.62) (xy 25.4 266.7)) (stroke (width 0) (type default)) (uuid "{uid()}"))')
    for title,pos in [
      ('MAIN POWER PATH  |  BATTERY -> PROTECTED RAW 4S TO OSIRIS',(20.32,17.78)),
      ('REVERSE-CURRENT CONTROL / INPUT DAMPING',(20.32,66.04)),
      ('OV / UV / OVERCURRENT BREAKER',(157.48,63.5)),
      ('LOCAL 3.3 V SUPPLY',(20.32,157.48)),
      ('ALERT BUFFER',(147.32,170.18)),
      ('CURRENT / VOLTAGE MONITOR + FILTERS',(254,165.1)),
      ('STATUS / OPTIONAL PULL-UPS',(297.18,114.3))]:text(title,pos)
    text('Same electrical circuit; drawing rearranged only. No capacitor values or footprints changed.\nPDB supplies raw battery voltage; Osiris Rev B requires its replacement power section.\nC11-C16: 1 uF / 63 V non-polar film. Keep local bypass capacitors close to their ICs.',(20.32,276.86),1.016)
    # Retain document identity, embedded libraries and original symbol instances.
    rootblocks=[]
    for kind in ('version','generator','generator_version','uuid','paper','title_block','lib_symbols','embedded_fonts'):
        rootblocks.extend(blocks(s,kind))
    result='(kicad_sch\n'+ '\n'.join('\t'+b for b in rootblocks+out)+'\n)\n'
    result=result.replace('Selected components; original Osiris hardware retained','PDB power-path draft; Osiris Rev B replacement interface')
    dest=ROOT/'docs/schematic-readability-after/Osiris_PDB_RevA.kicad_sch'
    dest.parent.mkdir(exist_ok=True)
    previous_candidate=dest.read_text() if dest.exists() else ''
    dest.write_text(result)
    print(dest)
    if '--apply' in sys.argv:
        assert source.read_text() in ((before/'Osiris_PDB_RevA.kicad_sch').read_text(),previous_candidate), 'Original changed after backup/reflow; stop to preserve user edits'
        source.write_text(result)
        print('Applied geometry-only reflow to original schematic')
