class Layout:
    def __init__(self, layout_spec):
        self.layout_spec = layout_spec

    def render(self, canvas, viewport):
        y_offset = 0

        for region, view_object in self.layout_spec.items():
            region_canvas = canvas.offset(y_offset)

            viewport.canvas = region_canvas
            viewport.render(view_object)

            y_offset += region_canvas.height  

        return canvas
