from Raccoon.ViewCore.Canvas import Canvas
from Raccoon.ViewCore.ViewParts.TableView import TableView
from Raccoon.ViewCore.ViewParts.LogView import LogView
from Raccoon.ViewCore.ViewParts.ProcessMap import ProcessMap

class ViewPort:
    def __init__(self):
        self.canvas = Canvas()

    def render(self, view_object):
        view_type = view_object.type

        if view_type == "table":
            part = TableView(view_object)

        elif view_type == "log":
            part = LogView(view_object)

        elif view_type == "process_map":
            part = ProcessMap(view_object)

        else:
            return {"canvas": self.canvas, "height": 0}

        
        part.render(self.canvas)

       
        return {
            "canvas": self.canvas,
            "height": part.height()
        }
