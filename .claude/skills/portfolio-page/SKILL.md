---
name: portfolio-page
description: Checklist à dérouler dès qu'une page du portfolio theogalh.dev est éditée, ajoutée ou traduite — pages projet sous projects/ et en/projects/, ainsi que les deux index.html. Le site est bilingue avec deux arbres miroirs : toute modification doit être appliquée des deux côtés. Utilise ce skill avant de toucher à index.html, en/index.html, projects/*.html ou en/projects/*.html.
---

# Éditer une page du portfolio

Le repo **est** le site : pas de build, pas de CI, pages éditables à la main. Le contenu
existe en deux exemplaires, un par langue. Le seul vrai risque de ce dépôt est la
**dérive** : une page mise à jour d'un côté et pas de l'autre.

## Carte du repo

```
index.html                    FR — accueil (canonique)
projects/<slug>.html          FR — 8 pages projet
en/index.html                 EN — accueil
en/projects/<slug>.html       EN — 8 pages projet
assets/site.css               styles propres au site, dont .langsw
assets/site.js                tiroir mobile + copie, chaînes UI bilingues
```

**Invariant** : les noms de fichiers sont identiques dans les deux arbres. La contrepartie
d'une page se déduit de son chemin. Ne francise jamais un slug.

Profondeur des chemins vers `assets/` :

| Fichier | Préfixe |
|---------|---------|
| `index.html` | `assets/` |
| `projects/*.html` | `../assets/` |
| `en/index.html` | `../assets/` |
| `en/projects/*.html` | `../../assets/` |

## Checklist — modifier une page existante

- [ ] La modification est appliquée aux **deux** versions de la page
- [ ] Le lien du sélecteur `.langsw` pointe vers une contrepartie qui existe vraiment
- [ ] Les deux `<link rel="alternate" hreflang>` sont présents et croisés correctement
- [ ] Le `<title>` et le fil d'ariane sont dans la langue de la page
- [ ] Le footer est dans la langue de la page (`sombre par défaut` / `dark by default`)
- [ ] Les chemins vers `assets/` correspondent à la profondeur du fichier (voir la table)
- [ ] Les zones non traduites sont restées **identiques mot pour mot** entre les deux versions
- [ ] Si le texte d'une carte projet a changé, `index.html` **et** `en/index.html` sont à jour

## Ce qui n'est pas traduit

Ces zones sont en anglais des deux côtés et doivent rester identiques octet pour octet :

- le `<tbody>` des tableaux `.ledger` (descriptions d'endpoints, de commandes, d'événements)
- les `.meta-label` et `.meta-value` des blocs Stack et Déploiement & ops
- le contenu des `.code-block`, commentaires compris
- les lignes `.stack` des cartes de la home (listes de technologies)

Seuls les titres de section et les en-têtes de tableau qui encadrent ces zones sont traduits.

## Lexique

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
| API | API *(inchangé)* |
| Commands | Commandes |
| Run it | Le lancer |
| Deploy & ops | Déploiement & ops |
| how it is built | sous le capot |
| `· project ·` | `· projet ·` |
| dark by default | sombre par défaut |
| Method / Path / Description | Méthode / Chemin / Description |
| Copy / Copied / Close | Copier / Copié / Fermer |

Les trois dernières vivent dans le dictionnaire `UI` en tête de `assets/site.js` ; la langue
est lue une fois via `document.documentElement.lang`, avec repli sur l'anglais.

## Ajouter une page projet

1. Copier une paire existante : `projects/<slug>.html` et `en/projects/<slug>.html`.
2. Corriger dans chacune : `<html lang>`, `<title>`, fil d'ariane, numéro d'`eyebrow`,
   contenu, footer.
3. Poser les deux `hreflang` croisés dans chaque `<head>`.
4. Poser le `.langsw` dans chaque topbar, hors de `.nav` — `assets/site.js` construit le
   tiroir mobile à partir de `.nav a`, un lien de langue placé là s'y retrouverait avalé.
   La contrepartie est `../en/projects/<slug>.html` côté FR, `../../projects/<slug>.html`
   côté EN.
5. Ajouter la carte dans `index.html` **et** dans `en/index.html`.
6. Mettre à jour le compteur `Projets` / `Projects` des stats de la home, des deux côtés.
7. Vérifier localement : `python3 -m http.server 8080`, puis dérouler la checklist ci-dessus.
