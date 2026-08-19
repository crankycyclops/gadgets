"""Assembled preview of the whole SUTEFOTO T15 barn-door kit.

Builds the collar and all four leaves and poses the leaves on their own hinge
axes, so you can see how the parts actually sit together rather than reasoning
about five separate STLs.

Edit OPEN_ANGLE below to choose how far the leaves are swung open; there are
commented-out settings there for fully open, fully closed and per-leaf posing.

The sign convention matches validate_assembly, so an angle means the same thing
in both places:

    0   fully closed -- all four leaves stacked flat over the diffuser
    90  fully open

Run it in CQ-Editor for a coloured preview, or from the command line to write
exports/assembly.step and exports/assembly.stl.

    python assembly.py

The hardware is not modelled; see the README for the M3 stack.
"""
from pathlib import Path

import cadquery as cq

import frame
import top_door, bottom_door, left_door, right_door
from common import hinge_axis

# How far the leaves are swung open, in degrees: 0 is fully closed and stacked
# flat over the diffuser, 90 is fully open.  Change this and re-run.
OPEN_ANGLE = 130

# OPEN_ANGLE = 90.0    # fully open
# OPEN_ANGLE = 0.0     # fully closed, stacked over the diffuser
# OPEN_ANGLE = 75.0    # roughly how far you would actually run them in use
#
# A dict poses each leaf independently, which is the quickest way to check one
# leaf's travel against its neighbours.  Any leaf left out sits closed.
# OPEN_ANGLE = {"top": 90, "bottom": 90, "left": 30, "right": 30}

DOORS = {
    "top": top_door,
    "bottom": bottom_door,
    "left": left_door,
    "right": right_door,
}

# Which way each leaf swings away from the diffuser.  Same table as
# validate_assembly's `directions`.
OPEN_DIRECTION = {"top": 1, "bottom": -1, "left": 1, "right": -1}

# 0-255, the form CQ-Editor's show_object options take.
COLORS = {
    "frame": (188, 190, 196),
    "top": (226, 118, 84),
    "bottom": (86, 162, 226),
    "left": (122, 194, 116),
    "right": (222, 186, 86),
}


def _angle_for(side, angle):
    """`angle` is either one number for every leaf or a dict keyed by side.

    None means "whatever OPEN_ANGLE says right now", read at call time rather
    than baked into the defaults, so editing the variable above -- or setting
    assembly.OPEN_ANGLE from another module -- always takes effect.
    """
    if angle is None:
        angle = OPEN_ANGLE
    if isinstance(angle, dict):
        return float(angle.get(side, 0.0))
    return float(angle)


def _pose(part, side, angle):
    """Swing one leaf about its own hinge axis."""
    x, y, z = hinge_axis(side)
    end = (x + 1, y, z) if side in ("top", "bottom") else (x, y + 1, z)
    return part.rotate((x, y, z), end, OPEN_DIRECTION[side] * angle)


def parts(angle=None):
    """[(name, solid, colour)] for the collar and all four posed leaves."""
    out = [("frame", frame.build(), COLORS["frame"])]
    for side, module in DOORS.items():
        posed = _pose(module.build(), side, _angle_for(side, angle))
        out.append(("%s_door" % side, posed, COLORS[side]))
    return out


def build(angle=None):
    """A cq.Assembly of the kit with the leaves opened `angle` degrees.

    Pass a dict keyed by side -- {"top": 90, "left": 0, ...} -- to pose the
    leaves independently, which is the quickest way to check one leaf's travel
    against its neighbours.
    """
    assy = cq.Assembly(name="sutefoto_t15_barn_doors")
    for name, part, (r, g, b) in parts(angle):
        assy.add(part, name=name, color=cq.Color(r / 255.0, g / 255.0, b / 255.0))
    return assy


def preview(angle=None):
    """Push each part into CQ-Editor separately so they stay individually
    selectable and can be toggled in the object tree."""
    for name, part, color in parts(angle):
        show_object(part, name=name, options={"color": color})


def export(angle=None):
    """Write the posed assembly to exports/, STEP keeping the parts and their
    colours separate and STL fused for a quick look in a slicer or mesh viewer."""
    out = Path(__file__).with_name("exports")
    out.mkdir(exist_ok=True)
    step = out / "assembly.step"
    stl = out / "assembly.stl"
    assy = build(angle)
    assy.export(str(step))
    cq.exporters.export(assy.toCompound(), str(stl))
    print("%s\n%s" % (step, stl))


# Preview in CQ-Editor, export otherwise.  The bare name lookup below decides
# which, and it runs before anything is built, so importing this module for
# assembly.build() stays free.
try:
    show_object
except NameError:
    if __name__ == "__main__":
        export()
else:
    preview()
