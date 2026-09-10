from pathlib import Path
import cadquery as cq
import frame, top_door, bottom_door, left_door, right_door, fit_test_coupon

OUT = Path(__file__).with_name("exports")
OUT.mkdir(exist_ok=True)
PARTS = {
    "frame": frame.build,
    "top_door": top_door.build,
    "bottom_door": bottom_door.build,
    "left_door": left_door.build,
    "right_door": right_door.build,
    "fit_test_coupon": fit_test_coupon.build,
}
for name, fn in PARTS.items():
    obj = fn()
    cq.exporters.export(obj, str(OUT / f"{name}.stl"))
    #cq.exporters.export(obj, str(OUT / f"{name}.step"))
    print(name)
