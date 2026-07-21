class LogView:
    def draw(self, canvas, data):
        for i, line in enumerate(data["lines"]):
            canvas.draw_text(0, i, line)
