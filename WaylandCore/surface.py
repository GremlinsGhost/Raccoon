"""wl_surface  piirtopinta.

wl_surface on abstraktio "jollekin mitä voi piirtää". Se ei itse
sisällä pikseleitä ne tulevat wl_bufferista joka liitetään surfaceen
attach kutsulla

Tämä moduuli hoitaa vain:
  - wl_surface-olion luomisen compositorilta
  - bufferin liittämisen (attach)
  - vahinkoalueen merkitsemisen (damage)
  - muutosten lähettämisen (commit)
"""

import struct


class WaylandSurface:
    def __init__(self, conn):
        self.conn = conn
        self.id = conn.allocate_id()
        conn.objects[self.id] = "wl_surface"

        # wl_compositor.create_surface(new_id)
        # wl_compositor-opcode 0 = create_surface
        payload = struct.pack("I", self.id)
        conn.send(conn.compositor, 0, payload)

        print(f"🪟 Surface id={self.id}")

    def attach(self, buffer_id, x=0, y=0):
        """wl_surface.attach(buffer, x, y) — opcode 1.

        Liittää bufferin surfaceen. x ja y kertovat mihin kohtaan
        buffer sijoitetaan suhteessa surfaceen (yleensä 0, 0).
        """
        payload = struct.pack("Iii", buffer_id, x, y)
        self.conn.send(self.id, 1, payload)

    def damage(self, x, y, w, h):
        """wl_surface.damage(x, y, w, h) — opcode 2.

        Kertoo compositorille että alue (x, y, w, h) on muuttunut
        ja pitää piirtää uudelleen.
        """
        payload = struct.pack("iiii", x, y, w, h)
        self.conn.send(self.id, 2, payload)

    def commit(self):
        """wl_surface.commit() — opcode 6.

        Lähettää kaikki edellisen commitin jälkeen tehdyt muutokset
        compositorille. Ilman tätä mikään ei näy ruudulla.
        """
        self.conn.send(self.id, 6)
        print("✅ Committed!")