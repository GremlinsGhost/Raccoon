
#DebugRects – Raccoonin rect-, layout- ja motion-datan visualisointi

# Tää moduuli piirtää UIn sisäisen rakenteen debug-näkymään


from .DebugCore import core

class DebugRects:
    def __init__(self):
        self.enabled = True

    def render(self):
        # Palauttaa UI elementtejä jotka kuvaavat rectejä ja motionia
        if not self.enabled:
            return []

        ui = []
        rect_data = core.state.get("rects", {})
        motion_data = core.state.get("motion", {})

        # RECT KARTTA
        

        for name, r in rect_data.items():
            ui.append({
                "type": "rect",
                "x": r.get("x", 0),
                "y": r.get("y", 0),
                "w": r.get("w", 0),
                "h": r.get("h", 0),
                "color": "#00ff88",
                "alpha": 0.25,
                "label": name
            })



        # MOTION PROFIILI
        if motion_data:
            ui.append({
                "type": "text",
                "value": f"Motion: {motion_data}",
                "x": 10,
                "y": 300,
                "color": "#ffaa00"
            })

        return ui

# yksittäinen instanssi
rects = DebugRects()
