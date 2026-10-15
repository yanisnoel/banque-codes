---
titre: Courbe médiane de plusieurs essais répétés et statistiques descriptives
description: À partir de plusieurs essais mesurés sur la même grille de temps, calcule la médiane et la moyenne point par point, et les statistiques (moyenne, médiane, écart-type n-1, étendue) d'une grandeur par essai. Trace les essais et la médiane.
mots_cles: [statistiques, médiane, écart-type, répétabilité, essais, expérimental, matplotlib, graphique, mesure]
langage: python
projet: TP Caractérisation multiphysique II - sonde FP2C (M2 S3)
date: 2026-09-06
---

## Code

```python
import statistics as st
import matplotlib.pyplot as plt


def stats(valeurs):
    """Moyenne, médiane, écart-type expérimental (n-1) et étendue d'une liste."""
    return {
        "moyenne": st.mean(valeurs),
        "mediane": st.median(valeurs),
        "ecart_type": st.stdev(valeurs) if len(valeurs) > 1 else 0.0,
        "etendue": max(valeurs) - min(valeurs),
    }


def combiner_essais(essais):
    """
    essais : dict {nom: (t, y)} mesurés sur la MÊME grille de temps.
    Renvoie t, la médiane et la moyenne point par point.
    """
    noms = list(essais)
    t_ref = essais[noms[0]][0]
    for nom in noms[1:]:
        assert essais[nom][0] == t_ref, f"Grille de temps différente pour l'essai {nom}"
    ys = [essais[nom][1] for nom in noms]
    mediane = [st.median(v) for v in zip(*ys)]
    moyenne = [st.mean(v) for v in zip(*ys)]
    return t_ref, mediane, moyenne


def tracer_essais(essais, t, mediane, titre="", chemin=None):
    fig, ax = plt.subplots(figsize=(8, 5))
    for nom, (tt, y) in essais.items():
        ax.plot(tt, y, linewidth=1.4, label=f"Essai {nom}")
    ax.plot(t, mediane, color="black", linestyle="--", linewidth=1.8, label="Médiane point par point")
    ax.set(title=titre, xlabel="Temps t (s)", ylabel="Température T (°C)")
    ax.grid(True, linestyle=":", alpha=0.7)
    ax.legend()
    fig.tight_layout()
    if chemin:
        fig.savefig(chemin, dpi=200)
    return fig


# Exemple (avec la fiche « Lire un export texte d'appareil de mesure ») :
# essais = {e: lire_txt_2colonnes(f"ECH_6_2{e}.txt") for e in "ABC"}
# t, med, moy = combiner_essais(essais)
# dT = [y[-1] - y[0] for _, y in essais.values()]   # élévation de température par essai
# print(stats(dT))
# tracer_essais(essais, t, med, "Échantillon 6.2", "ech_6_2.png")
```

## Notes

- Dépendance : matplotlib (les statistiques n'utilisent que la bibliothèque standard).
- Avec 3 essais, l'écart-type est très incertain : présenter aussi l'étendue, et ne pas parler de « distribution ».
- La médiane point par point n'est pas une mesure réelle : c'est une courbe représentative, utile pour lisser un essai aberrant. Le dire dans le rapport.
- Si les grilles de temps diffèrent, l'`assert` arrête le script : il faut d'abord rééchantillonner (`numpy.interp`).
