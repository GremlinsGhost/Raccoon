from BashCore.RunBash import run_bash
from Core.CommandRegistry import register

COMMAND = "network"
SCRIPT = "commands/raccoon_network.sh"

def run():
    res = run_bash(SCRIPT)

    if not res["ok"]:
        return Error(COMMAND, res["error"])

    return ("Network", res["output"])

register(COMMAND, run)

