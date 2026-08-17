"""Shared dimensions for the SUTEFOTO T15 barn-door system (millimetres).

Nominal light dimensions are 159 x 78 x 23 mm. The fit values below are
intentionally easy to tune after a small test print.
"""

# SUTEFOTO T15 nominal body dimensions
LIGHT_W = 159.0
LIGHT_H = 78.0
LIGHT_D = 23.0

# Collar / frame fit
XY_CLEARANCE = 0.60       # total extra size around the light body
COLLAR_DEPTH = 8.0        # how far the frame grips the front edge of the light
FRONT_LIP = 1.8           # front flange thickness
WALL = 2.7                # nominal outer wall
APERTURE_OVERLAP = 3.0    # frame overlaps diffuser/bezel from each edge

# Controls how rounded the corners are
#CORNER_RADIUS_BODY = 5.0
#CORNER_RADIUS_OUTER = 7.0
CORNER_RADIUS_BODY = 9.6
#CORNER_RADIUS_OUTER = 10.6
CORNER_RADIUS_OUTER = CORNER_RADIUS_BODY + WALL

# Adjustable friction-hinge geometry.
# Each hinge station is a simple through-bolt stack:
# M3 screw -> washer -> door fork -> frame knuckle -> door fork -> washer -> nyloc.
# Tighten the nyloc until the door moves with deliberate hand pressure and stays put.
HINGE_OD = 8.0
HINGE_BORE_D = 3.3        # clearance bore; friction comes from axial clamping, not bore fit
HINGE_CENTER_W = 5.0
HINGE_FORK_W = 3.0
HINGE_AXIAL_GAP = 0.35
HINGE_RADIAL_GAP = 0.80  # physical gap between frame/door edge and hinge barrel
HORIZONTAL_HINGE_STATIONS = (-55.0, 55.0)
VERTICAL_HINGE_STATIONS = (-23.0, 23.0)
HINGE_SCREW_LENGTH = 20.0 # recommended M3 x 20 mm through-bolt

# Barn-door leaves
DOOR_T = 2.2
DOOR_RIB_H = 1.0
DOOR_RIB_W = 3.0
TOP_BOTTOM_DEPTH = 65.0
SIDE_DEPTH = 56.0
TOP_BOTTOM_BASE_W = 154.0
TOP_BOTTOM_TIP_W = 144.0
SIDE_BASE_H = 74.0
SIDE_TIP_H = 64.0
