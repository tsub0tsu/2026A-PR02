import os 
import pandas as pd 
from exceptions import DonneeInvalideError

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
    df = pd.read_csv(chemin) 
    if CIBLE not in df.columns : 
        raise DonneeInvalideError(f"La colonne cible '{CIBLE}' est absente")
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
    df = df[df["mileage"] > 0]
    df = df[df["km_driven"] <= 500_000]
    return df.reset_index(drop=True)

# verifie les donnes de l interface(page4)
def verifier_champ_rempli(texte: str, nom: str) -> None:
    """ la foncitonne Reçoit un texte et un nom, elle ne renvoie rien et  elle lève DonneeInvalideError si le texte est vide."""
    if texte.strip() == "":
        raise DonneeInvalideError(f"Veuillez remplir le champ : {nom}.")
    

def valider_entier(texte: str, nom: str, minimum: float, maximum: float) -> int:
    """Reçoit une saisie(texte), son nom et ses limites(min et max).elle Renvoie un entier valide ou lève DonneeInvalideError."""
    verifier_champ_rempli(texte, nom)
    try:
        valeur = int(texte) 
    except ValueError:
        raise DonneeInvalideError(f"{nom} doit être un nombre entier.")

    if valeur < minimum or valeur > maximum:
        raise DonneeInvalideError( f"{nom} doit être entre {minimum} et {maximum}.")

    return valeur

def valider_decimal(texte: str, nom: str, minimum: float, maximum: float) -> float:
    """Reçoit une saisie(texte), son nom et ses limites,Elle Renvoie un nombre valide ou lève DonneeInvalideError."""
    verifier_champ_rempli(texte, nom)
    try:
        valeur = float(texte)
    except ValueError:
        raise DonneeInvalideError(f"{nom} doit être un nombre.")
    if not (minimum <= valeur <= maximum):
        raise DonneeInvalideError(f"{nom} doit être entre {minimum} et {maximum}.")

    return valeur

def valider_categorie(choix: str, nom: str, options: list[str]) -> str:
    """Reçoit un choix, son nom et les options autorisées.elle Renvoie le choix ou lève DonneeInvalideError s’il est invalide."""
    verifier_champ_rempli(choix, nom)

    if choix not in options:
        raise DonneeInvalideError(f"Choix invalide pour : {nom}.")

    return choix