"""xdg-shell-protokolla: ikkunoiden luominen.

wl_surface on pelkkä piirtopinta. Jotta siitä tulee "oikea ikkuna"
joka näkyy KDE:ssa, tarvitaan xdg-shell-protokolla:

    wl_surface           ← piirtopinta (ei näy)
        ↓
    xdg_surface          ← "tämä on xdg-ikkuna"
        ↓
    xdg_toplevel         ← "toplevel-ikkuna" (näkyy, liikuteltavissa, jne.)

Protokolla on kaksisuuntainen:
  1. Client luo xdg_surface ja xdg_toplevel
  2. Client lähettää commitin
  3. Compositor lähettää xdg_surface.configure-eventin (koko, tila)
  4. Client kuittaa: xdg_surface.ack_configure(serial)
  5. Client piirtää sisällön ja committaa uudelleen

Tämä moduuli hoitaa kohdat 1-4. Piirtäminen (5) on surface.py:n vastuulla.
"""

import struct


class XdgWmBase:
    """xdg_wm_base – globaali joka luo xdg_surface-olioita."""

    def __init__(self, conn, xdg_wm_base_id):
        self.conn = conn
        self.id = xdg_wm_base_id
        self.pending_configure = {}  # xdg_surface_id -> serial

    def get_xdg_surface(self, wl_surface_id):
        """xdg_wm_base.get_xdg_surface(new_id, surface) — opcode 2.

        Luo xdg_surface-olion annetulle wl_surfacelle.
        Palauttaa uuden xdg_surface-ID:n.
        """
        new_id = self.conn.allocate_id()
        self.conn.objects[new_id] = "xdg_surface"

        payload = struct.pack("II", new_id, wl_surface_id)
        self.conn.send(self.id, 2, payload)
        print(f"   📐 xdg_surface id={new_id} (wl_surface={wl_surface_id})")
        return new_id

    def handle_event(self, obj_id, opcode, payload):
        """xdg_wm_base-eventit."""
        if opcode == 0:  # ping
            serial, = struct.unpack("I", payload[:4])
            print(f"   🏓 xdg_wm_base.ping(serial={serial})")
            # Vastaa pongilla
            self.conn.send(self.id, 3, struct.pack("I", serial))
            return True
        return False


class XdgSurface:
    """xdg_surface – yhdistää wl_surfacen xdg_topleveliin."""

    def __init__(self, conn, xdg_surface_id):
        self.conn = conn
        self.id = xdg_surface_id
        self.configured = False
        self.last_serial = 0

    def get_toplevel(self):
        """xdg_surface.get_toplevel(new_id) — opcode 1.

        Luo xdg_toplevel-olion. Tämä tekee surfacesta "ikkunan".
        Palauttaa xdg_toplevel-ID:n.
        """
        new_id = self.conn.allocate_id()
        self.conn.objects[new_id] = "xdg_toplevel"

        payload = struct.pack("I", new_id)
        self.conn.send(self.id, 1, payload)
        print(f"   🪟 xdg_toplevel id={new_id}")
        return new_id

    def ack_configure(self, serial):
        """xdg_surface.ack_configure(serial) — opcode 4.

        Kuittaa compositorin configure-eventin. Tämä kertoo että
        client on valmis piirtämään annetulla koolla.
        """
        payload = struct.pack("I", serial)
        self.conn.send(self.id, 4, payload)
        print(f"   ✅ ack_configure(serial={serial})")

    def handle_event(self, obj_id, opcode, payload):
        """xdg_surface-eventit."""
        if opcode == 0:  # configure
            serial, = struct.unpack("I", payload[:4])
            self.last_serial = serial
            self.configured = True
            print(f"   ⚙️  xdg_surface.configure(serial={serial})")
            # Kuittaa välittömästi
            self.ack_configure(serial)
            return True
        return False


class XdgToplevel:
    """xdg_toplevel – itse ikkuna."""

    def __init__(self, conn, toplevel_id):
        self.conn = conn
        self.id = toplevel_id
        self.title = None
        self.app_id = None
        self.width = 0
        self.height = 0
        self.closed = False

    def set_title(self, title):
        """xdg_toplevel.set_title(title) — opcode 2."""
        title_bytes = title.encode("utf-8") + b"\x00"
        title_len = len(title_bytes)
        padding = (4 - (title_len % 4)) % 4

        payload = struct.pack("I", title_len) + title_bytes + b"\x00" * padding
        self.conn.send(self.id, 2, payload)
        self.title = title
        print(f"   📛 set_title({title!r})")

    def set_app_id(self, app_id):
        """xdg_toplevel.set_app_id(app_id) — opcode 3."""
        app_bytes = app_id.encode("utf-8") + b"\x00"
        app_len = len(app_bytes)
        padding = (4 - (app_len % 4)) % 4

        payload = struct.pack("I", app_len) + app_bytes + b"\x00" * padding
        self.conn.send(self.id, 3, payload)
        self.app_id = app_id
        print(f"   🏷️  set_app_id({app_id!r})")

    def handle_event(self, obj_id, opcode, payload):
        """xdg_toplevel-eventit."""
        if opcode == 0:  # configure
            width, height = struct.unpack("ii", payload[:8])
            self.width = width
            self.height = height
            print(f"   📏 xdg_toplevel.configure(w={width}, h={height})")
            return True

        if opcode == 1:  # close
            print(f"   ❌ xdg_toplevel.close()")
            self.closed = True
            return True

        if opcode == 2:  # configure_bounds
            width, height = struct.unpack("ii", payload[:8])
            print(f"   📐 configure_bounds(w={width}, h={height})")
            return True

        if opcode == 3:  # wm_capabilities
            print(f"   🎛️  wm_capabilities")
            return True

            
    def move(self, seat_id, serial):
        """xdg_toplevel.move(seat, serial) — opcode 5.

        Pyytää compositoria aloittamaan ikkunan liikuttamisen.
        Compositor ottaa hiiren vastuun, kunnes nappi vapautetaan.
        """
        payload = struct.pack("II", seat_id, serial)
        self.conn.send(self.id, 5, payload)
        print(f"   🚚 move(seat={seat_id}, serial={serial})")

        return False