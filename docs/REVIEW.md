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

### Proposed, awaiting Amish

1. Four stages with 6 mm gaps. Alternatives: three stages (simpler, about 10.5 L) or six stages (only with a water-cooled bottom).
2. Air-cooled fins under the bottom plate. Alternatives: a feed-water tray heat sink, or floating the unit on water.
3. Condenser plates in aluminum with a food-grade coating (recommended on cost). Alternatives: 316 stainless steel (over budget by about $100 to $150) or anodized aluminum.
4. Spacers in ASA or polycarbonate instead of PETG.
5. Tilt of 20 deg, with an adjustable stand to meet R11.
6. Prototype aperture of 1 m2 (alternative: 0.5 m2 to add budget margin).
7. Keep the budget at $250. No budget change is proposed now, but the stainless option would need one.
8. First co-design partner: a coastal NGO, a university water lab or a makerspace network.

### Safety concerns

- Distillate is not certified drinking water. The documents require testing (conductivity, E. coli), clean covered storage and disinfection, and they note brine carryover, volatile carryover and the need for remineralization.
- All wetted surfaces on the distillate side must be food-contact rated. Bare aluminum and unknown plastics are excluded.
- Hot surfaces: about 70 to 80 °C in use and above 100 °C when dry. Shade the panel before maintenance.
- A 1 m2 tilted panel can tip over in wind, so the stand must be anchored. Brine must be discharged away from crops and wells.

### Recommended next step

Review this note and the media. If approved, run `/advance-trl3` to write the stage energy balance calculation (gap heat transfer, evaporation fraction, heat rejection and stagnation temperature), select the condenser coating and wick, and produce the parametric model and drawing sheet.
