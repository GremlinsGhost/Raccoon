class LogView:
    def __init__(self, view_object):
        self.lines = view_object.data.get("lines", [])

    def render(self, canvas):
        y = 0
        for line in self.lines:
            canvas.draw_text(0, y, line)
            y += 1

    def height(self):
        return len(self.lines)

