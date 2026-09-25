"""StillStack concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

The panel is modeled flat in a local frame and then tilted:
  local x runs down the slope (x = -500 is the high, feed edge; x = +500 the low, collection edge),
  local y runs across the panel, local z is the panel normal (toward the sun).
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot
from concept import Part, render_all

TILT = 20.0                 # deg from horizontal, proposed for latitudes of about 15 to 30 deg
AP = 1000.0                 # aperture, 1000 x 1000 mm = 1.0 m2
WALL = 50.0                 # insulated frame wall thickness
PLATE_T, WICK_T, GAP = 1.0, 1.0, 6.0   # per stage: wick under plate, vapor gap, next plate
N_STAGES = 4
AIR_GAP, GLAZ_T = 25.0, 6.0
H0 = 600.0                  # height of the local origin above the ground, mm

s, c = math.sin(math.radians(TILT)), math.cos(math.radians(TILT))


def place(shape):
    """Tilt a local-frame shape (high edge at -x rises) and lift it onto the stand."""
    return Pos(0, 0, H0) * Rot(0, TILT, 0) * shape


def world(x, z):
    """World (x, z) of a local (x, z) point."""
    return x * c + z * s, -x * s + z * c + H0


def slab(z0, t, lx=AP, ly=AP, x=0.0, y=0.0):
    return Pos(x, y, z0 + t / 2) * Box(lx, ly, t)


def union(shapes):
    out = shapes[0]
    for sh in shapes[1:]:
        out = out + sh
    return out


# Stage stack, bottom up. The bottom plate is the last condenser and rejects heat to air through the fins.
z = 0.0
condensers, wicks, spacers = [], [], []
condensers.append(slab(z, PLATE_T)); z += PLATE_T
for k in range(N_STAGES):
    gap0 = z
    spacers += [slab(gap0, GAP + WICK_T, ly=20.0, y=sy) for sy in (-490.0, 490.0)]  # side rails only; ends stay open
    z += GAP
    wicks.append(slab(z, WICK_T)); z += WICK_T
    if k < N_STAGES - 1:
        condensers.append(slab(z, PLATE_T)); z += PLATE_T
absorber_z = z
absorber = slab(z, PLATE_T); z += PLATE_T
glaz_z = z + AIR_GAP
glazing = slab(glaz_z, GLAZ_T)
top_z = glaz_z + GLAZ_T + 4.0          # frame lip above the glazing

# Insulated frame (plywood box with foam liner): four walls around the aperture.
FZ0 = -5.0
fh = top_z - FZ0
outer = AP + 2 * WALL
frame = (Pos(0, 0, FZ0 + fh / 2) * Box(outer, outer, fh)) - (Pos(0, 0, FZ0 + fh / 2) * Box(AP, AP, fh + 2))

# Rear heat-rejection fins under the bottom condenser plate (shaded side, open to air).
fins = union([slab(-30.0, 30.0, lx=AP - 40, ly=2.0, y=yy) for yy in range(-450, 451, 100)])

# Feed trough along the high edge, outside the frame; wicks drape over the wall into it.
trough = Pos(-outer / 2 - 35, 0, 35) * (Box(70, AP, 70) - Pos(0, 0, 6) * Box(60, AP - 10, 70))
# Distillate manifold along the low edge, fed by one slot per stage; outlet spout at one end.
dist = Pos(outer / 2 + 25, 0, 30) * (Box(50, AP, 40) - Pos(0, 0, 5) * Box(40, AP - 10, 40))
dist = dist + Pos(outer / 2 + 25, AP / 2 - 30, -20) * Cylinder(8, 60)
# Brine drain gutter under the distillate manifold, with a separate outlet at the other end.
brine = Pos(outer / 2 + 30, 0, -25) * (Box(60, AP, 30) - Pos(0, 0, 5) * Box(50, AP - 10, 30))
brine = brine + Pos(outer / 2 + 30, -AP / 2 + 30, -70) * Cylinder(8, 60)

# Tilt stand: four timber posts under the frame corners plus two ground rails.
POST = 45.0
stand_parts = []
post_x = []
for lx in (-(AP / 2), AP / 2 - 20):
    wx, wz = world(lx, FZ0)
    post_x.append(wx)
    for yy in (-(AP / 2 + WALL / 2), AP / 2 + WALL / 2):
        h = wz + 10.0                  # posts meet the underside of the tilted frame
        stand_parts.append(Pos(wx, yy, h / 2) * Box(POST, POST, h))
rail_len = abs(post_x[1] - post_x[0]) + 2 * POST + 60
for yy in (-(AP / 2 + WALL / 2), AP / 2 + WALL / 2):
    stand_parts.append(Pos(sum(post_x) / 2, yy, 20) * Box(rail_len, POST, 40))
stand_parts.append(Pos(post_x[0], 0, 250) * Box(POST, AP + 2 * WALL, 40))   # cross brace, high side
stand = union(stand_parts)

n = (s, 0.0, c)            # panel normal in world
down = (c, 0.0, -s)        # down the slope in world


def along(v, d):
    return tuple(round(d * a, 1) for a in v)


def plus(a, b):
    return tuple(x + y for x, y in zip(a, b))


parts = [
    Part("Glazing, twin-wall polycarbonate", place(glazing), "#BFDBFE", 1, along(n, 900)),
    Part("Insulated frame", place(frame), "#B08D57", 2, (0, 0, 0)),
    Part("Absorber plate, black", place(absorber), "#1F2937", 3, along(n, 700)),
    Part("Wicks, 4 stages", place(union(wicks)), "#E7D8B8", 4, along(n, 520)),
    Part("Condenser plates, 4", place(union(condensers)), "#A8B0B8", 5, along(n, 220)),
    Part("Stage spacers", place(union(spacers)), "#0F766E", 6, along(n, 380)),
    Part("Feed trough", place(trough), "#2563EB", 7, plus(along(down, -260), along(n, 120))),
    Part("Distillate manifold", place(dist), "#0EA5E9", 8, plus(along(down, 260), along(n, 120))),
    Part("Brine gutter", place(brine), "#C2410C", 9, plus(along(down, 360), along(n, -80))),
    Part("Rear heat-rejection fins", place(fins), "#6B7280", 10, along(n, -140)),
    Part("Tilt stand", stand, "#8B5E34", 11, (0, 0, -480)),
]

render_all(
    parts, project="StillStack", title="Four-stage wick still concept", dwg_no="SSK-DWG-001",
    key_figures=["1.0 m2 aperture, tilted 20 deg", "4 stages, 6 mm vapor gaps",
                 "About 13 L per day on 5.5 kWh/m2 (estimate)",
                 "Single stage: about 3.8 L per day (estimate)",
                 "Gained output ratio about 1.5 (estimate)",
                 "About $240 in parts (indicative)"],
    cut_exclude=(),
    flow={"title": "energy (MJ) and water per m2 per day at 5.5 kWh/m2, total about 13 L (ALL VALUES ESTIMATES)", "unit": "MJ",
          "stages": [("Sunlight (est.)", 19.8), ("Absorber", 16.8), ("Stage 1: 3.8 L", 12.4),
                     ("Stage 2: 3.5 L", 11.2), ("Stage 3: 3.1 L", 10.0), ("Stage 4: 2.8 L", 9.0),
                     ("Heat to air", 8.1)],
          "losses": [(0, "Reflection", 3.0), (1, "Top loss", 4.4), (2, "Edge loss", 1.2),
                     (3, "Edge loss", 1.1), (4, "Edge loss", 1.0), (5, "Edge loss", 0.9)]},
)
