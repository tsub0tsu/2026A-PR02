import os 
import pandas as pd 
from src.exceptions import DonneeInvalideError

COLONNES_NUMERIQUES = ["year", "km_driven", "mileage", "engine", "max_power", "seats"]
COLONNES_CATEGORIELLES = ["fuel", "seller_type", "transmission", "owner", "marque"]
CIBLE = "selling_price"

def charger_donnees(chemin:str)-> pd.DataFrame :
    """Lit le fichier CSV des voitures. 
    Reçoit le chemin du fichier CSV
    Renvoie un DataFrame avec les données brutes
    Donne FileNotFoundError si le fichier n'existe pas ou DonneeInvalideError si la colonnne cible est absente. 
    """
    if not os.path.exists(chemin):
        raise FileNotFoundError(f"Fichier introuvable : {chemin}")
    df = pd.read_csv(chemin) #demander si ok ? ou with obligatoire
    if CIBLE not in df.columns : 
        raise DonneeInvalideError(f"La colonne cible '{CIBLE}est absente")
    return df

def extraire_nombre(colonne : pd.Series)-> pd.Series :
    """Transforme un texte en nombre. 
    Reçoit une colonne de textes
    Renvoie une colonne de nombres (ou NaN si texte pas convertible)
    """
    premier_mot = colonne.str.split().str[0]
    return pd.to_numeric(premier_mot, errors="coerce")

def nettoyer_donnees(df : pd.DataFrame)-> pd.DataFrame :
    """Nettoie les données (doublons, unités, valeurs manquantes ou aberrantes)
    Reçoit le DataFrame brut
    Renvoie un nouveau DataFrame propre. 
    """
    df = df.copy()
    df = df.drop_duplicates()
    df = df[df["fuel"].isin(["Diesel", "Petrol"])]
    df = df[df["owner"] != "Test Drive Car"]

    df["mileage"] = extraire_nombre(df["mileage"])
    df["engine"] = extraire_nombre(df["engine"])
    df["max_power"] = extraire_nombre(df["max_power"])

    df["marque"] = df["name"].str.split().str[0]
    comptes = df["marque"].value_counts()
    marques_rares = [marque for marque, nombre in comptes.items() if nombre < 10]
    df.loc[df["marque"].isin(marques_rares), "marque"] = "Autre"

    df = df.drop(columns=["name", "torque"])
    df = df.dropna()
    df = df[df["max_power"] > 0]
    df = df[df["km_driven"] <= 500_000]
    return df.reset_index(drop=True)
