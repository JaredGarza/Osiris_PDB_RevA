from pathlib import Path

import pcbnew


ROOT = Path(__file__).resolve().parent
KICAD_FP = Path(r"C:\Program Files\KiCad\10.0\share\kicad\footprints")
PROJECT_FP = ROOT / "Libraries" / "PDB_Footprints.pretty"
OUT = ROOT / "Osiris_PDB_RevA.kicad_pcb"


def mm(value):
    return pcbnew.FromMM(value)


def point(x, y):
    return pcbnew.VECTOR2I(mm(x), mm(y))


def load_footprint(library, name):
    fp = pcbnew.FootprintLoad(str(library), name)
    if fp is None:
        raise RuntimeError(f"Could not load footprint {library}:{name}")
    return fp


def add_footprint(board, library, name, ref, value, x, y, angle=0):
    fp = load_footprint(library, name)
    fp.SetReference(ref)
    fp.SetValue(value)
    fp.SetPosition(point(x, y))
    fp.SetOrientationDegrees(angle)
    fp.Reference().SetVisible(True)
    fp.Reference().SetLayer(pcbnew.F_Fab)
    fp.Value().SetVisible(False)
    fp.Reference().SetTextSize(point(1.0, 1.0))
    fp.Reference().SetTextThickness(mm(0.15))
    board.Add(fp)
    return fp


def assign(fp, pin_nets):
    for pad in fp.Pads():
        pin = pad.GetNumber()
        if pin in pin_nets:
            pad.SetNet(pin_nets[pin])


def add_track(board, net, x1, y1, x2, y2, width, layer=pcbnew.F_Cu):
    track = pcbnew.PCB_TRACK(board)
    track.SetStart(point(x1, y1))
    track.SetEnd(point(x2, y2))
    track.SetWidth(mm(width))
    track.SetLayer(layer)
    track.SetNet(net)
    board.Add(track)
    return track


def add_via(board, net, x, y, diameter=1.2, drill=0.6):
    via = pcbnew.PCB_VIA(board)
    via.SetPosition(point(x, y))
    via.SetWidth(mm(diameter))
    via.SetDrill(mm(drill))
    via.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
    via.SetNet(net)
    board.Add(via)
    return via


def add_shape(board, x1, y1, x2, y2, layer, width=0.1):
    shape = pcbnew.PCB_SHAPE(board)
    shape.SetShape(pcbnew.SHAPE_T_SEGMENT)
    shape.SetStart(point(x1, y1))
    shape.SetEnd(point(x2, y2))
    shape.SetWidth(mm(width))
    shape.SetLayer(layer)
    board.Add(shape)


def add_rect(board, x1, y1, x2, y2, layer, width=0.1):
    add_shape(board, x1, y1, x2, y1, layer, width)
    add_shape(board, x2, y1, x2, y2, layer, width)
    add_shape(board, x2, y2, x1, y2, layer, width)
    add_shape(board, x1, y2, x1, y1, layer, width)


def add_text(board, text, x, y, layer=pcbnew.F_SilkS, size=1.0, thickness=0.15,
             angle=0, justify=None):
    item = pcbnew.PCB_TEXT(board)
    item.SetText(text)
    item.SetPosition(point(x, y))
    item.SetLayer(layer)
    item.SetTextSize(point(size, size))
    item.SetTextThickness(mm(thickness))
    item.SetTextAngleDegrees(angle)
    if layer in (pcbnew.B_SilkS, pcbnew.B_Fab, pcbnew.B_Cu):
        item.SetMirrored(True)
    if justify is not None:
        item.SetHorizJustify(justify)
    board.Add(item)
    return item


def add_zone(board, net, layer, name):
    zone = pcbnew.ZONE(board)
    zone.SetLayer(layer)
    zone.SetNet(net)
    zone.SetZoneName(name)
    zone.SetLocalClearance(mm(0.50))
    zone.SetMinThickness(mm(0.25))
    zone.SetPadConnection(pcbnew.ZONE_CONNECTION_FULL)
    outline = zone.Outline()
    outline.NewOutline()
    for x, y in ((100.75, 100.75), (154.25, 100.75),
                 (154.25, 154.25), (100.75, 154.25)):
        outline.Append(point(x, y))
    board.Add(zone)
    return zone


