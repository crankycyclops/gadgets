import math

import cadquery as cq
from cadquery import Vector
import params as p


def rounded_prism(width, height, depth, radius, z0=0.0):
    wp = (cq.Workplane("XY")
          .box(width, height, depth, centered=(True, True, False))
          .edges("|Z").fillet(radius))
    return wp.translate((0, 0, z0)) if z0 else wp


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

_OPEN_DIRECTION = {"top": 1, "bottom": -1, "left": 1, "right": -1}
_PROFILE_PLANE = {"X": "YZ", "Y": "XZ"}


def _travel(side, about):
    """Signed in-plane travel of a leaf, in the (u, v) plane of its hinge.

    A right-handed rotation about +Y runs backwards in the (x, z) plane, so the
    left/right leaves sweep the opposite way to their door angle.
    """
    signed = _OPEN_DIRECTION[side] * p.FRAME_HINGE_MAX_OPEN
    return signed if about == "X" else -signed


def _stations(about):
    return (p.HORIZONTAL_HINGE_STATIONS if about == "X"
            else p.VERTICAL_HINGE_STATIONS)


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


def _sweep_wedge(side, station, width, rects, inner):
    """Everywhere `rects` reach over the door's travel, from `inner` outward.

    `inner` matters as much as the sector does.  The leaf is a thin plate that
    never comes nearer the axis than its root radius, so cutting the beam from
    the barrel outward on the leaf's account throws away a solid ring of plastic
    around the knuckle for nothing.

    A rect stays inside the annulus it spans, rotated by at most the door's
    travel, so one sector contains its whole swept volume.  Cutting that as a
    single shape -- rather than chasing the fork's flare band by band -- is what
    keeps the slot open instead of leaving stepped teeth standing in it.
    """
    about, ua, va, _, _ = _axis_frame(side)
    travel = _travel(side, about)
    amin = amax = None
    rmax = 0.0
    for rect in rects:
        _, r1, a0, a1 = _rect_polar(*rect)
        rmax = max(rmax, r1)
        amin = a0 if amin is None else min(amin, a0)
        amax = a1 if amax is None else max(amax, a1)
    slack = p.FRAME_HINGE_DOOR_ANGLE_CLEAR
    pts = _wedge_pts(rmax + 1.0,
                     amin + min(0.0, travel) - slack,
                     amax + max(0.0, travel) + slack)
    wedge = _prism(about, pts, ua, va, station, width)
    return wedge.cut(_axis_cylinder(about, ua, va, station, inner, width + 2.0))


def _fork_cuts(side, rho, width, stations=None):
    """Fork slots trimmed to the volume the forks actually sweep.

    `_shroud` takes the slots as full turns of revolution, which is safe but
    severs anything narrow they cross.  Out on a 2.4 mm shroud that costs a
    little coverage and nothing else.  A beam carrying the hinges cannot afford
    it, so here each slot is intersected with its own swept sector -- the same
    shape `_hinge_block` has always used, and exact rather than conservative,
    because outside the sector the fork is not there at any door angle.
    """
    about = _axis_frame(side)[0]
    fork = _door_profile_rects(side)[1]
    cuts = []
    for station in (_stations(about) if stations is None else stations):
        sector = _sweep_wedge(side, station, width, (fork,), p.HINGE_OD / 2)
        for cone in _fork_slots(side, rho, stations=(station,)):
            cuts.append(cone.intersect(sector))
    return cuts


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
    # The fork rect starts at the barrel radius, not at the axis, even though
    # the web and saddle now carry on inboard of it.  Everything they add there
    # stays inside FRAME_HINGE_FASTENER_R, where the coaxial channel has already
    # cleared the beam at every angle; taking the rect in to the axis instead
    # would swing the sector out to +-90 degrees and cut the beam away for
    # nothing.
    fork = (-sign * r, u_root,
            -p.DOOR_HINGE_WEB_H / 2, p.DOOR_HINGE_WEB_H / 2)
    return leaf, fork


