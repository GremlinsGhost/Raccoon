from UiCore.StartUi import start
from UiCore.ParseInput import parse
from UiCore.ShowOutput import show

from SyncNodes.ProcessesNode import processes
from SyncNodes.DiskNode import disk
from SyncNodes.NetworkNode import network



def raccoon():
    for user_input in start():
        command = parse(user_input)

        if command == "status":
            output = "Raccoon online."
        elif command == "version":
            output = "Raccoons test-of-concept"
        elif command == "info":
            output = "Minimal introspection tool running on Python."
        elif command == "processes":
            output = processes()
        elif command == "disk":
            output = disk()
        elif command == "network":
            output = network()

        
        else:
            output = "Unknown command."

        show(output)

if __name__ == "__main__":
    raccoon()
