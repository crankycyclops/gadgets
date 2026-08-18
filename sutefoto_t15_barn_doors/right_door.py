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
