"""Fonctions Streamlit partagées : cache et affichage de la population."""
import streamlit as st
from src.data import charger_reponses, charger_schema
from src.population import Population


@st.cache_data(show_spinner="Chargement des données 2026...")
def reponses_2026():
    return charger_reponses(2026)


@st.cache_data
def schema_2026():
    return charger_schema(2026)


def afficher_population(pop: Population) -> None:
    st.caption(pop.libelle())
