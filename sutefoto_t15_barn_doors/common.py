import cadquery as cq
from cadquery import Vector
import params as p


def rounded_prism(width, height, depth, radius, z0=0.0):
    wp = (cq.Workplane("XY")
          .box(width, height, depth, centered=(True, True, False))
          .edges("|Z").fillet(radius))
    return wp.translate((0, 0, z0)) if z0 else wp


def _cyl_x(cx, y, z, width):
    outer = cq.Solid.makeCylinder(p.HINGE_OD / 2, width,
                                  Vector(cx - width / 2, y, z), Vector(1, 0, 0))
    inner = cq.Solid.makeCylinder(p.HINGE_BORE_D / 2, width + 0.6,
                                  Vector(cx - width / 2 - 0.3, y, z), Vector(1, 0, 0))
    return cq.Workplane(obj=outer).cut(cq.Workplane(obj=inner))


def _cyl_y(x, cy, z, width):
    outer = cq.Solid.makeCylinder(p.HINGE_OD / 2, width,
                                  Vector(x, cy - width / 2, z), Vector(0, 1, 0))
    inner = cq.Solid.makeCylinder(p.HINGE_BORE_D / 2, width + 0.6,
                                  Vector(x, cy - width / 2 - 0.3, z), Vector(0, 1, 0))
    return cq.Workplane(obj=outer).cut(cq.Workplane(obj=inner))


def frame_dims():
    cavity_w = p.LIGHT_W + p.XY_CLEARANCE
    cavity_h = p.LIGHT_H + p.XY_CLEARANCE
    return cavity_w + 2 * p.WALL, cavity_h + 2 * p.WALL


def hinge_axis(side):
    ow, oh = frame_dims()
    r = p.HINGE_OD / 2
    if side == "top":
        return (0.0, oh / 2 + r + p.HINGE_RADIAL_GAP, p.HINGE_Z_TOP)
    if side == "bottom":
        return (0.0, -(oh / 2 + r + p.HINGE_RADIAL_GAP), p.HINGE_Z_BOTTOM)
    if side == "right":
        return (ow / 2 + r + p.HINGE_RADIAL_GAP, 0.0, p.HINGE_Z_SIDE)
    if side == "left":
        return (-(ow / 2 + r + p.HINGE_RADIAL_GAP), 0.0, p.HINGE_Z_SIDE)
    raise ValueError(side)


def _frame_x_hinges(model, side):
    """Center knuckles with a genuinely thick frame-to-barrel web.

    V8 keeps the hinge axis unchanged.  Unlike V7, the exposed bridge no longer
    terminates at the barrel tangent as a knife edge.  It penetrates into the
    barrel and joins it across a finite vertical chord whose thickness is set by
    FRAME_HINGE_WEB_THICKNESS.
    """
    _, oh = frame_dims()
    r = p.HINGE_OD / 2
    _, y, z = hinge_axis(side)
    sign = 1 if side == "top" else -1
    edge = sign * oh / 2
    tangent = y - sign * r
    root_depth = getattr(p, "FRAME_HINGE_ROOT_DEPTH", 4.0)
    web_t = getattr(p, "FRAME_HINGE_WEB_THICKNESS", 5.0)
    # Never let an older V7 params.py (which used 1.2 mm here) recreate the
    # paper-thin frame root. The root overlap is at least as thick as the web.
    root_overlap_z = max(getattr(p, "FRAME_HINGE_ROOT_Z_OVERLAP", 4.0), web_t)
    barrel_embed = getattr(p, "FRAME_HINGE_BARREL_EMBED", 1.5)
    root = edge - sign * root_depth
    attach = tangent + sign * barrel_embed

    # Keep the bridge chord inside the round barrel.
    chord_half = (max(0.0, r*r - (r - barrel_embed)**2)) ** 0.5
    half_web = min(web_t / 2.0, chord_half - 0.15)
    if half_web <= 0:
        raise ValueError("FRAME_HINGE_BARREL_EMBED is too small for the requested web thickness")

    for cx in p.HORIZONTAL_HINGE_STATIONS:
        model = model.union(_cyl_x(cx, y, z, p.HINGE_CENTER_W))
        yz = [(root, 0.0),
              (root, root_overlap_z),
              (edge, root_overlap_z),
              (attach, z + half_web),
              (attach, z - half_web),
              (edge, 0.0)]
        # Workplane YZ: local x=>Y, y=>Z, extrusion=>X.
        gus = (cq.Workplane("YZ")
               .polyline(yz).close()
               .extrude(p.HINGE_CENTER_W / 2, both=True)
               .translate((cx, 0, 0)))
        model = model.union(gus)
    return model


def _frame_y_hinges(model, side):
    ow, _ = frame_dims()
    r = p.HINGE_OD / 2
    x, _, z = hinge_axis(side)
    sign = 1 if side == "right" else -1
    edge = sign * ow / 2
    tangent = x - sign * r
    root_depth = getattr(p, "FRAME_HINGE_ROOT_DEPTH", 4.0)
    web_t = getattr(p, "FRAME_HINGE_WEB_THICKNESS", 5.0)
    # Never let an older V7 params.py (which used 1.2 mm here) recreate the
    # paper-thin frame root. The root overlap is at least as thick as the web.
    root_overlap_z = max(getattr(p, "FRAME_HINGE_ROOT_Z_OVERLAP", 4.0), web_t)
    barrel_embed = getattr(p, "FRAME_HINGE_BARREL_EMBED", 1.5)
    root = edge - sign * root_depth
    attach = tangent + sign * barrel_embed

    chord_half = (max(0.0, r*r - (r - barrel_embed)**2)) ** 0.5
    half_web = min(web_t / 2.0, chord_half - 0.15)
    if half_web <= 0:
        raise ValueError("FRAME_HINGE_BARREL_EMBED is too small for the requested web thickness")

    for cy in p.VERTICAL_HINGE_STATIONS:
        model = model.union(_cyl_y(x, cy, z, p.HINGE_CENTER_W))
        xz = [(root, 0.0),
              (root, root_overlap_z),
              (edge, root_overlap_z),
              (attach, z + half_web),
              (attach, z - half_web),
              (edge, 0.0)]
        # Workplane XZ: local x=>X, y=>Z, extrusion=>Y.
        gus = (cq.Workplane("XZ")
               .polyline(xz).close()
               .extrude(p.HINGE_CENTER_W / 2, both=True)
               .translate((0, cy, 0)))
        model = model.union(gus)
    return model


