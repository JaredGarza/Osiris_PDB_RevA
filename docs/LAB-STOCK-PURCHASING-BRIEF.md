# Lab stock and PDB purchasing brief

## Purchase strategy

### Purpose

Prepare a shared lab stock purchase for the new pick-and-place machine, plus the exact parts needed for PDB Rev A prototypes. Prepared September 14, 2026 for the September 15 discussion. Build quantity, machine model, budget and existing usable stock are not yet known.

### Recommendation

Inventory Ryan's R/C/L books first. Request quotes for small machine-ready reels of the most reusable passives and compare with one factory reel per selected stock item. Buy project-specific ICs, MOSFETs, shunts and connectors in prototype quantities. Do not buy full semiconductor reels just because the order code is a reel variant.

### What is confirmed

The A-P1 PDB baseline contains 27 unique purchased part codes, 33 physical items per board and 29 SMT placements across 23 SMT part types. Seven bare test pads do not require purchased parts. This list supports procurement planning; final circuit qualification and PCB layout remain open.

### Osiris Rev B boundary

The new Rev B power path and top-facing ports are planned, not saved as a completed design. Its new regulator, inductor and power-path BOM is unknown. Historical Osiris passives are largely 0402, while this PDB uses 0603/0805/1206. Equal values in different packages cannot share a reel. No new Rev B quantities are included here.

## Passives

| Exact MPN | References | Per PDB | Description | Package | Purchase class |
|---|---|---:|---|---|---|
| C0603C104K4RACTU | C3, C5, C8 | 3 | 100 nF, 16 V, X7R, 10% | 0603 (EIA) | A - stock candidate |
| C1608X7R1H104K080AA | C7 | 1 | 100 nF, 50 V, X7R, 10% | 0603 (EIA) | A - stock candidate |
| C2012C0G2A562J125AA | C1 | 1 | 5.6 nF, 100 V, C0G, 5% | 0805 (EIA) | B - small tape/reel |
| C2012X7R1A106K125AC | C6 | 1 | 10 uF, 10 V, X7R, 10% | 0805 (EIA) | B - small tape/reel |
| C2012X7R1H105K125AB | C2 | 1 | 1 uF, 50 V, X7R, 10% | 0805 (EIA) | B - small tape/reel |
| C3216X7R1H106K160AC | C4, C9 | 2 | 10 uF, 50 V, X7R, 10% | 1206 (EIA) | B - small tape/reel |
| RC0805FR-0710RL | R8, R9 | 2 | 10 ohm, 1%, 0.125 W | 0805 (EIA) | A - stock candidate |
| RC0805FR-07200KL | R7 | 1 | 200k ohm, 1%, 0.125 W | 0805 (EIA) | B - small tape/reel |
| RC0805FR-0722KL | R4 | 1 | 22k ohm, 1%, 0.125 W | 0805 (EIA) | A - stock candidate |
| RC0805FR-072ML | R1 | 1 | 2M0 ohm, 1%, 0.125 W | 0805 (EIA) | B - small tape/reel |
| RC0805FR-0743K2L | R2 | 1 | 43k2 ohm, 1%, 0.125 W | 0805 (EIA) | B - small tape/reel |
| RC0805FR-074K7L | R10 | 1 | 4k7 ohm, 1%, 0.125 W | 0805 (EIA) | A - stock candidate |
| RC0805FR-0756K2L | R3 | 1 | 56k2 ohm, 1%, 0.125 W | 0805 (EIA) | B - small tape/reel |
| RC0805FR-07680KL | R6 | 1 | 680k ohm, 1%, 0.125 W | 0805 (EIA) | B - small tape/reel |

## Specialized and mechanical parts

