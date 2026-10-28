---
doc_id: SSK-CAL-001
title: StillStack sizing calculations
project: StillStack
doc_type: Calculation
version: '0.9'
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-09-25
    author: Amish Chadha
    change: First TRL 3 sizing (stage energy balance, supports, stagnation, wick feed, salt, mass, tilt, cost)
  - version: "0.2"
    date: 2026-09-25
    author: Amish Chadha
    change: Recommendations accepted by Amish (DDR-002)
  - version: "0.3"
    date: 2026-09-26
    author: Amish Chadha
    change: Budget top-up approved by Amish
  - version: "0.4"
    date: 2026-10-01
    author: Amish Chadha
    change: Design for construction (SSK-DDR-003); constructability checks; budget treated as a value-engineering target
  - version: "0.5"
    date: '2026-10-02'
    author: Amish Chadha
    change: "SSK-DDR-003 accepted (2026-10-02); R4, R7 and R10 rows note the decisions; figures unchanged"
  - version: "0.6"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Approved follow-ups carried in: lip tabs, wick clips, PPS rails and stop blocks, labels; mass 18.7 kg dry, cost USD 443.20; R10 moves from at risk to met on paper"
  - version: "0.7"
    date: '2026-10-24'
    author: Amish Chadha
    change: "Kit 1.9.1 upgrade: stage 3 rails in PPS (SSK-DEC-001 D-01, STEM row S11); rail polymer checks added; mass 18.8 kg dry, cost USD 459.20; foot pins and pivot bolts lengthened (D-02); requirements quoted as PR numbers (SSK-PRS-001)"
  - version: "0.8"
    date: '2026-10-24'
    author: Amish Chadha
    change: "Independent review (SSK-STM-001): underside convection corrected (laminar flat plate, no 5 W/m2K floor), brine water activity added; underside and fins painted black (SSK-DEC-001 D-07); yield 10.3 L, GOR 1.22 to 1.29 (PR-002 not met), stagnation 138 and 142 C; tipping check added (16.5 m/s, PR-013 not met unanchored); harsher stagnation and glazing-transmittance cases"
  - version: '0.9'
    date: '2026-10-25'
    author: Amish Chadha
    change: 'Amish''s decisions of 2026-10-25: PR-002 restated as 1.2 or more (D-10), met on paper; PR-013 anchored, 28.8 m/s with 40 kg ballast, about 6 N per rear stake (D-09), met on paper; clips 5052 aluminium (D-08); panel label (D-05); cost USD 460.70'
---

# StillStack sizing calculations

On paper the design (four stages, 6 mm gaps, air-cooled fins painted black, 1 m2 at 20 deg) makes about **10.3 L per m2 per day** on the 5.5 kWh per m2 design day (10.9 L quasi-steady), with a gained output ratio of **1.22 to 1.29**. That meets PR-001 (R1) with a 3 % margin, meets PR-002 (R2) as restated by Amish on 2026-10-25 (1.2 or more for four stages, D-10) with a 1.7 % margin, and misses the 13 L design goal. Dry stagnation reaches about **138 °C** at stage 1 (**142 °C** in calm air). PR-008 (R8) asks for a 150 °C rating in stages 1 and 2 and 110 °C elsewhere, plus a stagnation cover; the margins are 8 K and 3 K, so PR-008 is **at risk**. Unanchored, the panel and stand tip forward at about **16.5 m/s** of wind from behind; PR-013 is stated for the anchored stand (D-09, decided by Amish on 2026-10-25), which with 40 kg of ballast tips at about **28.8 m/s**, so it is met on paper with anchoring a hold point. Value-engineering target: USD 355. Estimated cost of the constructable design: USD 460.70 (USD 105.70 over the target). The panel is 18.8 kg dry. Requirement numbers R1 to R12 are now PR-001 to PR-012 (SSK-PRS-001). Every number below is printed by `docs/04-calcs/sizing.py`; the geometry figures come from `cad/src/model.py`.

