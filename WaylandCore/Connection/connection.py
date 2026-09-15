"""Wayland-yhteys: yhdistäminen, ID allokointi, event dispatch."""

import os
import struct

from .wire import Wire
from .registry import parse_global


class WaylandConnection:
    def __init__(self, socket_path=None):
        if socket_path is None:
            runtime_dir = os.environ.get("XDG_RUNTIME_DIR")
            display = os.environ.get("WAYLAND_DISPLAY", "wayland-0")
            if not runtime_dir:
                raise RuntimeError("XDG_RUNTIME_DIR ei asetettu")
            socket_path = os.path.join(runtime_dir, display)

        self.wire = Wire(socket_path)

        self.objects = {1: "wl_display"}
        self.next_id = 2
        self.globals = {} 

        self.registry = None
        self.compositor = None
        self.shm = None
        self.seat = None
        self.xdg_wm_base = None
        self.xdg_handler = None          # XdgWmBase-instanssi
        self.xdg_surfaces = {}           # {id: XdgSurface}
        self.xdg_toplevels = {}          # {id: XdgToplevel}
        self.seat_obj = None         # hiiri 
        self.pointer = None          # hiiren liikkeet
        self.callbacks = {}


    def allocate_id(self):
        oid = self.next_id
        self.next_id += 1
        return oid

    def send(self, obj_id, opcode, payload=b""):
        self.wire.send(obj_id, opcode, payload)

    def send_with_fd(self, obj_id, opcode, payload, fd):
        self.wire.send_with_fd(obj_id, opcode, payload, fd)

    def sync(self, callback=None):
        cb_id = self.allocate_id()
        self.objects[cb_id] = "wl_callback"
        if callback:
            self.callbacks[cb_id] = callback
        self.send(1, 0, struct.pack("I", cb_id))
        return cb_id

    def get_registry(self):
        reg_id = self.allocate_id()
        self.objects[reg_id] = "wl_registry"
        self.registry = reg_id
        self.send(1, 1, struct.pack("I", reg_id))
        return reg_id


    def bind_globals(self):
        targets = []
        for name, (interface, version) in self.globals.items():
            if interface in ("wl_compositor", "wl_shm", "wl_seat", "xdg_wm_base"):
                targets.append((name, interface, version))

        for name, interface, version in targets:
            if interface == "wl_compositor":
                self.compositor = self.bind(name, interface, min(version, 4))
                print(f"     → bind: wl_compositor id={self.compositor}")
            elif interface == "wl_shm":
                self.shm = self.bind(name, interface, 1)
                print(f"     → bind: wl_shm id={self.shm}")
            elif interface == "wl_seat":
                self.seat = self.bind(name, interface, min(version, 7))
                print(f"     → bind: wl_seat id={self.seat}")
                # Luo WaylandSeat-instanssi
                from ..seat import WaylandSeat
                self.seat_obj = WaylandSeat(self, self.seat)
            elif interface == "xdg_wm_base":
                self.xdg_wm_base = self.bind(name, interface, min(version, 4))
                print(f"     → bind: xdg_wm_base id={self.xdg_wm_base}")

            self.event_loop_once()


    def create_window(self, wl_surface_id, title="Raccoon", app_id="raccoon"):
        """Luo xdg-ikkunan annetulle wl_surfacelle.

        Palauttaa (xdg_surface, xdg_toplevel) -parin.
        """
        from ..xdg import XdgWmBase, XdgSurface, XdgToplevel

        if self.xdg_wm_base is None:
            raise RuntimeError("xdg_wm_base ei ole bindattu")

        # Luo XdgWmBase-instanssi (eventtien käsittelyä varten)
        if self.xdg_handler is None:
            self.xdg_handler = XdgWmBase(self, self.xdg_wm_base)

        # 1) Luo xdg_surface
        xdg_surface_id = self.xdg_handler.get_xdg_surface(wl_surface_id)
        xdg_surface = XdgSurface(self, xdg_surface_id)
        self.xdg_surfaces[xdg_surface_id] = xdg_surface

        # 2) Luo xdg_toplevel
        toplevel_id = xdg_surface.get_toplevel()
        toplevel = XdgToplevel(self, toplevel_id)
        self.xdg_toplevels[toplevel_id] = toplevel

        # 3) Aseta otsikko ja app_id
        toplevel.set_title(title)
        toplevel.set_app_id(app_id)

        return xdg_surface, toplevel


        
    def bind(self, name, interface, version):
        new_id = self.allocate_id()

        iface_bytes = interface.encode("utf-8") + b"\x00"   # ← NULL mukaan
        iface_len = len(iface_bytes)
        padding = (4 - (iface_len % 4)) % 4

        payload = struct.pack("I", name)
        payload += struct.pack("I", iface_len) + iface_bytes + b"\x00" * padding
        payload += struct.pack("I", version)
        payload += struct.pack("I", new_id)



        self.send(self.registry, 0, payload)
        self.objects[new_id] = interface
        return new_id


    def event_loop_once(self):
        if not self.wire.recv_available(timeout=0.01):
            return False
        for obj_id, opcode, payload in self.wire.drain():
            self._handle_event(obj_id, opcode, payload)
        return True

    def event_loop(self):
        while not self.wire.closed:
            self.event_loop_once()

    def _handle_event(self, obj_id, opcode, payload):
        if obj_id == 1:
            self._handle_display(opcode, payload)
            return

        if obj_id == self.registry and opcode == 0:
            self._handle_registry_global(payload)
            return

        # wl_callback.done
        if self.objects.get(obj_id) == "wl_callback" and opcode == 0:
            cb = self.callbacks.pop(obj_id, None)
            if cb:
                cb()
            return

        # xdg_wm_base-eventit
        if self.objects.get(obj_id) == "xdg_wm_base" and self.xdg_handler:
            if self.xdg_handler.handle_event(obj_id, opcode, payload):
                return

        # xdg_surface-eventit
        if self.objects.get(obj_id) == "xdg_surface":
            handler = self.xdg_surfaces.get(obj_id)
            if handler and handler.handle_event(obj_id, opcode, payload):
                return

        # xdg_toplevel-eventit
        if self.objects.get(obj_id) == "xdg_toplevel":
            handler = self.xdg_toplevels.get(obj_id)
            if handler and handler.handle_event(obj_id, opcode, payload):
                return


        # wl_seat-eventit
        if self.seat_obj and obj_id == self.seat:
            if self.seat_obj.handle_event(obj_id, opcode, payload):
                return

        # wl_pointer-eventit
        if self.pointer and obj_id == self.pointer.id:
            if self.pointer.handle_event(obj_id, opcode, payload):
                return

        print(f"📩 obj={obj_id}, opcode={opcode}, len={len(payload)}")

    def _handle_display(self, opcode, payload):
        if opcode == 0:
            # error
            if len(payload) >= 12:
                err_obj, err_code = struct.unpack("II", payload[:8])
                msg_len, = struct.unpack("I", payload[8:12])
                msg = payload[12:12 + msg_len].decode("utf-8", errors="replace")
                print(f"❌ Wayland error: obj={err_obj} code={err_code} msg={msg}")
            self.wire.closed = True
            return

        if opcode == 1:
            # delete_id – älä ylikirjoita self.registry
            deleted_id, = struct.unpack("I", payload[:4])
            print(f"     🗑️ delete_id({deleted_id})")
            return

        print(f"📩 wl_display opcode={opcode} len={len(payload)}")

    def _handle_registry_global(self, payload):
        name, interface, version = parse_global(payload)
        print(f"  🌐 {interface} v{version} (name={name})")

        # Tallenna globaali talteen – EI bindata vielä
        self.globals[name] = (interface, version)