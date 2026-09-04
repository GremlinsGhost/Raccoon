import struct

class WaylandSurface:
    def __init__(self, conn):
        self.conn = conn
        self.id = len(conn.objects) + 1
        conn.objects[self.id] = "wl_surface"
        
        # wl_compositor.create_surface
        msg = struct.pack("IHHI", conn.compositor, 0, 12, self.id)
        conn.sock.send(msg)
        print(f"🪟 Surface luotu, id={self.id}")
    
    def attach(self, buffer_id, x=0, y=0):
        """Liitä bufferi surfaceen"""
        self.conn.send(self.id, 0, struct.pack("III", buffer_id, x, y))
    
    def commit(self):
        """Näytä surface"""
        self.conn.send(self.id, 2)  # opcode 2 = commit
        print("✅ Committed!")