#Tableau de bord principal
import streamlit as st
from interface import reponses_2026, afficher_population
from src.population import filtrer_france, decrire

st.set_page_config(page_title="L'IA chez les développeurs", layout="wide")
st.title("L'IA est-elle devenue indispensable aux développeurs ?")
st.write(
    "Cette étude explore les usages de l'intelligence artificielle "
    "chez les développeurs, leur confiance envers les outils IA "
    "et leur perception de son impact sur leur travail."
)

st.write("**Message pour le commanditaire :** _à rédiger après l'exploration (étape 2)._")

try:
    df = reponses_2026()
except (FileNotFoundError, ValueError) as e:
    st.error(str(e))
    st.stop()

# choix du périmètre d'étude
perimetre = st.radio("Périmètre", ["France", "Tous pays"], key="perimetre", horizontal=True)

#application du périmètre
base = filtrer_france(df) if perimetre == "France" else df
qui = "répondants en France" if perimetre == "France" else "répondants, tous pays"

# Calcul des indicateurs
total_repondants = len(base)
repondants_france = len(filtrer_france(df))
reponses_ia = base["AIUse"].notna().sum()


# Affichage des indicateurs
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Répondants dans le périmètre",
        total_repondants
    )

with col2:
    st.metric(
        "Répondants en France",
        repondants_france
    )

with col3:
    st.metric(
        "Réponses renseignées sur l'usage de l'IA",
        reponses_ia
    )


# Description de la population étudiée
afficher_population(decrire(base, qui))
