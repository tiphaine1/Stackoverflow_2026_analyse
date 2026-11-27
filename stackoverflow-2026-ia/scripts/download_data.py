"""Télécharge les données Stack Overflow dans data/ (jamais versionnées)."""
from pathlib import Path
import urllib.request

BASE = "https://media.githubusercontent.com/media/StackExchange/Survey/main/packages/archive"
FICHIERS = {
    "2026/survey_results_public.csv": "survey_results_public_2026.csv",
    "2026/survey_results_schema.csv": "survey_results_schema_2026.csv",
    # Option 2025 : décommenter après avoir écrit l'harmonisation
    # "2025/results.csv": "results_2025.csv",
    # "2025/schema.csv": "schema_2025.csv",
}


def main():
    dossier = Path(__file__).resolve().parent.parent / "data"
    dossier.mkdir(exist_ok=True)
    for chemin, nom in FICHIERS.items():
        cible = dossier / nom
        if cible.exists() and cible.stat().st_size > 10_000:
            print(f"Déjà présent : {nom}")
            continue
        print(f"Téléchargement de {nom} ...")
        urllib.request.urlretrieve(f"{BASE}/{chemin}", cible)
        taille = cible.stat().st_size
        if taille < 10_000:
            raise SystemExit(f"{nom} fait {taille} octets : pointeur Git LFS ? Vérifiez l'URL.")
        print(f"  OK ({taille / 1e6:.1f} Mo)")


if __name__ == "__main__":
    main()
