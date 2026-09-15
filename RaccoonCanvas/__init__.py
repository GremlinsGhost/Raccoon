"""RaccoonCanvas Raccoonin piirtoalusta.

Ottaa UI-dataa (layout, skin) ja maalaa sen targetille
(esim. WaylandBuffer). Tietää Raccoonin visuaalisen kielen.

Ei tiedä Waylandista. Target on mikä tahansa olio jolla on:
    fill_rect(x, y, w, h, r, g, b, a=255)
"""

from .canvas import RaccoonCanvas

__all__ = ["RaccoonCanvas"]