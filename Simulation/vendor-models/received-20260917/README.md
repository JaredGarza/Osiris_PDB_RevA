# Supplied model files

| Download | Contents and disposition |
|---|---|
| resources.zip | Nested ST Schottky libraries. ST_POWER_SCHOTTKY_V10.LIB includes exact STPST10H100SB electrical model; integrated into the release PDB model, with both anodes grounded. Original library and documentation preserved in st-schottky. |
| SMAJ24CA.txt | Taiwan Semiconductor electrical TVS model. Header identifies SMAJ24CA, but subcircuit name is SMAJ24A; internally two opposing diodes. Retained as Taiwan-SMAJ24CA.txt. Does not match Bourns BOM manufacturer. |
| smaj-series_pspice.zip | ST electrical TVS library containing SMAJ24CA. Retained in st-tvs-electrical for comparison; not substituted for Bourns. |
| smaj-series-thermal-ltspice-pspice.zip | ST encrypted LTspice electrothermal library and symbol. Header says validated with LTspice 24.1.8, typical breakdown only, and leakage may be outside part specifications. Symbol defaults to SMAJ5_0A. Retained in st-tvs-thermal; not yet simulated. |
| ul_ISC015N06NM5LF2ATMA1 (1).zip | KiCad symbol and footprint only. No transistor SPICE model. Original remains in Downloads. |
| smajxxa_cad_orcad_.zip | OrCAD symbol/PCB package assets only. No electrical SPICE model. Original remains in Downloads. |

ST library SHA-256: 633fb9263215d27c308e42fa32be0577889347a388021460cf87ddfe9e4e7bad.

Still needed: manufacturer transistor models for ISC015N06NM5LF2 and BSC070N10NS5; exact Bourns SMAJ24CA model if available; Osiris LM73100/AP64501 models and the intended Osiris schematic/load definition. Existing ADI LTC4368-1/LTC4359/LT3010 models are already available.
