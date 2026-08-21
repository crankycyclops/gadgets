import cadquery as cq
from common import build_door


def build():
    return build_door("right")


if __name__ == "__main__":
    result = build()
    try:
        show_object(result)
    except NameError:
        cq.exporters.export(result, "right_door.stl")

# CQ-Editor preview.  Still fires on Run in CQ-Editor; skipped when frame.py is
# imported by export_all/validate_assembly, where show_object does not exist.
try:
    show_object(build())
except NameError:
    pass