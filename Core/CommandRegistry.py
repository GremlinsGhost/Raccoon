COMMANDS = {}

def register(name: str, handler):
    COMMANDS[name] = handler

def get(name: str):
    return COMMANDS.get(name)
