---
doc_id: SSK-DEC-001
title: StillStack design decisions register
project: StillStack
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the design for construction (SSK-DDR-003); budget treated as a value-engineering target
---

# StillStack design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Design for construction as a whole (changes P1 to P12) | Accept; accept with changes; reject items | Accept | Every component | SSK-DDR-003, Table 1 |
| 2 | How brine leaves the low edge without reaching the distillate (R4, safety case) | (a) zigzag edges, distillate tongues at the rib lines, brine tongues at the strip centres, as modelled; (b) a cross-wick carrying brine to the side walls; (c) concept low edge, brine exit tested separately at TRL 4 | (a); confirm by each stage's distillate conductivity at TRL 4 | Plates (sections 3.7, 3.10, 3.12), wicks (3.11), low wall comb (3.3), manifold lid (3.14), steps 15 and 17 | SSK-DDR-003, A1 |
| 3 | Feed tails crossing the condensing plates' high edges 6 mm above them (R4, safety case) | (a) accept and measure at TRL 4; (b) stagger the plates' high edges about 22 mm per level (about 4 % less yield); (c) 4 mm downturned lip on each condensing plate's high edge | (a), with (c) as the first fix if carryover shows | Plates (3.10), wick tails at the high wall (3.2, 3.11) | SSK-DDR-003, A2 |
| 4 | How the wicks are held so one person can remove them in 30 min (R10) | Silicone dots, as built; clips or a frame per wick; loose wicks on a mesh | None yet | Wick bonding (section 3.11) | SSK-PRC-001, open questions |
| 5 | Food-contact coating for the condensing faces, 80 °C wet and salty, 150 °C dry on plates 1 and 2 (R7) | Product to be chosen from datasheets | None yet | Plates (sections 3.7, 3.10) | SSK-DDR-002, item 5 |
| 6 | Wick fabric with a permeability of 3.0 x 10^-11 m2 or more that tolerates 150 °C dry (R6) | Product to be chosen from datasheets | None yet | Wick strips (section 3.11) | SSK-DDR-002, item 5 |
| 7 | Rail polymer for stages 1 and 2 rated to 150 °C (R8) | PPS; high-heat polycarbonate copolymer | None yet (lowest cost that meets 150 °C) | Side rails and stop blocks (sections 3.6, 3.8) | SSK-PRC-001, open questions |
| 8 | First co-design partner | Coastal NGO; university water lab; makerspace network | None | Not part of the TRL 3 build | SSK-DDR-001, item 8 |
| 9 | Product model appearance items 2, 3, 4, 7 and 8 of the 2026-09-26 review (glazing flutes down the slope, removable manifold lid, drip valve at the front end, DISTILLATE and BRINE labels, different rail colours for stages 1 and 2) | Adopt; drop | Adopt all five; the build plan already specifies flutes down the slope, a removable lid and marked rails | Glazing, manifold, trough, rails | docs/REVIEW.md, 2026-09-26; items 1, 5 and 6 are now part of SSK-DDR-003 |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The manifold channel is about 56 x 50 mm with a snap-on lid that can be slotted | Sets the tongue bends and the lid slots (sketch SSK-DWG-114) | SSK-DDR-003 |
| 2 | The brine gutter is about 70 x 40 mm and the trough about 70 x 70 mm, with fascia brackets that fit it | Sets the outlet bracket length and the trough position | SSK-DDR-003 |
| 3 | The stone wool board has a compressive strength of 10 kPa or more | The glazing edge and its trim press on the liner tops | SSK-DDR-003 |
| 4 | The twin-wall sheet can be cut to 1,060 mm square with the flutes running down the slope, and breather tape is available for the flute ends | Drainage of condensate and rain from the flutes | SSK-PRC-001 |
| 5 | 7 mm sheet of the stage 1 and 2 rail polymer is sold in strips or small sheets | The rails and stop blocks are cut from it | SSK-DDR-002 |
| 6 | The coating and the high-temperature silicone adhesive bond to each other and to bare aluminium | The fins are bonded under the bottom plate; the chevron dams sit on the coating | SSK-DDR-003 |

## Value engineering

Value-engineering target: USD 355 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 416.20 (USD 61.20 over the target). Main cost drivers and savings worth trying:

- The largest lines are the five coated aluminium plates (USD 128 together, lines 3 and 5), the side rails (USD 50, line 6), the frame and liner (USD 35), the glazing (USD 32), the stand (USD 28) and the glazing trim and tape (USD 20).
- Making the design constructable added USD 65: larger plate blanks for the tongues (USD 20), the glazing trim and tape (USD 20), the stand's ground frame, gussets and pins (USD 7), brackets for the trough and outlets (USD 10), the feed closure (USD 6) and longer wicks (USD 2).
- Savings worth trying: nest the plates' tongues when ordering cut sheet so the blank is nearer 1.0 x 1.1 m (about USD 10); fold the trim from aluminium flashing instead of buying angle (about USD 8); silicone strip in place of the 150 °C polymer rails in stages 1 and 2 (about USD 14, from SSK-DDR-002); move the brine gutter closer to the manifold to shorten the brine tongues; reclaimed timber for the stand; a locally made stagnation cover.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | Four stages with 6 mm gaps; air-cooled fins; aluminium condenser plates with a food-contact coating; spacers in ASA or polycarbonate, not PETG; 20 deg tilt on an adjustable stand; 1 m2 aperture; budget kept at USD 250 | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | [SSK-DDR-001](decisions/0001-trl2-review-decisions.md) |
| 2026-09-25 | Silicone-cord ribs; R8 response (c): 150 °C materials in stages 1 and 2, stone wool liner, stagnation cover; budget raised to USD 320 | Amish: "i accept all your recommendations, go with them across all repos." | [SSK-DDR-002](decisions/0002-recommendations-accepted.md) |
| 2026-09-26 | Budget top-up to USD 355 | Amish: "I am ok with the budget top ups" | [SSK-DDR-002](decisions/0002-recommendations-accepted.md) v0.2 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | [SSK-DDR-003](decisions/0003-design-for-construction.md) (Draft, open for review) |
| 2026-09-30 | Open decisions live in this register, not in the build plan | Amish: "don't log outstanding decisions in this build plan - that is not the place for it." | This register |
| 2026-10-01 | `budget_usd` is a value-engineering target, not a limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens" | This register, Value engineering |
