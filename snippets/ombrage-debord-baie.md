---
titre: Fraction ensoleillée d'une fenêtre protégée par un débord
description: Calcule la part d'une baie au soleil quand un débord horizontal (casquette, avancée de toiture) la protège, à partir de la position du soleil et de l'angle de profil.
mots_cles: [solaire, ombrage, protection solaire, débord, casquette, baie, fenêtre, rtaa dom, numpy]
langage: python
projet: Mini-projet Analyse numérique AN2 (M2 S3)
date: 2026-10-14
---

## Code

```python
import numpy as np


def fraction_ensoleillee(hauteur, azimut, azimut_paroi, H, debord, ecart=0.2):
    """
    Fraction ensoleillée (0 à 1) d'une baie de hauteur H [m] protégée par un
    débord horizontal de profondeur 'debord' [m] placé 'ecart' [m] au-dessus.

    hauteur, azimut : position du soleil [rad], azimut depuis le Nord (Est = 90°)
    azimut_paroi    : orientation de la normale à la façade [°]
    Hauteur de l'ombre portée = debord * tan(angle de profil) - ecart.
    """
    if debord == 0.0 or hauteur <= 0:
        return 1.0
    cos_az = np.cos(azimut - np.radians(azimut_paroi))
    if cos_az <= 1e-6:                  # soleil derrière la façade : pas de direct
        return 1.0
    tan_profil = np.tan(hauteur) / cos_az
    ombre = min(max(debord * tan_profil - ecart, 0.0), H)
    return 1.0 - ombre / H


# Exemple : soleil à 60° de hauteur plein face, baie de 1,2 m, débord de 0,8 m
# print(fraction_ensoleillee(np.radians(60), np.radians(0), 0, H=1.2, debord=0.8))
```

## Notes

- Dépendance : numpy. Se combine avec la fiche « Position du soleil et éclairement sur une paroi inclinée » (argument `fraction_soleil`).
- Renvoie 1 quand le soleil est derrière la façade : il n'y a pas de direct, mais ce n'est pas de l'ombre. C'est `eclairement()` qui met alors le direct à zéro via cos(i) < 0.
- Hypothèses : débord infiniment large (pas d'effet de bord latéral), pas d'ombre de joues verticales. Pour des débords courts ou des brise-soleil verticaux, il faut un calcul 2D.
- Le « dimensionnement » des protections solaires de la RTAA DOM utilise des tables de facteur solaire, pas ce calcul horaire : ne pas confondre.
