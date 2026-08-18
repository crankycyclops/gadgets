import math

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


# --------------------------------------------------------------------------
# Frame-side hinge buttress (revision 9)
#
# The old design bridged frame to barrel with a tapered web that was exactly
# HINGE_CENTER_W (5 mm) wide and rooted 2 mm into the wall.  Printed with the
# collar's back face on the bed the layer planes run straight through that
# junction, so the hinges peeled off.
#
# The replacement is a solid rectangular beam standing on the outside of the
# collar, FRAME_HINGE_BEAM_W wide, spanning the full collar depth at its base
# and carrying on out and forward until it wraps over the barrel.  Because it is
# a plain prism whose outboard face is parallel to the build direction it prints
# without overhang and puts its full section exactly where the bending moment
# peaks -- at the frame.
#
# It is deliberately built over-fat and then cut back by the volume the doors
# actually sweep, so clearance is derived rather than guessed.  The two cuts
# are kept separate on purpose:
#
#   * the leaf sweep is cut across the whole beam;
#   * the fork sweep is cut only in the axial bands the forks occupy, which
#     leaves the beam full width in wings that straddle the hinge.
#
# A coaxial channel of radius FRAME_HINGE_FASTENER_R is bored either side of the
# centre knuckle so the fork barrels, washers, nyloc and driver all reach the
# bolt exactly as before.
#
# Each block only needs its own door's clearance: rotation about X leaves the
# top/bottom leaves inside |x| <= 77 while the side blocks start at |x| >= 80.6,
# and rotation about Y leaves the side leaves inside |y| <= 37 while the
# top/bottom blocks start at |y| >= 40.1.
# --------------------------------------------------------------------------

_TRAVEL = {"top": 90.0, "bottom": -90.0, "left": 90.0, "right": -90.0}
_PROFILE_PLANE = {"X": "YZ", "Y": "XZ"}


def _axis_frame(side):
    """Working frame for one hinge side.

    Returns (about, ua, va, sign, edge) where `about` is the rotation axis, and
    the profile plane is spanned by u (Y for top/bottom, X for left/right) and
    v (always Z).  `ua`/`va` locate the hinge axis in that plane, `sign` points
    outboard and `edge` is the frame's outer face.
    """
    ow, oh = frame_dims()
    x, y, z = hinge_axis(side)
    if side in ("top", "bottom"):
        sign = 1 if side == "top" else -1
        return "X", y, z, sign, sign * oh / 2
    sign = 1 if side == "right" else -1
    return "Y", x, z, sign, sign * ow / 2


def _prism(about, pts, ua, va, station, width):
    """Extrude an axis-relative (u, v) polygon across the hinge axis."""
    wp = (cq.Workplane(_PROFILE_PLANE[about])
          .polyline([(u + ua, v + va) for u, v in pts]).close()
          .extrude(width / 2.0, both=True))
    return wp.translate((station, 0, 0) if about == "X" else (0, station, 0))


def _axis_cylinder(about, ua, va, station, radius, length):
    if about == "X":
        base, direction = Vector(station - length / 2.0, ua, va), Vector(1, 0, 0)
    else:
        base, direction = Vector(ua, station - length / 2.0, va), Vector(0, 1, 0)
    return cq.Workplane(obj=cq.Solid.makeCylinder(radius, length, base, direction))


def _axis_slab(about, station, lo, hi, big=400.0):
    """Slab covering axial offsets [lo, hi] on one side of `station`."""
    width = hi - lo
    center = station + (lo + hi) / 2.0
    if about == "X":
        box = cq.Workplane("XY").box(width, big, big)
        return box.translate((center, 0, 0))
    box = cq.Workplane("XY").box(big, width, big)
    return box.translate((0, center, 0))


def _rect_polar(u0, u1, v0, v1):
    """Polar bounds of an axis-relative rectangle: (rmin, rmax, amin, amax)."""
    u0, u1 = sorted((u0, u1))
    v0, v1 = sorted((v0, v1))
    corners = [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]
    rmax = max(math.hypot(u, v) for u, v in corners)
    # Nearest point of the rectangle to the axis; may lie on an edge.
    rmin = math.hypot(min(max(0.0, u0), u1), min(max(0.0, v0), v1))
    base = math.degrees(math.atan2((v0 + v1) / 2.0, (u0 + u1) / 2.0))
    deltas = []
    for u, v in corners:
        d = math.degrees(math.atan2(v, u)) - base
        while d > 180.0:
            d -= 360.0
        while d <= -180.0:
            d += 360.0
        deltas.append(d)
    return rmin, rmax, base + min(deltas), base + max(deltas)


def _wedge_pts(radius, a0, a1):
    """Pie wedge from the hinge axis.  Its arc is faceted, which is harmless out
    at `radius`; the barrel end of the cut is trimmed by a real cylinder so the
    knuckle keeps an exactly round surface."""
    segs = max(8, int(abs(a1 - a0) / 4.0))
    pts = [(0.0, 0.0)]
    for i in range(segs + 1):
        a = math.radians(a0 + (a1 - a0) * i / segs)
        pts.append((radius * math.cos(a), radius * math.sin(a)))
    return pts


