from Raccoon.Debug.DebugSend import send as debug

from Raccoon.UiLayout.UiLayoutManager import UiLayoutManager
from Raccoon.UiLayout.SkinModel import default_skin
from Raccoon.UiLayout.PanelRegistry import PanelRegistry
from Raccoon.UiLayout.SelectionModel import highlight_selection
from Raccoon.UiLayout.BottomBarModel import build_bottombar_model

from Raccoon.BashCore.BashCore import get_process_table
from Raccoon.SyncNodes.StatusNode import run as status_run
from Raccoon.SyncNodes.ProcessesNode import run as processes_run
from Raccoon.SyncNodes.NetworkNode import run as network_run
from Raccoon.SyncNodes.DiskNode import run as disk_run

def main():
    # Skin
    skin = default_skin()

    # Paneelirekisteri
    registry = PanelRegistry()
    registry.register("Stage", skin)
    registry.register("Log", skin)
    registry.register("Tools", skin)
    registry.register("Properties", skin)
    registry.register("TopBar", skin)
    registry.register("BottomBar", skin)

    # Paneelien layout-rivit
    layout_rows = [
        {"content_type": "Stage", "col": 0, "row": 0},
        {"content_type": "Log", "col": 0, "row": 1},
        {"content_type": "Properties", "col": 1, "row": 0},
        {"content_type": "Tools", "col": 1, "row": 1},
    ]

    # UILayoutManager
    layout = UiLayoutManager(
        width=1280,
        height=720,
        layout_rows=layout_rows
    )

    # BashCore / SyncNodes data (NÄMÄ PITÄÄ OLLA ENNEN debug-shell)
    process_table = get_process_table()
    status_info = status_run()
    disk_info = disk_run()
    network_info = network_run()
    processes_info = processes_run()

    # DEBUG: rects
    debug("rects", {name: vars(r) for name, r in layout.rects.items()})

    # DEBUG: UI tree
    debug("ui", {
        "type": "root",
        "id": "root",
        "props": {},
        "children": [
            {"type": "Stage", "id": "stage", "props": {}, "children": []},
            {"type": "Log", "id": "log", "props": {}, "children": []},
        ]
    })

    # DEBUG: shell
    debug("shell", {
        "cpu": "12%",
        "memory": "1.3GB / 8GB",
        "disk": disk_info["raw"],
        "network": network_info["raw"],
        "processes": processes_info["raw"].split("\n")
    })

    # DEBUG: error
    debug("error", {"state": "error", "message": "test error"})

    # Stage items
    stage_items = []
    for row in process_table["rows"]:
        safe = row + [None] * (5 - len(row))
        stage_items.append({
            "id": safe[0],
            "process": safe[1],
            "user": safe[2],
            "cpu": safe[3],
            "mem": safe[4],
        })

    layout.set_stage_items(stage_items)

    # Highlight example
    highlighted = highlight_selection(
        layout.stage_items,
        selected_id="303",
        skin=skin
    )

    # Bottom bar model
    bottom_bar = build_bottombar_model(skin)

    # Debug output
    print("Raccoon UILayout ready.")
    print("Rects:", layout.rects)
    print("Highlighted:", highlighted)
    print("BottomBar:", bottom_bar)
    print("Status:", status_info)
    print("Disk:", disk_info)
    print("Network:", network_info)
    print("Processes:", processes_info)

    # DEBUG RENDER
    from Raccoon.run_view import render_frame
    ui = render_frame(layout)
    print(ui)

    from Raccoon.Debug.ErrorTimeline import explain_error
    import traceback

    try:
        ui = render_frame(layout)
        print(ui)

    except Exception as e:
        tb = traceback.format_exc()
        print(tb)

        notes = explain_error(e)
        print("\n=== Raccoon Error Timeline ===")
        for n in notes:
            print(n)

if __name__ == "__main__":
    main()
