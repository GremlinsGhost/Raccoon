from BashCore.RunBash import run_bash
from Core.CommandRegistry import register

COMMAND = "disk"
SCRIPT = "commands/raccoon_disk.sh"

def run():
    res = run_bash(SCRIPT)

    if not res["ok"]:
        return Error(COMMAND, res["error"])

    return ("Disk", res["output"])

register(COMMAND, run)
