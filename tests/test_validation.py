import pytest
from donnees import valider_entier, valider_decimal, valider_categorie
from exceptions import DonneeInvalideError


def test_annee_valide():
    assert valider_entier("2018", "Année", 1994, 2020) == 2018


def test_limites_incluses():
    assert valider_entier("1994", "Année", 1994, 2020) == 1994
    assert valider_entier("2020", "Année", 1994, 2020) == 2020


def test_champ_vide():
    with pytest.raises(DonneeInvalideError):
        valider_entier("   ", "Année", 1994, 2020)


def test_texte_invalide():
    with pytest.raises(DonneeInvalideError):
        valider_entier("bonjour", "Année", 1994, 2020)


def test_hors_limites():
    with pytest.raises(DonneeInvalideError):
        valider_entier("2025", "Année", 1994, 2020)


def test_decimal_valide():
    resultat = valider_decimal("85.5", "Puissance", 34.2, 400)
    assert resultat == pytest.approx(85.5)


def test_nan_refuse():
    with pytest.raises(DonneeInvalideError):
        valider_decimal("nan", "Puissance", 34.2, 400)


def test_categories():
    options = ["Diesel", "Petrol"]
    assert valider_categorie("Diesel", "Carburant", options) == "Diesel"

    with pytest.raises(DonneeInvalideError):
        valider_categorie("Inconnu", "Carburant", options)