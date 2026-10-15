# Construit le site publié : l'application installable (PWA) et la page d'accueil.
#
#   python3 src/build.py https://epitastudents.github.io/
#
# Entrées : src/app.html, src/cours.py (contenu), src/figs.py + src/figs2.py (schémas), src/installer.html,
#           src/installer_base.css, src/accueil.html, src/icons/, src/vendor/mathjax/
# Sorties : index.html (accueil), cinematique-s1/ (appli, page d'installation, service worker, manifeste)
import datetime
import hashlib
import io
import json
import os
import re
import shutil
import sys

SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)
sys.path.insert(0, SRC)
import cours  # noqa: E402
import figs  # noqa: E402
import figs2  # noqa: E402

APP_DIR = "cinematique-s1"   # dossier historique : on le garde pour ne pas casser les applis déjà installées
APP_NAME = "Mécanique S1"
SHORT_NAME = "Méca S1"
DESC = "Révisions de mécanique S1 : le cours en fiches courtes, QCM corrigés, exercices de TD guidés et cartes mémoire, hors ligne."
MATHJAX_SRC = os.environ.get("MATHJAX_DIR", os.path.join(SRC, "vendor", "mathjax"))
MONTHS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]


def counts():
    return {
        "NB_QCM": str(len(cours.QCM)),
        "NB_EXOS": str(len(cours.EXOS)),
        "NB_FICHES": str(len(cours.FICHES)),
        "NB_CARTES": str(sum(len(v) for v in cours.LECONS.values())),
    }


def fill_counts(s):
    for k, v in counts().items():
        s = s.replace(f"@@{k}@@", v)
    return s


def figures():
    out = {k: fn() for k, fn in figs.FIGS.items()}
    out.update({k: fn() for k, fn in figs2.FIGS2.items()})
    trio = lambda keys, caps: ('<div class="fig-row">' + "".join(
        f'<div>{out[k]}<div>{c}</div></div>' for k, c in zip(keys, caps)) + "</div>")
    out["SC3"] = trio(["SC_AIGU", "SC_DROIT", "SC_OPP"], ["angle aigu : &gt; 0", "angle droit : = 0", "sens opposés : &lt; 0"])
    out["SP3"] = trio(["SP_ACC", "SP_DEC", "SP_UNI"], ["v·a &gt; 0 : accéléré", "v·a &lt; 0 : décéléré", "v·a = 0 : virage"])
    return out


SEPS = (r"\quad\Longrightarrow\quad", r"\quad\Rightarrow\quad", r"\qquad")


def split_display(tex):
    """Coupe les blocs \\[ … \\] qui alignent plusieurs formules : une formule par ligne, lisible sur téléphone."""
    def one(block):
        body, parts, depth, i, cur = block, [], 0, 0, ""
        while i < len(body):
            if body.startswith(r"\begin", i):
                depth += 1
            elif body.startswith(r"\end", i):
                depth -= 1
            hit = next((sep for sep in SEPS if depth == 0 and body.startswith(sep, i)), None)
            if hit:
                parts.append(cur)
                cur = r"\Rightarrow " if "Rightarrow" in hit else ""
                i += len(hit)
                continue
            cur += body[i]
            i += 1
        parts.append(cur)
        return "".join(r"\[" + p.strip() + r"\]" for p in parts if p.strip())
    return re.sub(r"\\\[(.*?)\\\]", lambda m: one(m.group(1)), tex, flags=re.S)


def deep_split(obj):
    if isinstance(obj, str):
        return split_display(obj)
    if isinstance(obj, list):
        return [deep_split(x) for x in obj]
    if isinstance(obj, tuple):
        return tuple(deep_split(x) for x in obj)
    if isinstance(obj, dict):
        return {k: deep_split(v) for k, v in obj.items()}
    return obj