| Exact MPN | References | Per PDB | Description | Package | Purchase class |
|---|---|---:|---|---|---|
| 0297004.WXNV | F1 | 1 | 4A MINI | MINI blade fuse | HOLD rating |
| 74AUP1G07GW,125 | U4 | 1 | 74AUP1G07GW | SOT-353 | C - prototype SMT |
| BM04B-GHS-TBT(LF)(SN) | J2 | 1 | OSIRIS_I2C | JST GH 4-pin vertical | C - prototype SMT |
| FC4L64R005FER | R5 | 1 | 5 milliohm, 4-terminal shunt | 6432 4-terminal | C - prototype SMT |
| INA228AIDGSR | U2 | 1 | INA228AIDGSR | VSSOP-10 | C - prototype SMT |
| ISC015N06NM5LF2ATMA1 | Q1, Q2 | 2 | ISC015N06NM5LF2 | TDSON-8 5x6 mm | C - prototype SMT |
| LTC4368IMS-1#TRPBF | U1 | 1 | LTC4368IMS-1-PBF | MSOP-10 | C - prototype SMT |
| MBR0540T1G | D2, D3 | 2 | MBR0540 | SOD-123 | C - prototype SMT |
| SMAJ24CA | D1 | 1 | SMAJ24CA | SMA | C - prototype SMT |
| TPS7A1633DGNR | U3 | 1 | TPS7A1633DGNR | MSOP-8 exposed pad | C - prototype SMT |
| 3568 | F1-holder | 1 | MINI fuse holder | MINI fuse holder TH | C - manual/TH |
| XT60PW-F | J3 | 1 | XT60PW-F | XT60 horizontal TH | C - manual/TH |
| XT60PW-M | J1 | 1 | XT60PW-M | XT60 horizontal TH | C - manual/TH |

## Ryan's books: inventory before buying

Record value, EIA package, manufacturer/MPN, tolerance, power or voltage rating, dielectric, quantity and carrier condition. Distinguish loose parts, short tape strips and continuous tape. Count stock toward machine assembly only after feeder compatibility is established. Unidentified parts are not approved substitutions for the PDB.

## Shared stock proposal

For each of the five A-marked candidates, quote 250 and 1,000 parts on a custom reel, plus the smallest factory reel. These are quote tiers, not committed order quantities. Select one tier after checking other project BOMs, Ryan's stock and total cost including reeling. The two 100 nF parts remain separate MPNs; combining them needs a reviewed substitution.

## Project-specific quantity rule

For each B or C item, order max(0, boards to build x quantity per board + setup losses + repair spares - usable on-hand stock), rounded to supplier pack quantity. Establish setup loss with the machine supplier; do not assume a percentage covers feeder loading. Request continuous cut tape or a custom reel for SMT parts; loose pieces are for supported trays/manual work only.

## Machine and assembly purchases

Confirm machine model, 0402 capability, feeder widths and pitch, reel diameter, component height limits, nozzle selection, vision support and cut-tape/tray handling. There are 23 SMT part types on the PDB; that is not a guaranteed 23-slot feeder requirement because widths and staging vary. Budget feeders, suitable nozzles, leader/trailer supplies, ESD storage and moisture-control supplies as required by component handling specifications.

## Items outside the PCB BOM

Budget solder paste compatible with the process, flux/cleaning supplies, stencil and board support, reflow capability and inspection equipment. Quote stencil/panel details after layout is released. Add the PDB-to-Osiris power and I2C harnesses, mating housings/contacts and crimp tooling once connector orientation, wire gauge and length are fixed; they are not included in the 33-item board count.

## Hold before production-volume buying

Finalize the Rev B power/load budget and interface, then resolve the provisional 4 A fuse rating, MOSFET fault-energy/SOA and clamp validation. Historical overlaps in INA228 and JST/XT60 connectors are candidates only. Do not stock new Rev B regulators or inductors until their electrical and package requirements are selected.

## Decisions for the meeting

Agree a shared-stock budget, nominate someone to inventory Ryan's books, obtain the machine/feeder specification, and choose the initial PDB build quantity. Then request distributor quotes with exact MPN, carrier, pack quantity, lead time, stock and total price. No live prices or stock availability have been quoted in this brief.

## Sources

- A-P1 source: procurement/2026-09-13/PDB-grouped-order-list.csv; tag pdb-procurement-2026-09-13. Exact electrical specifications are retained in the baseline purchasing workbook and datasheets.
- Custom reels: https://forum.digikey.com/t/details-about-digi-reels/1303
- Cut tape packaging: https://forum.digikey.com/t/a-closer-look-at-taped-packaging-including-cut-tape-and-tape-and-reels/17211
