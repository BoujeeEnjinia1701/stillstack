"""StillStack parametric model (build123d), TRL 3, constructable design (SSK-DDR-003).

Run from the repo root:
    python cad/src/model.py            exports STEP and STL, prints masses and the tilt check
    python cad/src/model.py --check    also runs the constructability checks (overlaps, contacts,
                                       clearances, stand geometry at every tilt hole)

The panel is modelled flat in a local frame and then tilted about the front pivot:
  local x runs down the slope (x < 0 is the high, feed edge; x > 0 the low, collection edge),
  local y runs across the panel, local z is the panel normal (toward the sun).
Stack, bottom up: bottom plate (last condenser, fins underneath), then for each stage a vapor
gap and a wick bonded under the plate above; the top plate is the absorber.

Design for construction (SSK-DDR-003, made under Amish's 2026-09-30 instruction to make the
design physically buildable; open for his review):
  * a 12 mm plywood base ring under the walls carries the stack edges (the concept's ledge);
  * walls stop under the glazing, which sits on foam tape and is held by an aluminium trim;
  * the walls have openings (not slits) where the stack passes through;
  * the plates' low edges are cut to a zigzag that leads condensate to distillate tongues at the
    rib lines and corners; wick tails leave on brine tongues at the strip centres, over the
    lidded distillate manifold into the brine gutter (Proposed, awaiting Amish: A1, R4);
  * two stop blocks at the low corners hold the stack against sliding down the slope;
  * the feed-end wick tails rise up the high wall behind a foam closure into the trough;
  * the stand is a ground frame, front posts with gussets and a pivot bolt, and fixed-length
    props pinned to the ground rails at one hole per tilt (10 to 35 deg).
The stagnation cover (BOM line 14) is a loose accessory and is not modelled.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from build123d import Box, Compound, Cylinder, Polygon, Pos, Rot, extrude, export_step, export_stl

# Top-level parameters (mm, deg). Edit these, not the geometry below.
PARAMS = {
    "tilt": 20.0,          # deg from horizontal; the stand allows 10 to 35 in 5 deg steps (R11)
    "aperture": 1000.0,    # square aperture side
    "n_stages": 4,
    "plate_t": 0.5,        # aluminium absorber and condenser plates
    "plate_clear": 2.0,    # clearance each side for thermal growth (about 1.4 mm at 60 K)
    "wick_t": 1.0,
    "gap": 6.0,            # vapor gap, wick face to condensing face
    "rail_w": 12.0,        # side rail width (150 degC polymer in stages 1 and 2, PC in 3 and 4)
    "rib_d": 7.0,          # silicone cord rib diameter (gap plus wick)
    "n_ribs": 4,           # intermediate ribs per gap (CAL-001 section 3)
    "wick_break": 10.0,    # dry break each side of a rib or rail and inside a plate edge (R4)
    "air_gap": 25.0,       # absorber to glazing
    "glaz_t": 6.0,         # twin-wall polycarbonate
    "glaz_size": 1060.0,   # glazing sheet, square; rests on the wall tops
    "tape_t": 3.0,         # silicone foam glazing tape under the glazing
    "trim": (25.0, 20.0, 2.0),   # glazing trim angle: leg on the glazing, leg down the wall, thickness
    "ply_t": 12.0,         # plywood wall
    "foam_t": 25.0,        # stone wool liner (rated well above 150 degC)
    "ring_t": 12.0,        # plywood base ring under the walls
    "ledge": 15.0,         # base ring overlap into the aperture (carries the stack edges)
    "fin_n": 10, "fin_depth": 30.0, "fin_t": 0.5, "fin_flange": 20.0, "fin_len": 940.0,
    # low edge: distillate tongues at the rib lines and corners, brine tongues at strip centres
    "corner_tongue": 465.0,  # y of the corner distillate tongues (clear of the stop blocks)
    "d_tongue_w": 30.0,    # distillate tongue width
    "b_tongue_w": 50.0,    # brine tongue width (wick tail 30 mm, 10 mm dry each side)
    "tail_w": 30.0,        # wick tail width at the low end
    "v_depth": 25.0,       # depth of the zigzag low edge, tongue tip to brine tongue root
    "d_bend": 545.0,       # x where the bottom plate's distillate tongues turn down (+4 per level)
    "b_bend": 616.0,       # x where the lowest brine tongue turns down (+4 per level)
    "lid_z": -4.0,         # top of the distillate manifold lid (local z)
    "manifold": (541.0, 56.0, 50.0),   # inboard x, width, height of the manifold channel
    "gutter": (604.0, 70.0, 40.0),     # inboard x, width, height of the brine gutter
    "bracket": (30.0, 4.0),            # outlet bracket flat bar
    "bracket_y": 335.0,                # outlet bracket centres, each side (solid wall between openings)
    "trough": (546.0, 70.0, 36.0),     # trough inner wall x (outboard of the high wall), size, rim z
    "front_h": 350.0,      # height of the low edge underside (base ring) above ground
    "post": 45.0,          # timber section
    "pivot": (512.0, 10.0),            # front pivot bolt, local (x, z) on the side wall
    "prop_hinge": (-470.0, 10.0),      # prop hinge bolt, local (x, z) through the prop block
    "prop_len": 1000.0,    # prop pin centres
    "tilt_holes": (10.0, 15.0, 20.0, 25.0, 30.0, 35.0),
    "rail_rear": 760.0,    # ground rail length behind the pivot (centre of mass at 10 deg is about 500 mm back)
    "gusset": 150.0,       # plywood gusset leg at each post foot (inside face, behind the post)
}

DENSITY = {  # kg/m3, for the mass cross-check against CAL-001
    "Absorber plate": 2700, "Condenser plates": 2700, "Heat-rejection fins": 2700,
    "Glazing": 217,  # twin-wall sheet: 1.3 kg/m2 over 6 mm
    "Wicks": 200, "Side spacer rails": 1200, "Spacer ribs": 1150,
    "Insulated frame": 330,  # plywood walls (550) and stone wool liner (140), by volume share
    "Base ring": 550, "Glazing trim": 2700, "Glazing tape": 300, "Stack stops": 1350,
    "Outlet brackets": 2700, "Feed closure": 300,
}


def _slab(z0, t, lx, ly, x=0.0, y=0.0):
    return Pos(x, y, z0 + t / 2) * Box(lx, ly, t)


def _box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _union(shapes):
    shapes = [s for s in shapes if s is not None]
    out = shapes[0]
    for sh in shapes[1:]:
        out = out + sh
    return out


def _prism(pts_xy, z0, t):
    """Extrude a polygon given as (x, y) points from z0 up by t, whichever way the points run."""
    sh = extrude(Polygon(*pts_xy, align=None), t)
    return Pos(0, 0, z0 - sh.bounding_box().min.Z) * sh


def rib_positions(p=PARAMS):
    span = p["aperture"] - 2 * p["plate_clear"] - 2 * p["rail_w"]    # clear span between side rails
    n = p["n_ribs"] + 1
    y0 = -span / 2
    return [y0 + span * i / n for i in range(1, n)]


def wick_strips(p=PARAMS):
    """(y_min, y_max) of each wick strip between rails and ribs, with dry breaks (R4)."""
    inner = p["aperture"] / 2 - p["plate_clear"] - p["rail_w"]
    edges = [-inner] + [y for r in rib_positions(p) for y in (r - p["rib_d"] / 2, r + p["rib_d"] / 2)] + [inner]
    return [(a + p["wick_break"], b - p["wick_break"]) for a, b in zip(edges[0::2], edges[1::2])]


def derived(p=PARAMS):
    """Every derived level and position the parts, checks and pictures share."""
    AP = p["aperture"]
    half = AP / 2 - p["plate_clear"]                 # plate half size (498)
    OH = AP / 2 + p["ply_t"] + p["foam_t"]           # outer half size of the frame (537)
    z, levels = 0.0, []                               # plate bottoms, bottom plate first
    levels.append(z); z += p["plate_t"]
    for k in range(p["n_stages"]):
        z += p["gap"] + p["wick_t"]
        levels.append(z)
        z += p["plate_t"]
    stack_top = z
    glaz_z = stack_top + p["air_gap"]
    wall_top = glaz_z - p["tape_t"]
    strips = wick_strips(p)
    yb = [(a + b) / 2 for a, b in strips]
    yd = [-p["corner_tongue"]] + rib_positions(p) + [p["corner_tongue"]]
    return dict(half=half, OH=OH, levels=levels, stack_top=stack_top, glaz_z=glaz_z, wall_top=wall_top,
                open_top=stack_top + 2.5, strips=strips, yb=yb, yd=yd,
                tip=half, root=half - p["v_depth"], FZ0=-p["ring_t"])


def edge_points(p=PARAMS):
    """The plates' low edge as (y, x) points from y = -half to +half: flat tips at the
    distillate tongues, flat roots at the brine tongues, straight lines between."""
    D = derived(p)
    feats = [(y, "d") for y in D["yd"]] + [(y, "b") for y in D["yb"]]
    feats.sort()
    pts = [(-D["half"], D["tip"])]
    for y, kind in feats:
        w = (p["d_tongue_w"] if kind == "d" else p["b_tongue_w"]) / 2
        x = D["tip"] if kind == "d" else D["root"]
        pts += [(y - w, x), (y + w, x)]
    pts.append((D["half"], D["tip"]))
    return pts


def edge_x(y, p=PARAMS):
    pts = edge_points(p)
    for (y0, x0), (y1, x1) in zip(pts, pts[1:]):
        if y0 <= y <= y1:
            return x0 if y1 == y0 else x0 + (x1 - x0) * (y - y0) / (y1 - y0)
    return pts[-1][1]


def tongue_lengths(lvl, p=PARAMS):
    """Straight (unbent) tongue lengths of the plate at level lvl, measured from the tip line
    (distillate) and from the root line (brine), and where each is bent (mm from that line)."""
    D = derived(p)
    z0, t = D["levels"][lvl], p["plate_t"]
    xb = p["d_bend"] + 4 * lvl
    xbb = p["b_bend"] + 4 * (lvl - 1)
    return dict(d_bend=xb - D["tip"], d_len=xb - D["tip"] + z0 + t + 9.0,
                b_bend=xbb - D["root"], b_len=xbb - D["root"] + z0 + t + 24.0)


def plate(kind, lvl, p=PARAMS, bent=True, split=False):
    """One plate in the local frame. kind: 'bottom' (distillate tongues only), 'cond'
    (distillate and brine tongues) or 'absorber' (brine tongues only). lvl: 0 for the bottom
    plate, 4 for the absorber. bent=False gives the tongues straight, as the plate goes in.
    Returns (plate with tongues, chevron dams or None), or with split=True
    (body, distillate tongues, brine tongues, dams)."""
    D = derived(p)
    z0, t = D["levels"][lvl], p["plate_t"]
    h = D["half"]
    L = tongue_lengths(lvl, p)
    outline = [(-h, -h)] + [(x, y) for y, x in edge_points(p)] + [(-h, h)]
    body = _prism(outline, z0, t)
    parts, dt, btg = [body], [], []
    if kind in ("bottom", "cond"):
        xb = p["d_bend"] + 4 * lvl
        for y in D["yd"]:
            w = p["d_tongue_w"] / 2
            if bent:
                dt.append(_box(D["tip"] - 0.5, xb + t, y - w, y + w, z0, z0 + t))
                dt.append(_box(xb, xb + t, y - w, y + w, -9.0, z0 + t))
            else:
                dt.append(_box(D["tip"] - 0.5, D["tip"] + L["d_len"], y - w, y + w, z0, z0 + t))
    dams = None
    if kind in ("cond", "absorber"):
        xbb = p["b_bend"] + 4 * (lvl - 1)
        for y in D["yb"]:
            w = p["b_tongue_w"] / 2
            if bent:
                btg.append(_box(D["root"] - 0.5, xbb + t, y - w, y + w, z0, z0 + t))
                btg.append(_box(xbb, xbb + t, y - w, y + w, -24.0, z0 + t))
            else:
                btg.append(_box(D["root"] - 0.5, D["root"] + L["b_len"], y - w, y + w, z0, z0 + t))
        if kind == "cond":     # chevron dam of silicone on the condensing face at each brine tongue root
            ds = []
            for y in D["yb"]:
                w = p["b_tongue_w"] / 2
                for sgn in (-1, 1):
                    a = (D["root"] - 16.0, y)
                    b = (D["root"] - 1.0, y + sgn * (w + 1.0))
                    dx, dy = b[0] - a[0], b[1] - a[1]
                    L = math.hypot(dx, dy)
                    nx, ny = -dy / L * 1.5, dx / L * 1.5
                    ds.append(_prism([(a[0] + nx, a[1] + ny), (b[0] + nx, b[1] + ny), (b[0] - nx, b[1] - ny),
                                      (a[0] - nx, a[1] - ny)], z0 + t, 3.0))
            dams = _union(ds)
    dts = _union(dt) if dt else None
    bts = _union(btg) if btg else None
    if split:
        return body, dts, bts, dams
    return _union(parts + dt + btg), dams


def wick(stage, p=PARAMS, bent=True, split=False):
    """Wick strips of one stage (1 = under the absorber), with both tails. The strips stop
    10 mm inside the plate's zigzag edge; a 30 mm tail runs under each brine tongue at the low
    end; at the high end each strip runs out through its wall opening, up the outside of the
    wall behind the foam closure, over the trough rim and down into the feed."""
    D = derived(p)
    lvl = p["n_stages"] - stage + 1          # plate the wick hangs under
    z1 = D["levels"][lvl]
    z0 = z1 - p["wick_t"]
    OH = D["OH"]
    s = stage
    xv = -OH - s                              # rising tail, outermost for the lowest stage
    lay = p["trough"][2] + (p["n_stages"] - s)            # layer over the trough rim
    xin = -p["trough"][0] - 6.0 - (p["n_stages"] - s)      # falling tail inside the trough
    out, tails = [], []
    xbb = p["b_bend"] + 4 * (lvl - 1)
    L = tongue_lengths(lvl, p)
    for (a, b), yb in zip(D["strips"], D["yb"]):
        ys = [a] + [y for y, _ in edge_points(p) if a < y < b] + [b]
        low = [(edge_x(y, p) - 13.0, y) for y in ys]
        outline = [(xv, a)] + low + [(xv, b)]
        out.append(_prism(outline, z0, p["wick_t"]))
        tw = p["tail_w"] / 2
        if bent:
            tails.append(_box(D["root"] - 14.0, xbb, yb - tw, yb + tw, z0, z1))      # low tail, under the brine tongue
            tails.append(_box(xbb - 1.0, xbb, yb - tw, yb + tw, -24.0, z0))
        else:
            tails.append(_box(D["root"] - 14.0, D["root"] + L["b_len"] - 1.0, yb - tw, yb + tw, z0, z1))
        out.append(_box(xv, xv + 1.0, a, b, z0, lay + 1.0))                          # high tail, up the wall
        out.append(_box(xin, xv + 1.0, a, b, lay, lay + 1.0))                         # over the rim
        out.append(_box(xin, xin + 1.0, a, b, -20.0, lay))                            # down into the feed
    if split:
        return _union(out), _union(tails)
    return _union(out + tails)


def build_components(p=PARAMS, tilt=None, local_only=False):
    """{part name: shape}. Panel parts in the local frame when local_only, else in the world
    with the stand. Part names are the constructable components, finer than build()'s groups."""
    tilt = p["tilt"] if tilt is None else tilt
    D = derived(p)
    AP, h, OH = p["aperture"], D["half"], D["OH"]
    WT, FT = p["ply_t"], p["foam_t"]
    wt, ot = D["wall_top"], D["open_top"]
    C = {}

    # ---- base ring: four plywood strips under the side and high walls, inside the low wall's sill
    ri = AP / 2 - p["ledge"]
    z0r = D["FZ0"]
    xl = OH - WT                                     # inside face of the low wall (525)
    C["ring_side_r"] = _box(-OH, xl, ri, OH, z0r, 0)
    C["ring_side_l"] = _box(-OH, xl, -OH, -ri, z0r, 0)
    C["ring_high"] = _box(-OH, -ri, -ri, ri, z0r, 0)
    C["ring_low"] = _box(ri, xl, -ri, ri, z0r, 0)

    # ---- walls: side walls full length; high and low walls between them; liner inside.
    # The low wall is a comb (sill and teeth) with open-topped notches for the tongues, so each
    # plate drops in from above, and a removable cap that closes the notches above the stack.
    C["wall_side_r"] = _box(-OH, OH, OH - WT, OH, 0, wt)
    C["wall_side_l"] = _box(-OH, OH, -OH, -OH + WT, 0, wt)
    li = AP / 2
    C["liner_side_r"] = _box(-OH + WT, OH - WT, li, li + FT, 0, wt)
    C["liner_side_l"] = _box(-OH + WT, OH - WT, -li - FT, -li, 0, wt)
    high = _box(-OH, -OH + WT, -OH + WT, OH - WT, 0, wt)
    lh = _box(-li - FT, -li, -li, li, 0, wt)
    for a, b in D["strips"]:                        # feed openings, one per wick strip
        cut = _box(-OH - 1, -li + 1, a - 5, b + 5, -1, ot)
        high, lh = high - cut, lh - cut
    yst = h - p["rail_w"] - 1.0                      # stop blocks fill the liner's corners (485 to 500)
    low = _box(xl, OH, -OH + WT, OH - WT, z0r, ot)
    ll = _box(li, xl, -yst, yst, 0, ot)
    for y, w in [(y, 20.0) for y in D["yd"]] + [(y, 30.0) for y in D["yb"]]:   # tongue notches
        cut = _box(li - 1, OH + 1, y - w, y + w, 0, ot + 1)
        low, ll = low - cut, ll - cut
    C["wall_high"], C["liner_high"] = high, lh
    C["wall_low"], C["liner_low"] = low, ll
    C["wall_low_cap"] = _box(xl, OH, -OH + WT, OH - WT, ot, wt)
    C["liner_low_cap"] = _box(li, xl, -li, li, ot, wt)
    C["stops"] = _union([_box(h, xl, *sorted((sg * yst, sg * li)), 0, ot) for sg in (-1, 1)])

    # ---- stack
    n = p["n_stages"]
    C["plate_bottom"], _ = plate("bottom", 0, p)
    for lvl in range(1, n):
        stage_above = n - lvl + 1                   # plate lvl carries the wick of stage (n - lvl + 1)
        C[f"plate_{n - lvl}"], C[f"dams_{n - lvl}"] = plate("cond", lvl, p)   # plate_1 is just under the absorber
    C["absorber"], _ = plate("absorber", n, p)
    for st in range(1, n + 1):
        lvl = n - st + 1
        zb = D["levels"][lvl - 1] + p["plate_t"]    # top of the plate below
        hgt = p["gap"] + p["wick_t"]
        C[f"rails_{st}"] = _union([_slab(zb, hgt, 2 * h, p["rail_w"], y=sg * (h - p["rail_w"] / 2)) for sg in (-1, 1)])
        rl = 2 * h - 8.0                             # ribs stop 8 mm short of the tongue tips
        C[f"ribs_{st}"] = _union([Pos(-h + rl / 2, ry, zb + hgt / 2) * Rot(0, 90, 0) * Cylinder(p["rib_d"] / 2, rl)
                                  for ry in rib_positions(p)])
        C[f"wick_{st}"] = wick(st, p)

    # ---- fins under the bottom plate, running down the slope (flange bonded to the plate)
    pitch = 2 * h / p["fin_n"]
    fins = []
    for i in range(p["fin_n"]):
        y = -h + pitch * (i + 0.5)
        fins.append(_box(-p["fin_len"] / 2, p["fin_len"] / 2, y - p["fin_flange"] / 2, y + p["fin_flange"] / 2, -p["fin_t"], 0))
        fins.append(_box(-p["fin_len"] / 2, p["fin_len"] / 2, y - p["fin_flange"] / 2, y - p["fin_flange"] / 2 + p["fin_t"],
                         -p["fin_depth"], -p["fin_t"]))
    C["fins"] = _union(fins)

    # ---- glazing, tape, trim
    gs = p["glaz_size"] / 2
    C["tape"] = _box(-gs, gs, -gs, gs, wt, D["glaz_z"]) - _box(-li, li, -li, li, wt - 1, D["glaz_z"] + 1)
    C["glazing"] = _box(-gs, gs, -gs, gs, D["glaz_z"], D["glaz_z"] + p["glaz_t"])
    tl, td, tt = p["trim"]
    gt = D["glaz_z"] + p["glaz_t"]
    xo = OH + tt
    ring = _box(-xo, xo, -xo, xo, gt, gt + tt) - _box(-xo + tl, xo - tl, -xo + tl, xo - tl, gt - 1, gt + tt + 1)
    skirt = _box(-xo, xo, -xo, xo, gt + tt - td, gt + tt) - _box(-OH, OH, -OH, OH, gt - td - 1, gt + tt + 1)
    C["trim"] = ring + skirt

    # ---- feed trough, foam closure and trough brackets (high edge)
    xi, tw_, rim = p["trough"]
    tz0 = rim - tw_
    tr = _box(-xi - tw_, -xi, -AP / 2, AP / 2, tz0, rim) - _box(-xi - tw_ + 5, -xi - 5, -AP / 2 + 5, AP / 2 - 5, tz0 + 5, rim + 1)
    C["trough"] = tr
    ya, yb_ = D["strips"][0][0] - 5, D["strips"][-1][1] + 5
    C["closure"] = _box(-xi, -OH - n, ya, yb_, 0, ot)
    br = []
    for sg in (-1, 1):
        y0 = sg * (AP / 2 - 7)
        br.append(_box(-OH - 3, -OH, y0 - 10, y0 + 10, tz0 - 3, 25))
        br.append(_box(-xi - tw_ - 3, -OH, y0 - 10, y0 + 10, tz0 - 3, tz0))
        br.append(_box(-xi - tw_ - 3, -xi - tw_, y0 - 10, y0 + 10, tz0 - 3, tz0 + 30))
    C["trough_brackets"] = _union(br)

    # ---- distillate manifold with slotted lid, brine gutter, outlet brackets (low edge)
    mx, mw, mh = p["manifold"]
    lz = p["lid_z"]
    ch = _box(mx, mx + mw, -AP / 2, AP / 2, lz - mh, lz - 2) - _box(mx + 3, mx + mw - 3, -AP / 2 + 3, AP / 2 - 3, lz - mh + 3, lz)
    ch = ch + Pos(mx + mw / 2, AP / 2 - 30, lz - mh - 30) * Cylinder(8, 60)
    C["manifold"] = ch
    lid = _box(mx, mx + mw, -AP / 2, AP / 2, lz - 2, lz)
    for y in D["yd"]:
        lid = lid - _box(mx + 3, mx + 19, y - 18, y + 18, lz - 3, lz + 1)
    C["lid"] = lid
    gx, gw, gh = p["gutter"]
    gz1 = lz - mh + gh
    gut = _box(gx, gx + gw, -AP / 2, AP / 2, lz - mh, gz1) - _box(gx + 3, gx + gw - 3, -AP / 2 + 3, AP / 2 - 3, lz - mh + 3, gz1 + 1)
    C["gutter"] = gut + Pos(gx + gw / 2, -AP / 2 + 30, lz - mh - 30) * Cylinder(8, 60)
    bw, bt = p["bracket"]
    ob = []
    for sg in (-1, 1):
        y0 = sg * p["bracket_y"]
        ob.append(_box(OH, OH + bt, y0 - bw / 2, y0 + bw / 2, lz - mh - bt, 30.0))
        ob.append(_box(OH, gx + gw + 6, y0 - bw / 2, y0 + bw / 2, lz - mh - bt, lz - mh))
    C["outlet_brackets"] = _union(ob)

    if local_only:
        return C

    W = {k: place(v, p, tilt) for k, v in C.items()}
    W.update(stand(p, tilt))
    return W


