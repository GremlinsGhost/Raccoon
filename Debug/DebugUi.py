
# UI puun ja komponenttidatan visualisointi

#Tää moduuli näyttää UI n sisäisen rakenteen debug-näkymässä:
#komponentit, propsit, lapset, id t, jne.


from .DebugCore import core

class DebugUi:
    def __init__(self):
        self.enabled = True

    def render(self):
        #Palauttaa UI elementtejä jotka kuvaavat UI puuta
        if not self.enabled:
            return []

        ui = []
        ui_tree = core.state.get("ui", None)

        if not ui_tree:
            return ui

        y = 10

        # HEADER 
        ui.append({
            "type": "text",
            "value": "UI Tree",
            "x": 700,
            "y": y,
            "color": "#ffaa00"
        })
        y += 30

        # REKURSIO: PIIRRÄ PUU 
        def draw_node(node, depth=0, y_offset=0):
            indent = "  " * depth
            text = f"{indent}{node.get('type')} (id={node.get('id')})"

            ui.append({
                "type": "text",
                "value": text,
                "x": 700,
                "y": y_offset,
                "color": "#cccccc"
            })

            # Props
            props = node.get("props", {})
            for key, val in props.items():
                ui.append({
                    "type": "text",
                    "value": f"{indent}- {key}: {val}",
                    "x": 720,
                    "y": y_offset + 20,
                    "color": "#88bbff"
                })
                y_offset += 20

            # Lapset
            children = node.get("children", [])
            y_offset += 30
            for child in children:
                y_offset = draw_node(child, depth + 1, y_offset)

            return y_offset + 20

        # piirrä juurisolmu
        draw_node(ui_tree, depth=0, y_offset=y)

        return ui

# yksittäinen instanssi
ui_debug = DebugUi()
