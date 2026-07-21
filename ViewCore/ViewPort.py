from Raccoon.ViewCore.Canvas import Canvas

from Raccoon.ViewCore.ViewParts.TableView import TableView
from Raccoon.ViewCore.ViewParts.LogView import LogView
from Raccoon.ViewCore.ViewParts.ProcessMap import ProcessMap
from Raccoon.ViewCore.ViewObject import ViewObject


class ViewPort:
    def __init__(self):
        self.canvas = Canvas()

    def render(self, view_object):
        view_type = view_object.get("type")

        if view_type == "table":
            TableView().draw(self.canvas, view_object)
        elif view_type == "log":
            LogView().draw(self.canvas, view_object)
        elif view_type == "process_map":
            ProcessMap().draw(self.canvas, view_object)

        return self.canvas.render()
