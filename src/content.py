# Contenu du site : thèmes, QCM, exercices, annales, fiche.
GH = "https://github.com/Epidocs/past-exams/blob/master/S1/Midterms/Phys/"

# ---------------- Barres "ce qui tombe" ----------------
BARS = [
    ("Vitesse et accélération en cartésiennes", 7, "les 7 sujets", "#ch-cart"),
    ("Coordonnées polaires", 7, "les 7 sujets", "#ch-polaires"),
    ("Équation de la trajectoire", 6, "2017, nov. 2018, mai 2018, 2020, 2021, 2022", "#ch-cart"),
    ("Mouvement circulaire", 6, "nov. 2018, mai 2018, 2019, 2020, 2021, 2022", "#circulaire"),
    ("Produit scalaire et vectoriel", 5, "2017, nov. 2018, mai 2018, 2019, 2021", "#ch-outils"),
    ("Coordonnées cylindriques", 5, "nov. 2018, mai 2018, 2019, 2020, 2022", "#cylindriques"),
    ("Base de Frenet", 5, "2017, nov. 2018, mai 2018, 2019, 2020", "#ch-frenet"),
    ("Projection d’un vecteur", 4, "2017, nov. 2018, mai 2018, 2019", "#ch-outils"),
    ("Tir d’un projectile", 2, "2021 et 2022, les deux plus récents", "#ex-projectile"),
]

def bars_html():
    out = []
    for name, n, years, href in BARS:
        top = " top" if n == 7 else ""
        out.append(
            f'<a class="bar-row{top}" role="listitem" href="{href}" aria-label="{name} : {n} sujets sur 7">'
            f'<span class="name">{name}</span>'
            f'<span class="track"><span class="fill" style="width:{100*n/7:.1f}%"></span></span>'
            f'<span class="val">{n} / 7</span>'
            f'<span class="tip">Présent dans {n} sujets sur 7 : {years}</span></a>')
    return "\n".join(out)

