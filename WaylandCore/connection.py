# WaylandCore/connection.py
import socket
import struct
import select

class WaylandConnection:
    def __init__(self, socket_path="/run/user/1000/wayland-0"):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(socket_path)
        self.objects = {1: "wl_display"}
        self.registry = None
        self.compositor = None
        self.shm = None
        self.seat = None
        self.running = True
        
    def send(self, obj_id, opcode, payload=b""):
        length = 8 + len(payload)
        msg = struct.pack("IHH", obj_id, opcode, length) + payload
        self.sock.send(msg)
    
    def event_loop_once(self):
        r, _, _ = select.select([self.sock], [], [], 0.01)
        if r:
            data = self.sock.recv(4096)
            if data:
                self._parse_events(data)
                return True
        return False
        
    def event_loop(self):
        while self.running:
            data = self.sock.recv(4096)
            if not data:
                break
            self._parse_events(data)
    
    def _parse_events(self, data):
        offset = 0
        while offset < len(data):
            obj_id, opcode, length = struct.unpack("IHH", data[offset:offset+8])
            payload = data[offset+8:offset+length]
            
            print(f"📩 obj={obj_id}, opcode={opcode}, len={length}")
            
            if obj_id == 1:
                if opcode == 0:
                    print("  ✅ Sync OK!")
                elif opcode == 1:
                    registry_id = struct.unpack("I", payload[:4])[0]
                    print(f"  📋 Registry id={registry_id}")
                    self.registry = registry_id
                    self.objects[registry_id] = "wl_registry"
            
            elif obj_id == self.registry:
                if opcode == 0:
                    name, interface, version = self._parse_global(payload)
                    print(f"  🌐 {interface} v{version} (id={name})")
                    if interface == "wl_compositor":
                        self.compositor = name
                    elif interface == "wl_shm":
                        self.shm = name
                    elif interface == "wl_seat":
                        self.seat = name
            
            offset += length
    
    def _parse_global(self, payload):
        """Jäsennä wl_registry.global -viesti"""
        name = struct.unpack("I", payload[:4])[0]
        
        # Interface alkaa kohdasta 4
        # Etsi NULL-terminaattori
        null_pos = payload.find(b'\x00', 4)
        
        # Ota interface-nimi (nulliin asti)
        interface = payload[4:null_pos].decode('utf-8')
        
        # Versio on nullin JÄLKEEN (paddingin ohitus)
        padding = (4 - ((null_pos - 3) % 4)) % 4
        version_offset = null_pos + 1 + padding
        version = struct.unpack("I", payload[version_offset:version_offset+4])[0]
        
        return name, interface, version