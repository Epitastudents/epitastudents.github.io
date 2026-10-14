# Schémas supplémentaires pour le cours de mécanique (forces, ressort, pendule, ondes…).
# Même style que figs.py : classes CSS liées aux couleurs du thème.
import math
from figs import line, text, vec, base, arc, dot, svg, polyline, axes


def sub(s, i):
    return f"{s}<tspan dy='4' font-size='0.75em'>{i}</tspan><tspan dy='-4'></tspan>"


# ---------- Plan incliné : poids, réaction, frottement ----------
def fig_incline():
    a = math.radians(30)
    x0, y0, L = 40, 250, 360
    x1, y1 = x0 + L * math.cos(a), y0 - L * math.sin(a)
    b = [f'<polygon points="{x0},{y0} {x1:.1f},{y0} {x1:.1f},{y1:.1f}" class="area"/>',
         line(x0, y0, x1, y1, "ink2", 2, False), line(x0, y0, x1 + 10, y0, "ink3", 1.2, False)]
    b.append(arc(x0, y0, 52, 0, 30, "ink2", 1.4))
    b.append(text(x0 + 62, y0 - 10, "α", "ink2", size=15))
    t = 0.55
    Mx, My = x0 + t * L * math.cos(a), y0 - t * L * math.sin(a)
    ux = (-math.cos(a), math.sin(a))      # le long de la pente, vers le bas
    uy = (-math.sin(a), -math.cos(a))     # perpendiculaire, vers le haut (écran)
    P = 95
    b.append(line(Mx, My, Mx, My + P, "a", 3))
    b.append(text(Mx + 8, My + P + 4, vec("P"), "a", size=16))
    px, py = P * math.sin(a), P * math.cos(a)
    b.append(line(Mx, My, Mx + ux[0] * px, My + ux[1] * px, "a", 1.6, True, "5 4"))
    b.append(line(Mx, My, Mx - uy[0] * py, My - uy[1] * py, "a", 1.6, True, "5 4"))
    b.append(text(Mx + ux[0] * px - 6, My + ux[1] * px + 18, sub("P", "x"), "a", "end", 14))
    b.append(text(Mx - uy[0] * py + 8, My - uy[1] * py + 16, sub("P", "y"), "a", size=14))
    b.append(line(Mx, My, Mx + uy[0] * py, My + uy[1] * py, "v", 3))
    b.append(text(Mx + uy[0] * py - 6, My + uy[1] * py - 6, vec("R"), "v", "end", 16))
    b.append(line(Mx, My, Mx - ux[0] * px, My - ux[1] * px, "u2", 3))
    b.append(text(Mx - ux[0] * px + 6, My - ux[1] * px - 8, vec("f"), "u2", size=16))
    b.append(dot(Mx, My, "ink", 5))
    b.append(text(40, 286, "Équilibre : P + R + f = 0", "ink2", size=14))
    return svg(460, 300, "Plan incliné : poids, réaction et frottement", b, "fig-svg half")


# ---------- Travail d'une force ----------
def fig_work():
    A, B, y = 60, 360, 170
    th = math.radians(30)
    b = [line(A, y, B, y, "ink", 2.4), text(A - 6, y + 22, "A", "ink", "middle", 15, 700), text(B + 6, y + 22, "B", "ink", "middle", 15, 700)]
    b.append(dot(A, y, "ink", 4))
    Mx = 150
    F = 150
    fx, fy = Mx + F * math.cos(th), y - F * math.sin(th)
    b.append(line(Mx, y, fx, fy, "a", 3))
    b.append(text(fx + 8, fy, vec("F"), "a", size=16))
    b.append(line(Mx, y, fx, y, "u1", 2, True, "6 4"))
    b.append(line(fx, y, fx, fy, "ink3", 1, False, "3 3"))
    b.append(text((Mx + fx) / 2, y + 22, "F cos θ (travaille)", "u1", "middle", 13, 700))
    b.append(line(Mx, y, Mx, fy, "u2", 2, True, "6 4"))
    b.append(text(Mx - 8, fy + 14, "F sin θ (ne travaille pas)", "u2", "end", 13, 700))
    b.append(arc(Mx, y, 44, 0, 30, "ink2", 1.3))
    b.append(text(Mx + 52, y - 8, "θ", "ink2", size=14))
    b.append(text(210, 222, "W = F · AB · cos θ", "ink", "middle", 15, 700))
    return svg(420, 240, "Travail d'une force constante", b, "fig-svg half")


# ---------- Ressort horizontal ----------
def spring_path(x0, x1, y, n=10, amp=9):
    pts = [(x0, y)]
    seg = (x1 - x0) / (n + 1)
    for i in range(1, n + 1):
        pts.append((x0 + seg * i, y + (amp if i % 2 else -amp)))
    pts.append((x1, y))
    return pts


