class Error:
    def __init__(self, command: str, message: str):
        self.command = command
        self.message = message

    def __str__(self):
        return f"[{self.command}:Error] {self.message}"
