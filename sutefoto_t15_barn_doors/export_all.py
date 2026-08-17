"""Export all printable pieces as STL and STEP."""
from pathlib import Path
import cadquery as cq
import frame, top_door, bottom_door, left_door, right_door, fit_test_coupon

OUT = Path(__file__).resolve().parent / "exports"
OUT.mkdir(exist_ok=True)

parts = {
    "frame": frame.build(),
    "top_door": top_door.build(),
    "bottom_door": bottom_door.build(),
    "left_door": left_door.build(),
    "right_door": right_door.build(),
    "fit_test_coupon": fit_test_coupon.build(),
}

for name, solid in parts.items():
    cq.exporters.export(solid, str(OUT / f"{name}.stl"), tolerance=0.08, angularTolerance=0.1)
    cq.exporters.export(solid, str(OUT / f"{name}.step"))
    print(name, "STL + STEP")
