---
doc_id: SSK-DEC-001
title: StillStack design decisions register
project: StillStack
doc_type: Design decisions register
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the design for construction (SSK-DDR-003); budget treated as a value-engineering target
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Amish approved the recommendations for open decisions 1 to 9 (2026-10-02); moved to decisions made (SSK-DDR-003 accepted, A2 as option (c))"
---

# StillStack design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The manifold channel is about 56 x 50 mm with a snap-on lid that can be slotted | Sets the tongue bends and the lid slots (sketch SSK-DWG-114) | SSK-DDR-003 |
| 2 | The brine gutter is about 70 x 40 mm and the trough about 70 x 70 mm, with fascia brackets that fit it | Sets the outlet bracket length and the trough position | SSK-DDR-003 |
| 3 | The stone wool board has a compressive strength of 10 kPa or more | The glazing edge and its trim press on the liner tops | SSK-DDR-003 |
| 4 | The twin-wall sheet can be cut to 1,060 mm square with the flutes running down the slope, and breather tape is available for the flute ends | Drainage of condensate and rain from the flutes | SSK-PRC-001 |
| 5 | 7 mm PPS sheet (the stage 1 and 2 rail polymer, decided 2026-10-02) is sold in strips or small sheets | The rails and stop blocks are cut from it | SSK-DDR-002 |
| 6 | The coating and the high-temperature silicone adhesive bond to each other and to bare aluminium | The fins are bonded under the bottom plate; the chevron dams sit on the coating | SSK-DDR-003 |

## Value engineering

Value-engineering target: USD 355 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 416.20 (USD 61.20 over the target). Main cost drivers and savings worth trying:

- The largest lines are the five coated aluminium plates (USD 128 together, lines 3 and 5), the side rails (USD 50, line 6), the frame and liner (USD 35), the glazing (USD 32), the stand (USD 28) and the glazing trim and tape (USD 20).
- Making the design constructable added USD 65: larger plate blanks for the tongues (USD 20), the glazing trim and tape (USD 20), the stand's ground frame, gussets and pins (USD 7), brackets for the trough and outlets (USD 10), the feed closure (USD 6) and longer wicks (USD 2).
- Savings worth trying: nest the plates' tongues when ordering cut sheet so the blank is nearer 1.0 x 1.1 m (about USD 10); fold the trim from aluminium flashing instead of buying angle (about USD 8); silicone strip in place of the 150 °C polymer rails in stages 1 and 2 (about USD 14, from SSK-DDR-002) is not a saving to take, because it would undo the R8 materials decision (SSK-DDR-002, item 2) and the PPS rails decided on 2026-10-02; move the brine gutter closer to the manifold to shorten the brine tongues; reclaimed timber for the stand; a locally made stagnation cover.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | Four stages with 6 mm gaps; air-cooled fins; aluminium condenser plates with a food-contact coating; spacers in ASA or polycarbonate, not PETG; 20 deg tilt on an adjustable stand; 1 m2 aperture; budget kept at USD 250 | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | [SSK-DDR-001](decisions/0001-trl2-review-decisions.md) |
| 2026-09-25 | Silicone-cord ribs; R8 response (c): 150 °C materials in stages 1 and 2, stone wool liner, stagnation cover; budget raised to USD 320 | Amish: "i accept all your recommendations, go with them across all repos." | [SSK-DDR-002](decisions/0002-recommendations-accepted.md) |
| 2026-09-26 | Budget top-up to USD 355 | Amish: "I am ok with the budget top ups" | [SSK-DDR-002](decisions/0002-recommendations-accepted.md) v0.2 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | [SSK-DDR-003](decisions/0003-design-for-construction.md) (changes accepted on 2026-10-02, below) |
| 2026-09-30 | Open decisions live in this register, not in the build plan | Amish: "don't log outstanding decisions in this build plan - that is not the place for it." | This register |
| 2026-10-01 | `budget_usd` is a value-engineering target, not a limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens" | This register, Value engineering |
| 2026-10-02 | Design for construction accepted: the changes P1 to P12 and their knock-on changes, as made, with the two brine-separation details decided separately (A1 and A2, below) and the wick fixing of P11 replaced by the clip decision below | Amish: "i approve your recommendations for all 555 open decisions." | SSK-DDR-003, Table 1 |
| 2026-10-02 | Brine exit (R4, safety case): option (a), the zigzag edges with separate distillate and brine tongues; each stage's distillate conductivity test is a pass condition at TRL 4 before any water is drunk; the cross-wick (b) is the fallback | Amish: "i approve your recommendations for all 555 open decisions." | SSK-DDR-003, A1 |
| 2026-10-02 | Feed tails at the high edge (R4, safety case): option (c) now (changed from the register's (a)). A 4 mm downturned lip on each condensing plate's high edge, bent before coating; dropped only if TRL 4 conductivity tests without it show no carryover | Amish: "i approve your recommendations for all 555 open decisions." | SSK-DDR-003, A2 |
| 2026-10-02 | Wick fixing (R10): clips at each wick's high and low ends (stainless, or the 150 °C rail polymer in stages 1 and 2) and no adhesive, so the wicks lift out once the plates are up | Amish: "i approve your recommendations for all 555 open decisions." | SSK-PRC-001, open questions |
| 2026-10-02 | Coating (R7): the lowest-cost coating certified for drinking-water contact (NSF/ANSI 61 or an equivalent food-contact statement) in hot salty water and rated to 150 °C dry; first class to check, fluoropolymer (PTFE type) cookware coatings. If none meets both, 316 stainless for plates 1 and 2 | Amish: "i approve your recommendations for all 555 open decisions." | SSK-DDR-002, item 5 |
| 2026-10-02 | Wick fabric (R6): shortlist from datasheets one polyester or polyester-viscose nonwoven and one glass-fibre fabric, run a wicking-rise test on each, and pick the cheaper one that reaches 3.0 x 10^-11 m2 and tolerates 150 °C dry | Amish: "i approve your recommendations for all 555 open decisions." | SSK-DDR-002, item 5 |
| 2026-10-02 | Rail polymer (R8): PPS for the stage 1 and 2 rails and stop blocks | Amish: "i approve your recommendations for all 555 open decisions." | SSK-PRC-001, open questions |
| 2026-10-02 | First co-design partner: a university water or desalination lab first; first candidate to approach, the Politecnico di Torino group behind the 2018 floating multistage still. A coastal NGO for field use once the distillate passes its tests | Amish: "i approve your recommendations for all 555 open decisions." | SSK-DDR-001, item 8 |
| 2026-10-02 | Appearance items adopted, all five: glazing flutes down the slope, removable manifold lid, drip valve at the front end, DISTILLATE and BRINE labels, and different rail colours for stages 1 and 2 | Amish: "i approve your recommendations for all 555 open decisions." | docs/REVIEW.md, 2026-09-26 |
