import mmap
import os
import struct
import ctypes

class WaylandBuffer:
    def __init__(self, display, width, height):
        self.display = display
        self.width = width
        self.height = height
        self.stride = width * 4  # ARGB8888 = 4 bytes per pixel
        self.size = self.stride * height

        # 1) Luo POSIX shared memory -tiedosto
        self.shm_name = "/raccoon-shm"
        fd = os.open(self.shm_name, os.O_CREAT | os.O_RDWR)
        os.ftruncate(fd, self.size)

        # 2) mmap buffer
        self.data = mmap.mmap(fd, self.size, mmap.MAP_SHARED,
                              mmap.PROT_READ | mmap.PROT_WRITE)

        print(f"SHM-buffer luotu: {self.width}x{self.height}, {self.size} bytes")

    def fill(self, r, g, b, a=255):
        for y in range(self.height):
            for x in range(self.width):
                offset = (y * self.stride) + (x * 4)
                self.data[offset:offset+4] = bytes([b, g, r, a])
    def create_wl_buffer(self):
        # wl_shm id = 4 (me annetaan se itse)
        # wl_shm_pool id = 5
        # wl_buffer id = 6

        self.shm_id = 4
        self.pool_id = 5
        self.buffer_id = 6

        # 1) wl_shm.create_pool
        # sender = shm_id
        # opcode = 0
        # length = 16 bytes
        # fd = 0 (ei oikea fd, mutta Python ei voi lähettää oikeaa)
        # size = self.size

        msg_pool = struct.pack("IHHIi", self.shm_id, 0, 16, 0, self.size)
        self.display.sock.send(msg_pool)

        # 2) wl_shm_pool.create_buffer
        # sender = pool_id
        # opcode = 0
        # length = 24 bytes
        # new_id = buffer_id
        # offset = 0
        # width, height, stride, format = ARGB8888 (0)

        msg_buffer = struct.pack(
            "IHHIiii",
            self.pool_id, 0, 24,
            self.buffer_id,
            0,  # offset
            self.width,
            self.height,
            self.stride
        )

        self.display.sock.send(msg_buffer)

        print(f"wl_buffer luotu id={self.buffer_id}")
