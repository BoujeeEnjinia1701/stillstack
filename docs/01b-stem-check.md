---
doc_id: SSK-STM-001
title: StillStack STEM check
project: StillStack
doc_type: STEM check
version: '0.2'
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-24'
    author: Amish Chadha
    change: "First STEM check (kit 1.9.1 upgrade) of option A (the current design) and option B; S11 failed and is closed by SSK-DEC-001 D-01; independent review recorded: S7 failed and is closed by D-07, S16 and S30 have fixes proposed to Amish (D-09, D-08), rows S29 to S34 added"
  - version: '0.2'
    date: '2026-10-25'
    author: Amish Chadha
    change: 'Amish''s decisions of 2026-10-25: S30 within known science with 5052 aluminium clips (D-08); S16 restated for the anchored stand (D-09); S13 and S21 closing routes (D-05, D-04); 28 within, 10 plausible, 0 fail'
---

# StillStack STEM check

Verdict: the four-stage wick still (option A) sits within known science on its working principle: energy balance, gap heat and mass transfer, heat rejection, stagnation, structure and salt, and no row fails outright. Four rows failed during this check, each on a detail. Two are closed by fixes made under Amish's standing instruction of 2026-10-23: printed polycarbonate rails in stage 3 meet 110 °C at calm-air stagnation against a 113 °C softening point, so the stage 3 rails are now PPS (S11, SSK-DEC-001 D-01); and the independent reviewer showed that the calculation note over-credited the underside's convection, so the underside and fins are now painted black (S7, D-07), which keeps the yield at 10.3 L/m2/day. Two had fixes proposed to Amish because they reverse a decision of his or trade off safety, and he decided both as recommended on 2026-10-25 ("i concur with your recommendations"): the 304 stainless wick clips formed a galvanic couple with the aluminium plates in hot brine, so the clips are now 5052 aluminium (S30, D-08); and the unanchored stand tips at about 16.5 m/s of wind, so anchoring by the four stakes or 40 kg of ballast is a hold point and PR-013 is stated for the anchored stand, which holds to about 28.8 m/s with the ballast (S16, D-09). Ten rows stay **Plausible, to confirm**, among them the wick's permeability and heat rating, the coating certificate, crevice corrosion, brine drip and drop bridging, scaling and the glazing's solar transmittance, so `stem_check` is **open**. Option B (single-effect tilted wick still) is within known science, with its wick stagnation row plausible. Method: STANDARDS section 20. Calculations: `docs/04-calcs/stem_check.py`, which takes the CAL figures from `docs/04-calcs/sizing.py` (SSK-CAL-001 v0.8) and checks each with an independent first-order estimate where one exists; rows S1 and S2 are labelled consistency checks, because they restate the solver's balance.

## Claims checked

Table 1. Claims, governing science and verdicts (generated from `docs/04-calcs/stem_results.csv` by `stem_check.py`; rows S1 to S34 are option A, B1 to B4 option B).