# ---------------- QCM ----------------
COL = lambda a, b: rf"\(\begin{{pmatrix}} {a} \\ {b} \end{{pmatrix}}_{{(\vec u_\rho,\,\vec u_\theta)}}\)"
QCM = [
    ("2017 · 2018 · 2019", "Le produit scalaire de deux vecteurs non nuls, colinéaires et de sens opposés est :",
     [("a", "strictement positif"), ("b", "nul"), ("c", "strictement négatif")], "c",
     r"L’angle vaut 180°, donc \(\cos\alpha = -1\) et \(\vec U\cdot\vec V = -UV < 0\). « Nul » correspond à des vecteurs perpendiculaires."),
    ("2021", "Deux vecteurs sont orthogonaux si leur produit scalaire est nul.",
     [("a", "Vrai"), ("b", "Faux")], "a",
     r"\(\cos 90° = 0\). Et réciproquement : un produit scalaire nul (vecteurs non nuls) veut dire angle droit."),
    ("2017 · 2019", r"La norme de \(\vec V_3 = \vec V_1\wedge\vec V_2\), avec un angle α entre \(\vec V_1\) et \(\vec V_2\), est :",
     [("a", r"\(V_1V_2|\sin\alpha|\)"), ("b", r"\(V_1V_2|\cos\alpha|\)"), ("c", r"\(\sqrt{V_1^2+V_2^2+2V_1V_2\cos\alpha}\)")], "a",
     r"Produit vectoriel → sinus. La réponse c est la norme de la <b>somme</b> \(\vec V_1 + \vec V_2\)."),
    ("Mai 2018", "La norme de la résultante R de deux forces F₁ et F₂ non nulles et orthogonales est :",
     [("a", r"\(R = 0\)"), ("b", r"\(R = F_1 + F_2\)"), ("c", r"\(R = \sqrt{F_1^2 + F_2^2}\)"), ("d", r"\(R = F_1 - F_2\)")], "c",
     "Les deux forces forment un angle droit : c’est Pythagore."),
    ("Nov. 2018 · Mai 2018", r"Le produit vectoriel de \(\vec V_1 = (1\ ;\ 3\ ;\ 2)\) et \(\vec V_2 = (-4\ ;\ 1\ ;\ 1)\) est :",
     [("a", r"\((1\ ;\ 9\ ;\ 13)\)"), ("b", r"\((1\ ;\ -9\ ;\ 13)\)"), ("c", r"\((1\ ;\ -11\ ;\ 12)\)")], "b",
     r"\(W_x = 3\times1 - 2\times1 = 1\), \(W_y = 2\times(-4) - 1\times1 = -9\), \(W_z = 1\times1 - 3\times(-4) = 13\)."),
    ("2022", "L’unité d’une accélération peut être :",
     [("a", "m·s⁻¹"), ("b", "m·s⁻²"), ("c", "kg·m·s⁻¹"), ("d", "kg·s⁻²")], "b",
     "Une accélération est une vitesse (m·s⁻¹) divisée par un temps (s). m·s⁻¹ est une vitesse, kg·m·s⁻¹ une quantité de mouvement."),
    ("2021", r"L’accélération d’un mobile de vecteur position \(\OM(t)\) est donnée par :",
     [("a", r"\(\vec a = \left(\frac{d\OM}{dt}\right)^2\)"), ("b", r"\(\vec a = \frac{d^2\OM}{dt^2}\)"), ("c", r"\(\vec a = \sqrt{\OM}\)")], "b",
     "On dérive deux fois la position. Le carré de la dérivée n’a pas de sens ici."),
    ("2021", "Un mouvement est dit uniforme si :",
     [("a", "sa trajectoire est une ligne droite"), ("b", "son accélération est constante"), ("c", "sa vitesse (en norme) est constante"), ("d", "sa vitesse et son accélération varient très peu")], "c",
     "Uniforme = norme de la vitesse constante. Le corrigé scanné de 2021 entoure d, mais c’est la définition c qui est juste."),
    ("2022", "Choisis les affirmations justes :",
     [("a", "Un mouvement peut être uniforme sur une seule de ses composantes"), ("b", "L’équation de la trajectoire permet de dire si le mouvement est uniforme"), ("c", "Lors d’un mouvement circulaire uniforme, l’accélération est nulle"), ("d", "Lors d’un mouvement rectiligne uniforme, l’accélération est nulle")], "a,d",
     "a : le projectile est uniforme selon x. b : la trajectoire ne dit rien de la vitesse. c : en circulaire uniforme, a pointe vers le centre et vaut Rω². d : vrai.", True),
    ("2022", r"Un mouvement a pour équations horaires \(x(t) = 4t\) et \(y(t) = 3t^2 - 6t + 5\). Choisis les affirmations justes :",
     [("a", "Ce mouvement est décéléré"), ("b", "Ce mouvement est uniforme"), ("c", "La vitesse s’annule en un point de la trajectoire"), ("d", "Ce mouvement est parabolique")], "d",
     r"\(t = x/4\) donne \(y = \frac{3x^2}{16} - \frac{3x}{2} + 5\) : une parabole. \(v_x = 4\) ne s’annule jamais, donc la vitesse non plus (seul \(v_y\) s’annule, à t = 1 s). Le mouvement freine avant t = 1 s puis accélère : il n’est ni uniforme ni décéléré en tout temps.", True),
    ("2021, adaptée", r"Un mobile se déplace sur l’axe Ox avec \(x(t) = 10 - 2t^2\). Pour t &gt; 0 :",
     [("a", "le mouvement est uniforme"), ("b", "le mouvement est décéléré"), ("c", "le mouvement est accéléré et a = 4 m·s⁻²"), ("d", "a = 2 m·s⁻²")], "c",
     r"\(v = -4t\) et \(a = -4\). v et a ont le même signe, donc \(v\cdot a > 0\) : accéléré. Dans le sujet original, aucune des propositions n’était juste."),
    ("2020", r"Un point part à t = 1 s avec \(x(t) = \ln t\) et \(y(t) = t + \frac1t\). Son vecteur vitesse est :",
     [("a", r"\(\left(\frac1t\ ;\ 1 + \frac1{t^2}\right)\)"), ("b", r"\(\left(\frac1t\ ;\ 1 - \frac1{t^2}\right)\)"), ("c", r"\(\left(1\ ;\ 1 - \frac1{t^2}\right)\)")], "b",
     r"La dérivée de \(\ln t\) est \(\frac1t\), celle de \(\frac1t\) est \(-\frac1{t^2}\)."),
    ("2020", r"Pour \(x(t) = -2t^3 - t\) et \(y(t) = 4t^2\), le vecteur vitesse est :",
     [("a", r"\((-6t - 1\ ;\ 8t)\)"), ("b", r"\((-6t^2 - 1\ ;\ 8t)\)"), ("c", r"\((-2t^2 - 1\ ;\ 8t)\)")], "b",
     r"\((t^3)' = 3t^2\), donc \((-2t^3)' = -6t^2\)."),
    ("2019", r"La dérivée par rapport à t de \(f(t) = A\cos^2(\theta(t))\) est :",
     [("a", r"\(2A\dot\theta\cos\theta\sin\theta\)"), ("b", r"\(-2A\dot\theta\cos\theta\sin\theta\)"), ("c", r"\(2A\cos\theta\sin\theta\)")], "b",
     r"\((u^2)' = 2uu'\) avec \(u = \cos\theta\) et \(u' = -\dot\theta\sin\theta\). Ne pas oublier \(\dot\theta\) ni le signe moins."),
    ("2017", r"La trajectoire de \(x(t) = A\sin(\omega t)\), \(y(t) = B\cos(\omega t)\) (A ≠ B) a pour équation :",
     [("a", r"\(x^2 + y^2 = 1\)"), ("b", r"\(x^2 + y^2 = A^2 + B^2\)"), ("c", r"\(\frac{x^2}{A^2} + \frac{y^2}{B^2} = 1\)")], "c",
     r"\(\frac xA = \sin\), \(\frac yB = \cos\), on additionne les carrés : c’est une ellipse."),
    ("2020", r"La trajectoire de \(x(t) = R\cos(\omega t)\), \(y(t) = R\sin(\omega t)\) a pour équation :",
     [("a", r"\(x^2 + y^2 = R\)"), ("b", r"\(x^2 + y^2 = (R\omega)^2\)"), ("c", r"\(\frac{x^2}{R^2} + \frac{y^2}{R^2} = 1\)"), ("d", r"\(x^2 - y^2 = R^2\)")], "c",
     r"C’est \(x^2 + y^2 = R^2\) écrit autrement : un cercle de rayon R. ω n’apparaît pas dans la trajectoire."),
    ("2021", "En coordonnées polaires, le vecteur position est :",
     [("a", r"\(\rho\,\vec u_\rho + \theta\,\vec u_\theta\)"), ("b", r"\(\rho\,\vec u_\rho\)"), ("c", r"\(\theta\,\vec u_\rho + \rho\,\vec u_\theta\)"), ("d", r"\(\rho\,\vec u_\theta\)")], "b",
     "Un seul terme : M est à la distance ρ de O, dans la direction de u<sub>ρ</sub>."),
    ("2022", "En coordonnées cylindriques, le vecteur position est :",
     [("a", r"\(\rho\,\vec u_\rho\)"), ("b", r"\(\rho\,\vec u_\rho + \theta\,\vec u_\theta\)"), ("c", r"\(\rho\,\vec u_\rho + \theta\,\vec u_\theta + z\,\vec u_z\)"), ("d", r"\(\rho\,\vec u_\rho + z\,\vec u_z\)")], "d",
     "On ajoute la hauteur z au vecteur position polaire. Toujours pas de terme en θ."),
    ("Les 7 sujets", "En coordonnées polaires, le vecteur vitesse est :",
     [("a", r"\(\rho\,\vec u_\rho + \rho\dot\theta\,\vec u_\theta\)"), ("b", r"\(\dot\rho\,\vec u_\rho + \rho\dot\theta\,\vec u_\theta\)"), ("c", r"\(\dot\rho\,\vec u_\rho + \rho\ddot\theta\,\vec u_\theta\)")], "b",
     "On dérive ρu<sub>ρ</sub> comme un produit : ρ̇u<sub>ρ</sub> + ρ·θ̇u<sub>θ</sub>."),
    ("2019 · 2020", r"Le vecteur unitaire \(\vec u_\rho\) vérifie :",
     [("a", r"\(\frac{d\vec u_\rho}{dt} = -\dot\theta\,\vec u_\theta\)"), ("b", r"\(\frac{d\vec u_\rho}{dt} = \vec 0\)"), ("c", r"\(\frac{d\vec u_\rho}{dt} = \dot\theta\,\vec u_\rho\)"), ("d", r"\(\frac{d\vec u_\rho}{dt} = \dot\theta\,\vec u_\theta\)")], "d",
     "On tourne de +90° (u<sub>ρ</sub> → u<sub>θ</sub>) et on multiplie par θ̇. Le signe moins est pour la dérivée de u<sub>θ</sub>."),
    ("Mai 2018 · 2020", "Pour un mouvement circulaire uniforme de rayon R, l’accélération s’écrit :",
     [("a", COL(r"0", r"R\ddot\theta")), ("b", COL(r"R\dot\theta^2", r"0")), ("c", COL(r"-R\dot\theta^2", r"R\ddot\theta")), ("d", COL(r"-R\dot\theta^2", r"0"))], "d",
     r"\(\dot\rho = \ddot\rho = 0\) (rayon fixe) et \(\ddot\theta = 0\) (uniforme). Il reste \(-R\dot\theta^2\) sur \(\vec u_\rho\) : vers le centre."),
    ("2019", "Pour un mouvement circulaire décéléré de rayon R, l’accélération s’écrit :",
     [("a", COL(r"0", r"R\ddot\theta")), ("b", COL(r"R\dot\theta^2", r"0")), ("c", COL(r"-R\dot\theta^2", r"R\ddot\theta")), ("d", COL(r"-R\dot\theta^2", r"0"))], "c",
     r"Rayon fixe mais vitesse qui change : \(\ddot\theta \neq 0\). La forme est la même pour accéléré et décéléré, seul le signe de \(\ddot\theta\) change."),
    ("2022, adaptée", "Pour un mouvement circulaire uniforme, quelles égalités sont vraies ?",
     [("a", r"\(\dot\theta = \text{constante}\)"), ("b", r"\(\dot\theta = 0\)"), ("c", r"\(\ddot\theta = 0\)"), ("d", r"\(\dot\rho = 0\)")], "a,c,d",
     r"Circulaire : ρ = R fixe, donc \(\dot\rho = 0\). Uniforme : \(v = R\dot\theta\) constante, donc \(\dot\theta\) constante et \(\ddot\theta = 0\). \(\dot\theta = 0\) voudrait dire que M ne bouge pas.", True),
    ("Nov. 2018 · Mai 2018 · 2020", "Dans la base de Frenet, le vecteur vitesse d’un point sur un cercle de rayon R s’écrit :",
     [("a", r"\(R\dot\theta\,\vec u_N\)"), ("b", r"\(R\ddot\theta\,\vec u_T\)"), ("c", r"\(R\dot\theta\,\vec u_T\) (soit \(\frac{ds}{dt}\vec u_T\))")], "c",
     "La vitesse est toujours tangente, donc selon u<sub>T</sub>, et sa valeur est ds/dt = Rθ̇."),
    ("Nov. 2018 · Mai 2018", "Dans la base de Frenet, l’accélération a pour composantes :",
     [("a", r"\(a_T = \frac{dV}{dt},\ a_N = \frac{V^2}{R^2}\)"), ("b", r"\(a_T = \frac{d\theta}{dt},\ a_N = \frac{V^2}{R}\)"), ("c", r"\(a_T = \frac{dV}{dt},\ a_N = \frac{V^2}{R}\)")], "c",
     "a<sub>T</sub> change la valeur de la vitesse, a<sub>N</sub> fait tourner. Vérifie l’unité : V²/R est bien en m·s⁻²."),
    ("2017 · 2020", "L’abscisse curviligne s(t) est donnée par :",
     [("a", r"\(s(t) = \int_0^t a_T\,dt + s(0)\)"), ("b", r"\(s(t) = \int_0^t v\,dt + s(0)\)"), ("c", r"\(s(t) = \int_0^t a_N\,dt + s(0)\)")], "b",
     "v = ds/dt, donc on intègre la vitesse. Intégrer a<sub>T</sub> redonne v."),
    ("2017", "Sur un cercle de rayon R, l’abscisse curviligne élémentaire ds s’écrit :",
     [("a", r"\(ds = R\dot\theta\)"), ("b", r"\(ds = dV\cdot dt\)"), ("c", r"\(ds = R\,d\theta\)")], "c",
     "Un arc de cercle d’angle dθ mesure R dθ. La réponse a est une vitesse, pas une longueur."),
]

