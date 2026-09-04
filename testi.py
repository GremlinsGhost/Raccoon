# testi.py - KOKO HOMAN TESTI
import struct
import time
from WaylandCore.connection import WaylandConnection
from WaylandCore.surface import WaylandSurface
from WaylandCore.buffer import WaylandBuffer

# 1) Yhdistetään
print("🔌 Yhdistetään Waylandiin...")
conn = WaylandConnection()

# 2) Lähetetään sync + get_registry
print("📤 Lähetetään sync...")
conn.send(1, 0, struct.pack("I", 2))  # callback_id=2

print("📤 Lähetetään get_registry...")
conn.send(1, 1, struct.pack("I", 3))  # new_id=3

# 3) Odotetaan että registry vastaa
print("⏳ Odotetaan registryä...")
for _ in range(50):
    conn.event_loop_once()
    if conn.compositor is not None:
        break
    time.sleep(0.01)

# 4) Tulostetaan saadut ID:t
print(f"\n📋 Compositor ID: {conn.compositor}")
print(f"📋 SHM ID: {conn.shm}")
print(f"📋 Seat ID: {conn.seat}")

if conn.compositor is None:
    print("❌ Ei saatu compositoria!")
    exit()

# 5) Luodaan surface
print("\n🪟 Luodaan surface...")
surface = WaylandSurface(conn)

# 6) Luodaan buffer
print("📦 Luodaan buffer...")
buffer = WaylandBuffer(conn, 800, 600)

# 7) Piirretään topbar (sininen)
print("🎨 Piirretään topbar...")
buffer.fill_rect(0, 0, 800, 28, 0x44, 0x44, 0x88)   # sininen

# 8) Piirretään bottombar (harmaa)
print("🎨 Piirretään bottombar...")
buffer.fill_rect(0, 576, 800, 24, 0x33, 0x33, 0x33) # harmaa

# 9) Luodaan wl_buffer ja näytetään
print("🖼️ Luodaan wl_buffer...")
buffer_id = buffer.create_wl_buffer()

print("📤 Liitetään bufferi surfaceen...")
surface.attach(buffer_id)

print("📤 Commit...")
surface.commit()

# 10) Jäädään event loopiin (jotta ikkuna pysyy auki)
print("\n🔄 Ikkuna näkyy! Paina Ctrl+C lopettaaksesi.")
try:
    conn.event_loop()
except KeyboardInterrupt:
    print("\n👋 Lopetetaan...")