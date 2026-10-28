"""StillStack repo-specific CAD helpers (kit 1.9). Built on .kit/cad_parts.py; nothing here belongs in .kit/.

Helpers the parts library does not have (suggested kit additions are listed in docs/REVIEW.md):
    orient(shape, d)                 turn a part built along +Z so +Z points along +x, -x, +y, -y, +z or -z
    wood_screw(d, L)                 countersunk wood screw (ISO 7050 style head), head flush at z = 0, shank down -Z
    pan_screw(d, L)                  pan head screw, head on z = 0 upward, shank down -Z
    place_fastener(shape, xyz, d)    put a fastener built along -Z at xyz with its shank pointing along d
    bolt_set(d, grip, xyz, d, extra) ISO 4017 bolt, two ISO 7089 washers and an ISO 4032 nut, as (name, shape) pairs
    stake(d, L, head)                ground stake (round bar with a forged head), head top at z = 0
    twin_wall(w, L, t, skin, rib, pitch)  twin-wall polycarbonate sheet, flutes along +X
    split(shape)                     the separate solids of a union, in a stable order
    drill_all(parts, cutter, names)  subtract a fastener's own solid from every listed part it passes through
All sizes in millimetres.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Box, Cone, Cylinder, Pos, Rectangle, Rot, Sketch, Solid, extrude  # noqa: E402
import cad_parts as cp  # noqa: E402

ROT_TO = {"+z": (0, 0, 0), "-z": (180, 0, 0), "+x": (0, 90, 0), "-x": (0, -90, 0), "+y": (-90, 0, 0), "-y": (90, 0, 0)}
OPP = {"-z": "+z", "+z": "-z", "+x": "-x", "-x": "+x", "+y": "-y", "-y": "+y"}


def orient(shape, d):
    """Rotate a shape built along +Z so that +Z points along d."""
    return Rot(*ROT_TO[d]) * shape


def wood_screw(d, length):
    """Countersunk wood screw d x length: 90 degree head of diameter 2d flush at z = 0, shank to z = -length."""
    k = d / 2
    head = Pos(0, 0, -k / 2) * Cone(d / 2, d, k)
    shank = Pos(0, 0, -length) * cp.round_bar(d, length - k + 0.01, 0.3 * d)
    return head + shank


def pan_screw(d, length):
    """Pan head screw d x length: head of diameter 2d and height 0.7d above z = 0, shank to z = -length."""
    head = cp.break_edges(Pos(0, 0, 0.35 * d) * Cylinder(d, 0.7 * d), 0.25 * d)
    return head + Pos(0, 0, -length / 2) * Cylinder(d / 2, length)


def place_fastener(shape, xyz, d):
    """Place a fastener built along -Z (head at the origin) at xyz with its shank pointing along d."""
    return Pos(*xyz) * orient(shape, OPP[d])


def bolt_set(dia, grip, xyz, d, extra=None):
    """Bolt, washers and nut for a joint 'grip' thick; xyz is the head-side face, d the direction into the joint."""
    return [(n, Pos(*xyz) * orient(s, OPP[d])) for n, s in cp.hex_bolt_set(dia, grip, extra)]


def stake(d, length, head=20.0):
    """Galvanised ground stake: a forged head 5 mm thick, head top at z = 0, pointed bar to z = -length."""
    h = Pos(0, 0, -2.5) * Cylinder(head / 2, 5.0)
    bar = Pos(0, 0, -(length - 2 * d) / 2 - 5.0) * Cylinder(d / 2, length - 2 * d - 5.0)
    tip = Pos(0, 0, -length + d) * Cone(0.5, d / 2, 2 * d)
    return cp.break_edges(h, 1.0) + bar + tip


def twin_wall(w, length, t=6.0, skin=0.4, rib=0.3, pitch=6.0):
    """Twin-wall polycarbonate sheet w (Y) x length (X) x t (Z, from 0): two skins and ribs at 'pitch',
    flutes running along X."""
    n = int(round(w / pitch))
    sk = Sketch() + Pos(0, t / 2) * Rectangle(w, t)
    p = w / n
    for i in range(n):
        cx = -w / 2 + p * (i + 0.5)
        sk -= Pos(cx, t / 2) * Rectangle(p - rib, t - 2 * skin)
    s = extrude(sk, length)                         # profile in XY (x = across, y = thickness), along +Z
    return Pos(-length / 2, 0, 0) * Rot(0, 90, 0) * Rot(0, 0, 90) * s


def split(shape):
    """Separate solids of a union, ordered by centre (x, then y, then z) so names stay stable. Each is rebuilt as a
    free Solid: a solid taken straight from a compound keeps a link to it, and cad_parts.break_edges() on it would
    fillet the whole compound (build123d topo_parent behaviour)."""
    sols = [Solid(s.wrapped) for s in shape.solids()]
    return sorted(sols, key=lambda s: (round(s.center().X, 1), round(s.center().Y, 1), round(s.center().Z, 1)))


def _bb_overlap(a, b, pad=0.01):
    return not (a.max.X < b.min.X - pad or b.max.X < a.min.X - pad or a.max.Y < b.min.Y - pad or b.max.Y < a.min.Y - pad
                or a.max.Z < b.min.Z - pad or b.max.Z < a.min.Z - pad)


def drill_all(parts, cutter, keys=None):
    """Subtract 'cutter' (a fastener's solid, or its clearance) from every part in the dict 'parts' (name -> shape)
    whose box it touches. keys limits the parts considered."""
    cb = cutter.bounding_box()
    for k in (keys if keys is not None else list(parts)):
        sh = parts.get(k)
        if sh is None:
            continue
        if _bb_overlap(sh.bounding_box(), cb):
            try:
                if (sh & cutter).volume > 1e-3:
                    parts[k] = sh - cutter
            except Exception:
                parts[k] = sh - cutter
    return parts


def box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)
