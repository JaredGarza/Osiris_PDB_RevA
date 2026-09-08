# Osiris PDB Rev A

4S LiPo avionics power delivery and protection board for the Osiris platform.

The board is designed in KiCad. Project-specific symbols, footprints, and 3D models are stored under `Libraries/`, and library/model paths use `${KIPRJMOD}` for portability.

To use the project on another computer, clone this repository and open `Osiris_PDB_RevA.kicad_pro` in KiCad 10 or a compatible newer version. No vendor-library import should be required.

Verified vendor footprints must not be edited without checking the current official manufacturer datasheet. The optional Python generator scripts assume KiCad 10 is installed in its default Windows location; they are not required to open or edit the KiCad project.
