from UiCore.StartUi import read_input
from UiCore.ParseInput import parse
from UiCore.ShowOutput import show_output
from UiCore.ShowError import show_error
from Core.CommandRegistry import get
from Core.Error import Error

import SyncNodes.DiskNode
import SyncNodes.NetworkNode
import SyncNodes.ProcessesNode
import SyncNodes.StatusNode

def main():
    while True:
        raw = read_input()
        cmd = parse(raw)

        handler = get(cmd)
        if handler is None:
            show_error(f"Unknown command: {cmd}")
            continue

        result = handler()

        if isinstance(result, Error):
            show_error(str(result))
        else:
            title, content = result
            show_output(title, content)

if __name__ == "__main__":
    main()
