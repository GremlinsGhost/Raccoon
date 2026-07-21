from Raccoon.UiCore.Panel import Panel

# Globaalit viitteet paneeleihin
stage_panel = None
tools_panel = None
properties_panel = None
log_panel = None
topbar_panel = None
bottombar_panel = None


def render_region(name, skin):

    panel = Panel(
        name=name,
        bg=skin["panel_bg"],
        fg=skin["text"],
        border=skin["panel_border"]
    )

    # Rekisteröi paneeli
    global stage_panel, tools_panel, properties_panel, log_panel
    global topbar_panel, bottombar_panel

    if name == "Stage":
        stage_panel = panel
    elif name == "Tools":
        tools_panel = panel
    elif name == "Properties":
        properties_panel = panel
    elif name == "Log":
        log_panel = panel
    elif name == "TopBar":
        topbar_panel = panel
    elif name == "BottomBar":
        bottombar_panel = panel

    return panel