def _hinge_block(side, station):
    about, ua, va, sign, edge = _axis_frame(side)
    r = p.HINGE_OD / 2
    span = p.FRAME_HINGE_BEAM_W + 4.0

    u_out = ua + sign * (r + p.FRAME_HINGE_SADDLE_T)
    v_lo = va - (r + p.FRAME_HINGE_SADDLE_T)
    if _rail_borne(side, station):
        # The collar this beam used to root in is inside the adapter window, so
        # there is no wall left to put a foot in.  A plain prism instead,
        # stopped at the cut plane and standing on the rail -- see
        # _adapter_rail.
        pts = [(edge - ua, v_lo - va), (u_out - ua, v_lo - va),
               (u_out - ua, p.ADAPTER_CUT_Z - va),
               (edge - ua, p.ADAPTER_CUT_Z - va)]
    else:
        # An L in section: the base roots into the wall across the whole collar
        # depth, while everything forward of the front face stays outboard of
        # the frame's outer edge.  That is what keeps the beam clear of the
        # plane the closed leaves occupy, so the light trap is unaffected by it.
        u_in = edge - sign * p.FRAME_HINGE_ROOT_DEPTH
        pts = [(u_in - ua, p.COLLAR_DEPTH - va), (u_out - ua, p.COLLAR_DEPTH - va),
               (u_out - ua, v_lo - va), (edge - ua, v_lo - va),
               (edge - ua, -va), (u_in - ua, -va)]
    block = _prism(about, pts, ua, va, station, p.FRAME_HINGE_BEAM_W)

    leaf = _door_profile_rects(side)[0]
    leaf_rmin = _rect_polar(*leaf)[0]

    # Across the whole beam, only what the leaf sweeps -- and the leaf is a thin
    # plate that never comes nearer the axis than its root radius.
    block = block.cut(_sweep_wedge(side, station, span, (leaf,), leaf_rmin))

    # Only the centre knuckle has any business reaching round the barrel.  The
    # door hangs entirely off HINGE_CENTER_W; the bands either side of it carry
    # nothing, because no fork ever touches them.  Left standing they came out
    # as partial knuckles -- crescents of wall spanning the fastener channel to
    # the leaf's root radius, and tapering to a feather edge where the sweep
    # sector's boundary ran down tangent to the channel.  They boxed in the
    # nyloc from the one side a spanner could reach it, and the feathered ends
    # would have snapped off the moment they were handled.
    #
    # So outside the knuckle the beam stops dead at the channel's rear tangent
    # plane.  Being tangent, the channel then takes nothing out of the beam
    # there at all, which is what leaves a flat full-thickness face rather than
    # another thin edge -- and everything forward of it, the whole M3 stack
    # included, is open to a spanner from the front.
    z_step = va + p.FRAME_HINGE_FASTENER_R
    big = 400.0
    forward = (cq.Workplane("XY").box(big, big, big)
               .translate((0, 0, z_step - big / 2.0)))
    core = _axis_slab(about, station, -p.HINGE_CENTER_W / 2.0,
                      p.HINGE_CENTER_W / 2.0)
    block = block.cut(forward.cut(core))

    # The forks do reach the barrel, but only where they actually are.  Cutting
    # the full beam width down to the barrel is what left the saddle as a thin
    # hook tapering to a point; keeping it to the forks' own flared footprint
    # leaves a solid collar round the knuckle instead.
    for cut in _fork_cuts(side, p.FRAME_HINGE_BEAM_W, span, stations=(station,)):
        block = block.cut(cut)
    return block


def _hardware_cuts(side, station):
    """Room for the bolt, its washers and the nyloc, and for the door forks.

    Applied to the finished frame rather than to the beam alone, because the
    shroud runs straight through the same space.
    """
    about, ua, va, _, _ = _axis_frame(side)
    # Stops at the beam's own width.  The hardware never reaches past it, and
    # anything further would only be cutting the shroud for nothing.
    channel = _axis_cylinder(about, ua, va, station, p.FRAME_HINGE_FASTENER_R,
                             p.FRAME_HINGE_BEAM_W)
    core = _axis_slab(about, station, -p.HINGE_CENTER_W / 2.0, p.HINGE_CENTER_W / 2.0)
    # The bore only has to clear the knuckle, which is the only thing the
    # channel leaves standing on the axis.  Run at FRAME_HINGE_BEAM_W + 4 it
    # stood 2 mm proud of both ends of the beam, and on a wall carrying an
    # adapter rail those 2 mm are solid: four blind holes drilled into the one
    # member holding that wall's hinges up.  Ending inside the channel instead
    # puts both ends of the bore in space that is already empty.
    return [channel.cut(core),
            _axis_cylinder(about, ua, va, station, p.HINGE_BORE_D / 2.0,
                           p.HINGE_CENTER_W + 4.0)]


def _shroud_radius(side):
    """How far the shroud may reach from the hinge axis: just inside the circle
    the leaf root sweeps."""
    return _rect_polar(*_door_profile_rects(side)[0])[0] - p.FRAME_SHROUD_CLEAR


def _leaf_half_span(side):
    """Half-width of the widest thing on this leaf, exactly.

    Kept apart from _leaf_reach because the margin there is only ever safe when
    it widens a cut.  Asking how far the frame's outline has curved inboard by
    the time the leaf ends is the other kind of question, and a margin in it
    demands clearance for a leaf that is not present -- at |x| = 78 the top
    outline has reached y = 39.66, a 7.39 mm standoff, which is outside the
    clearance cylinder altogether and would delete the corner wall entirely.
    """
    base = (p.TOP_BOTTOM_BASE_W if side in ("top", "bottom") else p.SIDE_BASE_H)
    return base / 2.0


def _leaf_reach(side):
    """Half-width of the widest thing on this leaf, plus a margin.  Outside this
    the leaf simply is not there, at any angle."""
    return _leaf_half_span(side) + 1.0


def _outline_span_start(side):
    """Span position where the frame outline leaves its straight run and starts
    round the corner arc.  `span` is x for the top/bottom walls, y for the sides.
    """
    ow, oh = frame_dims()
    half = (ow if side in ("top", "bottom") else oh) / 2.0
    return half - p.CORNER_RADIUS_OUTER


