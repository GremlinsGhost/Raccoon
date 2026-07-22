class PanelRegistry:
    def __init__(self):
        self.panels = {}

    def register(self, name, skin):
        model = {
            "name": name,
            "colors": {
                "bg": skin.get("panel_bg"),
                "fg": skin.get("text"),
                "border": skin.get("panel_border"),
            }
        }

        self.panels[name.lower()] = model
        return model

    def get(self, name):
        return self.panels.get(name.lower())
