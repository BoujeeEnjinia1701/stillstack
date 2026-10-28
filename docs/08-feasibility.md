---
doc_id: SSK-FEA-001
title: StillStack feasibility assessment
project: StillStack
doc_type: Feasibility assessment
version: '0.2'
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-24'
    author: Amish Chadha
    change: First feasibility assessment (kit 1.9.1 upgrade)
  - version: '0.2'
    date: '2026-10-25'
    author: Amish Chadha
    change: 'PR-002 restated (D-10, decided by Amish 2026-10-25); cost USD 460.70'
---

# StillStack feasibility assessment

Feasible on paper as a garage-built prototype: the working principle sits within known science (SSK-STM-001), the design is detailed to D3 and buildable with the build plan, and the open questions are material choices that a short test programme at TRL 4 closes (wick permeability, coating certificate, crevice corrosion), not the working principle. Cost is the weakest aspect: USD 460.70 against the USD 355 value-engineering target. Method: STANDARDS section 23.

Table 1. Feasibility by aspect.

| Aspect | Assessment | Rating | Risks and notes | Evidence |
| --- | --- | --- | --- | --- |
| Design (working principle) | Four-stage multi-effect diffusion still gives 10.3 L/m2/day on the design day with a gained output ratio of 1.22 to 1.29, after the independent review's corrections and the painted underside (SSK-DEC-001 D-07); independent order-of-magnitude checks agree within a factor of 1.0 to 1.15 | High | Thin margin on PR-001 (3 %, at risk); PR-002 restated as 1.2 or more by Amish (D-10, 2026-10-25), met on paper with a 1.7 % margin | SSK-STM-001 S1 to S8, S27; SSK-CAL-001 sections 2 to 5 |
| Materials | PPS rails (stages 1 to 3), silicone ribs, stone wool liner and PTFE-class coating are rated above the stagnation temperatures; stage 3 fixed by D-01 | Medium | Wick fabric rating and permeability unknown (S17, S25); coating certificate not seen (S22); crevice corrosion of bare aluminium under the wicks (S21); the stainless clips on aluminium in brine are replaced by 5052 aluminium clips (S30, D-08, decided 2026-10-25); inner glazing 7 K under its limit, kept with the cover rule on the panel label (S13, D-05) | SSK-STM-001; SSK-DEC-001 D-01, D-04, D-05 |
| Manufacturing and assembly | Plywood box, cut and folded 0.5 mm aluminium, printed rails for stage 4 only, hand tools; 22 illustrated steps; the D3 model shows every screw and bolt and found two bolt lengths to correct (D-02); the unanchored stand tips at 16.5 m/s, so anchoring is required (D-09) | High | Plate tongue bends need care; the zigzag edges are hand-cut | SSK-BLD-001; `cad/fidelity.json` |
| Power and controls | None: passive, gravity feed from a container at most 1.5 m high | High | Feed must be refilled daily; a dry day drives stagnation | PR-005; SSK-CAL-001 section 5 |
| Supply of parts | Common building, metal and plastics supplies; PPS strip and a certified coater are the two specialist items | Medium | PPS priced from a distributor list price, not a quote; coater availability by region unknown | BOM lines 5 and 6; SSK-DEC-001 to confirm items 5, 7, 8 |
| Cost | USD 460.70 per 1 m2 panel, USD 105.70 over the value-engineering target | Low | Coated plates and PPS rails dominate; savings listed in SSK-DEC-001 | SSK-CAL-001 section 10 |
