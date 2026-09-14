# testaa_struct.py
import socket
import struct
import time

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect("/run/user/1000/wayland-0")

sock.send(struct.pack("IHHI", 1, 0, 12, 2))  # sync
sock.send(struct.pack("IHHI", 1, 1, 12, 3))  # registry

time.sleep(0.1)

data = sock.recv(8192)
offset = 0

while offset < len(data):
    obj_id, opcode, length = struct.unpack("IHH", data[offset:offset+8])
    payload = data[offset+8:offset+length]
    
    if obj_id == 2 and opcode == 0:
        print("✅ Sync callback")
    elif obj_id == 1 and opcode == 1:
        print("📋 Registry")
    elif obj_id == 3 and opcode == 0:
        # 1) Lue name
        name = struct.unpack("I", payload[:4])[0]
        
        # 2) Lue interfacen pituus (tavuissa)
        interface_len = payload[4]
        
        # 3) Interface alkaa kohdasta 5
        interface = payload[5:5+interface_len].decode('utf-8')
        
        # 4) Version alkaa kohdasta 5 + interface_len + 1 (null)
        version_offset = 5 + interface_len + 1
        # Tarkista padding (4-tavun raja)
        while version_offset % 4 != 0:
            version_offset += 1
        version = struct.unpack("I", payload[version_offset:version_offset+4])[0]
        
        # Korjaa interface-nimi (poista ylimääräiset merkit)
        interface = interface.strip('\x00')
        
        print(f"  🌐 {interface} v{version} (id={name})")
        
        if interface == "wl_compositor":
            print(f"    ✅ Compositor id={name}")
        elif interface == "wl_shm":
            print(f"    ✅ SHM id={name}")
        elif interface == "wl_seat":
            print(f"    ✅ Seat id={name}")
    
    offset += length

sock.close()