# Maintenance de l'appli « Cinématique S1 »

Ce fichier explique comment mettre l'appli à jour. Il sert aussi de consignes à la tâche programmée qui vérifie chaque semaine s'il y a du nouveau.

## Ce qui est publié

Le dépôt est un site GitHub Pages d'organisation (`epitastudents.github.io` (organisation Epitastudents)). Tout ce qui est poussé sur la branche par défaut est en ligne environ une minute après.

| Chemin | Rôle |
| --- | --- |
| `index.html` | Accueil du site, liste des applis (généré) |
| `cinematique-s1/` | L'appli installable : `index.html`, `installer.html`, `manifest.webmanifest`, `sw.js`, `icons/`, `vendor/mathjax/` (tout est généré) |
| `src/` | Les sources : on ne modifie que ces fichiers, puis on reconstruit |

## Reconstruire

```sh
pip install --break-system-packages qrcode pillow   # une fois par session
python3 src/build.py https://epitastudents.github.io/
```

Le script réécrit `index.html` et tout le dossier `cinematique-s1/`. Le service worker reçoit une nouvelle version (empreinte du contenu). Les téléphones qui ont installé l'appli voient alors le bandeau « Nouvelle version disponible ». Il ne faut jamais modifier à la main les fichiers générés.

Les icônes se refont avec `python3 src/make_icons.py src/icons`. On ne le fait que si le dessin change.

## Où est le contenu

- `src/content.py` contient les données :
  - `BARS` : les barres « Ce qui tombe » (thème, nombre de sujets, années, lien).
  - `QCM` : les questions, sous la forme `(source, énoncé, [(lettre, réponse)…], "bonne(s) lettre(s)", explication[, True si plusieurs réponses])`.
  - `EXOS` : les exercices, regroupés par thème. Chaque exercice a un `id` unique, des `chips`, des liens `src`, un `enonce` et des `qs` sous la forme (question, correction).
  - `ANNALES` : une carte par sujet, du plus récent au plus ancien.
  - `FICHE` : les formules de la fiche.
- `src/template.html` contient le cours (chapitres 1 à 5), les styles et le script de la page.
- `src/figs.py` contient les schémas SVG, dont la géométrie est calculée.

Les formules s'écrivent en LaTeX entre `\( … \)` (en ligne) ou `\[ … \]` (bloc). Les macros `\OM`, `\V`, `\A`, `\ur`, `\ut`, `\uT`, `\uN` colorent les vecteurs.

Les nombres de QCM, d'exercices et de sujets, ainsi que la plage d'années, sont calculés automatiquement à partir de `content.py`. Les textes qui disent « 7 sujets » dans la section « Ce qui tombe » et les valeurs de `BARS` (sur 7) sont à mettre à jour à la main quand un sujet s'ajoute.

## Vérifier s'il y a de nouveaux sujets

La source est le dépôt public `Epidocs/past-exams`, dans les dossiers `S1/Midterms/Phys` et `S1/Finals/Phys`. Les noms de dossiers sont des années de promo, pas des années d'examen. La liste des fichiers déjà traités est dans `src/annales_connues.txt`.

```sh
GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 --filter=blob:none --no-checkout https://github.com/Epidocs/past-exams /tmp/pe
git -C /tmp/pe ls-tree -r --name-only HEAD | grep -E '^S1/(Midterms|Finals)/Phys/' | sort > /tmp/actuel.txt
comm -13 src/annales_connues.txt /tmp/actuel.txt   # fichiers nouveaux
```

Pour chaque nouveau sujet de contrôle (`Midterms`) :

1. Lire le sujet et, s'il existe, le corrigé. Beaucoup sont scannés : on les rend en images (`pdftoppm -r 90 -gray -png`) et on les regarde.
2. Ajouter une carte dans `ANNALES`, puis les nouvelles questions de QCM (sans doublon) et les exercices qui ont un nouveau modèle.
3. Refaire chaque calcul soi-même. Les corrigés scannés contiennent parfois des erreurs : on les signale dans la correction.
4. Mettre à jour `BARS` et le texte « Ce qui tombe » si la répartition des thèmes change.
5. Ajouter les nouveaux chemins à `src/annales_connues.txt`, reconstruire et pousser.

Les nouveaux sujets de partiel (`Finals`) relèvent d'un module « Partiel » à part (statique, lois de Newton, travail et énergie). Ils n'entrent pas dans ce contrôle.

## Publier

```sh
git add -A
git -c user.name="Révisions S1" -c user.email="bot@revisions-s1.invalid" commit -m "Contenu : <résumé>"
git push origin HEAD
```

Les commits sont toujours signés « Révisions S1 » : on ne met jamais le nom ni l'adresse du propriétaire du compte. Après le push, on vérifie que `https://epitastudents.github.io/cinematique-s1/sw.js` affiche bien la nouvelle `VERSION` (une à deux minutes de délai).