def fig_spring():
    b = []
    for row, (y, xm, label, force) in enumerate([(70, 250, "au repos : x = 0", None), (190, 320, "étiré : x > 0", "left")]):
        b.append(f'<rect x="20" y="{y - 40}" width="10" height="70" class="mk-ink3"/>')
        b.append(polyline(spring_path(30, xm - 22, y), "ink2", 2))
        b.append(f'<rect x="{xm - 22}" y="{y - 20}" width="44" height="40" rx="6" class="ln ln-ink" stroke-width="2" fill="none"/>')
        b.append(text(xm, y + 6, "m", "ink", "middle", 15, 700))
        b.append(line(250, y + 36, 250, y + 46, "ink3", 1.2, False))
        b.append(text(250, y + 62, "O", "ink2", "middle", 13))
        b.append(text(470, y - 24, label, "ink2", "end", 13))
        if force:
            b.append(line(xm - 24, y, xm - 104, y, "a", 3))
            b.append(text(xm - 110, y - 10, "F = −k x", "a", "end", 14, 700))
            b.append(line(250, y + 41, xm, y + 41, "v", 1.6, True))
            b.append(text((250 + xm) / 2, y + 36, "x", "v", "middle", 13, 700))
    b.append(line(20, 280, 470, 280, "ink3", 1.2))
    b.append(text(474, 284, "x", "ink2", size=13))
    return svg(490, 300, "Ressort au repos et étiré", b, "fig-svg half")


# ---------- Oscillation x(t) ----------
def fig_osc():
    ox, oy, W, A = 50, 120, 400, 70
    T = 160
    b = [line(ox, oy, ox + W + 20, oy, "ink3", 1.3), line(ox, oy + A + 20, ox, oy - A - 26, "ink3", 1.3)]
    b.append(text(ox + W + 24, oy + 4, "t", "ink2", size=13))
    b.append(text(ox - 8, oy - A - 30, "x", "ink2", size=13))
    pts = [(ox + x, oy - A * math.cos(2 * math.pi * x / T)) for x in [i * W / 300 for i in range(301)]]
    b.append(polyline(pts, "v", 2.6))
    b.append(line(ox, oy - A, ox + W, oy - A, "ink3", 1, False, "3 4"))
    b.append(line(ox, oy + A, ox + W, oy + A, "ink3", 1, False, "3 4"))
    b.append(text(ox - 8, oy - A + 4, "A", "ink2", "end", 13, 700))
    b.append(text(ox - 8, oy + A + 4, "−A", "ink2", "end", 13, 700))
    b.append(line(ox, oy - A - 14, ox + T, oy - A - 14, "u1", 1.6, True))
    b.append(line(ox + T, oy - A - 14, ox, oy - A - 14, "u1", 1.6, True))
    b.append(text(ox + T / 2, oy - A - 20, sub("T", "0") + " = 2π/ω₀", "u1", "middle", 13, 700))
    return svg(480, 230, "Oscillations harmoniques x(t)", b, "fig-svg half")


# ---------- Pendule simple ----------
def fig_pendule():
    Ox, Oy, l = 200, 30, 190
    th = math.radians(28)
    Mx, My = Ox + l * math.sin(th), Oy + l * math.cos(th)
    b = [line(130, Oy, 270, Oy, "ink2", 2, False), dot(Ox, Oy, "ink", 4)]
    b.append(line(Ox, Oy, Ox, Oy + l + 30, "ink3", 1.1, False, "4 4"))
    b.append(line(Ox, Oy, Mx, My, "ink", 2))
    b.append(text((Ox + Mx) / 2 + 10, (Oy + My) / 2, "l", "ink2", size=15))
    b.append(arc(Ox, Oy, 60, -90, -90 + 28, "ink2", 1.3))
    b.append(text(Ox + 12, Oy + 82, "θ", "ink2", size=15))
    b.append(line(Mx, My, Mx, My + 80, "a", 3))
    b.append(text(Mx + 8, My + 82, vec("P"), "a", size=16))
    b.append(line(Mx, My, Mx - 70 * math.sin(th), My - 70 * math.cos(th), "v", 3))
    b.append(text(Mx - 70 * math.sin(th) - 8, My - 70 * math.cos(th) + 18, vec("T"), "v", "end", 16))
    ur = (math.sin(th), math.cos(th))
    ut = (math.cos(th), -math.sin(th))
    b.append(line(Mx, My, Mx + 50 * ur[0], My + 50 * ur[1], "u1", 2.4))
    b.append(text(Mx + 50 * ur[0] + 6, My + 50 * ur[1] + 4, base("r"), "u1", size=15))
    b.append(line(Mx, My, Mx + 50 * ut[0], My + 50 * ut[1], "u2", 2.4))
    b.append(text(Mx + 50 * ut[0] + 6, My + 50 * ut[1], base("θ"), "u2", size=15))
    b.append(dot(Mx, My, "ink", 7))
    return svg(400, 320, "Pendule simple : forces et base polaire", b, "fig-svg mini")


