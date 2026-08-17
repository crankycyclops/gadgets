import cadquery as cq
from common import vertical_door

def build():
    return vertical_door()

if __name__ == "__main__":
    result = build()
    try:
        show_object(result)
    except NameError:
        cq.exporters.export(result, "right_door.stl")
