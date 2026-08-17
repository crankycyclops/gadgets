"""Optional 25 mm-wide slice of the collar for checking fit before printing the frame."""
import cadquery as cq
import params as p
from common import rounded_prism


def build():
    cavity_h = p.LIGHT_H + p.XY_CLEARANCE
    outer_h = cavity_h + 2*p.WALL
    width = 25.0
    coupon = (cq.Workplane("XY").box(width, outer_h, p.COLLAR_DEPTH,
                                      centered=(True, True, False)))
    aperture = (cq.Workplane("XY").box(width + 2,
                                        p.LIGHT_H - 2*p.APERTURE_OVERLAP,
                                        p.COLLAR_DEPTH + 2,
                                        centered=(True, True, False))
                .translate((0,0,-1)))
    cavity = (cq.Workplane("XY").box(width + 2, cavity_h,
                                      p.COLLAR_DEPTH - p.FRONT_LIP + 0.5,
                                      centered=(True, True, False))
              .translate((0,0,p.FRONT_LIP)))
    return coupon.cut(aperture).cut(cavity)

if __name__ == "__main__":
    cq.exporters.export(build(), "fit_test_coupon.stl")

# In CQ-Editor, uncomment the next line to preview:
# show_object(build())
