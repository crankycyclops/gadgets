length = 34.54
width = 15
height = 23
thickness = 5
filletRadius = 1.7

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

result = result.edges("|Z").fillet(filletRadius)