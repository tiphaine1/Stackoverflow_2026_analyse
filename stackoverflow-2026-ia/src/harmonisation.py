
import pandas as pd


def nettoyer_donnees(df, colonne):
    # Suppression des réponses manquantes et des cellules vides
    serie = df[colonne].dropna()
    serie = serie.astype(str).str.strip()
    serie = serie[serie != ""]

    return serie


def calculer_effectifs(df, colonne):
    # Comptage des réponses par catégorie
    serie = nettoyer_donnees(df, colonne)

    return serie.value_counts()


def calculer_pourcentages(df, colonne):
    # Calcul des pourcentages par catégorie
    effectifs = calculer_effectifs(df, colonne)

    total = effectifs.sum()

    if total == 0:
        return effectifs.astype(float)

    pourcentages = (effectifs / total) * 100

    return pourcentages.round(2)


def preparer_donnees_categorielle(df, colonne):
    # Préparation des effectifs et pourcentages pour les graphiques
    effectifs = calculer_effectifs(df, colonne)
    pourcentages = calculer_pourcentages(df, colonne)

    resultat = pd.DataFrame({
        "Categorie": effectifs.index,
        "Effectif": effectifs.values,
        "Pourcentage": pourcentages.values
    })

    return resultat.reset_index(drop=True)

