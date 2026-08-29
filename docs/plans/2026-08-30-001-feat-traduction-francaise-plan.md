---
title: "feat: Version française canonique + anglais sous /en/"
date: 2026-08-30
type: feat
depth: standard
origin: docs/brainstorms/2026-08-30-traduction-francaise-requirements.md
---

# feat: Version française canonique + anglais sous `/en/`

## Résumé

Le portfolio passe en bilingue sans étape de build : le français devient la version
canonique à la racine, l'anglais est déplacé sous `en/`, les deux arbres sont des
miroirs stricts (mêmes noms de fichiers), et un skill projet impose la checklist de
synchronisation à chaque édition.

18 pages au total (2 × 9), un sélecteur `FR / EN` en dur dans la topbar, aucun JS de
détection, aucune règle serveur.

---

## Problème

Le site est intégralement en anglais et rien ne permet de partager un lien en français.
La contrainte structurante est que le repo *est* le site : pas de build, pas de CI,
pages éditables à la main (`build.py` a été supprimé délibérément au commit `dea7cf9`).
Le coût réel d'une architecture à deux arbres est la **dérive** — une page mise à jour
d'un côté et pas de l'autre. Le plan traite ça comme un problème de procédure, pas
d'outillage.

---

## Exigences couvertes

| ID | Exigence (origine) | Unités |
|----|--------------------|--------|
| R1 | Noms de fichiers identiques des deux côtés | U1 |
| R2 | Sélecteur `FR / EN` en dur dans la topbar | U2 |
| R3 | `lang` correct + `hreflang` croisés | U2 |
| R4 | Chaînes JS (`Copy`/`Copied`/`Close`) suivant `documentElement.lang` | U2 |
| R5 | Contenu traduit (titres, prose, cartes, footer) | U3, U4, U5 |
| R5b | Blocs techniques laissés en anglais, identiques des deux côtés | U3, U4, U5 |
| R6 | Skill projet de synchronisation | U6 |
| R7 | README à jour | U7 |

Voir l'origine : `docs/brainstorms/2026-08-30-traduction-francaise-requirements.md`.

---

## Décisions techniques

### D1 — Dupliquer l'arbre avant de traduire

U1 crée les deux arbres avec un contenu **identique en anglais** des deux côtés, puis la
traduction se fait page par page. Le site reste navigable et complet à chaque commit —
important puisque chaque push est déployé. L'alternative (déplacer sous `en/` puis écrire
le français) laisse la racine cassée entre deux commits.

### D2 — Le sélecteur vit en dehors de `.nav`

`assets/site.js` construit le tiroir mobile en lisant `[...document.querySelectorAll('.nav a')]`.
Un lien de langue placé dans `.nav` serait avalé dans la liste du tiroir aux côtés de
« Projets » et « À propos ». Le sélecteur est donc un élément frère de `.nav`, toujours
visible, avec ses propres styles dans `assets/site.css`.

### D3 — Lien de contrepartie en dur, pas calculé

Chaque page contient l'URL relative exacte de sa contrepartie. Pas de dérivation JS du
chemin : ça marche sans JS, c'est lisible dans la source, et un lien cassé se voit à la
relecture. Le prix est une ligne de plus dans la checklist du skill.

### D4 — Lexique figé, versionné dans le skill

Les titres de section reviennent à l'identique sur les 8 pages projet. La table de
correspondance est établie en U3 sur la page pilote, puis vit dans le skill : toute page
future utilise les mêmes mots sans avoir à relire une page existante.

| Anglais | Français |
|---------|----------|
| Projects | Projets |
| About | À propos |
| Open → | Ouvrir → |
| Repository | Dépôt |
| What it does | Ce que ça fait |
| Stack | Stack *(inchangé)* |
| Architecture | Architecture *(inchangé)* |
| Decisions | Décisions |
| Run it | Le lancer |
| Deploy & ops | Déploiement & ops |
| how it is built | sous le capot |
| `· project ·` | `· projet ·` |
| dark by default | sombre par défaut |
| Copy / Copied / Close | Copier / Copié / Fermer |

### D5 — Pas de harnais de test

Le repo n'en contient aucun et ce plan n'en introduit pas. La vérification est un audit
manuel énuméré par unité : serveur local, parcours des liens, contrôle des chemins
d'assets. Chaque unité liste ses contrôles explicitement.

---

## Arborescence cible

