from BashCore.RunBash import run_bash
from Core.CommandRegistry import register

COMMAND = "processes"
SCRIPT = "commands/raccoon_processes.sh"

def run():
    res = run_bash(SCRIPT)

    if not res["ok"]:
        return Error(COMMAND, res["error"])

    return ("Processes", res["output"])

register(COMMAND, run)
