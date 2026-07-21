class TableView:
    def __init__(self, view_object):
        data = view_object.data
        self.header = data.get("header", "")
        self.rows = data.get("rows", [])

    def render(self, canvas):
        canvas.draw_text(0, 0, self.header)
        y = 1
        for row in self.rows:
            canvas.draw_text(0, y, row)
            y += 1

    def height(self):
        return 1 + len(self.rows)
