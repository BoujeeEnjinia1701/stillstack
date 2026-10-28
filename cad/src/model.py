"""StillStack parametric model (build123d), kit 1.9 interface, TRL 3 (stage P3, detail level D3).

Run from the repo root:
    python .kit/cad_check.py --export  fidelity check of every option, STEP per part and per assembly
    python cad/src/model.py            exports the assembly STEP and STL, prints masses and the tilt check
    python cad/src/model.py --check    also runs the constructability checks (overlaps, contacts,
                                       clearances, stand geometry at every tilt hole)

Kit 1.9 (STANDARDS section 24; Amish, 2026-10-24: "Detail every option"): OPTIONS, PRINCIPLES, CHOSEN,
OPTION_VIEWS and components(option) are at the end of this file. Option A is the current design below, split
into its real parts with every screw, bolt, washer, nut, corner plate and stake; option B is the single-effect
tilted wick still of SSK-OPT-001. The calculations (sizing.py), the drawing sheets (sheets.py), the build plan
pictures (build_plan_media.py) and the concept media keep reading PARAMS, derived(), build_components() and
build(), unchanged. The stage 3 rails are PPS since 2026-10-24 (SSK-DEC-001 D-01); bolt lengths per D-02.

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
    lidded distillate manifold into the brine gutter (A1, accepted 2026-10-02);
  * two stop blocks at the low corners hold the stack against sliding down the slope;
  * each condensing plate has a 4 mm downturned lip on its high edge, as tabs on the rib lines (A2 (c));
  * each wick is held by two 5052 aluminium clips (D-08, decided by Amish 2026-10-25), one at the high end and one on the brine tongue, no adhesive;
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
    # SSK-DDR-003 A2 option (c) and the wick clips, decided 2026-10-02 (SSK-DEC-001)
    "lip_h": 4.0,          # downturned lip on each condensing plate's high edge (tabs between the wick strips)
    "lip_w": 7.0,          # lip tab width, centred on each rib line
    "rib_start": 6.0,      # ribs start this far inside the plate's high edge (clear of the lip tabs)
    "clip_t": 0.4,         # wick clip: 5052-H32 aluminium strip thickness (D-08, was 304 stainless)
    "clip_w": 8.0,         # wick clip strip width
    "clip_hi_x": 9.0,      # high-end clip bar runs from 1 to 9 mm inside the plate's high edge
    "clip_ear": 8.0,       # high-end clip ear width (in the dry break beside the strip)
    "clip_flap": 6.0,      # ear flap length over the plate's top face
    "clip_lo_x": (7.0, 15.0),   # low-end clip position, mm past the brine tongue root line
    "clip_flange": 3.0,    # low-end clip flange over the tongue's top face
    "ring_pocket": (5.0, 4.0),  # base ring slot (depth, width) under each lip tab of the bottom plate
}

DENSITY = {  # kg/m3, for the mass cross-check against CAL-001
    "Absorber plate": 2700, "Condenser plates": 2700, "Heat-rejection fins": 2700,
    "Glazing": 217,  # twin-wall sheet: 1.3 kg/m2 over 6 mm
    "Wicks": 200, "Side spacer rails": 1200, "Spacer ribs": 1150,
    "Insulated frame": 330,  # plywood walls (550) and stone wool liner (140), by volume share
    "Base ring": 550, "Glazing trim": 2700, "Glazing tape": 300, "Stack stops": 1350,
    "Outlet brackets": 2700, "Feed closure": 300, "Wick clips": 7900,
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
    if kind in ("bottom", "cond"):                    # downturned lip tabs on the high edge, on the rib lines
        for ry in rib_positions(p):
            parts.append(_box(-h, -h + t, ry - p["lip_w"] / 2, ry + p["lip_w"] / 2, z0 - p["lip_h"], z0 + t))
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


def wick_clips(stage, p=PARAMS):
    """The stage's wick clips: per strip a high-end bar with two ears that hook round the plate's high
    edge, and a low-end clip that straddles the brine tongue and the tail under it. 0.4 mm 5052-H32 aluminium (D-08, decided by Amish 2026-10-25; was 304 stainless)."""
    D = derived(p)
    lvl = p["n_stages"] - stage + 1
    z1 = D["levels"][lvl]
    z0 = z1 - p["wick_t"]
    h, t, ct = D["half"], p["plate_t"], p["clip_t"]
    ptop = z1 + t
    out_hi, out_lo = [], []
    for (a, b), yb in zip(D["strips"], D["yb"]):
        e = p["clip_ear"]
        xi = -h + p["clip_hi_x"]
        out_hi.append(_box(-h + 1.0, xi, a - e - 1.0, b + e + 1.0, z0 - ct, z0))              # bar under the wick
        for y0, y1 in ((a - e - 1.0, a - 1.0), (b + 1.0, b + e + 1.0)):                          # ears
            out_hi.append(_box(-h - ct, -h + 1.0, y0, y1, z0 - ct, z0))                          # out under the edge
            out_hi.append(_box(-h - ct, -h, y0, y1, z0 - ct, ptop + ct))                         # up the edge
            out_hi.append(_box(-h - ct, -h + p["clip_flap"], y0, y1, ptop, ptop + ct))           # flap over the top face
        xa, xb = (D["root"] + p["clip_lo_x"][0], D["root"] + p["clip_lo_x"][1])
        w = p["b_tongue_w"] / 2
        out_lo.append(_box(xa, xb, yb - w - ct, yb + w + ct, z0 - ct, z0))                      # bar under the tail
        fl = p["clip_flange"]
        for sg in (-1, 1):
            y0, y1 = sorted((yb + sg * w, yb + sg * (w + ct)))
            out_lo.append(_box(xa, xb, y0, y1, z0 - ct, ptop + ct))                              # leg up the tongue edge
            f0, f1 = sorted((yb + sg * (w + ct), yb + sg * (w - fl)))
            out_lo.append(_box(xa, xb, f0, f1, ptop, ptop + ct))                                 # flange over the top face
    return _union(out_hi), _union(out_lo)


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
    pd_, pw_ = p["ring_pocket"]                      # slots for the bottom plate's lip tabs
    for ry in rib_positions(p):
        C["ring_high"] = C["ring_high"] - _box(-D["half"] - 1.5, -D["half"] - 1.5 + pw_, ry - p["lip_w"] / 2 - 1.5,
                                               ry + p["lip_w"] / 2 + 1.5, -pd_, 0.1)
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
        rl = 2 * h - 8.0 - p["rib_start"]            # ribs stop 8 mm short of the tongue tips, start clear of the lip tabs
        C[f"ribs_{st}"] = _union([Pos(-h + p["rib_start"] + rl / 2, ry, zb + hgt / 2) * Rot(0, 90, 0) * Cylinder(p["rib_d"] / 2, rl)
                                  for ry in rib_positions(p)])
        C[f"wick_{st}"] = wick(st, p)
        C[f"clips_hi_{st}"], C[f"clips_lo_{st}"] = wick_clips(st, p)

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
    "Wick clips": [f"clips_{e}_{s_}" for s_ in range(1, 5) for e in ("hi", "lo")],
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
    # 3b. lip tabs (A2 (c)) and wick clips (decided 2026-10-02)
    n = p["n_stages"]
    for lvl in range(0, n):
        pl = C["plate_bottom"] if lvl == 0 else C[f"plate_{n - lvl}"]
        tabs = pl & _box(-D["half"] - 1, -D["half"] + 2, -600, 600, D["levels"][lvl] - 5, D["levels"][lvl] - 0.01)
        ok = abs(tabs.bounding_box().size.Z - p["lip_h"]) < 0.05
        rec(f"plate level {lvl}: lip tabs hang {p['lip_h']:.0f} mm below the plate", ok, f"{tabs.bounding_box().size.Z:.1f} mm")
        if lvl > 0:
            st = n - lvl + 1
            dw = _dist(tabs, C[f"wick_{st}"])
            rec(f"plate level {lvl}: lip tabs at least 1.5 mm from its wick (stage {st})", dw >= 1.5, f"{dw:.1f} mm")
            dn = _dist(tabs, C[f"wick_{st - 1}"]) if st > 1 else 99.0
            rec(f"plate level {lvl}: lip tabs clear of the wick tails above", dn >= 1.5, f"{dn:.1f} mm")
        dr = min(_dist(tabs, C[f"ribs_{s_}"]) for s_ in range(1, 5))
        rec(f"plate level {lvl}: lip tabs at least 5 mm from every rib end", dr >= 5.0, f"{dr:.1f} mm")
    d = _dist(C["plate_bottom"], C["ring_high"])
    rec("bottom plate lip tabs sit in the base ring slots, ring top touching the plate", d < 0.05, f"{d:.2f} mm")
    tabs0 = C["plate_bottom"] & _box(-D["half"] - 1, -D["half"] + 2, -600, 600, -5, -0.01)
    dsl = _dist(tabs0, C["ring_high"])
    rec("bottom plate lip tabs clear of the ring slots' walls", dsl >= 0.5, f"{dsl:.1f} mm")
    for st in range(1, n + 1):
        lvl = n - st + 1
        for e in ("hi", "lo"):
            cl = C[f"clips_{e}_{st}"]
            dwk = _dist(cl, C[f"wick_{st}"])
            rec(f"stage {st} {e} wick clips touch their wick", dwk < 0.05, f"{dwk:.2f} mm")
            pl = C["absorber"] if lvl == n else C[f"plate_{n - lvl}"]
            rec(f"stage {st} {e} wick clips grip their plate", _dist(cl, pl) < 0.05, f"{_dist(cl, pl):.2f} mm")
        rec(f"stage {st} high clips at least 1 mm from the high liner and ribs",
            min(_dist(C[f"clips_hi_{st}"], C["liner_high"]), _dist(C[f"clips_hi_{st}"], C[f"ribs_{st}"])) >= 0.9,
            f"{min(_dist(C[f'clips_hi_{st}'], C['liner_high']), _dist(C[f'clips_hi_{st}'], C[f'ribs_{st}'])):.1f} mm")
        dd = min(_dist(C[f"clips_lo_{st}"], C["lid"]), _dist(C[f"clips_lo_{st}"], C["wall_low"]))
        rec(f"stage {st} low clips clear of the lid and the low wall by 10 mm", dd >= 10.0, f"{dd:.1f} mm")
        dq = min(_dist(C[f"clips_lo_{st}"], C[k]) for k in ("dams_1", "dams_2", "dams_3"))
        rec(f"stage {st} low clips clear of the chevron dams", dq >= 5.0, f"{dq:.1f} mm")
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


# ================================================================== kit 1.9 interface (STANDARDS section 24)
# Every option as a list of cad_parts.part() dicts in the world frame (ground at z = 0), detailed to D3:
# every made part its own solid with its holes, every screw, bolt, washer, nut and stake, edges broken on
# sawn and cut parts. Option A is the design above (build_components) split into its real parts; option B
# is the single-effect tilted wick still of SSK-OPT-001. Neither changes a design dimension of option A.
sys.path[:0] = [str(Path(__file__).resolve().parent), str(Path(__file__).resolve().parents[2] / ".kit")]
import cad_parts as cp  # noqa: E402
from cad_parts import part  # noqa: E402
import ssk_parts as sp  # noqa: E402

TITLE = "StillStack"
OPTIONS = {"A": "Four-stage wick still", "B": "Single-effect tilted wick still"}
PRINCIPLES = {
    "A": "Four stacked wick stages under thin plates: the latent heat released when vapour condenses on each "
         "plate evaporates the wick under it, so the sun's heat is used about four times (multi-effect diffusion).",
    "B": "One black wick on an insulated backboard under a glass cover: vapour condenses on the cover and its "
         "latent heat is lost to the sky; distillate runs down the cover into an inner channel (single effect).",
}
CHOSEN = "A"           # current design, carried to the drawing, BOM and build plan; selection proposed, awaiting Amish
OPTION_VIEWS = {"A": {"el": 24, "az": -50, "ground_z": 0}, "B": {"el": 24, "az": -50, "ground_z": 0}}
ALLOWED_CONTACTS = []

# Materials (kit names) and colours per family. PPS is not in cad_parts.MATERIALS: it is drawn as "hdpe_natural"
# in tan, so the fidelity mass of the rails uses 950 rather than 1,350 kg/m3 (CAL-001 carries the real figure).
MAT = dict(ply="plywood", timber="timber", wool="insulated_white", al="aluminium", ss="stainless", pc="polycarbonate",
           sil="epdm", fab="canvas", pp="hdpe_natural", pvc="hdpe_natural", galv="galvanised", glass="glass")
COL = dict(wool="#C9CDD2", absorber="#1B1D20", pps="#C7AF7F", pc_rail="#0F766E", rib="#C65A3E", dam="#D98BA3",
           wick="#E8DFCC", wick_b="#2A2622", tape="#1F2937", trim="#3B424A", trough="#8F98A3", mani="#F2F3F1",
           gutter="#5B6470", foam="#E8E1D0", frame="#E4E2DC")
SCREW = "Stainless wood screw"


def _rec(name, shape, mat, kind="made", bom=None, group="shell", color=None):
    return dict(name=name, shape=shape, mat=mat, kind=kind, bom=bom, group=group, color=color)


def _screw(recs, name, d, L, xyz, direction, bom=13, pan=False, group="fixings"):
    sh = sp.pan_screw(d, L) if pan else sp.wood_screw(d, L)
    recs.append(_rec(f"{name} {d} x {L} ({'pan' if pan else 'countersunk'} head)", sp.place_fastener(sh, xyz, direction),
                     MAT["ss"], "fastener", bom, group))


def _bolts(recs, label, dia, grip, xyz, direction, extra=None, bom=12):
    for n, s in sp.bolt_set(dia, grip, xyz, direction, extra):
        recs.append(_rec(f"{label}: {n}", s, MAT["ss"], "fastener", bom, "stand"))


def _rib(length, d):
    """Silicone cord rib along +X, ends cut square and slightly rounded (not a bare cylinder)."""
    return cp.break_edges(Pos(0, 0, 0) * Rot(0, 90, 0) * Cylinder(d / 2, length), 1.0)


def _trim_pieces(trim, OH):
    """Split the glazing trim frame into its four mitred lengths (cut on the diagonals)."""
    X = OH + 50.0
    wedges = {"high": [(0, 0), (-X, X), (-X, -X)], "low": [(0, 0), (X, -X), (X, X)],
              "right": [(0, 0), (X, X), (-X, X)], "left": [(0, 0), (-X, -X), (X, -X)]}
    bb = trim.bounding_box()
    out = {}
    for k, pts in wedges.items():
        w = Pos(0, 0, bb.min.Z - 5) * extrude(Polygon(*pts, align=None), bb.size.Z + 10)
        out[k] = trim & w
    return out


def _stand_world(p, tilt, recs, tag=""):
    """Stand parts in the world (ground rails, cross rails, posts, gussets, props), with the foot pins, gusset
    screws, corner plates and ground stakes. Returns the dict of drillable stand shapes and the stand geometry."""
    S = stand(p, tilt)
    G = stand_geometry(p, tilt)
    OH, P_ = derived(p)["OH"], p["post"]
    px, pz = G["pivot"]
    x_rear, x_front = px - p["rail_rear"], px + P_ / 2 + P_
    W = {}
    for key, label in (("ground_rails", "Ground rail"), ("cross_rails", "Cross rail"), ("posts", "Post"),
                       ("gussets", "Gusset"), ("props", "Prop")):
        for i, s in enumerate(sp.split(S[key])):
            side = ("rear" if i == 0 else "front") if key == "cross_rails" else ("left" if s.center().Y < 0 else "right")
            W[f"{label}, {side}"] = s
    # ground stakes through 12 mm holes, one near each end of each rail
    stakes = []
    for sg in (-1, 1):
        yc = sg * (OH + P_ / 2)
        for xs in (x_rear + 70.0, px - 60.0):
            W[f"Ground rail, {'left' if sg < 0 else 'right'}"] -= Pos(xs, yc, P_ / 2) * Cylinder(6.0, P_ + 2)
            stakes.append(Pos(xs, yc, P_ + 5.0) * sp.stake(10.0, 305.0))
    for i, s in enumerate(stakes):
        recs.append(_rec(f"Ground stake {i + 1} (10 mm, 300 mm)", s, MAT["galv"], "bought", 12, "stand"))
    # corner plates over the cross rail ends, two screws each
    for xc in (x_rear + P_ / 2, x_front - P_ / 2):
        for sg in (-1, 1):
            yc = sg * (OH - 5.0)
            plate_ = Pos(xc, yc, P_) * cp.sheet(40.0, 100.0, 2.0, holes=[(0, -sg * 30.0, 4.5), (0, sg * 30.0, 4.5)])
            for dy in (-30.0, 30.0):
                sc = sp.place_fastener(sp.wood_screw(4, 25), (xc, yc + dy, P_ + 2.0), "-z")
                recs.append(_rec(f"{SCREW} 4 x 25 (countersunk head), corner plate", sc, MAT["ss"], "fastener", 13, "stand"))
                sp.drill_all(W, sc)
                plate_ = plate_ - sc                    # countersunk holes
            recs.append(_rec(f"Corner plate {'rear' if xc < px else 'front'} {'left' if sg < 0 else 'right'}", plate_,
                             MAT["galv"], "bought", 12, "stand"))
    # gusset screws: eight 4 x 40 through each gusset into the post and the rail
    xa = px + P_ / 2
    for sg in (-1, 1):
        for dx, z in ((-60, 22), (-95, 22), (-130, 22), (-160, 14), (-22, 70), (-22, 105), (-22, 140), (-12, 160)):
            y0 = sg * (OH - 12.0)
            sc = sp.place_fastener(sp.wood_screw(4, 40), (xa + dx, y0, z), "+y" if sg > 0 else "-y")
            recs.append(_rec(f"{SCREW} 4 x 40 (countersunk head), gusset", sc, MAT["ss"], "fastener", 13, "stand"))
            sp.drill_all(W, sc)
    # the 10 and 15 deg holes lie under the gussets, so they go through the gusset as well (SSK-DEC-001 D-02)
    for hx_ in G["holes"].values():
        for sg in (-1, 1):
            k = f"Gusset, {'left' if sg < 0 else 'right'}"
            W[k] = W[k] - Pos(hx_, sg * (OH - 6.0), P_ / 2) * Rot(90, 0, 0) * Cylinder(5.25, 14.0)
    # foot pins: M10 x 120 bolt, washers and nut (wing nut drawn as a hex nut) through the prop and the rail hole;
    # 120 mm so the same pin also takes the gusset at the 10 and 15 deg holes (grip 102 mm; SSK-DEC-001 D-02)
    fx, fz = G["foot"]
    for sg in (-1, 1):
        face = sg * (OH + 2 * P_)
        for n, s in sp.bolt_set(10, 2 * P_, (fx, face, fz), "-y" if sg > 0 else "+y", extra=17.6):
            recs.append(_rec(f"Prop foot pin{tag}: {n}", s, MAT["ss"], "fastener", 12, "stand"))
            sp.drill_all(W, s)
    return W, G


def _panel_stand_fixings(p, L, recs_local, side_keys):
    """Pivot and prop hinge bolts and the prop blocks with their screws, built in the panel frame and cut into the
    panel parts L (local shapes)."""
    D = derived(p)
    OH, P_ = D["OH"], p["post"]
    for sg in (-1, 1):
        s_ = "left" if sg < 0 else "right"
        y0, y1 = sorted((sg * OH, sg * (OH + P_)))
        hx = p["prop_hinge"][0]
        blk = cp.break_edges(_box(hx - 60, hx + 60, y0, y1, D["FZ0"], D["FZ0"] + P_), 2.0)
        L[f"Prop block, {s_}"] = blk
        inward = "-y" if sg > 0 else "+y"
        # pivot: M10 through post and side wall, washer and nut inside the wall in a pocket cut in the liner
        for n, s in sp.bolt_set(10, P_ + p["ply_t"], (p["pivot"][0], sg * (OH + P_), p["pivot"][1]), inward, extra=4.0):
            recs_local.append(_rec(f"Pivot bolt, {s_}: {n}", s, MAT["ss"], "fastener", 12, "stand"))
            sp.drill_all(L, s, side_keys)
        for n, s in sp.bolt_set(10, 2 * P_ + p["ply_t"], (hx, sg * (OH + 2 * P_), p["prop_hinge"][1]), inward):
            recs_local.append(_rec(f"Prop hinge bolt, {s_}: {n}", s, MAT["ss"], "fastener", 12, "stand"))
            sp.drill_all(L, s, side_keys + [f"Prop block, {s_}"])
        # four 4 x 40 screws from inside the side wall into the prop block
        for dx in (-30.0, 30.0):
            for z in (2.0, 24.0):
                sc = sp.place_fastener(sp.wood_screw(4, 40), (hx + dx, sg * (OH - p["ply_t"]), z), "+y" if sg > 0 else "-y")
                recs_local.append(_rec(f"{SCREW} 4 x 40 (countersunk head), prop block", sc, MAT["ss"], "fastener", 13, "stand"))
                sp.drill_all(L, sc, side_keys + [f"Prop block, {s_}"])


def _to_world(recs, p, tilt):
    for r in recs:
        r["shape"] = place(r["shape"], p, tilt)
    return recs


def _cut_world(recs_cutters, W):
    for r in recs_cutters:
        if r["kind"] == "fastener":
            sp.drill_all(W, r["shape"])


def _finish(recs, explode=None):
    out = []
    for r in recs:
        out.append(part(r["name"], r["shape"], r["mat"], kind=r["kind"], bom=r["bom"], group=r["group"],
                        color=r["color"]))
    return out


def option_a(p=PARAMS, tilt=None):
    """Option A (the current design) at D3: build_components() split into its real parts, with fasteners."""
    tilt = p["tilt"] if tilt is None else tilt
    D = derived(p)
    OH, WT, n = D["OH"], p["ply_t"], p["n_stages"]
    C = build_components(p, local_only=True)
    L, meta = {}, {}

    def add(name, shape, mat, bom, group="shell", color=None, kind="made", edge=None):
        if edge:
            shape = cp.break_edges(shape, edge)
        L[name] = shape
        meta[name] = (mat, kind, bom, group, color)

    for k, nm in (("ring_side_r", "Base ring, side strip right"), ("ring_side_l", "Base ring, side strip left"),
                  ("ring_high", "Base ring, high strip"), ("ring_low", "Base ring, low strip")):
        add(nm, C[k], MAT["ply"], 2, edge=1.0 if k != "ring_high" else None)
    for k, nm in (("wall_side_r", "Side wall, right"), ("wall_side_l", "Side wall, left"), ("wall_high", "High wall"),
                  ("wall_low", "Low wall comb"), ("wall_low_cap", "Low wall cap")):
        add(nm, C[k], MAT["ply"], 2, color=COL["frame"], edge=1.0 if k in ("wall_side_r", "wall_side_l", "wall_low_cap") else None)
    for k, nm in (("liner_side_r", "Liner, side right"), ("liner_side_l", "Liner, side left"), ("liner_high", "Liner, high"),
                  ("liner_low_cap", "Liner, low cap")):
        add(nm, C[k], MAT["wool"], 2, color=COL["wool"], edge=0.5 if k != "liner_high" else None)
    # low liner: the tongue notches cut it into separate pieces between the stop blocks (rebuilt here as boxes,
    # the same cuts as build_components)
    yst = D["half"] - p["rail_w"] - 1.0
    cuts = sorted([(y - 20.0, y + 20.0) for y in D["yd"]] + [(y - 30.0, y + 30.0) for y in D["yb"]])
    edges, y0 = [], -yst
    for c0, c1 in cuts:
        if c0 > y0:
            edges.append((y0, min(c0, yst)))
        y0 = max(y0, c1)
    if y0 < yst:
        edges.append((y0, yst))
    for i, (ya, yb_) in enumerate(e for e in edges if e[1] - e[0] > 1.0):
        add(f"Liner, low piece {i + 1}", cp.break_edges(_box(p["aperture"] / 2, OH - WT, ya, yb_, 0, D["open_top"]), 0.5),
            MAT["wool"], 2, color=COL["wool"])
    for i, s in enumerate(sp.split(C["stops"])):
        add(f"Stop block {'left' if s.center().Y < 0 else 'right'}", cp.break_edges(s, 0.5), MAT["pp"], 6, "internal", COL["pps"])
    add("Bottom plate", C["plate_bottom"], MAT["al"], 5, "internal")
    for k in range(1, n):
        add(f"Condenser plate {k}", C[f"plate_{k}"], MAT["al"], 5, "internal")
        for i, s in enumerate(sp.split(C[f"dams_{k}"])):
            add(f"Chevron dam, plate {k}, {i + 1}", s, MAT["sil"], 13, "internal", COL["dam"])
    add("Absorber plate", C["absorber"], MAT["al"], 3, "internal", COL["absorber"])
    h = D["half"]
    for st in range(1, n + 1):
        pps = st <= 3                          # SSK-DEC-001 D-01: PPS in stages 1 to 3, printed PC in stage 4
        for s in sp.split(C[f"rails_{st}"]):
            add(f"Side rail, stage {st}, {'left' if s.center().Y < 0 else 'right'} ({'PPS' if pps else 'printed PC'})",
                cp.break_edges(s, 0.5), MAT["pp"], 6, "internal", COL["pps"] if pps else COL["pc_rail"])
        lvl = n - st + 1
        zb = D["levels"][lvl - 1] + p["plate_t"]
        rl = 2 * h - 8.0 - p["rib_start"]
        for j, ry in enumerate(rib_positions(p)):
            rib = Pos(-h + p["rib_start"] + rl / 2, ry, zb + (p["gap"] + p["wick_t"]) / 2) * _rib(rl, p["rib_d"])
            add(f"Spacer rib, stage {st}, {j + 1}", rib, MAT["sil"], 7, "internal", COL["rib"])
        for i, s in enumerate(sp.split(C[f"wick_{st}"])):
            add(f"Wick strip, stage {st}, {i + 1}", s, MAT["fab"], 4, "internal", COL["wick"])
        for e, lab in (("hi", "high-end"), ("lo", "brine-tongue")):
            for i, s in enumerate(sp.split(C[f"clips_{e}_{st}"])):
                add(f"Wick clip, {lab}, stage {st}, {i + 1}", s, MAT["al"], 18, "internal")
    for i, s in enumerate(sp.split(C["fins"])):
        add(f"Heat-rejection fin {i + 1} (painted black, D-07)", s, MAT["al"], 11, "internal", COL["absorber"])
    add("Glazing tape", C["tape"], MAT["sil"], 15, color=COL["tape"])
    add("Glazing, twin-wall polycarbonate", Pos(0, 0, D["glaz_z"]) * sp.twin_wall(p["glaz_size"], p["glaz_size"], p["glaz_t"]),
        MAT["pc"], 1)
    for k, s in _trim_pieces(C["trim"], OH).items():
        add(f"Glazing trim, {k} length", s, MAT["al"], 15, color=COL["trim"])
    add("Feed trough", C["trough"], MAT["pvc"], 8, color=COL["trough"])
    add("Feed closure", cp.break_edges(C["closure"], 0.5), MAT["sil"], 17, color=COL["foam"])
    for s in sp.split(C["trough_brackets"]):
        add(f"Trough bracket, {'left' if s.center().Y < 0 else 'right'}", s, MAT["galv"], 8)
    add("Distillate manifold", C["manifold"], MAT["pp"], 9, color=COL["mani"])
    add("Distillate manifold lid", C["lid"], MAT["pp"], 9, color=COL["mani"])
    add("Brine gutter", C["gutter"], MAT["pvc"], 10, color=COL["gutter"])
    for s in sp.split(C["outlet_brackets"]):
        add(f"Outlet bracket, {'left' if s.center().Y < 0 else 'right'}", s, MAT["al"], 16)

    # ---- fasteners in the panel frame, each cut into the parts it passes through
    F = []
    wt, gz = D["wall_top"], D["glaz_z"]
    frame_keys = [k for k in L if k.startswith(("Base ring", "Side wall", "High wall", "Low wall", "Liner", "Prop block"))]
    for sg in (-1, 1):                                   # corners: three screws per corner through the side wall
        y = sg * OH
        d_in = "-y" if sg > 0 else "+y"
        for z in (10.0, 26.0, 42.0):
            _screw(F, f"{SCREW}, corner", 4, 40, (-OH + WT / 2, y, z), d_in)
        for z in (10.0, 26.0):
            _screw(F, f"{SCREW}, corner", 4, 40, (OH - WT / 2, y, z), d_in)
        _screw(F, f"{SCREW}, low wall cap", 4, 30, (OH - WT / 2, y, 42.0), d_in)
        for x in (-450.0, -300.0, -150.0, 0.0, 150.0, 300.0, 450.0):    # base ring up into the side walls
            _screw(F, f"{SCREW}, base ring", 4, 40, (x, sg * (OH - WT / 2), D["FZ0"]), "+z")
    for ry in rib_positions(p):                          # base ring up into the high wall, between the openings
        _screw(F, f"{SCREW}, base ring", 4, 40, (-OH + WT / 2, ry, D["FZ0"]), "+z")
    for y in (-300.0, 0.0, 300.0):                       # low wall sill into the low base ring strip
        _screw(F, f"{SCREW}, base ring", 4, 40, (OH, y, D["FZ0"] / 2), "-x")
    tt = p["trim"][2]
    zt = gz - 8.0
    for u in (-400.0, -200.0, 0.0, 200.0, 400.0):        # trim: pan head screws through the hanging leg
        _screw(F, "Stainless screw, glazing trim", 4, 20, (u, OH + tt, zt), "-y", pan=True)
        _screw(F, "Stainless screw, glazing trim", 4, 20, (u, -OH - tt, zt), "+y", pan=True)
        _screw(F, "Stainless screw, glazing trim", 4, 20, (OH + tt, u, zt), "-x", pan=True)
        _screw(F, "Stainless screw, glazing trim", 4, 20, (-OH - tt, u, zt), "+x", pan=True)
    bw, bt = p["bracket"]
    for sg in (-1, 1):                                   # outlet brackets: three screws into a tooth and the sill
        for z in (25.0, 10.0, -6.0):
            _screw(F, f"{SCREW}, outlet bracket", 4, 25, (OH + bt, sg * p["bracket_y"], z), "-x")
        y0 = sg * (p["aperture"] / 2 - 7)                # trough brackets: two screws into the high wall's solid ends
        for z in (18.0, 6.0):
            _screw(F, f"{SCREW}, trough bracket", 4, 25, (-OH - 3.0, y0, z), "+x")
    all_keys = list(L)
    for r in F:
        sp.drill_all(L, r["shape"], all_keys)
    side_keys = [k for k in L if k.startswith(("Side wall", "Liner, side", "Base ring, side"))]
    _panel_stand_fixings(p, L, F, side_keys)
    for k in L:
        if k.startswith("Prop block"):
            meta[k] = (MAT["timber"], "made", 12, "stand", None)

    recs = [_rec(k, v, *meta[k]) for k, v in L.items()] + F
    _to_world(recs, p, tilt)
    recs_w = []
    W, G = _stand_world(p, tilt, recs_w)
    _cut_world([r for r in recs if "bolt" in r["name"]], W)
    for k, s in W.items():
        recs_w.append(_rec(k, s, MAT["ply"] if k.startswith("Gusset") else MAT["timber"], "made", 2 if k.startswith("Gusset") else 12, "stand"))
    return _finish(recs + recs_w)


# ---- option B: single-effect tilted wick still on the same frame size, trough, gutter and stand
B_PARAMS = {
    "base_t": 12.0,        # plywood base panel
    "board_t": 25.0,       # stone wool backboard
    "tray_t": 0.5,         # black aluminium tray under the wick
    "wick_t": 1.0,
    "cover_gap": 60.0,     # wick face to glass underside
    "glass_t": 4.0,        # toughened float glass cover
    "channel": (40.0, 28.0, 1.5),   # distillate channel (PP): width, depth, wall
    "channel_x": 452.0,    # inboard edge of the channel (local x)
    "gutter_z": 18.0,      # top of the outside brine gutter
}


def option_b(p=PARAMS, tilt=None):
    """Option B at D3: one black wick on an insulated backboard under a glass cover, inner distillate channel."""
    tilt = p["tilt"] if tilt is None else tilt
    b = B_PARAMS
    D = derived(p)
    OH, WT, FT = D["OH"], p["ply_t"], p["foam_t"]
    li = p["aperture"] / 2                              # 500: inside of the liners
    z_board = b["board_t"]
    z_tray = z_board + b["tray_t"]
    z_wick = z_tray + b["wick_t"]
    g0 = z_wick + b["cover_gap"]                        # glass underside
    wt = g0 - p["tape_t"]
    L, meta = {}, {}

    def add(name, shape, mat, bom=None, group="shell", color=None, kind="made", edge=None):
        if edge:
            shape = cp.break_edges(shape, edge)
        L[name] = shape
        meta[name] = (mat, kind, bom, group, color)

    add("Base panel", _box(-OH, OH, -OH, OH, -b["base_t"], 0), MAT["ply"], edge=1.0)
    add("Side wall, right", _box(-OH, OH, OH - WT, OH, 0, wt), MAT["ply"], color=COL["frame"], edge=1.0)
    add("Side wall, left", _box(-OH, OH, -OH, -OH + WT, 0, wt), MAT["ply"], color=COL["frame"], edge=1.0)
    slot = lambda x0, x1: _box(x0, x1, -li + 10, li - 10, z_tray - 0.5, z_wick + 1.5)
    add("High wall", _box(-OH, -OH + WT, -OH + WT, OH - WT, 0, wt) - slot(-OH - 1, -OH + WT + 1), MAT["ply"], color=COL["frame"])
    add("Low wall", _box(OH - WT, OH, -OH + WT, OH - WT, 0, wt) - slot(OH - WT - 1, OH + 1), MAT["ply"], color=COL["frame"])
    add("Backboard, stone wool", _box(-OH + WT, OH - WT, -OH + WT, OH - WT, 0, z_board), MAT["wool"], color=COL["wool"], edge=0.5)
    add("Liner, side right", _box(-li - FT, li + FT, li, li + FT, z_board, wt), MAT["wool"], color=COL["wool"], edge=0.5)
    add("Liner, side left", _box(-li - FT, li + FT, -li - FT, -li, z_board, wt), MAT["wool"], color=COL["wool"], edge=0.5)
    add("Liner, high", _box(-li - FT, -li, -li, li, z_board, wt) - slot(-li - FT - 1, -li + 1), MAT["wool"], color=COL["wool"])
    add("Liner, low", _box(li, li + FT, -li, li, z_board, wt) - slot(li - 1, li + FT + 1), MAT["wool"], color=COL["wool"])
    add("Absorber tray, black", Pos(0, 0, z_board) * cp.sheet(2 * li - 4, 2 * li - 4, b["tray_t"], r_corner=5.0),
        MAT["al"], group="internal", color=COL["absorber"])
    # wick: one black sheet on the tray, out through the high wall slot to the trough and through the low wall slot
    xi, tw_, rim = p["trough"]
    yw = li - 20.0
    wick = _box(-li + 3, li - 3, -yw, yw, z_tray, z_wick)
    wick += _box(-OH - 1.0, -li + 3, -yw, yw, z_tray, z_wick)                       # out through the high wall slot
    wick += _box(-OH - 1.0, -OH, -yw, yw, z_tray, rim + 1.0)                         # up the outside of the wall
    wick += _box(-xi - 8.0, -OH, -yw, yw, rim, rim + 1.0)                            # over the trough rim
    wick += _box(-xi - 8.0, -xi - 7.0, -yw, yw, -20.0, rim)                          # down into the feed
    xg0 = OH + 12.0
    wick += _box(li - 3, xg0 + 30.0, -yw, yw, z_tray, z_wick)                      # out to the brine gutter
    wick += _box(xg0 + 29.0, xg0 + 30.0, -yw, yw, b["gutter_z"] - 25.0, z_tray)   # down into the gutter
    add("Wick, black cotton-viscose", wick, MAT["fab"], group="internal", color=COL["wick_b"])
    clip = _box(-li + 3, -li + 13, -yw - 2, yw + 2, z_wick, z_wick + 0.6)
    add("Wick clamp bar, high end (stainless)", cp.break_edges(clip, 0.2), MAT["ss"], group="internal")
    # glass, tape, trim
    gs = p["glaz_size"] / 2
    add("Glazing tape", _box(-gs, gs, -gs, gs, wt, g0) - _box(-li, li, -li, li, wt - 1, g0 + 1), MAT["sil"], color=COL["tape"])
    add("Cover, 4 mm toughened glass", Pos(0, 0, g0) * cp.sheet(2 * gs, 2 * gs, b["glass_t"], r_corner=4.0, edge=0.8), MAT["glass"])
    tl, td, tt = p["trim"]
    gt = g0 + b["glass_t"]
    xo = OH + tt
    ring = _box(-xo, xo, -xo, xo, gt, gt + tt) - _box(-xo + tl, xo - tl, -xo + tl, xo - tl, gt - 1, gt + tt + 1)
    skirt = _box(-xo, xo, -xo, xo, gt + tt - td, gt + tt) - _box(-OH, OH, -OH, OH, gt - td - 1, gt + tt + 1)
    for k, s in _trim_pieces(ring + skirt, OH).items():
        add(f"Glazing trim, {k} length", s, MAT["al"], color=COL["trim"])
    # distillate: silicone drip strip under the glass, PP channel with end caps, outlet tube through the right wall
    cw, cd, ct = b["channel"]
    cx = b["channel_x"]
    add("Drip strip, silicone", cp.break_edges(_box(cx + 12, cx + 18, -li + 2, li - 2, g0 - 6.0, g0), 0.8), MAT["sil"],
        group="internal", color=COL["dam"])
    zc1 = g0 - 8.0
    ch = Pos(cx + cw / 2, 0, zc1 - cd) * Rot(90, 0, 0) * Pos(0, 0, -(2 * li - 10) / 2) * cp.bent_channel_sheet(cw, cd, ct, 2 * li - 10)
    yo = li - 5.0
    tube_z = zc1 - cd + 8.0
    add("Distillate channel, PP", ch, MAT["pp"], group="internal", color=COL["mani"])
    for sg in (-1, 1):
        cap = _box(cx - 1, cx + cw + 1, *sorted((sg * yo, sg * (yo + 3))), zc1 - cd - 1, zc1)
        if sg > 0:
            cap -= Pos(cx + cw / 2, yo, tube_z) * Rot(-90, 0, 0) * Cylinder(6.0, 10)
        add(f"Channel end cap, {'left' if sg < 0 else 'right'}", cp.break_edges(cap, 0.4), MAT["pp"], group="internal", color=COL["mani"])
    tube = Pos(cx + cw / 2, yo - 6.0, tube_z) * Rot(-90, 0, 0) * cp.round_tube(12.0, 1.5, OH + 50.0 - (yo - 6.0))
    add("Distillate outlet tube, silicone", tube, MAT["sil"], group="internal", color=COL["mani"])
    bore = Pos(cx + cw / 2, li - 1.0, tube_z) * Rot(-90, 0, 0) * Pos(0, 0, 25.0) * Cylinder(6.0, 50.0)
    for k in ("Liner, side right", "Side wall, right"):
        L[k] = L[k] - bore
    # outside: brine gutter on two brackets, feed trough on two brackets, foam closure
    gw, gh = 70.0, 40.0
    gz1 = b["gutter_z"]
    gut = _box(xg0, xg0 + gw, -li, li, gz1 - gh, gz1) - _box(xg0 + 3, xg0 + gw - 3, -li + 3, li - 3, gz1 - gh + 3, gz1 + 1)
    gut += Pos(xg0 + gw / 2, -li + 30, gz1 - gh - 30) * Cylinder(8, 60)
    add("Brine gutter", gut, MAT["pvc"], color=COL["gutter"])
    bw, bt = p["bracket"]
    for sg in (-1, 1):
        y0 = sg * p["bracket_y"]
        br = _box(OH, OH + bt, y0 - bw / 2, y0 + bw / 2, gz1 - gh - bt, gz1 - 2.0)
        br += _box(OH, xg0 + gw + 6, y0 - bw / 2, y0 + bw / 2, gz1 - gh - bt, gz1 - gh)
        add(f"Gutter bracket, {'left' if sg < 0 else 'right'}", cp.break_edges(br, 0.5), MAT["al"])
    tz0 = rim - tw_
    tr = _box(-xi - tw_, -xi, -li, li, tz0, rim) - _box(-xi - tw_ + 5, -xi - 5, -li + 5, li - 5, tz0 + 5, rim + 1)
    add("Feed trough", tr, MAT["pvc"], color=COL["trough"])
    add("Feed closure", cp.break_edges(_box(-xi, -OH - 1.0, -yw - 2, yw + 2, z_wick, rim), 0.5), MAT["sil"], color=COL["foam"])
    for sg in (-1, 1):
        y0 = sg * (li - 7)
        br = _box(-OH - 3, -OH, y0 - 10, y0 + 10, tz0 - 3, z_tray - 1.0)
        br += _box(-xi - tw_ - 3, -OH, y0 - 10, y0 + 10, tz0 - 3, tz0)
        br += _box(-xi - tw_ - 3, -xi - tw_, y0 - 10, y0 + 10, tz0 - 3, tz0 + 30)
        add(f"Trough bracket, {'left' if sg < 0 else 'right'}", br, MAT["galv"])

    # ---- fasteners
    F = []
    for sg in (-1, 1):
        d_in = "-y" if sg > 0 else "+y"
        for xw in (-OH + WT / 2, OH - WT / 2):
            for z in (12.0, 40.0, wt - 12.0):
                _screw(F, f"{SCREW}, corner", 4, 40, (xw, sg * OH, z), d_in)
        for x in (-450.0, -225.0, 0.0, 225.0, 450.0):
            _screw(F, f"{SCREW}, base panel", 4, 40, (x, sg * (OH - WT / 2), -b["base_t"]), "+z")
            _screw(F, f"{SCREW}, base panel", 4, 40, (sg * (OH - WT / 2), x * 0.9, -b["base_t"]), "+z")
    zt = g0 - 6.0
    for u in (-400.0, 0.0, 400.0):
        _screw(F, "Stainless screw, glazing trim", 4, 20, (u, OH + tt, zt), "-y", pan=True)
        _screw(F, "Stainless screw, glazing trim", 4, 20, (u, -OH - tt, zt), "+y", pan=True)
        _screw(F, "Stainless screw, glazing trim", 4, 20, (OH + tt, u, zt), "-x", pan=True)
        _screw(F, "Stainless screw, glazing trim", 4, 20, (-OH - tt, u, zt), "+x", pan=True)
    for sg in (-1, 1):
        for z in (8.0, -6.0):
            _screw(F, f"{SCREW}, gutter bracket", 4, 25, (OH + bt, sg * p["bracket_y"], z), "-x")
        for z in (14.0, 4.0):
            _screw(F, f"{SCREW}, trough bracket", 4, 25, (-OH - 3.0, sg * (li - 7), z), "+x")
    keys = list(L)
    for r in F:
        sp.drill_all(L, r["shape"], keys)
    side_keys = [k for k in L if k.startswith(("Side wall", "Liner, side", "Backboard", "Base panel"))]
    _panel_stand_fixings(p, L, F, side_keys)
    for k in L:
        if k not in meta:
            meta[k] = (MAT["timber"], "made", None, "stand", None)
    recs = [_rec(k, v, *meta[k]) for k, v in L.items()] + F
    _to_world(recs, p, tilt)
    recs_w = []
    W, G = _stand_world(p, tilt, recs_w, " (B)")
    _cut_world([r for r in recs if "bolt" in r["name"]], W)
    for k, s in W.items():
        recs_w.append(_rec(k, s, MAT["ply"] if k.startswith("Gusset") else MAT["timber"], "made", None, "stand"))
    out = _finish(recs + recs_w)
    for q in out:                                   # option B is not carried to the BOM
        q["bom"] = None
    return out


def components(option=None):
    """kit 1.9: the parts of one option as cad_parts.part() dicts in the world frame (ground at z = 0)."""
    option = option or CHOSEN
    if option == "A":
        return option_a()
    if option == "B":
        return option_b()
    raise KeyError(option)


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    parts = build()
    asm = assembly(parts)
    (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
    export_step(asm, str(root / "step" / "stillstack-assembly.step"))
    export_stl(asm, str(root / "stl" / "stillstack-assembly.stl"), tolerance=0.15, angular_tolerance=0.2)
    rail = cp.break_edges(Box(PARAMS["aperture"] - 2 * PARAMS["plate_clear"], PARAMS["rail_w"], PARAMS["gap"] + PARAMS["wick_t"]), 0.5)
    export_stl(rail, str(root / "stl" / "side-rail.stl"), tolerance=0.1, angular_tolerance=0.2)   # stage 4 printed rail
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
