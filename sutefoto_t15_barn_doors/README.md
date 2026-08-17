# SUTEFOTO T15 printable barn doors — Revision 4

Five printable CadQuery modules:

- `frame.py`
- `top_door.py`
- `bottom_door.py`
- `left_door.py`
- `right_door.py`

Shared dimensions are in `params.py`; shared geometry helpers are in `common.py`.
`export_all.py` exports STL and STEP files. `fit_test_coupon.py` is the small fit-check print.

## Fit parameters you can keep from your prior copy

Your previous tuning remains compatible. In particular:

- `XY_CLEARANCE` — total width/height clearance around the light
- `CORNER_RADIUS_BODY` — inside corner radius that matches the light body
- `CORNER_RADIUS_OUTER` — outside frame corner radius

If you already tuned those values, copy your values into this V4 `params.py` before exporting.

## What V4 fixes

V2 put the top/bottom clamp bosses directly beside the hinge barrels, so a door could hit them.
V3 removed the bosses but made the screw access impractical.

V4 uses **rear-mounted external clamp bosses**. The M3 retaining screws are installed normally
from the outside toward the light, but the screw axes are at `CLAMP_SCREW_Z = 11.0 mm`, behind
the 8 mm collar and behind the hinge barrel. Thus the clamp hardware does not occupy the intended
0° to 90° barn-door sweep in front of the light.

Use four M3 retaining/set screws. Nylon screws are preferred; with metal screws use a small
felt/TPU/rubber pad at the contact point. Start with M3 x 8 to M3 x 10 depending on your final fit.

## Hinges: simple through-bolt friction pivots

Each of the eight hinge stations uses this stack:

`M3 screw head -> M3 washer -> door fork -> frame knuckle -> door fork -> M3 washer -> M3 nyloc nut`

The modeled bore is 3.3 mm, deliberately a clearance hole. The **friction comes from tightening
the nyloc nut**, not from making the screw bind in the printed bore. Tighten each pivot until the
door takes deliberate hand pressure to move and stays at arbitrary angles.

Recommended hardware:

- 8 x M3 x 20 mm socket-head cap screws
- 16 x M3 flat washers
- 8 x M3 nyloc nuts

The printed hinge stack is about 11.7 mm wide before washers/nut, so 20 mm gives comfortable
thread engagement through a nyloc nut without depending on perfect printed dimensions.

## Supports

Do not intentionally fill the 3.3 mm M3 hinge bores with support. Small horizontal bores are
better printed open and cleaned with a 3.2–3.3 mm drill by hand if necessary. Keep support only
where your slicer identifies genuinely unsupported exterior hinge geometry.

## Export

From this directory:

```bash
python export_all.py
```

Outputs are written to `exports/` as STL and STEP.
