---
doc_id: SSK-PRS-001
title: StillStack product requirements and specifications
project: StillStack
doc_type: Product requirements and specifications
version: '0.10'
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-24'
  author: Amish Chadha
  change: First measurable requirements for TRL 2
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Add TRL 3 status from SSK-CAL-001; record decisions from SSK-DDR-001 (budget kept at $250, tilt stand, aperture); targets unchanged
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget top-up approved by Amish
- version: "0.6"
  date: '2026-10-01'
  author: Amish Chadha
  change: Status from the constructable design (SSK-DDR-003); R12 reported against the value-engineering target
- version: "0.7"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Decisions of 2026-10-02 noted under R4, R6, R7, R8 and R10 (lip, conductivity pass condition, fabric test, coating rule, PPS, wick clips); no status changed"
- version: "0.9"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Approved follow-ups carried into the design: R9 mass 18.7 kg, R12 USD 443.20 (USD 88.20 over the target), R4 lip modelled, R10 moves from at risk to met on paper (wick clips modelled)"
- version: "0.9"
  date: '2026-10-24'
  author: Amish Chadha
  change: "Kit 1.9.1 upgrade: REQ migrated to PRS (SSK-PRS-001; was SSK-REQ-001); R1 to R12 become PR-001 to PR-012 with the same targets, verification and status, traced to SSK-URS-001; PR-013 (wind) added from the CAL; PR-008 and PR-012 updated for the stage 3 PPS rails (SSK-DEC-001 D-01); status from SSK-CAL-001 v0.8 after the independent review (PR-001 at risk, PR-002 not met, PR-013 not met unanchored)"
- version: '0.10'
  date: '2026-10-25'
  author: Amish Chadha
  change: 'Amish''s decisions of 2026-10-25 ("i concur with your recommendations"): PR-002 restated as 1.2 or more for four stages (D-10), not met to met on paper; PR-013 stated for the anchored stand with anchoring a hold point and the cover rule on the panel label (D-09, D-05), not met to met on paper; PR-010 clips 5052 aluminium (D-08); PR-012 USD 460.70 with the panel label'
---

# StillStack product requirements and specifications

What the design must do, each requirement traced to a user need in SSK-URS-001. Targets are proposals for review with the co-design partner. Method: STANDARDS section 22. This document replaces SSK-REQ-001 (kit 1.8); each PR keeps the target, verification and status of the R it replaces, with the old number in "Was". Status comes from SSK-CAL-001 v0.7 and the STEM check SSK-STM-001.

No requirement is **not met**. PR-002 (gained output ratio) and PR-013 (wind) were not met after the independent review of the STEM check; Amish decided on 2026-10-25 ("i concur with your recommendations") to restate PR-002 as 1.2 or more for four stages (D-10) and PR-013 for the anchored stand, with anchoring a hold point (D-09), so both are now met on paper. One is **over target**: PR-012, parts cost USD 460.70 against the USD 355 value-engineering target (USD 105.70 over; Amish set budgets as value-engineering targets, not limits, on 2026-10-01). Five are **at risk** (PR-001, PR-004, PR-006, PR-007, PR-008) and one can only be verified at TRL 4 (PR-003). The underside and fins are now painted black (SSK-DEC-001 D-07), without which PR-001 would not be met. The stage 3 rails moved from printed polycarbonate to PPS on 2026-10-24 under Amish's standing instruction of 2026-10-23 (SSK-DEC-001 D-01, STEM row S11), which gives PR-008 a real margin in stage 3 and adds USD 16 to PR-012.

Table 1. Product requirements and specifications.

