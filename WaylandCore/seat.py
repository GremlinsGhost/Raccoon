"""wl_seat – input-laitteet (hiiri, näppäimistö, kosketus).

wl_seat edustaa yhtä "istuinta" – käytännössä yhtä käyttäjää
istumassa koneen ääressä. Se tarjoaa pääsyn hiireen,
näppäimistöön ja kosketusnäyttöön.

Tämä moduuli hoitaa:
  - wl_seat-olion bindauksen (Connection.bind_globals tekee tämän)
  - wl_pointer-olion luomisen
  - wl_seat-eventtien käsittelyn (capabilities, name)
"""

import struct


class WaylandSeat:
    def __init__(self, conn, seat_id):
        self.conn = conn
        self.id = seat_id
        self.capabilities = 0
        self.pointer = None
        self.name = None

    def get_pointer(self):
        from .pointer import WaylandPointer

        pointer_id = self.conn.allocate_id()
        self.conn.objects[pointer_id] = "wl_pointer"

        payload = struct.pack("I", pointer_id)
        self.conn.send(self.id, 0, payload)

        self.pointer = WaylandPointer(self.conn, pointer_id)
        self.conn.pointer = self.pointer      # ← TÄMÄ
        print(f"   🖱️  wl_pointer id={pointer_id}")
        return self.pointer

    def handle_event(self, obj_id, opcode, payload):
        """wl_seat-eventit."""
        if opcode == 0:  # capabilities
            self.capabilities, = struct.unpack("I", payload[:4])
            print(f"   🎛️  seat.capabilities = 0x{self.capabilities:x}")
            # Jos hiiri löytyy ja sitä ei ole vielä luotu
            if self.capabilities & 1 and self.pointer is None:
                self.get_pointer()
            return True
        if opcode == 1:  # name
            name_len, = struct.unpack("I", payload[:4])
            self.name = payload[4:4 + name_len].rstrip(b"\x00").decode("utf-8")
            print(f"   🪑 seat.name = {self.name!r}")
            return True
        return False