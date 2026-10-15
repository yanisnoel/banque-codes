---
titre: Mailler une paroi multicouche en volumes finis 1D (et calculer son U)
description: Découpe une paroi multicouche en volumes de contrôle, calcule les positions des nœuds, les capacités thermiques et les conductances entre nœuds (demi-volumes en série aux interfaces), ainsi que la résistance R et le coefficient U.
mots_cles: [volumes finis, conduction, paroi, multicouche, maillage, résistance thermique, coefficient u, thermique du bâtiment, numpy]
langage: python
projet: Mini-projet Analyse numérique AN2 (M2 S3)
date: 2026-10-13
---

## Code

```python
import numpy as np


def mailler_paroi(couches, dx_max=0.02):
    """
    couches : liste de dict {lam [W/m/K], rho [kg/m3], c [J/kg/K], e [m]},
              de l'intérieur vers l'extérieur.

    Nœuds : [0] surface int. (sans masse), (1..N) centres des CV, [N+1] surface ext.
    Renvoie un dict :
      dx (N)   : épaisseurs des CV [m]
      x  (N+2) : positions des nœuds depuis la face intérieure [m]
      C  (N+2) : capacités surfaciques [J/m2/K] (0 aux surfaces)
      G  (N+1) : conductances entre nœuds voisins [W/m2/K]
    """
    dx, lam, rhoc = [], [], []
    for c in couches:
        n = int(np.ceil(c["e"] / dx_max - 1e-9))          # au moins 1 CV par couche
        dx += [c["e"] / n] * n
        lam += [c["lam"]] * n
        rhoc += [c["rho"] * c["c"]] * n
    dx, lam = np.array(dx), np.array(lam)
    N = len(dx)
    x_faces = np.concatenate(([0.0], np.cumsum(dx)))
    x = np.concatenate(([0.0], (x_faces[:-1] + x_faces[1:]) / 2, [x_faces[-1]]))
    C = np.concatenate(([0.0], np.array(rhoc) * dx, [0.0]))
    r = dx / (2 * lam)                                     # résistance d'un demi-CV
    G = np.zeros(N + 1)
    G[0] = 1 / r[0]                                        # = 2 lam / dx
    G[1:-1] = 1 / (r[:-1] + r[1:])                         # = lam / dx si même matériau
    G[-1] = 1 / r[-1]
    return {"dx": dx, "x": x, "C": C, "G": G, "N": N}


def resistance(couches):
    """Résistance thermique des couches [m2K/W]."""
    return sum(c["e"] / c["lam"] for c in couches)


def coefficient_U(couches, h_int=7.7, h_ext=25.0):
    """Coefficient de transmission surfacique U [W/m2/K] (Rsi = 1/h_int, Rse = 1/h_ext)."""
    return 1 / (1 / h_int + resistance(couches) + 1 / h_ext)


# Exemple : bloc béton 20 cm + isolant 4 cm (intérieur -> extérieur)
# mur = [{"lam": 1.75, "rho": 2300, "c": 1000, "e": 0.20},
#        {"lam": 0.035, "rho": 30, "c": 1450, "e": 0.04}]
# m = mailler_paroi(mur)
# print(m["N"], coefficient_U(mur))
# Contrôle : sum(1 / m["G"]) doit valoir resistance(mur).
```

## Notes

- Dépendance : numpy.
- Vérification intégrée : les conductances sont en série, donc `sum(1 / G)` = R des couches. Si ce n'est pas le cas, le maillage est faux.
- Pour avancer dans le temps : schéma theta sur les CV (C/dt (Tⁿ⁺¹ - Tⁿ) = θ Fⁿ⁺¹ + (1-θ) Fⁿ) ; les nœuds de surface, sans masse, portent les bilans de flux (convection, solaire, GLO). Le système est tri-diagonal : voir la fiche TDMA. L'assemblage complet (avec couplage à l'air intérieur) est dans `paroi.py` du mini-projet.
- `dx_max` = 2 cm par défaut. Contrôle de convergence : diviser dx_max par 2 et vérifier que les températures bougent peu.
- Valeurs h par défaut : Rsi = 0,13 m2K/W (paroi verticale, flux horizontal) et Rse = 0,04 m2K/W, conventions de la NF EN ISO 6946. À changer pour une toiture.
