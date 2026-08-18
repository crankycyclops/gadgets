"""Assembly checks for revision 6.

Checks valid solids, closed-door stacking, and each door's complete closed-to-open
90-degree sweep against the frame.  A tiny coincident-contact tolerance is ignored.
"""
import cadquery as cq
import params as p
import frame, top_door, bottom_door, left_door, right_door
from common import hinge_axis


def vol(a,b):
    x=a.intersect(b)
    return 0.0 if x.isNull() else x.Volume()


def rotate_door(solid, side, angle):
    x,y,z=hinge_axis(side)
    if side in ('top','bottom'):
        return solid.rotate(cq.Vector(x,y,z), cq.Vector(x+1,y,z), angle)
    return solid.rotate(cq.Vector(x,y,z), cq.Vector(x,y+1,z), angle)


def main():
    F=frame.build().val(); assert F.isValid()
    doors={
        'top':top_door.build().val(), 'bottom':bottom_door.build().val(),
        'left':left_door.build().val(), 'right':right_door.build().val()}
    for s,d in doors.items(): assert d.isValid(), s

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
    for s,d in doors.items():
        for deg in range(0,91,3):
            moved=rotate_door(d,s,directions[s]*deg)
            v=vol(F,moved)
            assert v < p.COLLISION_EPS, f'{s} frame collision at {deg}: {v}'
    print('PASS: valid solids; all doors stack closed and each clears the frame through 0-90 degrees')

if __name__=='__main__': main()
