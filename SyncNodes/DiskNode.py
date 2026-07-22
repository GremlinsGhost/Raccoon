from Raccoon.Core.CommandRegistry import register
from Raccoon.BashCore.RunBash import run_bash

SCRIPT = "raccoon_disk.sh"


def run():
    output = run_bash(SCRIPT)

    return {
        "ok": True,
        "raw": output,
    }


register("disk", run)
