class ViewObject:
    def __init__(self, view_type, payload):
        self.view_type = view_type
        self.type = view_type       
        self.payload = payload

    def get(self, key):
        if key == "type":
            return self.view_type
        return self.payload.get(key)
