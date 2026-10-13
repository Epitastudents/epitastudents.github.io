# Construit le site publié : l'application installable (PWA) et la page d'accueil.
#
#   python3 src/build.py https://revisions-s1.github.io/
#
# Entrées : src/template.html, src/content.py, src/figs.py, src/icons (générées par make_icons.py)
# Sorties : index.html (accueil), cinematique-s1/ (application, page d'installation, service worker, manifeste)
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
import content  # noqa: E402
import figs  # noqa: E402

APP_DIR = "cinematique-s1"
APP_NAME = "Cinématique S1"
SHORT_NAME = "Cinématique"
DESC = "Révisions du contrôle 1 de physique S1 : cours illustré, QCM et exercices des annales, hors ligne."
MATHJAX_SRC = os.environ.get("MATHJAX_DIR", os.path.join(SRC, "vendor", "mathjax"))
MONTHS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]


def counts():
    """Chiffres affichés dans les pages, calculés depuis content.py."""
    years = [int(y) for a in content.ANNALES for y in re.findall(r"(20\d\d)", a["date"])]
    nb_q = len(content.QCM)
    nb_e = sum(len(items) for _, items in content.EXOS)
    return {
        "NB_QCM": str(nb_q),
        "NB_EXOS": str(nb_e),
        "NB_TOTAL": str(nb_q + nb_e),
        "NB_SUJETS": str(len(content.ANNALES)),
        "ANNEES": f"{min(years)} à {max(years)}",
    }


def fill_counts(s):
    for k, v in counts().items():
        s = s.replace(f"@@{k}@@", v)
    return s


def page_body():
    """Assemble le contenu du cours (même résultat que le site Claude)."""
    figs_svg = {k: fn() for k, fn in figs.FIGS.items()}
    tpl = open(os.path.join(SRC, "template.html"), encoding="utf-8").read()
    exos = content.EXOS
    order = {"Cartésiennes et trajectoire": 0, "Polaires et cylindriques": 1, "Base de Frenet": 2}
    content.EXOS = sorted(exos, key=lambda g: order.get(g[0], 9))
    parts = {
        "BARS": content.bars_html(),
        "QCM": content.qcm_html(),
        "EXOS": content.exos_html(figs_svg),
        "ANNALES": content.annales_html(),
        "FICHE": content.fiche_html(),
    }
    content.EXOS = exos
    for k, v in parts.items():
        tpl = tpl.replace(f"@@{k}@@", v)
    for k, v in figs_svg.items():
        tpl = tpl.replace(f"@@{k}@@", v)
    tpl = fill_counts(tpl)
    left = re.findall(r"@@[A-Z_]+@@", tpl)
    assert not left, left
    return tpl.replace("class='eq'", 'class="eq"')


def head_common(theme_light="#F4F6FA", theme_dark="#0D1220"):
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
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">"""


APP_CSS = """<style>
/* Ajouts propres à l'application installée */
body { margin: 0; -webkit-text-size-adjust: 100%; }
img { max-width: 100%; }
html { scroll-padding-top: calc(72px + env(safe-area-inset-top, 0px)); }
.nav { top: 0; padding-top: env(safe-area-inset-top, 0px); }
.nav .wrap { padding-inline: max(20px, env(safe-area-inset-left, 0px)); }
footer { padding-bottom: calc(48px + env(safe-area-inset-bottom, 0px)); }
.inst { flex: 0 0 auto; font: 700 0.82rem var(--f-body); background: var(--ink); color: var(--paper); border-radius: 8px; padding: 6px 10px; text-decoration: none; white-space: nowrap; }
.inst:hover { filter: brightness(1.15); }
.toast { position: fixed; left: 50%; bottom: calc(16px + env(safe-area-inset-bottom, 0px)); transform: translateX(-50%); z-index: 60; display: flex; flex-wrap: wrap; align-items: center; gap: 10px 14px; width: max-content; max-width: calc(100% - 32px); background: var(--ink); color: var(--paper); border-radius: 14px; padding: 12px 14px 12px 18px; box-shadow: 0 8px 28px rgba(0, 0, 0, 0.28); font-size: 0.95rem; }
.toast b { font-weight: 700; }
.toast button { font: 700 0.9rem var(--f-body); border-radius: 9px; padding: 7px 12px; cursor: pointer; border: 1.5px solid var(--paper); }
.toast .go { background: var(--paper); color: var(--ink); }
.toast .later { background: transparent; color: var(--paper); }
.ver { font-family: var(--f-mono); font-size: 0.8rem; }
</style>"""

