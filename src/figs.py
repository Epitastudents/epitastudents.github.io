# Génère les schémas SVG du site (géométrie calculée, pas à l'œil).
import math

def f(x):
    return f"{x:.1f}".rstrip("0").rstrip(".") if isinstance(x, float) else str(x)

def line(x1, y1, x2, y2, c="ink", w=2.5, arrow=True, dash=None, extra=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    m = f' marker-end="url(#ar-{c})"' if arrow else ""
    return (f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" class="ln ln-{c}" '
            f'stroke-width="{w}"{d}{m}{extra}/>')

def text(x, y, s, c="ink", anchor="start", size=15, weight=None, italic=False):
    w = f' font-weight="{weight}"' if weight else ""
    it = ' font-style="italic"' if italic else ""
    return (f'<text x="{f(x)}" y="{f(y)}" class="tx tx-{c}" text-anchor="{anchor}" '
            f'font-size="{size}"{w}{it}>{s}</text>')

def vec(letter):
    return f'<tspan font-weight="700" font-style="italic">{letter}</tspan>'

def base(sub):
    return f'<tspan font-weight="700">u</tspan><tspan dy="5" font-size="0.75em" font-weight="700">{sub}</tspan>'

def arc(cx, cy, r, a0, a1, c="ink2", w=1.5):
    # angles en degrés, sens trigonométrique (y écran vers le bas)
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy - r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1))
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return (f'<path d="M{f(x0)} {f(y0)} A{f(r)} {f(r)} 0 {large} 0 {f(x1)} {f(y1)}" '
            f'class="ln ln-{c}" stroke-width="{w}" fill="none"/>')

def dot(x, y, c="ink", r=4.5):
    return f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" class="dot dot-{c}"/>'

def svg(w, h, label, body, cls="fig-svg"):
    return (f'<svg viewBox="0 0 {w} {h}" class="{cls}" role="img" aria-label="{label}">'
            + "".join(body) + "</svg>")

def axes(ox, oy, xmax, ymin, xl="x", yl="y", xmin=None, ymax=None):
    b = []
    b.append(line(ox if xmin is None else xmin, oy, xmax, oy, "ink3", 1.5))
    b.append(line(ox, oy if ymax is None else ymax, ox, ymin, "ink3", 1.5))
    b.append(text(xmax + 6, oy + 5, xl, "ink2", size=14, italic=True))
    b.append(text(ox, ymin - 8, yl, "ink2", "middle", size=14, italic=True))
    return b

# ---------- 1. Projection d'un vecteur ----------
def fig_projection(from_y=False):
    ox, oy, L, al = 70, 220, 190, 35
    b = axes(ox, oy, 300, 40)
    b.append(text(ox - 8, oy + 20, "O", "ink2", "end", 14))
    if not from_y:
        ex, ey = ox + L * math.cos(math.radians(al)), oy - L * math.sin(math.radians(al))
        b.append(line(ex, ey, ex, oy, "ink3", 1.2, False, "5 5"))
        b.append(line(ex, ey, ox, ey, "ink3", 1.2, False, "5 5"))
        b.append(line(ox, oy, ex, oy, "u1", 3.5))
        b.append(line(ox, oy, ox, ey, "u2", 3.5))
        b.append(line(ox, oy, ex, ey, "ink", 2.5))
        b.append(arc(ox, oy, 46, 0, al, "ink", 1.6))
        b.append(text(ox + 56, oy - 12, "α", "ink", size=16, weight=700))
        b.append(text(ex + 8, ey - 6, vec("F"), "ink", size=17))
        b.append(text((ox + ex) / 2, oy + 24, "F cos α", "u1", "middle", 15, 700))
        b.append(text(ox - 8, (oy + ey) / 2 + 5, "F sin α", "u2", "end", 15, 700))
    else:
        ex, ey = ox + L * math.sin(math.radians(al)), oy - L * math.cos(math.radians(al))
        b.append(line(ex, ey, ex, oy, "ink3", 1.2, False, "5 5"))
        b.append(line(ex, ey, ox, ey, "ink3", 1.2, False, "5 5"))
        b.append(line(ox, oy, ex, oy, "u1", 3.5))
        b.append(line(ox, oy, ox, ey, "u2", 3.5))
        b.append(line(ox, oy, ex, ey, "ink", 2.5))
        b.append(arc(ox, oy, 46, 90 - al, 90, "ink", 1.6))
        b.append(text(ox + 14, oy - 56, "α", "ink", size=16, weight=700))
        b.append(text(ex + 8, ey + 4, vec("F"), "ink", size=17))
        b.append(text((ox + ex) / 2, oy + 24, "F sin α", "u1", "middle", 15, 700))
        b.append(text(ox - 8, (oy + ey) / 2 + 5, "F cos α", "u2", "end", 15, 700))
    lab = "Angle mesuré depuis Oy" if from_y else "Angle mesuré depuis Ox"
    return svg(330, 260, lab, b)

