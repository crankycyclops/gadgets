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
HINGE_CENTER_W = 5.0
HINGE_FORK_W = 3.0
HINGE_AXIAL_GAP = 0.35
HINGE_RADIAL_GAP = 0.8
HORIZONTAL_HINGE_STATIONS = (-55.0, 55.0)
VERTICAL_HINGE_STATIONS = (-23.0, 23.0)
HINGE_SCREW_LENGTH = 25.0

# Hinge planes measured from the frame front face (negative Z is forward).
# Top is closest to the light; bottom is the second closed layer; left/right
# share the third layer because they do not meet in the middle.
HINGE_Z_TOP = -4.5
HINGE_Z_BOTTOM = -8.3
HINGE_Z_SIDE = -12.1

# Strength of frame-to-center-knuckle and door-fork attachments.
FRAME_HINGE_GUSSET_Z = 2.2
FRAME_HINGE_ROOT_DEPTH = 2.0
FRAME_HINGE_ROOT_Z_OVERLAP = 5.2
FRAME_HINGE_WEB_THICKNESS = 8.0
FRAME_HINGE_BARREL_EMBED = 1.5
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
