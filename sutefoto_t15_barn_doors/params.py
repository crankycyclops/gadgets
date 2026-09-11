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
# Bottom, top and left/right each get their own layer so all four leaves can
# close at once; left and right share one because they do not meet in the
# middle.  Revision 12 no longer sets them by hand -- the tripod adapter window
# is what decides how far forward they have to sit -- so they are derived at the
# foot of this file, under "Tripod adapter window".  The revision 11 values
# were HINGE_Z_TOP -4.5, HINGE_Z_BOTTOM -8.3, HINGE_Z_SIDE -12.1.

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

# --------------------------------------------------------------------------
# Tripod adapter window (revision 12)
#
# The light carries a 1/4-20 socket on one short side and one long side, and the
# quick-release plate that screws into either one has to seat flush on the
# light's own face.  Nothing in the collar is inboard of that face -- the cavity
# wall starts XY_CLEARANCE/2 outboard of it -- so there is no material to
# relieve down to and "flush" means the frame has to be absent over the plate's
# whole footprint.  Hence a window in each mounting wall.
#
# The window alone would have cost the short-side door.  That wall is only 84.5
# long, the window is 66.5 of it, and both of that side's hinge beams sit inside
# it (stations +-23, beams 24 wide, so |y| 11-35 against a 33.25 half-band): the
# beams lose the collar they root in, and with the axis at revision 11's -12.1
# the knuckle and its M3 stack sit inside the plate's footprint outright.
#
# What buys the door back is moving the hinge planes forward, and it is nearly
# free.  A leaf only ever sweeps the half-space forward of its own axis, so once
# the axis is forward of the plate's front edge the plate falls outside the
# swept sector and the door keeps all FRAME_HINGE_MAX_OPEN degrees -- on the
# long wall as well, which at -4.5 would otherwise have stopped against the
# plate at 42.  And it costs nothing in light control: shroud depth is
# |HINGE_Z| + 5.37 against an open-door gap of |HINGE_Z| + 7.8, so the unblocked
# residual stays 2.43 mm however far forward the axis goes, and the coverage
# ratio improves slightly.  The price is depth -- about 5.8 mm more standoff
# between the light and the closed doors -- which is the trade this revision
# makes deliberately.
# --------------------------------------------------------------------------

# Plate footprint.  ADAPTER_PLATE_L runs along the wall; ADAPTER_PLATE_W runs
# across it, into the light's depth.
ADAPTER_PLATE_L = 63.5             # 2 1/2 in
ADAPTER_PLATE_W = 47.63            # 1 7/8 in
# Only used by the validator's footprint check; the window is cut from the
# light's face outward regardless, so nothing in the frame depends on it.
ADAPTER_PLATE_T = 10.0

# MEASURE THESE TWO.  They are the only inputs to where the cut plane lands, and
# both are currently read off the photographs to about +-1.5 mm.  Everything
# else in this block, the hinge planes included, is derived from them, so a
# caliper on these two numbers is worth more than any other change in this file.
#
#   ADAPTER_SOCKET_Z   light's front (diffuser) face -> socket axis, along depth
#   ADAPTER_STUD_EDGE  plate's stud axis -> nearer plate edge, across the plate
#                      (ADAPTER_PLATE_W / 2 if the stud is centred, which is how
#                      it reads in adapter.jpg)
ADAPTER_SOCKET_Z = 11.0
ADAPTER_STUD_EDGE = ADAPTER_PLATE_W / 2.0

# Which walls get a window.  In this model's names the short (78 mm) walls are
# "left"/"right" and the long (159 mm) walls are "top"/"bottom" -- the opposite
# of how you would describe the light.  ("right", "top") is the light held front
# face towards you with the mounting short edge down and the long-side socket on
# your left; if it prints mirrored, the fix is ("right", "bottom").
ADAPTER_CUT_SIDES = ("right", "top")
# Where the socket sits along each wall, from the wall's centre.  Both read as
# centred; the short wall has only +-9 mm of room to be wrong in.
ADAPTER_CUT_CENTER = {"right": 0.0, "top": 0.0}

# Fill a window back in, for when that socket is not in use and the window is
# only letting light out.  By the light's own long and short sides, not the
# model's names, and applied to whichever long/short wall ADAPTER_CUT_SIDES
# lists.
#
# A blocked window is still a cut side as far as everything else is concerned:
# the hinge planes and the door leaf reliefs are derived from ADAPTER_CUT_SIDES
# alone.  So switching a block on or off changes the frame and nothing else, and
# the same set of printed doors fits either frame.  Taking the side out of
# ADAPTER_CUT_SIDES instead would move the hinge planes back and the doors with
# them.
ADAPTER_BLOCK_LONG = True
ADAPTER_BLOCK_SHORT = False

