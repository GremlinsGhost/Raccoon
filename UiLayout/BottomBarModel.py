def build_bottombar_model(skin):


    return {
        "status": "Ready",
        "settings_icon": "⚙",
        "colors": {
            "bg": skin.get("panel_bg"),
            "fg": skin.get("text"),
            "border": skin.get("border"),
        }
    }
