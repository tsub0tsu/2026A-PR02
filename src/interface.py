import json
import os
import streamlit as st
import pandas as pd
from donnees import valider_entier, valider_decimal, valider_categorie
from exceptions import DonneeInvalideError

from modele import ModelePrix, COLONNES_ENTREE
from donnees import charger_donnees, nettoyer_donnees, CIBLE
from graphiques import creer_graphique
from historique import Historique

try:
    modele = ModelePrix("modeles")
    voitures = nettoyer_donnees(charger_donnees(os.path.join("donnees", "voitures.csv")))
    prix_connus = voitures[CIBLE]
    historique = Historique(os.path.join("donnees", "historique.csv"), COLONNES_ENTREE)
except FileNotFoundError as erreur : 
    st.error(str(erreur))
    st.stop()

chemin = os.path.join("modeles", "metadonnees.json")

if not os.path.isfile(chemin):
    st.error("Le fichier de métadonnées est introuvable.")
    st.stop()

with open(chemin, "r", encoding="utf-8") as f:
    metadonnees = json.load(f) 
    
    
    
    

annee_min = metadonnees["colonnes_numeriques"]["year"]["min"]
annee_max = metadonnees["colonnes_numeriques"]["year"]["max"]    

kilometrage_min = metadonnees["colonnes_numeriques"]["km_driven"]["min"]
kilometrage_max = metadonnees["colonnes_numeriques"]["km_driven"]["max"] 

places_min = metadonnees["colonnes_numeriques"]["seats"]["min"]
places_max = metadonnees["colonnes_numeriques"]["seats"]["max"]

max_power_min = metadonnees["colonnes_numeriques"]["max_power"]["min"]
max_power_max = metadonnees["colonnes_numeriques"]["max_power"]["max"]

engine_min = metadonnees["colonnes_numeriques"]["engine"]["min"]
engine_max = metadonnees["colonnes_numeriques"]["engine"]["max"]

mileage_min = metadonnees["colonnes_numeriques"]["mileage"]["min"]
mileage_max = metadonnees["colonnes_numeriques"]["mileage"]["max"]
    
st.title("Informations de la voiture") # titre

info_Rentrer = {}

for colonne in metadonnees["colonnes_numeriques"]:
    info_Rentrer[colonne] = st.text_input(colonne)

annee = info_Rentrer["year"]
kilometrage = info_Rentrer["km_driven"]
places = info_Rentrer["seats"]
puissance = info_Rentrer["max_power"]
cylindree =info_Rentrer["engine"]
mileage = info_Rentrer["mileage"]

# AFFICHAGE A L'ECRAN POUR SELECTIONNER OU RENTER LES INFO DEMANDER

#1
choix_carburants = metadonnees["colonnes_categorielles"]["fuel"]

carburant = st.selectbox("Carburant", choix_carburants)  
#2
choix_transmissions = metadonnees["colonnes_categorielles"]["transmission"]

transmission = st.selectbox("Transmission", choix_transmissions) 
#3
choix_marques = metadonnees["colonnes_categorielles"]["marque"]

marque = st.selectbox("Marque de la voiture", choix_marques)
#4
choix_vendeurs = metadonnees["colonnes_categorielles"]["seller_type"]

vendeur = st.selectbox("Type de vendeur", choix_vendeurs) 
#5
choix_proprietaires = metadonnees["colonnes_categorielles"]["owner"]

proprietaire = st.selectbox("Catégorie de propriétaire", choix_proprietaires)

# VERIFIER SI LES INFORMATION RENTRE SONT VALIDE  
if st.button("Valider"):
    try:
        valeur = valider_entier(annee, "Année", annee_min, annee_max)
        
        valeur_km = valider_entier(kilometrage, "Kilométrage", kilometrage_min, kilometrage_max)
        
        valeur_places = valider_entier(places, "Places", places_min, places_max)
        
        valeur_engine = valider_entier(cylindree, "Engine", engine_min, engine_max)

        valeur_puissance = valider_decimal(puissance, "Puissance", max_power_min, max_power_max)

        valeur_mileage = valider_decimal(mileage, "Mileage", mileage_min, mileage_max)
        
        carburant = valider_categorie(carburant, "Carburant", choix_carburants)
        
        transmission = valider_categorie(transmission, "Transmission", choix_transmissions)
        
        marque = valider_categorie(marque, "Marque", choix_marques)
        
        vendeur = valider_categorie(vendeur, "Vendeur", choix_vendeurs)
        
        proprietaire = valider_categorie(proprietaire, "Propriétaire", choix_proprietaires)

        donnees_voiture = {
            "year": valeur,
            "km_driven": valeur_km,
            "seats": valeur_places,
            "max_power": valeur_puissance,
            "engine": valeur_engine,
            "mileage": valeur_mileage,
            "fuel": carburant,
            "transmission": transmission,
            "marque": marque,
            "seller_type": vendeur,
            "owner": proprietaire
        }

        prix_estime = modele.predire(donnees_voiture)
        historique.ajouter(donnees_voiture, prix_estime)
        st.success(f"Prix estimé : environ {prix_estime:.0f} roupies indiennes")
        st.write(f"En moyenne, le modèle se trompe de ± {modele.erreur_moyenne:.0f} roupies indiennes.")
        st.pyplot(creer_graphique(prix_connus, prix_estime))

    except DonneeInvalideError as erreur:
        st.error(str(erreur))
        
        
#python -m streamlit run src/interface.py  