| ID | Traces to | Category | Title | Requirement | Target | Tolerance | Units | Verification | Status | Was |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR-001 | UR-001, UR-002 | Performance | Daily distillate | The panel shall produce at least the target distillate per m2 of aperture on a clear 5.5 kWh/m2 day (design goal 13 L) | 10 | min | L/m2/day | Analysis (SSK-CAL-001 section 4), TRL 3; outdoor test beside a basin still at TRL 4 | At risk: 10.3 L after warm-up (10.9 quasi-steady), 3 % margin, with the painted underside of D-07; 10.1 L quasi-steady at a glazing transmittance of 0.75; 13 L goal not met | R1 |
| PR-002 | UR-002 | Performance | Heat reuse | The daily gained output ratio (latent heat in the distillate over solar input) shall reach the target for four stages (restated from 1.3 by Amish, 2026-10-25, D-10) | 1.2 | min | ratio | Analysis (SSK-CAL-001 section 4), TRL 3 | Met on paper: 1.29 quasi-steady, 1.22 after warm-up (1.7 % margin); 1.20 at a glazing transmittance of 0.75 | R2 |
| PR-003 | UR-003 | Safety | Distillate salinity | Distillate conductivity shall not exceed the target (about 50 mg/L dissolved solids) for feed up to 40 g/L | 75 | max | µS/cm | Analysis of carryover paths (SSK-CAL-001 section 7), TRL 3; conductivity meter per stage at TRL 4 (pass condition before any water is drunk) | To verify at TRL 4: brine carryover must stay below 8.2 mL/day (0.075 %) | R3 |
| PR-004 | UR-004 | Safety | Brine separation | Every wick edge shall keep a physical air break from every distillate path, with no shared drain, and the outlets shall be labelled DISTILLATE and BRINE | 10 | min | mm | Inspection of the model (`model.py --check`), TRL 3; conductivity per stage at TRL 4 | At risk: 10 mm breaks at ribs, rails and plate edges, brine tails 10.5 mm over the closed lid and 44 mm from any distillate tongue, lip tabs on the high edges; carryover proven only by test | R4 |
| PR-005 | UR-005 | Performance | Passive operation | The panel shall run with no pump, electronics or battery, fed by gravity from a container no higher than the target above ground | 1.5 | max | m | Inspection of the design, TRL 3 | Met: passive; trough rim at most 1.00 m (at 35 deg) | R5 |
| PR-006 | UR-006 | Performance | Feed water | The panel shall accept feed up to 40 g/L after a 20 µm or cloth prefilter at a feed-to-distillate ratio of at least the target, and the wick shall carry that feed | 2.5 | min | ratio | Analysis (SSK-CAL-001 sections 6 and 7), TRL 3; wicking-rise test of the shortlisted fabrics | At risk: brine 66.7 g/L, far below saturation; wick permeability of 2.9e-11 m2 needed (3.0e-11 used for the test), not yet measured | R6 |
| PR-007 | UR-007 | Materials | Food-contact wetted parts | Every surface that touches distillate shall be food-contact rated (316 stainless, certified coated aluminium, PP, HDPE or NSF/ANSI 51 or 61 silicone) | 100 | min | % of wetted area | Review of the material list and certificates, TRL 3 | At risk: fluoropolymer coating class chosen; no named product with a drinking-water certificate seen (rule of 2026-10-02: else 316 stainless for plates 1 and 2) | R7 |
| PR-008 | UR-008 | Environment and durability | Dry stagnation | After an empty-wick day at 1,000 W/m2 and 35 °C, calm or windy, there shall be no damage: stages 1 and 2 rated to 150 °C or more, every other internal material to 110 °C or more, a stagnation cover supplied and a shade rule written | 150 | min (stages 1, 2); 110 elsewhere | °C | Analysis (SSK-CAL-001 section 5) and datasheets, TRL 3 | At risk: stages 1 and 2 reach 142 °C calm (8 K margin to the 150 °C rating, none at 1,100 W/m2; PPS rails long-term 218 °C); stage 3 reaches 107 °C calm, with PPS rails (SSK-DEC-001 D-01); inner glazing 113 °C against 120 °C (kept with the cover and shade rule as the barrier, D-05); wick and coating ratings not yet confirmed | R8 |
| PR-009 | UR-009 | Physical architecture | Household scale | 1.0 m2 aperture; panel dry mass no more than the target; footprint within 1.3 x 1.3 m | 20 | max | kg | Analysis (SSK-CAL-001 section 8) and model, TRL 3; weigh at TRL 4 | Met on paper: 18.8 kg dry (22.8 kg wet); footprint 1.28 x 1.25 m at 10 deg | R9 |
| PR-010 | UR-010 | Usability | Wick maintenance | One person shall remove, rinse and refit the wicks without special tools within the target; salt flushing no more often than weekly | 30 | max | min | Design review (build plan SSK-BLD-001), TRL 3; timed at TRL 4 | Met on paper: plates lift out once the low wall cap is off; wicks held by two 5052 aluminium clips each (D-08), no adhesive | R10 |
| PR-011 | UR-011 | Usability | Tilt range | The stand shall set the tilt from 10 deg to the target | 35 | max | deg | Model check at every hole (`model.py --check`), TRL 3 | Met: six prop holes, 10 to 35 deg in 5 deg steps | R11 |
| PR-012 | UR-012 | Physical architecture | Cost and buildability | Parts cost reported against the value-engineering target; buildable with hand tools, sheet-metal shears and a 3D printer | 355 | target | USD | Priced BOM (SSK-CAL-001 section 10), TRL 3 | Over target: USD 460.70 (USD 105.70 over), after the stage 3 PPS rails of SSK-DEC-001 D-01 (USD 16) | R12 |
| PR-013 | UR-013 | Safety | Wind and hot surfaces | Anchored by its four ground stakes or 40 kg of ballast, a hold point before the panel is filled or faces the sun, the panel and stand shall not tip or lift below the target wind speed; and the hot-surface rules (cover, shade rule) shall be in the instructions and on the panel label (restated by Amish, 2026-10-25, D-09) | 17 | min | m/s | Analysis (SSK-CAL-001 section 9), TRL 3; stake pull-out in soft or sandy ground at TRL 5 | Met on paper anchored: with 40 kg of ballast it tips at 28.8 m/s, and each rear stake needs about 6 N of hold-down at 17 m/s; unanchored it tips at 16.5 m/s (lift at 18.7 m/s), which the hold point excludes; cover BOM line 14, panel label BOM line 19 | New |

Categories: physical architecture, performance, materials, usability, packaging and transport, safety, electrical, software. Status: met on paper, met by design, at risk, not met, over target, withdrawn, to verify at TRL 4.

## Assumptions

- Design day: 5.5 kWh per m2 per day (19.8 MJ per m2) on the tilted aperture, 30 °C mean daytime ambient, light wind (1 m/s in SSK-CAL-001).
- Latent heat of vaporization: SSK-CAL-001 uses temperature-dependent values (about 2.33 to 2.36 MJ per kg over the stage range).
- The WHO does not set a health-based limit for dissolved solids; 50 mg/L is a check that salt carryover is negligible, not a potability limit.
- Household need of about 3 L per person per day for drinking and 2 L for cooking, so 10 to 11 L per day serves a household of two.
- The history of each target (R numbers, SSK-DDR-001 to SSK-DDR-003, SSK-DEC-001) is in the revision table above and in the review note.