def _outline_u(side, span):
    """How far out the frame's outline stands at span position `span`, as a
    magnitude, for the wall on this side.

    Flat at the outer edge along the straight run, then curving inboard round
    the corner arc.  This is the number the shroud's clearance was missing: the
    straight run's `edge` is not what the wall stands on near a corner.
    """
    ow, oh = frame_dims()
    edge = (oh if side in ("top", "bottom") else ow) / 2.0
    s0 = _outline_span_start(side)
    if abs(span) <= s0:
        return edge
    d = min(abs(span) - s0, p.CORNER_RADIUS_OUTER)
    return edge - p.CORNER_RADIUS_OUTER + math.sqrt(
        max(0.0, p.CORNER_RADIUS_OUTER ** 2 - d * d))


def _shroud_corner_span(side):
    """Span range over which the outline has curved inboard *and* a leaf can
    still reach the wall.  Beyond it the leaf is simply not there."""
    return _outline_span_start(side), _leaf_reach(side)


def _shroud_corner_depth(side):
    """Depth allowed over that corner span.

    Same rule as _shroud_side_depth -- the wall may reach as deep as the
    clearance cylinder allows -- but measured from the standoff at the leaf's
    own outer end, which is the worst case anywhere a leaf actually sweeps.
    """
    _, ua, va, _, _ = _axis_frame(side)
    rho = _shroud_radius(side)
    standoff = abs(ua) - _outline_u(side, _leaf_half_span(side))
    return abs(va) + math.sqrt(max(0.0, rho * rho - standoff * standoff))


def _shroud_side_depth(side):
    """How far forward this side's wall may reach.

    Set by the wall's inboard face, which is the part nearest the circle the
    leaf root sweeps.  One number per side gives a plain flat-bottomed wall --
    following the clearance cylinder itself would buy about 1.4 mm more depth on
    the outboard half and cost a tapered, pointed edge to get it.
    """
    _, ua, va, _, edge = _axis_frame(side)
    rho = _shroud_radius(side)
    standoff = abs(edge - ua)
    return abs(va) + math.sqrt(max(0.0, rho * rho - standoff * standoff))


def _shroud_depth():
    return max(_shroud_side_depth(s)
               for s in ("top", "bottom", "left", "right"))


