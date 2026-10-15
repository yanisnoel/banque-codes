---
titre: Lire une année météo type PVGIS (JSON) et choisir une journée type
description: Charge le fichier JSON TMY téléchargé sur PVGIS en DataFrame horaire en heure locale, choisit pour un mois la journée la plus proche du jour moyen (température, amplitude, irradiation), puis en extrait les 24 valeurs horaires.
mots_cles: [météo, pvgis, tmy, année type, journée type, json, pandas, climat, la réunion]
langage: python
projet: Mini-projet Analyse numérique AN2 (M2 S3)
date: 2026-10-14
---

## Code

```python
import json
import pandas as pd


def lire_tmy(chemin, fuseau=4.0):
    """Lit le fichier JSON PVGIS et renvoie un DataFrame horaire en heure locale.
    fuseau : décalage horaire en heures (La Réunion = UTC+4)."""
    with open(chemin) as f:
        donnees = json.load(f)
    df = pd.DataFrame(donnees["outputs"]["tmy_hourly"])
    utc = pd.to_datetime(df["time(UTC)"], format="%Y%m%d:%H%M")
    local = utc + pd.Timedelta(hours=fuseau)
    df = df.rename(columns={"T2m": "Te", "RH": "HR", "G(h)": "Gh", "Gb(n)": "Gbn",
                            "Gd(h)": "Gdh", "IR(h)": "IR", "WS10m": "vent"})
    df["mois"] = local.dt.month
    df["jour"] = local.dt.day
    df["heure"] = local.dt.hour
    return df


def journee_type(df, mois):
    """
    Jour du mois le plus proche du « jour moyen » du mois, au sens de trois
    critères : température moyenne, amplitude de température et irradiation
    journalière (écarts réduits par l'écart-type, puis somme des carrés).
    """
    m = df[df["mois"] == mois]
    g = m.groupby("jour").agg(Tm=("Te", "mean"), Tmin=("Te", "min"),
                              Tmax=("Te", "max"), H=("Gh", "sum"))
    g["amplitude"] = g["Tmax"] - g["Tmin"]
    g = g[["Tm", "amplitude", "H"]]
    z = (g - g.mean()) / g.std()
    return int((z ** 2).sum(axis=1).idxmin())


def extraire_journee(df, jour, mois):
    """24 valeurs horaires (0 h à 23 h, heure locale) d'une journée."""
    j = df[(df["mois"] == mois) & (df["jour"] == jour)].sort_values("heure")
    clim = {c: j[c].to_numpy(dtype=float) for c in ("Te", "HR", "Gh", "Gbn", "Gdh", "IR", "vent")}
    clim["jour_annee"] = pd.Timestamp(2021, mois, jour).dayofyear
    clim["date"] = f"{jour:02d}/{mois:02d}"
    return clim


# Exemple
# df = lire_tmy("tmy_-21.278_55.518_2005_2023.json")
# j = journee_type(df, mois=2)          # journée type de février
# clim = extraire_journee(df, j, 2)
# print(clim["date"], clim["Te"].max())
```

## Notes

- Dépendance : pandas.
- Fichier d'entrée : PVGIS → onglet « TMY » → format **json**. Les colonnes renommées sont : Te [°C], HR [%], Gh / Gbn / Gdh [W/m2], IR [W/m2], vent [m/s] à 10 m.
- Une TMY assemble des mois réels issus d'années différentes : elle représente un climat moyen, **pas les extrêmes**. Pour du confort d'été ou une étude de surchauffe, prendre aussi une journée chaude (par ex. le jour au Tmax maximal).
- Le passage UTC → heure locale peut faire glisser les premières heures du 1er janvier sur le 31 décembre : sans conséquence pour une journée type, à surveiller pour une simulation annuelle.
- `journee_type` ne garde que 3 critères, au même poids. L'humidité et le vent ne sont pas pris en compte.
