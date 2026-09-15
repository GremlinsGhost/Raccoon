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
print("⏳ Odotetaan seat-capabilities...")
for _ in range(100):
    conn.event_loop_once()
    if conn.pointer is not None:
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

# === GOLDEN RATIO ===
print("🌟 Piirretään golden ratio...")

PHI = 1.618033988749895

# --- Kultaisen leikkauksen viivat ---
gx = WIDTH / PHI
gy = HEIGHT / PHI

canvas.create_line(gx, 0, gx, HEIGHT, color="#ff6b35", width=2)
canvas.create_line(0, gy, WIDTH, gy, color="#ff6b35", width=2)

print(f"   Kultainen leikkaus: x={gx:.0f}, y={gy:.0f}")


# --- Fibonacci-suorakaiteet (kasvaa ulospäin) ---
def fibonacci(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


fib = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
SCALE = 6
OX, OY = 200, 300   # ensimmäisen suorakaiteen vasen yläkulma

# Bounding box
x0, y0 = OX, OY
x1, y1 = OX + fib[0] * SCALE, OY + fib[0] * SCALE

canvas.create_rectangle(x0, y0, x1, y1,
                        outline="#4ecdc4", width=2)

for i in range(1, len(fib)):
    size = fib[i] * SCALE
    direction = (i - 1) % 4   # 0=oikea, 1=alas, 2=vasen, 3=ylös

    if direction == 0:      # oikealle
        nx0, ny0 = x1, y0
        nx1, ny1 = x1 + size, y0 + size
        x1 = nx1
    elif direction == 1:    # alas
        nx0, ny0 = x0, y1
        nx1, ny1 = x0 + size, y1 + size
        y1 = ny1
    elif direction == 2:    # vasemmalle
        nx0, ny0 = x0 - size, y0
        nx1, ny1 = x0, y0 + size
        x0 = nx0
    else:                   # ylös
        nx0, ny0 = x0, y0 - size
        nx1, ny1 = x0 + size, y0
        y0 = ny0

    canvas.create_rectangle(nx0, ny0, nx1, ny1,
                            outline="#4ecdc4", width=2)

print("✅ Golden ratio + Fibonacci-suorakaiteet valmis")

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

# === Pointer callback: liikuta ikkunaa kun vasen nappi painetaan ===
def on_pointer_button(serial, button, state):
    if button == 0x110 and state == 1:   # BTN_LEFT + PRESSED
        print(f"   🚚 Pyydetään move: seat={conn.seat}, serial={serial}")
        toplevel.move(conn.seat, serial)


# Aseta callback kun pointer on luotu
if conn.pointer:
    conn.pointer.on_button = on_pointer_button


# === 7. Event loop ===
print("\n🔄 Ikkuna näkyy! Ctrl+C lopettaa.")
try:
    while True:
        conn.event_loop_once()
        time.sleep(0.01)
except KeyboardInterrupt:
    print("\n👋 Lopetetaan...")