class Canvas:
    def __init__(self, width=80, height=24):
        self.width = width
        self.buffer = [[" "]*width for _ in range(height)]

    def draw_text(self, x, y, text):
        for i, ch in enumerate(text):
            if 0 <= x+i < self.width and 0 <= y < self.height:
                self.buffer[y][x+i] = ch

    def render(self):
        return "\n".join("".join(row) for row in self.buffer)

    def offset(self, y):
        new_canvas = Canvas(self.width, self.height - y)
        new_canvas.buffer = self.buffer[y:]
        return new_canvas

    @property
    def height(self):
        return len(self.buffer)
