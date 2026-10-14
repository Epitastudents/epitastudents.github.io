# Maintenance de l'appli « Mécanique S1 »

Ce fichier explique comment mettre l'appli à jour. Il sert aussi de consignes à la tâche programmée hebdomadaire.

## Ce qui est publié

Le dépôt est le site GitHub Pages de l'organisation : `epitastudents.github.io`. Tout ce qui est poussé sur `main` est en ligne environ une minute après.

| Chemin | Rôle |
| --- | --- |
| `index.html` | Accueil du site (généré) |
| `cinematique-s1/` | L'appli installable (générée). Le nom du dossier est historique : on le garde pour ne pas casser les applis déjà installées. |
| `src/` | Les sources : on ne modifie que ces fichiers, puis on reconstruit. |

## Reconstruire

```sh
pip install --break-system-packages qrcode pillow   # une fois par session
python3 src/build.py https://epitastudents.github.io/
```

Le script réécrit `index.html` et le dossier `cinematique-s1/`. Le service worker change de version (empreinte du contenu) : les téléphones voient le bandeau « Nouvelle version disponible ». Ne jamais modifier à la main les fichiers générés.

## Où est le contenu

Le contenu suit le cours de mécanique S1 de Moodle (poly « Cours cinématique V4 », fiche coordonnées, TD1 à TD8 2026). On garde les notations du poly : coordonnées polaires (r, θ), base (u_r, u_θ).

- `src/cours.py` contient tout :
  - `CHAPITRES` : 9 chapitres (0 = rappels de maths, puis un par TD).
  - `LECONS` : pour chaque chapitre, une liste de cartes courtes. Une carte = une idée. Champs : `t` (titre), `h` (texte, 80 mots au plus), `k` (formule à retenir), `fig` (schéma), `piege` (erreur fréquente).
  - `QCM` : `(chapitre, question, [(lettre, réponse)…], "bonne(s) lettre(s)", explication[, True si plusieurs réponses])`.
  - `EXOS` : exercices de TD, en étapes `(question, indice, correction)`. `officiel=True` seulement si la correction vient d'un corrigé publié sur Moodle.
  - `FICHES` : cartes mémoire `(chapitre, question, réponse)`.
  - `ANNALES` : anciens contrôles Epidocs (ancien format).
- `src/app.html` : l'interface (écrans, QCM, exercices, révision espacée).
- `src/figs.py`, `src/figs2.py` : les schémas SVG (géométrie calculée).

Formules : LaTeX entre `\( … \)` ou `\[ … \]`. Macros : `\OM`, `\V`, `\A`, `\ur`, `\ut`. Plusieurs formules dans un même `\[ … \]`, séparées par `\qquad`, sont automatiquement mises sur des lignes séparées.

## Principes de design (à respecter)

- Une idée par écran, aucune page interminable.
- Rien de décoratif : pas de fond à motif, pas d'illustration sans rapport. La couleur sert seulement aux vecteurs (v bleu, a rouge, u_r violet, u_θ vert) et à la correction.
- On privilégie l'entraînement actif : QCM, exercices guidés, cartes mémoire espacées.

## Mettre à jour le contenu

Sources possibles :
1. Le dépôt public `Epidocs/past-exams`, dossiers `S1/Midterms/Phys` et `S1/Finals/Phys`. La liste des fichiers déjà vus est dans `src/annales_connues.txt`.
   ```sh
   GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 --filter=blob:none --no-checkout https://github.com/Epidocs/past-exams /tmp/pe
   git -C /tmp/pe ls-tree -r --name-only HEAD | grep -E '^S1/(Midterms|Finals)/Phys/' | sort > /tmp/actuel.txt
   comm -13 src/annales_connues.txt /tmp/actuel.txt   # fichiers nouveaux
   ```
2. De nouveaux fichiers de cours, de TD ou de corrigés envoyés par le propriétaire.

Pour un nouveau sujet : le lire (les scans se rendent en images avec `pdftoppm -r 90 -gray -png`), ajouter les questions de QCM nouvelles au bon chapitre, et les exercices dont le modèle est nouveau. Refaire chaque calcul. Pour un nouveau corrigé de TD : remplacer la correction proposée et passer `officiel=True`.

## Publier

```sh
git add -A
git -c user.name="Révisions S1" -c user.email="bot@revisions-s1.invalid" commit -m "Contenu : <résumé>"
git push origin HEAD
```

Les commits sont toujours signés « Révisions S1 ». On n'y met jamais le nom, le pseudo ni l'adresse du propriétaire du compte. Après le push, vérifier que `https://epitastudents.github.io/cinematique-s1/` est à jour (une à deux minutes de délai).
