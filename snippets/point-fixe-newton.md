---
titre: Résoudre une équation non linéaire - point fixe et Newton-Raphson
description: Deux méthodes itératives. Point fixe pour x = g(x), Newton-Raphson pour f(x) = 0 avec la dérivée. Renvoient la solution et l'historique des écarts pour tracer la convergence.
mots_cles: [analyse numérique, point fixe, newton, racine, équation non linéaire, convergence]
langage: python
projet: Mini-projet Analyse numérique AN2 (M2 S3)
date: 2026-10-13
---

## Code

```python
def point_fixe(g, x0, tol=1e-8, itmax=500):
    """Itère x_{k+1} = g(x_k). Renvoie la solution et la liste des écarts."""
    x = x0
    ecarts = []
    for _ in range(itmax):
        x_new = g(x)
        ecarts.append(abs(x_new - x))
        x = x_new
        if ecarts[-1] < tol:
            break
    return x, ecarts


def newton(f, df, x0, tol=1e-8, itmax=50):
    """Newton-Raphson : x_{k+1} = x_k - f(x_k)/f'(x_k). Renvoie x et les écarts."""
    x = x0
    ecarts = []
    for _ in range(itmax):
        dx = -f(x) / df(x)
        x = x + dx
        ecarts.append(abs(dx))
        if ecarts[-1] < tol:
            break
    return x, ecarts


# Exemple : x = cos(x)  (solution ≈ 0.739085)
# import math
# x1, e1 = point_fixe(math.cos, 1.0)                                  # ~45 itérations
# x2, e2 = newton(lambda x: x - math.cos(x), lambda x: 1 + math.sin(x), 1.0)  # ~4 itérations
# Tracer la convergence : plt.semilogy(e1); plt.semilogy(e2)
```

## Notes

- Aucune dépendance.
- **Pas d'alerte en cas de non-convergence** : si `itmax` est atteint, la fonction renvoie quand même la dernière valeur. Vérifier `ecarts[-1] < tol` après l'appel.
- Point fixe : converge si |g'(x)| < 1 près de la solution (convergence linéaire). Si ça diverge, essayer une relaxation : `g_relax = lambda x: 0.5 * (x + g(x))`.
- Newton : convergence quadratique près de la solution, mais peut diverger si x0 est loin ou si f'(x) ≈ 0.
- Dans le mini-projet : point fixe pour la température de vêtement (PMV), Newton pour linéariser le rayonnement en Ts⁴.
