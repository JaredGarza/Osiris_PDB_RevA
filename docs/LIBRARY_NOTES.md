# Project library notes

The active schematic currently uses the project-local `FUSC9830X318N` fuse footprint. Additional PDB-specific library assets are included for continued design work:

- `ISC015N06NM5LF2`: pads 1–3 Source, 4 Gate, and 5–8 Drain. No vendor 3D model was available.
- `LTC4368IMS-1-PBF`: corrected MSOP-10 footprint with pads 1–10 only; the incorrect pad-11 vendor footprint was excluded.
- `INA228AIDGSR`: VSSOP-10 footprint and vendor STL model.
- `TPS7A1633DGNR`: HVSSOP-8 footprint with real PowerPAD pad 9 and vendor STL model.
- `FC4L64R005FER`: four-terminal current-shunt symbol and footprint; no 3D model was available.

The LTC4368 and ISC015N06NM5LF2 datasheets are stored in `Datasheets/`. Local datasheets were not found for INA228AIDGSR, TPS7A1633DGNR, FC4L64R005FER, or the fuse.