def pivot_world(p=PARAMS):
    """The front pivot is fixed in the world: x = 0, at the height where the base ring
    underside sits front_h above the ground when the panel is level."""
    return 0.0, p["front_h"] + p["pivot"][1] - derived(p)["FZ0"]


def place(sh, p=PARAMS, tilt=None):
    """Panel frame to world: rotate the panel about the front pivot."""
    tilt = p["tilt"] if tilt is None else tilt
    X0, Z0 = pivot_world(p)
    return Pos(X0, 0, Z0) * Rot(0, tilt, 0) * Pos(-p["pivot"][0], 0, -p["pivot"][1]) * sh


def to_world(xl, zl, p=PARAMS, tilt=None):
    tilt = p["tilt"] if tilt is None else tilt
    s, c = math.sin(math.radians(tilt)), math.cos(math.radians(tilt))
    X0, Z0 = pivot_world(p)
    dx, dz = xl - p["pivot"][0], zl - p["pivot"][1]
    return X0 + dx * c + dz * s, Z0 - dx * s + dz * c


def centre_of_mass(p=PARAMS, tilt=None, wet=True):
    """World (x, z) of the centre of mass of the panel (wicks wet) at a tilt."""
    tilt = p["tilt"] if tilt is None else tilt
    G = build(p, local_only=True)
    m_tot, mx, mz = 0.0, 0.0, 0.0
    for name, rho in DENSITY.items():
        if name not in G:
            continue
        sh = G[name]
        m = sh.volume * 1e-9 * rho * (5.0 if (wet and name == "Wicks") else 1.0)
        cpt = sh.center()
        x, z = to_world(cpt.X, cpt.Z, p, tilt)
        m_tot += m; mx += m * x; mz += m * z
    return mx / m_tot, mz / m_tot


