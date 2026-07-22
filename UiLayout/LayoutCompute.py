def compute_layout(rects, layout_rows, left_width, stage_ratio, tools_ratio):

    root = rects["root"]

    # Kiinteät palkit
    TOPBAR_H = 28
    BOTTOMBAR_H = 24

    # TopBar
    rects["topbar"].x = 0
    rects["topbar"].y = 0
    rects["topbar"].w = root.w
    rects["topbar"].h = TOPBAR_H

    # BottomBar
    rects["bottombar"].x = 0
    rects["bottombar"].y = root.h - BOTTOMBAR_H
    rects["bottombar"].w = root.w
    rects["bottombar"].h = BOTTOMBAR_H

    # Käytettävä tila paneeleille
    usable_y = TOPBAR_H
    usable_h = root.h - TOPBAR_H - BOTTOMBAR_H

    # Left / Right kontit
    rects["left"].x = 0
    rects["left"].y = usable_y
    rects["left"].w = left_width
    rects["left"].h = usable_h

    rects["right"].x = left_width
    rects["right"].y = usable_y
    rects["right"].w = root.w - left_width
    rects["right"].h = usable_h

    # Stage / Log / Properties / Tools
    for row in layout_rows:
        name = row["content_type"].lower()

        if name in ("topbar", "bottombar"):
            continue

        r = rects[name]
        col = row["col"]
        row_i = row["row"]

        # LEFT SIDE (Stage + Log)
        if col == 0:
            r.x = rects["left"].x
            r.w = rects["left"].w

            if row_i == 0:
                r.y = usable_y
                r.h = int(usable_h * stage_ratio)
            else:
                r.y = usable_y + int(usable_h * stage_ratio)
                r.h = usable_h - int(usable_h * stage_ratio)

        # RIGHT SIDE (Properties + Tools)
        else:
            r.x = rects["right"].x
            r.w = rects["right"].w

            if row_i == 0:
                r.y = usable_y
                r.h = int(usable_h * tools_ratio)
            else:
                r.y = usable_y + int(usable_h * tools_ratio)
                r.h = usable_h - int(usable_h * tools_ratio)
