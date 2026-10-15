---
titre: Température de ciel et température radiante extérieure (GLO)
description: Température de ciel équivalente à partir de l'éclairement infrarouge IR(h), puis température radiante vue par une paroi selon son inclinaison (ciel + sol), pour les échanges en grandes longueurs d'onde.
mots_cles: [rayonnement, glo, grande longueur d'onde, température de ciel, infrarouge, stefan-boltzmann, toiture, numpy]
langage: python
projet: Mini-projet Analyse numérique AN2 (M2 S3)
date: 2026-10-14
---

## Code

```python
import numpy as np

SIGMA = 5.67e-8     # constante de Stefan-Boltzmann [W/m2/K4]
TK = 273.15         # conversion °C -> K


def temperature_ciel(IR):
    """Température de ciel équivalente [°C] à partir de l'éclairement IR(h) mesuré [W/m2]."""
    return (IR / SIGMA) ** 0.25 - TK


def temperature_rayonnante_ext(IR, Te, inclinaison):
    """
    Température radiante vue par une paroi [°C] : ciel (facteur de forme
    (1 + cos beta)/2) et sol supposé à la température de l'air Te pour le reste.
    On moyenne les éclairements (en T^4) puis on revient à une température.
    inclinaison : 0° = toiture horizontale, 90° = façade verticale.
    """
    F_ciel = (1 + np.cos(np.radians(inclinaison))) / 2
    E = F_ciel * IR + (1 - F_ciel) * SIGMA * (Te + TK) ** 4
    return (E / SIGMA) ** 0.25 - TK


# Exemple : nuit claire, IR = 350 W/m2, Te = 20 °C
# print(temperature_ciel(350))                          # ≈ 7 °C
# print(temperature_rayonnante_ext(350, 20, 0))         # toiture : voit tout le ciel
# print(temperature_rayonnante_ext(350, 20, 90))        # façade : moitié ciel, moitié sol
```

## Notes

- Dépendance : numpy. IR(h) est fourni par PVGIS (colonne `IR(h)`) et par les fichiers EPW (« Horizontal Infrared Radiation Intensity »).
- Le flux GLO échangé par la paroi vaut ensuite `eps * SIGMA * ((Tr + TK)**4 - (Ts + TK)**4)`, avec eps ≈ 0,9 pour la plupart des matériaux de construction.
- Hypothèse forte : sol à la température de l'air. En journée, un sol ensoleillé est nettement plus chaud, donc la façade reçoit plus de GLO que ce modèle ne le prévoit.
- Une toiture voit tout le ciel : c'est elle qui rayonne le plus la nuit. C'est l'effet recherché par les cool roofs et le refroidissement radiatif.