Three changes on 2026-10-24 (kit 1.9.1 upgrade) move the figures of v0.6. The stage 3 rails are PPS (SSK-DEC-001 D-01, STEM row S11). The independent review of the STEM check found two optimistic steps in this note, which are now corrected: the sheltered underside was given a forced-convection floor of 5 W/m2K at 0.5 m/s, where a laminar flat plate gives about 2.8 W/m2K, and the wick's vapour pressure ignored the brine (water activity 0.972 at the mean wick salinity). Corrected, the bare-underside design made only 9.2 L after warm-up (PR-001 not met) and reached 150 °C at calm-air stagnation. The fix, decided under Amish's standing instruction of 2026-10-23 (SSK-DEC-001 D-07), paints the bottom plate's underside and the fins with the same high-temperature matte black as the absorber (emissivity 0.90 in place of 0.10), which restores 10.3 L and lowers stagnation by 8 K.

## 1. Method

The script solves a quasi-steady energy balance of the stack every 15 minutes through a sinusoidal design day, then integrates.

- **Nodes.** Absorber plate, three intermediate condenser plates and the bottom plate (five plate temperatures), plus the four wet wick faces. Heat conducts from each plate through its 1 mm wick (k = 0.45 W/mK) to the wick face.
- **Vapor gap.** Latent transfer by Stefan diffusion of vapor through air, m = (P M D / R T d) ln((P - p_c)/(P - p_w)), with p_w = a_w p_sat(T_w) and a brine water activity a_w = 0.972 at the mean wick salinity of 47 g/L (ln a_w = -2 m φ M_w, osmotic coefficient 0.93); conduction through still air (the gap is heated from above and stably stratified, so Nu = 1); gray-body radiation between the wet wick (emissivity 0.95) and the condensing face (0.90); conduction through the ribs and rails.
- **Top loss.** Absorber to glazing across the 25 mm air layer (Hollands correlation for an inclined layer, plus radiation with emissivities 0.90), across the twin-wall cells (9.3 W/m2K, from a typical sheet U-value of 3.6 W/m2K less surface films), and from the outer sheet to wind (h = max(5, 8.6 V^0.6 / L^0.4)) and sky (Swinbank sky temperature).
- **Bottom.** Natural convection from a heated surface facing down at 70 deg from vertical (Fujii and Imura), combined (cube law) with laminar forced convection over a 1 m flat plate at half the free-stream speed (Nu = 0.664 Re^0.5 Pr^(1/3)); fin efficiency for 0.5 mm aluminum fins 30 mm deep; radiation from the painted underside (emissivity 0.90, SSK-DEC-001 D-07) to ground at ambient. Before v0.8 the forced term had a 5 W/m2K floor and the underside was bare (0.10).
- **Feed.** Each stage heats its own feed from ambient to the wick temperature at a feed-to-distillate ratio of 2.5, and that heat leaves with the brine.
- **Edges.** 12 mm plywood plus 25 mm foil-faced stone wool (k about 0.035 W/mK), U = 1.07 W/m2K, over the wall height of each stage.
- **Thermal mass.** Treated separately as a warm-up deduction, because the quasi-steady solution ignores it.

