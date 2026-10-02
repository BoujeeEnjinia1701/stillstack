---
doc_id: SSK-PRB-001
title: StillStack problem statement
project: StillStack
doc_type: Problem statement
version: "0.6"
status: Draft
date: '2026-10-02'
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
  change: Populate to TRL 2 (users, context, constraints, out of scope, prior work)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the 1 m2 aperture decision (SSK-DDR-001) and the TRL 3 cost finding; partner question stays open
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget top-up approved by Amish
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Partner decided and first candidate to approach (SSK-DEC-001, 2026-10-02)"
---

# StillStack problem statement

Solar stills are the simplest way to turn salty or brackish water into drinking water without fuel or grid power, but a single-basin still makes only about 3 to 5 L per m2 per day, so a household needs 3 to 5 m2 of glazed basin to cover drinking and cooking water. That area is too large, too costly and too hard to maintain for most of the people who need it.

## The problem

A single-basin still throws away almost all of the energy it collects. Sunlight evaporates water from a shallow basin, the vapor condenses on the glass cover, and the latent heat released there (about 2.26 MJ per kg of water) is lost to the sky. The result is a daily efficiency of roughly 30 to 45 % of the solar input, which caps output at about 3 to 5 L per m2 per day under good sun. The deep water basin also takes hours to warm up each morning.

Multi-effect distillation fixes this in industry by condensing the vapor from one effect against the evaporator of the next, so the same heat evaporates water several times. Research groups have shown that the same idea works passively at small scale: thin wicks pressed against stacked metal plates, heated by sunlight from above, each stage reusing the heat of condensation from the stage above it. Laboratory prototypes of this kind (for example the passive multistage devices reported by Chiavazzo and colleagues in Nature Sustainability in 2018 and the thermally localized multistage still reported by Xu and colleagues in Energy and Environmental Science in 2020) produced two to four times the output of a basin still per unit area under simulated or real sun. There is still no open, documented, garage-buildable design that a community workshop, NGO or school can build, audit and adapt.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Household in an arid or saline coastal area | 5 to 15 L per day of safe drinking and cooking water from seawater or brackish well water | Rooftop or yard, no reliable grid, strong sun (5 to 7 kWh per m2 per day) |
| Rural clinic or school | A steady supply of low-salt water for drinking, and for rinsing and battery top-up | Small compound, a caretaker with basic tools, part-time maintenance |
| Small island or remote outpost | Backup water when a reverse osmosis unit or its power fails | Seawater feed, salt spray, high UV |
| NGO, makerspace or technical college | A reproducible, inspectable design to build, test and improve | Workshop with hand tools, a 3D printer and sheet metal tools |

## Constraints

- Garage-buildable prototype of 1 m2 aperture for about $355 USD in parts, using sheet aluminum, polycarbonate glazing, timber and cloth wicks. The 1 m2 aperture was confirmed by Amish on 2026-09-25 (SSK-DDR-001), the budget was raised from $250 to $320 the same day (SSK-DDR-002), and Amish approved a top-up to $355 on 2026-09-26. The priced BOM, including the 150 °C materials and stagnation cover decided in SSK-DDR-002, comes to about $351, so the cost constraint is met (SSK-CAL-001).
- Fully passive: no pumps, electronics or batteries. Feed water arrives by gravity from a container the user fills.
- Every surface that touches distillate must be food-contact safe, and all materials must tolerate dry stagnation under full sun.
- Feed water may be seawater (about 35 g per L of salt) or brackish groundwater, so wicks and plates must resist salt build-up and corrosion.
- Maintenance by a non-specialist with no special tools: rinsing or replacing wicks, clearing salt.
- Distillate is a raw product. It is not assumed to be safe to drink until tested, and the documentation must say so.

## Out of scope

- Certified drinking water treatment or any claim of potability.
- Brine disposal or salt recovery beyond a drain outlet.
- Large community plants (more than about 10 m2) and powered or hybrid (photovoltaic plus heater) versions.
- Water quality testing equipment and remineralization systems, which are named as needs but not designed here.

## Open questions

- Which users to involve first, and through which partner? Decided by Amish, 2026-10-02 (SSK-DEC-001): a university water or desalination lab first, to measure distillate quality; first candidate to approach, the Politecnico di Torino group behind the 2018 floating multistage still. A coastal NGO follows for field use once the distillate passes its tests. Nothing is agreed yet.
- The first size is settled: a household unit of 1 m2, decided by Amish on 2026-09-25 (SSK-DDR-001).
