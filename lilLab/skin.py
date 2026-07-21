from Designer.designer_loader import load_skin_sql
from Designer.designer_loader import load_all_sql


def build_skin_model(sql_rows):
    skin = {
        "colors": {},
        "input": {}
    }

    for key, value in sql_rows:
        if key in ["background_color", "text_color", "primary_color", "accent_color", "border_color"]:
            skin["colors"][key] = value
        elif key in ["radius", "padding", "margin"]:
            skin["input"][key] = value
        else:
            skin[key] = value

    return skin


def generate_skin():
    rows = load_skin_sql()
    skin = build_skin_model(rows)
    return skin
