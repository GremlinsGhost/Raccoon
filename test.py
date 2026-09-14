
#kultanen leikkaus
PHI = 1.618033988749895

def golden_split(n):
    return n / PHI

def fibonacci(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a

# Piirto 
def draw(canvas, w, h):
    
    gx = golden_split(w)
    gy = golden_split(h)
    canvas.create_line(gx, 0, gx, h, fill="#ff6b35", width=1)
    canvas.create_line(0, gy, w, gy, fill="#ff6b35", width=1)
    
    # Fibonacci-suorakaiteet
    x, y = 0, 0
    for i in range(8):
        size = fibonacci(i) * 15
        canvas.create_rectangle(x, y, x + size, y + size,
                                outline="#4ecdc4", width=1)
        x += size

