def highlight_selection(stage_items, selected_id, skin):
    """
    Raccoon-compatible selection highlighter.
    Takes a list of stage item models and returns updated highlight states.
    """

    updated = []

    for item in stage_items:
        cid = item.get("id")

        if cid == selected_id:
            updated.append({
                **item,
                "highlight": {
                    "color": skin["hover_coral"],
                    "thickness": 2
                }
            })
        else:
            updated.append({
                **item,
                "highlight": {
                    "color": skin["border"],
                    "thickness": 1
                }
            })

    return updated
