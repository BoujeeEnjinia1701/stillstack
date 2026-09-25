# StillStack

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Water Security · **TRL:** 3 of 9 (proof of concept on paper) · **Prototype budget:** about $250 USD (priced BOM about $317, over budget) · **Difficulty:** 3 of 5

Multi-stage wick still that reuses the latent heat of condensation from each stage in the next one.

![StillStack concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [General arrangement (PDF)](cad/drawings/SSK-DWG-002.pdf) · [Sizing note](docs/04-calcs/01-sizing.md) · [Review note](docs/REVIEW.md)

## Problem

Single-basin solar stills make only about 3 to 5 L per m2 per day.

## Concept

Multi-stage wick still that reuses the latent heat of condensation from each stage in the next one.

The TRL 3 sizing (SSK-CAL-001) gives about 10.6 L per m2 per day on a 5.5 kWh per m2 day, with a gained output ratio of about 1.3. Dry stagnation (about 140 °C) and cost are not yet within requirements.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Twin-wall polycarbonate glazing
- Insulated plywood and PIR frame
- Black aluminum absorber and four coated aluminum condenser plates
- Wick strips, four stages
- Polycarbonate side rails and silicone-cord spacer ribs
- Feed trough, lidded distillate manifold and brine gutter
- Rear heat-rejection fins and an adjustable tilt stand

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Distillate must be tested before drinking. Use food-safe materials on all wetted surfaces. The absorber reaches about 140 °C if the wicks run dry: shade the panel before maintenance. Anchor the stand against wind.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (SSK-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `SSK-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
