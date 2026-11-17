import csv
import os 

class Historique :
    """Fichier CSV qui garde toutes les estimations faites dans l'application."""

    def __init__(self, chemin: str, colonnes: list):
        self._chemin = chemin
        self._colonnes = colonnes

    def ajouter(self, valeurs: dict, prix: float) -> None :
        """Ajoute une estimation à la fin du fichier (crée le fichier et l'en-tête si c'est la première)
        Reçoit les valeurs saisies et le prix estimé.
        """
        nouveau_fichier = not os.path.exists(self._chemin)
        with open(self._chemin, "a", encoding="utf-8", newline="") as f:
            ecrivain = csv.writer(f)
            if nouveau_fichier:
                ecrivain.writerow(self._colonnes + ["prix_estime"])
            ligne = [valeurs[colonne] for colonne in self._colonnes]
            ecrivain.writerow(ligne + [round(prix)])

    def lire(self) -> list:
        """Renvoie toutes les lignes du fichier avec l'en-tête en première ligne."""
        if not os.path.exists(self._chemin):
            return[]
        with open(self._chemin, "r", encoding="utf-8", newline="") as f :
            lecteur = csv.reader(f)
            return [rangee for rangee in lecteur]

    def __str__(self) -> str :
        nombre = max(len(self.lire()) - 1, 0)
        return f"Historique de {nombre} estimation(s)."