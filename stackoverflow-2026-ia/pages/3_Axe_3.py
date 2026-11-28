"""Axe 3 — Confiance dans l'IA. Responsable : Ayoub."""
import sys
from pathlib import Path

import plotly.express as px
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src import data, population  # noqa: E402
from src.axes import axe_3  # noqa: E402

st.set_page_config(page_title="Axe 3 · Confiance", page_icon="🛡️", layout="wide")
st.title("Axe 3 · Confiance dans l'IA")
st.caption("Quelle opinion les développeurs ont de l'IA, leur font-ils confiance, et pour quelles tâches ?")


@st.cache_data(show_spinner="Chargement de l'enquête…")
def charger():
    return data.charger_reponses(2026)


try:
    brut = charger()
except (FileNotFoundError, ValueError) as erreur:
    st.error(str(erreur))
    st.stop()

france = st.sidebar.toggle("France seulement")
df = population.filtrer_france(brut) if france else brut
zone = "France" if france else "Monde"

question = st.radio("Question", list(axe_3.QUESTIONS), format_func=axe_3.QUESTIONS.get, horizontal=True)

st.subheader(axe_3.QUESTIONS[question])
table, n = axe_3.distribution(df, question)
if n == 0:
    st.info("Aucun répondant pour cette sélection.")
    st.stop()

fig = px.bar(table, x="pct", y="modalité", orientation="h",
             text=table["pct"].map(lambda v: f"{v:.0f} %"))
fig.update_yaxes(categoryorder="array", categoryarray=table["modalité"][::-1].tolist(), title="")
fig.update_xaxes(title="% des répondants", ticksuffix=" %")
fig.update_traces(textposition="outside", cliponaxis=False)
st.plotly_chart(fig, key="axe2_distribution")

utiles = df[axe_3.recoder(df[question], question).notna()]
pop = population.decrire(utiles, f"Répondants ({zone})", 2026, question)
st.caption("👥 " + pop.libelle())
with st.expander("Voir les données"):
    st.dataframe(table, hide_index=True)

st.subheader("Solde de confiance")
conf, mefi, n_conf = axe_3.part_confiance(df)
col1, col2 = st.columns(2)
col1.metric("Font confiance", f"{conf:.0f} %")
col2.metric("Se méfient", f"{mefi:.0f} %")
st.caption(f"Solde = % qui font confiance − % qui se méfient. n = {n_conf} répondants ayant répondu à « "
           f"{axe_3.QUESTIONS['AIAcc']} ».")

GROUPES = {"RemoteWork": "Mode de travail", "OrgSize": "Taille de l'organisation", "Age": "Âge"}
groupe = st.selectbox("Croiser avec", list(GROUPES), format_func=GROUPES.get)
solde = axe_3.solde_par_groupe(df, groupe)
if solde.empty:
    st.info("Aucun groupe n'atteint 30 répondants.")
else:
    fig2 = px.bar(solde, x="solde", y="groupe", orientation="h",
                  text=solde["solde"].map(lambda v: f"{v:+.0f}"))
    fig2.update_yaxes(categoryorder="total ascending", title="")
    fig2.update_xaxes(title="Solde (points de %)", zeroline=True)
    fig2.update_traces(textposition="outside", cliponaxis=False)
    st.plotly_chart(fig2, key="axe2_solde")
    st.caption(f"👥 Répondants ({zone}) · Enquête 2026 · groupes de 30 répondants ou plus, "
               "les autres sont masqués. " + population.MENTION_VOLONTAIRES)
    with st.expander("Voir les données"):
        st.dataframe(solde, hide_index=True)
