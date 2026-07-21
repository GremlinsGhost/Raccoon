from Raccoon.BashCore.BashCore import get_process_table
from Raccoon.ViewCore.ViewObject import ViewObject
from Raccoon.ViewCore.ViewPort import ViewPort
from Raccoon.ViewCore.Layout import Layout as ViewLayout
from Raccoon.ViewCore.Canvas import Canvas


class Layout:
    def __init__(self):
        self.current_view = "dashboard"

    def set_view(self, name):
        self.current_view = name

    def render(self):
        if self.current_view == "dashboard":
            return self.render_dashboard()

        elif self.current_view == "processes":
            return self.render_process_table()

        elif self.current_view == "map":
            return self.render_process_map()

        elif self.current_view == "log":
            return self.render_log()

 
    #   VIEW RENDERERS
    # -----------------

    def render_dashboard(self):
        raw = get_process_table()

        table_vo = ViewObject(
            raw["type"],
            {
                "columns": raw["columns"],
                "rows": raw["rows"]
            }
        )

        log_vo = ViewObject(
            "log",
            {
                "rows": [
                    "Starting Raccoon...",
                    "Loading modules...",
                    "Pipeline OK",
                    "Ready."
                ]
            }
        )

        layout = ViewLayout({
            "top": table_vo,
            "bottom": log_vo
        })

        canvas = Canvas()
        vp = ViewPort()
        return layout.render(canvas, vp).render()

    def render_process_table(self):
        raw = get_process_table()

        vo = ViewObject(
            raw["type"],
            {
                "columns": raw["columns"],
                "rows": raw["rows"]
            }
        )

        canvas = Canvas()
        vp = ViewPort()
        return vp.render(vo)

    def render_process_map(self):
        vo = ViewObject(
            "process_map",
            {
                "nodes": [
                    {"x": 2, "y": 2, "label": "bash"},
                    {"x": 10, "y": 4, "label": "python"},
                    {"x": 20, "y": 6, "label": "raccoon"},
                ]
            }
        )

        canvas = Canvas()
        vp = ViewPort()
        return vp.render(vo)

    def render_log(self):
        vo = ViewObject(
            "log",
            {
                "rows": [
                    "Starting Raccoon...",
                    "Loading modules...",
                    "Pipeline OK",
                    "Ready."
                ]
            }
        )

        canvas = Canvas()
        vp = ViewPort()
        return vp.render(vo)
