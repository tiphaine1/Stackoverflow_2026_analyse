"""Première exploration : colonnes liées à l'IA et effectif France.
Usage : python scripts/explorer_schema.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.data import charger_reponses, charger_schema
from src.population import COLONNE_PAYS, VALEUR_FRANCE

MOTS_CLES = ["AI", "LLM", "agent", "assistant", "copilot", "trust", "Trust"]


def main():
    schema = charger_schema()
    print("Colonnes du schéma :", list(schema.columns))
    texte = schema.astype(str).agg(" ".join, axis=1)
    masque = texte.str.contains("|".join(MOTS_CLES), regex=True)
    print(f"\n{masque.sum()} lignes du schéma mentionnent l'IA :\n")
    print(schema[masque].to_string(max_colwidth=100))

    df = charger_reponses()
    print(f"\nTotal répondants : {len(df)}")
    if COLONNE_PAYS in df.columns:
        print(f"Répondants France : {(df[COLONNE_PAYS] == VALEUR_FRANCE).sum()}")
    else:
        print(f"Colonne pays '{COLONNE_PAYS}' absente. Colonnes : {list(df.columns)[:30]}")


if __name__ == "__main__":
    main()
