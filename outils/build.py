"""Construit la banque de codes.

Lit chaque fiche de snippets/*.md (sauf celles qui commencent par "_")
et produit :
  - site/index.html : la page avec barre de recherche (publiée sur GitHub Pages)
  - README.md       : le catalogue lisible directement sur github.com

Utilisation (depuis la racine du dépôt) :
    python outils/build.py

Aucune dépendance : uniquement la bibliothèque standard Python.
"""

import json
import os
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
DOSSIER_FICHES = RACINE / "snippets"
GABARIT = RACINE / "outils" / "template.html"
SORTIE = RACINE / "site" / "index.html"
README = RACINE / "README.md"

CHAMPS_OBLIGATOIRES = ["titre", "description", "mots_cles", "langage"]
DEBUT_CATALOGUE = "<!-- CATALOGUE:DEBUT -->"
FIN_CATALOGUE = "<!-- CATALOGUE:FIN -->"


def lire_entete(texte, nom):
    """Sépare l'en-tête (entre les deux '---') du corps de la fiche."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", texte, re.S)
    if not m:
        raise ValueError(f"{nom} : l'en-tête entre '---' est absent ou mal fermé.")
    entete, corps = m.groups()

    infos = {}
    for ligne in entete.splitlines():
        if not ligne.strip() or ligne.strip().startswith("#"):
            continue
        if ":" not in ligne:
            raise ValueError(f"{nom} : ligne d'en-tête illisible : {ligne!r}")
        cle, valeur = ligne.split(":", 1)
        cle, valeur = cle.strip(), valeur.strip()
        if valeur.startswith("[") and valeur.endswith("]"):
            valeur = [v.strip() for v in valeur[1:-1].split(",") if v.strip()]
        infos[cle] = valeur
    return infos, corps


def lire_sections(corps):
    """Découpe le corps en sections '## Titre' -> texte."""
    sections = {}
    titre = None
    for ligne in corps.splitlines(keepends=True):
        m = re.match(r"^##\s+(.+?)\s*$", ligne)
        if m:
            titre = m.group(1).strip().lower()
            sections[titre] = ""
        elif titre:
            sections[titre] += ligne
    return sections


def lire_fiche(chemin):
    nom = chemin.name
    infos, corps = lire_entete(chemin.read_text(encoding="utf-8"), nom)

    manquants = [c for c in CHAMPS_OBLIGATOIRES if not infos.get(c)]
    if manquants:
        raise ValueError(f"{nom} : champ(s) manquant(s) dans l'en-tête : {', '.join(manquants)}")
    if isinstance(infos["mots_cles"], str):
        infos["mots_cles"] = [infos["mots_cles"]]

    sections = lire_sections(corps)
    bloc = re.search(r"```[^\n]*\n(.*?)```", sections.get("code", ""), re.S)
    if not bloc:
        raise ValueError(f"{nom} : pas de bloc de code ``` sous '## Code'.")

    return {
        "fichier": nom,
        "titre": infos["titre"],
        "description": infos["description"],
        "mots_cles": infos["mots_cles"],
        "langage": infos["langage"].lower(),
        "projet": infos.get("projet", ""),
        "date": infos.get("date", ""),
        "code": bloc.group(1).rstrip("\n"),
        "notes": sections.get("notes", "").strip(),
    }


def ecrire_site(fiches, depot):
    donnees = json.dumps({"fiches": fiches, "depot": depot}, ensure_ascii=False)
    donnees = donnees.replace("</", "<\\/")  # empêche de fermer la balise <script> par accident
    html = GABARIT.read_text(encoding="utf-8").replace("/*__DONNEES__*/null", donnees)
    SORTIE.parent.mkdir(exist_ok=True)
    SORTIE.write_text(html, encoding="utf-8")


def ecrire_catalogue(fiches):
    lignes = [DEBUT_CATALOGUE, "", f"**{len(fiches)} fiche(s)**", "",
              "| Titre | Langage | Mots-clés | Projet |", "|---|---|---|---|"]
    for f in sorted(fiches, key=lambda f: f["titre"].lower()):
        cles = ", ".join(f["mots_cles"]).replace("|", "/")
        titre = f["titre"].replace("|", "/")
        lignes.append(f"| [{titre}](snippets/{f['fichier']}) | {f['langage']} | {cles} | {f['projet']} |")
    lignes += ["", FIN_CATALOGUE]
    bloc = "\n".join(lignes)

    texte = README.read_text(encoding="utf-8")
    if DEBUT_CATALOGUE not in texte or FIN_CATALOGUE not in texte:
        raise ValueError("README.md : les marqueurs du catalogue ont été supprimés.")
    avant = texte.split(DEBUT_CATALOGUE)[0]
    apres = texte.split(FIN_CATALOGUE)[1]
    README.write_text(avant + bloc + apres, encoding="utf-8")


def main():
    chemins = sorted(p for p in DOSSIER_FICHES.glob("*.md") if not p.name.startswith("_"))
    fiches, erreurs = [], []
    for chemin in chemins:
        try:
            fiches.append(lire_fiche(chemin))
        except ValueError as e:
            erreurs.append(str(e))

    if erreurs:
        print("Erreurs à corriger :", *erreurs, sep="\n  - ")
        sys.exit(1)

    # Sur GitHub Actions, GITHUB_REPOSITORY vaut "utilisateur/depot" : sert aux liens "Modifier".
    depot = os.environ.get("GITHUB_REPOSITORY", "")
    ecrire_site(fiches, depot)
    ecrire_catalogue(fiches)
    print(f"OK : {len(fiches)} fiche(s) -> {SORTIE.relative_to(RACINE)} et README.md")


if __name__ == "__main__":
    main()