APP_JS = """<script>
(function () {
  var standalone = window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true;
  var inst = document.getElementById('instBtn');
  var deferred = null;
  if (inst && !standalone) inst.hidden = false;
  window.addEventListener('beforeinstallprompt', function (e) { e.preventDefault(); deferred = e; });
  window.addEventListener('appinstalled', function () { if (inst) inst.hidden = true; });
  if (inst) inst.addEventListener('click', function (e) {
    if (!deferred) return;
    e.preventDefault();
    deferred.prompt();
    deferred.userChoice.then(function () { deferred = null; });
  });

  var toast = document.getElementById('updToast');
  var waitingWorker = null, updating = false;
  function offer(w) { waitingWorker = w; toast.hidden = false; }
  document.getElementById('updGo').addEventListener('click', function () {
    if (!waitingWorker) return;
    updating = true;
    this.textContent = 'Mise à jour…';
    waitingWorker.postMessage('skipWaiting');
  });
  document.getElementById('updLater').addEventListener('click', function () { toast.hidden = true; });

  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () {
      navigator.serviceWorker.register('sw.js', { updateViaCache: 'none' }).then(function (reg) {
        if (reg.waiting && navigator.serviceWorker.controller) offer(reg.waiting);
        reg.addEventListener('updatefound', function () {
          var w = reg.installing;
          if (!w) return;
          w.addEventListener('statechange', function () {
            if (w.state === 'installed' && navigator.serviceWorker.controller) offer(w);
          });
        });
        document.addEventListener('visibilitychange', function () {
          if (document.visibilityState === 'visible') reg.update().catch(function () {});
        });
        setInterval(function () { reg.update().catch(function () {}); }, 3600000);
      }).catch(function () {});
      navigator.serviceWorker.addEventListener('controllerchange', function () {
        if (updating) { updating = false; window.location.reload(); }
      });
    });
  }
})();
</script>"""

SW_TEMPLATE = """// Service worker : fonctionnement hors ligne et mises à jour de l'application.
const VERSION = '@@VERSION@@';
const PREFIX = 'cinematique-s1-';
const CACHE = PREFIX + VERSION;
const FONTS = PREFIX + 'polices';
const PRECACHE = @@PRECACHE@@;

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) => cache.addAll(PRECACHE.map((u) => new Request(u, { cache: 'reload' }))))
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
    body = page_body()
    cut = body.index('<svg width="0"')
    tpl_head, tpl_body = body[:cut], body[cut:]
    tpl_body = tpl_body.replace(
        '<script src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg.js" async></script>',
        '<script src="vendor/mathjax/tex-svg.js" async></script>')
    assert "vendor/mathjax/tex-svg.js" in tpl_body
    tpl_body = tpl_body.replace(
        '<div class="prog"',
        '<a class="inst" id="instBtn" href="installer.html" hidden>Installer</a>\n    <div class="prog"', 1)
    footer_extra = (f'<p class="ver">Version du {version_label(now)} · <a href="installer.html">Installer ou partager l’appli</a></p>\n'
                    '    <div class="reset">')
    tpl_body = tpl_body.replace('<div class="reset">', footer_extra, 1)
    toast = ('<div class="toast" id="updToast" role="status" hidden><span><b>Nouvelle version disponible.</b> '
             'Nouveaux contenus ou corrections.</span><span style="display:flex;gap:8px">'
             '<button class="go" id="updGo" type="button">Mettre à jour</button>'
             '<button class="later" id="updLater" type="button">Plus tard</button></span></div>')
    app_html = ('<!doctype html>\n<html lang="fr">\n<head>\n' + head_common() + "\n" + tpl_head + APP_CSS +
                "\n</head>\n<body>\n" + tpl_body + "\n" + toast + "\n" + APP_JS + "\n</body>\n</html>\n")
    open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(app_html)

    # ---------- Page d'installation ----------
    style = re.search(r"<style>.*?</style>", tpl_head, re.S).group(0)
    fonts = re.search(r'<link rel="stylesheet"[^>]*>', tpl_head).group(0)
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
    if os.path.isdir(os.path.join(SRC, "icons")):
        shutil.copytree(os.path.join(SRC, "icons"), os.path.join(out, "icons"), dirs_exist_ok=True)
    mj_out = os.path.join(out, "vendor", "mathjax")
    os.makedirs(os.path.join(mj_out, "input", "tex", "extensions"), exist_ok=True)
    shutil.copy(os.path.join(MATHJAX_SRC, "tex-svg.js"), os.path.join(mj_out, "tex-svg.js"))
    shutil.copy(os.path.join(MATHJAX_SRC, "input", "tex", "extensions", "html.js"),
                os.path.join(mj_out, "input", "tex", "extensions", "html.js"))

    # ---------- Manifeste ----------
    manifest = {
        "id": "./",
        "name": APP_NAME,
        "short_name": SHORT_NAME,
        "description": DESC,
        "lang": "fr",
        "dir": "ltr",
        "start_url": "./?source=appli",
        "scope": "./",
        "display": "standalone",
        "orientation": "any",
        "background_color": "#F4F6FA",
        "theme_color": "#141C33",
        "categories": ["education"],
        "icons": [
            {"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
            {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
            {"src": "icons/maskable-192.png", "sizes": "192x192", "type": "image/png", "purpose": "maskable"},
            {"src": "icons/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
        ],
        "shortcuts": [
            {"name": "QCM", "url": "./#qcm", "icons": [{"src": "icons/icon-192.png", "sizes": "192x192"}]},
            {"name": "Exercices", "url": "./#exos", "icons": [{"src": "icons/icon-192.png", "sizes": "192x192"}]},
            {"name": "Fiche", "url": "./#fiche", "icons": [{"src": "icons/icon-192.png", "sizes": "192x192"}]},
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
    assert "@@" not in hub
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(hub)
    open(os.path.join(ROOT, ".nojekyll"), "w").write("")
    print("ok · version", version, "·", app_url)


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "https://epitastudents.github.io/")