<!-- STM_TABLE -->
| # | Claim | Field | Branch | Governing law or source | First-order check | Verdict | Closed by |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | Consistency check: stage 1 takes no more heat than the absorber keeps after top and edge losses (10.5 of 15.1 MJ/m2 absorbed) | Physics | Thermodynamics | First law at the absorber node; a check of the solver's integration, not an independent result (independent review) | in 15.05 MJ/m2, out 15.16 MJ/m2 | Within known science | Open |
| S2 | Consistency check: stage 2 takes in no more than the heat crossing gap 1 (9.1 of 9.2 MJ/m2) | Physics | Thermodynamics | First law: heat into stage 2 is the latent, conducted, radiated and rib heat crossing gap 1, less edge loss (like quantities) | in 9.176 MJ/m2, out 9.142 MJ/m2 | Within known science | Open |
| S3 | Gained output ratio 1.29 quasi-steady (1.22 after warm-up) is below the ideal limit for four stages | Physics | Thermodynamics | Ideal multi-effect still: GOR <= N x tau x alpha (every effect reuses all the heat, no losses) | 1.29  <= 3.04  | Within known science | Open |
| S4 | Daily distillate 10.3 L/m2 (10.9 L quasi-steady) on a 5.5 kWh/m2 day (an upper-bound screen only) | Physics | Thermodynamics | Multi-effect upper bound: N stages x single-stage evaporation limit at tau alpha (limits.evaporation_kg_per_m2_day) | 10.9 L/m2/day <= 24.77 L/m2/day | Within known science | Open |
| S5 | Latent flux across a 6 mm gap with 5 K across it is about 362 W/m2 at a 60 C brine-wet wick face (water activity 0.972) | Physics | Heat transfer | Fick diffusion with the Stefan flow correction, independent property fits; cf. Chiavazzo et al. 2018 | claimed 362 W/m2, estimate 328 W/m2 (ratio 1.10) | Within known science | Open |
| S6 | Conduction across the still 6 mm gap is about 23 W/m2 at 5 K (Nu = 1, heated from above) | Physics | Heat transfer | Fourier conduction, k air 0.028 W/mK; stable stratification (Incropera, ch. 9) | claimed 23.4 W/m2, estimate 23.3 W/m2 (ratio 1.00) | Within known science | Open |
| S7 | Painted fins and underside reject the peak 286 W/m2 at 25 K above ambient (effective 11.5 W/m2K per m2 of aperture) | Physics | Heat transfer | Downward-facing natural plus laminar forced convection over the finned area, radiation at emissivity 0.90 (Incropera) | claimed 11.5 W/m2K, estimate 11.6 W/m2K (ratio 0.99) | Within known science | SSK-DEC-001 D-07 (painted underside and fins; CAL v0.8) |
| S8 | Dry stagnation holds the absorber near 138 C (142 C in calm air) at 1,000 W/m2 and 35 C | Physics | Heat transfer | Absorbed flux = (U top + U down) x rise; U top about 5.5 W/m2K, four dry gaps and the fins in series below | claimed 103 K above ambient, estimate 90.7 K above ambient (ratio 1.14) | Within known science | Open |
| S9 | 0.5 mm plates sag about 0.5 mm between ribs at 194 mm pitch, under one sixth of the 6 mm gap | Physics | Strength of materials | Simply supported strip, w = 5 q L^4 / 384 E I, aluminium E 69 GPa, 22.6 N/m2 | 0.52 mm <= 1 mm | Within known science | Open |
| S10 | A plate grows about 1.4 mm across 1 m at a 60 K rise, inside the 2 mm clearance each side | Physics | Strength of materials | Linear expansion, aluminium 23e-6 /K | 1.38 mm <= 4 mm | Within known science | Open |
| S11 | Stage 3 side rails survive calm-air dry stagnation (107 C) with at least 10 K margin | Physics | Strength of materials | Long-term service temperature in air: PPS 218 C (Mitsubishi Chemical Tecatron 1000 PPS); printed PC softens at 113 C (ISO 75, 0.45 MPa) | 117 C <= 218 C | Within known science | SSK-DEC-001 D-01 (PPS rails in stage 3) |
| S12 | Stage 1 and 2 PPS rails and silicone ribs survive 142 C calm-air stagnation | Physics | Strength of materials | PPS long-term service 218 C (datasheet); silicone rubber cord rated about 200 C (supplier class) | 152 C <= 200 C | Within known science | Open |
| S13 | The inner twin-wall glazing sheet stays below its service limit at calm-air stagnation (113 C) | Physics | Strength of materials | Twin-wall polycarbonate service temperature -40 to 120 C (Multicraft TW6C624 data) | 113 C <= 120 C | Plausible, to confirm at TRL 3 | Kept with the stagnation cover and shade rule as the barrier, the rule on the panel label (SSK-DEC-001 D-05, decided by Amish 2026-10-25) |
| S14 | M10 pivot bolt bearing on 12 mm plywood is about 1.4 MPa with the wet panel and 17 m/s wind | Physics | Mechanics and statics | Embedment strength of plywood f_h = 0.11 (1 - 0.01 d) rho_k (EN 1995-1-1, eq. 8.20), rho_k 500 kg/m3 | 1.4 MPa <= 49.5 MPa | Within known science | Open |
| S15 | A 45 x 45 mm timber prop, 1.0 m pinned, does not buckle under the panel and wind load (about 0.4 kN) | Physics | Mechanics and statics | Euler buckling, softwood E 8 GPa | 0.4 kN <= 26.98 kN | Within known science | Open |
| S16 | Anchored (four stakes or 40 kg of ballast, a hold point), the panel and stand do not tip below 17 m/s of wind (PR-013); unanchored it tips at 16.5 m/s | Physics | Mechanics and statics | Moment balance about the front end of the ground frame: normal force 0.5 rho v^2 Cf A (Cf 1.2) at the panel centre against the wet weight plus 40 kg of ballast at the rear of the ground rails | 17 m/s <= 28.8 m/s | Within known science | SSK-DEC-001 D-09 (decided by Amish 2026-10-25); stake pull-out in soft or sandy ground to check at TRL 5 |
| S17 | A 1 mm wick carries the 1.44 kg/h per metre of width that stage 1 needs at noon if its permeability is 3.0e-11 m2 or more | Physics | Fluid mechanics | Darcy flow, gravity along 20 deg plus 4 kPa capillary pressure (SSK-CAL-001 section 6) | Needed 3.0e-11 m2; permeability of the shortlisted fabrics not yet measured (wicking-rise test, SSK-DEC-001) | Plausible, to confirm at TRL 3 | Open |
| S18 | The gravity feed needs no pump: the trough rim is at most 1.00 m above the ground at 35 deg | Engineering and technology | Power and link budgets | Hydrostatic head from a user-filled container at most 1.5 m (R5) | 1 m <= 1.5 m | Within known science | Open |
| S19 | Brine leaves at 66.7 g/L from 40 g/L feed at a feed ratio of 2.5, so salt stays in solution | Chemistry | Physical chemistry | Salt mass balance; NaCl saturation about 317 g/L of solution at 25 to 80 C (CRC Handbook) | 66.7 g/L <= 317 g/L | Within known science | Open |
| S20 | Dissolved salt does not evaporate with the vapour, so distillate salinity comes only from liquid carryover | Chemistry | Physical chemistry | Raoult's law; NaCl is non-volatile at still temperatures | The 8.2 mL/day of SSK-CAL-001 section 7 is an allowance for 50 mg/L, not a computed carryover (rows S29, PR-003); volatile organics can carry over (PRC safety) | Within known science | Open |
| S21 | Bare 3003 or 1050 aluminium plate undersides survive contact with hot (60 to 80 C) brine-wet wicks for years | Chemistry | Electrochemistry and batteries | 3000 and 5000 series aluminium resists seawater to 125 C; crevice corrosion under gaskets is the main concern (Kappes 2017); 1050 resists better than 3003 (Dumitrascu et al. 2016) | The wick under its clips is a crevice in 58 to 67 g/L brine; no crevice rate at 60 to 80 C found; a perforation would let brine reach the distillate face | Plausible, to confirm at TRL 3 | Corrosion coupon test in the TRL 4 plan, 1050 preferred over 3003; 5052 plates if the coupons show crevice attack (SSK-DEC-001 D-04, decided by Amish 2026-10-25) |
| S22 | The fluoropolymer coating on the condensing faces is food-contact safe in hot salty distillate and tolerates 150 C dry | Chemistry | Materials and polymer chemistry | PTFE and PFA are stable well above 150 C; drinking-water contact needs an NSF/ANSI/CAN 61 or equivalent certificate | Coating class chosen, certified product not yet seen (SSK-DEC-001, to confirm item 8) | Plausible, to confirm at TRL 3 | Open |
| S23 | Distillate is a raw product and is not claimed safe to drink without testing and disinfection | Biology | Microbiology | WHO Guidelines for Drinking-water Quality, 4th ed. with first and second addenda (2022) | Stages run at 58 to 80 C, below pasteurization certainty; brine carryover can carry microbes; test (conductivity, E. coli) and disinfect (PRC safety) | Within known science | Open |
| S24 | Long-term drinking of distillate needs remineralization; low dissolved solids are not a health target | Biology | Human physiology and biomechanics | WHO, Nutrients in Drinking Water (2005), on demineralized and desalinated water; WHO TDS fact sheet: no health-based value | 50 mg/L is used as a carryover check only (PRS PR-003) | Within known science | Open |
| S25 | The wick fabric tolerates 150 C dry without losing its wicking, and conducts like the k 0.45 W/mK the CAL assumes | Chemistry | Materials and polymer chemistry | Polyester nonwovens soften well below their 250 C melt; glass-fibre fabric is stable far above 150 C; cellulose (cotton, viscose) degrades with time at 140 C | Fabric chosen by the wicking-rise test between a polyester-type nonwoven and a glass-fibre fabric (SSK-DEC-001, 2026-10-02); the CAL's k and dry mass are cotton or viscose values | Plausible, to confirm at TRL 3 | Open |
| S26 | The design-day integration is resolved in time: halving the 15 min step moves the daily yield by under 1 % | Mathematics | Numerical method | Quasi-steady fsolve over a 10 h sine day (SSK-CAL-001 section 1); noon solution converged: True | 0.037 % <= 1 % | Within known science | Open |
| S27 | 10.3 L/m2/day is two to three times a single-basin still (3 to 5 L/m2/day) | Mathematics | Orders of magnitude | Basin still 3 to 5 L/m2/day (SSK-PRB-001) times a gained-output gain of 2 to 3 | claimed 10.3 L/m2/day, estimate 10 L/m2/day (ratio 1.03) | Within known science | Open |
| S28 | Vapour lost through the low-end tongue openings is about 25 mL/day (0.2 % of the yield) | Physics | Fluid mechanics | Fick diffusion through the openings, 4 gaps, 60 C inside, 30 C at 60 % RH outside | claimed 25 mL/day, estimate 22.7 mL/day (ratio 1.10) | Within known science | Open |
| S29 | Brine does not drip from the wick onto the condensing face below, and condensate drops do not bridge the 6 mm gap to the wick | Physics | Fluid mechanics | Capillary retention in an unsaturated wick; sessile drops on a 20 deg face slide at a few mm (capillary length 2.7 mm), below the 6 mm gap | A wick fed past its capacity or a hydrophobic (fluoropolymer) face holding pinned drops could carry brine across; per-stage conductivity at TRL 4 decides | Plausible, to confirm at TRL 3 | Open |
| S30 | The 5052 aluminium wick clips survive in hot brine and do not attack the aluminium plates | Chemistry | Electrochemistry and batteries | Galvanic series in seawater: stainless steel is about 0.5 V nobler than aluminium, so the 304 clips first chosen drove aluminium corrosion; 5052 is a marine alloy within the same aluminium group as 1050 and 3003, so the couple is negligible | The clips touch bare plate in 58 to 67 g/L brine at 60 to 80 C. Fixed by D-08 (a), decided by Amish 2026-10-25: clips bent from 5052-H32 strip 0.4 x 8 mm, same shape; the crevice under the clip stays with S21 and the TRL 4 coupon test | Within known science | SSK-DEC-001 D-08 |
| S31 | Carbonate and sulphate scale on the wicks stays within weekly rinsing | Chemistry | Inorganic chemistry | Seawater concentrated 1.7 times at 60 to 80 C exceeds calcium carbonate saturation; calcium sulphate stays below saturation at that factor | Scale rate not computed; the weekly rinse (PR-010) and a vinegar soak are the controls; the wicking-rise test should be repeated on a scaled wick | Plausible, to confirm at TRL 3 | Open |
| S32 | Adhesives, glazing tape and sealant survive their stagnation temperatures | Chemistry | Materials and polymer chemistry | High-temperature silicone adhesives and sealants are commonly rated about 200 to 260 C; the fins sit at about 64 C, the tape under the glazing edge near the inner sheet (113 C calm) | Products not yet named; check each datasheet when buying (SSK-DEC-001, to confirm item 6) | Plausible, to confirm at TRL 3 | Open |
| S33 | The glazing passes about 0.80 of the sun (solar-weighted, with incidence and dust losses) | Physics | Optics and radiation | The 80 % of the source is a light transmission; solar-weighted values with incidence-angle loss and soiling are likely 0.72 to 0.78 (independent review) | At 0.75 the design day gives 10.1 L quasi-steady (CAL sensitivity), so PR-001 is met only near 0.80; measure the sheet at TRL 4 | Plausible, to confirm at TRL 3 | Open |
| S34 | Brine lowers the wick's vapour pressure (water activity 0.972 at the mean wick salinity of 47 g/L), now in the CAL | Chemistry | Physical chemistry | Raoult's law with an osmotic coefficient of 0.93 for NaCl (CAL v0.8, added after the independent review) | 0.972  <= 1  | Within known science | Open |
| B1 | Option B makes about 3.8 L/m2/day at an assumed (not computed) 45 % daily efficiency on the 5.5 kWh/m2 day | Physics | Thermodynamics | Single-effect limit: evaporation <= tau alpha x sun / h_fg (limits.evaporation_kg_per_m2_day) | 3.8 L/m2/day <= 6.372 L/m2/day | Within known science | Open |
| B2 | Option B yield of 3.8 L/m2/day matches tilted wick stills in the literature | Mathematics | Orders of magnitude | Sharon et al., tilted wick and basin still, 4.54 and 4.99 L/m2/day (cited in Agrawal and Rana 2019) | claimed 3.8 L/m2/day, estimate 4.77 L/m2/day (ratio 0.80) | Within known science | Open |
| B3 | Option B wick survives dry stagnation (about 141 C) only with a 150 C fabric | Physics | Heat transfer | Absorbed flux = (U top 6.5 + U back 0.9) x rise, single glazing | 141 C <= 150 C | Plausible, to confirm at TRL 3 | Open |
| B4 | Condensate runs down the underside of a 20 deg glass cover to the low-edge gutter as a film | Physics | Fluid mechanics | Clean glass is wetted by water (low contact angle), so film-wise condensation drains along the slope; standard in tilted stills | 20 deg is above the 10 to 15 deg usually needed for drops to run on clean glass | Within known science | Open |
<!-- /STM_TABLE -->