Not modelled, and named as risks in SSK-STM-001: contact resistance between the clipped wick and its plate (about 1 K per stage if equal to the wick's own resistance, independent review), heat conducted out through the tongues and trim, scaling of the wicks (S31), and a solar-weighted glazing transmittance below 0.80 (S33; at 0.75 the design day gives 10.1 L quasi-steady).

### Assumptions

- Design day: 5.5 kWh per m2 (19.8 MJ per m2) on the tilted aperture, spread as a sine over 10 h (peak 864 W/m2); ambient 30 °C; wind 1 m/s.
- Optics: twin-wall polycarbonate transmittance 0.80 and absorber absorptance 0.95, so τα = 0.76. The 0.80 is a light transmission from the sheet data; a solar-weighted value with incidence loss and dust may be 0.72 to 0.78 (STEM row S33).
- Latent heat varies with temperature (2.33 to 2.36 MJ per kg over the stage range).
- Wet wick area: wicks are cut into five strips with 10 mm dry breaks at each rib and rail (PR-004) and stop 13 mm inside the zigzag low edge, leaving 81.7 % of the aperture wet.
- The feed ratio is held at the PR-006 minimum of 2.5 to limit sensible loss.
- Properties of air and vapor use standard power-law fits; saturation pressure uses the Buck equation.

## 2. Vapor gap transfer

Most of the heat crossing each gap is latent, and the fraction rises steeply with temperature (Table 1). At the noon operating point the four stages run at 0.89, 0.86, 0.84 and 0.81.

Table 1. Heat flux across one 6 mm gap with 5 K between the wick face and the condensing face (brine-wet wick, a_w 0.972).

| Wick face (°C) | Latent (W/m2) | Conduction (W/m2) | Radiation (W/m2) | Evaporation fraction |
| --- | --- | --- | --- | --- |
| 40 | 132 | 22.3 | 29.2 | 0.72 |
| 50 | 219 | 22.9 | 32.1 | 0.80 |
| 60 | 362 | 23.4 | 35.2 | 0.86 |
| 70 | 609 | 24.0 | 38.5 | 0.91 |
| 80 | 1,092 | 24.6 | 42.0 | 0.94 |

## 3. Plate support and spacer ribs

A 0.5 mm aluminum plate carrying a wet wick cannot span the frame. Under 22.6 N/m2 (plate, 1.0 kg/m2 of wet wick and condensate, normal to the 20 deg slope), beam theory gives a sag of about 325 mm over the 0.972 m clear span, so the TRL 2 concept with side rails only would close every gap. Treating each strip as simply supported, a sag of 1.0 mm (one sixth of the gap) allows a pitch of up to 229 mm. **Four intermediate ribs per gap at 194 mm pitch** give a sag of 0.52 mm. The ribs run down the slope so they do not block feed or condensate. Each plate grows about 1.4 mm across 1 m at a 60 K rise, so the model leaves 2 mm of clearance each side instead of tensioning the plates.

**Support of the whole stack (SSK-DDR-003).** The stack rests on a 12 mm plywood base ring whose 15 mm ledge carries the bottom plate's edges and the side rails. The ribs carry their share of the stack (about 108 N/m2 normal to the plate at 20 deg) onto the bottom plate, which spans the 970 mm between the high and low ledges as ten fin-stiffened strips: with the fins bonded the sag is about 0.5 mm, and 1.0 mm if the fins carried the load alone (section 13). The whole stack moves together, so the gaps do not change. The wicks now stop 13 mm inside the plates' zigzag low edge, which lowers the wet wick fraction from 0.824 to 0.817; the change to the design-day yield is under 0.01 L.

The ribs are 7 mm food-grade silicone cord (decided by Amish on 2026-09-25, SSK-DDR-002): silicone is rated well above the stagnation temperature and wets poorly, which limits brine creep across the rib. Printed polycarbonate ribs would cost about the same.

## 4. Design day

Table 2. Daily energy and water balance per m2 of aperture.

| Quantity | Value |
| --- | --- |
| Solar input | 19.8 MJ |
| Optical loss | 4.8 MJ |
| Absorbed | 15.1 MJ |
| Top loss | 4.5 MJ |
| Edge loss | 0.15 MJ |
| Heat into stage 1, 2, 3, 4 wicks | 10.5, 9.1, 8.1, 7.3 MJ |
| Feed heating lost with brine, stages 1 to 4 | 1.29, 0.99, 0.75, 0.57 MJ (3.6 MJ total) |
| Heat rejected at the bottom | 6.8 MJ (peak 286 W/m2) |
| Distillate, stages 1 to 4 | 3.33, 2.86, 2.50, 2.20 L |
| Distillate, quasi-steady | 10.9 L |
| Gained output ratio, quasi-steady | 1.29 |
| Warm-up energy (25.7 kJ/K per m2 of stack to the mean noon temperature) | 0.88 MJ |
| Distillate after warm-up deduction | 10.3 L |
| Gained output ratio after warm-up deduction | 1.22 |

At noon the plates run at 73.3, 68.9, 64.4, 59.8 and 54.9 °C, the bottom plate 24.9 K above ambient, and the top loss is 172 W/m2. The warm-up deduction is conservative, since part of the stored heat still produces distillate as the stack cools in the evening.

Table 3. Sensitivity of daily output (quasi-steady).

| Case | Distillate (L/m2/day) | Gained output ratio | Peak absorber (°C) | Peak bottom (°C) |
| --- | --- | --- | --- | --- |
| 3 stages | 8.8 | 1.05 | 72 | 58 |
| 4 stages (base, painted underside) | 10.9 | 1.29 | 73 | 55 |
| 6 stages | 14.1 | 1.68 | 75 | 50 |
| No rib breaks in the wicks | 11.3 | 1.35 | 72 | 55 |
| Feed ratio 3.5 | 10.1 | 1.21 | 71 | 52 |
| Wind 3 m/s | 10.9 | 1.30 | 71 | 51 |
| Bare underside (emissivity 0.10, before D-07) | 9.9 | 1.17 | 80 | 68 |
| Sunny day, 6.5 kWh/m2 | 13.2 | 1.32 | 77 | 58 |
| Hazy day, 4.5 kWh/m2 | 8.6 | 1.25 | 69 | 51 |
| Glazing transmittance 0.75 (solar-weighted, soiled) | 10.1 | 1.20 | 72 | 54 |

With the painted underside, air fins are adequate for four stages. A gained output ratio of 1.3 after warm-up would need more stages or less sensible loss, which changes the design's scope (six stages give 1.68 quasi-steady but need a cooler bottom). Amish decided on 2026-10-25 to restate PR-002 as 1.2 or more for four stages (SSK-DEC-001 D-10), so it is met on paper at 1.22 after warm-up, with no margin left at a glazing transmittance of 0.75 (1.20).

## 5. Hot operation and dry stagnation

At 1,000 W/m2 and 35 °C ambient, wet operation peaks at 79.7 °C at the absorber and 62.6 °C at the bottom plate. With dry wicks the plates reach **138, 121, 103, 83 and 61 °C** (absorber first). In calm air they reach **142, 125, 107, 87 and 64 °C**. The inner glazing sheet reaches about 108 °C (113 °C in calm air) and the outer sheet 60 °C. Harsher cases: at 40 °C ambient in calm air the plates reach 146, 129, 111, 91 and 69 °C and the inner glazing 118 °C; at 1,100 W/m2 and 35 °C in calm air they reach 151, 133, 113, 91 and 67 °C and the inner glazing 121 °C.

> **Safety:** A dry panel in full sun holds the absorber near 140 °C. Fit the stagnation cover before opening the stack, and treat an empty feed container as a burn and material-damage hazard.

Consequences for PR-008 (R8, as restated in SSK-DDR-002). Stages 1 and 2 (absorber to plate 2) peak at 142 °C against the 150 °C rating, a margin of 8 K, which closes at 1,100 W/m2; their rails are PPS (long-term service 218 °C), the ribs silicone and the liner stone wool, and the wick and the coating on plates 1 and 2 must tolerate 150 °C. Stage 3 peaks at 107 °C in calm air against the 110 °C rating, a margin of 3 K; printed polycarbonate softens at 113 °C (ISO 75 at 0.45 MPa), a short-term figure, so the stage 3 rails are PPS like stages 1 and 2 (SSK-DEC-001 D-01). Stage 4 peaks at 87 °C, 26 K under the polycarbonate softening point, so its printed rails stay. ASA (softening near 95 to 100 °C) stays excluded from stages 1 to 3. The inner glazing sheet at 113 °C in calm air is 7 K under the 120 °C service limit of twin-wall polycarbonate and reaches it at 1,100 W/m2 (STEM row S13). The stagnation cover (BOM line 14) and the shade rule are the second barrier: the cover is fitted whenever the feed runs out.

## 6. Wick feed capacity

At noon stage 1 evaporates 0.56 kg/m2/h, so each metre of wick width must carry 1.41 kg/h of feed at a ratio of 2.5. With gravity along the 20 deg slope (3,360 Pa/m) and an assumed 4 kPa of capillary pressure over the 1 m run, Darcy flow through a 1 mm wick needs a permeability of at least **2.9 x 10^-11 m2** (the fabric test keeps the rounder 3.0 x 10^-11 m2). Capacity is 0.48, 1.44 and 4.81 kg/h per metre at 1 x 10^-11, 3 x 10^-11 and 1 x 10^-10 m2. The permeability of the candidate fabrics is not known, so feed supply is a risk to PR-001 and PR-006.

## 7. Salt balance and carryover

At a feed ratio of 2.5 the brine leaves at 58.3 g/L for 35 g/L seawater and 66.7 g/L for 40 g/L feed, a factor of 4.8 below sodium chloride saturation (about 317 g/L). Salt does not travel with the vapor, so distillate salinity depends only on liquid carryover. To stay below 50 mg/L the brine reaching the distillate must be under 0.075 % of the distillate, about **8.2 mL per day** on the design day. This is an allowance, not a computed carryover (STEM rows S20 and S29). On the design day the panel takes about 27.2 L of feed and discharges 16.3 L of brine.

## 8. Mass, footprint and tilt

Table 4. Panel mass (constructable design, SSK-DDR-003).

| Item | Mass (kg) |
| --- | --- |
| Plates, five 0.5 mm aluminum, with tongues | 6.94 |
| Glazing, twin-wall polycarbonate, 1.06 m square | 1.46 |
| Walls, 12 mm plywood, less openings | 1.35 |
| Liner, 25 mm stone wool | 0.69 |
| Base ring, 12 mm plywood | 1.40 |
| Glazing trim, aluminum angle | 1.00 |
| Wicks, dry, with tails | 1.12 |
| Side rails, PPS (stages 1 to 3) and printed polycarbonate (stage 4) | 0.88 |
| Stop blocks, PPS | 0.04 |
| Wick clips, 40 of 0.4 x 8 mm stainless strip | 0.14 |
| Ribs, silicone cord | 0.71 |
| Fins | 0.63 |
| Trough, manifold, gutter, brackets, closure and fittings | 1.80 |
| Sealant, tape, fasteners and tubing | 0.60 |
| **Panel, dry** | **18.8** |
| Panel, wet wicks | 22.8 |
| Adjustable stand | 8.9 |

The model's own volume-based estimate for the modeled parts (16.2 kg without the trough, manifold, gutter and fasteners) agrees within the allowances above.

The stand (SSK-DDR-003) pivots the panel on two M10 bolts through front posts 372 mm above the ground and holds it with two fixed props, 1,000 mm between pins, hinged on blocks near the high end and pinned to the ground rails. One hole per tilt sets the angle; measured back from the pivot the holes are at 113, 151, 195, 245, 309 and 396 mm for 10, 15, 20, 25, 30 and 35 deg. The plan footprint is 1.28 x 1.25 m at 10 deg, 1.21 x 1.25 m at 20 deg and 1.05 x 1.25 m at 35 deg. The ground rails run 760 mm behind the pivot, so the wet panel's centre of mass (about 500 mm behind the pivot at 10 deg) stays at least 260 mm inside the ground frame. The model builds and checks the stand at all six holes; the feed trough rim is at most 1.00 m above the ground.

## 9. Wind

At 20 m/s the normal force on the 1.15 m2 panel (force coefficient 1.2) is about 332 N, against 311 N for the wet panel and stand. Lift equals weight at about 18.7 m/s, but tipping governs: with wind from behind on the underside, the normal force at the panel centre (overturning arm 0.70 m) tips the unanchored panel and stand about the front end of the ground frame (restoring arm 0.51 m) at about **16.5 m/s**. Unanchored, PR-013 as first written (no tipping below 17 m/s unanchored) was not met. Amish decided on 2026-10-25 (SSK-DEC-001 D-09) that the four ground stakes or 40 kg of ballast are a hold point before the panel is filled or faces the sun, and PR-013 is stated for the anchored stand. With 40 kg of ballast on the rear of the ground rails (arm 0.83 m from the front tipping edge, `sizing.py` section 12) the stand tips at about **28.8 m/s**; staked, each of the two rear stakes needs about 6 N of hold-down at 17 m/s. PR-013 is met on paper anchored. Stake pull-out in soft or sandy ground is not calculated and is checked at TRL 5.

> **Safety:** The panel and stand can overturn in a strong breeze. Anchor the stand to the ground or ballast it before filling.

## 10. Cost

Value-engineering target: USD 355 (a hypothetical control target, `budget_usd` in `project.yaml`). Estimated cost of the constructable design: USD 460.70 from `bom/bom.csv` (20 lines), USD 105.70 over the target. Before SSK-DDR-003 the concept priced at USD 351.20. The USD 65 added for construction is USD 20 for larger plate blanks for the tongues (lines 3 and 5), USD 2 for longer wicks (line 4), USD 20 for the glazing trim and tape (line 15), USD 7 for the stand's ground frame, gussets and pins (line 12), USD 4 for the trough brackets (line 8), USD 6 for the outlet brackets (line 16) and USD 6 for the feed closure (line 17). The decisions of 2026-10-02 add USD 27 more: USD 10 for PPS rails at a distributor list price (line 6, not a quote), USD 14 for 40 stainless wick clips (line 18, now 5052 aluminium at the same estimate, D-08) and USD 3 for the DISTILLATE and BRINE labels (line 19). The lip is a bend and adds nothing (section 13). The stage 3 PPS rails of 2026-10-24 add USD 16 (two PPS rails at USD 11.50 in place of two printed rails at USD 3.50, line 6; SSK-DEC-001 D-01). Amish's decisions of 2026-10-25 add USD 1.50 for the panel label with the stagnation cover rule (line 19, D-05); the 5052 aluminium clips (D-08) keep the stainless price as an estimate until the strip is priced.

## 11. Results against requirements

Table 5. Requirement status at TRL 3, not met first (PR numbers of SSK-PRS-001, old R numbers in brackets).

| ID | Quantity | Value | Target | Status |
| --- | --- | --- | --- | --- |
| PR-008 (R8) | Temperatures at dry stagnation | Stages 1 and 2: 142 °C calm (8 K margin, 0 K at 1,100 W/m2); stage 3: 107 °C calm (3 K), PPS rails since D-01; stage 4: 87 °C; inner glazing 113 °C against 120 °C; cover specified | 150 °C in stages 1 and 2, 110 °C elsewhere, cover and shade rule | At risk |
| PR-004 (R4) | Air break between wick edges and distillate paths | 10 mm at ribs and rails and inside the plate edges; brine tongues pass 10.5 mm or more over the closed manifold lid and at least 44 mm from any distillate tongue; high-edge lip modelled | 10 mm or more, no shared drain | At risk |
| PR-006 (R6) | Brine salinity; wick feed | 66.7 g/L at 40 g/L feed; needs permeability of 2.9 x 10^-11 m2 or more | Feed ratio 2.5 or more, salt stays in solution | At risk |
| PR-007 (R7) | Food-contact wetted surfaces | Coated aluminum decided; coating product not selected (rule of 2026-10-02) | All distillate-side surfaces food-contact rated | At risk |
| PR-001 (R1) | Daily distillate | 10.3 L/m2 (10.9 quasi-steady); 10.1 quasi-steady at a glazing transmittance of 0.75 | 10 L/m2 or more (goal 13) | At risk (3 % margin; goal not met) |
| PR-010 (R10) | Wick removal time; flushing interval | Plates lift out after the low wall cap is removed; wicks held by end clips with no adhesive | 30 min or less; weekly or less often | Met on paper (timing at TRL 4) |
| PR-003 (R3) | Distillate conductivity | Carryover allowance 0.075 % (8.2 mL/day) | 75 µS/cm or less | Not verifiable at TRL 3 |
| PR-012 (R12) | Parts cost | USD 460.70 | Value-engineering target USD 355 | USD 105.70 over the target |
| PR-005 (R5) | Power; feed head | Passive; feed trough rim 1.00 m at 35 deg | No power; container at most 1.5 m | Met |
| PR-009 (R9) | Mass; footprint | 18.8 kg dry; 1.28 x 1.25 m | 20 kg or less; within 1.3 x 1.3 m | Met |
| PR-002 (R2) | Gained output ratio | 1.29 quasi-steady; 1.22 after warm-up deduction; 1.20 at a glazing transmittance of 0.75 | 1.2 or more (restated from 1.3 by Amish, 2026-10-25, D-10) | Met on paper (1.7 % margin) |
| PR-013 | Tipping wind speed, anchored | 28.8 m/s with 40 kg of ballast; about 6 N hold-down on each rear stake at 17 m/s; 16.5 m/s unanchored (lift at 18.7 m/s) | 17 m/s or more, anchored (restated by Amish, 2026-10-25, D-09) | Met on paper anchored; anchoring a hold point; stake pull-out at TRL 5 |
| PR-011 (R11) | Tilt range | Six prop holes, 10 to 35 deg in 5 deg steps; model built and checked at each | 10 to 35 deg | Met |

## 12. Changes to earlier figures

Version 0.9 of this note records Amish's decisions of 2026-10-25 ("i concur with your recommendations"): PR-002 restated as 1.2 or more for four stages (D-10), not met to met on paper; PR-013 stated for the anchored stand (D-09), with the ballasted tipping speed (28.8 m/s) and the stake hold-down (about 6 N each) added to `sizing.py` section 12, not met to met on paper; wick clips in 5052 aluminium (D-08) at the stainless price as an estimate; a panel label with the cover rule (D-05) takes the parts cost from USD 459.20 to USD 460.70. No dimension, mass or energy figure changed.

SSK-PRC-001 v0.2 gave 13.2 L per day, a gained output ratio of about 1.5, stage 1 at 70 to 80 °C, dry stagnation at 100 to 120 °C, feed of 35 L and brine of 22 L, a panel of about 15 kg and parts of about $241. The precis v0.3 now quotes the values in this note.

Version 0.2 of this note (SSK-DDR-002) adds the calm-air plate temperatures and the restated R8 check, and changes the panel mass from 15.9 to 16.7 kg dry (19.9 to 20.7 kg wet), the wet panel and stand weight from 264 to 272 N, and the parts cost from $317.20 to $351.20 against a budget raised from $250 to $320. The energy balance, yield and gained output ratio are unchanged.

Version 0.3 of this note records the budget top-up to $355 approved by Amish on 2026-09-26; the parts cost is unchanged at $351.20 and R12 moves from not met to met.

Version 0.4 of this note follows SSK-DDR-003 (design for construction, made under Amish's 2026-09-30 instruction to make the design physically buildable; accepted by Amish on 2026-10-02 with the exceptions recorded there). The wet wick fraction falls from 0.824 to 0.817, which moves the stage outputs by at most 0.01 L; the daily yield (10.6 L), gained output ratio and stagnation temperatures are unchanged at the precision quoted. The panel rises from 16.7 to 18.5 kg dry (20.7 to 22.5 kg wet), the stand from 7.1 to 8.9 kg, the footprint from 1.28 x 1.16 m to 1.28 x 1.25 m, the wind speed at which lift equals weight from 17.5 to 18.7 m/s, and the cost from USD 351.20 to USD 416.20, now reported against the USD 355 value-engineering target. Feed and brine figures were also brought in line with the script (28.2 and 16.9 L per day).

Version 0.7 of this note (kit 1.9.1 upgrade, 2026-10-24) moves the stage 3 rails to PPS (SSK-DEC-001 D-01): the rails go from 0.86 to 0.88 kg, the panel from 18.7 to 18.8 kg dry (22.7 to 22.8 kg wet) and the cost from USD 443.20 to USD 460.70. The detailed model (kit 1.9) showed that the pivot bolts need to be M10 x 75 (not 70) to show two thread pitches past the nut, and that the 10 and 15 deg prop holes lie under the gussets, so the foot pins go through the gusset there and are M10 x 120 (not 100); both are bolt lengths only (SSK-DEC-001 D-02) and change no figure here.

Version 0.8 of this note follows the independent review recorded in SSK-STM-001: the underside convection is corrected (laminar flat plate in place of a 5 W/m2K floor), the brine's water activity enters the gap transfer, and the underside and fins are painted black (SSK-DEC-001 D-07). The yield moves from 10.6 to 10.3 L after warm-up (11.3 to 10.9 L quasi-steady), the gained output ratio from 1.26 to 1.34 to 1.22 to 1.29, dry stagnation from 140 and 144 °C to 138 and 142 °C, the peak bottom rejection from 277 to 286 W/m2, feed and brine from 28.2 and 16.9 to 27.2 and 16.3 L per day, and the carryover allowance from 8.5 to 8.2 mL per day. A tipping check (section 9) and harsher stagnation and transmittance cases (sections 4 and 5) are added.

## 13. Design for construction checks

Table 6. Checks added for the constructable design (section 14 of the script).

| Check | Result |
| --- | --- |
| Bottom plate sag on the base ring, fins bonded (composite) | 0.5 mm |
| Bottom plate sag, fins carrying the load alone | 1.0 mm |
| Glazing growth, 1.06 m sheet at a 70 K rise | 4.8 mm, against 14 mm of room inside the trim |
| Load per pivot bolt, wet panel plus 17 m/s wind | 164 N; bearing on 12 mm plywood 1.4 MPa (embedment strength about 50 MPa, STEM row S14) |
| Prop buckling, 45 x 45 mm timber, 1.0 m pinned | 27 kN, far above the load |
| Outlet bracket load, manifold and gutter full | 29 N each; 62 N pull on the top screw |
| Vapor lost through the low-end tongue openings (diffusion, 4 gaps) | 25 mL per day (0.2 % of the yield) |
| Lowest brine tongue tail above the distillate lid | 10.5 mm |
| Lip tabs, 4 mm on the high edge of each condensing plate | 5.0 mm of sheet each, 140 mm2 per plate, 0.76 g for the four plates; the plate blank is 1,224 mm long against a 1,250 mm sheet, so sheet size and cost are unchanged (a bend, no yield loss) |
| Wick clips, 304 stainless 0.4 x 8 mm | 40 clips from 5.5 m of strip, 0.14 kg |

The parametric model also runs its own constructability checks (`python cad/src/model.py --check`): no overlaps among the 54 panel parts, every part that must touch does touch, the lip tabs and wick clips keep their clearances (the tabs 1.5 mm or more from every wick and 5 mm or more from every rib end; the clips 1.5 mm or more from the liner and ribs and 10 mm or more from the lid), every brine path keeps 10 mm or more from every distillate path, and the stand at each of the six tilt holes has no clashes, keeps the centre of mass inside the ground frame and stays within the 1.3 x 1.3 m footprint.
