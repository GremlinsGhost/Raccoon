class TableView:
    def draw(self, canvas, view_object):
        cols = view_object.get("columns")
        rows = view_object.get("rows")

        # header
        header = " | ".join(cols)
        canvas.draw_text(0, 0, header)

        # rows
        for i, row in enumerate(rows):
            line = " | ".join(row)
            canvas.draw_text(0, i+1, line)
