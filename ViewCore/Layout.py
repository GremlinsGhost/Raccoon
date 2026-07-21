class Layout:
    def __init__(self, regions):
        self.regions = regions

    def render(self, canvas, viewport):
        y_offset = 0

        for key, view_object in self.regions.items():
            
            result = viewport.render(view_object)

            
            region_canvas = canvas.offset(0, y_offset)

            
            region_canvas.merge(result["canvas"])

            
            y_offset += result["height"]

        return canvas

