def build_bottombar_model(skin):
    """
    Raccoon compatible bottom bar model.
    No Tkinter, no UI rendering.
    Returns pure data for the UI layer to decide how to display.
    """

    return {
        "status": "Ready",
        "settings_icon": "⚙",
        "colors": {
            "bg": skin.get("panel_bg"),
            "fg": skin.get("text"),
            "border": skin.get("border"),
        }
    }
