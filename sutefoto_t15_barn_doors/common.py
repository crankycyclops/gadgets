import cadquery as cq
from cadquery import Vector
import params as p


def rounded_prism(width, height, depth, radius, z0=0.0):
    """Rounded rectangle prism centered on X/Y."""
    wp = cq.Workplane("XY").box(width, height, depth, centered=(True, True, False)).edges("|Z").fillet(radius)
    if z0:
        wp = wp.translate((0, 0, z0))
    return wp


def cylinder_along_x(x0, y, z, length, ro, ri=None):
    outer = cq.Solid.makeCylinder(ro, length, Vector(x0, y, z), Vector(1, 0, 0))
    shape = cq.Workplane(obj=outer)
    if ri:
        inner = cq.Solid.makeCylinder(ri, length + 0.4, Vector(x0 - 0.2, y, z), Vector(1, 0, 0))
        shape = shape.cut(cq.Workplane(obj=inner))
    return shape


def cylinder_along_y(x, y0, z, length, ro, ri=None):
    outer = cq.Solid.makeCylinder(ro, length, Vector(x, y0, z), Vector(0, 1, 0))
    shape = cq.Workplane(obj=outer)
    if ri:
        inner = cq.Solid.makeCylinder(ri, length + 0.4, Vector(x, y0 - 0.2, z), Vector(0, 1, 0))
        shape = shape.cut(cq.Workplane(obj=inner))
    return shape


def _x_knuckle(cx, y, z, width):
    return cylinder_along_x(cx - width / 2, y, z, width, p.HINGE_OD / 2, p.HINGE_BORE_D / 2)


def _y_knuckle(x, cy, z, width):
    return cylinder_along_y(x, cy - width / 2, z, width, p.HINGE_OD / 2, p.HINGE_BORE_D / 2)


def _box_xyz(dx, dy, dz, cx, cy, z0):
    return (cq.Workplane("XY")
            .box(dx, dy, dz, centered=(True, True, False))
            .translate((cx, cy, z0)))


def add_x_friction_hinges(model, y, z, frame_side):
    """Add X-axis hinge knuckles plus dedicated connector webs.

    The hinge barrel no longer intrudes into the mating frame/door body. This is
    important: only the frame's CENTER knuckle is connected to the frame, and only
    the door's FORK knuckles are connected to the door. The separate parts therefore
    do not occupy the same solid volume when assembled.
    """
    r = p.HINGE_OD / 2
    for cx in p.HORIZONTAL_HINGE_STATIONS:
        if frame_side:
            model = model.union(_x_knuckle(cx, y, z, p.HINGE_CENTER_W))
            # y is either positive (top) or negative (bottom). The nominal frame edge
            # is r + radial_gap inward from the hinge center.
            sign = 1 if y > 0 else -1
            edge_y = y - sign * (r + p.HINGE_RADIAL_GAP)
            barrel_tangent = y - sign * r
            cy = (edge_y + barrel_tangent) / 2
            dy = abs(barrel_tangent - edge_y) + 0.6
            web = _box_xyz(p.HINGE_CENTER_W, dy, 4.8, cx, cy, 1.2)
            model = model.union(web)
        else:
            off = p.HINGE_CENTER_W / 2 + p.HINGE_AXIAL_GAP + p.HINGE_FORK_W / 2
            for kx in (cx - off, cx + off):
                model = model.union(_x_knuckle(kx, y, z, p.HINGE_FORK_W))
                # Generic horizontal door extends from y=0 toward +Y; hinge center is
                # on negative Y. Bridge each fork to the panel without moving the
                # barrel into the frame volume.
                tangent = y + r
                cy = (tangent + 0.15) / 2
                dy = abs(0.15 - tangent) + 0.5
                web = _box_xyz(p.HINGE_FORK_W, dy, 3.2, kx, cy, 0.0)
                model = model.union(web)
    return model


def add_y_friction_hinges(model, x, z, frame_side):
    """Y-axis equivalent of add_x_friction_hinges()."""
    r = p.HINGE_OD / 2
    for cy in p.VERTICAL_HINGE_STATIONS:
        if frame_side:
            model = model.union(_y_knuckle(x, cy, z, p.HINGE_CENTER_W))
            sign = 1 if x > 0 else -1
            edge_x = x - sign * (r + p.HINGE_RADIAL_GAP)
            barrel_tangent = x - sign * r
            cx = (edge_x + barrel_tangent) / 2
            dx = abs(barrel_tangent - edge_x) + 0.6
            web = _box_xyz(dx, p.HINGE_CENTER_W, 4.8, cx, cy, 1.2)
            model = model.union(web)
        else:
            off = p.HINGE_CENTER_W / 2 + p.HINGE_AXIAL_GAP + p.HINGE_FORK_W / 2
            for ky in (cy - off, cy + off):
                model = model.union(_y_knuckle(x, ky, z, p.HINGE_FORK_W))
                tangent = x + r
                cx = (tangent + 0.15) / 2
                dx = abs(0.15 - tangent) + 0.5
                web = _box_xyz(dx, p.HINGE_FORK_W, 3.2, cx, ky, 0.0)
                model = model.union(web)
    return model


def horizontal_door():
    """Generic top/bottom leaf in print-friendly local coordinates.

    Hinge axis is along X on negative Y; panel extends toward +Y.
    """
    d = p.TOP_BOTTOM_DEPTH
    wb = p.TOP_BOTTOM_BASE_W
    wt = p.TOP_BOTTOM_TIP_W
    t = p.DOOR_T
    pts = [(-wb / 2, 0), (wb / 2, 0), (wt / 2, d), (-wt / 2, d)]
    panel = cq.Workplane("XY").polyline(pts).close().extrude(t)

    rib = cq.Workplane("XY").polyline(pts).close().offset2D(-p.DOOR_RIB_W).extrude(p.DOOR_RIB_H + t)
    inner = cq.Workplane("XY").polyline(pts).close().offset2D(-2 * p.DOOR_RIB_W).extrude(p.DOOR_RIB_H + t + 0.2)
    panel = panel.union(rib.cut(inner))

    hinge_y = -(p.HINGE_OD / 2 + p.HINGE_RADIAL_GAP)
    hinge_z = p.HINGE_OD / 2
    panel = add_x_friction_hinges(panel, hinge_y, hinge_z, frame_side=False)
    return panel


def vertical_door():
    """Generic left/right leaf in print-friendly local coordinates.

    Hinge axis is along Y on negative X; panel extends toward +X.
    """
    d = p.SIDE_DEPTH
    hb = p.SIDE_BASE_H
    ht = p.SIDE_TIP_H
    t = p.DOOR_T
    pts = [(0, -hb / 2), (0, hb / 2), (d, ht / 2), (d, -ht / 2)]
    panel = cq.Workplane("XY").polyline(pts).close().extrude(t)
    rib = cq.Workplane("XY").polyline(pts).close().offset2D(-p.DOOR_RIB_W).extrude(p.DOOR_RIB_H + t)
    inner = cq.Workplane("XY").polyline(pts).close().offset2D(-2 * p.DOOR_RIB_W).extrude(p.DOOR_RIB_H + t + 0.2)
    panel = panel.union(rib.cut(inner))

    hinge_x = -(p.HINGE_OD / 2 + p.HINGE_RADIAL_GAP)
    hinge_z = p.HINGE_OD / 2
    panel = add_y_friction_hinges(panel, hinge_x, hinge_z, frame_side=False)
    return panel
