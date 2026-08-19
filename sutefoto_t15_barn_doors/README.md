# SUTEFOTO T15 barn doors — Revision 6 fold-flat / light-trap redesign

This revision replaces the previous frame and doors.  It keeps the same collar-fit concept and familiar fit parameter names, but moves the hinge axes forward of the light so the doors can close over the diffuser without striking the frame.

## What changed

- **Fold-flat closing:** each door is modeled in its fully closed position and opens outward to `FRAME_HINGE_MAX_OPEN` (180°).
- **Closed-door stacking:** top, bottom, and side leaves use three slightly staggered Z planes so all four can be closed at once. Left/right share one plane because they do not meet in the center.
- **Light-leak control:** each leaf overlaps the outer frame edge by `LIGHT_TRAP_OVERLAP`; when opened, that root portion becomes a skirt across the former frame/door gap.
- **Stronger door hinges:** the fork knuckles use tapered 11 mm roots and 10 mm-deep reinforced webs.
- **Simple friction hardware:** M3 through-bolt + washers + nyloc nut. Tighten until the door takes deliberate hand pressure to move.

## Revision 9 — frame hinge buttress

The hinges used to peel off the frame. They were bridged to the collar by a tapered web only `HINGE_CENTER_W` (5 mm) wide, rooted 2 mm into a 2.7 mm wall. Printed with the collar's back face on the bed, the layer planes run straight through that junction, and the side hinges were cantilevering a 56 mm door off a 4.6 mm² sliver.

Each hinge now sits on a solid beam, `FRAME_HINGE_BEAM_W` (24 mm) wide, standing on the outside of the collar. In section it is an L: the base roots `FRAME_HINGE_ROOT_DEPTH` into the wall across the full collar depth, and everything forward of the front face stays outboard of the frame's outer edge. Its outboard face is parallel to the build direction, so it prints without overhang, and its full section lands exactly where the bending moment peaks.

Minimum section between barrel and frame:

| hinge | revision 8 | revision 9 |
|---|---|---|
| top | 9.5 mm² | 171 mm² |
| bottom | 6.2 mm² | 171 mm² |
| left / right | 4.6 mm² | 171 mm² |

`HINGE_CENTER_W` also goes 5 mm → 8 mm, which is what sets how wide the beam can be where it actually grips the barrel. The door forks are positioned from it and move outboard to suit. **This changes the screw length — see below.**

The beam is built deliberately over-fat and then cut back by the volume the doors sweep, so clearance is derived rather than guessed. The cut is a single sector, which is what keeps the slot open rather than leaving thin stepped teeth in it, and it bottoms out at exactly the barrel radius so the knuckle stays perfectly round. A coaxial channel of radius `FRAME_HINGE_FASTENER_R` either side of the centre knuckle clears the fork barrels, washers and nyloc.

The leaves are not modified. `LIGHT_TRAP_OVERLAP`, the leaf outlines and the hinge axes are all untouched, and no beam material intrudes forward of the front face inboard of the outer edge, so fold-flat closing and the light trap behave exactly as before.
- **No external clamp blocks:** this revision assumes the collar fit and front retaining lip hold the light, avoiding the protruding clamp-boss interference from earlier revisions.

## Revision 10 — full travel and the light shroud

**Travel.** Revision 9's beam silently capped the doors at 96°, because its slot was only cut for 0–90° of sweep. Barn doors need to fold well back, so `FRAME_HINGE_MAX_OPEN` is now 180°. The cost is only in the beam's minimum section — 171 mm² at 135°, 128 mm² at 180°, against revision 8's 4.6 mm². `validate_assembly.py` now sweeps the full travel rather than a fixed 0–90°, which is what would have caught the cap in the first place.

**The gap.** With a leaf open, the distance from the frame's front face to the leaf root is `|HINGE_Z| + 7.8` — 12.3 mm at the top, 16.1 at the bottom, 19.9 at the sides — and light poured straight out of it. Two things set it: the hinge axes sit forward of the front face (needed so all four leaves can stack when closed), and the leaf root has to stand 7.8 mm off its axis (barrel 4.0 + `HINGE_RADIAL_GAP` 0.8 + `LIGHT_TRAP_OVERLAP` 3.0).

Nothing flat can close that at more than one door angle. As a leaf turns, the only thing that holds still relative to the frame is a *surface of revolution about the hinge axis* — so the shroud is a wall following the frame's whole outline, standing forward from the front face, with its tip trimmed by a cylinder concentric with the hinge axis sitting `FRAME_SHROUD_CLEAR` inside the circle the leaf root sweeps. Both surfaces being coaxial, their separation is identical at every angle from 0 to 180.

Two things make it cover far more than it first did:

- **The corners are left at full depth.** The leaves are narrower than the frame (|x| ≤ 77 against an 82.75 edge, |y| ≤ 37 against 42.25), so nothing sweeps the corners at any angle and there is nothing there to clear.
- **The depth limit applies only inside the sector a leaf actually sweeps.** Keeping everything within `rho` of the axis would also delete the wall between the front face and the *top* of that cylinder; on the sides that cylinder does not begin until z = −4.9, so a naive trim throws away 5.9 mm of wall along the entire run to clear a door that is never there.

Measured as blocked area against the raw gap: **74 %** overall — top 70 %, bottom 77 %, sides 74 %. What is left is the `FRAME_SHROUD_CLEAR` running gap plus the slots where the door forks pass through. Narrowing the fork flare (`DOOR_HINGE_ROOT_W`) to close those slots was measured and returns only 3 %, which is not worth weakening the door for.

The shroud is carried back over the collar's full depth rather than stopping at the front face, so it joins the frame face-to-face instead of along a knife edge.

**Assembly note:** `FRAME_HINGE_FASTENER_R` dropped 5.5 → 4.6 mm, since every 0.1 mm there costs shroud (5.5 → 4.6 returned 593 mm³ of it). It still clears the fork barrels, an M3 washer and an M3 nyloc, but there is no longer room to bring a socket down the bolt axis past the shroud — hold the nyloc with a thin open-end spanner from the front instead.

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
3. each door clears the frame through its complete 0–90° closed-to-open sweep.

Run:

```bash
python validate_assembly.py
```

Expected output:

```text
PASS: valid solids; all doors stack closed and each clears the frame through 0-90 degrees
```

## CQ-Editor

Every main part module can render directly in CQ-Editor. Open the module and click Run; each contains:

```python
if __name__ == "__main__":
    result = build()
    show_object(result)
```

(The `try/except` wrapper also permits normal command-line STL export.)

## Assembled preview

`assembly.py` builds the collar and all four leaves and poses the leaves on their own hinge axes, so you can see how the parts fit together instead of reasoning about five separate STLs. Open it in CQ-Editor and click Run for a coloured preview, one selectable object per part.

How far the leaves swing is the `OPEN_ANGLE` variable at the top of the module — 0 is fully closed and stacked flat over the diffuser, 90 is fully open. It ships at 45, with commented-out settings alongside it for fully open, fully closed, and per-leaf posing:

```python
OPEN_ANGLE = 45.0
# OPEN_ANGLE = 90.0    # fully open
# OPEN_ANGLE = {"top": 90, "bottom": 90, "left": 30, "right": 30}
```

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
