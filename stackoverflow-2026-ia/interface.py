#Fonctions Streamlit partagées cache et affichage de la population
import streamlit as st
from src.data import load_survey_data
from src.population import Population


@st.cache_data(show_spinner="Chargement des données 2026...")
def reponses_2026():
    survey, schema = load_survey_data()
    return survey


@st.cache_data
def schema_2026():
    survey, schema = load_survey_data()
    return schema


def afficher_population(pop: Population) -> None:
    st.caption(pop.libelle())