Verdicts: **Within known science**, **Plausible, to confirm at TRL 3**, **Fails, fix proposed**, **Fails**.

### Row S11: failed, fixed and closed

At first run S11 checked the printed polycarbonate rails of stage 3: the plate above stage 3 reaches 110 °C at calm-air dry stagnation (SSK-CAL-001 section 5), and printed polycarbonate softens at 113 °C (ISO 75 at 0.45 MPa, Prusament PC Blend). A softening point is a short-term figure, so with the 10 K margin used for every rail row the check failed (120 °C against 113 °C). The fix keeps the working principle and the section: the stage 3 rails are cut from the same 7 mm PPS as stages 1 and 2 (long-term service 218 °C), at USD 16 more (BOM line 6). It was decided on 2026-10-24 under Amish's standing instruction of 2026-10-23 and recorded as SSK-DEC-001 D-01; the model, BOM, CAL, PRS, build plan and drawings carry it. The rerun row checks the fixed design: 120 °C against 218 °C, within known science. Stage 4 peaks at 91 °C, 22 K under the polycarbonate softening point, so its printed rails stay.

### Row S7: failed in review, fixed and closed

The calculation note gave the sheltered underside a forced-convection floor of 5 W/m2K at 0.5 m/s and treated it as bare aluminium (emissivity 0.10). The independent reviewer computed about 2.8 W/m2K for a laminar flat plate at that speed, which matched this check's own independent estimate (a ratio of 1.77 to the CAL that should not have passed as within known science). With the convection corrected and the brine's water activity added, the bare design made 9.2 L after warm-up and reached 150 °C at calm-air stagnation. The fix keeps the principle and every dimension: the bottom plate's underside and the fins are painted with the absorber's high-temperature matte black (emissivity 0.90), decided under the standing instruction as SSK-DEC-001 D-07. The row now checks the painted design: 11.5 W/m2K claimed against 11.6 estimated.

