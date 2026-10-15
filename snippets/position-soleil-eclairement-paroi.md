---
titre: Position du soleil et éclairement sur une paroi inclinée
description: Hauteur et azimut du soleil pour une date, une heure locale et un lieu, puis éclairement total sur une paroi d'inclinaison et d'orientation quelconques (direct + diffus isotrope + réfléchi par le sol).
mots_cles: [solaire, rayonnement, géométrie solaire, éclairement, façade, toiture, duffie beckman, la réunion, numpy]
langage: python
projet: Mini-projet Analyse numérique AN2 (M2 S3)
date: 2026-10-14
---

## Code

```python
import numpy as np

# Lieu par défaut : Le Tampon / Saint-Pierre (La Réunion), UTC+4
LATITUDE, LONGITUDE, FUSEAU = -21.278, 55.518, 4.0


def position_soleil(jour_annee, heure_locale, lat=LATITUDE, lon=LONGITUDE, fuseau=FUSEAU):
    """Hauteur et azimut du soleil [rad] (formules classiques, Duffie & Beckman).
    Azimut compté depuis le Nord, sens horaire (Est = 90°)."""
    phi = np.radians(lat)
    decl = np.radians(23.45) * np.sin(2 * np.pi * (284 + jour_annee) / 365)   # déclinaison
    B = 2 * np.pi * (jour_annee - 81) / 364
    eq_temps = 9.87 * np.sin(2 * B) - 7.53 * np.cos(B) - 1.5 * np.sin(B)      # [min]
    # temps solaire vrai [h] (méridien de référence du fuseau : 15° x fuseau)
    tsv = heure_locale + (lon - 15 * fuseau) / 15 + eq_temps / 60
    omega = np.radians(15 * (tsv - 12))                                       # angle horaire
    sin_h = np.sin(phi) * np.sin(decl) + np.cos(phi) * np.cos(decl) * np.cos(omega)
    hauteur = np.arcsin(np.clip(sin_h, -1, 1))
    azimut = np.arctan2(-np.cos(decl) * np.sin(omega),
                        np.sin(decl) * np.cos(phi) - np.cos(decl) * np.cos(omega) * np.sin(phi))
    return float(hauteur), float(np.mod(azimut, 2 * np.pi))


def eclairement(hauteur, azimut, Gbn, Gdh, Gh, inclinaison, azimut_paroi,
                albedo=0.2, fraction_soleil=1.0):
    """
    Éclairement solaire total sur une paroi [W/m2] :
    direct + diffus (ciel isotrope) + réfléchi par le sol.

    hauteur, azimut : position du soleil [rad] (sortie de position_soleil)
    Gbn : direct normal, Gdh : diffus horizontal, Gh : global horizontal [W/m2]
    inclinaison : 0° = horizontale (toiture), 90° = verticale (façade)
    azimut_paroi : orientation de la normale [°] depuis le Nord (Nord = 0, Est = 90)
    fraction_soleil : part de la paroi au soleil (1 = pas d'ombre)
    """
    if hauteur <= 0:
        Gbn = 0.0                          # soleil couché : pas de direct
    beta = np.radians(inclinaison)
    cos_i = (np.sin(hauteur) * np.cos(beta)
             + np.cos(hauteur) * np.sin(beta) * np.cos(azimut - np.radians(azimut_paroi)))
    direct = Gbn * max(cos_i, 0.0) * fraction_soleil
    diffus = Gdh * (1 + np.cos(beta)) / 2
    reflechi = albedo * Gh * (1 - np.cos(beta)) / 2
    return direct + diffus + reflechi


# Exemple : 21 décembre (jour 355), midi, façade nord verticale
# h, az = position_soleil(355, 12.0)
# print(np.degrees(h), np.degrees(az))
# print(eclairement(h, az, Gbn=800, Gdh=150, Gh=1000, inclinaison=90, azimut_paroi=0))
```

## Notes

- Dépendance : numpy.
- **Hémisphère sud** : à La Réunion le soleil passe au nord en hiver austral, mais peut passer au sud (azimut ≈ 180°) autour du solstice de décembre. Ne pas supposer « façade nord = façade la plus ensoleillée » toute l'année.
- Précision de l'ordre du degré (déclinaison de Cooper, équation du temps approchée) : suffisant pour la thermique du bâtiment, pas pour du suivi solaire de précision. Pour mieux : `pvlib.solarposition`.
- Diffus isotrope : modèle simple qui sous-estime le diffus sur les façades orientées vers le soleil. Pour mieux : modèle de Perez (`pvlib.irradiance`).
- Dans la version d'origine, ces fonctions lisaient un dictionnaire `c` et un module `parametres` : j'ai mis les grandeurs en arguments pour pouvoir copier-coller la fiche.