```
index.html                    FR — home
projects/<slug>.html          FR — 8 pages projet
en/index.html                 EN — home
en/projects/<slug>.html       EN — 8 pages projet
assets/site.css               + styles du sélecteur de langue
assets/site.js                + dictionnaire des 3 chaînes UI
.claude/skills/portfolio-page/SKILL.md
README.md
docs/                         brainstorms & plans (non liés depuis le site)
```

Profondeurs relatives vers `assets/` :

| Fichier | Chemin |
|---------|--------|
| `index.html` | `assets/…` |
| `projects/*.html` | `../assets/…` |
| `en/index.html` | `../assets/…` |
| `en/projects/*.html` | `../../assets/…` |

---

## Unités d'implémentation

### U1. Créer les deux arbres et corriger les chemins relatifs

**Objectif** — Obtenir `en/` et la racine, contenu anglais identique des deux côtés, tous
les chemins relatifs et liens internes corrects.

**Exigences** — R1
**Dépendances** — aucune

**Fichiers**
- Créer `en/index.html`, `en/projects/{screenator,screen,ytp,theoproject,guess,bbc,theoapi,self-pages}.html`
- Conserver `index.html` et `projects/*.html` à la racine (contenu EN pour l'instant)

**Approche**
Copier les 9 pages actuelles dans `en/` en conservant les noms de fichiers. Dans l'arbre
`en/`, ajouter un cran à tous les chemins relatifs : `assets/` → `../assets/` pour
`en/index.html`, `../assets/` → `../../assets/` pour `en/projects/*.html`. Même chose pour
les liens internes (`../index.html` → `../../index.html` dans les pages projet EN, wordmark
et nav compris). Les URLs absolues (design system, GitHub, LinkedIn, domaines des projets)
ne bougent pas.

**Modèles à suivre** — Le gabarit de `projects/ytp.html` est représentatif : les 8 pages
projet partagent la même structure de topbar, fil d'ariane, `page-head` et footer.

**Vérification**
- `python3 -m http.server 8080` : `/` et `/en/` chargent avec les styles appliqués
- Aucune 404 sur `assets/site.css`, `assets/site.js`, `assets/avatar.webp` depuis les 18 pages
- Depuis chaque page projet de `en/`, le wordmark et le fil d'ariane mènent à `en/index.html`, pas à la racine
- Depuis `en/index.html`, les 8 cartes mènent bien vers `en/projects/`
- Un `grep` de `href="assets/` dans `en/` et de `href="../../assets/` à la racine ne remonte rien

**Attente de tests : aucune** — duplication et réécriture de chemins, aucun comportement nouveau.

---

### U2. Poser l'infrastructure bilingue sur les 18 pages

**Objectif** — Chaque page déclare sa langue, pointe vers sa contrepartie, et offre le
sélecteur `FR / EN`.

**Exigences** — R2, R3, R4
**Dépendances** — U1

**Fichiers**
- Modifier les 18 pages HTML
- Modifier `assets/site.css` (styles `.langsw`)
- Modifier `assets/site.js` (dictionnaire des chaînes UI)

**Approche**
Sur chaque page : `lang="fr"` à la racine, `lang="en"` sous `en/`, plus deux
`<link rel="alternate" hreflang="fr|en" href="…">` croisés pointant vers la contrepartie.

Le sélecteur est un élément frère de `.nav` dans `.topbar` (voir D2) : la langue courante
est un élément inerte, l'autre un lien relatif en dur vers la page contrepartie (D3). Ses
styles vivent dans `assets/site.css` et reprennent la grammaire visuelle de `.contact a`
(mono, majuscules, `var(--faint)` pour l'inactif, `var(--peri)` au survol).

Dans `assets/site.js`, un dictionnaire à deux entrées en tête de fichier fournit `copy`,
`copied` et `close` ; la langue est lue une fois via `document.documentElement.lang`, avec
repli sur l'anglais pour toute valeur inattendue.

**Modèles à suivre** — `.contact a` dans `assets/site.css` pour le style des petits liens
encadrés ; le bloc `.copy` existant de `assets/site.js` pour le point d'insertion.

**Vérification**
- Depuis `/projects/ytp.html`, cliquer `EN` mène à `/en/projects/ytp.html`, et le retour `FR` ramène exactement à la page de départ — vérifié sur les 9 paires
- La langue courante n'est pas cliquable
- Le tiroir mobile (bouton burger) ne contient que les liens de navigation, pas le sélecteur
- Sur une page `en/`, le bouton d'un `code-block` affiche `Copy` puis `Copied` ; sur la page racine correspondante, `Copier` puis `Copié`
- Le bouton de fermeture du tiroir affiche `Close` sous `en/` et `Fermer` à la racine
- Une page avec un `lang` inconnu retomberait sur l'anglais (contrôle par lecture du code, pas de page de test à créer)
- Chaque page a exactement deux `hreflang`, dont l'un pointe vers elle-même et l'autre vers une page qui existe

---

### U3. Traduire la page pilote et figer le lexique

**Objectif** — `projects/ytp.html` entièrement en français, et la table de correspondance
de D4 validée en conditions réelles.

**Exigences** — R5, R5b
**Dépendances** — U2

**Fichiers**
- Modifier `projects/ytp.html`

**Approche**
Traduire : `<title>`, fil d'ariane, `eyebrow` (`· projet · 03`), `display`, `sub`, libellés
des boutons d'action, `stat-label` et `stat-delta`, titres de section, prose des `.feature`,
étapes du `.flow`, intitulés et corps des `.decisions`, en-têtes de tableau, footer.

Restent **inchangés, mot pour mot** avec la version anglaise (R5b) : les descriptions
d'endpoints dans le `<tbody>` du tableau `.ledger`, les `meta-label` et `meta-value` des
blocs Stack et Déploiement, et le contenu des `.code-block` (y compris les commentaires
`c-com`). Seuls les titres de section qui les encadrent sont traduits.

C'est la page pilote : toute hésitation de vocabulaire est tranchée ici et reportée dans
la table de D4, qui sera copiée dans le skill en U6.

**Vérification**
- Aucune phrase anglaise résiduelle hors des zones exclues par R5b
- Un `diff` structurel entre `projects/ytp.html` et `en/projects/ytp.html` ne montre que
  du texte : même nombre de sections, mêmes classes, même ordre de blocs
- Le tableau `.ledger` et les `.code-block` sont identiques octet pour octet entre les deux versions
- Les liens externes (`ytp.theogalh.dev`, dépôt GitHub) sont inchangés
- La page reste correcte en dessous de 900 px (les titres français sont plus longs : contrôler
  qu'aucun `stat-value` ni `.section-title` ne déborde)

**Attente de tests : aucune** — contenu éditorial, aucun comportement.

---

### U4. Traduire les 7 pages projet restantes

**Objectif** — `screenator`, `screen`, `theoproject`, `guess`, `bbc`, `theoapi`,
`self-pages` en français, avec le lexique de U3.

**Exigences** — R5, R5b
**Dépendances** — U3

**Fichiers**
- Modifier `projects/{screenator,screen,theoproject,guess,bbc,theoapi,self-pages}.html`

**Approche**
Même traitement que U3, page par page. Les titres de section récurrents viennent de la
table de D4 sans variation. Les titres propres à une page se traduisent au cas par cas —
`A set, from result to rating`, `A round, state by state`, `From drop to link`,
`From empty folder to first deploy`, `A push, from GitHub to nginx`, `A login, step by step`,
`Commands`, `Events on the lobby stream`. Les sections `Commands` de `screenator` et
`theoproject` contiennent des listes de commandes CLI : le titre et la prose se traduisent,
les commandes elles-mêmes relèvent de R5b.

**Vérification**
- Les 8 pages projet racine utilisent exactement les mêmes traductions pour les titres récurrents
- Pour chaque paire, le `diff` structurel ne montre que du texte
- Les zones R5b sont identiques dans chaque paire
- Aucun `<title>`, fil d'ariane ou footer resté en anglais

**Attente de tests : aucune** — contenu éditorial.

---

### U5. Traduire la home

**Objectif** — `index.html` en français : hero, stats, les 8 cartes projet, footer.

**Exigences** — R5
**Dépendances** — U3

**Fichiers**
- Modifier `index.html`

**Approche**
Traduire l'`eyebrow`, le `display`, le `sub`, les libellés `.contact .k`
(`mail` / `github` / `linkedin`), les quatre `stat-label` et `stat-delta`, le titre et
l'introduction de la section Projets, les 8 descriptions de carte, le libellé `Ouvrir →`
et le footer. Les lignes `.stack` des cartes (`fastapi · redis · s3 · …`) sont des listes
de technologies : inchangées.

Les liens des cartes restent relatifs à l'arbre courant (`projects/<slug>.html`), pas de
préfixe de langue.

**Vérification**
- Les 8 cartes de la home française mènent aux pages françaises, celles de `en/index.html` aux pages anglaises
- Les descriptions de carte correspondent au `sub` de la page qu'elles ouvrent
- Le compteur `Projets = 8` correspond au nombre réel de cartes
- Les liens de contact (mailto, GitHub, LinkedIn) sont inchangés

**Attente de tests : aucune** — contenu éditorial.

---

### U6. Écrire le skill de synchronisation

**Objectif** — Un skill projet qui se déclenche à l'édition d'une page du portfolio et
déroule la checklist de R6.

**Exigences** — R6
**Dépendances** — U2 (la checklist décrit la structure posée là)

**Fichiers**
- Créer `.claude/skills/portfolio-page/SKILL.md`

**Approche**
Frontmatter YAML avec `name: portfolio-page` et une `description` qui se déclenche sur
l'édition, l'ajout ou la traduction d'une page du portfolio — pages projet **et**
`index.html` (l'oubli le plus probable est la carte de la home, pas la page elle-même).

Le corps contient trois blocs :

1. **La carte du repo** — les deux arbres, la règle des noms identiques, la table des
   profondeurs relatives vers `assets/`.
2. **La checklist d'édition** — les huit points de R6, formulés comme des vérifications
   actionnables plutôt que des rappels vagues.
3. **Le lexique** — la table de D4, telle que figée en U3, plus la règle R5b (ce qui reste
   en anglais des deux côtés).

Ajouter une section « Ajouter une page projet » qui énumère les fichiers à créer et à
modifier : 2 pages, 2 cartes de home, le numéro d'`eyebrow`, les deux `hreflang`, le
sélecteur des deux côtés.

**Vérification**
- Le frontmatter est valide et le skill apparaît dans la liste des skills disponibles
- Dérouler la checklist à la main sur une modification fictive de `projects/screen.html`
  fait bien remonter la page anglaise correspondante
- Le lexique du skill correspond exactement aux traductions employées dans les 8 pages
- Aucun chemin absolu dans le fichier

**Attente de tests : aucune** — document de procédure.

---

### U7. Mettre à jour le README

**Objectif** — Le README décrit l'arborescence bilingue et renvoie au skill.

**Exigences** — R7
**Dépendances** — U6

**Fichiers**
- Modifier `README.md`

**Approche**
Réécrire la section « Layout » avec les deux arbres et `.claude/skills/`. Réécrire
« Add a project » : la procédure crée désormais deux pages et deux cartes, et renvoie au
skill pour la checklist complète. Ajouter une ligne sur la règle des noms de fichiers
identiques — c'est l'invariant dont tout le reste dépend.

**Vérification**
- L'arborescence du README correspond à `find . -not -path './.git/*' -type f`
- La procédure « Add a project » suivie littéralement produit une page accessible dans les deux langues

**Attente de tests : aucune** — documentation.

---

## Périmètre exclu

### Non-objectifs

- Traduction par dictionnaire JSON au runtime
- Retour à un générateur ou une étape de build (`dea7cf9` a tranché en sens inverse)
- Détection automatique de langue ou redirection serveur
- URLs sans extension `.html`
- Traduction du design system externe (hors de ce repo)

### Reporté

- **Une troisième langue.** L'arborescence la supporte (`/es/`), rien n'est fait pour.
- **Un vérificateur de liens automatisé.** Un script qui parcourt les 18 pages et
  compare la structure des paires remplacerait une partie de la checklist manuelle.
  Utile si la dérive se produit malgré le skill ; prématuré avant.
- **Retirer `docs/` du périmètre servi.** Voir Risques.

---

## Risques

| Risque | Traitement |
|--------|-----------|
| Dérive entre les deux arbres à la première édition post-livraison | Le skill (U6) est le garde-fou ; le README (U7) y renvoie |
| Chemins relatifs cassés dans `en/projects/` (deux crans de profondeur) | Vérification explicite en U1, contrôlée par `grep` |
| Le sélecteur avalé par le tiroir mobile | D2 le place hors de `.nav` ; vérifié en U2 |
| Débordement de mise en page (le français est ~15 % plus long) | Contrôle responsive explicite en U3 sur la page pilote, avant de dérouler les 7 autres |
| `docs/` est servi publiquement — le repo *est* le site, donc `docs/plans/` et `docs/brainstorms/` sont accessibles en HTTP | Aucune page n'y renvoie et rien n'y est sensible. Si c'est gênant, les déplacer hors du repo ou les exclure côté service — hors périmètre de ce plan |

---

## Questions différées à l'implémentation

- Le libellé exact du sélecteur (`FR / EN` contre `Français / English`) se tranche en U2, à l'œil, dans la topbar réelle.
- La formulation française de quelques titres propres à une page (`A set, from result to rating`) se fixe en U4, page par page.