def qcm_html():
    out = []
    for i, item in enumerate(QCM, 1):
        src, text, opts, ans, expl = item[:5]
        multi = len(item) > 5 and item[5]
        qid = f"q{i}"
        attrs = f' data-q="{qid}" data-answer="{ans}"' + (" data-multi" if multi else "")
        head = f'<div class="q-head"><span class="q-num">{i}</span><span>{src}</span>' + ('<span class="q-multi">plusieurs réponses</span>' if multi else "") + "</div>"
        bt = "".join(f'<button class="opt" type="button" data-k="{k}"><span class="k">{k}</span><span>{h}</span></button>' for k, h in opts)
        foot = '<div class="q-foot">' + ('<button class="btn small q-validate" type="button">Valider</button>' if multi else "") + '<button class="btn ghost small q-retry" type="button" hidden>Réessayer</button></div>'
        out.append(f'<div class="q"{attrs}>{head}<p class="q-text">{text}</p><div class="opts">{bt}</div>{foot}'
                   f'<div class="q-expl" hidden aria-live="polite"><span class="verdict"></span>{expl}</div></div>')
    return "\n".join(out)

# ---------------- Exercices ----------------
EXOS = [
 ("Polaires et cylindriques", [
  dict(id="base", title="La base polaire, pas à pas", chips=["Nov. 2021", "8 points", "question de cours"], hot=True,
   src=[("Sujet 2021", GH + "2026/midterm-2026-s1-phys-subject-fr.pdf"), ("Corrigé", GH + "2026/midterm-2026-s1-phys-correction-fr.pdf")],
   enonce=r"Le point M est repéré à la fois en cartésiennes (x, y) et en polaires (ρ, θ), dans le même plan.",
   qs=[
    (r"Exprime \(\vec u_\rho\) et \(\vec u_\theta\) en fonction de θ, \(\vec u_x\) et \(\vec u_y\).",
     r"<p>\(\vec u_\rho\) est un vecteur de longueur 1 incliné de θ : on le projette comme une force de norme 1. \(\vec u_\theta\) est le même tourné de +90°.</p>\[\ur = \cos\theta\,\vec u_x + \sin\theta\,\vec u_y \qquad \ut = -\sin\theta\,\vec u_x + \cos\theta\,\vec u_y\]"),
    (r"Calcule \(\frac{d\vec u_\rho}{d\theta}\) et exprime-la en fonction de \(\vec u_\theta\).",
     r"\[\frac{d\ur}{d\theta} = -\sin\theta\,\vec u_x + \cos\theta\,\vec u_y = \ut\]"),
    (r"Calcule \(\frac{d\vec u_\theta}{d\theta}\) et exprime-la en fonction de \(\vec u_\rho\).",
     r"\[\frac{d\ut}{d\theta} = -\cos\theta\,\vec u_x - \sin\theta\,\vec u_y = -\ur\]"),
    (r"Exprime le vecteur position \(\OM\) dans la base cartésienne, puis dans la base polaire.",
     r"\[\OM = x\,\vec u_x + y\,\vec u_y = \rho\,\ur\]"),
    (r"Donne l’expression générale du vecteur vitesse, puis son expression dans la base polaire, en expliquant chaque étape.",
     r"<p>Par définition \(\V = \frac{d\OM}{dt}\). On dérive le produit ρ × \(\vec u_\rho\) :</p>\[\V = \dot\rho\,\ur + \rho\,\frac{d\ur}{dt}\]<p>Avec la dérivée composée : \(\frac{d\ur}{dt} = \frac{d\ur}{d\theta}\cdot\frac{d\theta}{dt} = \dot\theta\,\ut\). Donc :</p>\[\V = \dot\rho\,\ur + \rho\dot\theta\,\ut\]"),
   ]),
  dict(id="helice", title="L’hélice", chips=["Mai 2018", "2019", "2020", "6 à 9 points"],
   src=[("Sujet mai 2018", GH + "2023%23/midterm-2023%23-s1-phys-subject-fr.pdf"), ("Corrigé 2020", GH + "2025/midterm-2025-s1-phys-correction-fr.pdf")],
   enonce=r"Un point M a pour coordonnées \(x(t) = R\cos(\omega t)\), \(y(t) = R\sin(\omega t)\), \(z(t) = H\omega t\), avec R, ω et H constantes positives.",
   qs=[
    (r"Exprime le vecteur vitesse dans la base cartésienne et calcule sa norme.",
     r"\[\V = -R\omega\sin(\omega t)\,\vec u_x + R\omega\cos(\omega t)\,\vec u_y + H\omega\,\vec u_z\]<p>\(v = \sqrt{R^2\omega^2(\sin^2 + \cos^2) + H^2\omega^2} = \omega\sqrt{R^2 + H^2}\). Elle est constante : le mouvement est uniforme.</p>"),
    (r"Exprime le vecteur accélération et calcule sa norme.",
     r"\[\A = -R\omega^2\cos(\omega t)\,\vec u_x - R\omega^2\sin(\omega t)\,\vec u_y\]<p>\(a = R\omega^2\).</p>"),
    (r"Quel est le mouvement dans le plan (xOy) ? Et selon l’axe Oz ?",
     r"<p>Dans le plan : \(x^2 + y^2 = R^2\), cercle de rayon R parcouru à vitesse Rω : <b>circulaire uniforme</b>. Selon Oz : \(\dot z = H\omega\) constante : <b>rectiligne uniforme</b>.</p>"),
    (r"Avec les équations de passage, écris \(\OM\) en coordonnées cylindriques.",
     r"<p>On reconnaît ρ = R, θ = ωt et z = Hωt :</p>\[\OM = R\,\ur + H\omega t\,\vec u_z\]"),
    (r"Exprime \(\vec v\) et \(\vec a\) en cylindriques et retrouve leurs normes.",
     r"<p>\(\dot\rho = 0\), \(\dot\theta = \omega\), \(\ddot\theta = 0\), \(\dot z = H\omega\), \(\ddot z = 0\) :</p>\[\V = R\omega\,\ut + H\omega\,\vec u_z \qquad \A = -R\omega^2\,\ur\]<p>On retrouve \(v = \omega\sqrt{R^2+H^2}\) et \(a = R\omega^2\).</p>"),
    (r"(Version 2020) Déduis-en \(a_T\), \(a_N\) et le rayon de courbure \(R_c\).",
     r"<p>v est constante donc \(a_T = 0\) et \(a_N = a = R\omega^2\). Puis :</p>\[R_c = \frac{v^2}{a_N} = \frac{\omega^2(R^2+H^2)}{R\omega^2} = \frac{R^2 + H^2}{R}\]<p>Vérification : si H = 0, l’hélice devient un cercle et \(R_c = R\). Le sujet 2020 écrit \(\OM = R\vec u_\rho + Kt\,\vec u_z\) : remplace Hω par K et tu trouves \(R_c = \frac{R^2\omega^2 + K^2}{R\omega^2}\).</p>"),
   ]),
  dict(id="cone", title="La spirale sur un cône", chips=["Nov. 2018", "8 points"],
   src=[("Sujet nov. 2018", GH + "2023/midterm-2023-s1-phys-subject-fr.pdf")],
   enonce=r"En cylindriques : \(\rho(t) = \rho_0 e^{\omega t}\), \(\theta(t) = \omega t\), \(z(t) = k\rho_0 e^{\omega t}\). Le sujet appelle la constante <b>a</b> ; on l’appelle <b>k</b> ici pour ne pas la confondre avec l’accélération.",
   qs=[
    (r"Écris \(\OM\), déduis-en \(\vec v\) et montre que \(v = \rho_0\omega e^{\omega t}\sqrt{2 + k^2}\).",
     r"\[\OM = \rho_0 e^{\omega t}\,\ur + k\rho_0 e^{\omega t}\,\vec u_z\]<p>\(\dot\rho = \rho_0\omega e^{\omega t}\), \(\rho\dot\theta = \rho_0\omega e^{\omega t}\), \(\dot z = k\rho_0\omega e^{\omega t}\) :</p>\[\V = \rho_0\omega e^{\omega t}\left(\ur + \ut + k\,\vec u_z\right) \qquad v = \rho_0\omega e^{\omega t}\sqrt{1 + 1 + k^2}\]"),
    (r"Exprime \(\vec a\) et montre que \(a = \rho_0\omega^2 e^{\omega t}\sqrt{4 + k^2}\).",
     r"<p>\(\ddot\rho - \rho\dot\theta^2 = \rho_0\omega^2e^{\omega t} - \rho_0\omega^2e^{\omega t} = 0\) ; \(2\dot\rho\dot\theta + \rho\ddot\theta = 2\rho_0\omega^2e^{\omega t}\) ; \(\ddot z = k\rho_0\omega^2e^{\omega t}\).</p>\[\A = \rho_0\omega^2e^{\omega t}\left(2\,\ut + k\,\vec u_z\right) \qquad a = \rho_0\omega^2e^{\omega t}\sqrt{4 + k^2}\]"),
    (r"Donne x(t), y(t) et z(t) en cartésiennes.",
     r"\[x = \rho_0e^{\omega t}\cos(\omega t) \qquad y = \rho_0e^{\omega t}\sin(\omega t) \qquad z = k\rho_0e^{\omega t}\]"),
    (r"Calcule \(\vec v\) en cartésiennes et retrouve sa norme.",
     r"<p>Dérivée d’un produit : \(v_x = \rho_0\omega e^{\omega t}(\cos\omega t - \sin\omega t)\), \(v_y = \rho_0\omega e^{\omega t}(\sin\omega t + \cos\omega t)\), \(v_z = k\rho_0\omega e^{\omega t}\).</p><p>Comme \((\cos - \sin)^2 + (\sin + \cos)^2 = 2\), on retrouve \(v = \rho_0\omega e^{\omega t}\sqrt{2 + k^2}\).</p>"),
   ]),
  dict(id="spirale", title="La spirale logarithmique", chips=["2017", "6 points"],
   src=[("Sujet 2017", GH + "2022/midterm-2022-s1-phys-subject-fr.pdf")],
   enonce=r"\(x(t) = k e^{\omega t}\cos(\omega t)\) et \(y(t) = k e^{\omega t}\sin(\omega t)\), avec k et ω constantes positives (le sujet note la constante a).",
   qs=[
    (r"Écris \(\OM\) en coordonnées polaires.",
     r"<p>\(\rho = \sqrt{x^2+y^2} = ke^{\omega t}\) et \(\theta = \omega t\), donc \(\OM = ke^{\omega t}\,\ur\).</p>"),
    (r"Exprime \(\vec v\) en polaires et calcule sa norme.",
     r"\[\V = k\omega e^{\omega t}\,\ur + k\omega e^{\omega t}\,\ut \qquad v = \sqrt2\,k\omega e^{\omega t}\]"),
    (r"Exprime \(\vec a\) en polaires et calcule sa norme.",
     r"<p>\(\ddot\rho - \rho\dot\theta^2 = 0\) et \(2\dot\rho\dot\theta + \rho\ddot\theta = 2k\omega^2e^{\omega t}\) :</p>\[\A = 2k\omega^2e^{\omega t}\,\ut \qquad a = 2k\omega^2e^{\omega t}\]"),
    (r"Exprime \(a_T\) et \(a_N\) dans la base de Frenet, puis le rayon de courbure \(R_c\).",
     r"<p>\(a_T = \frac{dv}{dt} = \sqrt2\,k\omega^2e^{\omega t}\), puis \(a_N = \sqrt{a^2 - a_T^2} = \sqrt{4 - 2}\,k\omega^2e^{\omega t} = \sqrt2\,k\omega^2e^{\omega t}\).</p>\[R_c = \frac{v^2}{a_N} = \frac{2k^2\omega^2e^{2\omega t}}{\sqrt2\,k\omega^2e^{\omega t}} = \sqrt2\,ke^{\omega t}\]"),
   ]),
  dict(id="vilebrequin", title="Le vilebrequin", chips=["Oct. 2022", "6 points"], hot=True,
   src=[("Sujet 2022", GH + "2027/midterm-2027-s1-phys-subject-fr.pdf")],
   enonce=r"Dans un moteur, le point M tourne sur un cercle de centre O et de rayon R à vitesse angulaire ω constante : \(\theta(t) = \omega t\). Le piston P glisse sur l’axe Oy. L’énoncé donne \(\overrightarrow{OP} = (R\sin\theta + L\cos\theta)\,\vec u_y\), avec L constante.",
   qs=[
    (r"Partie 1. Donne \(\dot\theta(t)\) et le vecteur position \(\OM\).",
     r"<p>\(\dot\theta = \omega\). M est sur le cercle de rayon R : \(\OM = R\,\ur\). Il n’y a pas de terme en z, le mouvement est plan.</p>"),
    (r"Calcule \(\vec v_M\) et \(\vec a_M\) en fonction de R et ω.",
     r"<p>ρ = R constant et \(\ddot\theta = 0\) : c’est un mouvement circulaire uniforme.</p>\[\vec v_M = R\omega\,\ut \qquad \vec a_M = -R\omega^2\,\ur\]"),
    (r"Partie 2. Établis \(\vec v_P\) en fonction de R, L et ω.",
     r"\[\vec v_P = \frac{d\overrightarrow{OP}}{dt} = \left(R\omega\cos(\omega t) - L\omega\sin(\omega t)\right)\vec u_y\]"),
    (r"Établis \(\vec a_P\) en fonction de R, L et ω.",
     r"\[\vec a_P = -\omega^2\left(R\sin(\omega t) + L\cos(\omega t)\right)\vec u_y = -\omega^2\,\overrightarrow{OP}\]"),
   ]),
 ]),
 ("Cartésiennes et trajectoire", [
  dict(id="projectile", title="Le tir d’un projectile", chips=["Oct. 2022", "Nov. 2021", "8 points"], hot=True,
   src=[("Sujet 2022", GH + "2027/midterm-2027-s1-phys-subject-fr.pdf"), ("Sujet 2021", GH + "2026/midterm-2026-s1-phys-subject-fr.pdf"), ("Corrigé 2021", GH + "2026/midterm-2026-s1-phys-correction-fr.pdf")],
   enonce=r"Une balle est lancée depuis le point (0 ; h) avec une vitesse \(v_0\) qui fait un angle α avec l’horizontale. Son vecteur position est :<div class='eq'>\[\OM = (v_0\cos\alpha)\,t\,\vec u_x + \left(-\tfrac12gt^2 + (v_0\sin\alpha)\,t + h\right)\vec u_y\]</div>",
   qs=[
    (r"Donne les équations horaires du mouvement.",
     r"\[x(t) = (v_0\cos\alpha)\,t \qquad y(t) = -\tfrac12gt^2 + (v_0\sin\alpha)\,t + h\]<p>Ce sont des nombres : pas de \(\vec u_x\) ni de \(\vec u_y\) dans x(t) et y(t).</p>"),
    (r"Établis l’équation de la trajectoire.",
     r"<p>On isole \(t = \frac{x}{v_0\cos\alpha}\) et on remplace dans y :</p>\[y(x) = -\frac{g\,x^2}{2v_0^2\cos^2\alpha} + x\tan\alpha + h\]<p>C’est une parabole tournée vers le bas.</p>"),
    (r"Calcule \(\vec v(t)\) et sa norme.",
     r"\[\V = v_0\cos\alpha\,\vec u_x + (v_0\sin\alpha - gt)\,\vec u_y \qquad v = \sqrt{v_0^2\cos^2\alpha + (v_0\sin\alpha - gt)^2}\]"),
    (r"Calcule \(\vec a(t)\) et sa norme.",
     r"<p>\(\A = -g\,\vec u_y\), de norme g, constante.</p>"),
    (r"Qualifie le mouvement selon Ox et selon Oy.",
     r"<p>Selon Ox : \(v_x\) constante et \(a_x = 0\), <b>rectiligne uniforme</b>. Selon Oy : accélération constante −g, <b>uniformément varié</b> : décéléré à la montée, accéléré à la descente.</p>"),
    (r"Représente les vecteurs vitesse et accélération aux points M₁, M₂, M₃ et au sommet S.",
     r"<p>La vitesse est tangente à la parabole et horizontale en S. L’accélération est la même partout : verticale, vers le bas.</p>@@PROJECTILE@@"),
    (r"À quelle date \(t_S\) la balle atteint-elle le sommet ? Calcule les coordonnées \((x_S\ ;\ y_S)\) du sommet.",
     r"<p>Au sommet \(v_y = 0\), donc \(t_S = \frac{v_0\sin\alpha}{g}\). On remplace dans x(t) et y(t) :</p>\[x_S = \frac{v_0^2\sin\alpha\cos\alpha}{g} \qquad y_S = h + \frac{v_0^2\sin^2\alpha}{2g}\]<p>En 2021, le sujet prenait g = 10 (d’où le −5t²) et h = 0 : \(y_{max} = \frac{v_0^2\sin^2\alpha}{20}\).</p>"),
   ]),
  dict(id="cercle", title="Le cercle décalé", chips=["2017", "4 points"],
   src=[("Sujet 2017", GH + "2022/midterm-2022-s1-phys-subject-fr.pdf")],
   enonce=r"\(x(t) = 1 + R\sin(\omega t)\) et \(y(t) = 2 + R\cos(\omega t)\), avec ω et R constantes.",
   qs=[
    (r"Exprime les composantes de \(\vec v\) et calcule sa norme.",
     r"<p>\(v_x = R\omega\cos(\omega t)\), \(v_y = -R\omega\sin(\omega t)\), donc \(v = R\omega\).</p>"),
    (r"Exprime les composantes de \(\vec a\) et calcule sa norme.",
     r"<p>\(a_x = -R\omega^2\sin(\omega t)\), \(a_y = -R\omega^2\cos(\omega t)\), donc \(a = R\omega^2\).</p>"),
    (r"Trouve l’équation de la trajectoire. Précise sa nature et ses caractéristiques.",
     r"<p>\(x - 1 = R\sin(\omega t)\) et \(y - 2 = R\cos(\omega t)\). On additionne les carrés :</p>\[(x-1)^2 + (y-2)^2 = R^2\]<p>Cercle de centre (1 ; 2) et de rayon R. Comme v est constante, le mouvement est circulaire uniforme.</p>"),
   ]),
  dict(id="ellipse", title="L’ellipse", chips=["Nov. 2018", "Mai 2018", "2020", "4 à 6 points"],
   src=[("Sujet nov. 2018", GH + "2023/midterm-2023-s1-phys-subject-fr.pdf"), ("Corrigé 2020", GH + "2025/midterm-2025-s1-phys-correction-fr.pdf")],
   enonce=r"\(x(t) = 2a\cos(\omega t)\) et \(y(t) = a\sin(\omega t)\), avec a et ω constantes positives.",
   qs=[
    (r"Montre que la trajectoire est une ellipse et donne ses demi-axes A et B.",
     r"<p>\(\frac{x}{2a} = \cos(\omega t)\) et \(\frac ya = \sin(\omega t)\). On additionne les carrés :</p>\[\frac{x^2}{4a^2} + \frac{y^2}{a^2} = 1\]<p>Ellipse de demi-axes A = 2a (selon x) et B = a (selon y).</p>"),
    (r"Exprime \(\vec v\) et sa norme.",
     r"<p>\(v_x = -2a\omega\sin(\omega t)\), \(v_y = a\omega\cos(\omega t)\).</p>\[v = a\omega\sqrt{4\sin^2(\omega t) + \cos^2(\omega t)} = a\omega\sqrt{1 + 3\sin^2(\omega t)}\]<p>Astuce : \(4\sin^2 + \cos^2 = 3\sin^2 + (\sin^2 + \cos^2) = 1 + 3\sin^2\).</p>"),
    (r"Exprime \(\vec a\) et sa norme.",
     r"<p>\(a_x = -2a\omega^2\cos(\omega t)\), \(a_y = -a\omega^2\sin(\omega t)\), donc \(a = a\omega^2\sqrt{1 + 3\cos^2(\omega t)}\).</p>"),
    (r"Trouve une relation entre \(\vec a\) et \(\OM\).",
     r"<p>\(a_x = -\omega^2x\) et \(a_y = -\omega^2y\), donc \(\A = -\omega^2\,\OM\) : l’accélération pointe toujours vers O.</p>"),
   ]),
  dict(id="droite", title="La droite cachée", chips=["2020", "5 points"],
   src=[("Corrigé 2020", GH + "2025/midterm-2025-s1-phys-correction-fr.pdf")],
   enonce=r"\(x(t) = \sin^2(\omega t)\) et \(y(t) = 1 + \cos(2\omega t)\). On donne \(\cos(2\omega t) = 1 - 2\sin^2(\omega t)\).",
   qs=[
    (r"Trouve l’équation de la trajectoire et sa nature, puis trace-la.",
     r"<p>\(y = 1 + 1 - 2\sin^2(\omega t) = 2 - 2x\). C’est une droite. Comme \(0 \le \sin^2 \le 1\), le point ne parcourt que le <b>segment</b> de (0 ; 2) à (1 ; 0), en faisant des allers-retours.</p>"),
    (r"Exprime les composantes de \(\vec v\) et sa norme.",
     r"<p>\(v_x = 2\omega\sin(\omega t)\cos(\omega t) = \omega\sin(2\omega t)\) et \(v_y = -2\omega\sin(2\omega t)\).</p>\[v = \sqrt{\omega^2\sin^2(2\omega t) + 4\omega^2\sin^2(2\omega t)} = \sqrt5\,\omega\,|\sin(2\omega t)|\]<p>Attention : le corrigé scanné de 2020 trouve \(\sqrt2\,\omega|\sin 2\omega t|\) avec une erreur sur \(v_y\). Sur la droite y = 2 − 2x, on doit avoir \(v_y = -2v_x\), ce qui confirme \(\sqrt5\).</p>"),
   ]),
  dict(id="cycloide", title="La cycloïde", chips=["2019", "6 points"],
   src=[("Sujet 2019", GH + "2024/midterm-2024-s1-phys-subject-fr.pdf"), ("Corrigé 2019", GH + "2024/midterm-2024-s1-phys-correction-fr.pdf")],
   enonce=r"Un point d’une roue qui roule sans glisser : \(x(t) = A(\omega t - \sin\omega t)\) et \(y(t) = A(1 - \cos\omega t)\), avec A et ω constantes positives.",
   qs=[
    (r"Donne les composantes cartésiennes de \(\vec v\) et de \(\vec a\).",
     r"\[v_x = A\omega(1 - \cos\omega t) \quad v_y = A\omega\sin\omega t \qquad a_x = A\omega^2\sin\omega t \quad a_y = A\omega^2\cos\omega t\]"),
    (r"Déduis-en les normes. On donne \(1 - \cos\alpha = 2\sin^2(\alpha/2)\).",
     r"<p>\(v^2 = A^2\omega^2\left[(1-\cos)^2 + \sin^2\right] = A^2\omega^2(2 - 2\cos\omega t) = 4A^2\omega^2\sin^2(\omega t/2)\).</p>\[v = 2A\omega\,|\sin(\omega t/2)| \qquad a = A\omega^2\ \text{(constante)}\]"),
    (r"Trace la cycloïde sur deux périodes, avec \(\omega = 2\pi/T\).",
     r"<p>Points utiles : t = 0 → (0 ; 0) ; T/4 → (A(π/2 − 1) ; A) ; T/2 → (πA ; 2A) ; 3T/4 → (A(3π/2 + 1) ; A) ; T → (2πA ; 0). On obtient des arches de hauteur 2A.</p>@@CYCLOID@@"),
   ]),
 ]),
 ("Base de Frenet", [
  dict(id="frenetv", title="Frenet avec une vitesse donnée", chips=["2019", "4 points"],
   src=[("Sujet 2019", GH + "2024/midterm-2024-s1-phys-subject-fr.pdf"), ("Corrigé 2019", GH + "2024/midterm-2024-s1-phys-correction-fr.pdf")],
   enonce=r"Un point décrit un cercle de centre O et de rayon R avec une vitesse \(v(t) = \frac{v_0}{1 + \alpha t}\) (v₀ et α constantes positives), et s(0) = 0.",
   qs=[
    (r"Exprime l’abscisse curviligne s(t).",
     r"\[s(t) = \int_0^t \frac{v_0}{1 + \alpha t}\,dt = \frac{v_0}{\alpha}\ln(1 + \alpha t)\]"),
    (r"Au bout de combien de temps le mobile fait-il un tour ?",
     r"<p>Un tour = \(2\pi R\). On résout \(s(T) = 2\pi R\) : \(\ln(1 + \alpha T) = \frac{2\pi R\alpha}{v_0}\), donc :</p>\[T = \frac{1}{\alpha}\left(e^{2\pi R\alpha/v_0} - 1\right)\]"),
    (r"Exprime \(a_T\), \(a_N\) et la norme de l’accélération.",
     r"\[a_T = \frac{dv}{dt} = -\frac{\alpha v_0}{(1+\alpha t)^2} \qquad a_N = \frac{v^2}{R} = \frac{v_0^2}{R(1+\alpha t)^2}\]<p>\(a_T &lt; 0\) : le mobile ralentit. Norme : \(a = \frac{v_0}{(1+\alpha t)^2}\sqrt{\alpha^2 + \frac{v_0^2}{R^2}}\).</p>"),
   ]),
  dict(id="freneta", title="Frenet avec une accélération donnée", chips=["2017", "6 points"],
   src=[("Sujet 2017", GH + "2022/midterm-2022-s1-phys-subject-fr.pdf")],
   enonce=r"Un point se déplace dans un plan avec \(\A = \alpha\,\uT + \beta t^2\,\uN\) (α, β constantes positives), v(0) = 0 et s(0) = 0.",
   qs=[
    (r"Quelles sont les unités de α et β ? Justifie.",
     r"<p>Chaque terme est une accélération (m·s⁻²). Donc α est en m·s⁻², et βt² aussi, d’où β en m·s⁻⁴.</p>"),
    (r"Calcule l’abscisse curviligne s(t).",
     r"<p>\(a_T = \frac{dv}{dt} = \alpha\), donc \(v = \alpha t\) (car v(0) = 0), puis \(s(t) = \frac12\alpha t^2\).</p>"),
    (r"Montre que le rayon de courbure vaut \(R_c = \frac{\alpha^2}{\beta}\).",
     r"<p>\(a_N = \frac{v^2}{R_c}\) donne \(\beta t^2 = \frac{\alpha^2t^2}{R_c}\), donc \(R_c = \frac{\alpha^2}{\beta}\). Il est constant : la trajectoire est un cercle.</p>"),
   ]),
 ]),
]

