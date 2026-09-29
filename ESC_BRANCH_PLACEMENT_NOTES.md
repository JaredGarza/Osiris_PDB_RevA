# ESC branch placement notes

**Historical placement study.** The compact three-XT60 board and routing in
[the 29 September review](COMPACT_XT60_ROUTE_REVIEW_2026-09-29.md) supersede
the positions and unrouted status below.

Date: 2026-09-29

## What was changed

The high-current ESC branch components were placed, but no new copper was routed.
All existing routing and copper zones were preserved.

- J1 battery input: `(29.0, -3.0) mm`, 0 degrees
- F2 100 A branch fuse: `(51.0, -3.0) mm`, 0 degrees
- D5 ESC transient clamp: `(88.0, -3.0) mm`, 0 degrees
- C17 ESC bulk capacitor: `(100.0, -3.0) mm`, 0 degrees
- C18 ESC bypass capacitor: `(95.0, 5.0) mm`, 0 degrees
- C19 ESC bypass capacitor: `(101.0, 5.0) mm`, 0 degrees
- J3 ESC output: `(123.0, -3.0) mm`, 180 degrees

J1 and J3 use a provisional Phoenix Contact MKDSP 25/2-15.00 footprint. F2
uses a provisional Schurter UHS footprint. Verify both footprints against the
exact ordered manufacturer part numbers before fabrication.

## Mechanical result

The board envelope is approximately `126.05 x 83.30 mm`. The added upper shelf
keeps the existing avionics placement and every mounting hole unchanged:

- H1: `(45.5, 18.75) mm`
- H2: `(90.5, 18.75) mm`
- H3: `(90.5, 59.5) mm`
- H4: `(45.5, 58.75) mm`

## Routing intent

Use broad copper pours rather than ordinary traces. The placement provides a
direct battery-positive path from J1 through F2 to J3, with D5 and the ESC
capacitors close to J3. A broad, direct ground-return path can run on the
opposite copper layer.

For the preliminary 60 A continuous target:

- 1 oz copper is not suitable for this layout.
- With 2.5 oz copper, reserve about 22-24 mm of uninterrupted width per main
  current path.
- With 4.5 oz copper, reserve about 14-16 mm per main current path for useful
  margin.
- Expand immediately from component pads into the wide pours, use via arrays
  where current changes layers, and avoid routing at the fabricator's minimum
  clearance.

Confirm the final copper weight, allowable temperature rise, continuous and
peak ESC current, and the board house's current-capacity rules before routing
or fabrication.

## Outlined or apparently unfilled copper

The saved board contains filled copper zones, and the final 3D render shows
them as filled. If KiCad displays outlines only:

1. Press `B` to refill all zones.
2. Enable **Show filled areas in zones** and disable zone-outline-only display.
3. If ordinary traces are hollow outlines, disable **Tracks in sketch mode**.

## Verification

- KiCad DRC placement/geometry violations: 0
- Unconnected items: 25, expected because this placement is intentionally not routed
- Track count before and after placement: 499
- Copper zones preserved: 13

