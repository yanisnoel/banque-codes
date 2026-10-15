---
titre: Calculer le PMV et le PPD (Fanger, NF EN ISO 7730)
description: Indices de confort thermique PMV et PPD à partir de la température d'air, de la température radiante, de la vitesse d'air, de l'humidité, du métabolisme et de la vêture. Inclut la pression de vapeur saturante (Magnus).
mots_cles: [confort thermique, pmv, ppd, fanger, iso 7730, humidité, point fixe, numpy]
langage: python
projet: Mini-projet Analyse numérique AN2 (M2 S3)
date: 2026-10-13
---

## Code

```python
import numpy as np


def p_sat(T):
    """Pression de vapeur saturante [Pa], T en °C (formule de Magnus)."""
    return 610.94 * np.exp(17.625 * T / (T + 243.04))


def pmv_ppd(ta, tr, va, pa, met, clo):
    """
    ta : température d'air [°C]          tr : température moyenne radiante [°C]
    va : vitesse d'air [m/s]             pa : pression partielle de vapeur [Pa]
    met : métabolisme [met]              clo : isolement vestimentaire [clo]
    Renvoie (PMV, PPD [%]).
    """
    M = met * 58.15                       # [W/m2], travail mécanique nul
    Icl = 0.155 * clo                     # [m2K/W]
    fcl = 1.0 + 1.29 * Icl if Icl <= 0.078 else 1.05 + 0.645 * Icl
    hc_forcee = 12.1 * np.sqrt(va)
    taK, trK = ta + 273.0, tr + 273.0

    # --- point fixe sur t_cl (en K/100, comme dans la norme) ---
    x = (taK + (35.5 - ta) / (3.5 * Icl + 0.1)) / 100      # estimation initiale
    for _ in range(150):
        hc = max(hc_forcee, 2.38 * abs(100 * x - taK) ** 0.25)
        x_new = (308.7 - 0.028 * M + Icl * fcl * 3.96 * (trK / 100) ** 4
                 + Icl * fcl * hc * taK - Icl * fcl * 3.96 * x ** 4) / (100 + Icl * fcl * 100 * hc)
        x_new = 0.5 * (x + x_new)                           # relaxation
        if abs(x_new - x) < 1.5e-5:
            x = x_new
            break
        x = x_new
    tcl = 100 * x - 273.0

    # --- bilan thermique du corps [W/m2] ---
    pertes = (3.05e-3 * (5733 - 6.99 * M - pa)              # diffusion de vapeur par la peau
              + (0.42 * (M - 58.15) if M > 58.15 else 0.0)   # transpiration
              + 1.7e-5 * M * (5867 - pa)                     # respiration latente
              + 0.0014 * M * (34 - ta)                       # respiration sensible
              + 3.96 * fcl * (x ** 4 - (trK / 100) ** 4)     # rayonnement
              + fcl * hc * (tcl - ta))                       # convection
    pmv = (0.303 * np.exp(-0.036 * M) + 0.028) * (M - pertes)
    ppd = 100 - 95 * np.exp(-0.03353 * pmv ** 4 - 0.2179 * pmv ** 2)
    return pmv, ppd


# Contrôle avec le tableau D.1 de la norme ISO 7730 :
# ta = tr = 22 °C, va = 0,1 m/s, HR = 60 %, 1,2 met, 0,5 clo -> PMV = -0,75
# print(pmv_ppd(22, 22, 0.1, 0.6 * p_sat(22), 1.2, 0.5))
```

## Notes

- Dépendance : numpy.
- Entrée humidité : la **pression partielle** pa, pas l'HR. Conversion : `pa = HR * p_sat(ta)` avec HR entre 0 et 1.
- Domaine de validité ISO 7730 : PMV entre -2 et +2, ta 10-30 °C, va 0-1 m/s, 0,8-4 met, 0-2 clo. En climat tropical ventilé naturellement, le PMV surestime souvent l'inconfort : comparer avec le modèle adaptatif (ASHRAE 55 / EN 16798-1).
- Fonction scalaire (boucle + `if`) : pour une série temporelle, l'appeler ligne par ligne ou utiliser `pythermalcomfort` (vectorisé, plusieurs normes).
