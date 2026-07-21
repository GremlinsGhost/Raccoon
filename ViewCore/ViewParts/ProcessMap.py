class ProcessMap:
    def __init__(self, view_object):
        self.nodes = view_object.data.get("nodes", [])

    def render(self, canvas):
        for n in self.nodes:
            canvas.draw(n.x, n.y, n.char)

    def height(self):
        if not self.nodes:
            return 0
        return max(n.y for n in self.nodes) + 1
