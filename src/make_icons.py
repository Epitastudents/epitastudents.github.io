# Dessine l'icône de l'application : une trajectoire, le point M, la vitesse (bleu) et l'accélération (orange).
import math
import os
import sys
from PIL import Image, ImageDraw

OUT = sys.argv[1] if len(sys.argv) > 1 else "icons"
S = 2048  # dessin en haute définition puis réduction (anti-crénelage)

BG = (20, 28, 51)
GRID = (30, 41, 70)
CURVE = (201, 211, 234)
V = (92, 168, 255)
A = (255, 123, 94)
DOT = (255, 255, 255)


def P(x, y, k):
    """Coordonnées unitaires -> pixels, avec un facteur k de réduction autour du centre."""
    return ((0.5 + (x - 0.5) * k) * S, (0.5 + (y - 0.5) * k) * S)


def arrow(d, x0, y0, dx, dy, length, color, k, width=0.042, head=0.085):
    n = math.hypot(dx, dy)
    ux, uy = dx / n, dy / n
    x1, y1 = x0 + ux * length, y0 + uy * length
    bx, by = x1 - ux * head, y1 - uy * head
    d.line([P(x0, y0, k), P(bx, by, k)], fill=color, width=int(width * S * k))
    px, py = -uy, ux
    h = head * 0.62
    d.polygon([P(x1, y1, k), P(bx + px * h, by + py * h, k), P(bx - px * h, by - py * h, k)], fill=color)


def draw(k):
    im = Image.new("RGB", (S, S), BG)
    d = ImageDraw.Draw(im)
    step = S / 8
    for i in range(1, 8):
        d.line([(i * step, 0), (i * step, S)], fill=GRID, width=int(S * 0.006))
        d.line([(0, i * step), (S, i * step)], fill=GRID, width=int(S * 0.006))
    f = lambda x: 0.46 + 2.4 * (x - 0.5) ** 2
    rr = 0.015 * S * k
    for i in range(1201):
        x = 0.16 + i * (0.68 / 1200)
        cx0, cy0 = P(x, f(x), k)
        d.ellipse([cx0 - rr, cy0 - rr, cx0 + rr, cy0 + rr], fill=CURVE)
    mx = 0.37
    my = f(mx)
    slope = 4.8 * (mx - 0.5)
    arrow(d, mx, my, 1, slope, 0.33, V, k)
    arrow(d, mx, my, -slope, 1, 0.24, A, k)
    r = 0.045 * S * k
    cx, cy = P(mx, my, k)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=DOT)
    return im


os.makedirs(OUT, exist_ok=True)
full = draw(1.0)          # icône standard : le dessin occupe la tuile
safe = draw(0.78)         # icône « maskable » : le dessin reste dans la zone sûre (cercle de 80 %)
for size in (192, 512):
    full.resize((size, size), Image.LANCZOS).save(os.path.join(OUT, f"icon-{size}.png"), optimize=True)
    safe.resize((size, size), Image.LANCZOS).save(os.path.join(OUT, f"maskable-{size}.png"), optimize=True)
safe.resize((180, 180), Image.LANCZOS).save(os.path.join(OUT, "apple-touch-icon.png"), optimize=True)
full.resize((64, 64), Image.LANCZOS).save(os.path.join(OUT, "favicon-64.png"), optimize=True)
print("icônes écrites dans", OUT)
