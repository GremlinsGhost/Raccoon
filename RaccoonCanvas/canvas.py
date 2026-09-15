"""RaccoonCanvas piirtää Raccoonin UI n targetille."""


# Väliaikaiset paneelivärit
# Myöhemmin nämä tulevat skinistä
PANEL_COLORS = {
    "topbar":     (0x44, 0x44, 0x88),
    "bottombar":  (0x33, 0x33, 0x33),
    "left":       (0x2a, 0x2a, 0x2a),
    "right":      (0x22, 0x22, 0x22),
    "stage":      (0x50, 0x28, 0x28),
    "log":        (0x28, 0x50, 0x28),
    "properties": (0x28, 0x28, 0x50),
    "tools":      (0x50, 0x50, 0x28),
}


class RaccoonCanvas:
    def __init__(self, target, skin=None):
        """target: olio jolla on fill_rect(x, y, w, h, r, g, b, a=255)"""
        self.target = target
        self.skin = skin

    def paint_layout(self, layout):
        """Piirtää layoutin kaikki rectit."""
        for name, rect in layout.rects.items():
            if name == "root":
                continue

            color = PANEL_COLORS.get(name, (0x10, 0x10, 0x10))
            self.target.fill_rect(
                rect.x, rect.y, rect.w, rect.h,
                color[0], color[1], color[2]
            )