### Rows S16 and S30: fixes decided by Amish (2026-10-25)

S16: unanchored, the panel and stand tip forward about the front end of the ground frame at about 16.5 m/s of wind from behind (SSK-CAL-001 section 9), under the 17 m/s of PR-013. The stakes are in the design and the build plan; whether to make anchoring the requirement or lengthen the frame is a safety trade-off (D-09). S30: 304 stainless clips on bare aluminium in 58 to 67 g/L brine at 60 to 80 °C form a galvanic couple that drives aluminium corrosion, and 304 can pit and stress-crack in hot chloride; the recommended aluminium clips reverse Amish's 2026-10-02 choice of stainless, so the fix is his (D-08). Amish decided both on 2026-10-25 as recommended: anchoring is a hold point in the build plan and PR-013 is stated for the anchored stand, which with 40 kg of ballast tips only at about 28.8 m/s (each rear stake needs about 6 N of hold-down at 17 m/s; pull-out in soft or sandy ground to check at TRL 5); and the clips are bent from 5052-H32 aluminium strip, same shape (S30 now within known science).

## Fields not relevant

Every field has at least one row. Within the fields, these branches are not relevant: electromagnetism and circuits (no electrical parts, PR-005); nuclear and ionising radiation (none); acoustics and vibration (no moving parts in service); ecology and agronomy beyond the brine note (brine discharge is covered as hazard H5 in SSK-RSK-001); epidemiology (no health claim is made; S23); control and sensing (passive, no control).

