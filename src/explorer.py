import os 
import matplotlib.pyplot as plt
from donnees import charger_donnees, nettoyer_donnees, CIBLE

chemin = os.path.join("donnees", "voitures.csv")    
df = charger_donnees(chemin)

print("Avant nettoyage :", df.shape)
print(df.dtypes)
print(df.isna().sum())
print("Doublons :", df.duplicated().sum())

propre = nettoyer_donnees(df)
print("Apres nettoyage :", propre.shape)
print(propre.describe())
print(propre["marque"].value_counts())

fig, axes = plt.subplots(1, 2, figsize=(12,5))

axes[0].hist(propre[CIBLE] / 100_000, bins=50, color ="steelblue")
axes[0].set_title("Distribution des prix de vente")
axes[0].set_xlabel("Prix de vente (centaines de milliers de roupies)")
axes[0].set_ylabel("Nombre de voitures")

axes[1].scatter(propre["year"], propre[CIBLE] / 100_000, s=5, alpha=0.4)
axes[1].set_title("Prix de vente selon l'année")
axes[1].set_xlabel("Année du modèle")
axes[1].set_ylabel("Prix de vente (centaines de milliers de roupies)")

if not os.path.exists("figures"):
    os.mkdir("figures")
fig.savefig(os.path.join("figures", "exploration.png"), dpi=150)
print("Graphique enregistré dans figures/exploration.png")