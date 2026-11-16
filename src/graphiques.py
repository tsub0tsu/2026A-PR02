import matplotlib.pyplot as plt

def creer_graphique(prix_connus, prix_estime: float):
    """Cree un histogramme des prix des voitures du fichier et une ligne rouge qui correspond a notre estimation.
    Recoit la colonne des prix du jeu de donnees et le prix estime selon la prediction et renvoie un graphique
    """
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(prix_connus / 100_000, bins=60, color="blue", label="Voitures du jeu de donnees")
    ax.axvline(prix_estime / 100_000, color="red", linewidth=3, label="voiture estimee")
    ax.set_title(f"Voiture estimee parmi les {len(prix_connus)} voitures du jeu de donnees")
    ax.set_xlabel("Prix de vente (en centaines de milliers de roupies)")
    ax.set_ylabel("Nombre de voitures")
    ax.legend()
    return fig