## Concept options

- **Option A, four-stage wick still (current design):** within known science; no outright Fails row; S7 and S11 closed by fixes (D-07, D-01); S16 and S30 closed by the fixes Amish decided on 2026-10-25 (D-09, D-08); ten plausible rows (material confirmations, margins and carryover paths, not the principle).
- **Option B, single-effect tilted wick still:** within known science (B1, B2, B4); B3 plausible: its black wick reaches about 141 °C at dry stagnation, so it needs the same 150 °C fabric as option A. Its yield of about 3.8 L/m2/day is within the single-effect limit and close to tilted wick stills in the literature.

## Independent review

A separate reviewer agent saw only this check's claims, the calculation note SSK-CAL-001, the product requirements SSK-PRS-001 and `sizing.py`, not the author's reasoning, and tried to refute the headline results and every "Within known science" verdict. Its findings and the changes made are recorded below.

Reviewer: a second Claude instance run headless from the command line (`claude -p`, tools disabled), because the Agent tool was not available in this session; it saw only this document as it stood before the review, SSK-CAL-001, SSK-PRS-001 and `sizing.py`. Its verdicts and the changes made:

Table 2. Independent review findings and responses.

| Item | Reviewer's finding | Response |
| --- | --- | --- |
| Headline yield 10.6 L | Weakened: the underside convection floor of 5 W/m2K is optimistic (about 2.8 for a laminar plate), the brine's water activity is ignored, and τ = 0.80 is a light, not solar, transmittance; net 9 to 10 L | CAL corrected (laminar plate, a_w 0.972); D-07 paints the underside and fins (S7 closed); τ = 0.75 added as a sensitivity (10.1 L quasi-steady) and as row S33; PR-001 now 10.3 L, at risk |
| Gained output ratio 1.26 to 1.34 | Weakened: inherits the yield risks, plausibly 1.1 to 1.25 | Now 1.22 to 1.29; PR-002 restated as 1.2 or more by Amish on 2026-10-25 (D-10), met on paper |
| Stagnation 140 and 144 °C | Upheld as a number, weakened as a margin; sensitive to the bottom h, 40 °C ambient and 1,100 W/m2 | Painted underside lowers it to 138 and 142 °C; 40 °C and 1,100 W/m2 cases added to CAL section 5 (151 °C and 121 °C glazing at 1,100 W/m2); PR-008 stays at risk |
| Mass 18.8 kg and cost USD 459.20 | Mass upheld (6 % margin, 2.4 kg of allowances); cost weakened by an apparent PPS price conflict | No change: the four stage 1 and 2 rails were already priced at USD 11.50 each on 2026-10-02 (USD 46, the "USD 10" was the rise over a USD 9 allowance), so USD 11.50 for stage 3 is consistent |
| S1, S2 circular | S1 restates the solver; S2 compares unlike quantities | Both relabelled consistency checks; S2 now compares the heat crossing gap 1 with the heat into stage 2 |
| S3, S4, S27 low power | Upheld, but the bounds are loose | Kept as screens; S4 relabelled an upper-bound screen |
| S7 | Refuted: a 1.77 ratio is not within known science | Accepted; fixed by D-07 and closed (see above) |
| S8 | Weakened: passes only through a conservative top U | Kept; the CAL harsher cases now carry the margin question |
| S9 | Upheld, small mismatch (0.58 against 0.52 mm) | The check now uses the plate stiffness E t^3/12(1 - ν^2), as the CAL: 0.52 mm |
| S11 | Upheld for PPS; other stage 3 materials unchecked | Adhesives, tape and sealant added as S32; wick and coating are S25 and S22 |
| S13 | Closure by the CAL is circular | Closure removed; the row stays open (D-05) |
| S16 | Weakened: tipping, not lift, governs, near 16 to 17 m/s | Replaced by a tipping moment check: 16.5 m/s, fix proposed to Amish (D-09) |
| S19 | Weakened: NaCl only; carbonate and sulphate scale likely | Scaling added as S31 (plausible) |
| S20 | Weakened: 8.5 mL is an allowance; drops on a hydrophobic face may bridge to the wick | S20 reworded as an allowance; brine drip and drop bridging added as S29 (plausible) |
| S24 | Wrong source | Now cites WHO, Nutrients in Drinking Water (2005) |
| B1 | The 3.8 L comes from an assumed efficiency | Reworded as assumed, not computed |
| Missing claims | Stainless clips and galvanics, wick fabric k and cellulose at 144 °C, scaling, drop bridging, adhesives, tipping | Added as S30 (fix proposed, D-08), S25 (extended), S31, S29, S32 and S16 |
| Not modelled | Wick-to-plate contact resistance and conduction out through tongues and trim | Named in CAL section 1 as unmodelled risks; part of why PR-001 is at risk |
| Upheld | S5, S6, S10, S12, S14, S15, S18, S23, S26, S28, B2, B4 | No change |


