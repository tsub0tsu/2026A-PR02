import os 
import matplotlib.pyplot as plt
from donnees import charger_donnees, nettoyer_donnees
from modele import (separer_donnees, creer_reference, creer_foret, entrainer, evaluer, creer_metadonnees, sauvegarder)

df = nettoyer_donnees(charger_donnees(os.path.join("donnees", "voitures.csv")))

#Séparer
X_train, X_test, y_train, y_test = separer_donnees(df)
print("Entraînement :", X_train.shape, "Test :", X_test.shape)

#Modèle de référence
reference = entrainer(creer_reference(), X_train, y_train)
scores_reference = evaluer(reference, X_test, y_test)
print("Référence (prix moyen) :", scores_reference)

#Vrai modèle
foret = entrainer(creer_foret(), X_train, y_train)
scores = evaluer(foret, X_test, y_test)
print("Forêt aléatoire :", scores)

y_predit = foret.predict(X_test)
fig, ax = plt.subplots(figsize=(7, 7))
ax.scatter(y_test /100_000, y_predit / 100_000, s=8, alpha=0.4, label="Voitures de test")
limite = max(y_test.max(), y_predit.max()) / 100_000
ax.plot([0, limite], [0, limite], color="red", label="Prédiction parfaite")
ax.set_title("Prix prédit contre prix réel (ensemble de test)")
ax.set_xlabel("Prix réel (centaines de milliers de roupies)")
ax.set_ylabel("Prix prédit (centaines de milliers de roupies)")
ax.legend()
if not os.path.exists("figures"):
    os.mkdir("figures")
fig.savefig(os.path.join("figures", "predit_vs_reel.png"), dpi=150)

#Sauvegarder 
metadonnees = creer_metadonnees(df, scores, scores_reference)
sauvegarder(foret, metadonnees, "modeles")
print("Modèle et métadonnées enregistrés dans modeles/")