"""SUTEFOTO T15 collar/frame, revision 8.

The collar fit is unchanged in concept.  Only the hinge mounting geometry is
reworked: all hinge axes are forward of the front face, allowing the leaves to
close flat over the diffuser and open without striking the frame.
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


# CQ-Editor preview (uncomment when desired):
show_object(build())
