
# shell, prosessi ja järjestelmädatan visualisointi
#Tää moduuli näyttää debug-näkymässä kaiken mitä Raccoon saa järjestelmästä:
#ps aux, disk info, network info, CPU/memory snapshotit jne.


from .DebugCore import core

class DebugShell:
    def __init__(self):
        self.enabled = True

    def render(self):
        #Palauttaa UIelementtejä jotka kuvaavat shell ja system dataa
        if not self.enabled:
            return []

        ui = []
        shell_data = core.state.get("shell", {})
        y = 10

        # SHELL HEADER 
        ui.append({
            "type": "text",
            "value": "Shell / System Info",
            "x": 400,
            "y": y,
            "color": "#ffaa00"
        })
        y += 30

        #  CPU / MEMORY / DISK / NET 
        for key in ["cpu", "memory", "disk", "network"]:
            if key in shell_data:
                ui.append({
                    "type": "text",
                    "value": f"{key.upper()}: {shell_data[key]}",
                    "x": 400,
                    "y": y,
                    "color": "#cccccc"
                })
                y += 20

        # PROSESSIT 
        processes = shell_data.get("processes", [])
        if processes:
            ui.append({
                "type": "text",
                "value": "Processes:",
                "x": 400,
                "y": y + 10,
                "color": "#66aaff"
            })
            y += 30

            for p in processes[:10]:  # näytä 10 prosessia
                ui.append({
                    "type": "text",
                    "value": f"{p}",
                    "x": 420,
                    "y": y,
                    "color": "#88bbff"
                })
                y += 20

        #  RAW SHELL OUTPUT 
        raw = shell_data.get("raw", None)
        if raw:
            ui.append({
                "type": "text",
                "value": "Raw Output:",
                "x": 400,
                "y": y + 10,
                "color": "#ff6666"
            })
            y += 30

            for line in raw.split("\n")[:8]:
                ui.append({
                    "type": "text",
                    "value": line,
                    "x": 420,
                    "y": y,
                    "color": "#ff8888"
                })
                y += 20

        return ui

# yksittäinen instanssi
shell = DebugShell()
