from copy import deepcopy
from pathlib import Path
from uuid import uuid4

from kiutils.schematic import (
    Effects,
    HierarchicalSheetInstance,
    LocalLabel,
    Position,
    Property,
    Schematic,
    SchematicSymbol,
    SymbolProjectInstance,
    SymbolProjectPath,
    Text,
    TitleBlock,
)
from kiutils.items.common import Font
from kiutils.symbol import SymbolLib


ROOT = Path(__file__).resolve().parent
DEVICE_LIB = Path(r"C:\Program Files\KiCad\10.0\share\kicad\symbols\Device.kicad_sym")
CONNECTOR_LIB = Path(r"C:\Program Files\KiCad\10.0\share\kicad\symbols\Connector_Generic.kicad_sym")


def uid():
    return str(uuid4())


def hidden_effects():
    return Effects(font=Font(height=1.0, width=1.0), hide=True)


def visible_effects():
    return Effects(font=Font(height=1.27, width=1.27))


def add_embedded_symbol(schematic, library_path, entry_name, nickname):
    library = SymbolLib().from_file(str(library_path))
    symbol = deepcopy(next(item for item in library.symbols if item.libId == entry_name))
    symbol.libId = f"{nickname}:{entry_name}"
    schematic.libSymbols.append(symbol)


def symbol_properties(ref, value, footprint, datasheet, x, y):
    return [
        Property("Reference", ref, position=Position(x, y - 3.0, 0), effects=visible_effects()),
        Property("Value", value, position=Position(x, y + 3.0, 0), effects=visible_effects()),
        Property("Footprint", footprint, position=Position(x, y, 0), effects=hidden_effects()),
        Property("Datasheet", datasheet, position=Position(x, y, 0), effects=hidden_effects()),
        Property("Description", value, position=Position(x, y, 0), effects=hidden_effects()),
    ]


def add_symbol(schematic, root_uuid, nickname, entry_name, ref, value, footprint,
               datasheet, x, y, angle, pin_numbers, dnp=False):
    symbol_uuid = uid()
    pins = {number: uid() for number in pin_numbers}
    symbol = SchematicSymbol(
        libraryNickname=nickname,
        entryName=entry_name,
        position=Position(x, y, angle),
        unit=1,
        inBom=True,
        onBoard=True,
        dnp=dnp,
        uuid=symbol_uuid,
        properties=symbol_properties(ref, value, footprint, datasheet, x, y),
        pins=pins,
        instances=[
            SymbolProjectInstance(
                name="Osiris_PDB_RevA",
                paths=[SymbolProjectPath(f"/{root_uuid}", ref, 1)],
            )
        ],
    )
    schematic.schematicSymbols.append(symbol)
    return symbol


def add_label(schematic, name, x, y, angle=0):
    schematic.labels.append(
        LocalLabel(name, Position(x, y, angle), visible_effects(), uid())
    )


def add_connector(schematic, root_uuid, ref, value, footprint, x, y, net1, net2):
    add_symbol(
        schematic, root_uuid, "Connector_Generic", "Conn_01x02", ref, value,
        footprint, "", x, y, 0, ["1", "2"]
    )
    add_label(schematic, net1, x - 5.08, y, 0)
    add_label(schematic, net2, x - 5.08, y + 2.54, 0)


def add_vertical_two_pin(schematic, root_uuid, entry, ref, value, footprint,
                         datasheet, x, y, top_net, bottom_net, dnp=False):
    add_symbol(
        schematic, root_uuid, "Device", entry, ref, value, footprint,
        datasheet, x, y, 0, ["1", "2"], dnp=dnp
    )
    if entry in ("C", "C_Polarized"):
        add_label(schematic, top_net, x, y - 3.81, 90)
        add_label(schematic, bottom_net, x, y + 3.81, 90)
    else:
        raise ValueError(entry)


