from Raccoon.Debug.DebugView import view as DebugView
from Raccoon.Debug.DebugRects import rects as DebugRects
from Raccoon.Debug.DebugShell import shell as DebugShell
from Raccoon.Debug.DebugUi import ui_debug as DebugUi

def render_frame(layout):
    ui_elements = []

    # DEBUG-ELEMENTIT
    debug_ui = []
    debug_ui += DebugView.render()
    debug_ui += DebugRects.render()
    debug_ui += DebugShell.render()
    debug_ui += DebugUi.render()

    ui_elements += debug_ui

    return ui_elements
