from WaylandCore.display import WaylandDisplay
from WaylandCore.surface import WaylandSurface
from WaylandCore.buffer import WaylandBuffer

wd = WaylandDisplay()
wd.sync()


surface = WaylandSurface(wd)
buffer = WaylandBuffer(wd, 400, 200)

buffer.create_wl_buffer()

buffer.fill(0, 255, 136)  # neon green