def exos_html(figs):
    out = []
    for gname, items in EXOS:
        out.append(f'<div class="ex-group"><h3>{gname}</h3>')
        for e in items:
            chips = "".join(f'<span class="chip">{c}</span>' for c in e["chips"])
            if e.get("hot"):
                chips = '<span class="chip hot">format actuel</span>' + chips
            qs = []
            for i, (qt, corr) in enumerate(e["qs"], 1):
                for k, v in figs.items():
                    corr = corr.replace(f"@@{k}@@", f'<figure class="panel" style="margin:10px 0 0">{v}</figure>')
                tid, cid = f'a-{e["id"]}-{i}', f'c-{e["id"]}-{i}'
                qs.append(f'<li class="qa"><p>{qt}</p>'
                          f'<textarea id="{tid}" aria-label="Ta réponse à la question {i}" placeholder="Écris ta réponse ici…" spellcheck="false"></textarea>'
                          f'<div class="row"><button class="show" type="button" aria-expanded="false" aria-controls="{cid}">Voir la correction</button></div>'
                          f'<div class="corr" id="{cid}" hidden>{corr}</div></li>')
            src = " · ".join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in e["src"])
            out.append(f'<article class="ex" id="ex-{e["id"]}"><div class="ex-head"><h4>{e["title"]}</h4><div class="chips">{chips}</div></div>'
                       f'<div class="enonce"><b>Énoncé.</b> {e["enonce"]}</div><ol class="qs">{"".join(qs)}</ol>'
                       f'<div class="ex-foot"><label class="done-lbl"><input type="checkbox" id="d-{e["id"]}"> J’ai réussi cet exercice</label>'
                       f'<span class="src-link">Original : {src}</span></div></article>')
        out.append("</div>")
    return "\n".join(out)