## Sources

- Agrawal, Abhay, and R. S. Rana. "Theoretical and Experimental Performance Evaluation of Single-Slope Single-Basin Solar Still with Multiple V-Shaped Floating Wicks." *Heliyon* 5, no. 4 (2019): e01525 (cites Sharon et al., tilted wick and basin still, 4.54 and 4.99 L/m2/day). https://pmc.ncbi.nlm.nih.gov/articles/PMC6479174 (checked 2026-10-24).
- Chiavazzo, Eliodoro, and others. "Passive Solar High-Yield Seawater Desalination by Modular and Low-Cost Distillation." *Nature Sustainability* 1 (2018): 763 to 772. https://doi.org/10.1038/s41893-018-0186-x.
- Dumitrascu, Valentin Marian, Camelia Staicu, and Lidia Benea. "Corrosion Behavior of 1050 and 3003 Aluminum Alloys Used in Naval Industry." Galati, 2016. https://gup.ugal.ro/ugaljournals/index.php/mms/article/view/1263 (checked 2026-10-24).
- Filament2Print. "Prusament PC Blend," softening temperature 113 °C (ISO 75, 0.45 MPa). https://filament2print.com/en/pc-polycarbonate/3457-prusament-pc-blend.html (checked 2026-10-24).
- Incropera, Frank P., and others. *Fundamentals of Heat and Mass Transfer.* 6th ed. Wiley, 2007 (conduction across a stratified layer, natural convection from a downward-facing heated plate).
- Kappes, Mariano. *Localized Corrosion of Aluminum Alloy 5052 for Desalination Service.* AMPP paper 9151, 2017 (3000, 5000 and 6000 series aluminium resist seawater to 125 °C; crevice corrosion is the main concern). https://store.ampp.org/localized-corrosion-of-aluminum-alloy-5052-for-desalination-service (checked 2026-10-24).
- Mitsubishi Chemical Advanced Materials. "Tecatron 1000 PPS" datasheet: maximum service temperature in air 218 °C, long term. https://www.polymershapes.com/wp-content/uploads/2020/04/Polymershapes_MitsubishiChemicalAdvancedMaterials_DataSheet-Tecatron-1000-PPS.pdf (checked 2026-10-24).
- Multicraft Plastics. "6 mm Clear Twinwall Polycarbonate, TW6C624": service temperature -40 to 248 °F (-40 to 120 °C), light transmission 80 %. https://multicraftplastics.com/product/TW6C624 (checked 2026-10-24).
- Standards Council of Canada. "NSF/ANSI/CAN 61 - 2023." https://scc-ccn.ca/standardsdb/standards/4032142 (checked 2026-10-24).
- World Health Organization. *Guidelines for Drinking-Water Quality*, 4th ed. incorporating the first and second addenda, 2022; and "Chemical Fact Sheets: Total Dissolved Solids." https://www.who.int/publications/i/item/9789240045064 (checked 2026-10-24).
- World Health Organization. *Nutrients in Drinking Water.* Geneva: WHO, 2005 (health risks of demineralized and desalinated water).
- CEN. *EN 1995-1-1* (Eurocode 5), equation 8.20, embedment strength of plywood.
- SSK-CAL-001, `docs/04-calcs/sizing.py`: every CAL figure quoted in Table 1.
