"""Build an unrouted, compact Phoenix-terminal placement study.

Run with KiCad 10's bundled Python. The source is the historical placement
preview, so the active routed board is not overwritten by an unqualified
high-current layout.
"""

from pathlib import Path

import pcbnew as pcb


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tmp" / "Osiris_PDB_RevA-placement-preview.kicad_pcb"
DESTINATION = (
    ROOT / "design-studies" / "phoenix-through-pdb" / "Osiris_PDB_RevA.kicad_pcb"
)


def at(x_mm, y_mm):
    return pcb.VECTOR2I(pcb.FromMM(x_mm), pcb.FromMM(y_mm))


board = pcb.LoadBoard(str(SOURCE))
footprints = {item.GetReference(): item for item in board.GetFootprints()}

# A 4S pack's XT60 mates to a short XT60-to-wire harness at J1. The same
# high-current board corridor connects J1 to F2 and J3. The XT60 pair at the
# battery remains an unqualified current limit and is not represented as a
# higher-rated component by these PCB footprints.
placement = {
    "J1": (42.0, -4.0, 0),
    "F2": (65.0, -4.0, 0),
    "J3": (88.0, -4.0, 180),
    "C17": (80.0, -27.0, 0),
    "D5": (94.0, -27.0, 0),
    "C18": (61.0, -27.0, 0),
    "C19": (68.0, -27.0, 0),
}
for reference, (x_mm, y_mm, angle) in placement.items():
    item = footprints[reference]
    item.SetPosition(at(x_mm, y_mm))
    item.SetOrientationDegrees(angle)

for reference in ("J1", "J3"):
    footprints[reference].SetValue("MKDSP 25/2-15.00 PROVISIONAL")

# Retain the lower avionics region and four frame-hole positions. The taller
# top shelf accommodates the two 30 x 31 mm Phoenix bodies and a capacitor
# row without putting those bodies over H1/H2. It has no asserted frame fit.
outline = [
    (13.75, 39.0),
    (13.75, 21.75),
    (25.0, 21.75),
    (25.0, -35.0),
    (105.0, -35.0),
    (105.0, 21.75),
    (108.25, 23.5),
    (108.25, 56.25),
    (95.75, 63.5),
    (44.5, 63.5),
]
shape = pcb.SHAPE_POLY_SET()
shape.NewOutline()
for x_mm, y_mm in outline:
    shape.Append(at(x_mm, y_mm))
edges = [item for item in board.GetDrawings() if item.GetLayer() == pcb.Edge_Cuts]
assert len(edges) == 1 and edges[0].GetShapeStr() == "Polygon"
edges[0].SetPolyShape(shape)

DESTINATION.parent.mkdir(parents=True, exist_ok=True)
pcb.SaveBoard(str(DESTINATION), board)
print(DESTINATION)
