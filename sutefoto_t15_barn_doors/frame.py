"""SUTEFOTO T15 collar/frame, revision 9.

The collar fit and the hinge axes are unchanged.  What is reworked is how the
hinges are held on.  Revision 8 bridged frame to barrel with a tapered web only
HINGE_CENTER_W wide, rooted 2 mm into the wall; printed with the collar's back
face on the bed the layer planes ran straight through that junction and the
hinges peeled off.  Revision 9 stands a FRAME_HINGE_BEAM_W-wide beam on the
outside of the collar instead, taking the minimum section between barrel and
frame from 4.6-9.5 mm2 to 171 mm2.

The leaves themselves are untouched, so the fold-flat stacking and the
LIGHT_TRAP_OVERLAP skirt behave exactly as before.  See common.add_frame_hinges.
"""
import cadquery as cq
import params as p
from common import rounded_prism, add_frame_hinges


def build():
    cavity_w = p.LIGHT_W + p.XY_CLEARANCE
    cavity_h = p.LIGHT_H + p.XY_CLEARANCE
    outer_w = cavity_w + 2 * p.WALL
    outer_h = cavity_h + 2 * p.WALL

    frame = rounded_prism(outer_w, outer_h, p.COLLAR_DEPTH, p.CORNER_RADIUS_OUTER)
    aperture = rounded_prism(
        p.LIGHT_W - 2*p.APERTURE_OVERLAP,
        p.LIGHT_H - 2*p.APERTURE_OVERLAP,
        p.COLLAR_DEPTH + 2,
        max(2.0, p.CORNER_RADIUS_BODY - 1.0), z0=-1.0)
    frame = frame.cut(aperture)
    cavity = rounded_prism(cavity_w, cavity_h,
                           p.COLLAR_DEPTH - p.FRONT_LIP + 0.5,
                           p.CORNER_RADIUS_BODY, z0=p.FRONT_LIP)
    frame = frame.cut(cavity)
    return add_frame_hinges(frame)


# CQ-Editor preview.  Still fires on Run in CQ-Editor; skipped when frame.py is
# imported by export_all/validate_assembly, where show_object does not exist.
try:
    show_object(build())
except NameError:
    pass
