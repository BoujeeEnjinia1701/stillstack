# Review note: StillStack

## Session 2026-09-24: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (SSK-PRB-001 v0.2): the problem, users and context (arid and saline coastal households, clinics and schools, remote outposts, makerspaces), constraints, out of scope, prior research described without links.
- `docs/03-requirements.md` (SSK-REQ-001 v0.2): 12 measurable requirements (R1 to R12) with targets, planned verification and stated assumptions.
- `docs/02-concept.md` (SSK-PRC-001 v0.2): how it works, main components numbered to match the exploded view and BOM, first-order energy balance, design choices, safety, open questions.
- `cad/src/concept_media.py`: massing model of a 1 m2 tilted panel (glazing, insulated frame, absorber, four wicks, four condenser plates, spacers, feed trough, distillate manifold, brine gutter, fins, tilt stand) with the 1.75 m figure for scale.
- `media/`: hero, blueprint sheet SSK-DWG-001 (PNG and PDF), cutaway, exploded view with BOM callouts, energy and water flow diagram marked as estimates, `model.glb` and `viewer.html`.
- `bom/bom.csv`: 12 lines with indicative prices, numbered to match the exploded view; `bom/bom-notes.md`.
- `README.md`: hero image and links line.
- `docs/pdf/`: branded PDFs of the three controlled documents.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Solar input | 19.8 MJ per m2 per day (5.5 kWh) | |
| Single-stage yield | about 3.8 L per m2 per day | Matches basin stills |
| Four-stage yield | about 13.2 L per m2 per day (range 10.5 to 17.5) | R1 met on paper |
| Gained output ratio | about 1.5 | R2 met on paper |
| Stage 1 temperature | about 70 to 80 °C at noon | |
| Heat to reject at the bottom | about 8.1 MJ per day, peak about 280 W/m2 | |
| Panel mass | about 15 kg dry | R9 met |
| Parts cost | about $241 | R12 met, about $9 margin |

Requirements not met or at risk:

- **R7 (food-safe wetted parts):** not met by bare aluminum condenser plates. It depends on a coating or stainless choice that is still open.
- **R8 (dry stagnation):** not met by the PETG "printed spacers" in the original scaffold. The precis and BOM now specify ASA or polycarbonate, pending approval.
- **R11 (adjustable tilt):** not met by the massing model, which has a fixed 20 deg stand.
- **R12 (cost):** met with almost no margin. The stainless plate option would exceed the $250 budget.
- **R1 and R2:** depend on an assumed evaporation fraction of 0.70 per stage and on air fins rejecting about 280 W/m2. Both are unverified and are the main technical risks.

### Proposed, awaiting Amish (items 1 to 7 since decided, see SSK-DDR-001)

1. Four stages with 6 mm gaps. Alternatives: three stages (simpler, about 10.5 L) or six stages (only with a water-cooled bottom). Decided by Amish, 2026-09-25: go with recommendation.
2. Air-cooled fins under the bottom plate. Alternatives: a feed-water tray heat sink, or floating the unit on water. Decided by Amish, 2026-09-25: go with recommendation.
3. Condenser plates in aluminum with a food-grade coating (recommended on cost). Alternatives: 316 stainless steel (over budget by about $100 to $150) or anodized aluminum. Decided by Amish, 2026-09-25: go with recommendation.
4. Spacers in ASA or polycarbonate instead of PETG. Decided by Amish, 2026-09-25: go with recommendation.
5. Tilt of 20 deg, with an adjustable stand to meet R11. Decided by Amish, 2026-09-25: go with recommendation.
6. Prototype aperture of 1 m2 (alternative: 0.5 m2 to add budget margin). Decided by Amish, 2026-09-25: go with recommendation.
7. Keep the budget at $250. No budget change is proposed now, but the stainless option would need one. Decided by Amish, 2026-09-25: go with recommendation.
8. First co-design partner: a coastal NGO, a university water lab or a makerspace network. No recommendation; still proposed, awaiting Amish.

### Safety concerns