def _door_opening(side, station, width):
    """The single open slot the door swings in.

    Leaf and fork each stay inside the annulus their own rectangle spans,
    rotated by at most the door's travel, so one sector over the wider of the
    two contains the whole swept volume.  Cutting that as a single shape --
    rather than chasing the fork's flare band by band -- is what keeps the slot
    open instead of leaving thin stepped teeth standing in it.

    The inner radius is the barrel radius exactly, with no radial slack: the
    forks turn about this same axis, so there is nothing to clear radially and
    any inflation here would eat into the knuckle the bolt runs through.
    """
    about, ua, va, _, _ = _axis_frame(side)
    # A right-handed rotation about +Y runs backwards in the (x, z) plane, so
    # the left/right leaves sweep the opposite way to their door angle.
    travel = _TRAVEL[side] if about == "X" else -_TRAVEL[side]
    amin = amax = None
    rmax = 0.0
    for rect in _door_profile_rects(side):
        _, r1, a0, a1 = _rect_polar(*rect)
        rmax = max(rmax, r1)
        amin = a0 if amin is None else min(amin, a0)
        amax = a1 if amax is None else max(amax, a1)
    slack = p.FRAME_HINGE_DOOR_ANGLE_CLEAR
    pts = _wedge_pts(rmax + 1.0,
                     amin + min(0.0, travel) - slack,
                     amax + max(0.0, travel) + slack)
    wedge = _prism(about, pts, ua, va, station, width)
    barrel = _axis_cylinder(about, ua, va, station, p.HINGE_OD / 2, width + 2.0)
    return wedge.cut(barrel)


def _door_profile_rects(side):
    """Leaf and fork cross-sections as axis-relative (u0, u1, v0, v1).

    Read straight off build_door so the clearance can never drift away from the
    door that is actually built -- including the light-trap root overlap, which
    is what puts the leaf root only 7.8 mm from the hinge axis.
    """
    ow, oh = frame_dims()
    r = p.HINGE_OD / 2
    if side in ("top", "bottom"):
        _, ua, _ = hinge_axis(side)
        sign = 1 if side == "top" else -1
        u_root = sign * (oh / 2 - p.LIGHT_TRAP_OVERLAP) - ua
        depth = p.TOP_BOTTOM_DEPTH
    else:
        ua, _, _ = hinge_axis(side)
        sign = 1 if side == "right" else -1
        u_root = sign * (ow / 2 - p.LIGHT_TRAP_OVERLAP) - ua
        depth = p.SIDE_DEPTH
    grow = -sign                      # the leaf runs inboard from its axis
    reach = min(depth, p.FRAME_HINGE_SWEEP_REACH)
    leaf = (u_root, u_root + grow * reach,
            -p.DOOR_T / 2, p.DOOR_T / 2 + p.DOOR_RIB_H)
    fork = (-sign * r, u_root,
            -p.DOOR_HINGE_WEB_H / 2, p.DOOR_HINGE_WEB_H / 2)
    return leaf, fork


def _hinge_block(side, station):
    about, ua, va, sign, edge = _axis_frame(side)
    r = p.HINGE_OD / 2
    span = p.FRAME_HINGE_BEAM_W + 4.0

    # An L in section: the base roots into the wall across the whole collar
    # depth, while everything forward of the front face stays outboard of the
    # frame's outer edge.  That is what keeps the beam clear of the plane the
    # closed leaves occupy, so the light trap is unaffected by it.
    u_in = edge - sign * p.FRAME_HINGE_ROOT_DEPTH
    u_out = ua + sign * (r + p.FRAME_HINGE_SADDLE_T)
    v_lo = va - (r + p.FRAME_HINGE_SADDLE_T)
    pts = [(u_in - ua, p.COLLAR_DEPTH - va), (u_out - ua, p.COLLAR_DEPTH - va),
           (u_out - ua, v_lo - va), (edge - ua, v_lo - va),
           (edge - ua, -va), (u_in - ua, -va)]
    block = _prism(about, pts, ua, va, station, p.FRAME_HINGE_BEAM_W)

    # Hardware channel: coaxial, everywhere except the centre knuckle itself.
    channel = _axis_cylinder(about, ua, va, station, p.FRAME_HINGE_FASTENER_R, span)
    core = _axis_slab(about, station, -p.HINGE_CENTER_W / 2.0, p.HINGE_CENTER_W / 2.0)
    block = block.cut(channel.cut(core))

    # One clean opening for the door, across the whole beam.  What survives is
    # the arc behind and outboard of the barrel, which is the load path back to
    # the frame; the beam keeps its full width all the way along it.
    block = block.cut(_door_opening(side, station, span))

    return block.cut(_axis_cylinder(about, ua, va, station, p.HINGE_BORE_D / 2.0, span))


def add_frame_hinges(model):
    for side in ("top", "bottom"):
        for station in p.HORIZONTAL_HINGE_STATIONS:
            model = model.union(_hinge_block(side, station))
    for side in ("left", "right"):
        for station in p.VERTICAL_HINGE_STATIONS:
            model = model.union(_hinge_block(side, station))
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
