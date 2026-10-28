"""StillStack product appearance model for photoreal renders (kit 1.9), TRL 3, constructable design.

Every part of the chosen design comes from cad/src/model.py components(CHOSEN) as it is: the plywood box on its
base ring, stone wool liner, twin-wall glazing under the mitred trim, black absorber, four wick stages with their
PPS and polycarbonate rails, silicone ribs, wick clips and chevron dams, the coated condenser plates with their
tongues, the fins, feed trough, lidded distillate manifold and brine gutter on their brackets, the stand with its
bolts, gussets, corner plates and stakes, and every screw. Only the scene is added as context parts: a sandy
coastal yard, a feed bucket on a concrete block, a distillate jar on a block under the manifold outlet, and a
1.75 m mannequin standing on the ground beside the panel. Ground level is z = 0; every site part reaches below it.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Groups: "shell" (frame, glazing, trim, trough, manifold, gutter, brackets, fixings), "internal" (the stack seen
through the glazing), "stand" (timber stand and its hardware) and "context" (site, bucket, jar, mannequin).

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Compound, Cylinder, Pos  # noqa: E402
import cad_parts as cp  # noqa: E402
from cad_parts import part  # noqa: E402
from ssk_parts import box  # noqa: E402
import model  # noqa: E402

TITLE = "StillStack: four-stage solar wick still"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "stand", "context"], "explode": False, "el": 22, "az": -40,
     "args": ["--scene=outdoor", "--ground=sand", "--ground-z=0", "--sun=48,-70", "--lens=40"],
     "note": "Site render from the front right (low, collection edge) and above, about 22 deg elevation: the panel "
             "on its staked timber stand at 20 deg in a sandy coastal yard, feed bucket by the trough at the high "
             "edge, distillate jar under the manifold outlet, brine gutter outboard; 1.75 m mannequin for scale"},
    {"name": "studio", "groups": ["shell", "internal", "stand"], "explode": False, "el": 26, "az": -50,
     "note": "Studio render from the front right and above, about 26 deg elevation: the whole still on its stand; "
             "through the twin-wall glazing the black absorber, and at the low edge the distillate tongues into the "
             "lidded manifold and the brine tongues over it into the gutter"},
    {"name": "low-edge", "groups": ["shell", "internal", "stand"], "explode": False, "el": 12, "az": -15,
     "note": "Studio render looking up the slope at the low edge, about 12 deg elevation: comb low wall, distillate "
             "manifold on its two outlet brackets, brine gutter outboard and lower, front posts with the pivot bolts"},
]


def _group(p):
    n = p["name"]
    if p["group"] == "stand" or n.startswith(("Ground", "Cross rail", "Post", "Gusset", "Prop", "Corner plate")):
        return "stand"
    if p["group"] == "internal":
        return "internal"
    return "shell"


def scene():
    """Site parts in the world frame (ground at z = 0)."""
    out = []
    bb = Compound([p["shape"] for p in model.components(model.CHOSEN)]).bounding_box()
    out.append(part("Sandy yard (site)", box(bb.min.X - 2500, bb.max.X + 2500, bb.min.Y - 2500, bb.max.Y + 2500, -80, 0),
                    "sand", "context"))
    # feed bucket on a concrete block behind the high edge
    xb, yb = bb.min.X - 260, bb.min.Y + 420
    out.append(part("Concrete block under the feed bucket (site)", cp.break_edges(box(xb - 200, xb + 200, yb - 100, yb + 100, -60, 200), 3.0),
                    "concrete", "context"))
    bucket = Pos(xb, yb, 200) * (cp.break_edges(Pos(0, 0, 180) * Cylinder(150, 360), 4.0) - Pos(0, 0, 200) * Cylinder(142, 340))
    out.append(part("Feed bucket, 20 L", bucket, "pe_tank_white", "context"))
    # distillate jar on a block under the manifold outlet (outlet at +Y end of the manifold, low edge)
    C = model.build_components()
    mo = C["manifold"].bounding_box()
    xj, yj = mo.center().X + 60, mo.max.Y - 30
    out.append(part("Concrete block under the distillate jar (site)", cp.break_edges(box(xj - 200, xj + 200, yj - 100, yj + 100, -60, 140), 3.0),
                    "concrete", "context"))
    jar = Pos(xj, yj, 140) * (cp.break_edges(Pos(0, 0, 130) * Cylinder(90, 260), 6.0) - Pos(0, 0, 140) * Cylinder(85, 260))
    out.append(part("Distillate jar, 5 L glass", jar, "glass", "context"))
    from context_parts import mannequin
    person = Pos(bb.center().X - 250, bb.min.Y - 650, 0) * mannequin(1750.0, "stand")
    out.append(part("Person, 1.75 m mannequin (scale)", person, "skin", "context"))
    return out


def product_parts():
    out = []
    for p in model.components(model.CHOSEN):
        q = dict(p)
        q["group"] = _group(p)
        out.append(q)
    for p in scene():
        q = dict(p)
        q["group"] = "context"
        out.append(q)
    return out


if __name__ == "__main__":
    ps = product_parts()
    for p in ps:
        if p["group"] == "context":
            s = p["shape"]
            b = s.bounding_box()
            print(f"{p['name']:50s} {p['material']:10s} z {b.min.Z:7.0f} to {b.max.Z:7.0f}")
    print(len(ps), "parts")
