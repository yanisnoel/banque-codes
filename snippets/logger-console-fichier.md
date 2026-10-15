---
titre: Journal d'exécution affiché à l'écran et écrit dans un fichier
description: Petite classe Logger qui horodate chaque message, l'affiche en console et l'ajoute à un fichier log, avec des niveaux INFO, WARN, ERROR, OK. Pratique pour les longs calculs lancés la nuit.
mots_cles: [log, journal, automatisation, script, simulation, suivi, fichier texte]
langage: python
projet: Mémoire M1 - orchestrateur des simulations EnergyPlus
date: 2026-06-14
---

## Code

```python
from datetime import datetime
from pathlib import Path


class Logger:
    """Logger qui écrit en console ET dans un fichier."""
    def __init__(self, log_path):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.f = open(self.log_path, "a", encoding="utf-8")

    def log(self, msg, level="INFO"):
        ts = datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}] [{level}] {msg}"
        print(line)
        self.f.write(line + "\n")
        self.f.flush()                    # écrit tout de suite : rien de perdu en cas de crash

    def info(self, msg):  self.log(msg, "INFO")
    def warn(self, msg):  self.log(msg, "WARN")
    def error(self, msg): self.log(msg, "ERROR")
    def ok(self, msg):    self.log(msg, "OK  ")
    def sep(self):        self.log("=" * 70, "----")
    def close(self):      self.f.close()


# Exemple
# ts = datetime.now().strftime("%Y%m%d_%H%M%S")
# log = Logger(f"logs/RUN_LOG_{ts}.txt")
# log.info("Début des simulations")
# log.ok("Campagne baseline terminée")
# log.close()
```

## Notes

- Aucune dépendance.
- Alternative standard : le module `logging` de Python (plus complet : niveaux filtrables, rotation des fichiers). Cette classe est plus simple à lire et suffit pour un script de calcul.
- Le fichier est ouvert en mode `"a"` (ajout) : relancer le script ajoute à la suite au lieu d'écraser. Mettre un horodatage dans le nom pour un fichier par exécution.
