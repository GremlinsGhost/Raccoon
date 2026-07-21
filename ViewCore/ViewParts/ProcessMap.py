class ProcessMap:
    def __init__(self, view_object):
        self.view_object = view_object

    def render(self, canvas):
        data = self.view_object.data

        for node in data.get("nodes", []):
            x = node.get("x", 0)
            y = node.get("y", 0)
            label = node.get("label", "")
            canvas.draw_text(x, y, label)

        return canvas
