def highlight_selection(stage_items, selected_id, skin):
    updated = []

    for item in stage_items:
        cid = item.get("id")

        if cid == selected_id:
            updated.append({
                **item,
                "highlight": {
                    "color": skin["colors"]["accent_color"],  # tai hover_coral
                    "thickness": 2
                }
            })
        else:
            updated.append({
                **item,
                "highlight": {
                    "color": skin["colors"]["border_color"],
                    "thickness": 1
                }
            })

    return updated
