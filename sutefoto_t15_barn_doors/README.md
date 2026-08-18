# SUTEFOTO T15 barn doors — Revision 6 fold-flat / light-trap redesign

This revision replaces the previous frame and doors.  It keeps the same collar-fit concept and familiar fit parameter names, but moves the hinge axes forward of the light so the doors can close over the diffuser without striking the frame.

## What changed

- **Fold-flat closing:** each door is modeled in its fully closed position and opens 90° outward.
- **Closed-door stacking:** top, bottom, and side leaves use three slightly staggered Z planes so all four can be closed at once. Left/right share one plane because they do not meet in the center.
- **Light-leak control:** each leaf overlaps the outer frame edge by `LIGHT_TRAP_OVERLAP`; when opened, that root portion becomes a skirt across the former frame/door gap.
- **Stronger door hinges:** the fork knuckles use tapered 11 mm roots and 10 mm-deep reinforced webs.
- **Simple friction hardware:** M3 through-bolt + washers + nyloc nut. Tighten until the door takes deliberate hand pressure to move.
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

- 8 × M3 × 20 mm socket-head screws
- 16 × M3 flat washers
- 8 × M3 nyloc nuts

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
