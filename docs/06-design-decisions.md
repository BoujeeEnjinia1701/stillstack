---
doc_id: SSK-DEC-001
title: StillStack design decisions register
project: StillStack
doc_type: Design decisions register
version: '0.5'
status: Draft
date: '2026-10-25'
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
  - version: "0.3"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Value engineering restated for the follow-ups carried into the design (USD 443.20, USD 88.20 over the target); two items to confirm when parts are bought"
  - version: "0.4"
    date: '2026-10-24'
    author: Amish Chadha
    change: "Kit 1.9.1 upgrade: D-01 stage 3 rails in PPS (STEM fix, decided under Amish's standing instruction of 2026-10-23); D-02 bolt lengths from the detailed model; D-03 concept selection between options A and B (within 10 %, proposed, awaiting Amish); D-04 to D-06 proposed; D-07 painted underside and fins (STEM fix after the independent review); D-08 wick clip material and D-09 wind anchoring proposed; value engineering restated (USD 459.20)"
  - version: '0.5'
    date: '2026-10-25'
    author: Amish Chadha
    change: 'Amish decided D-04, D-05, D-06, D-08, D-09 and D-10 as recommended on 2026-10-25 ("i concur with your recommendations"); moved to decisions made; D-03 stays open (no pick); USD 460.70'
---

# StillStack design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

Table 1. Decisions proposed, awaiting Amish (kit 1.9.1 upgrade, 2026-10-24). D-03 had no pick, so it stays open; D-04, D-05, D-06, D-08, D-09 and D-10 were decided by Amish on 2026-10-25 as recommended and are under Decisions made.

| # | Decision | Options | Recommendation | Record |
| --- | --- | --- | --- | --- |
| D-03 | Concept selection: carry option A (four-stage wick still, the current design) or option B (single-effect tilted wick still) | (a) A; (b) B; (c) A with B's best idea grafted on (a glass cover over the absorber, see SSK-OPT-001) | **No pick.** The options score 152 and 153 of 220, within 10 %, so both go to Amish (STANDARDS section 21). A makes 2.8 times the water per panel; B is simpler, safer to maintain and cheaper per panel but needs about 2.6 panels for a household's 10 L. The repo stays on A until Amish decides | [SSK-DDR-004](decisions/0004-concept-selection.md), SSK-OPT-001 |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The manifold channel is about 56 x 50 mm with a snap-on lid that can be slotted | Sets the tongue bends and the lid slots (sketch SSK-DWG-114) | SSK-DDR-003 |
| 2 | The brine gutter is about 70 x 40 mm and the trough about 70 x 70 mm, with fascia brackets that fit it | Sets the outlet bracket length and the trough position | SSK-DDR-003 |
| 3 | The stone wool board has a compressive strength of 10 kPa or more | The glazing edge and its trim press on the liner tops | SSK-DDR-003 |
| 4 | The twin-wall sheet can be cut to 1,060 mm square with the flutes running down the slope, and breather tape is available for the flute ends | Drainage of condensate and rain from the flutes | SSK-PRC-001 |
| 5 | 7 mm PPS sheet (the stage 1 and 2 rail polymer, decided 2026-10-02) is sold in strips or small sheets | The rails and stop blocks are cut from it | SSK-DDR-002 |
| 6 | The coating and the high-temperature silicone adhesive bond to each other and to bare aluminium | The fins are bonded under the bottom plate; the chevron dams sit on the coating | SSK-DDR-003 |
| 7 | A quote for the 7 mm PPS sheet (BOM line 6 is priced at a distributor list price of about USD 70 per kg, not a quote) | The rails cost about USD 46 for four at that price | SSK-DEC-001 |
| 8 | The coater supplies an NSF/ANSI 61 or equivalent drinking-water certificate for the fluoropolymer coating in hot salty water, rated to 150 °C dry | Decides whether plates 1 and 2 keep the coating or move to 316 stainless | SSK-DEC-001 |

## Value engineering

Value-engineering target: USD 355 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 460.70 (USD 105.70 over the target), after the stage 3 PPS rails of D-01 (USD 16) and the panel label of D-05 (USD 1.50, 2026-10-25). Main cost drivers and savings worth trying:

