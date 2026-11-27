# Architecture technique (à compléter au fil du projet)

## Fonctionnalités principales
| Fonctionnalité | Fichiers | Fonctions |
|---|---|---|
| Téléchargement des données | scripts/download_data.py | main |
| Chargement | src/data.py | charger_reponses, charger_schema |
| Population et libellé | src/population.py | filtrer_france, decrire, Population.libelle |
| Cache Streamlit | interface.py | reponses_2026, schema_2026 |
| Tableau de bord principal | app.py | |
| Axes 1 à 5 | src/axes/axe_N.py (logique), pages/N_Axe_N.py (vues) | |

## Circulation des données
`data/*.csv` → `src/data.py` → `interface.py` (@st.cache_data) → filtrage `src/population.py` → `src/axes/axe_N.py` → `pages/` → figure + libellé de population.

## Cache et session
- **@st.cache_data** : chargement des CSV (interface.py).
- **st.session_state** : périmètre (France / tous pays), filtres des axes (clés préfixées par axe).

## Séparation analyse / interface
`src/` n'importe jamais Streamlit. Seuls `app.py`, `pages/` et `interface.py` l'utilisent.

## Harmonisation 2025 (optionnel)
Voir `src/harmonisation.py`.
