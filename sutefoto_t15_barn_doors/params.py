"""Shared dimensions for SUTEFOTO T15 barn doors, revision 6 (mm).

The frame fit/corner parameters intentionally retain the familiar names so prior
fit tuning can be copied over.  The hinge axes are now moved forward of the
front face and staggered by side so all four doors can close over the diffuser
without occupying the same plane.
"""

LIGHT_W = 159.0
LIGHT_H = 78.0
LIGHT_D = 23.0

# Frame fit -- copy your tuned values here if you changed them previously.
#XY_CLEARANCE = 0.60
XY_CLEARANCE = 1.1
COLLAR_DEPTH = 8.0
FRONT_LIP = 1.8
WALL = 2.7
APERTURE_OVERLAP = 3.0
#CORNER_RADIUS_BODY = 5.0
CORNER_RADIUS_BODY = 9.6
CORNER_RADIUS_OUTER = CORNER_RADIUS_BODY + WALL

# Through-bolt friction hinges.
HINGE_OD = 8.0
HINGE_BORE_D = 3.3
# Width of the frame-side centre knuckle.  This also sets how wide the beam can
# be where it actually grips the barrel, so it is the single most important
# number for hinge strength.  The door forks are positioned from it.
HINGE_CENTER_W = 8.0
HINGE_FORK_W = 3.0
HINGE_AXIAL_GAP = 0.35
HINGE_RADIAL_GAP = 0.8
HORIZONTAL_HINGE_STATIONS = (-55.0, 55.0)
VERTICAL_HINGE_STATIONS = (-23.0, 23.0)
# Stack under the head: HINGE_CENTER_W + 2*HINGE_AXIAL_GAP + 2*HINGE_FORK_W
# = 14.7, plus two flat washers and an M3 nyloc.
HINGE_SCREW_LENGTH = 20.0

# Hinge planes measured from the frame front face (negative Z is forward).
# Top is closest to the light; bottom is the second closed layer; left/right
# share the third layer because they do not meet in the middle.
HINGE_Z_TOP = -4.5
HINGE_Z_BOTTOM = -8.3
HINGE_Z_SIDE = -12.1

# Frame-side hinge buttress.  Revision 9 replaces the old tapered web -- which
# was only HINGE_CENTER_W wide and rooted 2 mm into the wall, and duly peeled
# off the frame -- with a solid beam standing on the outside of the collar.
# Axial width of the beam where it meets the frame.  It necks down to
# HINGE_CENTER_W only in the last few mm around the barrel, because that is the
# only place the door forks need the room.
FRAME_HINGE_BEAM_W = 24.0
# How far the beam roots into the frame wall.  Must stay under WALL so it never
# breaks into the light cavity.
FRAME_HINGE_ROOT_DEPTH = 2.2
# Plastic carried around the outboard side of the barrel.
FRAME_HINGE_SADDLE_T = 3.2
# Coaxial channel bored through the beam either side of the centre knuckle.
# Sized to what actually has to fit and no more, because this channel also cuts
# through the light shroud: door fork barrels (r 4.0 plus running clearance), an
# M3 washer (r 3.5), an M3 nyloc across corners (r 3.2).  Every 0.1 mm here
# costs shroud -- going from 5.5 to 4.6 returned 593 mm3 of it.
FRAME_HINGE_FASTENER_R = 4.6
# How far the leaves must swing.  The frame's hinge slot is cut for exactly this
# much travel, so this is also what stops the doors -- past it the leaf meets the
# beam.  Barn doors need to fold well back, so this is 180; the cost is only in
# the beam's minimum section (171 mm2 at 135 degrees, 128 mm2 at 180), against
# 4.6 mm2 in the revision 8 design that peeled off.
FRAME_HINGE_MAX_OPEN = 180.0
# Slack added either end of that travel.  Angular rather than linear: the doors
# turn about the barrel axis, so an angle is what actually separates them.
FRAME_HINGE_DOOR_ANGLE_CLEAR = 4.0
# Radial truncation of the door-leaf sweep used for the clearance cut.  Only has
# to exceed the beam's own reach from the hinge axis (~22 mm worst case).
FRAME_HINGE_SWEEP_REACH = 40.0

# Light shroud (revision 10).  With a leaf open, the gap between the frame's
# front face and the leaf root is |HINGE_Z| + 7.8 -- 12.3 mm at the top, 19.9 mm
# at the sides -- and light pours straight out of it.  A wall standing forward
# from the outer edge closes most of that.  What makes it work at every door
# angle rather than only at 90 is its tip: an arc concentric with the hinge axis,
# just inside the circle the leaf root sweeps.  Both are then surfaces of
# revolution about the axis, so their separation never changes as the door turns.
FRAME_SHROUD_T = 2.4
# Radial gap between the shroud tip and the circle the leaf root sweeps.  This
# is the residual leak, and it is the same at every angle.
FRAME_SHROUD_CLEAR = 0.6
# Axial gap either side of a door fork where it passes through the shroud.
FRAME_SHROUD_FORK_CLEAR = 0.6

DOOR_HINGE_ROOT_W = 11.0
DOOR_HINGE_ROOT_DEPTH = 10.0
DOOR_HINGE_WEB_H = 5.2
# Revision 11.  The web used to stop at the barrel's tangent plane, which meets
# the knuckle along a line of zero area: the two never fused, and every door
# exported as a leaf plus four loose rings.  The web now runs through to the
# hinge axis and a saddle carries material over the whole outboard half of the
# knuckle.  The saddle is a cylinder concentric with the hinge axis, so like the
# shroud tip it is a surface of revolution -- its clearance inside the frame's
# FRAME_HINGE_FASTENER_R channel is the same at every door angle, which is what
# lets it be added without touching the frame.  This is the radial part of that
# clearance; the saddle radius is FRAME_HINGE_FASTENER_R minus it.
DOOR_HINGE_SADDLE_CLEAR = 0.3

# Door leaves.
DOOR_T = 2.4
DOOR_RIB_H = 1.0
DOOR_RIB_W = 3.0
TOP_BOTTOM_DEPTH = 65.0
SIDE_DEPTH = 56.0
TOP_BOTTOM_BASE_W = 154.0
TOP_BOTTOM_TIP_W = 144.0
SIDE_BASE_H = 74.0
SIDE_TIP_H = 64.0

# The closed leaf extends this far inward past the outer frame edge.  When the
# door is opened 90 degrees this same portion becomes a light-trap skirt over
# the frame/door gap, preventing a direct leak path.
LIGHT_TRAP_OVERLAP = 3.0

# Clearance used by the assembly validator.
COLLISION_EPS = 0.02
