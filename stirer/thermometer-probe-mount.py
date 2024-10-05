length = 34.54
width = 15
height = 23
probeRadius = 1.7
filletRadius = 3.2
thickness = filletRadius * 2 + 0.1 # The thickness must be greater than filletRadius * 2

#r = cq.Workplane("front").hLine(length)
#r = (
#    r.vLine(thickness).hLine(-0.25).vLine(-0.25).hLineTo(0.0)
#)  # hLineTo allows using xCoordinate not distance

# hLineTo allows using xCoordinate not distance
r = cq.Workplane("front").hLine(length)\
    .vLine(height)\
    .hLine(-thickness)\
    .vLine(-height + thickness)\
    .hLineTo(0.0)

result = r.mirrorY().extrude(width)  # mirror the geometry and extrude

# This adds the rounded inner edges for the bracket to sit comfortably
# on top of the stirer
result = result.edges("|Z and <<Y[-2]").fillet(filletRadius)

# This just rounds the top to make it smoother to the touch
result = result.edges("|Z and <Y").fillet(1)