def _shroud(t=None, sector_forks=False, level_corners=True):
    """One wall following the frame's whole outline, standing forward from the
    front face, to block the light that otherwise pours out of the frame/leaf
    gap when a door is open.

    `t` overrides FRAME_SHROUD_T, `sector_forks` takes the fork slots as swept
    sectors rather than full turns, and `level_corners=False` leaves the
    corners at full depth.  All three exist for `_adapter_rail`, which needs
    this same wall -- same outline, same per-side and per-corner depth steps --
    only thicker, not severed by its own slots, and with its corners kept whole
    to root in.  Deriving the rail
    from here rather than re-writing the steps is the whole point: the corner
    step is the one the shroud got wrong in revision 10, and a rail that wraps
    the corners has to get it right for two walls at once.

    Where a leaf can reach it, the wall is trimmed by a cylinder concentric with
    that leaf's hinge axis, FRAME_SHROUD_CLEAR inside the circle the leaf root
    sweeps.  Both being surfaces of revolution about the axis, their separation
    is the same at every door angle -- which is exactly what a flat skirt cannot
    manage, and why this works away from 90 degrees.

    The corners get a second, shallower step of their own.  Revision 10 left
    them at full depth, reasoning that the leaves are narrower than the frame --
    |x| <= 77 against an 82.75 edge -- so nothing sweeps them.  That compares the
    leaf against the wrong number: the outline does not stay at its straight-run
    edge out there, it curves inboard round CORNER_RADIUS_OUTER, and by |x| = 77
    it has reached y = 40.36.  That is a 6.69 mm standoff from the hinge axis
    where the straight run has 4.8, and a standoff that large leaves room for
    much less depth.  The leaf duly swept the corner wall from 27 degrees on.

    Those steps only run out to each wall's own leaf reach, though, and the
    ring is built at the deepest wall's depth.  So the piece of corner past
    both neighbours' reach was never stepped at all, and stood as a fin at full
    depth above the corner step either side of it -- 7 mm proud at the top
    corners, 12 mm at the bottom.  No leaf reaches it, so it is levelled to the
    shallower of the two corner steps it sits between.  `_adapter_rail` turns
    that off: on the rail the full-depth corner is not a fin but what the rail
    roots in.

    The wall sits outboard of the frame's outer face, so it stays clear of the
    plane the closed leaves stack in and leaves the light trap untouched.
    """
    ow, oh = frame_dims()
    t = p.FRAME_SHROUD_T if t is None else t
    sides = ("top", "bottom", "left", "right")
    depth = _shroud_depth()

    # Carried back over the collar's full depth, not just forward of the front
    # face.  Stopping at z=0 would leave the wall joined to the frame along the
    # outer edge line only -- a knife edge that is neither strong nor printable.
    # Sheathing the collar gives a proper face-to-face join instead.
    height = depth + p.COLLAR_DEPTH
    outer = rounded_prism(ow + 2 * t, oh + 2 * t, height,
                          p.CORNER_RADIUS_OUTER + t, z0=-depth)
    inner = rounded_prism(ow, oh, height + 2, p.CORNER_RADIUS_OUTER, z0=-depth - 1)
    ring = outer.cut(inner)

    for side in sides:
        about, ua, va, sign, edge = _axis_frame(side)
        reach = _leaf_reach(side)
        # A single flat step back to this side's own depth, across the span the
        # leaf can reach.
        cut_h = depth + 2 - _shroud_side_depth(side)
        lo, hi = sorted((edge - sign * 1.0, edge + sign * (t + 1.0)))
        if about == "X":
            box = cq.Workplane("XY").box(2 * reach, hi - lo, cut_h,
                                         centered=(True, True, False))
            box = box.translate((0, (lo + hi) / 2, -(depth + 2)))
        else:
            box = cq.Workplane("XY").box(hi - lo, 2 * reach, cut_h,
                                         centered=(True, True, False))
            box = box.translate(((lo + hi) / 2, 0, -(depth + 2)))
        ring = ring.cut(box)

        # Then a second, shallower step at each end, over the span where the
        # outline has curved inboard and a leaf still reaches it.  Reaching
        # further inboard than the first step, too: out there the wall itself
        # stands inboard of `edge`, so a band starting at edge - 1 misses it.
        s_lo, s_hi = _shroud_corner_span(side)
        if s_hi > s_lo:
            c_h = depth + 2 - _shroud_corner_depth(side)
            c_lo, c_hi = sorted((sign * (_outline_u(side, s_hi) - 1.0),
                                 edge + sign * (t + 1.0)))
            for end in (1, -1):
                a, b = sorted((end * s_lo, end * s_hi))
                if about == "X":
                    box = cq.Workplane("XY").box(b - a, c_hi - c_lo, c_h,
                                                 centered=(True, True, False))
                    box = box.translate(((a + b) / 2, (c_lo + c_hi) / 2,
                                         -(depth + 2)))
                else:
                    box = cq.Workplane("XY").box(c_hi - c_lo, b - a, c_h,
                                                 centered=(True, True, False))
                    box = box.translate(((c_lo + c_hi) / 2, (a + b) / 2,
                                         -(depth + 2)))
                ring = ring.cut(box)

        rho = _shroud_radius(side)
        cuts = (_fork_cuts(side, rho, p.FRAME_HINGE_BEAM_W + 4.0) if sector_forks
                else _fork_slots(side, rho))
        for cut in cuts:
            ring = ring.cut(cut)

    if level_corners:
        # Past both neighbours' leaf reach, at the shallower of their corner
        # depths.  Nothing but the ring stands out there, so the box can run
        # generously past the outline.
        for long_side, short_side in (("top", "right"), ("top", "left"),
                                      ("bottom", "right"), ("bottom", "left")):
            sx = _axis_frame(short_side)[3]
            sy = _axis_frame(long_side)[3]
            c_depth = min(_shroud_corner_depth(long_side),
                          _shroud_corner_depth(short_side))
            x0, x1 = sorted((sx * _leaf_reach(long_side), sx * (ow / 2 + t + 1.0)))
            y0, y1 = sorted((sy * _leaf_reach(short_side), sy * (oh / 2 + t + 1.0)))
            box = cq.Workplane("XY").box(x1 - x0, y1 - y0, depth + 2 - c_depth,
                                         centered=False)
            ring = ring.cut(box.translate((x0, y0, -(depth + 2))))
    return ring


_REVOLVE_PLANE = {"X": "XZ", "Y": "YZ"}


def _fork_slots(side, rho, stations=None):
    """Slots where the door forks sweep through the shroud.

    A fork web flares from HINGE_FORK_W at the barrel to DOOR_HINGE_ROOT_W at
    its root, so the slot has to widen with radius.  That makes the exact slot a
    solid of revolution about the hinge axis with a straight tapered side, which
    is what gets revolved here -- approximating it with a stack of radial bands
    leaves a staircase down the slot edge.

    Revolved through a full turn because a fork visits many angles, so the slot
    has to be open at all of them.
    """
    about, ua, va, _, _ = _axis_frame(side)
    r = p.HINGE_OD / 2
    u_root = abs(_door_profile_rects(side)[1][1])
    off = p.HINGE_CENTER_W / 2 + p.HINGE_AXIAL_GAP + p.HINGE_FORK_W / 2
    flare = (p.DOOR_HINGE_ROOT_W - p.HINGE_FORK_W) / 2.0

    near = p.HINGE_FORK_W / 2 + p.FRAME_SHROUD_FORK_CLEAR
    # The flare runs from the barrel out to the web's own root radius and stops
    # there, so that -- not `rho` -- is where the taper ends.  `rho` is a
    # different quantity: how far this cut has to reach.  Interpolating the
    # taper to it stretched a 4 -> 7.8 flare over 4 -> 24 for the beam, so the
    # slot came out 2.86 mm half-width where the web is 5.5, and the doors could
    # not be pressed onto their axes at all.  Where rho is inside u_root, as it
    # is for the shroud, the two agree and the slot is unchanged.
    r_flare = min(u_root, rho)
    far = near + flare * (r_flare - r) / (u_root - r)

    cuts = []
    for station in (_stations(about) if stations is None else stations):
        for c in (station - off, station + off):
            # Constant width inside the barrel radius, then the flare.
            pts = [(c - near, va), (c + near, va), (c + near, va + r),
                   (c + far, va + r_flare), (c + far, va + rho + 2.0),
                   (c - far, va + rho + 2.0), (c - far, va + r_flare),
                   (c - near, va + r)]
            sol = (cq.Workplane(_REVOLVE_PLANE[about])
                   .polyline(pts).close()
                   .revolve(360, (0, va), (1, va)))
            cuts.append(sol.translate((0, ua, 0) if about == "X" else (ua, 0, 0)))
    return cuts


