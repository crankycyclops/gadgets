# SUTEFOTO T15 barn doors — Revision 10

Barn doors for a SUTEFOTO T15 pocket light. The collar-fit concept and the familiar fit parameter names carry over from revision 6, which moved the hinge axes forward of the light so the doors can close over the diffuser without striking the frame. Revision 9 reworked how the hinges are held on; revision 10 restored full door travel and added a light shroud.

> **Current status:** `validate_assembly.py` does not pass — see [Known issue](#known-issue). The frame itself builds as one valid solid.

## What changed

- **Fold-flat closing:** each door is modeled in its fully closed position and opens outward to `FRAME_HINGE_MAX_OPEN` (180°).
- **Closed-door stacking:** top, bottom, and side leaves use three slightly staggered Z planes so all four can be closed at once. Left/right share one plane because they do not meet in the center.
- **Light-leak control, closed:** each leaf overlaps the outer frame edge by `LIGHT_TRAP_OVERLAP`, so a closed leaf laps the frame's front face rather than butting it.
- **Light-leak control, open:** the frame carries a shroud around its whole outline — see [Revision 10](#revision-10--full-travel-and-the-light-shroud). The `LIGHT_TRAP_OVERLAP` lap does *not* double as an open-door skirt, as earlier notes here claimed; 3 mm of overlap cannot span a gap of 12–20 mm.
- **Stronger door hinges:** the fork knuckles use tapered 11 mm roots and 10 mm-deep reinforced webs.
- **No external clamp blocks:** the collar fit and front retaining lip hold the light, avoiding the protruding clamp-boss interference from earlier revisions.
- **Simple friction hardware:** M3 through-bolt + washers + nyloc nut. Tighten until the door takes deliberate hand pressure to move.

## Revision 9 — frame hinge buttress

The hinges used to peel off the frame. They were bridged to the collar by a tapered web only `HINGE_CENTER_W` (5 mm) wide, rooted 2 mm into a 2.7 mm wall. Printed with the collar's back face on the bed, the layer planes run straight through that junction, and the side hinges were cantilevering a 56 mm door off a 4.6 mm² sliver.

Each hinge now sits on a solid beam, `FRAME_HINGE_BEAM_W` (24 mm) wide, standing on the outside of the collar. In section it is an L: the base roots `FRAME_HINGE_ROOT_DEPTH` into the wall across the full collar depth, and everything forward of the front face stays outboard of the frame's outer edge. Its outboard face is parallel to the build direction, so it prints without overhang, and its full section lands exactly where the bending moment peaks.

Minimum section between barrel and frame:

| hinge | revision 8 | revision 9 | revision 10 |
|---|---|---|---|
| top | 9.5 mm² | 171 mm² | 206 mm² |
| bottom | 6.2 mm² | 171 mm² | 206 mm² |
| left / right | 4.6 mm² | 171 mm² | 208 mm² |

`HINGE_CENTER_W` also goes 5 mm → 8 mm, which is what sets how wide the beam can be where it actually grips the barrel. The door forks are positioned from it and move outboard to suit. **This changes the screw length — see below.**

The beam is built deliberately over-fat and then cut back by the volume the doors sweep, so clearance is derived rather than guessed, and the cut is a single swept sector rather than a stack of radial bands — bands leave a staircase of thin teeth down the slot edge. A coaxial channel of radius `FRAME_HINGE_FASTENER_R` either side of the centre knuckle clears the fork barrels, washers and nyloc.

The leaves were not modified. `LIGHT_TRAP_OVERLAP`, the leaf outlines and the hinge axes are all untouched, and no beam material intrudes forward of the front face inboard of the outer edge, so fold-flat closing and the closed-door light trap behave exactly as before.

## Revision 10 — full travel and the light shroud

**Travel.** Revision 9's beam silently capped the doors at 96°, because its slot was only cut for 0–90° of sweep. Barn doors need to fold well back, so `FRAME_HINGE_MAX_OPEN` is now 180°. `validate_assembly.py` now sweeps the full travel rather than a fixed 0–90°, which is what would have caught the cap in the first place.

Widening the slot to 180° costs section, but the beam's cut was also split in two to pay it back:

- across the **whole** beam, only the leaf's sweep is removed, and starting from the leaf's *root radius* rather than the barrel — the leaf is a thin plate that never comes nearer the axis than 7.8 mm, so cutting from the barrel on its account threw away a ring of plastic for nothing;
- the **forks** do reach the barrel, so their sweep is cut only over their own flared footprint.

Cutting the full beam width down to the barrel is what used to leave the saddle as a thin hook tapering to a point. Keeping it to the forks leaves a solid collar round the knuckle instead, and nets 206 mm² at 180° — better than revision 9 managed at 90°.

**The gap.** With a leaf open, the distance from the frame's front face to the leaf root is `|HINGE_Z| + 7.8` — 12.3 mm at the top, 16.1 at the bottom, 19.9 at the sides — and light poured straight out of it. Two things set it: the hinge axes sit forward of the front face (needed so all four leaves can stack when closed), and the leaf root has to stand 7.8 mm off its axis (barrel 4.0 + `HINGE_RADIAL_GAP` 0.8 + `LIGHT_TRAP_OVERLAP` 3.0).

Nothing flat can close that at more than one door angle. As a leaf turns, the only thing that holds still relative to the frame is a *surface of revolution about the hinge axis*. So each side's wall is taken as deep as the clearance cylinder concentric with its own hinge axis allows — that cylinder sits `FRAME_SHROUD_CLEAR` inside the circle the leaf root sweeps, which makes the running gap the same at every angle from 0 to 180 rather than only at 90.

The shroud is one wall following the frame's whole outline, standing forward from the front face and carried back over the collar's full depth rather than stopping at it — stopping at z = 0 would join it to the frame along the outer edge line only, a knife edge that is neither strong nor printable.

Three things matter to how much it covers:

- **The corners stay at full depth.** The leaves are narrower than the frame (|x| ≤ 77 against an 82.75 edge, |y| ≤ 37 against 42.25), so nothing sweeps the corners at any angle and there is nothing there to clear.
- **The depth limit is one flat step per side, not the cylinder itself.** Following the cylinder buys about 1.4 mm more depth on the outboard half of the wall and costs a tapered, pointed edge to get it. A flat bottom per side, set by the wall's *inboard* face — the part nearest the leaf — is simpler to print and to look at.
- **It applies only where a leaf can reach.** Trimming to the cylinder everywhere would also delete the wall between the front face and the *top* of that cylinder; on the sides the cylinder does not begin until z = −4.9, so a naive trim throws away 5.9 mm of wall along the whole run to clear a door that is never there.

Measured as blocked area against the raw gap: **74 %** overall — top 69 %, bottom 76 %, sides 76 %. What is left is the `FRAME_SHROUD_CLEAR` running gap plus the slots where the door forks pass through. Narrowing the fork flare (`DOOR_HINGE_ROOT_W`) to close those slots was measured and returns only 3 %, which is not worth weakening the door for.

**Assembly note:** `FRAME_HINGE_FASTENER_R` dropped 5.5 → 4.6 mm, because this channel cuts through the shroud as well as the beam and every 0.1 mm of it costs coverage. It still clears the fork barrels, an M3 washer and an M3 nyloc, but there is no longer room to bring a socket down the bolt axis past the shroud — hold the nyloc with a thin open-end spanner from the front instead.

## Keep your fit tuning

If you already tuned the old project, copy your preferred values for these into this `params.py`:

- `XY_CLEARANCE`
- `CORNER_RADIUS_BODY`
- `CORNER_RADIUS_OUTER` (or leave it derived as `CORNER_RADIUS_BODY + WALL`)
- `WALL` if you changed it

Do not copy old hinge-Z or clamp parameters.

## Hinge hardware

Each of 8 hinge stations uses:

`M3 screw -> washer -> door fork -> frame center knuckle -> door fork -> washer -> M3 nyloc`

Recommended starting hardware:

- 8 × M3 × **20 mm** socket-head screws
- 16 × M3 flat washers
- 8 × M3 nyloc nuts

**Screw length changed in revision 9.** The stack under the head is
`HINGE_CENTER_W + 2*HINGE_AXIAL_GAP + 2*HINGE_FORK_W` = 14.7 mm, plus two flat
washers (~1.0 mm) and an M3 nyloc (~4.0 mm) = **19.7 mm**. Revision 8's 16 mm
screws reached only 0.3 mm into the nut and will no longer work; use 20 mm.
Dropping the washers still needs 18.7 mm, so 20 mm is the length either way.

The modeled bore is 3.3 mm. Do not intentionally generate support inside it; clean with a 3.2–3.3 mm drill by hand if necessary.

## Validation

`validate_assembly.py` checks:

1. all five solids are valid;
2. all four doors can occupy their fully closed stacked positions simultaneously without solid intersection;
3. each door clears the frame through its complete closed-to-open sweep, all the way to `FRAME_HINGE_MAX_OPEN`.

The sweep runs to the full travel deliberately. Revision 9's beam capped the doors at 96° and no fixed 0–90° check could ever have caught it.

Run:

```bash
python validate_assembly.py
```

Output on success:

```text
PASS: valid solids; all doors stack closed and each clears the frame through 0-180 degrees
```

## Known issue

Check 2 currently fails:

```text
AssertionError: top closed/frame collision 0.06738828340566716
```

The closed top leaf's fork webs foul the frame by 0.067 mm³ at y = 42.25–42.35, right at the frame's outer face, in eight slivers around the four fork positions. The cause is in `_fork_slots` in `common.py`:

```python
far = near + flare * min(1.0, max(0.0, (rho - r) / (u_root - r)))
```

A fork web flares from `HINGE_FORK_W` at the barrel to `DOOR_HINGE_ROOT_W` at its root, and that flare finishes at the fork's own root radius (7.8 mm), staying constant beyond. But `rho` here is only how far the *cut* has to reach, and `_hinge_block` passes the beam's reach (24 mm) rather than 7.8. That stretches the taper over radius 4→24 instead of 4→7.8, so the slot comes out too narrow near the barrel. The hardware channel masks all of it except right at the outer face.

Holding the width constant past `u_root` instead of interpolating to `rho` clears this check, but on the geometry as it stands it exposes a second clash at 27° where the ring's inner face curves inboard around the corner fillet (to y = 40.36, a 6.69 mm standoff from the hinge axis instead of 4.8), which the one flat depth step per side does not account for. Both want fixing together.

The frame still builds as a single valid solid, so exports work; treat the doors' closed fit as unverified until this is resolved.

## CQ-Editor

Every part module exposes `build()` and can render directly in CQ-Editor — open it and click Run.

The four door modules and `fit_test_coupon.py` guard on `__main__`, falling back to STL export from the command line:

```python
if __name__ == "__main__":
    result = build()
    try:
        show_object(result)
    except NameError:
        cq.exporters.export(result, "top_door.stl")
```

`frame.py` and `assembly.py` instead look up `show_object` at module level:

```python
try:
    show_object
except NameError:
    ...
else:
    ...
```

Python resolves that name before evaluating anything else, so importing these modules costs nothing — `import frame` does not build the frame.

## Assembled preview

`assembly.py` builds the collar and all four leaves and poses the leaves on their own hinge axes, so you can see how the parts fit together instead of reasoning about five separate STLs. Open it in CQ-Editor and click Run for a coloured preview, one selectable object per part.

How far the leaves swing is the `OPEN_ANGLE` variable at the top of the module — 0 is fully closed and stacked flat over the diffuser, 90 is square to the frame, and it goes to 180. It currently sits at 130, with commented-out settings alongside it for fully open, fully closed, and per-leaf posing:

```python
OPEN_ANGLE = 130
# OPEN_ANGLE = 90.0    # fully open
# OPEN_ANGLE = 0.0     # fully closed, stacked over the diffuser
# OPEN_ANGLE = {"top": 90, "bottom": 90, "left": 30, "right": 30}
```

A dict poses each leaf independently, which is the quickest way to check one leaf's travel against its neighbours; any leaf left out sits closed.

Run it from the command line instead and it writes `exports/assembly.step` (parts and colours kept separate) and `exports/assembly.stl` (fused):

```bash
python assembly.py
```

`assembly.build(angle)` also returns a `cq.Assembly` if you want to drive it from your own script; the angle argument overrides `OPEN_ANGLE`.

The hardware is not modelled — see [Hinge hardware](#hinge-hardware) for the M3 stack.

## Export

```bash
python export_all.py
```

STL and STEP files are written to `exports/`.
