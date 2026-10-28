---
doc_id: SSK-MKT-001
title: StillStack market and viability
project: StillStack
doc_type: Market and viability
version: '0.2'
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-24'
    author: Amish Chadha
    change: First market and viability note (kit 1.9.1 upgrade); prices checked 2026-10-24
  - version: '0.2'
    date: '2026-10-25'
    author: Amish Chadha
    change: 'Unit cost USD 460.70 (panel label, D-05, decided by Amish 2026-10-25)'
---

# StillStack market and viability

StillStack is for households, clinics and outposts that have only salty or brackish water and no reliable power, and for the NGOs and workshops that serve them; it competes with basin stills and small commercial stills that make a few litres a day. An open design matters because the people who need it are rarely reached by commercial desalination, and a still has to be built and repaired where it is used. Prices and benchmarks were checked 2026-10-24. Method: STANDARDS section 23.

Table 1. Market segments.

| Segment | Target users and region | Competitive benchmark (cited price) | Estimated cost per unit (USD) | Value proposition |
| --- | --- | --- | --- | --- |
| Coastal and saline-inland households | Southwest Bangladesh, Pacific atolls, Atacama coast, MENA (README) | SolAqua Rainmaker 550 solar still, USD 450 assembled or USD 245 as a kit, plus shipping (Farm Show, 2021); output not stated in the source | 460.70 in parts (BOM), plus local labour | About 10.3 L/m2/day on paper, two to three times a basin still of the same area, from parts sold almost anywhere |
| Emergency and marine | Liferafts, small boats, remote outposts | Aquamate inflatable solar still, USD 355.49 sale price (list USD 399.95), 0.5 to 2 L/day stated by the seller (AM Nautical, checked 2026-10-24) | 460.70 | Ten times the stated daily output for a fixed site; not portable in a pocket |
| NGOs, makerspaces and colleges | Groups that build and test water technology | Research multistage stills: none for sale; Chiavazzo et al. (2018) and Xu et al. (2020) are laboratory devices | 460.70 | Open drawings, build plan, calculation note and model to build, audit and adapt |
| Off-grid battery top-up water | Solar home and telecom systems | Distilled water bought in; price varies by region, to assess | 460.70 | Local supply of low-salt water |

The cost per litre over a life of a few years is not estimated yet: the life of the wicks, coating and rails in salty service is not known (SSK-RSK-001 P1, P2, P6). It is to assess at TRL 5 with a field partner.

## Open route

Community workshops, technical colleges and makerspaces build the panel from the build plan with plywood, cut sheet aluminium, a 3D printer for the stage 4 rails and common hardware; a coater applies the food-contact coating. NGOs and WASH programmes carry it to households once a university lab has measured the distillate (first candidate: the Politecnico di Torino group, SSK-DEC-001). CERN-OHL-S keeps every change open, and the parametric model and calculation note let a builder resize the panel or change materials with the numbers rechecked.

## Sources

- AM Nautical. "Aquamate Inflatable Solar Still Desalinator, Liferaft." https://amnautical.com/products/aquamate-inflatable-solar-still-desalinator-liferaft (checked 2026-10-24; listed as sold out).
- Farm Show Magazine. Article on the SolAqua Rainmaker 550 solar still. 2021, vol. 45, no. 6, p. 28. https://farmshow.com/a_article.php?aid=37586 (checked 2026-10-24).
- Chiavazzo, Eliodoro, Matteo Morciano, Francesca Viglino, Matteo Fasano, and Pietro Asinari. "Passive Solar High-Yield Seawater Desalination by Modular and Low-Cost Distillation." *Nature Sustainability* 1 (2018): 763 to 772. https://doi.org/10.1038/s41893-018-0186-x.
- Xu, Zhenyuan, Lenan Zhang, Lin Zhao, Bangjun Li, Bikram Bhatia, Chenxi Wang, Kyle L. Wilke, Youngsup Song, Omar Labban, John H. Lienhard, Ruzhu Wang, and Evelyn N. Wang. "Ultrahigh-Efficiency Desalination via a Thermally-Localized Multistage Solar Still." *Energy and Environmental Science* 13 (2020): 830 to 839. https://dspace.mit.edu/handle/1721.1/123794.