# --------------------------------------------------------------------------
# Tripod adapter window (revision 12)
#
# See params.py for why the window is needed and why the hinge planes move
# forward to suit.  Here there are only five shapes: the window itself, the
# rail that carries a cut short wall's hinges once the collar under them is
# gone, the gap cut back out of that rail between its hinges, the fill that
# closes a window that is not in use, and the relief that keeps a cut wall's
# closed leaf out of the plate.
# --------------------------------------------------------------------------


def _is_cut(side):
    return side in p.ADAPTER_CUT_SIDES


def adapter_blocked(side):
    """Is this wall's window filled back in?

    Only ever the frame's business.  The wall is still cut as far as the hinge
    planes and the door leaf reliefs are concerned, which is what lets one set
    of doors fit a frame with the window open or closed.
    """
    if not _is_cut(side):
        return False
    short = _axis_frame(side)[0] == "Y"
    return p.ADAPTER_BLOCK_SHORT if short else p.ADAPTER_BLOCK_LONG


def _adapter_band(side):
    """Along-wall bounds of the window: x on the long walls, y on the short."""
    c = p.ADAPTER_CUT_CENTER.get(side, 0.0)
    half = p.ADAPTER_PLATE_L / 2.0 + p.ADAPTER_CUT_CLEAR
    return c - half, c + half


def _rail_borne(side, station):
    """Does this station's beam lose the collar it roots in?

    Only on a cut short wall.  A cut long wall's stations are at |x| 43-67
    against a 33.25 half-band, so they never meet the window at all -- which is
    the whole reason the long-side cutout is cheap and the short-side one is
    not.
    """
    if not _is_cut(side) or _axis_frame(side)[0] != "Y":
        return False
    lo, hi = _adapter_band(side)
    half = p.FRAME_HINGE_BEAM_W / 2.0
    return station + half > lo and station - half < hi


def _light_face(side):
    """Signed position of the light's own outer face on this side.

    This -- not the cavity wall, which stands XY_CLEARANCE/2 outboard of it --
    is the surface the plate seats on, so it is where the window has to start.
    There being nothing inboard of it is exactly why the window is a window and
    not a relief pocket.
    """
    sign = _axis_frame(side)[3]
    half = (p.LIGHT_H if side in ("top", "bottom") else p.LIGHT_W) / 2.0
    return sign * half


def _wall_box(side, lo, hi, u0, u1, z0, z1):
    """Box in wall-relative terms: `lo`/`hi` along the wall, `u0`/`u1` across it."""
    u0, u1 = sorted((u0, u1))
    if _axis_frame(side)[0] == "X":            # long wall: the span runs along x
        box = cq.Workplane("XY").box(hi - lo, u1 - u0, z1 - z0, centered=False)
        return box.translate((lo, u0, z0))
    box = cq.Workplane("XY").box(u1 - u0, hi - lo, z1 - z0, centered=False)
    return box.translate((u0, lo, z0))


def _adapter_cut(side):
    """Everything the seated plate's footprint has to be clear of on one wall.

    One box: from the light's face outward past the frame's outer extent, and
    from ADAPTER_CUT_Z rearward past the collar's back face.  So it takes the
    collar wall, the front lip, the shroud and anything else standing in the
    window in a single cut, which is also why it is applied last.
    """
    sign = _axis_frame(side)[3]
    lo, hi = _adapter_band(side)
    face = _light_face(side)
    return _wall_box(side, lo, hi, face, face + sign * 60.0,
                     p.ADAPTER_CUT_Z, p.COLLAR_DEPTH + 2.0)