- The largest lines are the five coated aluminium plates (USD 128 together, lines 3 and 5), the side rails (USD 76, line 6), the frame and liner (USD 35), the glazing (USD 32), the stand (USD 28) the glazing trim and tape (USD 20) and the 40 wick clips (USD 14, now 5052 aluminium at the stainless price as an estimate, D-08).
- The decisions of 2026-10-02 added USD 27: PPS rails at list price (USD 10), the wick clips (USD 14) and the labels (USD 3).
- Making the design constructable added USD 65: larger plate blanks for the tongues (USD 20), the glazing trim and tape (USD 20), the stand's ground frame, gussets and pins (USD 7), brackets for the trough and outlets (USD 10), the feed closure (USD 6) and longer wicks (USD 2).
- Savings worth trying: nest the plates' tongues when ordering cut sheet so the blank is nearer 1.0 x 1.1 m (about USD 10); fold the trim from aluminium flashing instead of buying angle (about USD 8); silicone strip in place of the 150 °C polymer rails in stages 1 and 2 (about USD 14, from SSK-DDR-002) is not a saving to take, because it would undo the R8 materials decision (SSK-DDR-002, item 2) and the PPS rails decided on 2026-10-02; move the brine gutter closer to the manifold to shorten the brine tongues; reclaimed timber for the stand; a locally made stagnation cover.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-10-25 | **D-04.** Plate alloy (STEM row S21): option (a), keep 3003 or 1050 plates, with 1050 preferred where both are offered (Dumitrascu et al. 2016), and a corrosion coupon test of plate, wick and clip in hot brine added to the TRL 4 plan; 5052 marine aluminium (b) is the change if the coupons show crevice attack | Amish: "i concur with your recommendations" | SSK-STM-001 S21; BOM lines 3 and 5; SSK-PLN-001 |
| 2026-10-25 | **D-05.** Inner glazing margin (STEM row S13, 113 °C calm against 120 °C): option (a), keep the twin-wall polycarbonate with the stagnation cover and shade rule as the barrier, and write the cover rule on a panel label (BOM line 19, one more label, USD 1.50) | Amish: "i concur with your recommendations" | SSK-STM-001 S13; BOM line 19; SSK-BLD-001 |
| 2026-10-25 | **D-06.** Bolt lengths of D-02: keep (pivot bolts M10 x 75, prop foot pins M10 x 120), as modelled on 2026-10-24 | Amish: "i concur with your recommendations" | D-02 below; SSK-BLD-001 |
| 2026-10-25 | **D-08.** Wick clip material (STEM row S30): option (a), clips bent from 5052-H32 aluminium strip 0.4 x 8 mm, same shape and hand tools, in place of the 304 stainless chosen on 2026-10-02, so no galvanic couple with the plates; price of 5052 strip to confirm (BOM line 18 keeps the stainless basis as an estimate) | Amish: "i concur with your recommendations" | SSK-STM-001 S30; BOM line 18; `cad/src/model.py`; SSK-DWG-111 Rev P3, SSK-DWG-119 and 120 Rev P2, SSK-DWG-002 Rev P6 |
| 2026-10-25 | **D-09.** Wind anchoring (STEM row S16, PR-013): option (a), the four stakes or 40 kg of ballast are a hold point in the build plan and PR-013 is stated for the anchored stand (28.8 m/s with the ballast; about 6 N hold-down on each rear stake at 17 m/s); stake pull-out in soft or sandy ground checked at TRL 5 | Amish: "i concur with your recommendations" | SSK-PRS-001 v0.10 PR-013; SSK-CAL-001 v0.9 section 9; SSK-BLD-001 safety stops S4, S5 |
| 2026-10-25 | **D-10.** PR-002: option (a), the target restated as a gained output ratio of 1.2 or more for four stages; met on paper at 1.22 after warm-up | Amish: "i concur with your recommendations" | SSK-PRS-001 v0.10 PR-002; SSK-CAL-001 v0.9 section 4 |
| 2026-10-24 | **D-01.** Stage 3 side rails in PPS (as stages 1 and 2) instead of printed polycarbonate. STEM row S11 failed: stage 3 reaches 110 °C at calm-air dry stagnation and printed PC softens at 113 °C (ISO 75 at 0.45 MPa, a short-term figure), so no continuous rating with a 10 K margin. Options weighed: (a) PPS rails, USD +16 (two at USD 11.50 for two at USD 3.50), same section, cut not printed, one rail colour for stages 1 to 3; (b) a high-temperature printed polymer (PEI or PEKK) needs a heated-chamber printer beyond the "hand tools and a 3D printer" scope; (c) accept the 0 K margin and rely on the cover alone. Chosen (a), best for the design and its constructability. Stage 4 (91 °C) keeps printed PC. Amish can reverse it | Under Amish's standing instruction of 2026-10-23 ("when a STEM check row fails, propose and implement the best fix ... in the same session") | SSK-STM-001 S11; BOM line 6; SSK-CAL-001 v0.7 |
| 2026-10-24 | **D-07.** Bottom plate underside and fins painted with the absorber's high-temperature matte black (emissivity about 0.90 in place of 0.10 for bare aluminium). The independent review showed that SSK-CAL-001 gave the sheltered underside a 5 W/m2K convection floor (a laminar flat plate gives about 2.8 W/m2K); corrected, the bare design made 9.2 L after warm-up (PR-001 not met) and reached 150 °C at calm stagnation (STEM row S7 failed). Options weighed: (a) paint, +1.1 L and -8 K at stagnation, extra paint only, no dimension changes; (b) 50 mm fins, +0.3 L, more aluminium and a dimension change; (c) six stages, a scope change. Chosen (a); the fin flanges are masked where they bond. Amish can reverse it | Under Amish's standing instruction of 2026-10-23 | SSK-STM-001 S7; SSK-CAL-001 v0.8; BOM line 11 |
| 2026-10-24 | **D-02.** Bolt lengths corrected from the detailed model: pivot bolts M10 x 75 (were 70, which left 0.6 mm of thread past the nut over the 57 mm post and wall); prop foot pins M10 x 120 (were 100, which cannot take washers and a nut on the 90 mm prop and rail), because the 10 and 15 deg holes lie under the gussets and the pin goes through the gusset there (grip 102 mm, the same bolt as the hinge). No design dimension of a part changes; the gussets gain two holes each | Made in the model under the intent of the standing instruction of 2026-10-23; open for Amish's review (D-06) | SSK-BLD-001 v0.4; this register |
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
