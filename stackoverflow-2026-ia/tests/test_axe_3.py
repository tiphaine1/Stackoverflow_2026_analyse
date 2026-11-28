import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "axes"))
import axe_3  # noqa: E402


@pytest.mark.parametrize("brut,attendu", [
    ("Highly trust", "Très confiant"),
    ("Somewhat distrust", "Plutôt méfiant"),
    ("Neither trust nor distrust", "Ni confiance ni méfiance"),
])
def test_recodage_confiance(brut, attendu):
    assert axe_3.recoder(pd.Series([brut]), "AIAcc").iloc[0] == attendu


def test_reponse_inconnue_devient_manquante():
    assert pd.isna(axe_3.recoder(pd.Series(["Autre chose"]), "AIAcc").iloc[0])


def test_distribution_somme_100_et_effectif():
    df = pd.DataFrame({"AIAcc": ["Highly trust", "Highly trust", "Highly distrust", None]})
    table, n = axe_3.distribution(df, "AIAcc")
    assert n == 3
    assert table["pct"].sum() == pytest.approx(100)


def test_part_confiance():
    df = pd.DataFrame({"AIAcc": ["Highly trust", "Somewhat distrust", "Neither trust nor distrust", None]})
    conf, mefi, n = axe_3.part_confiance(df)
    assert n == 3
    assert conf == pytest.approx(100 / 3)
    assert mefi == pytest.approx(100 / 3)


def test_solde_ignore_petits_groupes():
    df = pd.DataFrame({"AIAcc": ["Highly trust"] * 30 + ["Highly distrust"] * 5,
                       "RemoteWork": ["Remote"] * 30 + ["In-person"] * 5})
    s = axe_3.solde_par_groupe(df, "RemoteWork", min_n=30)
    assert list(s["groupe"]) == ["Remote"]
    assert s["solde"].iloc[0] == pytest.approx(100)
