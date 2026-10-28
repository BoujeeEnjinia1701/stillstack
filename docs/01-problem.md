---
doc_id: SSK-PRB-001
title: StillStack problem statement
project: StillStack
doc_type: Problem statement
version: '0.8'
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
- version: "0.7"
  date: '2026-10-24'
  author: Amish Chadha
  change: "Kit 1.9.1 upgrade: users-and-needs and stakeholder tables added (STANDARDS section 22); constraint cost updated to USD 459.20 after SSK-DEC-001 D-01"
- version: '0.8'
  date: '2026-10-25'
  author: Amish Chadha
  change: 'Constraint cost USD 460.70 after the panel label of D-05 (decided by Amish 2026-10-25)'
---

# StillStack problem statement

Solar stills are the simplest way to turn salty or brackish water into drinking water without fuel or grid power, but a single-basin still makes only about 3 to 5 L per m2 per day, so a household needs 3 to 5 m2 of glazed basin to cover drinking and cooking water. That area is too large, too costly and too hard to maintain for most of the people who need it.

## The problem

A single-basin still throws away almost all of the energy it collects. Sunlight evaporates water from a shallow basin, the vapor condenses on the glass cover, and the latent heat released there (about 2.26 MJ per kg of water) is lost to the sky. The result is a daily efficiency of roughly 30 to 45 % of the solar input, which caps output at about 3 to 5 L per m2 per day under good sun. The deep water basin also takes hours to warm up each morning.

Multi-effect distillation fixes this in industry by condensing the vapor from one effect against the evaporator of the next, so the same heat evaporates water several times. Research groups have shown that the same idea works passively at small scale: thin wicks pressed against stacked metal plates, heated by sunlight from above, each stage reusing the heat of condensation from the stage above it. Laboratory prototypes of this kind (for example the passive multistage devices reported by Chiavazzo and colleagues in Nature Sustainability in 2018 and the thermally localized multistage still reported by Xu and colleagues in Energy and Environmental Science in 2020) produced two to four times the output of a basin still per unit area under simulated or real sun. There is still no open, documented, garage-buildable design that a community workshop, NGO or school can build, audit and adapt.

## Users and context

Table 1. Users and context.

| User | Need | Context |
| --- | --- | --- |
| Household in an arid or saline coastal area | 5 to 15 L per day of safe drinking and cooking water from seawater or brackish well water | Rooftop or yard, no reliable grid, strong sun (5 to 7 kWh per m2 per day) |
| Rural clinic or school | A steady supply of low-salt water for drinking, and for rinsing and battery top-up | Small compound, a caretaker with basic tools, part-time maintenance |
| Small island or remote outpost | Backup water when a reverse osmosis unit or its power fails | Seawater feed, salt spray, high UV |
| NGO, makerspace or technical college | A reproducible, inspectable design to build, test and improve | Workshop with hand tools, a 3D printer and sheet metal tools |

### Users and needs

Table 2. Users and needs (the source of the user requirements in SSK-URS-001).

| User type | Goals and needs | Typical use scenario | Pain points and challenges |
| --- | --- | --- | --- |
| Household in an arid or saline coastal area | 5 to 15 L of low-salt water a day for drinking and cooking, without fuel, power or a water bill | One panel in the yard or on a flat roof, filled each morning from a bucket of seawater or well water | Basin stills need 3 to 5 m2 for the same water; glass breaks; nobody nearby can repair a membrane unit |
| Rural clinic or school caretaker | A steady daily supply of low-salt water and simple upkeep that fits a part-time role | One or two panels in a compound; the caretaker fills the feed, empties the distillate jar and rinses the wicks weekly | Little time and few tools; must be sure the brine never reaches the drinking water |
| Small island or remote outpost | Backup water when a reverse osmosis unit or its power fails | Panels stored and set up when needed, fed with seawater | Salt spray and high UV; spare parts arrive rarely |
| NGO, makerspace or technical college | A reproducible, inspectable design to build, test and adapt | A workshop builds a batch from the drawings and build plan and runs it beside a basin still | Research devices are not documented for building; costs and materials must be local |

### Stakeholders

Table 3. Stakeholders.

| Stakeholder group | Role or interest | Engagement needed |
| --- | --- | --- |
| University water or desalination lab (first candidate: Politecnico di Torino group) | Measures distillate quality and output; first co-design partner (SSK-DEC-001, 2026-10-02) | Share the design and calculation note; agree a TRL 4 test programme (on hold under the TRL 3 cap) |
| Coastal NGO or WASH programme | Field use once the distillate passes its tests | Co-design of feed handling, maintenance and training; later field trial |
| Local health or water authority | Rules on drinking-water materials and household water claims | Consulted before any claim about drinking water (SSK-REG-001) |
| Builders (makerspaces, technical colleges, local workshops) | Make and repair the panels | Feedback on the build plan, parts sourcing and cost |
| Neighbours and land users near the brine outlet | Brine discharged near crops, wells or soil | Brine disposal guidance in the instructions |

## Constraints

- Garage-buildable prototype of 1 m2 aperture for about $355 USD in parts, using sheet aluminum, polycarbonate glazing, timber and cloth wicks. The 1 m2 aperture was confirmed by Amish on 2026-09-25 (SSK-DDR-001), the budget was raised from $250 to $320 the same day (SSK-DDR-002), and Amish approved a top-up to $355 on 2026-09-26. The priced BOM of the constructable design comes to USD 460.70 (SSK-CAL-001 v0.7, after the stage 3 rail fix of SSK-DEC-001 D-01), USD 105.70 over the value-engineering target that Amish set on 2026-10-01.
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
