import time
from WaylandCore.Connection import WaylandConnection
from WaylandCore.surface import WaylandSurface
from WaylandCore.buffer import WaylandBuffer

print("🔌 Yhdistetään Waylandiin...")
conn = WaylandConnection()

print("📤 Pyydetään registry...")
conn.get_registry()

print("⏳ Odotetaan globaaleja...")
for _ in range(200):
    conn.event_loop_once()
    if len(conn.globals) >= 40:
        break
    time.sleep(0.01)

print("🔗 Bindataan tarvittavat globaalit...")
conn.bind_globals()

print(f"\n📋 Compositor ID: {conn.compositor}")
print(f"📋 SHM ID: {conn.shm}")
print(f"📋 Seat ID: {conn.seat}")
print(f"📋 xdg_wm_base ID: {conn.xdg_wm_base}")

if conn.compositor is None or conn.shm is None or conn.xdg_wm_base is None:
    print("❌ Compositor, SHM tai xdg_wm_base puuttuu!")
    exit(1)

# 1. Luo wl_surface (EI bufferiä vielä)
print("\n🪟 Luodaan wl_surface...")
surface = WaylandSurface(conn)

# 2. Luo xdg-ikkuna HETI 
print("\n🪟 Luodaan xdg-ikkuna...")
xdg_surface, toplevel = conn.create_window(
    surface.id,
    title="Raccoon",
    app_id="raccoon"
)

# 3. Commit ilman bufferiä – tämä lähettää "configure pyydetty" 
print("📤 commit (ilman bufferiä)...")
surface.commit()

# 4. Odota configure-eventtiä 
print("⏳ Odotetaan configure...")
for _ in range(200):
    conn.event_loop_once()
    if xdg_surface.configured and toplevel.width > 0:
        break
    time.sleep(0.01)

if not xdg_surface.configured:
    print("⚠️  Ei saatu configurea, mutta jatketaan...")
else:
    print(f"✅ Configure saatu: serial={xdg_surface.last_serial}")
    print(f"   Koko: {toplevel.width}x{toplevel.height}")

# === 5. Nyt luodaan buffer ja piirretään ===
print("\n📦 Luodaan buffer...")
buffer = WaylandBuffer(conn, 800, 600)

print("🎨 Piirretään...")
buffer.fill_rect(0, 0, 800, 28, 0x44, 0x44, 0x88)      # topbar sininen
buffer.fill_rect(0, 576, 800, 24, 0x33, 0x33, 0x33)    # bottombar harmaa

print("🖼️ Luodaan wl_buffer...")
buffer_id = buffer.create_wl_buffer()

# === 6. Attach + damage + commit ===
print("📤 attach...")
surface.attach(buffer_id)

print("📤 damage...")
surface.damage(0, 0, 800, 600)

print("📤 commit...")
surface.commit()

print("\n🔄 Ikkuna näkyy! Ctrl+C lopettaa.")
try:
    while True:
        conn.event_loop_once()
except KeyboardInterrupt:
    print("\n👋 Lopetetaan...")