class Layout:
    def __init__(self, padding=1):
        self.padding = padding

    def offset(self, x, y):
        return x + self.padding, y + self.padding
