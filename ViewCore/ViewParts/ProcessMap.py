class ProcessMap:
    def draw(self, canvas, data):
        for node in data["nodes"]:
            canvas.draw_text(node["x"], node["y"], node["label"])