# ---------------- Annales ----------------
ANNALES = [
    dict(date="Octobre 2022", dir="2027", recent=True,
         items=["QCM de 6 points, réponses multiples", "Tir d’un projectile depuis (0 ; h), 8 points", "Vilebrequin en polaires et cartésiennes, 6 points"],
         exos=[("projectile", "Projectile"), ("vilebrequin", "Vilebrequin")],
         sujet=GH + "2027/midterm-2027-s1-phys-subject-fr.pdf", corr=None,
         warn="Le sujet en ligne est une copie d’étudiant annotée (10,5/20) : ne te fie pas aux réponses écrites dessus."),
    dict(date="Novembre 2021", dir="2026", recent=True,
         items=["QCM de 2,5 points", "Base polaire et ses dérivées, 8 points", "Tir d’un projectile, 5,5 points", "Accélération circulaire, 4 points"],
         exos=[("base", "Base polaire"), ("projectile", "Projectile")],
         sujet=GH + "2026/midterm-2026-s1-phys-subject-fr.pdf", corr=GH + "2026/midterm-2026-s1-phys-correction-fr.pdf", warn=None),
    dict(date="Novembre 2020", dir="2025", recent=False,
         items=["QCM de 4 points", "Ellipse, 5 points", "Trajectoire en droite, 5 points", "Hélice et Frenet, 6 points"],
         exos=[("ellipse", "Ellipse"), ("droite", "Droite"), ("helice", "Hélice")],
         sujet=None, corr=GH + "2025/midterm-2025-s1-phys-correction-fr.pdf", warn="Le sujet est inclus dans le corrigé."),
    dict(date="Novembre 2019", dir="2024", recent=False,
         items=["QCM de 4 points", "Cycloïde, 6 points", "Hélice en cartésiennes et cylindriques, 6 points", "Frenet avec v = v₀/(1 + αt), 4 points"],
         exos=[("cycloide", "Cycloïde"), ("helice", "Hélice"), ("frenetv", "Frenet")],
         sujet=GH + "2024/midterm-2024-s1-phys-subject-fr.pdf", corr=GH + "2024/midterm-2024-s1-phys-correction-fr.pdf", warn=None),
    dict(date="Novembre 2018", dir="2023", recent=False,
         items=["QCM de 4 points", "Ellipse, 4 points", "Spirale sur un cône, 8 points", "Cercle et Frenet, 4 points"],
         exos=[("ellipse", "Ellipse"), ("cone", "Spirale sur un cône")],
         sujet=GH + "2023/midterm-2023-s1-phys-subject-fr.pdf", corr=None, warn=None),
    dict(date="Mai 2018 (S1#)", dir="2023#", recent=False,
         items=["QCM de 5 points", "Ellipse, 6 points", "Hélice en cartésiennes et cylindriques, 9 points"],
         exos=[("ellipse", "Ellipse"), ("helice", "Hélice")],
         sujet=GH + "2023%23/midterm-2023%23-s1-phys-subject-fr.pdf", corr=GH + "2023%23/midterm-2023%23-s1-phys-correction-fr.pdf", warn=None),
    dict(date="Novembre 2017", dir="2022", recent=False,
         items=["QCM de 4 points", "Cercle décalé, 4 points", "Spirale logarithmique et Frenet, 6 points", "Frenet avec α et β, 6 points"],
         exos=[("cercle", "Cercle décalé"), ("spirale", "Spirale"), ("freneta", "Frenet")],
         sujet=GH + "2022/midterm-2022-s1-phys-subject-fr.pdf", corr=None, warn=None),
]

