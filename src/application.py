from donnees import charger_donnees, nettoyer_donnees, CIBLE
from modele import ModelePrix, COLONNES_ENTREE
from historique import Historique
from variables import VariableNumerique, VariableCategorielle

ETIQUETTES = {
    "year": "Année du modèle",
    "km_driven": "Kilométrage (km)",
    "mileage": "Consommation (km/L)",
    "engine": "Cylindrée (cm³)",
    "max_power": "Puissance (bhp)",
    "seats": "Nombre de places",
    "fuel": "Carburant",
    "seller_type": "Type de vendeur",
    "transmission": "Boîte de vitesses",
    "owner": "Propriétaires précédents",
    "marque": "Marque",
}
COLONNES_ENTIERES = ["year", "km_driven", "engine", "seats"]


class Application:
    """Logique de l'application : contient le modèle, les variables et l'historique."""

    def __init__(self, dossier_modele: str, chemin_donnees: str, chemin_historique: str):
        """Charge le modèle, crée les variables et l'historique.
        FileNotFoundError si le modèle ou le CSV est introuvable.
        """
        self._modele = ModelePrix(dossier_modele)
        self._variables = self._creer_variables()
        self._historique = Historique(chemin_historique, COLONNES_ENTREE)
        voitures = nettoyer_donnees(charger_donnees(chemin_donnees))
        self._prix_connus = voitures[CIBLE]

    def _creer_variables(self) -> list:
        """Crée une variable par colonne, à partir des métadonnées du modèle."""
        meta = self._modele.metadonnees
        variables = []
        for nom, limites in meta["colonnes_numeriques"].items():
            entier = nom in COLONNES_ENTIERES
            variables.append(VariableNumerique(nom, ETIQUETTES[nom], limites["min"], limites["max"], entier))
        for nom, choix in meta["colonnes_categorielles"].items():
            variables.append(VariableCategorielle(nom, ETIQUETTES[nom], choix))
        return variables

    @property
    def variables(self) -> list:
        return list(self._variables)

    @property
    def modele(self) -> ModelePrix:
        return self._modele

    @property
    def historique(self) -> Historique:
        return self._historique

    @property
    def prix_connus(self):
        return self._prix_connus

    def estimer(self, saisies: dict) -> float:
        """Valide les saisies, prédit le prix et l'ajoute à l'historique.
        Reçoit {nom de colonne: texte saisi} pour les 11 caractéristiques.
        Renvoie le prix estimé en roupies.
        DonneeInvalideError à la première saisie invalide (rien n'est enregistré).
        """
        valeurs = {}
        for variable in self._variables:
            valeurs[variable.nom] = variable.valider(saisies[variable.nom])   # polymorphisme
        prix = self._modele.predire(valeurs)
        self._historique.ajouter(valeurs, prix)
        return prix

    def __str__(self) -> str:
        return f"Application : {len(self._variables)} variables, {self._modele}"