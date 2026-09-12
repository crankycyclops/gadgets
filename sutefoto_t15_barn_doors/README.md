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

These no longer describe the part as built — see
[Beams cut back to the knuckle](#beams-cut-back-to-the-knuckle).

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

- **The corners are levelled.** Each wall's depth steps run only as far as its own leaf reaches (|x| ≤ 78, |y| ≤ 38), and past both of them nothing sweeps the corner at any angle. That piece used to be left at the full ring depth, a fin standing 7 mm proud of the corner step at the top corners and 12 mm at the bottom; it is now cut to the shallower of the two neighbouring corner steps. The adapter rail is the exception: it keeps its corners at full depth, because that is what it roots in, and starts only at |x| = 78 so the long-wall hinges beside it have room to start their nuts.
- **The depth limit is one flat step per side, not the cylinder itself.** Following the cylinder buys about 1.4 mm more depth on the outboard half of the wall and costs a tapered, pointed edge to get it. A flat bottom per side, set by the wall's *inboard* face — the part nearest the leaf — is simpler to print and to look at.
- **It applies only where a leaf can reach.** Trimming to the cylinder everywhere would also delete the wall between the front face and the *top* of that cylinder; on the sides the cylinder does not begin until z = −4.9, so a naive trim throws away 5.9 mm of wall along the whole run to clear a door that is never there.

Measured as blocked area against the raw gap: **74 %** overall — top 69 %, bottom 76 %, sides 76 %. What is left is the `FRAME_SHROUD_CLEAR` running gap plus the slots where the door forks pass through. Narrowing the fork flare (`DOOR_HINGE_ROOT_W`) to close those slots was measured and returns only 3 %, which is not worth weakening the door for.

**Assembly note:** `FRAME_HINGE_FASTENER_R` dropped 5.5 → 4.6 mm, because this channel cuts through the shroud as well as the beam and every 0.1 mm of it costs coverage. It still clears the fork barrels, an M3 washer and an M3 nyloc, but there is no longer room to bring a socket down the bolt axis past the shroud — hold the nyloc with a thin open-end spanner from the front instead.

## Beams cut back to the knuckle

Revision 9's beam wrapped the barrel across its whole 24 mm width, and the
`FRAME_HINGE_FASTENER_R` channel then bored the middle out of it either side of
the knuckle. What that left standing was a pair of crescents per station —
partial knuckles spanning the channel out to the leaf's root radius, tapering to
a feather edge where the sweep sector's boundary ran down tangent to the
channel. Nothing hangs off them: the door is carried entirely by
`HINGE_CENTER_W`, and no fork ever reaches them. What they did do was close the
one side a spanner could get to the nyloc from, and stand ready to snap off.

Outside the knuckle the beam now stops dead at the channel's rear tangent plane,
`FRAME_HINGE_FASTENER_R` behind the hinge axis. Because the plane is tangent,
the channel takes nothing out of the beam there at all, so the step is a flat
full-thickness face rather than another thin edge, and everything forward of it —
fork, washer, nyloc, spanner — is in open air.

The bolt hole was also cut back. At `FRAME_HINGE_BEAM_W + 4` it stood 2 mm proud
of both ends of every beam; on the short wall, where the beams stand on the
adapter rail, that meant four blind holes drilled into the one member holding
those hinges up. It only ever had to clear the knuckle, so it now runs
`HINGE_CENTER_W + 4` and both ends land inside the channel, in space that is
already empty.

The cost is section. Measured as the least cross-section on any plane between
the barrel's rear tangent and the beam's footing — the collar's front face, or
`ADAPTER_CUT_Z` where the beam stands on the rail — every station goes from
173 mm² to 82 mm², a 53 % loss, since the load now crosses the 8 mm knuckle
alone. That is still an order of magnitude above the 4.6–9.5 mm² of the
revision 8 hinges that actually peeled off. `HINGE_CENTER_W` is the number to
raise if it wants more; it sets the tongue's width directly, and the door forks
are positioned from it.

## Tripod adapter windows

The long and short walls that carry the light's 1/4-20 sockets (`ADAPTER_CUT_SIDES`) each have a window cut in them so a quick-release plate can seat flush on the light. See the revision 12 notes in `params.py` for why.

**Blocking a window.** A window you are not using is just a light leak, so either one can be filled back in:

```python
ADAPTER_BLOCK_LONG = True    # default: long-wall window closed
ADAPTER_BLOCK_SHORT = False  # default: short-wall window open
```

A blocked window gets back the wall it would otherwise have: collar wall, front lip and the ordinary 2.4 mm shroud, from `ADAPTER_CUT_Z` rearward. It is still a cut side for everything else — the hinge planes and the door leaf reliefs follow `ADAPTER_CUT_SIDES` alone — so these two switches change only the frame. The same doors fit every combination. Do not remove a side from `ADAPTER_CUT_SIDES` to close its window; that moves the hinge planes back and the printed doors will no longer fit.

On the short wall, a blocked window also gives the two hinge beams something to stand on instead of overhanging the window.

**Short-wall rail gap.** The rail that carries the short wall's hinges does not run across the middle. Between the two hinge beams (|y| < 11), everything forward of `ADAPTER_RAIL_REAR_Z` is removed, rail and shroud alike. That solid bar started exactly where the fastener channels end, so a 20 mm screw's tip ran into it and the nyloc could not go on. From each beam's inner face in to its knuckle (|y| 11–19), the rail is also cut back to the channel's rear tangent plane, the same rule the beams follow. Otherwise it was left standing as a free tube around the channel, the kind of stub that snaps off. Only the flat plate behind it stays. Each beam still hangs off its own corner through the rest of the rail. The cost is that stretch of shroud — a 22 × 17.4 mm slot — so with the short-side door open some light escapes sideways between the hinges.

## Revision 13 — extra depth

`FRAME_EXTRA_DEPTH` (40 mm) holds the whole hinge line further out in front of the light. It exists because the short wall's hinge sat about 6 mm in front of a seated quick-release plate's front edge — right where the tripod head's lock closes — so mounting the light by that socket fouled the hinge.

**Changing it.** Edit the one number and re-export; nothing else needs touching.

```python
FRAME_EXTRA_DEPTH = 40.0   # 0 gives the revision 12 frame back
```

The frame's overall depth tracks it 1:1 — 33.1 mm at 0, 73.1 mm at 40, 113.1 mm at 80. `validate_assembly.py` passes at 0, 20, 40 and 60, and the frame builds as one valid solid with nothing intruding on either window at 0, 10, 20, 40, 60 and 80. Only the frame needs reprinting: the leaves are placed on their own axes, so changing this moves them in the assembly but does not change their geometry at all.

It is one number because nothing forward of the collar is placed by hand. The shroud's depth is `|HINGE_Z|` plus an in-plane term, the hinge beams are built from `HINGE_Z`, the adapter rail is the shroud at a greater thickness, and the leaves are placed on their own axes. So the parameter does one thing: shift the three hinge planes forward, after the adapter limits have been derived. Every one of those limits is a "no further rearward than" bound, and the 5.215/4.35 mm stagger between the three leaf layers is preserved, so the closed stack is unaffected.

- **The windows do not move.** `ADAPTER_CUT_Z`, the window band and the collar are all rearward of z = 0 and none of them reads `HINGE_Z`. The short wall rearward of the cut plane is geometrically identical to revision 12 — checked, byte for byte. The 40 mm is added on top of the cutouts.
- **The doors do not change.** All four leaves come out with identical volume and identical bounding boxes, only translated in Z. A set already printed still fits.
- **The frame goes from 33 to 73 mm deep** overall (z −65.06 … +8).

**What stands over the cutout.** Revision 12 ran the `ADAPTER_RAIL_T` rail from the cut plane forward, because that was the whole wall it had. Carried straight through the extra depth that becomes a 12 mm slab 46 mm tall, standing in exactly the space the extra depth is there to vacate — the hinge would have moved out of the tripod head's way and the rail moved into it. So `ADAPTER_RAIL_DEPTH` (12 mm, measured rearward from the hinge axis) makes the rail only as tall as the hinges it carries, and the wall under it is the ordinary 2.4 mm shroud:

| z | over the window band |
| --- | --- |
| −65.1 … −45.9 | hinge beams and rail, out to x 94.75 (12 mm off the frame edge) |
| −45.9 … −11.8 | plain 2.4 mm shroud, out to x 85.15 |
| −11.8 … +8 | the window itself, open to the light's face |

2.4 mm off the frame's outer edge is 3.25 mm off the light's own face, inside the plate's 10 mm thickness, so nothing that clamps the plate can reach it. Bounding the rail gap at `ADAPTER_RAIL_REAR_Z` rather than at the cut plane is also what keeps the documented leak between the hinges to 17.4 mm instead of 46.

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
3. each door clears the frame through its complete closed-to-open sweep, all the way to `FRAME_HINGE_MAX_OPEN`;
4. a blocked adapter window has all of its collar wall and lip back across the plate's footprint;
5. nothing stands in the short-wall rail gap;
6. a plate seated in each open adapter window clears the frame and every door through the full sweep.

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
