---
titre: Lire un CSV de sortie EnergyPlus avec de vraies dates
description: Charge le fichier eplusout.csv dans un DataFrame pandas et convertit la colonne Date/Time d'EnergyPlus (format " 01/01  01:00:00", avec 24:00:00 en fin de journée) en index datetime exploitable.
mots_cles: [energyplus, pandas, csv, datetime, série temporelle, simulation]
langage: python
projet: Ajout à la création de la banque
date: 2026-10-15
---

## Code

```python
import pandas as pd


def lire_sortie_energyplus(chemin_csv, annee=2026):
    """Lit un CSV de sortie EnergyPlus et renvoie un DataFrame indexé par date.

    EnergyPlus écrit les dates sans année et note minuit "24:00:00"
    (fin du jour J), ce que pandas ne sait pas lire directement.
    """
    df = pd.read_csv(chemin_csv)
    brut = df["Date/Time"].str.strip()            # " 01/01  24:00:00" -> "01/01  24:00:00"
    jour = brut.str.split().str[0]                 # "01/01"
    heure = brut.str.split().str[1]                # "24:00:00"

    minuit = heure == "24:00:00"
    heure = heure.where(~minuit, "00:00:00")       # 24:00 -> 00:00 ...
    dates = pd.to_datetime(f"{annee}/" + jour + " " + heure, format="%Y/%m/%d %H:%M:%S")
    dates = dates.where(~minuit, dates + pd.Timedelta(days=1))  # ... du jour suivant

    df.index = dates
    df.index.name = "date"
    return df.drop(columns="Date/Time")


# Exemple d'utilisation
# df = lire_sortie_energyplus("eplusout.csv")
# df.filter(like="Zone Mean Air Temperature").resample("D").max().plot()
```

## Notes

- Dépendances : pandas.
- Fonctionne pour des sorties horaires ou au pas de temps (Timestep). Pour une sortie "RunPeriod" ou "Monthly", le format de date est différent : à adapter.
- L'année est arbitraire (EnergyPlus ne l'écrit pas). Choisis-en une non bissextile si ton fichier météo n'a pas de 29 février.
- Vérification rapide : `df.index.is_monotonic_increasing` doit valoir True et `len(df)` doit faire 8760 pour une année horaire.