# ---------- 2. Produit scalaire : trois cas ----------
def fig_scalar(kind):
    b = []
    if kind == "aigu":
        ox, oy = 40, 110
        b.append(line(ox, oy, ox + 130, oy, "ink", 2.5))
        a = 40
        vx, vy = ox + 95 * math.cos(math.radians(a)), oy - 95 * math.sin(math.radians(a))
        b.append(line(ox, oy, vx, vy, "v", 2.5))
        b.append(arc(ox, oy, 30, 0, a, "ink2", 1.4))
        b.append(text(ox + 136, oy + 5, vec("U"), "ink", size=16))
        b.append(text(vx + 6, vy - 4, vec("V"), "v", size=16))
        b.append(text(ox + 38, oy - 10, "α", "ink2", size=14))
    elif kind == "droit":
        ox, oy = 40, 110
        b.append(line(ox, oy, ox + 130, oy, "ink", 2.5))
        b.append(line(ox, oy, ox, oy - 90, "v", 2.5))
        b.append(f'<path d="M{ox+14} {oy} V{oy-14} H{ox}" class="ln ln-ink2" stroke-width="1.4" fill="none"/>')
        b.append(text(ox + 136, oy + 5, vec("U"), "ink", size=16))
        b.append(text(ox + 8, oy - 84, vec("V"), "v", size=16))
    else:
        ox, oy = 100, 90
        b.append(line(ox, oy, ox + 85, oy, "ink", 2.5))
        b.append(line(ox, oy, ox - 85, oy, "v", 2.5))
        b.append(arc(ox, oy, 22, 0, 180, "ink2", 1.4))
        b.append(text(ox + 90, oy + 5, vec("U"), "ink", size=16))
        b.append(text(ox - 90, oy + 5, vec("V"), "v", "end", size=16))
        b.append(text(ox, oy - 30, "180°", "ink2", "middle", 13))
    return svg(200, 130, "Produit scalaire : cas " + kind, b, "fig-svg mini")

# ---------- 3. Produit vectoriel ----------
def fig_cross():
    O = (80, 200)
    U = (190, 0)
    V = (80, -60)
    b = []
    p = [O, (O[0] + U[0], O[1]), (O[0] + U[0] + V[0], O[1] + V[1]), (O[0] + V[0], O[1] + V[1])]
    pts = " ".join(f"{f(float(x))},{f(float(y))}" for x, y in p)
    b.append(f'<polygon points="{pts}" class="area"/>')
    b.append(line(O[0], O[1], O[0] + U[0], O[1], "ink", 2.5))
    b.append(line(O[0], O[1], O[0] + V[0], O[1] + V[1], "v", 2.5))
    b.append(line(O[0], O[1], O[0], O[1] - 150, "a", 3))
    a = math.degrees(math.atan2(-V[1], V[0]))
    b.append(arc(O[0], O[1], 34, 0, a, "ink2", 1.4))
    b.append(text(O[0] + 44, O[1] - 8, "α", "ink2", size=14))
    b.append(text(O[0] + U[0] + 6, O[1] + 18, vec("U"), "ink", size=16))
    b.append(text(O[0] + V[0] - 6, O[1] + V[1] - 6, vec("V"), "v", "end", size=16))
    b.append(text(O[0] + 10, O[1] - 150, vec("W") + " = " + vec("U") + " ∧ " + vec("V"), "a", size=16))
    b.append(text(O[0] + U[0] / 2 + V[0] / 2 + 20, O[1] + V[1] / 2 + 5, "aire = U·V·|sin α|", "ink2", "middle", 13))
    b.append(text(O[0] + 12, O[1] - 110, "⟂ au plan de U et V", "ink2", size=13))
    return svg(400, 230, "Produit vectoriel", b)

