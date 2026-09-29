"""Place the provisional high-current ESC branch without adding routing.

This intentionally preserves all existing tracks, zones, mounting holes, and
avionics footprint positions.  J1 and J3 are replaced by the provisional
high-current terminal footprint and moved onto a new top-side power shelf.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pcbnew


MM = pcbnew.FromMM
ROOT = Path(__file__).resolve().parents[1]
LOCAL_LIB = ROOT / "Libraries" / "PDB_Footprints.pretty"
KICAD_LIB = Path(r"C:\Program Files\KiCad\10.0\share\kicad\footprints")


SYMBOL_PATHS = {
    "J1": "/d7a6f7f7-e189-4d31-add5-350b6906ff4c",
    "J3": "/74dbfffc-d519-4ff9-9d7b-ca3bef50bdd7",
    "F2": "/022b7ac5-f65d-4ffb-97ca-eeedfb3cf934",
    "D5": "/e7c6d47c-055b-49e1-8ae5-bfe5883643aa",
    "C17": "/3c337106-31a5-47eb-bc8a-69daee2ad90e",
    "C18": "/0a696b28-fb1c-4810-815e-b7d50f412b5c",
    "C19": "/e9b97c4b-c6d3-473a-be7e-d35121fd6261",
}


def v(x_mm: float, y_mm: float) -> pcbnew.VECTOR2I:
    return pcbnew.VECTOR2I(MM(x_mm), MM(y_mm))


def load_footprint(library: Path, name: str) -> pcbnew.FOOTPRINT:
    fp = pcbnew.FootprintLoad(str(library), name)
    if fp is None:
        raise RuntimeError(f"Unable to load footprint {library}:{name}")
    return fp


def ensure_net(board: pcbnew.BOARD, name: str) -> pcbnew.NETINFO_ITEM:
    net = board.FindNet(name)
    if net is None:
        net = pcbnew.NETINFO_ITEM(board, name)
        board.Add(net)
    return net


def set_pad_nets(fp: pcbnew.FOOTPRINT, mapping: dict[str, pcbnew.NETINFO_ITEM]) -> None:
    for pad in fp.Pads():
        number = pad.GetNumber()
        if number not in mapping:
            raise RuntimeError(f"No net mapping for {fp.GetReference()} pad {number}")
        pad.SetNet(mapping[number])


def add_footprint(
    board: pcbnew.BOARD,
    fp: pcbnew.FOOTPRINT,
    reference: str,
    value: str,
    x_mm: float,
    y_mm: float,
    rotation_deg: float,
    nets: dict[str, pcbnew.NETINFO_ITEM],
) -> None:
    # Iterate pads before passing other SWIG-owned temporary objects into the
    # footprint.  KiCad 10's Python bindings can otherwise lose the PADS
    # iterator wrapper after SetPosition/SetPath.
    set_pad_nets(fp, nets)
    fp.SetReference(reference)
    fp.SetValue(value)
    fp.SetPosition(v(x_mm, y_mm))
    fp.SetOrientationDegrees(rotation_deg)
    fp.SetPath(pcbnew.KIID_PATH(SYMBOL_PATHS[reference]))


def replace_outline_with_power_shelf(board: pcbnew.BOARD) -> None:
    edge_shapes = [d for d in board.GetDrawings() if d.GetLayer() == pcbnew.Edge_Cuts]
    if len(edge_shapes) != 1 or edge_shapes[0].GetShape() != pcbnew.SHAPE_T_POLY:
        raise RuntimeError("Expected one polygonal Edge.Cuts outline")

    points_mm = [
        (13.00, 39.00),
        (13.00, -19.75),
        (139.00, -19.75),
        (139.00, 56.25),
        (95.75, 63.50),
        (44.50, 63.50),
    ]
    chain = pcbnew.SHAPE_LINE_CHAIN()
    for x_mm, y_mm in points_mm:
        chain.Append(v(x_mm, y_mm))
    chain.SetClosed(True)
    poly = pcbnew.SHAPE_POLY_SET()
    poly.AddOutline(chain)
    edge_shapes[0].SetPolyShape(poly)


def place(input_board: Path, output_board: Path) -> None:
    # Load every library item before mutating the board; this avoids a KiCad
    # 10 SWIG lifetime issue in which the footprint I/O plugin can be released
    # after other owned objects are removed.
    terminal_name = "MKDSP25_2_15mm_PROVISIONAL"
    j1_fp = load_footprint(LOCAL_LIB, terminal_name)
    j3_fp = load_footprint(LOCAL_LIB, terminal_name)
    f2_fp = load_footprint(LOCAL_LIB, "SCHURTER_UHS_8.4x9.4mm_PROVISIONAL")
    d5_fp = load_footprint(KICAD_LIB / "Diode_SMD.pretty", "D_SMB")
    c17_fp = load_footprint(KICAD_LIB / "Capacitor_SMD.pretty", "CP_Elec_10x10.5")
    c18_fp = load_footprint(KICAD_LIB / "Capacitor_SMD.pretty", "C_0805_2012Metric")
    c19_fp = load_footprint(KICAD_LIB / "Capacitor_SMD.pretty", "C_0805_2012Metric")

    board = pcbnew.LoadBoard(str(input_board))

    # Only the two power connectors are deliberately relocated.  The other
    # references are removed here solely to make repeated runs idempotent.
    replaced = {"J1", "J3", "F2", "D5", "C17", "C18", "C19"}
    old_footprints = [fp for fp in list(board.GetFootprints()) if fp.GetReference() in replaced]

    replace_outline_with_power_shelf(board)

    gnd = ensure_net(board, "GND")
    vbat_raw = ensure_net(board, "/VBAT_RAW")
    esc_vbat = ensure_net(board, "/ESC_VBAT")

    add_footprint(
        board,
        j1_fp,
        "J1",
        "Phoenix 1932588 125A PROVISIONAL",
        29.0,
        -3.0,
        0.0,
        {"1": gnd, "2": vbat_raw},
    )
    add_footprint(
        board,
        j3_fp,
        "J3",
        "Phoenix 1932588 125A PROVISIONAL",
        123.0,
        -3.0,
        180.0,
        {"1": gnd, "2": esc_vbat},
    )

    add_footprint(
        board,
        f2_fp,
        "F2",
        "SCHURTER UHS 100A 3-140-177 PROVISIONAL",
        51.0,
        -3.0,
        0.0,
        {"1": vbat_raw, "2": esc_vbat},
    )
    add_footprint(
        board,
        d5_fp,
        "D5",
        "SMBJ24CA",
        88.0,
        -3.0,
        0.0,
        {"1": esc_vbat, "2": gnd},
    )
    add_footprint(
        board,
        c17_fp,
        "C17",
        "470u 35V LOW-ESR",
        100.0,
        -3.0,
        0.0,
        {"1": esc_vbat, "2": gnd},
    )
    add_footprint(
        board,
        c18_fp,
        "C18",
        "1u 50V X7R",
        95.0,
        5.0,
        0.0,
        {"1": esc_vbat, "2": gnd},
    )
    add_footprint(
        board,
        c19_fp,
        "C19",
        "100n 50V X7R",
        101.0,
        5.0,
        0.0,
        {"1": esc_vbat, "2": gnd},
    )

    for fp in [j1_fp, j3_fp, f2_fp, d5_fp, c17_fp, c18_fp, c19_fp]:
        board.Add(fp)
    for fp in old_footprints:
        board.Remove(fp)

    board.SetFileName(str(output_board))
    if not pcbnew.SaveBoard(str(output_board), board):
        raise RuntimeError(f"Failed to save {output_board}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    place(args.input.resolve(), args.output.resolve())


if __name__ == "__main__":
    main()
