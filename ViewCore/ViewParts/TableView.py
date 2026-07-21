class TableView:
    def __init__(self, view_object):
        self.view_object = view_object

    def render(self, canvas):
        columns = self.view_object.get("columns") or []
        rows = self.view_object.get("rows") or []

        # Piirrä otsikot
        header = " | ".join(columns)
        canvas.draw_text(0, 0, header)

        # Piirrä rivit
        for i, row in enumerate(rows, start=1):
            line = " | ".join(str(x) for x in row)
            canvas.draw_text(0, i, line)

        return canvas