def main():
    schematic = Schematic().create_new()
    root_uuid = uid()
    schematic.uuid = root_uuid
    schematic.generator = "osiris-pdb-generator"
    schematic.titleBlock = TitleBlock(
        title="Osiris 4S Power Distribution Board",
        date="2026-09-03",
        revision="A-PROTOTYPE",
        company="Osiris UAV",
        comments={
            1: "4S input, four external ESC branches, fused Osiris output",
            2: "Four-layer 2 oz copper target; prototype requires qualification",
            3: "Do not connect a LiPo before current-limited bench bring-up",
        },
    )
    schematic.sheetInstances = [HierarchicalSheetInstance("/", "1")]

    for name in ("C", "C_Polarized", "D_TVS", "Fuse"):
        add_embedded_symbol(schematic, DEVICE_LIB, name, "Device")
    add_embedded_symbol(schematic, CONNECTOR_LIB, "Conn_01x02", "Connector_Generic")

    pwr_4sq = "Connector_Wire:SolderWire-4sqmm_1x02_P12mm_D3mm_OD6mm"
    pwr_2sq = "Connector_Wire:SolderWire-2sqmm_1x02_P7.8mm_D2mm_OD3.9mm"

    add_connector(schematic, root_uuid, "J1", "BATTERY_IN_4S", pwr_4sq,
                  35.56, 35.56, "VBAT", "GND")
    add_connector(schematic, root_uuid, "J2", "ESC1_OUT", pwr_4sq,
                  86.36, 25.40, "VBAT", "GND")
    add_connector(schematic, root_uuid, "J3", "ESC2_OUT", pwr_4sq,
                  86.36, 40.64, "VBAT", "GND")
    add_connector(schematic, root_uuid, "J4", "ESC3_OUT", pwr_4sq,
                  127.00, 25.40, "VBAT", "GND")
    add_connector(schematic, root_uuid, "J5", "ESC4_OUT", pwr_4sq,
                  127.00, 40.64, "VBAT", "GND")
    add_connector(schematic, root_uuid, "J6", "OSIRIS_OUT_XT60_M_PIGTAIL", pwr_2sq,
                  147.32, 96.52, "OSIRIS_FUSED", "GND")

    # Main bus suppression and capacitance.
    add_symbol(schematic, root_uuid, "Device", "D_TVS", "D1", "SMCJ17CA",
               "Diode_SMD:D_SMC", "https://www.littelfuse.com/assetdocs/tvs-diodes-smcj-datasheet",
               40.64, 60.96, 90, ["1", "2"])
    add_label(schematic, "VBAT", 40.64, 64.77, 90)
    add_label(schematic, "GND", 40.64, 57.15, 90)
    add_vertical_two_pin(schematic, root_uuid, "C_Polarized", "C1",
                         "1000uF 35V LOW-ESR", "Capacitor_THT:CP_Radial_D12.5mm_P5.00mm",
                         "https://industrial.panasonic.com/ww/products/pt/aluminum-cap-lead/models/EEUFR1V102",
                         55.88, 60.96, "VBAT", "GND")
    add_vertical_two_pin(schematic, root_uuid, "C", "C2", "100nF 50V X7R",
                         "Capacitor_SMD:C_0805_2012Metric", "", 71.12, 60.96, "VBAT", "GND")

    # Osiris branch fuse, laid horizontally by rotating the vertical Fuse symbol.
    add_symbol(schematic, root_uuid, "Device", "Fuse", "F1", "0678H6300-02 6.3A",
               "PDB_Footprints:FUSC9830X318N",
               "https://www.belfuse.com/products/circuit-protection/fuses/0678h6300-02",
               86.36, 96.52, 90, ["1", "2"])
    add_label(schematic, "VBAT", 82.55, 96.52, 0)
    add_label(schematic, "OSIRIS_FUSED", 90.17, 96.52, 180)

    add_symbol(schematic, root_uuid, "Device", "D_TVS", "D2", "SMCJ17CA",
               "Diode_SMD:D_SMC", "https://www.littelfuse.com/assetdocs/tvs-diodes-smcj-datasheet",
               101.60, 116.84, 90, ["1", "2"])
    add_label(schematic, "OSIRIS_FUSED", 101.60, 120.65, 90)
    add_label(schematic, "GND", 101.60, 113.03, 90)
    add_vertical_two_pin(schematic, root_uuid, "C", "C3", "1uF 50V X7R",
                         "Capacitor_SMD:C_0805_2012Metric",
                         "https://search.kemet.com/component-documentation/download/specsheet/C0805C105K5RACAUTO",
                         116.84, 116.84, "OSIRIS_FUSED", "GND")
    add_vertical_two_pin(schematic, root_uuid, "C", "C4", "100nF 50V X7R",
                         "Capacitor_SMD:C_0805_2012Metric", "", 132.08, 116.84,
                         "OSIRIS_FUSED", "GND")
    add_vertical_two_pin(schematic, root_uuid, "C_Polarized", "C5", "100uF 35V DNP",
                         "Capacitor_THT:CP_Radial_D8.0mm_P3.50mm", "", 147.32, 116.84,
                         "OSIRIS_FUSED", "GND", dnp=True)

    schematic.texts.extend([
        Text("4S BATTERY AND FOUR EXTERNAL ESC BRANCHES", Position(25, 15, 0),
             visible_effects(), uid()),
        Text("FUSED RAW-4S OSIRIS BRANCH", Position(78, 82, 0),
             visible_effects(), uid()),
        Text("C5 DNP until hot-plug testing establishes a need.", Position(95, 130, 0),
             visible_effects(), uid()),
    ])

    schematic.to_file(str(ROOT / "Osiris_PDB_RevA.kicad_sch"))


if __name__ == "__main__":
    main()
