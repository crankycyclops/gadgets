import cadquery as cq
from common import horizontal_door

def build():
    return horizontal_door()

if __name__ == "__main__":
    result = build()
    try:
        show_object(result)
    except NameError:
        cq.exporters.export(result, "bottom_door.stl")