def _adapter_rail(side):
    """The beam that carries a cut short wall's hinges once the collar under
    them is gone.  None for any wall that does not need one.

    A cut long wall needs nothing: its stations stand clear of the window, so
    those beams keep their collar feet.  A cut short wall loses both of its --
    the wall is 84.5 long, the window is 66.5 of it -- and what is still
    standing forward of the cut plane there is the shroud.  So the rail is that
    shroud, thickened to ADAPTER_RAIL_T over this wall and the outer part of
    its two corners, and
    still sheathing the collar outside the window where that survives, which is
    what actually roots it.  It gives a 12 x 11.5 mm section running in from
    each corner, the stiffest part of the frame, to the hinge beam it carries --
    but not on across the middle; see `adapter_rail_gaps`.

    How deep it may reach is a question the shroud already answers, so it is
    built by `_shroud` itself at the greater thickness rather than re-derived
    here.  That matters most at the ends: the rail wraps the corners, where the
    limit belongs to the *neighbouring* wall's leaf, and getting the corner step
    wrong is the mistake revision 10 already made once.

    Clipping is at the neighbouring walls' leaf reach, which is where their own
    depth steps stop and the rail's full-depth corner begins.  It used to be
    the corner arc's start, 7.5 mm further round, but all that bought was a
    band of full-thickness rail cut down to the neighbour's corner step -- and
    it stood exactly where that wall's hinge has its nut started on the screw
    tip, leaving 3.3 mm to do it in.  Inside the reach the ordinary shroud is
    left standing at that same step.

    Its corners are kept at full depth rather than levelled like the shroud's:
    here that corner is the rail's own root, not a fin.
    """
    about, _, _, sign, _ = _axis_frame(side)
    if not _is_cut(side) or about != "Y":
        return None
    keep = max(_leaf_reach(s) for s in ("top", "bottom"))
    big = 400.0
    half_space = (cq.Workplane("XY").box(big, big, big)
                  .translate((sign * (keep + big / 2.0), 0, 0)))
    return (_shroud(p.ADAPTER_RAIL_T, sector_forks=True, level_corners=False)
            .intersect(half_space))


def adapter_rail_gaps(side):
    """Open space between a cut short wall's hinge beams, forward of the cut
    plane.  Empty for any wall without a rail.

    The rail used to bridge the window from corner to corner, and between the
    two beams that left a solid 12 x 11.5 mm bar starting exactly where the
    FRAME_HINGE_FASTENER_R channels stop.  A 20 mm screw's tip reaches about
    0.15 mm past the channel end, so the bar stood in the way of the nyloc going
    on at all, and out there in front of the plate it also fouled the tripod
    head.  It carried nothing: each beam hangs off its own corner through the
    rest of the rail, rooted in the collar sheath outside the window.

    So everything forward of the cut plane between the beams' inner faces goes,
    the ordinary shroud included -- it is still inside the nyloc's corners.
    The price is shroud over this stretch, which leaks light with that door
    open.  Stops at the cut plane so it never reaches a blocked window's fill.

    That alone left the rail's own ends behind: from each beam's inner face in
    to its knuckle the rail still wrapped the fastener channel, a tube standing
    forward of the beam with nothing on its free end -- the same kind of stub
    `_hinge_block` already cuts out of the beams, and for the same reason.  So
    over that band the rail follows the beam's rule too and stops dead at the
    channel's rear tangent plane, leaving the flat plate behind it.  Only on
    the gap side of each knuckle: on the corner side that same wrap is what
    carries the knuckle out to the rest of the rail.
    """
    about, _, va, sign, _ = _axis_frame(side)
    if not _is_cut(side) or about != "Y":
        return []
    face = _light_face(side)
    beam = p.FRAME_HINGE_BEAM_W / 2.0
    core = p.HINGE_CENTER_W / 2.0
    z_step = va + p.FRAME_HINGE_FASTENER_R
    borne = sorted(s for s in _stations(about) if _rail_borne(side, s))
    gaps = []
    for a, b in zip(borne, borne[1:]):
        for half, z1 in ((beam, p.ADAPTER_CUT_Z), (core, z_step)):
            lo, hi = a + half, b - half
            if hi > lo:
                gaps.append(_wall_box(side, lo, hi, face, face + sign * 60.0,
                                      -60.0, z1))
    return gaps


def _adapter_fill(side, collar):
    """What closes a blocked window: the wall it would otherwise have had.

    The collar wall and front lip, out of the plain collar, and the ordinary
    FRAME_SHROUD_T shroud sheathing them -- not the rail, whose 12 mm over the
    window would be a slab with no job to do.  Both only inside the window's
    own box, so the fill starts at the cut plane and the beams on a short wall
    stand on it rather than overhanging the window.

    The shroud has its fork slots taken as swept sectors.  The full-turn slots
    it cuts by default reach 9.2 mm from the hinge axis, well rearward of the
    cut plane on a short wall, and would notch a light leak straight through
    the fill at each fork.
    """
    box = _adapter_cut(side)
    return collar.intersect(box).union(_shroud(sector_forks=True).intersect(box))


