---
doc_id: SSK-DDR-004
title: StillStack concept selection
project: StillStack
doc_type: Design decision record
version: '0.2'
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-24'
  author: Amish Chadha
  change: "Concept selection between option A (four-stage wick still) and option B (single-effect tilted wick still); within 10 %, both to Amish; proposed, awaiting Amish"
- version: '0.2'
  date: '2026-10-25'
  author: Amish Chadha
  change: 'Option A cost USD 460.70 (panel label, D-05); the selection itself is still proposed, awaiting Amish (no pick)'
---

# StillStack concept selection

**Status: Proposed, awaiting Amish (SSK-DEC-001 D-03).** No option is picked, because the two score within 10 % (STANDARDS section 21).

## Context

StillStack was designed before kit 1.8, so its current design is option A, the four-stage wick still, and the repo is not redesigned without Amish's go. The kit 1.9.1 upgrade (2026-10-24) adds option B, a single-effect tilted wick still, with a different working principle: one evaporation and one condensation, the latent heat lost through the cover, rather than four stages that reuse it. Both are modelled to detail level D3 in `cad/src/model.py` and checked in SSK-STM-001. The comparison and scores are in SSK-OPT-001.

## Options

1. **Option A, four-stage wick still (current design).** About 10.3 L/m2/day on the design day, USD 460.70 per 1 m2 panel, 18.8 kg dry. Complex: five shaped plates, twenty wick strips, forty clips, a certified food-contact coating; PR-002 not met and several material confirmations open.
2. **Option B, single-effect tilted wick still.** About 3.8 L/m2/day (an assumed 45 % efficiency, near the 4.5 to 5.0 L reported for tilted wick stills), so about 2.6 panels for a household's 10 L. Simpler, glass condensing surface with no coating to certify, one wick, easy to clean; heavier per panel and costlier per litre.
3. **Option A with option B's best idea.** B's glass cover is the one feature worth grafting: a glass outer sheet in place of twin-wall polycarbonate would remove the 120 °C glazing limit (STEM S13) at a mass cost of about 9 kg. It is not proposed now, because it would push the panel over the 20 kg of PR-009.

## Scores

Option A scores 152 and option B 153 of 220 (SSK-OPT-001, Table 2): a difference of under 1 %. A wins on the core needs, water per panel and per square metre (UR-001, UR-002); B wins on simplicity, safe materials, cleaning and buildability (UR-003, UR-004, UR-006, UR-007, UR-010, buildability, maintenance).

## Recommendation

None, by rule. For Amish's choice: if the measure is water per household for the money and the effort of building, A is ahead (about USD 461 and one panel for 10 L a day, against about 2.6 panels and roughly USD 590 for B); if the measure is the lowest risk to drinking-water safety and the easiest care by a part-time caretaker, B is ahead. The repo stays on option A until Amish decides.

## Consequences

- If A: no change; the open items of SSK-DEC-001 (D-04 to D-10) continue.
- If B: a new constructable design, drawings, BOM and build plan for option B at TRL 3, in a later session.
