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

    def offset(self, dx, dy):
        return OffsetCanvas(self, dx, dy)
    
    def merge(self, other):
        for y in range(other.height):
            for x in range(other.width):
                ch = other.buffer[y][x]
                if ch != " ":
                    if 0 <= y < self.height and 0 <= x < self.width:
                        self.buffer[y][x] = ch


    @property
    def height(self):
        return len(self.buffer)


class OffsetCanvas:
    def __init__(self, parent, dx, dy):
        self.parent = parent
        self.dx = dx
        self.dy = dy
        self.width = parent.width
        self.height = parent.height

    def draw(self, x, y, ch):
        px = x + self.dx
        py = y + self.dy
        if 0 <= px < self.width and 0 <= py < self.height:
            self.parent.buffer[py][px] = ch

    def draw_text(self, x, y, text):
        for i, ch in enumerate(text):
            self.draw(x + i, y, ch)

    def draw_rect(self, x, y, w, h, ch):
        for yy in range(h):
            for xx in range(w):
                self.draw(x + xx, y + yy, ch)

    def render(self):
        return self.parent.render()

    def merge(self, other):
        for y in range(other.height):
            for x in range(other.width):
                ch = other.buffer[y][x]
                if ch != " ":
                    self.draw(x, y, ch)
