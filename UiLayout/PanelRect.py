class PanelRect:
    def __init__(self, name, x=0, y=0, w=100, h=100):
        self.name = name
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    @property
    def right(self):
        return self.x + self.w

    @property
    def bottom(self):
        return self.y + self.h

    def set(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def copy(self):
        return PanelRect(self.name, self.x, self.y, self.w, self.h)
