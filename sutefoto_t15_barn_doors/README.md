# SUTEFOTO T15 barn doors — Revision 6 fold-flat / light-trap redesign

This revision replaces the previous frame and doors.  It keeps the same collar-fit concept and familiar fit parameter names, but moves the hinge axes forward of the light so the doors can close over the diffuser without striking the frame.

## What changed

- **Fold-flat closing:** each door is modeled in its fully closed position and opens 90° outward.
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

The beam is built deliberately over-fat and then cut back by the volume the doors sweep, so clearance is derived rather than guessed. The cut is a single sector, which is what keeps the slot open rather than leaving thin stepped teeth in it, and it bottoms out at exactly the barrel radius so the knuckle stays perfectly round. A coaxial channel of radius `FRAME_HINGE_FASTENER_R` either side of the centre knuckle clears the fork barrels, washers, nyloc and driver, so assembly is unchanged.

The leaves are not modified. `LIGHT_TRAP_OVERLAP`, the leaf outlines and the hinge axes are all untouched, and no beam material intrudes forward of the front face inboard of the outer edge, so fold-flat closing and the light trap behave exactly as before.
- **No external clamp blocks:** this revision assumes the collar fit and front retaining lip hold the light, avoiding the protruding clamp-boss interference from earlier revisions.

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

## Export

```bash
python export_all.py
```

STL and STEP files are written to `exports/`.
