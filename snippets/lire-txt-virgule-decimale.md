---
titre: Lire un export texte d'appareil de mesure (virgule décimale, latin-1)
description: Lit un fichier texte à deux colonnes (temps, valeur) exporté par un logiciel d'acquisition français - virgule comme séparateur décimal, encodage latin-1, en-têtes et lignes parasites ignorés. Renvoie deux listes.
mots_cles: [lecture fichier, txt, csv, virgule décimale, encodage, latin-1, acquisition, mesure, sonde, expérimental]
langage: python
projet: TP Caractérisation multiphysique II - sonde FP2C (M2 S3)
date: 2026-09-06
---

## Code

```python
def lire_txt_2colonnes(chemin, encodage="latin-1"):
    """Lit un fichier texte à deux colonnes (t, valeur) séparées par une
    tabulation ou des espaces, avec la virgule comme séparateur décimal.
    Les lignes vides, les en-têtes et les lignes non numériques sont ignorées.
    Renvoie deux listes (t, valeurs)."""
    t_vals, y_vals = [], []
    with open(chemin, "r", encoding=encodage) as f:
        for ligne in f:
            ligne = ligne.strip()
            if not ligne:
                continue
            parts = ligne.replace(",", ".").split("\t")
            if len(parts) < 2:
                parts = ligne.replace(",", ".").split()
            if len(parts) < 2:
                continue
            try:
                t_vals.append(float(parts[0]))
                y_vals.append(float(parts[1]))
            except ValueError:
                continue                     # en-tête ou ligne parasite
    return t_vals, y_vals


# Exemple
# t, T = lire_txt_2colonnes("ECH_6_2A.txt")
# print(len(t), t[0], T[0])

# Équivalent pandas (plus court, mais moins tolérant aux lignes parasites) :
# import pandas as pd
# df = pd.read_csv("ECH_6_2A.txt", sep="\t", decimal=",", encoding="latin-1")
```

## Notes

- Aucune dépendance.
- **Piège** : `replace(",", ".")` est fait sur toute la ligne. Si le fichier utilise la virgule comme séparateur de colonnes (et non la tabulation), les colonnes fusionnent. Vérifier le fichier dans un éditeur avant.
- Les lignes ignorées le sont **en silence**. Pour un fichier inconnu, compter les lignes lues et comparer au nombre de lignes du fichier.
- `latin-1` ne plante jamais (chaque octet est un caractère valide) : si les accents de l'en-tête sont bizarres, essayer `cp1252` ou `utf-8`.
- Origine : lecture des fichiers de la sonde à choc thermique FP2C (conductivité de la fibre de coco).