def app_data():
    """Toutes les données de l'appli, en JSON."""
    figs_all = figures()
    used = set()
    lecons = {}
    for ch, cards in cours.LECONS.items():
        lecons[ch] = cards
        used.update(c["fig"] for c in cards if c.get("fig"))
    exos = []
    for e in cours.EXOS:
        exos.append(dict(e))
        if e.get("fig"):
            used.add(e["fig"])
    qcm = []
    for i, item in enumerate(cours.QCM):
        ch, q, opts, ans, expl = item[:5]
        qcm.append(dict(id=f"q{i}-{ch}", ch=ch, q=q, opts=opts, ans=ans, expl=expl, multi=bool(len(item) > 5 and item[5])))
    fiches = [dict(id=f"f{i}-{ch}", ch=ch, q=q, r=r) for i, (ch, q, r) in enumerate(cours.FICHES)]
    missing = [k for k in used if k != "POLAR" and k not in figs_all]
    assert not missing, missing
    lecons, exos, fiches = deep_split(lecons), deep_split(exos), deep_split(fiches)
    data = dict(
        chapitres=cours.CHAPITRES, lecons=lecons, qcm=qcm, exos=exos, fiches=fiches,
        figs={k: v for k, v in figs_all.items() if k in used},
        annales=cours.ANNALES, partiels=cours.PARTIELS_GH,
    )
    for ch in lecons:
        assert ch in {c["id"] for c in cours.CHAPITRES}, ch
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")


