"""Chargement des données brutes. Aucune dépendance à Streamlit."""
from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
FICHIERS = {
    2026: {
        "reponses": DATA_DIR / "survey_results_public_2026.csv",
        "schema": DATA_DIR / "survey_results_schema_2026.csv",
    },
}


def _verifier(chemin: Path) -> None:
    if not chemin.exists():
        raise FileNotFoundError(
            f"{chemin.name} introuvable. Lancez : python scripts/download_data.py"
        )
    if chemin.stat().st_size < 10_000:
        raise ValueError(f"{chemin.name} semble être un pointeur Git LFS, pas les données.")


def charger_reponses(annee: int = 2026) -> pd.DataFrame:
    chemin = FICHIERS[annee]["reponses"]
    _verifier(chemin)
    return pd.read_csv(chemin, low_memory=False)


def charger_schema(annee: int = 2026) -> pd.DataFrame:
    chemin = FICHIERS[annee]["schema"]
    _verifier(chemin)
    return pd.read_csv(chemin)