def _adapter_leaf_relief(side):
    """Pulls a cut wall's closed leaf back out of the plate's footprint.

    LIGHT_TRAP_OVERLAP leaves the lap standing
    LIGHT_TRAP_OVERLAP - WALL - XY_CLEARANCE/2 = 0.25 mm proud of the light's
    face, which is little but is still enough to hold the plate off.  Over the
    window the lap is lapping a front face that has been cut away in any case,
    so pulling it back to ADAPTER_LEAF_RELIEF inboard of the face costs nothing
    that was working.
    """
    about, _, va, sign, _ = _axis_frame(side)
    lo, hi = _adapter_band(side)
    start = _light_face(side) - sign * p.ADAPTER_LEAF_RELIEF
    return _wall_box(side, lo, hi, start, start + sign * 60.0, va - 30.0, va + 30.0)


def _relief_reaches_forks(side):
    """Does a cut wall's leaf relief cross that wall's own fork webs?

    True on a cut short wall, whose stations sit at |y| 23 against a 33.25
    half-band, and false on a cut long wall, whose stations stand at |x| 55
    well outside it.  The same split as `_rail_borne`, and for the same reason:
    the window is cut in a 84.5 mm wall on one side and a 165.5 mm wall on the
    other, so it swallows the short wall's hinges and misses the long wall's.
    """
    if not _is_cut(side):
        return False
    lo, hi = _adapter_band(side)
    off = p.HINGE_CENTER_W / 2 + p.HINGE_AXIAL_GAP + p.HINGE_FORK_W / 2
    half = p.DOOR_HINGE_ROOT_W / 2
    return any(c + half > lo and c - half < hi
               for station in _stations(_axis_frame(side)[0])
               for c in (station - off, station + off))


def _relieved_leaf_root(side, root):
    """The edge a wall's fork webs actually have to root on.

    Normally the lap's own edge, LIGHT_TRAP_OVERLAP inside the frame's outer
    edge.  Over an adapter window the lap is pulled back to
    ADAPTER_LEAF_RELIEF inboard of the light's face instead, and where that
    reaches the forks they have to follow it or they root on an edge that is
    no longer there.

    Rooting them 1.75 mm outboard of it is not a small gap but a severance,
    because _adapter_leaf_relief is a box running from the light's face
    *outward*: everything of the door's standing out there goes with the lap.
    That is what happened to the right door, which came out a bare leaf with
    all four webs, barrels and saddles cut off it -- and passed every check,
    because a bare leaf is still one solid and collides with nothing.
    """
    if not _relief_reaches_forks(side):
        return root
    return _light_face(side) - _axis_frame(side)[3] * p.ADAPTER_LEAF_RELIEF


def adapter_plate_envelope(side):
    """The seated plate as a solid, for the assembly checks.

    Its own footprint, not the window's, and measured from the light's face --
    the surface it seats on -- so the checks are against the part rather than
    against the clearance that was cut for it.
    """
    sign = _axis_frame(side)[3]
    c = p.ADAPTER_CUT_CENTER.get(side, 0.0)
    half = p.ADAPTER_PLATE_L / 2.0
    face = _light_face(side)
    z0 = p.ADAPTER_PLATE_FRONT_Z
    return _wall_box(side, c - half, c + half,
                     face, face + sign * p.ADAPTER_PLATE_T,
                     z0, z0 + p.ADAPTER_PLATE_W)


def add_frame_hinges(model):
    collar = model
    model = model.union(_shroud())
    for side in p.ADAPTER_CUT_SIDES:
        rail = _adapter_rail(side)
        if rail is not None:
            model = model.union(rail)
    for side in ("top", "bottom", "left", "right"):
        about = _axis_frame(side)[0]
        for station in _stations(about):
            model = model.union(_hinge_block(side, station))
    # The adapter window after all of that, because all of it is in the way,
    # and the gap between a short wall's hinges with it.  A blocked window then
    # gets its wall back -- after the cut, so the cut takes the rail and the
    # fill puts back only the wall.
    for side in p.ADAPTER_CUT_SIDES:
        model = model.cut(_adapter_cut(side))
        for gap in adapter_rail_gaps(side):
            model = model.cut(gap)
        if adapter_blocked(side):
            model = model.union(_adapter_fill(side, collar))
    # Hardware clearance last, so it applies to the shroud, the beams and any
    # fill alike.
    for side in ("top", "bottom", "left", "right"):
        for station in _stations(_axis_frame(side)[0]):
            for cut in _hardware_cuts(side, station):
                model = model.cut(cut)
    return model


def _panel_rib_from_polygon(pts, z0):
    panel = cq.Workplane("XY").polyline(pts).close().extrude(p.DOOR_T).translate((0, 0, z0))
    rib = (cq.Workplane("XY").polyline(pts).close().offset2D(-p.DOOR_RIB_W)
           .extrude(p.DOOR_T + p.DOOR_RIB_H).translate((0, 0, z0)))
    inner = (cq.Workplane("XY").polyline(pts).close().offset2D(-2 * p.DOOR_RIB_W)
             .extrude(p.DOOR_T + p.DOOR_RIB_H + 0.2).translate((0, 0, z0 - 0.1)))
    return panel.union(rib.cut(inner))


def _leaf_side_half_space(about, ua, sign, big=400.0):
    """Everything on the leaf's side of the hinge axis plane."""
    box = cq.Workplane("XY").box(big, big, big)
    return (box.translate((0, ua - sign * big / 2, 0)) if about == "X"
            else box.translate((ua - sign * big / 2, 0, 0)))


