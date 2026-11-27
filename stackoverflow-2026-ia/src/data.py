from pathlib import Path

import pandas as pd
import streamlit as st


# Chemin racine du projet
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Dossier contenant les données
DATA_DIR = PROJECT_ROOT / "data"

# Chemins des fichiers CSV
SURVEY_FILE = DATA_DIR / "survey_results_public_2026.csv"
SCHEMA_FILE = DATA_DIR / "survey_results_schema_2026.csv"


@st.cache_data
def load_survey_data():
    """Charge les données du sondage Stack Overflow 2026 et le dictionnaire des variables"""

    if not SURVEY_FILE.exists():
        raise FileNotFoundError(
            f"Fichier introuvable : {SURVEY_FILE}"
        )

    if not SCHEMA_FILE.exists():
        raise FileNotFoundError(
            f"Fichier introuvable : {SCHEMA_FILE}"
        )

    survey = pd.read_csv(
        SURVEY_FILE,
        low_memory=False
    )

    schema = pd.read_csv(
        SCHEMA_FILE
    )

    return survey, schema