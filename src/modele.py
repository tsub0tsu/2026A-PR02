import os 
import json
import time 

import joblib
import numpy as np 
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.dummy import DummyRegressor
from sklearn.metrics  import r2_score

from donnees import COLONNES_NUMERIQUES, COLONNES_CATEGORIELLES, CIBLE

GRAINE = 22

def chronometrer(fonction): 
    """Décorateur qui affiche la durée d'exécution de la fonction décorée."""
    def nouvelle(modele, X, y):
        debut = time.time()
        resultat = fonction(modele, X, y)
        fin = time.time()
        print("Durée de l'entraînement :", round(fin - debut, 2), "s")
        return resultat
    return nouvelle

def separer_donnees(df: pd.DataFrame, taille_test: float = 0.2) -> tuple:
    """Sépare les données en ensemble d'entraînement et de test.
    Reçoit le DataFrame propre et les 20% de lignes réservées au test.
    Renvoie X_train, X_test, y_train, y_test. 
    """
    X = df[COLONNES_CATEGORIELLES + COLONNES_NUMERIQUES]
    y = df[CIBLE]
    return train_test_split(X, y, test_size=taille_test, random_state=GRAINE)

def creer_reference() -> DummyRegressor:
    """Renvoie un modèle qui prédit toujours le prix moyen."""
    return DummyRegressor(strategy="mean")

def creer_foret() -> Pipeline:
    """Renvoie un pipeline : encodage des catégories, puis forêt aléatoire."""
    encodeur = OneHotEncoder(handle_unknown="ignore")
    etape_encodage = ("categories", encodeur, COLONNES_CATEGORIELLES)
    preparation = ColumnTransformer([etape_encodage], remainder="passthrough")
    foret = RandomForestRegressor(n_estimators=100, min_samples_leaf=3, random_state=GRAINE)
    return Pipeline([("preparation", preparation), ("modele", foret)])

@chronometrer
def entrainer(modele, X_train: pd.DataFrame, y_train: pd.Series):
    """Entraîne le modèle sur les données d'entraînement et le renvoie."""
    return modele.fit(X_train, y_train)

def erreur_absolue_moyenne(y_vrai, y_predit) -> float : 
    """Calcule la MAE avec NumPy, sans boucle (calcul vectorisé).
    Reçoit les vraies valeurs et les valeurs prédites. 
    Renvoie la moyenne des écarts absolus. 
    Donne ValueError si les deux tableaux n'ont pas la même taille.
    """
    y_vrai = np.array(y_vrai, dtype=float)
    y_predit = np.array(y_predit, dtype=float)
    if y_vrai.shape != y_predit.shape:
        raise ValueError("Les deux tableaux doivent avoir la même taille.")
    ecarts = abs(y_vrai - y_predit)
    return float(ecarts.mean())

def evaluer(modele, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    """Calcule la MAE et le R² du modèle. 
    Reçoit un modèle entraîné et les données de test.
    Renvoie un dictionnaire avec la mae et le r²
    """
    y_predit = modele.predict(X_test)
    return{"mae": erreur_absolue_moyenne(y_test, y_predit), "r2": float(r2_score(y_test, y_predit))}

def creer_metadonnees(df: pd.DataFrame, scores: dict, scores_reference: dict) -> dict:
    """Construit le dictionnaire de métadonnées
    Reçoit le DataFrame propre et les scores du modèle et de la référence. 
    Renvoie un dictionnaire prêt à être écrit en JSON. 
    """
    numeriques = {}
    for colonne in COLONNES_NUMERIQUES:
        numeriques[colonne] = {"min": float(df[colonne].min()), "max": float(df[colonne].max())}
    categorielles = {}
    for colonne in COLONNES_CATEGORIELLES:
        categorielles[colonne] = sorted(df[colonne].unique().tolist())
    return {
        "cible": CIBLE, 
        "unite_cible": "roupies indiennes", 
        "colonnes_numeriques": numeriques,
        "colonnes_categorielles": categorielles,
        "metriques": scores, 
        "metriques_reference": scores_reference,
    }

def sauvegarder(modele, metadonnees: dict, dossier: str) -> None:
    """Enregistre le modèle (joblib) et ses métadonnées (JSON) dans le dossier. 
    Reçoit le modèle entraîné, les métadonnées et le dossier de destination.
    Ne renvoie rien et crée le dossier si il n'exsite pas. 
    """
    if not os.path.exists(dossier):
        os.mkdir(dossier)
    joblib.dump(modele, os.path.join(dossier, "modele.joblib"), compress=3)
    with open(os.path.join(dossier, "metadonnees.json"), "w", encoding="utf-8") as f:
        json.dump(metadonnees, f, indent=2, ensure_ascii=False)