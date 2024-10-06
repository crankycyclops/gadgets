innerLength = 34.54
width = 15
height = 23
probeRadius = 1.8
filletRadius = 3.2

probeHousingHeight = height / 2.5
thickness = filletRadius * 2 + 0.1 # The thickness must be greater than filletRadius * 2

# This is to ensure that the length of the inside is exactly the value above
outerLength = innerLength + 2 * thickness

# Draws half the C-shaped bracket
result = cq.Workplane("front").hLine(outerLength / 2)\
    .vLine(height)\
    .hLine(-thickness)\
    .vLine(-height + thickness)\
    .hLineTo(0.0)

# Draws the other half of the C-shaped bracket
result = result.mirrorY().extrude(width)

# This adds the rounded inner edges for the bracket to sit comfortably
# on top of the stirer
result = result.edges("|Z and <<Y[-2]").fillet(filletRadius)

# This just rounds the top to make it smoother to the touch
result = result.edges("|Z and <Y").fillet(1)

# Subtract a smaller cylinder to create the hole for the probe.
# This should have just enough clearance for a tight fit.
innerCylinder = cq.Workplane("XZ").cylinder(probeHousingHeight, probeRadius)\
    .translate((outerLength / 2 + (probeRadius * 2) - (0.5 * probeRadius), height / 2, width / 2))

# Add the cylindrical housing for the probe. Use probeRadius
# to size the cylinder.
outerCylinder = cq.Workplane("XZ").cylinder(probeHousingHeight, probeRadius * 2)\
    .translate((outerLength / 2 + (probeRadius * 2) - (0.5 * probeRadius), height / 2, width / 2))\
    .cut(innerCylinder)

# This is the tighter inner width that the probe pushes into
snapInVLineInner = probeRadius * 0.9

# This is the outer width of the snap in for the probe
snapInVLineOuter = probeRadius * 1.2

# These are the X and Z components of the lines that connect
# snapInVLineInner and snapInVLineOuter
snapInHLineXComponent = probeRadius + 0.2
snapInHLineZComponent = (snapInVLineOuter - snapInVLineInner) / 2

# A small cutaway where we can push the probe into position
snapIn = cq.Workplane("XZ").moveTo(-probeRadius / 2, -probeRadius / 2)\
    .line(snapInHLineXComponent, -snapInHLineZComponent)\
    .vLine(snapInVLineOuter)\
    .line(-snapInHLineXComponent, -snapInHLineZComponent)\
    .vLine(-snapInVLineInner)\
    .close()\
    .extrude(probeHousingHeight)\
    .translate((outerLength / 2 + (probeRadius * 2) - (0.5 * probeRadius), height / 2, width / 2))\
    .translate((probeRadius * 1.5 - 0.2, probeHousingHeight / 2, 0))

outerCylinder = outerCylinder.cut(snapIn)

# Combine the bracket and the cylinder (attachment)
result = result.union(outerCylinder)

show_object(result)

# For some reason, cq-editor has the export options greyed out.
# For now, I just need to uncomment this when I need to export to STL. Grr.
#result.export("/home/james/Desktop/bracket.stl")