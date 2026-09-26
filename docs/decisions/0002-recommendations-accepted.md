---
doc_id: SSK-DDR-002
title: StillStack recommendations accepted
project: StillStack
doc_type: Design decision record
version: "0.1"
status: Draft
date: 2026-09-25
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-09-25
    author: Amish Chadha
    change: Recommendations accepted by Amish (DDR-002)
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted (items 1 to 3); items 4 and 5 remain proposed, awaiting Amish

On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every open item in docs/REVIEW.md and docs/decisions/ that carried a recommendation is therefore decided as recommended. Items without a recommendation stay open. TRL 4 remains on hold by Amish's instruction, so the decisions are implemented on paper only (TRL 3).

## Context

The TRL 3 review (docs/REVIEW.md, session 2026-09-25: TRL 3) listed five items as awaiting Amish. Three carried a recommendation: the intermediate spacer ribs, the response to R8 (dry stagnation) and the response to R12 (cost). The first co-design partner (SSK-DDR-001 item 8) and the coating and wick selections carried none.

## Decision

Table 1. Items decided by this record.

| # | Item | Options considered | Decision |
| --- | --- | --- | --- |
| 1 | Intermediate spacer ribs | Silicone cord; printed polycarbonate | Decided by Amish, 2026-09-25: go with recommendation. 7 mm food-grade silicone cord, four per gap at 194 mm pitch. |
| 2 | Response to R8 not met | (a) materials rated to about 150 °C in stages 1 and 2 and R8 restated to match; (b) keep R8 and add a stagnation cover or shade rule; (c) both | Decided by Amish, 2026-09-25: go with recommendation. Option (c): both. |
| 3 | Response to R12 not met | (a) raise budget_usd to about $320; (b) keep $250 and cut cost; (c) exclude the stand from the budget | Decided by Amish, 2026-09-25: go with recommendation. Option (a): budget_usd raised from $250 to $320. |

## What changed in the repo

- **Item 1.** The silicone-cord ribs were already in the model and BOM as a proposal; they are now a decided design choice in SSK-PRC-001 v0.4, bom/bom.csv (line 7) and SSK-CAL-001 v0.2. No geometry change.
- **Item 2, materials.** The frame liner changes from 25 mm PIR foam to 25 mm foil-faced stone wool board (rated well above 150 °C); the four side rails in stages 1 and 2 change from printed polycarbonate to a polymer rated to 150 °C or more continuous (PPS or a high-heat polycarbonate copolymer, product not yet selected); the wick and the condenser coating on plates 1 and 2 must tolerate 150 °C. The rails in stages 3 and 4 stay printed polycarbonate. Panel dry mass rises from 15.9 to 16.7 kg (wet 19.9 to 20.7 kg) because of the denser liner. The outside dimensions do not change.
- **Item 2, requirement.** R8 in SSK-REQ-001 v0.4 is restated: materials in stages 1 and 2 rated to 150 °C or more, all other internal materials to 110 °C or more, a stagnation cover supplied and a shade rule in the instructions. SSK-CAL-001 v0.2 now checks both limits in calm air as well as at 1 m/s. Stages 1 and 2 peak at 144 °C (6 K margin); stage 3 peaks at 110 °C in calm air (0 K margin), so R8 moves from **not met** to **at risk**.
- **Item 2, cover.** A stagnation cover (opaque white or aluminized tarpaulin with an elastic edge cord, $12) is added as BOM line 14. It is a loose accessory and is not modeled. The safety notes now require fitting it whenever the feed runs out and before maintenance.
- **Item 3.** budget_usd in project.yaml changes from $250 to $320 and R12 now reads $320 or less. The item 2 materials and cover add $34 ($22 for the rails, $12 for the cover), so the priced BOM rises from $317.20 to **$351.20**, which is **$31.20 over** the new budget. R12 therefore stays **not met**. A new response is proposed, awaiting Amish (item 6 below).
- **Drawings and media.** GA drawing SSK-DWG-002 moves from Rev P1 to P2 (material block and notes). The concept blueprint SSK-DWG-001 moves from Rev P2 to P3 (key figures). The model, STEP and STL files were re-exported; the geometry is unchanged.
- **Documents.** SSK-PRB-001 v0.4, SSK-PRC-001 v0.4, SSK-REQ-001 v0.4 and SSK-CAL-001 v0.2, with revision entries "Recommendations accepted by Amish (DDR-002)".

## Items still open

Table 2. Items that stay proposed, awaiting Amish.

| # | Item | Status |
| --- | --- | --- |
| 4 | First co-design partner (coastal NGO, university water lab or makerspace network) | No recommendation. Proposed, awaiting Amish. |
| 5 | Coating product for the condensing faces (R7) and wick fabric with a permeability of 3.0 x 10^-11 m2 or more (R6) | Selections that need datasheets. No recommendation. Proposed, awaiting Amish. |
| 6 | Response to R12 not met at the $320 budget (new) | Options: (a) raise budget_usd to about $355; (b) keep $320 and cut cost, for example by making the stage 1 and 2 rails from silicone strip (about $14 less) and sourcing the cover locally; (c) exclude the stagnation cover and stand from the budget. Recommendation: (a), because the extra cost comes from parts that items 2 and 3 require. Proposed, awaiting Amish. |

## Consequences

- R8 is now at risk rather than not met, and R12 remains not met at the higher budget. Requirement targets other than R8 and R12 are unchanged.
- TRL 4 is on hold by Amish's instruction. Nothing in this record authorizes hardware, tests or purchasing.
