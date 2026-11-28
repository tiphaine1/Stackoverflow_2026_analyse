# L'IA chez les développeurs : enquête Stack Overflow 2026

**Problématique :** l'IA est-elle devenue un outil indispensable aux développeurs, ou suscite-t-elle encore de la méfiance ?
**Commanditaire :** _à définir_

Les répondants sont des volontaires à une enquête en ligne : les résultats ne représentent pas tous les développeurs.

## Lancer l'application
```bash
python -m venv .venv && source .venv/bin/activate   # Windows : .venv\Scripts\activate
pip install -r requirements.txt
python scripts/download_data.py      # télécharge ~120 Mo dans data/ (non versionné)
streamlit run app.py
```

## Explorer
```bash
python scripts/explorer_schema.py    # colonnes liées à l'IA + effectif France
pytest
```

## Axes
| Axe | Sujet | Branche | Responsable |
|---|---|---|---|
| 1 | Utilisation de l'IA | axe-1 | |
| 2 | Outils d'IA | axe-2 | |
| 3 | Confiance | axe-3 | Ayoub CHABBA |
| 4 | Utilité perçue et freins | axe-4 | |
| 5 | Profil des utilisateurs | axe-5 | |

Architecture : voir [ARCHITECTURE.md](ARCHITECTURE.md).
