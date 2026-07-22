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

    # BashCore / SyncNodes data
    process_table = get_process_table()
    status_info = status_run()
    disk_info = disk_run()
    network_info = network_run()
    processes_info = processes_run()

    # Stage items
    stage_items = []

    for row in process_table["rows"]:
        # Täytä puuttuvat kentät None:lla
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
    
    
    

    # Debug output (until OS window exists)
    print("Raccoon UILayout ready.")
    print("Rects:", layout.rects)
    print("Highlighted:", highlighted)
    print("BottomBar:", bottom_bar)
    print("Status:", status_info)
    print("Disk:", disk_info)
    print("Network:", network_info)
    print("Processes:", processes_info)


if __name__ == "__main__":
    main()