# ---------- Régimes amortis ----------
def fig_regimes():
    ox, oy, W, A = 40, 110, 420, 80
    b = [line(ox, oy, ox + W + 10, oy, "ink3", 1.3), line(ox, oy + 50, ox, oy - A - 16, "ink3", 1.3)]
    b.append(text(ox + W + 14, oy + 4, "t", "ink2", size=13))
    w0 = 2 * math.pi / 110
    def curve(fn):
        return [(ox + t, oy - A * fn(t)) for t in [i * W / 300 for i in range(301)]]
    lam = 0.012
    w = math.sqrt(w0 * w0 - lam * lam)
    b.append(polyline(curve(lambda t: math.exp(-lam * t) * (math.cos(w * t) + lam / w * math.sin(w * t))), "v", 2.4))
    b.append(polyline(curve(lambda t: (1 + w0 * t) * math.exp(-w0 * t)), "a", 2.4))
    l2 = 3 * w0
    r1, r2 = -l2 + math.sqrt(l2 * l2 - w0 * w0), -l2 - math.sqrt(l2 * l2 - w0 * w0)
    A1, A2 = r2 / (r2 - r1), -r1 / (r2 - r1)
    b.append(polyline(curve(lambda t: A1 * math.exp(r1 * t) + A2 * math.exp(r2 * t)), "u2", 2.4))
    b.append(text(ox + 70, oy + 46, "pseudo-périodique (λ < ω₀)", "v", size=13, weight=700))
    b.append(text(ox + 110, oy - 58, "critique (λ = ω₀)", "a", size=13, weight=700))
    b.append(text(ox + 230, oy - 30, "apériodique (λ > ω₀)", "u2", size=13, weight=700))
    return svg(480, 180, "Trois régimes d'un oscillateur amorti", b, "fig-svg half")


# ---------- Signal : période et longueur d'onde ----------
def fig_wave():
    b = []
    for row, (oy, axis, sym, lab) in enumerate([(70, "t", "T", "période T (dans le temps)"), (190, "x", "λ", "longueur d'onde λ (dans l'espace)")]):
        ox, W, A, P = 40, 400, 40, 160
        b.append(line(ox, oy, ox + W + 10, oy, "ink3", 1.2))
        b.append(text(ox + W + 14, oy + 4, axis, "ink2", size=13))
        b.append(polyline([(ox + x, oy - A * math.sin(2 * math.pi * x / P)) for x in [i * W / 300 for i in range(301)]], "v" if row == 0 else "u2", 2.4))
        x1 = ox + P / 4
        b.append(line(x1, oy - A - 10, x1 + P, oy - A - 10, "ink", 1.4, True))
        b.append(line(x1 + P, oy - A - 10, x1, oy - A - 10, "ink", 1.4, True))
        b.append(text(x1 + P / 2, oy - A - 16, lab, "ink", "middle", 13, 700))
    b.append(text(40, 262, "λ = c · T = c / f", "ink", size=15, weight=700))
    return svg(470, 275, "Période et longueur d'onde", b, "fig-svg half")


# ---------- Modes d'une corde fixée ----------
def fig_modes():
    b = []
    L, ox = 360, 70
    for n in (1, 2, 3):
        oy = 40 + (n - 1) * 70
        b.append(text(ox - 12, oy + 5, f"n = {n}", "ink2", "end", 13, 700))
        for s in (1, -1):
            b.append(polyline([(ox + x, oy - s * 22 * math.sin(n * math.pi * x / L)) for x in [i * L / 200 for i in range(201)]], "v" if s == 1 else "ink3", 2 if s == 1 else 1.2, None if s == 1 else "4 4"))
        for k in range(n + 1):
            b.append(dot(ox + k * L / n, oy, "ink", 3.5))
        b.append(text(ox + L + 10, oy + 5, f"λ = 2L/{n}" if n > 1 else "λ = 2L", "ink2", size=13))
    b.append(text(ox, 232, "• nœuds (immobiles) aux extrémités et entre les ventres", "ink2", size=13))
    return svg(500, 245, "Modes propres d'une corde fixée aux deux bouts", b, "fig-svg half")


FIGS2 = {
    "INCLINE": fig_incline,
    "WORK": fig_work,
    "SPRING": fig_spring,
    "OSC": fig_osc,
    "PENDULE": fig_pendule,
    "REGIMES": fig_regimes,
    "WAVE": fig_wave,
    "MODES": fig_modes,
}