def annales_html():
    out = []
    for a in ANNALES:
        cls = "an recent" if a["recent"] else "an"
        badge = '<span class="chip hot">format actuel</span>' if a["recent"] else ""
        items = "".join(f"<li>{x}</li>" for x in a["items"])
        ex = " · ".join(f'<a href="#ex-{i}">{n}</a>' for i, n in a["exos"])
        links = []
        links.append(f'<a href="{a["sujet"]}" target="_blank" rel="noopener">Sujet</a>' if a["sujet"] else '<span>Sujet dans le corrigé</span>')
        links.append(f'<a href="{a["corr"]}" target="_blank" rel="noopener">Corrigé</a>' if a["corr"] else '<span>Pas de corrigé</span>')
        warn = f'<p class="warn" style="margin:0">{a["warn"]}</p>' if a["warn"] else ""
        out.append(f'<article class="{cls}"><div class="an-top"><span class="an-date">{a["date"]}</span>{badge}</div>'
                   f'<span class="an-dir">Dossier {a["dir"]}</span><ul>{items}</ul>'
                   f'<p class="small" style="margin:0"><b>Exercices corrigés ici :</b> {ex}</p>{warn}'
                   f'<div class="links2">{"".join(links)}</div></article>')
    return "\n".join(out)

# ---------------- Fiche ----------------
FICHE = [
    ("Norme", r"\[\|\vec V\| = \sqrt{V_x^2 + V_y^2 + V_z^2}\]"),
    ("Produit scalaire", r"\[\vec U\cdot\vec V = U_xV_x + U_yV_y + U_zV_z = UV\cos\alpha\]"),
    ("Produit vectoriel", r"\[\|\vec U\wedge\vec V\| = UV|\sin\alpha|\]"),
    ("Vitesse et accélération", r"\[\V = \frac{d\OM}{dt} \qquad \A = \frac{d\V}{dt} = \frac{d^2\OM}{dt^2}\]"),
    ("Passage polaire → cartésien", r"\[x = \rho\cos\theta \qquad y = \rho\sin\theta\]"),
    ("Base polaire", r"\[\ur = (\cos\theta\ ;\ \sin\theta) \qquad \ut = (-\sin\theta\ ;\ \cos\theta)\]"),
    ("Dérivées de la base", r"\[\frac{d\ur}{dt} = \dot\theta\,\ut \qquad \frac{d\ut}{dt} = -\dot\theta\,\ur\]"),
    ("Position", r"\[\OM = \rho\,\ur\ \ (+\,z\,\vec u_z)\]"),
    ("Vitesse polaire", r"\[\V = \dot\rho\,\ur + \rho\dot\theta\,\ut\ \ (+\,\dot z\,\vec u_z)\]"),
    ("Accélération polaire", r"\[\A = (\ddot\rho - \rho\dot\theta^2)\,\ur + (2\dot\rho\dot\theta + \rho\ddot\theta)\,\ut\]"),
    ("Circulaire uniforme", r"\[v = R\omega \qquad \A = -R\omega^2\,\ur \qquad a = R\omega^2 = \frac{v^2}{R}\]"),
    ("Abscisse curviligne", r"\[v = \frac{ds}{dt} \qquad s = R\theta \text{ sur un cercle}\]"),
    ("Frenet", r"\[\V = v\,\uT \qquad \A = \frac{dv}{dt}\,\uT + \frac{v^2}{R_c}\,\uN\]"),
    ("Rayon de courbure", r"\[R_c = \frac{v^2}{a_N} \qquad a_N = \sqrt{a^2 - a_T^2}\]"),
    ("Accéléré ou décéléré", r"\[\V\cdot\A > 0 \text{ : accéléré} \qquad \V\cdot\A < 0 \text{ : décéléré}\]"),
    ("Projectile : sommet", r"\[t_S = \frac{v_0\sin\alpha}{g} \qquad y_S = h + \frac{v_0^2\sin^2\alpha}{2g}\]"),
    ("Trigonométrie", r"\[\cos^2x + \sin^2x = 1 \qquad \cos 2x = 1 - 2\sin^2x \qquad \sin 2x = 2\sin x\cos x\]"),
    ("Méthode d’exercice", r"<p style='margin:0'>Écrire \(\OM\) → dériver pour \(\vec v\) → dériver pour \(\vec a\) → normes → simplifier avec cos² + sin² = 1 → interpréter.</p>"),
]

def fiche_html():
    return "\n".join(f'<div class="fc" tabindex="0"><h4>{t}</h4><div class="body">{b}</div></div>' for t, b in FICHE)
