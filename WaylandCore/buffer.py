
import mmap
import os
import struct
import socket

class WaylandBuffer:
    def __init__(self, conn, width, height):
        self.conn = conn
        self.width = width
        self.height = height
        self.stride = width * 4
        self.size = self.stride * height
        
        # Luo SHM
        self.shm_name = "/raccoon-shm"
        self.fd = os.open(self.shm_name, os.O_CREAT | os.O_RDWR)
        os.ftruncate(self.fd, self.size)
        self.data = mmap.mmap(self.fd, self.size, mmap.MAP_SHARED,
                              mmap.PROT_READ | mmap.PROT_WRITE)
        print(f"SHM: {width}x{height}, {self.size} bytes")
    
    def fill_rect(self, x, y, w, h, r, g, b, a=255):
        """Täytä suorakulmio väreillä"""
        for row in range(h):
            for col in range(w):
                px = x + col
                py = y + row
                if 0 <= px < self.width and 0 <= py < self.height:
                    offset = (py * self.stride) + (px * 4)
                    self.data[offset:offset+4] = bytes([b, g, r, a])
    
    def create_wl_buffer(self):
        """Luo wl_buffer ja lähetä fd oikein"""
        shm_id = self.conn.shm
        pool_id = len(self.conn.objects) + 1
        buffer_id = pool_id + 1
        
        self.conn.objects[pool_id] = "wl_shm_pool"
        self.conn.objects[buffer_id] = "wl_buffer"
        
        # 1) wl_shm.create_pool (fd lähetetään SCM_RIGHTS:lla)
        msg = struct.pack("IHHII", shm_id, 0, 16, pool_id, self.size)
        self.conn.sock.sendmsg([msg], [(socket.SOL_SOCKET, socket.SCM_RIGHTS, struct.pack('i', self.fd))])
        
        # 2) wl_shm_pool.create_buffer
        msg = struct.pack("IHHIiii", pool_id, 0, 24, buffer_id, 0, self.width, self.height, self.stride)
        self.conn.sock.send(msg)
        
        print(f" wl_buffer id={buffer_id}")
        return buffer_id