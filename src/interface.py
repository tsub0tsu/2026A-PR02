import json
import os
import streamlit as st

chemin = os.path.join("modeles", "metadonnees.json")

with open(chemin, "r", encoding="utf-8") as f:         
    metadonnees = json.load(f)             # charge le metadonnee.json
# LES LIMIES DES INFORMATIONS

annee_min = metadonnees["colonnes_numeriques"]["year"]["min"]
annee_max = metadonnees["colonnes_numeriques"]["year"]["max"]    

kilometrage_min = metadonnees["colonnes_numeriques"]["km_driven"]["min"]
kilometrage_max = metadonnees["colonnes_numeriques"]["km_driven"]["max"] 

places_min = metadonnees["colonnes_numeriques"]["seats"]["min"]
places_max = metadonnees["colonnes_numeriques"]["seats"]["max"]


puissance_min = metadonnees["colonnes_numeriques"]["max_power"]["min"]
puissance_max = metadonnees["colonnes_numeriques"]["max_power"]["max"]

    
    
st.title("Informations de la voiture") # titre

# INFORMATION RENTER PAR L'UTILISATEUR 
annee = st.text_input("Année de la voiture")  # sa fait la case sur l interface avec le text_input()
kilometrage = st.text_input("Kilométrage de la voiture (km)")
places = st.text_input("Nombre de places")
puissance = st.text_input("Puissance du moteur (bhp)")

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
    if annee.strip() == "":
        st.error("Veuillez entrer une année.")
        
    elif kilometrage.strip() == "":
        st.error("Veuillez entrer un kilométrage.")
        
    elif places.strip() == "":
        st.error("Veuillez entrer le nombre de places.")
        
    elif puissance.strip() == "":
        st.error("Veuillez entrer la puissance du moteur.")
        
    else:
         try:
            valeur = int(annee)
            valeur_km = int(kilometrage)
            valeur_places = int(places)
            valeur_puissance = float(puissance)

            if valeur < annee_min or valeur > annee_max:
                st.error("Veuilliez rentrer une année  entre 1994 et 2020")
                
            elif valeur_km < kilometrage_min or valeur_km > kilometrage_max:
                st.error("Veuillez entre un  kilométrage entre 1000 et 500 000") 
                
            elif valeur_places < places_min or valeur_places > places_max:
                st.error("Veuillez rentrer  nombre de places entre 4 et 14") 
                
            else:
               st.success("L’année, le kilométrage et le nombre de places sont valides.")
               
         except ValueError:
            st.error("Entrez des nombres entiers pour l’année, le kilométrage et les places, et un nombre pour la puissance.")

#python -m streamlit run src/interface.py  