def stand_geometry(p=PARAMS, tilt=None):
    """Pivot, prop hinge and prop foot (world x, z) at a tilt, and the foot hole positions."""
    tilt = p["tilt"] if tilt is None else tilt
    P_ = p["post"]
    pv = to_world(*p["pivot"], p, tilt)
    hg = to_world(*p["prop_hinge"], p, tilt)
    zf = P_ / 2

    def foot(t):
        hx, hz = to_world(*p["prop_hinge"], p, t)
        dz = hz - zf
        return hx + math.sqrt(p["prop_len"] ** 2 - dz ** 2), zf
    holes = {t: foot(t)[0] for t in p["tilt_holes"]}
    return dict(pivot=pv, hinge=hg, foot=foot(tilt), holes=holes)


def stand(p=PARAMS, tilt=None):
    """Stand parts in the world: ground rails, cross rails, posts, gussets, prop blocks, props."""
    tilt = p["tilt"] if tilt is None else tilt
    D = derived(p)
    OH, P_ = D["OH"], p["post"]
    G = stand_geometry(p, tilt)
    px, pz = G["pivot"]
    x_rear = px - p["rail_rear"]          # far enough back to keep the centre of mass inside the frame
    x_front = px + P_ / 2 + P_            # front cross rail just in front of the posts
    out = {}
    rails, posts, gus, blocks, props, cross, bolts = [], [], [], [], [], [], []
    for sg in (-1, 1):
        y0, y1 = sorted((sg * OH, sg * (OH + P_)))
        rail = _box(x_rear, x_front, y0, y1, 0, P_)
        for hx_ in G["holes"].values():               # one 10.5 mm hole per tilt
            rail = rail - Pos(hx_, (y0 + y1) / 2, P_ / 2) * Rot(90, 0, 0) * Cylinder(5.25, P_ + 2)
        rails.append(rail)
        posts.append(_box(px - P_ / 2, px + P_ / 2, y0, y1, P_, pz + 22.0))
        # plywood gusset on the inside faces of the post and rail, behind the post
        go = min(sg * (OH - 12.0), sg * OH)
        g = p["gusset"]
        xa = px + P_ / 2
        tri = Rot(90, 0, 0) * extrude(Polygon((xa, 0), (xa - P_ - g, 0), (xa, P_ + g), align=None), 12.0)
        gb = tri.bounding_box()
        gus.append(Pos(0, go - gb.min.Y, 0) * tri)
        # prop block on the side wall (in the panel frame), then the prop itself
        yb0, yb1 = sorted((sg * OH, sg * (OH + P_)))
        blk = _box(p["prop_hinge"][0] - 60, p["prop_hinge"][0] + 60, yb0, yb1, D["FZ0"], D["FZ0"] + P_)
        blocks.append(place(blk, p, tilt))
        hx, hz = G["hinge"]
        fx, fz = G["foot"]
        L = math.hypot(fx - hx, fz - hz)
        ang = math.degrees(math.atan2(fx - hx, hz - fz))      # lean from vertical toward +x
        yp0, yp1 = sorted((sg * (OH + P_), sg * (OH + 2 * P_)))
        # square top end 22 mm past the hinge; foot end rounded to a 22 mm radius about its pin,
        # so it clears the ground at every tilt
        ux, uz = (fx - hx) / L, (fz - hz) / L
        cx, cz = hx - ux * 22.0 + (L + 22.0) / 2 * ux, hz - uz * 22.0 + (L + 22.0) / 2 * uz
        pr = Pos(cx, (yp0 + yp1) / 2, cz) * Rot(0, -ang, 0) * Box(P_, P_, L + 22.0)
        pr = pr + Pos(fx, (yp0 + yp1) / 2, fz) * Rot(90, 0, 0) * Cylinder(22.0, P_)
        props.append(pr)
        # bolts: pivot, prop hinge (through the block), prop pin (through the rail)
        for (bx, bz), ya_, yb2 in ((G["pivot"], OH - 12.0, OH + P_ + 14), (G["hinge"], OH - 12.0, OH + 2 * P_ + 3),
                                   (G["foot"], OH, OH + 2 * P_ + 3)):
            yy0, yy1 = sorted((sg * ya_, sg * yb2))
            bolts.append(Pos(bx, (yy0 + yy1) / 2, bz) * Rot(90, 0, 0) * Cylinder(5.0, yy1 - yy0))
    for xc in (x_rear + P_ / 2, x_front - P_ / 2):
        cross.append(_box(xc - P_ / 2, xc + P_ / 2, -OH, OH, 0, P_))
    out["ground_rails"] = _union(rails)
    out["cross_rails"] = _union(cross)
    out["posts"] = _union(posts)
    out["gussets"] = _union(gus)
    out["prop_blocks"] = _union(blocks)
    out["props"] = _union(props)
    out["stand_bolts"] = _union(bolts)
    return out


