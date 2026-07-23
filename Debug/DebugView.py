
#  debug-näkymä Raccoonin UI:lle
# Piirtää DebugCoren keräämän tilan, tapahtumat ja virheet.


from .DebugCore import core

class DebugView:
    def __init__(self):
        self.visible = True   # debug tila voidaan myöhemmin togglata

    def render(self):
        # Palauttaa UI rakenteen joka voidaan piirtää Raccoonin ruudulle
        if not self.visible:
            return []

        ui = []

        # YHTEENVETO 
        summary = core.summary()
        ui.append({
            "type": "text",
            "value": f"Debug Summary: events={summary['events']} errors={summary['errors']}",
            "x": 10,
            "y": 10,
            "color": "#ffcc00"
        })

        #  VIIMEISIN TILA 
        y_offset = 40
        ui.append({
            "type": "text",
            "value": "Latest State:",
            "x": 10,
            "y": y_offset,
            "color": "#ffffff"
        })
        y_offset += 20

        for key, value in core.state.items():
            ui.append({
                "type": "text",
                "value": f"{key}: {value}",
                "x": 20,
                "y": y_offset,
                "color": "#cccccc"
            })
            y_offset += 20

        # VIRHEET 
        ui.append({
            "type": "text",
            "value": "Errors:",
            "x": 10,
            "y": y_offset + 10,
            "color": "#ff4444"
        })
        y_offset += 30

        for err in core.errors[-5:]:  # näytä viimeiset 5 virhettä
            ui.append({
                "type": "text",
                "value": f"{err['time']} – {err['event']}: {err['data']}",
                "x": 20,
                "y": y_offset,
                "color": "#ff6666"
            })
            y_offset += 20

        # HISTORIA 
        ui.append({
            "type": "text",
            "value": "History:",
            "x": 10,
            "y": y_offset + 10,
            "color": "#66aaff"
        })
        y_offset += 30

        for h in core.history[-10:]:  # viimeiset 10 tapahtumaa
            ui.append({
                "type": "text",
                "value": h,
                "x": 20,
                "y": y_offset,
                "color": "#88bbff"
            })
            y_offset += 20

        return ui

# yksittäinen instanssi
view = DebugView()
