import os
import streamlit as st
import pandas as pd

from application import Application
from exceptions import DonneeInvalideError
from graphiques import creer_graphique


def lancer():
    """Construit toute la page de l'application."""
    try:
        application = Application("modeles", os.path.join("donnees", "voitures.csv"),
                                  os.path.join("donnees", "historique.csv"))
    except FileNotFoundError as erreur:
        st.error(str(erreur))
        st.stop()

    metadonnees = application.modele.metadonnees

    st.title("Informations de la voiture") # titre
    st.warning("Attention estimation basée sur le marché indien donc à prendre avec du recul pour le marché canadien")

    info_Rentrer = {}

    ETIQUETTES = {
        "year": "Année du modèle",
        "km_driven": "Kilométrage (km)",
        "mileage": "Consommation (km/L)",
        "engine": "Cylindrée (cm³)",
        "max_power": "Puissance (bhp)",
        "seats": "Nombre de places",
    }

    for colonne in metadonnees["colonnes_numeriques"]:
        info_Rentrer[colonne] = st.text_input(ETIQUETTES[colonne])

    annee = info_Rentrer["year"]
    kilometrage = info_Rentrer["km_driven"]
    places = info_Rentrer["seats"]
    puissance = info_Rentrer["max_power"]
    cylindree = info_Rentrer["engine"]
    mileage = info_Rentrer["mileage"]

    # AFFICHAGE A L'ECRAN POUR SELECTIONNER OU RENTRER LES INFOS DEMANDEES

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

    # ESTIMER LE PRIX : la validation est faite par les classes Variable, dans Application
    if st.button("Estimer le prix"):
        saisies = {
            "year": annee,
            "km_driven": kilometrage,
            "seats": places,
            "max_power": puissance,
            "engine": cylindree,
            "mileage": mileage,
            "fuel": carburant,
            "transmission": transmission,
            "marque": marque,
            "seller_type": vendeur,
            "owner": proprietaire,
        }
        try:
            prix_estime = application.estimer(saisies)
            st.success(f"Prix estimé : environ {prix_estime:.0f} roupies indiennes")
            st.write(f"En moyenne, le modèle se trompe de ± {application.modele.erreur_moyenne:.0f} roupies indiennes.")
            st.pyplot(creer_graphique(application.prix_connus, prix_estime))
        except DonneeInvalideError as erreur:
            st.error(str(erreur))

    st.subheader("Historique des estimations")
    lignes = application.historique.lire()
    if len(lignes) <= 1:
        st.info("Aucune estimation pour le moment.")
    else:
        st.table(pd.DataFrame(lignes[1:], columns=lignes[0]))