# ------------------------------------------------------------------ groups (concept media, GA, masses)
GROUPS = {
    "Glazing": ["glazing"],
    "Insulated frame": ["wall_side_r", "wall_side_l", "wall_high", "wall_low", "wall_low_cap", "liner_side_r",
                        "liner_side_l", "liner_high", "liner_low", "liner_low_cap"],
    "Base ring": ["ring_side_r", "ring_side_l", "ring_high", "ring_low"],
    "Absorber plate": ["absorber"],
    "Wicks": ["wick_1", "wick_2", "wick_3", "wick_4"],
    "Condenser plates": ["plate_1", "plate_2", "plate_3", "plate_bottom"],
    "Side spacer rails": ["rails_1", "rails_2", "rails_3", "rails_4"],
    "Spacer ribs": ["ribs_1", "ribs_2", "ribs_3", "ribs_4", "dams_1", "dams_2", "dams_3"],
    "Feed trough": ["trough", "trough_brackets"],
    "Feed closure": ["closure"],
    "Distillate manifold": ["manifold", "lid"],
    "Brine gutter": ["gutter"],
    "Outlet brackets": ["outlet_brackets"],
    "Heat-rejection fins": ["fins"],
    "Glazing trim": ["trim"],
    "Glazing tape": ["tape"],
    "Stack stops": ["stops"],
    "Adjustable tilt stand": ["ground_rails", "cross_rails", "posts", "gussets", "prop_blocks", "props", "stand_bolts"],
}