- Distillate is not certified drinking water. The documents require testing (conductivity, E. coli), clean covered storage and disinfection, and they note brine carryover, volatile carryover and the need for remineralization.
- All wetted surfaces on the distillate side must be food-contact rated. Bare aluminum and unknown plastics are excluded.
- Hot surfaces: about 70 to 80 °C in use and above 100 °C when dry. Shade the panel before maintenance.
- A 1 m2 tilted panel can tip over in wind, so the stand must be anchored. Brine must be discharged away from crops and wells.

### Recommended next step

Review this note and the media. If approved, run `/advance-trl3` to write the stage energy balance calculation (gap heat transfer, evaporation fraction, heat rejection and stagnation temperature), select the condenser coating and wick, and produce the parametric model and drawing sheet.

## Session 2026-09-25: TRL 3

### What was done

Amish accepted every TRL 2 recommendation on 2026-09-25 and instructed that no repo proceeds to TRL 4. This session advanced StillStack to TRL 3 (trl: 3, trl_target: 3).

- `docs/decisions/0001-trl2-review-decisions.md` (SSK-DDR-001 v0.1): seven decisions recorded; the co-design partner stays open.
- `docs/04-calcs/01-sizing.md` (SSK-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: quasi-steady stage energy balance over a design day (Stefan diffusion, conduction and radiation across each gap; top-loss network; fin and radiation heat rejection; feed sensible heat; warm-up deduction), plate sag and rib pitch, dry stagnation, wick feed capacity, salt balance and carryover allowance, mass, tilt and footprint, wind overturning and BOM cost. The script prints every number the note quotes.
- `cad/src/model.py`: parametric build123d model (tilt, aperture, stage count, gap, rib count, wall build-up and stand as parameters) exporting `cad/step/stillstack-assembly.step`, `cad/stl/stillstack-assembly.stl` and `cad/stl/side-rail.stl`; it prints part masses and checks the tilt range at 10, 20 and 35 deg.
- `cad/src/sheets.py` and `cad/drawings/SSK-DWG-002.svg`, `.pdf`, `.png`: general arrangement at Rev P1, "PRELIMINARY, NOT FOR FABRICATION", with three views at 1:20, isometric view, stack detail at 2:1 and low-edge detail at 1:2. The concept blueprint remains SSK-DWG-001 (now Rev P2).
- `bom/bom.csv` (13 lines, every line priced with a supplier type) and `bom/bom-notes.md`.
- `cad/src/concept_media.py` now builds from the parametric model; all media in `media/` refreshed and inspected (hero, blueprint, cutaway, exploded view with BOM callouts 1 to 12, flow diagram with calculated values, `model.glb`, `viewer.html`). The scale figure was moved clear of the panel so it no longer overlaps the isometric view.
- `docs/01-problem.md`, `docs/02-concept.md` and `docs/03-requirements.md` at v0.3; `project.yaml` and `README.md` updated; PDFs rebuilt in `docs/pdf/`.

### Requirements at TRL 3 (not met first)

| ID | Status | Key figure |
| --- | --- | --- |
| R8 | **Not met** | Dry stagnation about 140 °C at stage 1 (144 °C in calm air), above the 110 °C rating |
| R12 | **Not met** | Parts $317.20 against $250 ($67.20 over) |
| R2 | At risk | Gained output ratio 1.34 quasi-steady, 1.26 after warm-up deduction (target 1.3) |
| R4 | At risk | 10 mm breaks modeled at ribs and rails; brine exit over the lidded manifold not detailed |
| R6 | At risk | Brine 66.7 g/L is fine; wick needs a permeability of 3.0 x 10^-11 m2 or more, unknown |
| R7 | At risk | Coating product for wet, salty service at 80 °C not selected |
| R10 | At risk | Bonded wicks; removal method not defined |
| R3 | Not verifiable at TRL 3 | Brine carryover must stay below 0.075 % (8.6 mL per day) |
| R1 | Met | 10.6 L per m2 per day (11.3 quasi-steady); the 13 L goal is not met |
| R5 | Met | Passive; feed trough top at most 1.06 m |
| R9 | Met | 15.9 kg dry, 19.9 kg wet; footprint 1.28 x 1.16 m |
| R11 | Met | Stand and model at 10 to 35 deg |

Numbers the TRL 2 documents overstated and that are now corrected: 13.2 L per day (now 10.6 to 11.3 L), gained output ratio 1.5 (now 1.26 to 1.34), glazing transmittance 0.88 (now 0.80 for twin-wall polycarbonate), stagnation 100 to 120 °C (now about 140 °C), feed 35 L and brine 22 L (now 28.7 and 17.2 L), cost $241 (now $317.20). The TRL 2 assumption of an evaporation fraction of 0.70 was conservative; the calculation gives 0.85 to 0.91 at noon. The main new losses are the sensible heat of the feed (3.8 MJ per day) and the lower glazing transmittance.

A structural finding changed the model: 0.5 mm plates held only by side rails would sag about 325 mm, so four intermediate ribs per gap at 194 mm pitch were added (sag 0.52 mm), with the wicks cut into strips around them.

### Decisions recorded (SSK-DDR-001)

Decided by Amish, 2026-09-25, going with the recommendation: four stages with 6 mm gaps; air-cooled fins; aluminum condenser plates with a food-contact coating; spacers in ASA or polycarbonate, not PETG; 20 deg tilt on an adjustable stand; 1 m2 aperture; budget kept at $250 with no redefinition.

### Still awaiting Amish

1. First co-design partner (coastal NGO, university water lab or makerspace network). No recommendation made.
2. **Intermediate spacer ribs** (new): silicone cord (recommended: rated well above 140 °C and poorly wetting, so it limits brine creep) or printed polycarbonate. About $20 either way. Decided by Amish, 2026-09-25: go with recommendation. Silicone cord (SSK-DDR-002).
3. **Response to R8 not met** (new). Options: (a) specify materials rated to about 150 °C in stages 1 and 2 (silicone ribs, high-heat polycarbonate or PPS rails, higher-rated liner) and change the R8 rating to match the calculated stagnation temperature; (b) keep R8 as written and add a stagnation cover or a shade rule when the feed runs out; (c) both. Recommendation: (c), since a cover also protects the glazing. Decided by Amish, 2026-09-25: go with recommendation. Option (c) (SSK-DDR-002).
4. **Response to R12 not met** (new). Options: (a) raise budget_usd to about $320; (b) keep $250 and cut cost (for example ribs and rails from one material, a cheaper frame liner, or fewer coated faces); (c) redefine the budget to exclude the stand. Recommendation: (a), because the extra cost comes from parts the calculation shows are needed. The budget is not changed here. Decided by Amish, 2026-09-25: go with recommendation. Option (a), budget_usd $320 (SSK-DDR-002).
5. Coating product for the condensing faces (R7) and wick fabric with a permeability of at least 3.0 x 10^-11 m2 (R6). Both are selections that need datasheets; no product is recommended yet. Still proposed, awaiting Amish.

### Safety concerns

- Dry stagnation reaches about 140 °C at the absorber and about 109 °C at the inner glazing sheet. This is a burn hazard and can damage the stack if the feed runs out in sun.
- Lift on the panel equals its weight at about 17 m/s of wind; the stand must be anchored or ballasted.
- Distillate is not certified drinking water. Brine carryover of more than about 8.6 mL per day would exceed the 50 mg/L check, so test before drinking and disinfect.
- Brine (up to about 67 g/L) must be discharged away from crops and wells.

### Other notes

- No TRL 4 material (tests, build procedures, purchasing lists, build-log entries) exists in the repo, and none was created. STANDARDS section 9 asks for TRL changes to be recorded in the build log; no build-log entry was added, because build-log material is outside this session's scope. The change is recorded here and in `project.yaml`.
- No citations were flagged as unchecked in the TRL 2 review, so no web verification was attempted. The two research papers named in SSK-PRB-001 remain described without links.
- Material limits quoted for ASA, polycarbonate, PIR and twin-wall sheet are typical values, not datasheet checks.

### Recommended next step

TRL 4 is on hold by Amish's instruction. The recommended next step is for Amish to decide items 2 to 4 above, after which SSK-CAL-001 and the BOM can be rerun on paper. For reference only, TRL 4 would need: a lab test article of one or two stages, a test report (TST, environment: lab) measuring gap heat transfer, evaporation fraction, wick feed rate and distillate conductivity, and build-log entries. None of that should start until Amish lifts the TRL 3 cap.

## Session 2026-09-25: recommendations accepted

### Decisions applied

Amish wrote on 2026-09-25: "i accept all your recommendations, go with them across all repos." Three items that carried a recommendation are now decided and recorded in `docs/decisions/0002-recommendations-accepted.md` (SSK-DDR-002 v0.1):

1. **Intermediate spacer ribs:** silicone cord, as recommended. Already in the model and BOM; now a decided choice (no cost or geometry change).
2. **Response to R8 not met:** option (c), both. Materials in stages 1 and 2 rated to 150 °C (four side rails in PPS or a high-heat polycarbonate copolymer; frame liner changed from PIR to foil-faced stone wool; wick and plate 1 and 2 coating to tolerate 150 °C), R8 restated (150 °C in stages 1 and 2, 110 °C elsewhere, cover and shade rule), and a stagnation cover added as BOM line 14.
3. **Response to R12 not met:** option (a). budget_usd changed from **$250 to $320**.

### What changed (before and after)

| Quantity | Before | After |
| --- | --- | --- |
| budget_usd | $250 | $320 |
| Priced BOM | $317.20 (13 lines), $67.20 over | $351.20 (15 lines), $31.20 over |
| R8 rating | 110 °C for all internal materials | 150 °C in stages 1 and 2; 110 °C elsewhere; cover and shade rule |
| R8 status | Not met (140 °C, 144 °C calm) | At risk (144 °C vs 150 °C, 6 K; stage 3 110 °C vs 110 °C in calm air, 0 K) |
| Frame liner | 25 mm PIR foam | 25 mm foil-faced stone wool |
| Panel mass | 15.9 kg dry, 19.9 kg wet | 16.7 kg dry, 20.7 kg wet |
| Wind: lift equals weight | about 17 m/s | about 17.5 m/s |
| Daily distillate, gained output ratio | 10.6 L, 1.26 to 1.34 | Unchanged |

Files changed: `project.yaml`, `README.md`, `docs/01-problem.md` (SSK-PRB-001 v0.4), `docs/02-concept.md` (SSK-PRC-001 v0.4), `docs/03-requirements.md` (SSK-REQ-001 v0.4), `docs/04-calcs/01-sizing.md` (SSK-CAL-001 v0.2) and `sizing.py` (calm-air plate temperatures and R8 check added, budget from DDR-002), `bom/bom.csv` and `bom/bom-notes.md`, `cad/src/model.py` (material notes and liner density; geometry unchanged; STEP and STL re-exported), `cad/src/sheets.py` (SSK-DWG-002 Rev P1 to P2: material block and notes), `cad/src/concept_media.py` (blueprint SSK-DWG-001 Rev P2 to P3: key figures), all media and PDFs regenerated. The README gained the Concept rationale, Burning platform, Where it could be used and What sparked the idea sections.

### Requirement status (not met first)

| Status | Requirements |
| --- | --- |
| Not met | R12 (parts $351.20 against $320) |
| At risk | R8 (0 K margin at stage 3 in calm air; rail polymer not selected), R2 (gained output ratio 1.26 to 1.34 against 1.3), R4 (brine exit over the manifold not detailed), R6 (wick permeability unknown), R7 (coating product not selected), R10 (wick removal not defined) |
| Not verifiable at TRL 3 | R3 (carryover below 8.6 mL per day) |
| Met on paper | R1 (10.6 L), R5, R9 (16.7 kg dry), R11 |

### Still awaiting Amish

1. First co-design partner (coastal NGO, university water lab or makerspace network). No recommendation.
2. Coating product for the condensing faces (R7) and wick fabric (R6). Selections that need datasheets; no recommendation.
3. **Response to R12 not met at $320** (new). Options: (a) raise budget_usd to about $355; (b) keep $320 and cut cost (for example silicone strip rails in stages 1 and 2, a locally sourced cover); (c) exclude the cover and stand from the budget. Recommendation: (a), because the extra cost follows from the decided R8 response.

### Cross-repo actions

None. No decision in this repo requires a change to another repo.

### TRL

trl: 3 and trl_target: 3 are unchanged. TRL 4 remains on hold by Amish's instruction: no hardware, tests, purchasing or build-log entries were created. Selecting the rail polymer, coating and wick from datasheets can be done on paper; measuring stagnation temperatures or wick permeability is TRL 4 work and is on hold.
