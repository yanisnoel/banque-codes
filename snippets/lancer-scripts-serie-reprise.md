---
titre: Enchaîner des scripts Python en série avec timeout et reprise après crash
description: Lance une liste de scripts les uns après les autres via subprocess, avec une limite de temps par script, et enregistre dans un fichier JSON ceux déjà terminés pour pouvoir reprendre là où ça s'est arrêté.
mots_cles: [automatisation, subprocess, batch, simulation, energyplus, reprise, timeout, json, orchestrateur]
langage: python
projet: Mémoire M1 - orchestrateur des simulations EnergyPlus
date: 2026-06-14
---

## Code

```python
import json
import subprocess
import sys
import time
from pathlib import Path


def lancer_script(script, dossier=".", timeout_min=180):
    """Lance un script Python avec le même interpréteur. Renvoie (succès, message)."""
    script = Path(dossier) / script
    if not script.exists():
        return False, f"Script introuvable : {script}"
    t0 = time.time()
    try:
        res = subprocess.run([sys.executable, str(script)], cwd=str(dossier),
                             capture_output=True, text=True, timeout=timeout_min * 60,
                             encoding="utf-8", errors="replace")
    except subprocess.TimeoutExpired:
        return False, f"Timeout ({timeout_min} min)"
    if res.returncode != 0:
        return False, f"Code retour {res.returncode} : {res.stderr[-500:]}"
    return True, f"OK en {(time.time() - t0) / 60:.1f} min"


def charger_etat(chemin):
    chemin = Path(chemin)
    if chemin.exists():
        return json.loads(chemin.read_text(encoding="utf-8"))
    return {"faits": []}


def sauver_etat(chemin, etat):
    Path(chemin).write_text(json.dumps(etat, indent=2), encoding="utf-8")


def lancer_tout(scripts, dossier=".", etat_json="RUN_STATE.json", essais=2):
    """Lance chaque script non encore fait ; réessaie une fois en cas d'échec."""
    etat = charger_etat(etat_json)
    for script in scripts:
        if script in etat["faits"]:
            print(f"[saute] {script} déjà fait")
            continue
        for essai in range(1, essais + 1):
            ok, msg = lancer_script(script, dossier)
            print(f"[{'OK' if ok else 'ECHEC'}] {script} (essai {essai}) : {msg}")
            if ok:
                etat["faits"].append(script)
                sauver_etat(etat_json, etat)      # sauvegarde après CHAQUE script
                break
    return etat


# Exemple
# lancer_tout(["baseline.py", "protection_solaire.py", "cool_roof.py"], dossier="04_simulations")
# Après un crash, relancer la même commande : les scripts déjà faits sont sautés.
# Pour tout refaire : supprimer RUN_STATE.json.
```

## Notes

- Aucune dépendance.
- `sys.executable` garantit que chaque script tourne avec le même Python (même environnement conda) que l'orchestrateur.
- `capture_output=True` garde la sortie en mémoire : pour des scripts très bavards, rediriger vers un fichier à la place.
- Un code retour 0 ne prouve pas que les résultats sont bons : vérifier aussi les fichiers produits (voir la fiche « Vérifier qu'un CSV EnergyPlus n'est pas tronqué »).
- Version d'origine (mémoire M1) plus complète : patch de l'IDF, archivage des anciens résultats, rapport final des écarts par KPI.
