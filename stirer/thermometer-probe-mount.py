length = 34.54
width = 15
height = 23
probeRadius = 1.7
filletRadius = 3.2

probeHousingHeight = height / 2.5
thickness = filletRadius * 2 + 0.1 # The thickness must be greater than filletRadius * 2

# hLineTo allows using xCoordinate not distance
result = cq.Workplane("front").hLine(length / 2)\
    .vLine(height)\
    .hLine(-thickness)\
    .vLine(-height + thickness)\
    .hLineTo(0.0)

result = result.mirrorY().extrude(width)  # mirror the geometry and extrude

# This adds the rounded inner edges for the bracket to sit comfortably
# on top of the stirer
result = result.edges("|Z and <<Y[-2]").fillet(filletRadius)

# This just rounds the top to make it smoother to the touch
result = result.edges("|Z and <Y").fillet(1)

# Subtract a smaller cylinder to create the hole for the probe.
# This should have just enough clearance for a tight fit.
innerCylinder = cq.Workplane("XZ").cylinder(probeHousingHeight, probeRadius)\
    .translate((length / 2 + (probeRadius * 2) - (0.5 * probeRadius), height / 2, width / 2))

# Add the cylindrical housing for the probe
# Use probeRadius to size the cylinder
outerCylinder = cq.Workplane("XZ").cylinder(probeHousingHeight, probeRadius * 2)\
    .translate((length / 2 + (probeRadius * 2) - (0.5 * probeRadius), height / 2, width / 2))\
    .cut(innerCylinder)

snapInShortSide = probeRadius * 0.8
snapInLongSide = probeRadius * 1.2

# A small cutaway where we can push the probe into position
snapIn = cq.Workplane("XZ").moveTo(-probeRadius / 2, -probeRadius / 2)\
    .hLine(probeRadius + 0.2).vLine(probeRadius * 0.85)\
    .hLine(-probeRadius - 0.2).vLine(-probeRadius * 0.85)\
    .close()\
    .extrude(probeHousingHeight)\
    .translate((length / 2 + (probeRadius * 2) - (0.5 * probeRadius), height / 2, width / 2))\
    .translate((probeRadius * 1.5 - 0.2, probeHousingHeight / 2, 0))

outerCylinder = outerCylinder.cut(snapIn)

# Combine the bracket and the cylinder (attachment)
result = result.union(outerCylinder)

show_object(result)

# For some reason, cq-editor has the export options greyed out.
# For now, I just need to uncomment this when I need to export to STL. Grr.
#result.export("/home/james/Desktop/bracket.stl")