import socket
import struct

WAYLAND_SOCKET = "/run/user/1000/wayland-0"

class WaylandDisplay:
    def __init__(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(WAYLAND_SOCKET)

    def sync(self):
        # display object id = 1
        # opcode 0 = sync
        # length = 12 bytes
        msg = struct.pack("IHHI", 1, 0, 12, 0)
        self.sock.send(msg)