def head_common(theme_light="#FFFFFF", theme_dark="#111318"):
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="{theme_light}" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="{theme_dark}" media="(prefers-color-scheme: dark)">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icons/favicon-64.png" type="image/png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="{SHORT_NAME}">
<meta name="apple-mobile-web-app-status-bar-style" content="default">"""


SW_TEMPLATE = """// Service worker : fonctionnement hors ligne et mises à jour de l'application.
const VERSION = '@@VERSION@@';
const PREFIX = 'cinematique-s1-';
const CACHE = PREFIX + VERSION;
const FONTS = PREFIX + 'polices';
const PRECACHE = @@PRECACHE@@;

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) => cache.addAll(PRECACHE.map((u) => new Request(u, { cache: 'reload' }))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k.startsWith(PREFIX) && k !== CACHE && k !== FONTS).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('message', (event) => {
  if (event.data === 'skipWaiting') self.skipWaiting();
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);

  // Polices Google : servies depuis le cache, rafraîchies en arrière-plan.
  if (url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com') {
    event.respondWith(
      caches.open(FONTS).then((cache) => cache.match(req).then((hit) => {
        const net = fetch(req).then((res) => { if (res && (res.ok || res.type === 'opaque')) cache.put(req, res.clone()); return res; }).catch(() => hit);
        return hit || net;
      }))
    );
    return;
  }
  if (url.origin !== self.location.origin) return;

  // Pages et fichiers de l'appli : d'abord le cache (marche sans réseau), sinon le réseau.
  event.respondWith(
    caches.match(req, { ignoreSearch: true }).then((hit) => {
      if (hit) return hit;
      return fetch(req).then((res) => {
        if (res && res.ok && res.type === 'basic') {
          const copy = res.clone();
          caches.open(CACHE).then((cache) => cache.put(req, copy));
        }
        return res;
      }).catch(() => (req.mode === 'navigate' ? caches.match('./') : Response.error()));
    })
  );
});
"""


def version_label(now):
    return f"{now.day} {MONTHS[now.month - 1]} {now.year}"


def qr_svg(url):
    import qrcode
    import qrcode.image.svg
    img = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage, box_size=10, border=2)
    buf = io.BytesIO()
    img.save(buf)
    svg = buf.getvalue().decode("utf-8")
    svg = re.sub(r"<\?xml[^>]*\?>", "", svg).strip()
    svg = svg.replace('fill="#000000"', 'fill="currentColor"')
    svg = re.sub(r'width="[^"]*mm" height="[^"]*mm" ', "", svg, count=1)
    return svg.replace("<svg ", '<svg class="qr" role="img" aria-label="QR code vers la page d\'installation" ', 1)


def build(base_url):
    base_url = base_url.rstrip("/") + "/"
    app_url = base_url + APP_DIR + "/"
    install_url = app_url + "installer.html"
    out = os.path.join(ROOT, APP_DIR)
    os.makedirs(out, exist_ok=True)
    now = datetime.datetime.now()

    # ---------- Application ----------
    tpl = open(os.path.join(SRC, "app.html"), encoding="utf-8").read()
    tpl = tpl.replace("@@DATA@@", app_data()).replace("@@MATHJAX@@", "vendor/mathjax/tex-svg.js")
    left = re.findall(r"@@[A-Z_]+@@", tpl)
    assert not left, left
    cut = tpl.index('<svg width="0"')
    head_part, body_part = tpl[:cut], tpl[cut:]
    app_html = ('<!doctype html>\n<html lang="fr">\n<head>\n' + head_common() + "\n" + head_part +
                "</head>\n<body>\n" + body_part + "\n</body>\n</html>\n")
    open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(app_html)

    # ---------- Page d'installation ----------
    fonts = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&display=swap">'
    style = "<style>\n" + open(os.path.join(SRC, "installer_base.css"), encoding="utf-8").read() + "</style>"
    inst = open(os.path.join(SRC, "installer.html"), encoding="utf-8").read()
    inst = (inst.replace("@@HEAD@@", head_common())
                .replace("@@FONTS@@", fonts)
                .replace("@@BASE_STYLE@@", style)
                .replace("@@QR@@", qr_svg(install_url))
                .replace("@@INSTALL_URL@@", install_url)
                .replace("@@APP_URL@@", app_url)
                .replace("@@VERSION@@", version_label(now)))
    inst = fill_counts(inst)
    assert "@@" not in inst, re.findall(r"@@\w+@@", inst)
    open(os.path.join(out, "installer.html"), "w", encoding="utf-8").write(inst)

    # ---------- Icônes et MathJax ----------
    shutil.copytree(os.path.join(SRC, "icons"), os.path.join(out, "icons"), dirs_exist_ok=True)
    mj_out = os.path.join(out, "vendor", "mathjax")
    os.makedirs(os.path.join(mj_out, "input", "tex", "extensions"), exist_ok=True)
    shutil.copy(os.path.join(MATHJAX_SRC, "tex-svg.js"), os.path.join(mj_out, "tex-svg.js"))
    shutil.copy(os.path.join(MATHJAX_SRC, "input", "tex", "extensions", "html.js"),
                os.path.join(mj_out, "input", "tex", "extensions", "html.js"))

    # ---------- Manifeste ----------
    manifest = {
        "id": "./", "name": APP_NAME, "short_name": SHORT_NAME, "description": DESC,
        "lang": "fr", "dir": "ltr", "start_url": "./?source=appli", "scope": "./",
        "display": "standalone", "orientation": "any",
        "background_color": "#FFFFFF", "theme_color": "#FFFFFF", "categories": ["education"],
        "icons": [
            {"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
            {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
            {"src": "icons/maskable-192.png", "sizes": "192x192", "type": "image/png", "purpose": "maskable"},
            {"src": "icons/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
        ],
        "shortcuts": [
            {"name": "QCM rapide", "url": "./#/qcm/go/tout", "icons": [{"src": "icons/icon-192.png", "sizes": "192x192"}]},
            {"name": "Fiches du jour", "url": "./#/fiches", "icons": [{"src": "icons/icon-192.png", "sizes": "192x192"}]},
            {"name": "Exercices de TD", "url": "./#/exos", "icons": [{"src": "icons/icon-192.png", "sizes": "192x192"}]},
        ],
    }
    open(os.path.join(out, "manifest.webmanifest"), "w", encoding="utf-8").write(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")

    # ---------- Service worker (version = empreinte du contenu) ----------
    files = ["index.html", "installer.html", "manifest.webmanifest", "vendor/mathjax/tex-svg.js",
             "vendor/mathjax/input/tex/extensions/html.js"] + sorted("icons/" + f for f in os.listdir(os.path.join(out, "icons")))
    h = hashlib.sha256()
    for f in files:
        h.update(open(os.path.join(out, f), "rb").read())
    version = h.hexdigest()[:12]
    sw = SW_TEMPLATE.replace("@@VERSION@@", version).replace("@@PRECACHE@@", json.dumps(["./"] + files))
    open(os.path.join(out, "sw.js"), "w", encoding="utf-8").write(sw)

    # ---------- Accueil du site ----------
    hub = open(os.path.join(SRC, "accueil.html"), encoding="utf-8").read()
    hub = fill_counts(hub.replace("@@FONTS@@", fonts).replace("@@APP_DIR@@", APP_DIR))
    assert "@@" not in hub, re.findall(r"@@\w+@@", hub)
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(hub)
    open(os.path.join(ROOT, ".nojekyll"), "w").write("")
    print("ok · version", version, "·", app_url, "·", counts())


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "https://epitastudents.github.io/")
