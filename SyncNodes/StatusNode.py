from Raccoon.Core.CommandRegistry import register
from Raccoon.BashCore.RunBash import run_bash

SCRIPT = "raccoon_status.sh"


def run():
    output = run_bash(SCRIPT)

    return {
        "ok": True,
        "raw": output,
    }


register("status", run)
