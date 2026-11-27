import pandas as pd
from src.population import filtrer_france, decrire


def test_filtrer_france_et_effectif():
    df = pd.DataFrame({"Country": ["France", "Germany", "France"], "x": [1, None, 3]})
    fr = filtrer_france(df)
    assert len(fr) == 2
    assert decrire(fr, "test", 2026, colonne="x").n == 2
