"""StillStack concept media, generated from the parametric model (TRL 3).

Run from the repo root:  python cad/src/concept_media.py
Geometry comes from cad/src/model.py; numbers come from docs/04-calcs/sizing.py (SSK-CAL-001).
Not for fabrication.
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / ".kit"))
sys.path.insert(0, str(HERE))
from concept import Part, render_all, human_figure  # noqa: E402
from build123d import Compound  # noqa: E402
import model  # noqa: E402

p = model.PARAMS
parts = model.build()
# fold the parts added for construction (SSK-DDR-003) into the BOM groups the media number
_fold = {"Insulated frame": ["Base ring", "Stack stops", "Glazing trim", "Glazing tape"],
         "Feed trough": ["Feed closure"], "Distillate manifold": ["Outlet brackets"]}
for _k, _extra in _fold.items():
    for _e in _extra:
        if _e in parts:
            parts[_k] = parts[_k] + parts.pop(_e)
s, c = math.sin(math.radians(p["tilt"])), math.cos(math.radians(p["tilt"]))
n = (s, 0.0, c)            # panel normal in world
down = (c, 0.0, -s)        # down the slope in world


def along(v, d):
    return tuple(round(d * a, 1) for a in v)


def plus(a, b):
    return tuple(x + y for x, y in zip(a, b))


spec = [
    # name in model, label, color, BOM line, explode offset
    ("Glazing", "Glazing, twin-wall polycarbonate", "#BFDBFE", 1, along(n, 900)),
    ("Insulated frame", "Insulated frame", "#B08D57", 2, (0, 0, 0)),
    ("Absorber plate", "Absorber plate, black", "#1F2937", 3, along(n, 720)),
    ("Wicks", "Wick strips, 4 stages", "#E7D8B8", 4, along(n, 560)),
    ("Condenser plates", "Condenser plates, 4", "#A8B0B8", 5, along(n, 200)),
    ("Side spacer rails", "Side spacer rails", "#0F766E", 6, along(n, 400)),
    ("Spacer ribs", "Spacer ribs, silicone cord", "#DC2626", 7, plus(along(n, 470), (0, 420, 0))),
    ("Feed trough", "Feed trough", "#2563EB", 8, plus(along(down, -260), along(n, 120))),
    ("Distillate manifold", "Distillate manifold", "#0EA5E9", 9, plus(along(down, 240), along(n, 140))),
    ("Brine gutter", "Brine gutter", "#C2410C", 10, plus(along(down, 380), along(n, -60))),
    ("Heat-rejection fins", "Rear heat-rejection fins", "#6B7280", 11, along(n, -160)),
    ("Adjustable tilt stand", "Adjustable tilt stand", "#8B5E34", 12, (0, 0, -480)),
]
media_parts = [Part(label, parts[key], color, bom, off) for key, label, color, bom, off in spec]
# 1.75 m person for scale, set well clear of the panel so it does not overlap the isometric view
_bb = Compound(children=list(parts.values())).bounding_box()
person = human_figure(1750.0, x=_bb.max.X + 1000.0, y=_bb.max.Y + 300.0, z=0.0)

render_all(
    media_parts, project="StillStack", title="Four-stage wick still concept", dwg_no="SSK-DWG-001",
    rev="P4", date="2026-10-01",
    key_figures=["1.0 m2 aperture, tilt 20 deg (stand 10 to 35 deg)", "4 stages, 6 mm vapor gaps, ribs at 194 mm",
                 "About 10.6 L per day on 5.5 kWh/m2 (SSK-CAL-001)",
                 "Gained output ratio about 1.3",
                 "Dry stagnation about 140 C; stages 1, 2 rated 150 C",
                 "About USD 416 in parts (target USD 355)"],
    cut_exclude=("Adjustable tilt stand",), scale_figure=False, context=[person],
    flow={"title": "energy (MJ) and water per m2 per day at 5.5 kWh/m2, total about 11 L (CALCULATED ESTIMATES, SSK-CAL-001)",
          "unit": "MJ",
          "stages": [("Sunlight", 19.8), ("Absorber", 15.1), ("Stage 1: 3.5 L", 10.5),
                     ("Stage 2: 3.0 L", 9.2), ("Stage 3: 2.6 L", 8.1), ("Stage 4: 2.3 L", 7.3),
                     ("Heat to air", 6.6)],
          "losses": [(0, "Reflection", 4.8), (1, "Top and edge loss", 4.6), (2, "Feed heating", 1.3),
                     (3, "Feed heating", 1.0), (4, "Feed heating", 0.8), (5, "Feed heating", 0.6)]},
)