def add_frame_hinges(model):
    for side in ("top", "bottom"):
        model = _frame_x_hinges(model, side)
    for side in ("left", "right"):
        model = _frame_y_hinges(model, side)
    return model


def _panel_rib_from_polygon(pts, z0):
    panel = cq.Workplane("XY").polyline(pts).close().extrude(p.DOOR_T).translate((0, 0, z0))
    rib = (cq.Workplane("XY").polyline(pts).close().offset2D(-p.DOOR_RIB_W)
           .extrude(p.DOOR_T + p.DOOR_RIB_H).translate((0, 0, z0)))
    inner = (cq.Workplane("XY").polyline(pts).close().offset2D(-2 * p.DOOR_RIB_W)
             .extrude(p.DOOR_T + p.DOOR_RIB_H + 0.2).translate((0, 0, z0 - 0.1)))
    return panel.union(rib.cut(inner))


def _door_x_forks(model, side, root_y):
    _, y, z = hinge_axis(side)
    sign = 1 if side == "top" else -1
    r = p.HINGE_OD / 2
    for cx in p.HORIZONTAL_HINGE_STATIONS:
        off = p.HINGE_CENTER_W / 2 + p.HINGE_AXIAL_GAP + p.HINGE_FORK_W / 2
        for kx in (cx - off, cx + off):
            model = model.union(_cyl_x(kx, y, z, p.HINGE_FORK_W))
            barrel_tangent = y - sign * r
            half_fork = p.HINGE_FORK_W / 2
            half_root = p.DOOR_HINGE_ROOT_W / 2
            # Top grows toward -Y, bottom toward +Y.
            pts = [(kx-half_fork, barrel_tangent), (kx+half_fork, barrel_tangent),
                   (kx+half_root, root_y), (kx-half_root, root_y)]
            web = (cq.Workplane("XY").polyline(pts).close()
                   .extrude(p.DOOR_HINGE_WEB_H)
                   .translate((0, 0, z - p.DOOR_HINGE_WEB_H/2)))
            model = model.union(web)
    return model


def _door_y_forks(model, side, root_x):
    x, _, z = hinge_axis(side)
    sign = 1 if side == "right" else -1
    r = p.HINGE_OD / 2
    for cy in p.VERTICAL_HINGE_STATIONS:
        off = p.HINGE_CENTER_W / 2 + p.HINGE_AXIAL_GAP + p.HINGE_FORK_W / 2
        for ky in (cy - off, cy + off):
            model = model.union(_cyl_y(x, ky, z, p.HINGE_FORK_W))
            barrel_tangent = x - sign * r
            half_fork = p.HINGE_FORK_W / 2
            half_root = p.DOOR_HINGE_ROOT_W / 2
            pts = [(barrel_tangent, ky-half_fork), (barrel_tangent, ky+half_fork),
                   (root_x, ky+half_root), (root_x, ky-half_root)]
            web = (cq.Workplane("XY").polyline(pts).close()
                   .extrude(p.DOOR_HINGE_WEB_H)
                   .translate((0, 0, z - p.DOOR_HINGE_WEB_H/2)))
            model = model.union(web)
    return model


def build_door(side):
    """Build a door in its assembled, fully-closed position.

    Closed leaves lie in planes through their own forward hinge axes.  The top,
    bottom and side axes are staggered in Z, so closed leaves stack without
    colliding.  Opening is a 90-degree rotation away from the diffuser.
    """
    ow, oh = frame_dims()
    if side in ("top", "bottom"):
        _, _, z = hinge_axis(side)
        z0 = z - p.DOOR_T / 2
        s = 1 if side == "top" else -1
        root_y = s * (oh / 2 - p.LIGHT_TRAP_OVERLAP)
        tip_y = root_y - s * p.TOP_BOTTOM_DEPTH
        wb, wt = p.TOP_BOTTOM_BASE_W, p.TOP_BOTTOM_TIP_W
        pts = [(-wb/2, root_y), (wb/2, root_y), (wt/2, tip_y), (-wt/2, tip_y)]
        model = _panel_rib_from_polygon(pts, z0)
        return _door_x_forks(model, side, root_y)

    x, _, z = hinge_axis(side)
    z0 = z - p.DOOR_T / 2
    s = 1 if side == "right" else -1
    root_x = s * (ow / 2 - p.LIGHT_TRAP_OVERLAP)
    tip_x = root_x - s * p.SIDE_DEPTH
    hb, ht = p.SIDE_BASE_H, p.SIDE_TIP_H
    pts = [(root_x, -hb/2), (root_x, hb/2), (tip_x, ht/2), (tip_x, -ht/2)]
    model = _panel_rib_from_polygon(pts, z0)
    return _door_y_forks(model, side, root_x)
