"""Définition de la population et libellé « qui / année / combien »."""
from dataclasses import dataclass
import pandas as pd

# À VÉRIFIER dans survey_results_schema_2026.csv
COLONNE_PAYS = "Country"
VALEUR_FRANCE = "France"

MENTION_VOLONTAIRES = (
    "Répondants volontaires à une enquête en ligne : "
    "résultats non représentatifs de l'ensemble des développeurs."
)


@dataclass(frozen=True)
class Population:
    qui: str
    annee: int
    n: int

    def libelle(self) -> str:
        return f"Population : {self.qui} · Enquête {self.annee} · {self.n} répondants. {MENTION_VOLONTAIRES}"


def filtrer_france(df: pd.DataFrame) -> pd.DataFrame:
    return df[df[COLONNE_PAYS] == VALEUR_FRANCE]


def decrire(df: pd.DataFrame, qui: str, annee: int = 2026, colonne: str | None = None) -> Population:
    """Décrit la population réelle d'une figure.
    Si `colonne` est donnée, ne compte que les répondants ayant répondu à cette question."""
    n = int(df[colonne].notna().sum()) if colonne else len(df)
    return Population(qui=qui, annee=annee, n=n)
