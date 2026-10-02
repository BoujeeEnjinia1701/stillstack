---
doc_id: SSK-DDR-001
title: StillStack TRL 2 review decisions
project: StillStack
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-09-25
    author: Amish Chadha
    change: Record the decisions Amish made on the TRL 2 review points, and the items still open
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Item 8 decided by Amish on 2026-10-02 (SSK-DEC-001)"
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted (items 1 to 7); item 8 decided by Amish on 2026-10-02 (SSK-DEC-001)

Amish accepted every recommendation in the TRL 2 review note (docs/REVIEW.md, session 2026-09-24) on 2026-09-25, with the instruction that no repo proceeds to TRL 4. Seven items are decided. The first co-design partner had no recommendation and stays open.

## Context

The TRL 2 review listed eight items as "Proposed, awaiting Amish". Amish wrote on 2026-09-25: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." Items that carried a recommendation are recorded below as decided. Items without one stay open.

## Options considered

The options for each item are those listed in the TRL 2 review note and in SSK-PRC-001 v0.2, section "Key design choices".

## Decision

Table 1. Decisions on the TRL 2 review points.

| # | Item | Options considered | Decision |
| --- | --- | --- | --- |
| 1 | Stage count and gap | Three stages; four stages with 6 mm gaps; six stages with a water-cooled bottom | Decided by Amish, 2026-09-25: go with recommendation. Four stages with 6 mm vapor gaps. |
| 2 | Heat rejection at the bottom | Air-cooled fins; feed-water tray heat sink; floating on water | Decided by Amish, 2026-09-25: go with recommendation. Air-cooled aluminum fins under the bottom plate. |
| 3 | Condenser plate material | Aluminum with a food-grade coating; 316 stainless steel; anodized aluminum | Decided by Amish, 2026-09-25: go with recommendation. Aluminum plates with a food-contact coating on the condensing face. |
| 4 | Spacer material | PETG; ASA; polycarbonate | Decided by Amish, 2026-09-25: go with recommendation. ASA or polycarbonate, not PETG. |
| 5 | Tilt | Fixed 20 deg; 20 deg with an adjustable stand | Decided by Amish, 2026-09-25: go with recommendation. Nominal tilt 20 deg on a stand adjustable over the R11 range. |
| 6 | Prototype aperture | 1 m2; 0.5 m2 | Decided by Amish, 2026-09-25: go with recommendation. 1 m2. |
| 7 | Budget | Keep $250; raise for stainless plates | Decided by Amish, 2026-09-25: go with recommendation. Keep budget_usd at $250 with no redefinition of what it covers. |
| 8 | First co-design partner | Coastal NGO; university water lab; makerspace network | No recommendation was made on 2026-09-25. Decided by Amish, 2026-10-02: a university water or desalination lab first; first candidate to approach, the Politecnico di Torino group behind the 2018 floating multistage still; a coastal NGO for field use once the distillate passes its tests (SSK-DEC-001). |

## Consequences

- SSK-PRC-001 and SSK-REQ-001 move to v0.3 with items 1 to 7 stated as design choices rather than proposals. SSK-PRB-001 moves to v0.3 with the aperture question closed and the partner question left open.
- The TRL 3 calculation note SSK-CAL-001 sizes the design as decided. It finds that dry stagnation reaches about 140 °C at stage 1, which rules out ASA in stages 1 to 3 and leaves polycarbonate as the only decided spacer material that is close to adequate (item 4). It also finds that the parts cost of about $317 exceeds the $250 budget kept under item 7. Both findings are reported against R8 and R12, and the responses are proposed, awaiting Amish, in docs/REVIEW.md. This record does not change either decision.
- TRL 4 is on hold by Amish's instruction. Nothing in this record authorizes hardware, tests or purchasing.