# ---------- 4. Trajectoire, vitesse, accélération ----------
def curve_pts(fn, x0, x1, n=120):
    pts = []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        pts.append((x, fn(x)))
    return pts

def polyline(pts, c="ink2", w=2.2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    s = " ".join(f"{f(float(x))},{f(float(y))}" for x, y in pts)
    return f'<polyline points="{s}" class="ln ln-{c}" stroke-width="{w}" fill="none"{d}/>'

def fig_trajectory():
    A, k = 100, math.pi / 400
    fn = lambda x: 190 - A * math.sin(k * (x - 60))
    b = [polyline(curve_pts(fn, 60, 580), "ink2", 2.2)]
    Mx = 200.0
    My = fn(Mx)
    s = -A * k * math.cos(k * (Mx - 60))
    n = math.hypot(1, s)
    T = (1 / n, s / n)
    N = (-T[1], T[0])  # vers +y écran = intérieur du virage ici
    O = (50, 278)
    b.append(text(O[0] - 6, O[1] + 18, "O", "ink2", "end", 14))
    b.append(dot(O[0], O[1], "ink2", 3.5))
    b.append(line(O[0], O[1], Mx, My, "ink", 2.2))
    b.append(text((O[0] + Mx) / 2 - 12, (O[1] + My) / 2, vec("OM"), "ink", "end", 15))
    vx, vy = Mx + 95 * T[0], My + 95 * T[1]
    b.append(line(Mx, My, vx, vy, "v", 3))
    b.append(text(vx + 8, vy, vec("v") + " (tangente)", "v", size=15))
    ad = (0.3 * T[0] + N[0], 0.3 * T[1] + N[1])
    an = math.hypot(*ad)
    ax, ay = Mx + 78 * ad[0] / an, My + 78 * ad[1] / an
    b.append(line(Mx, My, ax, ay, "a", 3))
    b.append(text(ax + 8, ay + 14, vec("a") + " (vers l’intérieur)", "a", size=15))
    b.append(dot(Mx, My, "ink"))
    b.append(text(Mx - 10, My - 12, "M", "ink", "end", 16, 700))
    ex = 560.0
    b.append(text(ex, fn(ex) - 14, "trajectoire", "ink3", "end", 13, italic=True))
    return svg(640, 310, "Trajectoire avec vecteur position, vitesse et accélération", b)

# ---------- 5. Accéléré / décéléré ----------
def fig_speed(kind):
    b = []
    if kind in ("acc", "dec"):
        b.append(line(20, 70, 300, 70, "ink3", 1.2, False))
        x = 120
        b.append(line(x, 58, x + 100, 58, "v", 3))
        b.append(text(x + 106, 63, vec("v"), "v", size=15))
        if kind == "acc":
            b.append(line(x, 84, x + 65, 84, "a", 3))
            b.append(text(x + 71, 89, vec("a"), "a", size=15))
        else:
            b.append(line(x, 84, x - 65, 84, "a", 3))
            b.append(text(x - 71, 89, vec("a"), "a", "end", size=15))
        b.append(dot(x, 70, "ink"))
        return svg(320, 110, "accéléré" if kind == "acc" else "décéléré", b, "fig-svg mini")
    cx, cy, R = 160, 120, 80
    b.append(arc(cx, cy, R, 20, 160, "ink3", 1.2))
    ang = 90
    Mx, My = cx, cy - R
    b.append(line(Mx, My, Mx - 85, My, "v", 3))
    b.append(text(Mx - 92, My + 5, vec("v"), "v", "end", size=15))
    b.append(line(Mx, My, Mx, My + 55, "a", 3))
    b.append(text(Mx + 8, My + 55, vec("a"), "a", size=15))
    b.append(dot(Mx, My, "ink"))
    b.append(dot(cx, cy, "ink3", 3))
    return svg(320, 140, "virage à vitesse constante", b, "fig-svg mini")

# ---------- 6. Formes de trajectoires ----------
def fig_shape(kind):
    b = []
    ox, oy = 80, 70
    b.append(line(10, oy, 150, oy, "ink3", 1.1))
    b.append(line(ox, 130, ox, 8, "ink3", 1.1))
    if kind == "cercle":
        b.append(f'<circle cx="{ox}" cy="{oy}" r="42" class="ln ln-v" stroke-width="2.5" fill="none"/>')
    elif kind == "ellipse":
        b.append(f'<ellipse cx="{ox}" cy="{oy}" rx="60" ry="32" class="ln ln-v" stroke-width="2.5" fill="none"/>')
    elif kind == "droite":
        b.append(polyline([(30, 20), (140, 120)], "v", 2.5))
    else:
        b.append(polyline(curve_pts(lambda x: 120 - (100 - (x - 80) ** 2 / 36), 20, 140), "v", 2.5))
    return svg(160, 136, kind, b, "fig-svg icon")

# ---------- 8. Mouvement circulaire ----------
def fig_circular(kind):
    cx, cy, R = 150, 140, 92
    b = [f'<circle cx="{cx}" cy="{cy}" r="{R}" class="ln ln-ink3" stroke-width="1.4" fill="none"/>']
    t = math.radians(50)
    Mx, My = cx + R * math.cos(t), cy - R * math.sin(t)
    T = (-math.sin(t), -math.cos(t))
    N = (-math.cos(t), math.sin(t))
    b.append(line(cx, cy, Mx, My, "ink3", 1.2, False, "4 4"))
    b.append(text(cx + 0.3 * (Mx - cx) - 12, cy + 0.3 * (My - cy) - 8, "R", "ink2", "middle", 14, italic=True))
    b.append(dot(cx, cy, "ink2", 3.5))
    b.append(text(cx - 6, cy + 18, "O", "ink2", "end", 14))
    vx, vy = Mx + 78 * T[0], My + 78 * T[1]
    b.append(line(Mx, My, vx, vy, "v", 3))
    b.append(text(vx - 6, vy - 2, vec("v"), "v", "end", size=16))
    if kind == "uniforme":
        ax, ay = Mx + 62 * N[0], My + 62 * N[1]
        b.append(line(Mx, My, ax, ay, "a", 3))
        b.append(text(ax - 4, ay + 18, vec("a"), "a", "middle", size=16))
    else:
        aN = (Mx + 62 * N[0], My + 62 * N[1])
        aT = (Mx + 40 * T[0], My + 40 * T[1])
        ax, ay = Mx + 62 * N[0] + 40 * T[0], My + 62 * N[1] + 40 * T[1]
        b.append(line(Mx, My, aN[0], aN[1], "u2", 1.8, True, "5 4"))
        b.append(line(Mx, My, aT[0], aT[1], "u1", 1.8, True, "5 4"))
        b.append(line(aN[0], aN[1], ax, ay, "ink3", 1, False, "3 3"))
        b.append(line(aT[0], aT[1], ax, ay, "ink3", 1, False, "3 3"))
        b.append(line(Mx, My, ax, ay, "a", 3))
        b.append(text(ax - 8, ay + 4, vec("a"), "a", "end", size=16))
        b.append(text(aN[0] + 8, aN[1] + 16, "a<tspan dy='4' font-size='0.75em'>N</tspan>", "u2", size=15, weight=700))
        b.append(text(aT[0] + 8, aT[1] - 4, "a<tspan dy='4' font-size='0.75em'>T</tspan>", "u1", size=15, weight=700))
    b.append(dot(Mx, My, "ink"))
    b.append(text(Mx + 10, My + 4, "M", "ink", size=15, weight=700))
    return svg(300, 260, "Mouvement circulaire " + kind, b, "fig-svg half")

# ---------- 9. Hélice en cylindriques ----------
def fig_helix():
    cx, cy, R, pitch = 230, 340, 110, 92
    P = lambda x, y, z: (cx + x - 0.45 * y, cy + 0.32 * y - z)
    b = []
    zt = 2.25 * pitch
    b.append(line(cx, cy + 20, cx, cy - zt - 40, "ink3", 1.4))
    b.append(text(cx + 8, cy - zt - 40, "z", "ink2", size=14, italic=True))
    ax1 = P(R + 40, 0, 0)
    b.append(line(cx, cy, ax1[0], ax1[1], "ink3", 1.4))
    b.append(text(ax1[0] + 6, ax1[1] + 5, "x", "ink2", size=14, italic=True))
    ay1 = P(0, R + 60, 0)
    b.append(line(cx, cy, ay1[0], ay1[1], "ink3", 1.4))
    b.append(text(ay1[0] - 6, ay1[1] + 12, "y", "ink2", "end", 14, italic=True))
    n = 360
    tmax = 2.25 * 2 * math.pi
    seg_front, seg_back = [], []
    prev = None
    for i in range(n + 1):
        t = tmax * i / n
        p = P(R * math.cos(t), R * math.sin(t), pitch * t / (2 * math.pi))
        if prev is not None:
            front = math.sin(t) > 0
            (seg_front if front else seg_back).append((prev, p))
        prev = p
    def segs(lst, c, w, dash=None):
        out = []
        for (p0, p1) in lst:
            d = f' stroke-dasharray="{dash}"' if dash else ""
            out.append(f'<line x1="{f(p0[0])}" y1="{f(p0[1])}" x2="{f(p1[0])}" y2="{f(p1[1])}" class="ln ln-{c}" stroke-width="{w}" stroke-linecap="round"{d}/>')
        return out
    b += segs(seg_back, "ink3", 1.4)
    b += segs(seg_front, "ink2", 2.4)
    t = 2 * math.pi + math.pi / 4
    z = pitch * t / (2 * math.pi)
    M = P(R * math.cos(t), R * math.sin(t), z)
    C = P(0, 0, z)
    b.append(line(C[0], C[1], M[0], M[1], "ink3", 1.2, False, "4 4"))
    b.append(text((C[0] + M[0]) / 2, (C[1] + M[1]) / 2 - 8, "ρ = R", "ink2", "middle", 13, italic=True))
    Mp = P(R * math.cos(t), R * math.sin(t), 0)
    b.append(line(M[0], M[1], Mp[0], Mp[1], "ink3", 1, False, "3 4"))
    b.append(text(Mp[0] + 8, (M[1] + Mp[1]) / 2, "z", "ink2", size=13, italic=True))
    def tip(dx, dy, dz, L):
        p = P(R * math.cos(t) + dx * L, R * math.sin(t) + dy * L, z + dz * L)
        return p
    ur = tip(math.cos(t), math.sin(t), 0, 95)
    ut = tip(-math.sin(t), math.cos(t), 0, 62)
    uz = tip(0, 0, 1, 62)
    b.append(line(M[0], M[1], ur[0], ur[1], "u1", 3))
    b.append(line(M[0], M[1], ut[0], ut[1], "u2", 3))
    b.append(line(M[0], M[1], uz[0], uz[1], "ink", 3))
    b.append(text(ur[0] + 8, ur[1] + 6, base("ρ"), "u1", size=16))
    b.append(text(ut[0] - 8, ut[1] + 16, base("θ"), "u2", "end", size=16))
    b.append(text(uz[0] + 8, uz[1] + 4, base("z"), "ink", size=16))
    b.append(dot(M[0], M[1], "ink"))
    b.append(text(M[0] + 10, M[1] + 22, "M", "ink", size=16, weight=700))
    return svg(460, 400, "Hélice en coordonnées cylindriques", b, "fig-svg half")

# ---------- 10. Frenet ----------
def fig_frenet():
    A, k = 110, math.pi / 300
    fn = lambda x: 200 - A * math.sin(k * (x - 40))
    b = []
    Mx = 160.0
    My = fn(Mx)
    y1 = -A * k * math.cos(k * (Mx - 40))
    y2 = A * k * k * math.sin(k * (Mx - 40))
    n = math.hypot(1, y1)
    T = (1 / n, y1 / n)
    N = (-T[1], T[0])
    Rc = (1 + y1 * y1) ** 1.5 / abs(y2)
    C = (Mx + Rc * N[0], My + Rc * N[1])
    b.append(f'<circle cx="{f(C[0])}" cy="{f(C[1])}" r="{f(Rc)}" class="ln ln-ink3" stroke-width="1.3" fill="none" stroke-dasharray="6 5"/>')
    b.append(polyline(curve_pts(fn, 40, 420), "ink2", 2.4))
    b.append(line(Mx, My, C[0], C[1], "ink3", 1.3, False, "4 4"))
    b.append(dot(C[0], C[1], "ink2", 3.5))
    b.append(text(C[0] - 8, C[1] + 18, "C (centre de courbure)", "ink2", "end", 13))
    mid = (Mx + 0.72 * Rc * N[0], My + 0.72 * Rc * N[1])
    b.append(text(mid[0] + 10, mid[1], "R<tspan dy='4' font-size='0.75em'>c</tspan>", "ink2", size=15, italic=True))
    uT = (Mx + 70 * T[0], My + 70 * T[1])
    uN = (Mx + 60 * N[0], My + 60 * N[1])
    b.append(line(Mx, My, uT[0], uT[1], "u1", 3))
    b.append(line(Mx, My, uN[0], uN[1], "u2", 3))
    b.append(text(uT[0] + 6, uT[1] - 6, base("T"), "u1", size=16))
    b.append(text(uN[0] - 10, uN[1] + 4, base("N"), "u2", "end", size=16))
    b.append(dot(Mx, My, "ink"))
    b.append(text(Mx - 8, My - 12, "M", "ink", "end", 16, 700))
    b.append(text(410, fn(410) - 12, "trajectoire", "ink3", "end", 13, italic=True))
    return svg(440, 320, "Base de Frenet et rayon de courbure", b, "fig-svg half")

def fig_frenet_acc():
    M = (150, 50)
    aT, aN = 170, 110
    b = []
    b.append(line(M[0], M[1], M[0] + aT, M[1], "u1", 2, True, "6 4"))
    b.append(line(M[0], M[1], M[0], M[1] + aN, "u2", 2, True, "6 4"))
    b.append(line(M[0] + aT, M[1], M[0] + aT, M[1] + aN, "ink3", 1, False, "3 3"))
    b.append(line(M[0], M[1] + aN, M[0] + aT, M[1] + aN, "ink3", 1, False, "3 3"))
    b.append(line(M[0], M[1], M[0] + aT, M[1] + aN, "a", 3.2))
    b.append(dot(M[0], M[1], "ink"))
    b.append(text(M[0] - 10, M[1] - 8, "M", "ink", "end", 16, 700))
    b.append(text(M[0] + aT / 2, M[1] - 12, "a<tspan dy='4' font-size='0.75em'>T</tspan><tspan dy='-4'> = dv/dt</tspan>", "u1", "middle", 15, 700))
    b.append(text(M[0] - 12, M[1] + aN / 2 + 4, "a<tspan dy='4' font-size='0.75em'>N</tspan><tspan dy='-4'> = v²/R</tspan><tspan dy='4' font-size='0.75em'>c</tspan>", "u2", "end", 15, 700))
    b.append(text(M[0] + aT + 8, M[1] + aN + 6, vec("a"), "a", size=17))
    b.append(text(M[0] + aT / 2, M[1] + aN + 40, "norme : a = √(a<tspan dy='4' font-size='0.75em'>T</tspan><tspan dy='-4'>² + a</tspan><tspan dy='4' font-size='0.75em'>N</tspan><tspan dy='-4'>²)</tspan>", "ink2", "middle", 14))
    return svg(370, 220, "Décomposition de l'accélération dans la base de Frenet", b, "fig-svg half")

# ---------- 11. Projectile ----------
def fig_projectile():
    ox, oy, h = 50, 300, 46
    al = math.radians(50)
    tg = math.tan(al)
    c = tg / 400
    yup = lambda x: h + tg * x - c * x * x
    land = (tg + math.sqrt(tg * tg + 4 * c * h)) / (2 * c)
    b = []
    b.append(line(20, oy, ox + land + 50, oy, "ink3", 1.4))
    b.append(text(ox + land + 50, oy + 18, "x (sol)", "ink2", "end", 13, italic=True))
    b.append(line(ox, oy + 10, ox, 40, "ink3", 1.4))
    b.append(text(ox, 30, "y", "ink2", "middle", 14, italic=True))
    b.append(polyline([(ox + x, oy - yup(x)) for x in [land * i / 160 for i in range(161)]], "ink2", 2.2))
    # hauteur h
    b.append(line(ox - 18, oy, ox - 18, oy - h, "ink3", 1, False))
    b.append(text(ox - 24, oy - h / 2 + 5, "h", "ink2", "end", 14, italic=True))
    vx = 52.0
    pts = [("A", 0), ("M₁", 100), ("S", 200), ("M₂", 300), ("M₃", 400)]
    for name, x in pts:
        X, Y = ox + x, oy - yup(x)
        vy = vx * (tg - 2 * c * x)
        b.append(line(X, Y, X + vx, Y - vy, "v", 2.6))
        if name != "A":
            b.append(line(X, Y, X, Y + 42, "a", 2.6))
        b.append(dot(X, Y, "ink", 4))
        if name == "S":
            b.append(text(X, Y - 14, "S (sommet) : v<tspan dy='4' font-size='0.75em'>y</tspan><tspan dy='-4'> = 0</tspan>", "ink", "middle", 14, 700))
        elif name == "A":
            b.append(text(X + 10, Y + 18, "A", "ink", size=15, weight=700))
        else:
            b.append(text(X - 10, Y - 6, name, "ink", "end", 15, 700))
    A = (ox, oy - h)
    b.append(arc(A[0], A[1], 34, 0, 50, "ink2", 1.3))
    b.append(line(A[0], A[1], A[0] + 60, A[1], "ink3", 1, False, "3 3"))
    b.append(text(A[0] + 40, A[1] - 8, "α", "ink2", size=14))
    b.append(text(ox + vx + 6, oy - h - vx * tg - 2, vec("v") + "₀", "v", size=15))
    b.append(text(ox + 200 + 8, oy - yup(200) + 40, vec("a") + " = −g " + base("y"), "a", size=14))
    return svg(560, 330, "Tir d'un projectile : vitesse et accélération", b)

# ---------- Cycloïde (correction) ----------
def fig_cycloid():
    A = 26
    ox, oy = 30, 120
    pts = []
    for i in range(301):
        t = 4 * math.pi * i / 300
        pts.append((ox + A * (t - math.sin(t)), oy - A * (1 - math.cos(t))))
    b = [line(10, oy, ox + A * 4 * math.pi + 20, oy, "ink3", 1.2), line(ox, oy + 8, ox, 40, "ink3", 1.2)]
    b.append(polyline(pts, "v", 2.6))
    for i, lab in [(0, "t = 0"), (2, "T/2"), (4, "T")]:
        t = math.pi * i / 2 * 1.0
    marks = [(0, "0"), (math.pi, "T/2"), (2 * math.pi, "T"), (3 * math.pi, "3T/2"), (4 * math.pi, "2T")]
    for t, lab in marks:
        X, Y = ox + A * (t - math.sin(t)), oy - A * (1 - math.cos(t))
        b.append(dot(X, Y, "ink", 3.5))
        b.append(text(X, (Y - 10) if Y < oy - 1 else (oy + 18), lab, "ink2", "middle", 12))
    b.append(text(ox + A * math.pi, oy - 2 * A - 26, "hauteur max 2A", "ink3", "middle", 12, italic=True))
    return svg(400, 140, "Cycloïde sur deux périodes", b)

FIGS = {
    "PROJ_X": lambda: fig_projection(False),
    "PROJ_Y": lambda: fig_projection(True),
    "SC_AIGU": lambda: fig_scalar("aigu"),
    "SC_DROIT": lambda: fig_scalar("droit"),
    "SC_OPP": lambda: fig_scalar("opp"),
    "CROSS": fig_cross,
    "TRAJ": fig_trajectory,
    "SP_ACC": lambda: fig_speed("acc"),
    "SP_DEC": lambda: fig_speed("dec"),
    "SP_UNI": lambda: fig_speed("uni"),
    "SH_CERCLE": lambda: fig_shape("cercle"),
    "SH_ELLIPSE": lambda: fig_shape("ellipse"),
    "SH_DROITE": lambda: fig_shape("droite"),
    "SH_PARAB": lambda: fig_shape("parabole"),
    "CIRC_U": lambda: fig_circular("uniforme"),
    "CIRC_A": lambda: fig_circular("accéléré"),
    "HELIX": fig_helix,
    "FRENET": fig_frenet,
    "FRENET_A": fig_frenet_acc,
    "PROJECTILE": fig_projectile,
    "CYCLOID": fig_cycloid,
}