def build(p=PARAMS, tilt=None, local_only=False):
    """{group name: shape}, grouped as the concept media and the BOM number them."""
    C = build_components(p, tilt, local_only)
    out = {}
    for g, keys in GROUPS.items():
        ks = [k for k in keys if k in C and C[k] is not None]
        if ks:
            out[g] = _union([C[k] for k in ks])
    return out


STACK = ["Absorber plate", "Wicks", "Condenser plates", "Side spacer rails", "Spacer ribs", "Heat-rejection fins"]


def stack_detail(p=PARAMS, x=(-10.0, 10.0), y=(72.0, 122.0), z=(-32.0, 36.0), keep=None):
    """Slice of the untilted panel (local frame) for drawing detail views."""
    cut = Pos(sum(x) / 2, sum(y) / 2, sum(z) / 2) * Box(x[1] - x[0], y[1] - y[0], z[1] - z[0])
    keep = STACK if keep is None else keep
    local = build(p, local_only=True)
    out = []
    for k in keep:
        sh = local[k] & cut
        if sh.volume > 1e-6:
            out.append(sh)
    return Compound(children=out)


def assembly(parts):
    kids = []
    for name, sh in parts.items():
        sh.label = name
        kids.append(sh)
    return Compound(children=kids, label="StillStack assembly")