def _door_forks(model, side, root_u):
    """The door's fork knuckles and the webs that carry them to the leaf.

    Revision 11.  The web used to run from the leaf root only as far as the
    barrel's tangent plane.  A plane tangent to a circle meets it along a line
    of zero area, so the knuckle never fused to the web at all: every door came
    out as a leaf plus four loose 125 mm3 rings, and a printed one would have
    had a crack the length of the joint waiting to split along the layers.

    Two things fix it.  The web now runs through to the hinge axis, so it
    engulfs the barrel instead of butting it; and a saddle -- the outboard half
    of a slightly fatter cylinder on the same axis -- carries material over the
    whole of the ring's outer face rather than one line of it.

    The saddle costs nothing in clearance because of what it is.  Being
    concentric with the hinge axis it is a surface of revolution, so it keeps
    the same DOOR_HINGE_SADDLE_CLEAR gap inside the frame's FRAME_HINGE_FASTENER_R
    channel at every door angle, exactly as the shroud tip does against the leaf
    root.  Nothing on the frame has to know about it.
    """
    about, ua, va, sign, _ = _axis_frame(side)
    r = p.HINGE_OD / 2
    saddle_r = p.FRAME_HINGE_FASTENER_R - p.DOOR_HINGE_SADDLE_CLEAR
    off = p.HINGE_CENTER_W / 2 + p.HINGE_AXIAL_GAP + p.HINGE_FORK_W / 2
    half_fork = p.HINGE_FORK_W / 2
    half_root = p.DOOR_HINGE_ROOT_W / 2
    tangent = ua - sign * r
    centres = [station + d
               for station in _stations(about) for d in (-off, off)]
    leaf_side = _leaf_side_half_space(about, ua, sign)

    for c in centres:
        model = model.union(_axis_cylinder(about, ua, va, c, r, p.HINGE_FORK_W))
        model = model.union(
            _axis_cylinder(about, ua, va, c, saddle_r, p.HINGE_FORK_W)
            .intersect(leaf_side))
        # Fork-width in as far as the axis, flaring only once clear of the
        # barrel -- inside it the slot the web passes through is parallel-sided.
        pts = [(c - half_fork, ua), (c + half_fork, ua),
               (c + half_fork, tangent), (c + half_root, root_u),
               (c - half_root, root_u), (c - half_fork, tangent)]
        if about == "Y":
            pts = [(u, a) for a, u in pts]
        model = model.union(cq.Workplane("XY").polyline(pts).close()
                            .extrude(p.DOOR_HINGE_WEB_H)
                            .translate((0, 0, va - p.DOOR_HINGE_WEB_H / 2)))

    # The bore comes out of the finished fork, not out of the ring on its own:
    # the web and saddle now cross the bolt axis, so cutting it any earlier
    # would just have it filled back in.
    for c in centres:
        model = model.cut(_axis_cylinder(about, ua, va, c, p.HINGE_BORE_D / 2,
                                         p.HINGE_FORK_W + 0.6))
    return model


def build_door(side):
    """Build a door in its assembled, fully-closed position.

    Closed leaves lie in planes through their own forward hinge axes.  The top,
    bottom and side axes are staggered in Z, so closed leaves stack without
    colliding.  Opening is a 90-degree rotation away from the diffuser.

    A leaf on a wall with an adapter window gets its lap relieved over the
    window -- see _adapter_leaf_relief.  That relief goes in before the forks
    rather than after, because it is a box running from the light's face
    outward and the forks stand out there: applied last it does not relieve
    them, it deletes them.  The webs then root on the relieved edge, which is
    what _relieved_leaf_root is for.
    """
    ow, oh = frame_dims()
    if side in ("top", "bottom"):
        _, _, z = hinge_axis(side)
        z0 = z - p.DOOR_T / 2
        s = 1 if side == "top" else -1
        root = s * (oh / 2 - p.LIGHT_TRAP_OVERLAP)
        tip_y = root - s * p.TOP_BOTTOM_DEPTH
        wb, wt = p.TOP_BOTTOM_BASE_W, p.TOP_BOTTOM_TIP_W
        pts = [(-wb/2, root), (wb/2, root), (wt/2, tip_y), (-wt/2, tip_y)]
    else:
        x, _, z = hinge_axis(side)
        z0 = z - p.DOOR_T / 2
        s = 1 if side == "right" else -1
        root = s * (ow / 2 - p.LIGHT_TRAP_OVERLAP)
        tip_x = root - s * p.SIDE_DEPTH
        hb, ht = p.SIDE_BASE_H, p.SIDE_TIP_H
        pts = [(root, -hb/2), (root, hb/2), (tip_x, ht/2), (tip_x, -ht/2)]

    model = _panel_rib_from_polygon(pts, z0)
    if _is_cut(side):
        model = model.cut(_adapter_leaf_relief(side))
    return _door_forks(model, side, _relieved_leaf_root(side, root))
