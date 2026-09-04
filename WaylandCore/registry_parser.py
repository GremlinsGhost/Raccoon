#registryn jäsentelyyn


def parse_global(payload):
    """Jäsennä wl_registry.global -payload"""
    import struct
    
    name = struct.unpack("I", payload[:4])[0]
    interface_len = payload[4]
    interface = payload[5:5+interface_len].decode('utf-8')
    
    # Version alkaa kohdasta 5 + interface_len + 1 (null)
    version_offset = 5 + interface_len + 1
    while version_offset % 4 != 0:
        version_offset += 1
    version = struct.unpack("I", payload[version_offset:version_offset+4])[0]
    
    return name, interface, version