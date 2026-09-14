"""wl_buffer – pikselidata.

wl_buffer on abstraktio "jollekulle pikselijoukolle". Se luodaan
jakamalla muistialue (SHM) compositorin kanssa, ja täyttämällä se
piirtämällä.

Tämä moduuli hoitaa:
  - SHM-muistialueen luomisen (memfd_create)
  - wl_shm_pool-olion luomisen compositorilla
  - wl_buffer-olion luomisen poolista
  - Pikselien kirjoittamisen muistiin
"""

import mmap
import os
import struct


# Waylandin vakioformaatti 32-bittiselle RGB:lle
# 0xAARRGGBB, alpha-kanava jätetään huomiotta (X = unused)
WL_SHM_FORMAT_XRGB8888 = 1


class WaylandBuffer:
    def __init__(self, conn, width, height):
        self.conn = conn
        self.width = width
        self.height = height
        self.stride = width * 4
        self.size = self.stride * height

        # Luo jaettu muistialue
        # memfd_create on Linux-spesifi, ei luo tiedostoa levylle
        self.fd = os.memfd_create("raccoon-shm")
        os.ftruncate(self.fd, self.size)

        self.data = mmap.mmap(
            self.fd, self.size,
            mmap.MAP_SHARED,
            mmap.PROT_READ | mmap.PROT_WRITE,
        )

        print(f"📦 SHM: {width}x{height}, {self.size} bytes, fd={self.fd}")

    def fill_rect(self, x, y, w, h, r, g, b, a=255):
        """Täytä suorakulmio värillä.

        Waylandin XRGB8888-formaatissa tavut ovat muistissa:
          [B, G, R, X]  (little-endian)
        """
        for row in range(h):
            for col in range(w):
                px = x + col
                py = y + row
                if 0 <= px < self.width and 0 <= py < self.height:
                    offset = (py * self.stride) + (px * 4)
                    self.data[offset:offset + 4] = bytes([b, g, r, a])

    def create_wl_buffer(self):
        """Luo wl_shm_pool ja wl_buffer, palauttaa bufferin ID:n."""
        shm_id = self.conn.shm
        if shm_id is None:
            raise RuntimeError("wl_shm ei ole vielä rekisteröitynyt")

        pool_id = self.conn.allocate_id()
        buffer_id = self.conn.allocate_id()

        self.conn.objects[pool_id] = "wl_shm_pool"
        self.conn.objects[buffer_id] = "wl_buffer"

        # 1) wl_shm.create_pool(new_id, size, fd)
        #    Opcode 0, fd lähetetään SCM_RIGHTS-ancillary-datana
        payload = struct.pack("II", pool_id, self.size)
        self.conn.send_with_fd(shm_id, 0, payload, self.fd)

        # 2) wl_shm_pool.create_buffer(new_id, offset, width, height, stride, format)
        #    Opcode 0
        payload = struct.pack(
            "IIIII",
            buffer_id,
            0,              # offset
            self.width,
            self.height,
            self.stride,
        ) + struct.pack("I", WL_SHM_FORMAT_XRGB8888)
        self.conn.send(pool_id, 0, payload)

        print(f"🖼️  wl_buffer id={buffer_id} (pool id={pool_id})")
        return buffer_id