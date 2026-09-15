import time

from WaylandCore.Connection import WaylandConnection
from WaylandCore.surface import WaylandSurface
from WaylandCore.buffer import WaylandBuffer

from UiLayout.UiLayoutManager import UiLayoutManager
from UiLayout.SkinModel import default_skin
from RaccoonCanvas import RaccoonCanvas


# === 1. Yhdistä Waylandiin ===
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

if conn.compositor is None or conn.shm is None or conn.xdg_wm_base is None:
    print("❌ Compositor, SHM tai xdg_wm_base puuttuu!")
    exit(1)


# === 2. Luo wl_surface + xdg-ikkuna ===
print("\n🪟 Luodaan ikkuna...")
surface = WaylandSurface(conn)

xdg_surface, toplevel = conn.create_window(
    surface.id,
    title="Raccoon",
    app_id="raccoon"
)

surface.commit()

print("⏳ Odotetaan configure...")
for _ in range(200):
    conn.event_loop_once()
    if xdg_surface.configured:
        break
    time.sleep(0.01)


# === 3. Raccoon UI:n layout ===
print("\n📐 Rakennetaan layout...")
skin = default_skin()

layout_rows = [
    {"content_type": "Stage",      "col": 0, "row": 0},
    {"content_type": "Log",        "col": 0, "row": 1},
    {"content_type": "Properties", "col": 1, "row": 0},
    {"content_type": "Tools",      "col": 1, "row": 1},
]

WIDTH = 1280
HEIGHT = 720

layout = UiLayoutManager(
    width=WIDTH,
    height=HEIGHT,
    layout_rows=layout_rows
)

print("Rects:")
for name, r in layout.rects.items():
    print(f"  {name:12s} x={r.x:4d} y={r.y:4d} w={r.w:4d} h={r.h:4d}")


# === 4. Buffer ===
print("\n📦 Luodaan buffer...")
buffer = WaylandBuffer(conn, WIDTH, HEIGHT)


# === 5. Maalataan layout bufferoon ===
print("🎨 Maalataan layout...")
canvas = RaccoonCanvas(buffer, skin=skin)
canvas.paint_layout(layout)

# === GOLDEN SPIRAL ===
import math

print("✨ Piirretään golden spiral...")

# Fibonacci-luvut
fib = [1, 1]
for _ in range(15):
    fib.append(fib[-1] + fib[-2])

# Aloita keskeltä
cx = 640
cy = 400

# Piirretään neliöt ja niiden sisään neljännesympyrät
# Jokainen neliö on käännetty 90° edelliseen verrattuna
for i in range(len(fib) - 1):
    size = fib[i] * 8   # skaalauskerroin

    # Kulma kertoo mihin suuntaan piirretään
    angle = i * (math.pi / 2)
    dir_x = math.cos(angle)
    dir_y = math.sin(angle)

    # Piirretään neljännesympyrä
    # (yksinkertaistettu: pisteitä käyrällä)
    for t in range(0, 90):
        theta = math.radians(t + i * 90)
        radius = size
        x = int(cx + math.cos(theta) * radius * dir_x - math.sin(theta) * radius * dir_y)
        y = int(cy + math.sin(theta) * radius * dir_x + math.cos(theta) * radius * dir_y)

        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            buffer.fill_rect(x, y, 2, 2, 0xFF, 0xD7, 0x00)  # kultainen väri

    # Siirretään keskipistettä
    cx += int(size * dir_y)
    cy -= int(size * dir_x)

print("✅ Golden spiral valmis")

# === 6. Attach + damage + commit ===
print("🖼️ Luodaan wl_buffer...")
buffer_id = buffer.create_wl_buffer()

print("📤 attach...")
surface.attach(buffer_id)

print("📤 damage...")
surface.damage(0, 0, WIDTH, HEIGHT)

print("📤 commit...")
surface.commit()


# === 7. Event loop ===
print("\n🔄 Ikkuna näkyy! Ctrl+C lopettaa.")
try:
    while True:
        conn.event_loop_once()
        time.sleep(0.01)
except KeyboardInterrupt:
    print("\n👋 Lopetetaan...")