def main():
    board = pcbnew.BOARD()
    board.SetCopperLayerCount(4)
    design = board.GetDesignSettings()
    design.SetBoardThickness(mm(1.6))
    design.m_CopperEdgeClearance = mm(0.50)
    design.m_HoleClearance = mm(0.30)
    design.m_MinClearance = mm(0.25)

    title = board.GetTitleBlock()
    title.SetTitle("Osiris 4S PDB - four external ESC outputs")
    title.SetDate("2026-09-03")
    title.SetRevision("A-PROTOTYPE")
    title.SetCompany("Osiris UAV")
    title.SetComment(0, "4 layers; fabrication requirement: 2 oz copper on every layer")
    title.SetComment(1, "55 x 55 mm; 30.5 mm square M3 mounting pattern")
    title.SetComment(2, "Prototype only: staged load and transient qualification required")

    nets = {}
    for name in ("GND", "VBAT", "OSIRIS_FUSED"):
        net = pcbnew.NETINFO_ITEM(board, name)
        board.Add(net)
        nets[name] = net

    # Board edge and mounting pattern.
    add_rect(board, 100, 100, 155, 155, pcbnew.Edge_Cuts, 0.10)
    holes = ((112.25, 112.25), (142.75, 112.25),
             (112.25, 142.75), (142.75, 142.75))
    for index, (x, y) in enumerate(holes, start=1):
        add_footprint(board, KICAD_FP / "MountingHole.pretty", "MountingHole_3.2mm_M3",
                      f"H{index}", "M3", x, y)

    # Cable solder pads: pin 1 is positive, pin 2 is ground.
    j1 = add_footprint(board, KICAD_FP / "Connector_Wire.pretty",
                       "SolderWire-4sqmm_1x02_P12mm_D3mm_OD6mm",
                       "J1", "BATTERY_IN_4S", 121.5, 149.0)
    j2 = add_footprint(board, KICAD_FP / "Connector_Wire.pretty",
                       "SolderWire-4sqmm_1x02_P12mm_D3mm_OD6mm",
                       "J2", "ESC1_OUT", 104.0, 107.0, 270)
    j3 = add_footprint(board, KICAD_FP / "Connector_Wire.pretty",
                       "SolderWire-4sqmm_1x02_P12mm_D3mm_OD6mm",
                       "J3", "ESC2_OUT", 104.0, 135.0, 270)
    j4 = add_footprint(board, KICAD_FP / "Connector_Wire.pretty",
                       "SolderWire-4sqmm_1x02_P12mm_D3mm_OD6mm",
                       "J4", "ESC3_OUT", 151.0, 107.0, 270)
    j5 = add_footprint(board, KICAD_FP / "Connector_Wire.pretty",
                       "SolderWire-4sqmm_1x02_P12mm_D3mm_OD6mm",
                       "J5", "ESC4_OUT", 151.0, 135.0, 270)
    j6 = add_footprint(board, KICAD_FP / "Connector_Wire.pretty",
                       "SolderWire-2sqmm_1x02_P7.8mm_D2mm_OD3.9mm",
                       "J6", "OSIRIS_OUT_XT60_M_PIGTAIL", 123.6, 104.0)
    for fp in (j1, j2, j3, j4, j5):
        assign(fp, {"1": nets["VBAT"], "2": nets["GND"]})
    assign(j6, {"1": nets["OSIRIS_FUSED"], "2": nets["GND"]})

    # Main-bus transient suppression at the battery entry.
    c1 = add_footprint(board, KICAD_FP / "Capacitor_THT.pretty",
                       "CP_Radial_D12.5mm_P5.00mm", "C1",
                       "1000uF 35V LOW-ESR", 121.5, 138.0)
    d1 = add_footprint(board, KICAD_FP / "Diode_SMD.pretty", "D_SMC",
                       "D1", "SMCJ17CA", 135.0, 139.0, 90)
    c2 = add_footprint(board, KICAD_FP / "Capacitor_SMD.pretty", "C_0805_2012Metric",
                       "C2", "100nF 50V X7R", 136.5, 130.0, 90)
    for fp in (c1, d1, c2):
        assign(fp, {"1": nets["VBAT"], "2": nets["GND"]})

    # Fused branch to the Osiris J15 pigtail.
    f1 = add_footprint(board, PROJECT_FP, "FUSC9830X318N", "F1",
                       "0678H6300-02 6.3A", 127.65, 111.5, 180)
    assign(f1, {"1": nets["VBAT"], "2": nets["OSIRIS_FUSED"]})
    d2 = add_footprint(board, KICAD_FP / "Diode_SMD.pretty", "D_SMC",
                       "D2", "SMCJ17CA", 127.0, 117.0)
    c3 = add_footprint(board, KICAD_FP / "Capacitor_SMD.pretty", "C_0805_2012Metric",
                       "C3", "1uF 50V X7R", 127.0, 122.0)
    c4 = add_footprint(board, KICAD_FP / "Capacitor_SMD.pretty", "C_0805_2012Metric",
                       "C4", "100nF 50V X7R", 127.0, 125.0)
    c5 = add_footprint(board, KICAD_FP / "Capacitor_THT.pretty",
                       "CP_Radial_D8.0mm_P3.50mm", "C5", "100uF 35V DNP",
                       118.0, 127.5, 180)
    for fp in (d2, c3, c4, c5):
        assign(fp, {"1": nets["OSIRIS_FUSED"], "2": nets["GND"]})

    # Short fused-branch spine and local branches.
    add_track(board, nets["OSIRIS_FUSED"], 123.6, 104.0, 123.6, 127.5, 3.0)
    add_track(board, nets["OSIRIS_FUSED"], 123.6, 122.0, 126.05, 122.0, 1.5)
    add_track(board, nets["OSIRIS_FUSED"], 123.6, 125.0, 126.05, 125.0, 1.5)
    add_track(board, nets["OSIRIS_FUSED"], 118.0, 127.5, 123.6, 127.5, 2.0)

    # Ground drops for top-side SMD suppression parts. Multiple vias at each
    # TVS keep the transient loop inductance low.
    ground_drops = [
        ((135.0, 135.6), [(132.7, 133.8), (135.0, 133.2), (137.3, 133.8)]),
        ((136.5, 129.05), [(138.5, 129.05)]),
        ((130.4, 117.0), [(133.0, 115.8), (133.0, 118.2)]),
        ((127.95, 122.0), [(130.5, 122.0)]),
        ((127.95, 125.0), [(130.5, 125.0)]),
    ]
    for (px, py), via_points in ground_drops:
        for vx, vy in via_points:
            add_track(board, nets["GND"], px, py, vx, vy, 1.0)
            add_via(board, nets["GND"], vx, vy)

    # Four high-current planes: two positive layers and two return layers.
    add_zone(board, nets["VBAT"], pcbnew.F_Cu, "VBAT_TOP")
    add_zone(board, nets["VBAT"], pcbnew.In1_Cu, "VBAT_INNER1")
    add_zone(board, nets["GND"], pcbnew.In2_Cu, "GND_INNER2")
    add_zone(board, nets["GND"], pcbnew.B_Cu, "GND_BOTTOM")

    # Assembly and safety markings.
    add_text(board, "OSIRIS PDB REV A", 127.5, 153.8, size=1.2)
    add_text(board, "4S ONLY", 108.0, 102.0, size=0.9)
    add_text(board, "ESC 1", 109.0, 113.0, angle=90)
    add_text(board, "ESC 2", 109.0, 141.0, angle=90)
    add_text(board, "ESC 3", 146.0, 113.0, angle=90)
    add_text(board, "ESC 4", 146.0, 141.0, angle=90)
    add_text(board, "OSIRIS", 144.0, 102.0, size=0.9)
    add_text(board, "+", 121.5, 145.0, size=1.5)
    add_text(board, "-", 133.5, 145.0, size=1.5)
    # A simple component-zone box on documentation layer aids assembly review.
    add_rect(board, 110.5, 108.5, 136.5, 132.0, pcbnew.Cmts_User, 0.15)
    add_text(board, "SUPPRESSION / OSIRIS BRANCH", 123.5, 131.0,
             layer=pcbnew.Cmts_User, size=0.8)
    add_text(board, "FAB: 4 LAYERS, 2 OZ COPPER EACH", 127.5, 134.0,
             layer=pcbnew.Cmts_User, size=0.8)

    board.BuildListOfNets()
    pcbnew.ZONE_FILLER(board).Fill(board.Zones())
    pcbnew.SaveBoard(str(OUT), board)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
