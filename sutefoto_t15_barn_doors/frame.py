"""Front collar/frame for the SUTEFOTO T15.

Revision 4 fixes the clamp/door interference found in V2 and the inaccessible
flush-clamp idea from V3. The clamp screws are again installed from OUTSIDE,
but their bosses are moved behind the 8 mm collar/hinge plane. They press on
the top/bottom surfaces of the light several millimetres behind the front edge,
leaving the hinge barrels and barn-door sweep unobstructed.
"""
import cadquery as cq
from cadquery import Vector
import params as p
from common import rounded_prism, add_x_friction_hinges, add_y_friction_hinges


def build():
    cavity_w = p.LIGHT_W + p.XY_CLEARANCE
    cavity_h = p.LIGHT_H + p.XY_CLEARANCE
    outer_w = cavity_w + 2 * p.WALL
    outer_h = cavity_h + 2 * p.WALL

    frame = rounded_prism(outer_w, outer_h, p.COLLAR_DEPTH, p.CORNER_RADIUS_OUTER)

    # Front light aperture: overlaps the diffuser/bezel only a few millimetres.
    aperture = rounded_prism(
        p.LIGHT_W - 2 * p.APERTURE_OVERLAP,
        p.LIGHT_H - 2 * p.APERTURE_OVERLAP,
        p.COLLAR_DEPTH + 2,
        max(2.0, p.CORNER_RADIUS_BODY - 1.0),
        z0=-1.0,
    )
    frame = frame.cut(aperture)

    # Body cavity opens from the rear, leaving the front retaining lip.
    cavity = rounded_prism(
        cavity_w,
        cavity_h,
        p.COLLAR_DEPTH - p.FRONT_LIP + 0.5,
        p.CORNER_RADIUS_BODY,
        z0=p.FRONT_LIP,
    )
    frame = frame.cut(cavity)

    # Through-bolt friction hinges around the front perimeter.
    r = p.HINGE_OD / 2
    z = r
    y_top = outer_h / 2 + r + p.HINGE_RADIAL_GAP
    y_bot = -y_top
    x_right = outer_w / 2 + r + p.HINGE_RADIAL_GAP
    x_left = -x_right
    frame = add_x_friction_hinges(frame, y_top, z, True)
    frame = add_x_friction_hinges(frame, y_bot, z, True)
    frame = add_y_friction_hinges(frame, x_right, z, True)
    frame = add_y_friction_hinges(frame, x_left, z, True)
    return frame


if __name__ == "__main__":
    result = build()
    try:
        show_object(result)
    except NameError:
        cq.exporters.export(result, "frame.stl")

# Comment this out if not using cq-editor
show_object(build())