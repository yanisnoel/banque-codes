---
titre: Vérifier que les CSV de sortie EnergyPlus ne sont pas tronqués
description: Parcourt un dossier de résultats, compte les lignes de chaque eplusout.csv et sépare les simulations complètes (année horaire ≈ 8760 lignes) des runs incomplets ou plantés.
mots_cles: [energyplus, simulation, contrôle qualité, csv, batch, vérification, automatisation]
langage: python
projet: Mémoire M1 - orchestrateur des simulations EnergyPlus
date: 2026-06-14
---

## Code

```python
from pathlib import Path


def verifier_runs(dossier, seuil_lignes=8700, motif="**/eplusout.csv"):
    """
    Compte les lignes de chaque CSV de sortie EnergyPlus trouvé dans 'dossier'.
    Renvoie (liste des CSV valides, liste des CSV suspects avec leur nombre de lignes).
    seuil_lignes : 8700 pour une année au pas horaire (8760 lignes + en-tête).
    """
    valides, suspects = [], []
    for csv in sorted(Path(dossier).glob(motif)):
        try:
            with open(csv, "r", encoding="utf-8", errors="replace") as f:
                n = sum(1 for _ in f)
        except OSError:
            n = 0
        (valides if n > seuil_lignes else suspects).append((csv, n))
    return valides, suspects


# Exemple
# valides, suspects = verifier_runs("results/baseline_naturel", seuil_lignes=8700)
# print(f"{len(valides)} runs complets, {len(suspects)} à relancer")
# for csv, n in suspects:
#     print(f"  {csv.parent.name} : {n} lignes")
```

## Notes

- Aucune dépendance.
- Adapter le seuil au pas de temps : horaire 8760, pas de 15 min 35 040, journalier 365. Avec plusieurs RunPeriod ou des jours de dimensionnement en sortie, le nombre de lignes change aussi.
- Un CSV complet ne prouve pas une simulation correcte : lire aussi `eplusout.err` (rechercher `** Severe` et `** Fatal`).
- Origine : des runs du mémoire écrivaient parfois un CSV coupé ; ce contrôle déclenchait une relance automatique.
