"""RaccoonCanvas – piirtää Raccoonin UI:n targetille."""


def hex_to_rgb(hex_color):
    """#rrggbb → (r, g, b)."""
    hex_color = hex_color.lstrip("#")
    return (
        int(hex_color[0:2], 16),
        int(hex_color[2:4], 16),
        int(hex_color[4:6], 16),
    )


# Väliaikaiset paneelivärit.
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

    

    def create_line(self, x1, y1, x2, y2, color="#ffffff", width=1):
        """Piirrä viiva (Bresenhamin algoritmi)."""
        r, g, b = hex_to_rgb(color)

        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            self.target.fill_rect(x1, y1, width, width, r, g, b)
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def create_rectangle(self, x1, y1, x2, y2, outline="#ffffff", width=1):
        """Piirrä suorakaide (vain reunat)."""
        self.create_line(x1, y1, x2, y1, outline, width)   # ylä
        self.create_line(x2, y1, x2, y2, outline, width)   # oikea
        self.create_line(x2, y2, x1, y2, outline, width)   # ala
        self.create_line(x1, y2, x1, y1, outline, width)   # vasen

