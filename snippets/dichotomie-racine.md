---
titre: Trouver la racine d'une fonction par dichotomie
description: Cherche x tel que f(x) = 0 sur un intervalle [a, b] où f change de signe. Renvoie la racine approchée et le nombre d'itérations.
mots_cles: [analyse numérique, dichotomie, racine, équation non linéaire]
langage: python
projet: Ajout à la création de la banque
date: 2026-10-15
---

## Code

```python
def dichotomie(f, a, b, tol=1e-8, max_iter=200):
    """Racine de f sur [a, b] par dichotomie. f(a) et f(b) doivent être de signes opposés."""
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise ValueError("f(a) et f(b) ont le même signe : pas de racine garantie sur [a, b].")

    for n in range(1, max_iter + 1):
        m = (a + b) / 2
        fm = f(m)
        if fm == 0 or (b - a) / 2 < tol:
            return m, n
        if fa * fm < 0:
            b, fb = m, fm
        else:
            a, fa = m, fm
    raise RuntimeError("Pas de convergence : augmente max_iter ou vérifie f.")


# Exemple : racine de x^3 - 2x - 5 (≈ 2.0946)
# racine, n = dichotomie(lambda x: x**3 - 2*x - 5, 2, 3)
```

## Notes

- Aucune dépendance.
- Convergence lente mais garantie : l'erreur est divisée par 2 à chaque itération, donc environ log2((b - a) / tol) itérations.
- Pour aller plus vite quand on connaît la dérivée : méthode de Newton. En pratique : `scipy.optimize.brentq` fait le même travail, plus vite et de façon robuste.
