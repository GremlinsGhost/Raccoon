class LogView:
    def __init__(self, view_object):
        self.view_object = view_object

    def render(self, canvas):
        logs = self.view_object.get("rows") or []

        for i, line in enumerate(logs):
            canvas.draw_text(0, i, line)

        return canvas
