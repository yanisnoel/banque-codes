# Banque de codes

Mes codes réutilisables (Python et autres), issus de mes études et projets.
Chaque fiche contient un titre, une description, le code prêt à copier et une section de notes.

**Site avec recherche : https://yanisnoel.github.io/banque-codes/**

## Ajouter une fiche

1. Copier `snippets/_modele.md` dans `snippets/` sous un nom parlant, par ex. `pandas-moyenne-glissante.md`
   (minuscules, tirets, sans espace ni accent).
2. Remplir l'en-tête (titre, description, mots-clés, langage, projet, date), coller le code sous `## Code`.
3. Commit + push. Le site et le catalogue ci-dessous se mettent à jour tout seuls en 1 à 2 minutes.

Depuis le téléphone : sur github.com, dossier `snippets/` → **Add file → Create new file**, puis coller le modèle.

Pour vérifier en local avant de pousser : `python outils/build.py`, puis ouvrir `site/index.html`.

## Catalogue

<!-- CATALOGUE:DEBUT -->

**15 fiche(s)**

| Titre | Langage | Mots-clés | Projet |
|---|---|---|---|
| [Calculer le PMV et le PPD (Fanger, NF EN ISO 7730)](snippets/pmv-ppd-iso7730.md) | python | confort thermique, pmv, ppd, fanger, iso 7730, humidité, point fixe, numpy | Mini-projet Analyse numérique AN2 (M2 S3) |
| [Courbe médiane de plusieurs essais répétés et statistiques descriptives](snippets/mediane-essais-repetes-stats.md) | python | statistiques, médiane, écart-type, répétabilité, essais, expérimental, matplotlib, graphique, mesure | TP Caractérisation multiphysique II - sonde FP2C (M2 S3) |
| [Enchaîner des scripts Python en série avec timeout et reprise après crash](snippets/lancer-scripts-serie-reprise.md) | python | automatisation, subprocess, batch, simulation, energyplus, reprise, timeout, json, orchestrateur | Mémoire M1 - orchestrateur des simulations EnergyPlus |
| [Fraction ensoleillée d'une fenêtre protégée par un débord](snippets/ombrage-debord-baie.md) | python | solaire, ombrage, protection solaire, débord, casquette, baie, fenêtre, rtaa dom, numpy | Mini-projet Analyse numérique AN2 (M2 S3) |
| [Journal d'exécution affiché à l'écran et écrit dans un fichier](snippets/logger-console-fichier.md) | python | log, journal, automatisation, script, simulation, suivi, fichier texte | Mémoire M1 - orchestrateur des simulations EnergyPlus |
| [Lire un CSV de sortie EnergyPlus avec de vraies dates](snippets/energyplus-lire-csv-sortie.md) | python | energyplus, pandas, csv, datetime, série temporelle, simulation | Ajout à la création de la banque |
| [Lire un export texte d'appareil de mesure (virgule décimale, latin-1)](snippets/lire-txt-virgule-decimale.md) | python | lecture fichier, txt, csv, virgule décimale, encodage, latin-1, acquisition, mesure, sonde, expérimental | TP Caractérisation multiphysique II - sonde FP2C (M2 S3) |
| [Lire une année météo type PVGIS (JSON) et choisir une journée type](snippets/pvgis-tmy-journee-type.md) | python | météo, pvgis, tmy, année type, journée type, json, pandas, climat, la réunion | Mini-projet Analyse numérique AN2 (M2 S3) |
| [Mailler une paroi multicouche en volumes finis 1D (et calculer son U)](snippets/paroi-multicouche-volumes-finis.md) | python | volumes finis, conduction, paroi, multicouche, maillage, résistance thermique, coefficient u, thermique du bâtiment, numpy | Mini-projet Analyse numérique AN2 (M2 S3) |
| [Position du soleil et éclairement sur une paroi inclinée](snippets/position-soleil-eclairement-paroi.md) | python | solaire, rayonnement, géométrie solaire, éclairement, façade, toiture, duffie beckman, la réunion, numpy | Mini-projet Analyse numérique AN2 (M2 S3) |
| [Résoudre un système tri-diagonal (algorithme de Thomas, TDMA)](snippets/tdma-thomas-tridiagonal.md) | python | analyse numérique, tdma, thomas, système linéaire, tri-diagonal, volumes finis, conduction, numpy | Mini-projet Analyse numérique AN2 (M2 S3) |
| [Résoudre une équation non linéaire - point fixe et Newton-Raphson](snippets/point-fixe-newton.md) | python | analyse numérique, point fixe, newton, racine, équation non linéaire, convergence | Mini-projet Analyse numérique AN2 (M2 S3) |
| [Température de ciel et température radiante extérieure (GLO)](snippets/temperature-ciel-rayonnement-glo.md) | python | rayonnement, glo, grande longueur d'onde, température de ciel, infrarouge, stefan-boltzmann, toiture, numpy | Mini-projet Analyse numérique AN2 (M2 S3) |
| [Trouver la racine d'une fonction par dichotomie](snippets/dichotomie-racine.md) | python | analyse numérique, dichotomie, racine, équation non linéaire | Ajout à la création de la banque |
| [Vérifier que les CSV de sortie EnergyPlus ne sont pas tronqués](snippets/energyplus-verifier-csv-tronque.md) | python | energyplus, simulation, contrôle qualité, csv, batch, vérification, automatisation | Mémoire M1 - orchestrateur des simulations EnergyPlus |

<!-- CATALOGUE:FIN -->
