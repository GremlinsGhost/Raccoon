def build_skin_model(raw):

    skin = {
        "colors": {},
        "input": {}
    }

    for key, value in raw.items():
        if key in ["background_color", "text_color", "primary_color", "accent_color", "border_color"]:
            skin["colors"][key] = value

        elif key in ["radius", "padding", "margin"]:
            skin["input"][key] = value

        else:
            skin[key] = value

    return skin


def default_skin():

    return build_skin_model({
        "background_color": "#1e1e1e",
        "text_color": "#ffffff",
        "primary_color": "#4fc3f7",
        "accent_color": "#ffca28",
        "border_color": "#333333",

        "radius": 4,
        "padding": 6,
        "margin": 8,

        "panel_bg": "#252525",
        "panel_border": "#3a3a3a",
        "hover_coral": "#ff7f50"
    })
