"""Axe 3 — Confiance dans l'IA : opinion, confiance dans les réponses, tâches complexes.

Logique pure (pandas), sans Streamlit. Travaille sur les colonnes BRUTES de l'enquête 2026
(celles que renvoie src/data.py). Colonnes à vérifier dans survey_results_schema_2026.csv :
AIAcc, AISent, AIComplex.
"""
from __future__ import annotations

import re

import numpy as np
import pandas as pd

QUESTIONS = {
    "AIAcc": "Confiance dans les réponses de l'IA",
    "AISent": "Opinion sur l'IA",
    "AIComplex": "IA et tâches complexes",
}

# Règles de recodage : motif (minuscules, regex) -> modalité en français. L'ordre compte : la première règle qui correspond gagne.
RECODAGE: dict[str, list[tuple[str, str]]] = {
    "AIAcc": [
        (r"highly trust", "Très confiant"),
        (r"somewhat trust", "Plutôt confiant"),
        (r"neither", "Ni confiance ni méfiance"),
        (r"somewhat distrust", "Plutôt méfiant"),
        (r"highly distrust", "Très méfiant"),
    ],
    "AISent": [
        (r"very unfavorable", "Très défavorable"),
        (r"unfavorable", "Défavorable"),
        (r"very favorable", "Très favorable"),
        (r"favorable", "Favorable"),
        (r"indifferent", "Indifférent"),
        (r"unsure|not sure", "Ne sait pas"),
    ],
    "AIComplex": [
        (r"don'?t use|don'?t know", "Pas d'usage / ne sait pas"),
        (r"neither", "Ni bien ni mal"),
        (r"very poor", "Très mal"),
        (r"bad|poor", "Mal"),
        (r"very well", "Très bien"),
        (r"good", "Bien"),
    ],
}

ORDRE: dict[str, list[str]] = {
    "AIAcc": ["Très confiant", "Plutôt confiant", "Ni confiance ni méfiance", "Plutôt méfiant", "Très méfiant"],
    "AISent": ["Très favorable", "Favorable", "Indifférent", "Ne sait pas", "Défavorable", "Très défavorable"],
    "AIComplex": ["Très bien", "Bien", "Ni bien ni mal", "Mal", "Très mal", "Pas d'usage / ne sait pas"],
}

CONFIANCE = {"Très confiant", "Plutôt confiant"}
MEFIANCE = {"Très méfiant", "Plutôt méfiant"}


def recoder(serie: pd.Series, colonne: str) -> pd.Series:
    """Réponses brutes -> modalités en français ; NaN si aucune règle ne correspond."""
    regles = RECODAGE[colonne]

    def une_valeur(valeur):
        if pd.isna(valeur):
            return np.nan
        texte = str(valeur).strip().lower()
        for motif, libelle in regles:
            if re.search(motif, texte):
                return libelle
        return np.nan

    return serie.map(une_valeur)


def distribution(df: pd.DataFrame, colonne: str) -> tuple[pd.DataFrame, int]:
    """Parts par modalité (sur les répondants ayant répondu) et effectif correspondant."""
    recodees = recoder(df[colonne], colonne).dropna()
    n = len(recodees)
    compte = recodees.value_counts().reindex(ORDRE[colonne], fill_value=0)
    table = pd.DataFrame({"modalité": compte.index, "n": compte.values})
    table["pct"] = 100 * table["n"] / n if n else 0.0
    return table, n


def part_confiance(df: pd.DataFrame) -> tuple[float, float, int]:
    """(% qui font confiance, % qui se méfient, effectif) sur la question de confiance."""
    recodees = recoder(df["AIAcc"], "AIAcc").dropna()
    n = len(recodees)
    if n == 0:
        return np.nan, np.nan, 0
    return (100 * recodees.isin(CONFIANCE).mean(), 100 * recodees.isin(MEFIANCE).mean(), n)


def solde_par_groupe(df: pd.DataFrame, groupe: str, min_n: int = 30) -> pd.DataFrame:
    """Solde de confiance (% confiants − % méfiants) par groupe, groupes de moins de min_n écartés."""
    d = pd.DataFrame({"h": recoder(df["AIAcc"], "AIAcc"), "groupe": df[groupe]}).dropna()
    lignes = []
    for nom, sous in d.groupby("groupe", observed=True):
        if len(sous) < min_n:
            continue
        confiants = 100 * sous["h"].isin(CONFIANCE).mean()
        mefiants = 100 * sous["h"].isin(MEFIANCE).mean()
        lignes.append({"groupe": str(nom), "n_groupe": len(sous),
                       "% confiants": confiants, "% méfiants": mefiants, "solde": confiants - mefiants})
    return pd.DataFrame(lignes, columns=["groupe", "n_groupe", "% confiants", "% méfiants", "solde"]) \
        .sort_values("solde", ascending=False).reset_index(drop=True)
