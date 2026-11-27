"""Tableau de bord principal."""
import streamlit as st
from interface import reponses_2026, afficher_population
from src.population import filtrer_france, decrire

st.set_page_config(page_title="L'IA chez les développeurs", layout="wide")
st.title("L'IA est-elle devenue indispensable aux développeurs ?")
st.write("**Message pour le commanditaire :** _à rédiger après l'exploration (étape 2)._")

try:
    df = reponses_2026()
except (FileNotFoundError, ValueError) as e:
    st.error(str(e))
    st.stop()

# Filtre conservé dans st.session_state
perimetre = st.radio("Périmètre", ["France", "Tous pays"], key="perimetre", horizontal=True)
base = filtrer_france(df) if perimetre == "France" else df
qui = "répondants en France" if perimetre == "France" else "répondants, tous pays"

st.metric("Répondants dans le périmètre", len(base))
afficher_population(decrire(base, qui))