def masses(parts):
    return {name: parts[name].volume * 1e-9 * rho for name, rho in DENSITY.items() if name in parts}


def check_tilt_range(p=PARAMS):
    """R11: build at the ends of the tilt range and report clearances and heights."""
    rows = []
    for t in (10.0, 20.0, 35.0):
        parts = build(p, tilt=t)
        zmin = min(sh.bounding_box().min.Z for k, sh in parts.items() if k != "Adjustable tilt stand")
        bb = Compound(children=list(parts.values())).bounding_box()
        trough_top = parts["Feed trough"].bounding_box().max.Z
        rows.append((t, zmin, bb.size.X, bb.size.Y, trough_top))
    return rows


# ------------------------------------------------------------------ constructability checks
def _vol(a, b):
    ba, bb = a.bounding_box(), b.bounding_box()
    if (ba.max.X < bb.min.X or bb.max.X < ba.min.X or ba.max.Y < bb.min.Y or bb.max.Y < ba.min.Y
            or ba.max.Z < bb.min.Z or bb.max.Z < ba.min.Z):
        return 0.0
    try:
        return (a & b).volume
    except Exception:
        return float("nan")


def _dist(a, b):
    return a.distance_to(b)


def checks(p=PARAMS, verbose=True):
    """Constructability checks. Returns (n_pass, n_fail, rows)."""
    rows = []

    def rec(name, ok, value=""):
        rows.append((name, bool(ok), value))
        if verbose:
            print(f"  {'ok  ' if ok else 'FAIL'} {name} {value}")

    C = build_components(p, local_only=True)
    D = derived(p)
    names = [k for k, v in C.items() if v is not None]
    # 1. nothing overlaps anything else in the panel (0.5 mm3 tolerance for touching faces)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            v = _vol(C[a], C[b])
            if v != v or v > 0.5:
                rec(f"no overlap: {a} / {b}", False, f"{v:.1f} mm3")
    n_pairs = len(names) * (len(names) - 1) // 2
    if not any(not r[1] for r in rows):
        rec(f"no overlaps among {len(names)} panel parts ({n_pairs} pairs)", True)
    # 2. parts that must touch, touch
    must_touch = [("plate_bottom", "ring_low"), ("plate_bottom", "ring_side_r"), ("plate_bottom", "fins"),
                  ("rails_4", "plate_bottom"), ("rails_4", "plate_3"), ("rails_1", "absorber"), ("rails_1", "plate_1"),
                  ("ribs_4", "plate_bottom"), ("ribs_1", "absorber"), ("wick_1", "absorber"), ("wick_4", "plate_3"),
                  ("wall_side_r", "ring_side_r"), ("wall_low", "ring_low"), ("liner_high", "ring_high"),
                  ("wall_low_cap", "wall_low"), ("liner_low_cap", "liner_low"), ("wall_low_cap", "trim"),
                  ("tape", "wall_side_r"), ("glazing", "tape"), ("trim", "glazing"), ("trim", "wall_side_r"),
                  ("stops", "rails_1"), ("stops", "absorber"), ("stops", "plate_bottom"), ("stops", "wall_low"),
                  ("trough", "trough_brackets"), ("trough_brackets", "wall_high"), ("closure", "trough"),
                  ("closure", "wick_4"), ("manifold", "outlet_brackets"), ("lid", "manifold"),
                  ("gutter", "outlet_brackets"), ("outlet_brackets", "wall_low"), ("dams_1", "plate_1")]
    for a, b in must_touch:
        d = _dist(C[a], C[b])
        rec(f"touches: {a} / {b}", d < 0.05, f"{d:.2f} mm")
    # 3. clearances
    lid = C["lid"]
    for st in range(1, 5):
        d = _dist(C[f"wick_{st}"], lid)
        rec(f"wick {st} tails at least 10 mm from the distillate lid", d >= 10.0 - 1e-6, f"{d:.1f} mm")
    dist_all = _union([C["plate_bottom"], C["plate_1"], C["plate_2"], C["plate_3"]])
    for st in range(1, 5):
        tails = C[f"wick_{st}"] & _box(D["tip"] + 1, 800, -600, 600, -100, 100)
        dts = [_dist(tails, _box(D["tip"] + 1, 800, y - 15, y + 15, -100, 100) & dist_all) for y in D["yd"]]
        rec(f"wick {st} low tails at least 10 mm from every distillate tongue", min(dts) >= 10.0, f"{min(dts):.1f} mm")
    for k in ("plate_bottom", "plate_1", "plate_2", "plate_3", "absorber"):
        teeth = C["wall_low"] & _box(0, 1000, -1000, 1000, 0.6, 100)     # the sill is what the bottom plate rests on
        dw = _dist(C[k], teeth)
        dl = _dist(C[k], C["liner_low"])
        rec(f"{k} tongues pass the low wall notches clear", min(dw, dl) >= 1.0, f"{min(dw, dl):.1f} mm")
    gs = p["glaz_size"] / 2
    rec("glazing edge room to grow inside the trim (4.8 mm needed per sheet)", (D["OH"] - gs) * 2 >= 4.8,
        f"{D['OH'] - gs:.1f} mm each side")
    tl = p["trim"][0]
    rec("trim leg clear of the aperture (no shading)", D["OH"] + p["trim"][2] - tl >= p["aperture"] / 2,
        f"{D['OH'] + p['trim'][2] - tl:.0f} mm from centre")
    d = _dist(C["fins"], C["ring_low"])
    rec("fins clear of the base ring", d >= 2.0, f"{d:.1f} mm")
    # 4. stand at every tilt hole
    for t in p["tilt_holes"]:
        W = build_components(p, tilt=t)
        S = stand(p, t)
        panel = _union([W[k] for k in ("wall_side_r", "wall_side_l", "trim", "ring_side_r", "ring_side_l", "manifold",
                                       "gutter", "outlet_brackets", "trough", "trough_brackets", "glazing")])
        bad = []
        for k in ("posts", "props", "ground_rails", "cross_rails", "gussets"):
            v = _vol(S[k], panel)
            if v != v or v > 0.5:
                bad.append(f"{k} {v:.0f} mm3")
        for a, b in (("props", "posts"), ("props", "gussets"), ("props", "ground_rails"), ("posts", "prop_blocks")):
            v = _vol(S[a], S[b])
            if v != v or v > 0.5:
                bad.append(f"{a}/{b} {v:.0f} mm3")
        rec(f"stand at {t:.0f} deg: no clashes", not bad, ", ".join(bad))
        dpt = _dist(S["posts"], W["wall_side_r"])
        rec(f"stand at {t:.0f} deg: posts on the side walls", dpt < 0.05, f"{dpt:.2f} mm")
        dd_ = [_dist(S[a], S[b]) for a, b in (("props", "prop_blocks"), ("props", "ground_rails"), ("gussets", "posts"),
                                              ("gussets", "ground_rails"), ("posts", "ground_rails"))]
        rec(f"stand at {t:.0f} deg: props on blocks and rails, gussets on posts and rails", max(dd_) < 0.05,
            ", ".join(f"{x:.2f}" for x in dd_) + " mm")
        G = stand_geometry(p, t)
        zmin = min(W[k].bounding_box().min.Z for k in ("gutter", "manifold", "fins", "ring_low"))
        rec(f"stand at {t:.0f} deg: panel clear of the ground", zmin > 100, f"{zmin:.0f} mm")
        allb = Compound(children=list(W.values())).bounding_box()
        rec(f"stand at {t:.0f} deg: footprint within 1.3 x 1.3 m", allb.size.X <= 1300 and allb.size.Y <= 1300,
            f"{allb.size.X:.0f} x {allb.size.Y:.0f} mm")
        cg = centre_of_mass(p, t)
        rear = px_ = stand_geometry(p, t)["pivot"][0] - p["rail_rear"]
        rec(f"stand at {t:.0f} deg: centre of mass inside the ground frame", cg[0] - rear >= 150.0,
            f"{cg[0] - rear:.0f} mm in front of the rear rail end")
        tt = W["trough"].bounding_box().max.Z
        rec(f"stand at {t:.0f} deg: feed trough top at most 1.5 m", tt <= 1500, f"{tt:.0f} mm")
    n_ok = sum(1 for r in rows if r[1])
    return n_ok, len(rows) - n_ok, rows


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    parts = build()
    asm = assembly(parts)
    (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
    export_step(asm, str(root / "step" / "stillstack-assembly.step"))
    export_stl(asm, str(root / "stl" / "stillstack-assembly.stl"), tolerance=0.5)
    rail = Box(PARAMS["aperture"] - 2 * PARAMS["plate_clear"], PARAMS["rail_w"], PARAMS["gap"] + PARAMS["wick_t"])
    export_stl(rail, str(root / "stl" / "side-rail.stl"))
    bb = asm.bounding_box()
    D = derived()
    print(f"Assembly envelope at {PARAMS['tilt']:.0f} deg: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    print("Rib centers (mm):", ", ".join(f"{y:.1f}" for y in rib_positions()))
    print("Wick strip widths (mm):", ", ".join(f"{b - a:.0f}" for a, b in wick_strips()))
    print(f"Wall height {D['wall_top']:.1f} mm; stack top {D['stack_top']:.1f} mm; glazing underside {D['glaz_z']:.1f} mm")
    wet = 0.0
    for (a, b) in D["strips"]:
        ys = [a] + [y for y, _ in edge_points() if a < y < b] + [b]
        for y0, y1 in zip(ys, ys[1:]):
            wet += (y1 - y0) * ((edge_x(y0) + edge_x(y1)) / 2 - 13.0 + D["half"])
    print(f"Wet wick area per stage inside the plates: {wet / 1e6:.4f} m2 (fraction {wet / PARAMS['aperture'] ** 2:.3f})")
    m = masses(parts)
    for k, v in m.items():
        print(f"  {k:<22s} {v:6.2f} kg")
    print(f"Modelled panel mass (excl. trough, manifold, gutter, fasteners): {sum(m.values()):.1f} kg")
    G = stand_geometry()
    print("Prop foot hole positions along the ground rail, from the pivot (mm):",
          ", ".join(f"{t:.0f} deg {x - G['pivot'][0]:.0f}" for t, x in G["holes"].items()))
    print("Tilt check (tilt deg, lowest panel part above ground mm, plan X, plan Y, feed trough top mm):")
    for t, zmin, sx, sy, tt in check_tilt_range():
        print(f"  {t:4.0f}  {zmin:6.0f}  {sx:6.0f}  {sy:6.0f}  {tt:6.0f}")
    print("Exported cad/step/stillstack-assembly.step, cad/stl/stillstack-assembly.stl, cad/stl/side-rail.stl")
    if "--check" in sys.argv:
        print("Constructability checks:")
        ok, bad, _ = checks()
        print(f"{ok} checks pass, {bad} fail")
        sys.exit(1 if bad else 0)
