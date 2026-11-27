from dataclasses import dataclass
import pandas as pd


# Variables pour décrire la population
POPULATION_VARIABLES = [
    "Age",
    "Country",
    "Employment",
    "Education",
    "YearsCode",
    "WorkExp",
    "Role",
    "WorkSetting",
    "Industry"
]

# Informations sur l'enquête
ANNEE_ENQUETE = 2026
COLONNE_PAYS = "Country"
VALEUR_FRANCE = "France"

MENTION_VOLONTAIRES = (
    "Répondants volontaires à une enquête en ligne "
    "résultats non représentatifs de l'ensemble des développeurs"
)


@dataclass(frozen=True)
class Population:
    qui: str
    annee: int
    n: int

    def libelle(self) -> str:
        return (
            f"Population : {self.qui} · "
            f"Enquête {self.annee} · "
            f"{self.n} répondants. "
            f"{MENTION_VOLONTAIRES}"
        )


def get_population_summary(df):
    # Informations générales sur la population étudiée
    summary = {
        "total_respondents": len(df),
        "variables": POPULATION_VARIABLES
    }

    return summary


def get_filter_options(df, column):
    # Valeurs disponibles pour un filtre
    values = df[column].fillna("Non renseigné")

    return sorted(values.unique().tolist(), key=str)


def apply_population_filters(df, filters):
    # Application des filtres sélectionnés
    filtered_df = df.copy()

    for column, selected_values in filters.items():

        if selected_values:

            values = filtered_df[column].fillna("Non renseigné")

            filtered_df = filtered_df[
                values.isin(selected_values)
            ]

    return filtered_df


def get_valid_responses(df, column):
    # Nombre de réponses renseignées pour une variable
    return int(df[column].notna().sum())


def filtrer_france(df):
    # Sélection des répondants ayant indiqué la France
    return df[df[COLONNE_PAYS] == VALEUR_FRANCE]


def decrire(df, qui, annee=ANNEE_ENQUETE, colonne=None):
    # Description de la population utilisée pour une figure
    if colonne:
        n = int(df[colonne].notna().sum())
    else:
        n = len(df)

    return Population(
        qui=qui,
        annee=annee,
        n=n
    )