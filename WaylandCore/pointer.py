"""wl_pointer  hiiren tapahtumat.

wl_pointer kertoo hiiren liikkeestä, napeista ja rullasta.
Tärkein käyttötarkoitus tässä: havaita napin painallus
ja pyytää compositoria liikuttamaan ikkunaa.
"""

import struct


# Linux input-event-koodit
BTN_LEFT = 0x110
BTN_MIDDLE = 0x111
BTN_RIGHT = 0x112

# Napin tila
STATE_RELEASED = 0
STATE_PRESSED = 1


class WaylandPointer:
    def __init__(self, conn, pointer_id):
        self.conn = conn
        self.id = pointer_id
        self.focus_surface = None
        self.last_x = 0.0
        self.last_y = 0.0
        # Callback: kutsutaan kun nappi painetaan
        # (serial, button, state)
        self.on_button = None

    def handle_event(self, obj_id, opcode, payload):
        """wl_pointer-eventit."""
        if opcode == 0:  # enter
            serial, surface_id, x, y = struct.unpack("IIff", payload[:16])
            self.focus_surface = surface_id
            self.last_x = x
            self.last_y = y
            print(f"   🖱️  pointer.enter(surface={surface_id}, x={x:.0f}, y={y:.0f})")
            return True

        if opcode == 1:  # leave
            serial, surface_id = struct.unpack("II", payload[:8])
            if self.focus_surface == surface_id:
                self.focus_surface = None
            print(f"   🖱️  pointer.leave(surface={surface_id})")
            return True

        if opcode == 2:  # motion
            time, x, y = struct.unpack("Iff", payload[:12])
            self.last_x = x
            self.last_y = y
            return True

        if opcode == 3:  # button
            serial, time, button, state = struct.unpack("IIII", payload[:16])
            state_name = "pressed" if state == STATE_PRESSED else "released"
            print(f"   🖱️  pointer.button(button=0x{button:x}, {state_name})")
            if self.on_button:
                self.on_button(serial, button, state)
            return True

        if opcode == 4:  # axis
            time, axis, value = struct.unpack("IIf", payload[:12])
            print(f"   🖱️  pointer.axis(axis={axis}, value={value:.1f})")
            return True

        return False