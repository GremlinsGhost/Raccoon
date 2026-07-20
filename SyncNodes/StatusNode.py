from Core.CommandRegistry import register
from Core.Error import Error

COMMAND = "status"

def run():
    return ("Status", "Raccoon online.")

register(COMMAND, run)
