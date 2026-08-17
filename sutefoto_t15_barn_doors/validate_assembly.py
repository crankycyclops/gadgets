"""Quick geometry validation for V4.

Checks that the frame and representative top/right doors are valid solids and
that the doors do not intersect the frame over the intended 0..90 degree sweep.
"""
import cadquery as cq
import params as p
import frame, top_door, right_door


def intersection_volume(a, b):
    i = a.intersect(b)
    return 0.0 if i.isNull() else i.Volume()


def main():
    F = frame.build().val()
    assert F.isValid(), "frame is not a valid solid"

    cavity_w = p.LIGHT_W + p.XY_CLEARANCE
    cavity_h = p.LIGHT_H + p.XY_CLEARANCE
    outer_w = cavity_w + 2 * p.WALL
    outer_h = cavity_h + 2 * p.WALL
    r = p.HINGE_OD / 2

    local_y = -(r + p.HINGE_RADIAL_GAP)
    top_y = outer_h / 2 + r + p.HINGE_RADIAL_GAP
    T = top_door.build().val().translate(cq.Vector(0, top_y - local_y, 0))
    assert T.isValid(), "top door is not a valid solid"
    for angle in range(0, -91, -5):
        moved = T.rotate(cq.Vector(0, top_y, r), cq.Vector(1, top_y, r), angle)
        v = intersection_volume(F, moved)
        assert v < 1e-5, f"top door/frame collision at {angle} deg: {v} mm^3"

    local_x = -(r + p.HINGE_RADIAL_GAP)
    right_x = outer_w / 2 + r + p.HINGE_RADIAL_GAP
    D = right_door.build().val().translate(cq.Vector(right_x - local_x, 0, 0))
    assert D.isValid(), "right door is not a valid solid"
    for angle in range(0, 91, 5):
        moved = D.rotate(cq.Vector(right_x, 0, r), cq.Vector(right_x, 1, r), angle)
        v = intersection_volume(F, moved)
        assert v < 1e-5, f"right door/frame collision at {angle} deg: {v} mm^3"

    print("PASS: valid solids; no frame/door interference through intended 0-90 degree sweeps")


if __name__ == "__main__":
    main()
