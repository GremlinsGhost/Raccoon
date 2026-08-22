import struct

class WaylandSurface:
    def __init__(self, display):
        self.display = display
        self.id = 2  # seuraava vapaa objektin ID (1 = display)

        # wl_compositor.create_surface:
        # sender = compositor_id (3)
        # opcode = 0
        # length = 8 bytes
        # new_id = self.id

        msg = struct.pack("IHHI", 3, 0, 12, self.id)
        display.sock.send(msg)

        print(f"WaylandSurface luotu, id={self.id}")
