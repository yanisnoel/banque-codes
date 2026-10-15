---
titre: Résoudre un système tri-diagonal (algorithme de Thomas, TDMA)
description: Résout A x = d quand A est tri-diagonale, en O(n) au lieu de O(n³). Cas typique - conduction 1D en volumes finis ou différences finies. Accepte plusieurs seconds membres d'un coup.
mots_cles: [analyse numérique, tdma, thomas, système linéaire, tri-diagonal, volumes finis, conduction, numpy]
langage: python
projet: Mini-projet Analyse numérique AN2 (M2 S3)
date: 2026-10-13
---

## Code

```python
import numpy as np


def tdma(a, b, c, d):
    """
    Résout A x = d avec A tri-diagonale (algorithme de Thomas).

    a : sous-diagonale (a[0] ignoré)
    b : diagonale
    c : sur-diagonale (c[-1] ignoré)
    d : second membre, vecteur (n) ou tableau (n, k) pour résoudre k
        systèmes qui ont la même matrice en une seule fois
    """
    n = len(b)
    cp = np.zeros(n)
    dp = np.array(d, dtype=float)
    # descente : élimination de la sous-diagonale
    cp[0] = c[0] / b[0]
    dp[0] = dp[0] / b[0]
    for i in range(1, n):
        m = b[i] - a[i] * cp[i - 1]
        if i < n - 1:
            cp[i] = c[i] / m
        dp[i] = (dp[i] - a[i] * dp[i - 1]) / m
    # remontée
    x = dp
    for i in range(n - 2, -1, -1):
        x[i] = x[i] - cp[i] * x[i + 1]
    return x


# Exemple et vérification contre numpy :
# n = 5
# a, b, c = np.full(n, -1.0), np.full(n, 4.0), np.full(n, -1.0)
# d = np.arange(1.0, n + 1)
# A = np.diag(b) + np.diag(a[1:], -1) + np.diag(c[:-1], 1)
# print(np.allclose(tdma(a, b, c, d), np.linalg.solve(A, d)))   # True
```

## Notes

- Dépendance : numpy.
- Les trois vecteurs a, b, c ont tous la longueur n : a[0] et c[-1] ne servent pas.
- Stable sans pivotage si la matrice est à diagonale dominante (|b_i| ≥ |a_i| + |c_i|), ce qui est le cas pour la conduction implicite. Sinon, utiliser `scipy.linalg.solve_banded`.
- Seconds membres multiples : passer d de forme (n, k). La matrice n'est factorisée qu'une fois, x sort en (n, k).
- Utilisé dans le mini-projet pour la paroi multicouche (voir la fiche « Mailler une paroi multicouche en volumes finis »).
