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
# Clears the door fork barrels (r 4.0), an M3 washer (r 3.5), an M3 nyloc across
# corners (r 3.2) and a 6 mm socket, so assembly is unchanged.
FRAME_HINGE_FASTENER_R = 5.5
# Slack added either end of the door's travel when cutting the slot it swings
# in.  Angular rather than linear: the doors turn about the barrel axis, so an
# angle is what actually separates them from the beam.  Past this the leaf meets
# the beam, which gives the door a natural end stop just outside 0 and 90.
FRAME_HINGE_DOOR_ANGLE_CLEAR = 4.0
# Radial truncation of the door-leaf sweep used for the clearance cut.  Only has
# to exceed the beam's own reach from the hinge axis (~22 mm worst case).
FRAME_HINGE_SWEEP_REACH = 40.0

DOOR_HINGE_ROOT_W = 11.0
DOOR_HINGE_ROOT_DEPTH = 10.0
DOOR_HINGE_WEB_H = 5.2

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