# Slack on the window.  Along the wall this also absorbs the ~1.6 mm the stud
# reads off-centre along the plate's 2 1/2 in axis; across it, it comes straight
# off the hinge planes below, so it is kept tighter.
ADAPTER_CUT_CLEAR = 1.5
ADAPTER_CUT_Z_CLEAR = 0.75

# Front edge of the seated plate, and the plane the frame has to stop at.
ADAPTER_PLATE_FRONT_Z = FRONT_LIP + ADAPTER_SOCKET_Z - ADAPTER_STUD_EDGE
ADAPTER_CUT_Z = ADAPTER_PLATE_FRONT_Z - ADAPTER_CUT_Z_CLEAR

# Margin between the cut plane and the rearmost hinge feature on a cut wall.
# This is where the +-1.5 mm on the two measurements above gets absorbed.
ADAPTER_HINGE_CLEAR = 1.5

# Beam that carries a cut short wall's hinges once the collar under them is
# gone: the shroud over that wall, thickened from FRAME_SHROUD_T to this.
#
# Taken flush with the hinge beams' own outboard face rather than picked.  The
# axis stands HINGE_OD/2 + HINGE_RADIAL_GAP off the frame's outer edge and the
# beam carries HINGE_OD/2 + FRAME_HINGE_SADDLE_T of saddle past it, so this is
# the whole radial depth the beams already occupy -- which makes the rail and
# the two beams read as one continuous member instead of two blocks perched on
# a ledge.  At 6.0 the rail was 69 mm2 in section against the 171-208 mm2
# revision 9 put between barrel and frame; flush it is 138 mm2 over the window
# and 374 mm2 where it roots outside it, and that is the difference between the
# hinges standing on something and standing on nothing.
ADAPTER_RAIL_T = HINGE_OD + HINGE_RADIAL_GAP + FRAME_HINGE_SADDLE_T

# How far the closed leaf's LIGHT_TRAP_OVERLAP lap is pulled back over the
# window.  The lap stands LIGHT_TRAP_OVERLAP - WALL - XY_CLEARANCE/2 = 0.25 mm
# proud of the light's face, which is enough to foul the plate, and over the
# window it laps a front face that is no longer there anyway.
ADAPTER_LEAF_RELIEF = 1.5

# Pitch of the closed-leaf stack: leaf thickness plus a running gap.
LEAF_STACK_PITCH = DOOR_T + DOOR_RIB_H + 0.4

_CUT = set(ADAPTER_CUT_SIDES)

# How far forward a cut wall's axis has to sit, per what that wall actually puts
# inside the plate's footprint.
#
# A cut long wall puts only its leaf there -- the hinge stations are at |x|
# 43-67, well outside the window -- and the leaf root is relieved, so all that
# is left is the angular condition: the plate has to fall outside the swept
# sector, which needs the axis forward of the plate's front edge by enough to
# clear FRAME_HINGE_DOOR_ANGLE_CLEAR at the plate's inboard front corner.  One
# millimetre covers it (the corner stands 8.05 mm off the axis, and 8.05*tan 4
# = 0.56).
#
# A cut short wall puts the centre knuckle and the whole M3 stack there, so it
# needs the full FRAME_HINGE_FASTENER_R channel clear of the cut plane.
_LONG_LIMIT = ADAPTER_PLATE_FRONT_Z - 1.0 - ADAPTER_HINGE_CLEAR
_SHORT_LIMIT = ADAPTER_CUT_Z - FRAME_HINGE_FASTENER_R - ADAPTER_HINGE_CLEAR

HINGE_Z_TOP = min(-4.5, _LONG_LIMIT) if "top" in _CUT else -4.5
HINGE_Z_BOTTOM = min(-8.3, _LONG_LIMIT) if "bottom" in _CUT else -8.3
# The sides take the most forward layer of the stack.  They have to clear the
# nearer long wall's leaf by a full pitch whether or not a short wall is cut,
# and clear the cut plane themselves if one is.
HINGE_Z_SIDE = min(HINGE_Z_TOP, HINGE_Z_BOTTOM) - LEAF_STACK_PITCH
if _CUT & {"left", "right"}:
    HINGE_Z_SIDE = min(HINGE_Z_SIDE, _SHORT_LIMIT)

# Clearance used by the assembly validator.
COLLISION_EPS = 0.02
