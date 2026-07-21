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
            TableView(view_object).render(self.canvas)

        elif view_type == "log":
            LogView(view_object).render(self.canvas)

        elif view_type == "process_map":
            ProcessMap(view_object).render(self.canvas)

        return self.canvas.render()
