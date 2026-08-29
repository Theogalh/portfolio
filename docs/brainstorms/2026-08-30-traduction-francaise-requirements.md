# Traduction française du portfolio — requirements

**Date** : 2026-08-30
**Statut** : prêt pour planification

## Problème

Le site est intégralement en anglais. Le public principal (recruteurs, contacts FR)
n'a aucune version française, et rien ne permet de partager un lien « en français ».

## Ce qu'on construit

Une version française **canonique à la racine**, l'anglais déplacé sous `/en/`,
avec une arborescence strictement miroir. Un skill projet impose la checklist de
synchronisation à chaque édition d'une page, pour que les deux versions ne dérivent pas.

Contrainte structurante : le repo *est* le site. Pas d'étape de build, pas de CI,
pages éditables à la main. Le commit `dea7cf9` a supprimé `build.py` délibérément —
toute solution qui réintroduit une génération est hors périmètre.

## Arborescence cible

```
index.html                  FR — home
projects/<slug>.html        FR — 8 pages projet
en/index.html               EN — home
en/projects/<slug>.html     EN — 8 pages projet
assets/                     inchangé, partagé par les deux arbres
.claude/skills/<nom>/SKILL.md   checklist de mise à jour
```

Les 9 pages actuelles sont **déplacées** dans `en/`, pas copiées : leurs chemins
relatifs vers `assets/` gagnent un cran (`assets/` → `../assets/` pour `en/index.html`,
`../assets/` → `../../assets/` pour `en/projects/*.html`).

## Exigences

### R1 — Noms de fichiers identiques des deux côtés
Un slug FR n'existe pas. `projects/ytp.html` et `en/projects/ytp.html`.
La contrepartie d'une page se déduit du chemin, ce qui rend le sélecteur trivial
et la checklist vérifiable d'un coup d'œil.

### R2 — Sélecteur de langue dans la topbar
Une paire `FR / EN` à côté de la nav ; la langue courante est inerte, l'autre est un
lien **en dur** vers la page contrepartie. Pas de JS, pas de `localStorage`, pas de
détection navigateur, pas de redirection — le serveur sert les fichiers tels quels.

### R3 — Métadonnées de langue correctes
Chaque page porte le bon `lang` sur `<html>` (`fr` à la racine, `en` sous `/en/`) et
deux `<link rel="alternate" hreflang="fr|en" href="...">` croisés.

### R4 — Chaînes d'interface de `assets/site.js`
Les trois libellés produits en JS (`Copy`, `Copied`, `Close`) sont choisis selon
`document.documentElement.lang`, via un petit dictionnaire à deux entrées en tête de
fichier. Aucun autre fichier de `assets/` n'a de contenu textuel.

### R5 — Contenu traduit
Titres de page, fil d'ariane, eyebrow, `display`, `sub`, titres de section, prose des
`.feature`, `.flow .step`, `.decisions`, les 8 cartes projet de `index.html`, le hero
et les stats, et le footer.

### R5b — Les blocs techniques restent en anglais
Les descriptions d'endpoints dans les tableaux `.ledger`, les labels `.meta-label` et le
contenu des `.code-block` ne sont pas traduits : ils sont identiques mot pour mot dans les
deux arbres. C'est le registre attendu par le lecteur de ces sections, et ça retire une
grande part de la surface de dérive. Seuls les titres de section qui les encadrent
(`Stack`, `API`, `Deploy & ops`…) sont traduits.

### R6 — Skill projet de synchronisation
Un skill dans `.claude/skills/` qui se déclenche à l'édition d'une page du portfolio et
déroule la checklist :

- [ ] La modification est appliquée aux **deux** versions de la page
- [ ] Le lien du sélecteur de langue pointe bien vers la contrepartie existante
- [ ] Les deux `hreflang` sont présents et croisés correctement
- [ ] Le fil d'ariane et le `<title>` sont dans la bonne langue
- [ ] Le footer est dans la bonne langue
- [ ] Si c'est une nouvelle page : la carte est ajoutée à `index.html` **et** `en/index.html`
- [ ] Les chemins relatifs vers `assets/` correspondent à la profondeur du fichier
- [ ] Les blocs techniques restent en anglais et identiques des deux côtés (voir R5b)

### R7 — README à jour
La section « Layout » et la procédure « Add a project » décrivent l'arborescence à deux
langues et renvoient au skill.

## Périmètre exclu

- **Dictionnaire JSON traduit au runtime** — tue le HTML éditable à la main et rend le
  français invisible pour l'indexation.
- **Retour à un générateur / build step** — décision déjà prise en sens inverse (`dea7cf9`).
- **Détection automatique de langue / redirection** — mauvais pour le crawl, pénible pour
  montrer l'anglais volontairement.
- **Une troisième langue** — l'architecture la supporte (`/es/`), mais rien n'est fait pour.
- **Traduction du design system externe** (`theogalh.github.io/design-system/styles.css`) —
  hors de ce repo.

## Critères de succès

1. `theogalh.dev/projects/ytp.html` répond en français, `theogalh.dev/en/projects/ytp.html`
   en anglais, et chacune renvoie vers l'autre en un clic.
2. Aucun lien interne cassé dans les deux arbres, aucun `assets/` en 404.
3. Une édition de page faite via le skill met à jour les deux versions sans oubli.
4. Le repo se sert toujours tel quel : `python3 -m http.server 8080` suffit à tout tester.

## Hypothèses

- Les URLs gardent leur extension `.html` et restent servies en statique pur. La config
  de service (self-pages / nginx) est hors de ce repo, donc non vérifiée ici, mais aucune
  exigence ci-dessus n'en dépend.
- Personne ne dépend d'une URL anglaise à la racine au point qu'il faille une redirection
  depuis les anciennes adresses.
