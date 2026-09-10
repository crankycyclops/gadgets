"""Assembly checks.

Checks single solids, closed-door stacking, each door's complete sweep from
closed to FRAME_HINGE_MAX_OPEN against the frame, and -- revision 12 -- that a
seated tripod plate is clear of the frame and of every door at every angle.  A
tiny coincident-contact tolerance is ignored.

The plate checks are the point of revision 12 and neither is redundant.  The
frame one is what the window is *for*: the plate seats on the light's own face,
so any frame material left in its footprint holds it off, and 0.25 mm of leaf
lap is enough to do it.  The door one is what moving the hinge planes forward
bought: a leaf only sweeps the half-space forward of its own axis, so with the
axis forward of the plate the plate falls outside the swept sector and the door
keeps its full travel.  That argument is angular and easy to get backwards --
at revision 11's HINGE_Z_TOP of -4.5 the plate's inboard front corner sits at
222 degrees, squarely inside the sector, and the top door would have stopped
against it at 42 -- so it is worth checking rather than trusting.

The sweep runs to the full travel deliberately: revision 9's beam silently
capped the doors at 96 degrees, which no 0-90 check could ever have caught.

`isValid()` is not enough on its own, either.  A compound of disjoint solids is
perfectly valid, and that is exactly what the doors were up to revision 11: the
fork webs met their knuckles along a tangent line of zero area, never fused, and
each door exported as a leaf plus four loose rings.  So count the solids too.
"""
import cadquery as cq
import params as p
import frame, top_door, bottom_door, left_door, right_door
from common import hinge_axis, adapter_plate_envelope


def vol(a,b):
    x=a.intersect(b)
    return 0.0 if x.isNull() else x.Volume()


def rotate_door(solid, side, angle):
    x,y,z=hinge_axis(side)
    if side in ('top','bottom'):
        return solid.rotate(cq.Vector(x,y,z), cq.Vector(x+1,y,z), angle)
    return solid.rotate(cq.Vector(x,y,z), cq.Vector(x,y+1,z), angle)


def one_solid(shape, name):
    assert shape.isValid(), f'{name} is not a valid shape'
    n=len(shape.Solids())
    assert n==1, f'{name} is {n} disjoint solids, not one printable part'


def main():
    F=frame.build().val(); one_solid(F,'frame')
    doors={
        'top':top_door.build().val(), 'bottom':bottom_door.build().val(),
        'left':left_door.build().val(), 'right':right_door.build().val()}
    for s,d in doors.items(): one_solid(d,f'{s} door')

    # Closed doors must not collide with the frame or each other.
    for s,d in doors.items():
        v=vol(F,d)
        assert v < p.COLLISION_EPS, f'{s} closed/frame collision {v}'
    names=list(doors)
    for i,a in enumerate(names):
        for b in names[i+1:]:
            v=vol(doors[a],doors[b])
            assert v < p.COLLISION_EPS, f'closed {a}/{b} collision {v}'

    directions={'top':1, 'bottom':-1, 'left':1, 'right':-1}
    travel=int(p.FRAME_HINGE_MAX_OPEN)
    for s,d in doors.items():
        for deg in range(0,travel+1,3):
            moved=rotate_door(d,s,directions[s]*deg)
            v=vol(F,moved)
            assert v < p.COLLISION_EPS, f'{s} frame collision at {deg}: {v}'

    # A seated plate must be clear of the frame, and of every door at every
    # angle -- including the doors on the other three walls, which swing past
    # the corners near it.
    for side in p.ADAPTER_CUT_SIDES:
        plate=adapter_plate_envelope(side).val()
        v=vol(F,plate)
        assert v < p.COLLISION_EPS, f'{side} plate/frame clash {v}'
        for s,d in doors.items():
            for deg in range(0,travel+1,3):
                moved=rotate_door(d,s,directions[s]*deg)
                v=vol(plate,moved)
                assert v < p.COLLISION_EPS, \
                    f'{side} plate/{s} door clash at {deg}: {v}'
    sides=', '.join(p.ADAPTER_CUT_SIDES)
    print(f'PASS: five single solids; all doors stack closed and each clears the '
          f'frame through 0-{travel} degrees; a plate on {sides} clears the frame '
          f'and every door through the same travel')

if __name__=='__main__': main()
