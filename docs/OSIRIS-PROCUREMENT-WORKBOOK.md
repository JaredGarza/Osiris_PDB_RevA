# Osiris procurement workbook update

Updated September 14, 2026. The existing Lab-Procurement.xlsx now includes an Osiris build calculator, supplier price breaks, a supply-risk review and the results of the link checks already attempted. General lab targets and equipment quantities remain independent of board count.

Use **Osiris build!B4** to select 0, 1, 2, 3, 5, 10, 15, 20, 25, 50 or 100 boards. The initial 10 boards, 10% spares and two setup pieces per line are editable planning assumptions, not an authorized build. Planned and inventory-adjusted costs use their respective quantity price breaks. An optional price contingency is a user scenario, not a price forecast.

## Scope and missing information

- Source: `OsirisRevA (1).zip`, SHA-256 `82c98a07af79acc3e7d6a1046bf02901b6d08617cb8b6946c63fdf98da97b7e5`.
- Direct extraction matched the earlier archive component audit. 455 symbol records reduce to 425 unique designators and 113 source groups. Multipart MCUs and the P1 connector are counted once. Assembly variants and DNP intent are not verified.
- The new Rev B power path and connector changes are planned. Archive quantities are not an approved Rev B BOM.
- Eighteen specialized Osiris parts have sourced USD price tiers. Other prices remain blank; the complete total is withheld while included lines remain unpriced. General lab and equipment rows now have editable price fields and cost formulas, but exact selections/quotes are still required.
- Conflicting crystal MPN/frequency entries and the 3.3 V versus 1.8 V regulator entries default to excluded. Bare TC2030 programming footprints are also excluded from purchased-component counts.
- Prices are supplier snapshots, not firm quotes. Tax, freight, tariffs, fabrication, assembly and reeling fees are excluded. No verified future price-rise notice was established.

## Information to collect manually

Per the user's instruction, do not retry websites that block access. For desired parts, obtain the exact manufacturer order code, package/carrier, available quantity, quoted lead time, unit prices at the intended quantity, pack minimum/multiple, packaging fees and a usable product URL. Enter prices on the lab/equipment tabs or in the Osiris quote-override column. Keep the quoted quantity and date with the source.

Prioritize STM32H743IIK6, STM32F446RET6, BMI088, ICM-42688-P, LPS22HBTR and LIS2MDLTR: the checked DigiKey listings reported no stock. TESEO-LIV3R has a distributor last-time-buy date and ST NRND status. HHM1595A1 is TDK NRND despite listed inventory. These findings do not prove a global shortage. Make a retention/redesign decision before reserving legacy parts for Rev B.

## Checks completed

Tested the board selector, zero and missing board quantities, spare/setup arithmetic, price-break thresholds, inventory subtraction, net-order price tiers, price contingency, missing-price handling and lab cost inputs. Verified original A:O values/formulas on both existing sheets were preserved. Export contains six worksheets, 536 native hyperlink instances and no Excel cell errors. Numeric dropdown uses a defined range. Workbook has not been exercised in native Microsoft Excel.

261 unique URLs were attempted before the user stopped further checking: 249 blocked automated requests, 11 returned HTTP responses and one timed out. The key supplier/lifecycle evidence was readable through web research. The link-validation sheet distinguishes those results; it does not claim that every link passed or that search links identify an approved part.
