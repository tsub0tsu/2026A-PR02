from abc import ABC, abstractmethod
from donnees import valider_entier, valider_decimal, valider_categorie


class Variable(ABC):
    """Une caractéristique de la voiture que l'utilisateur doit saisir."""

    def __init__(self, nom: str, etiquette: str):
        self._nom = nom              
        self._etiquette = etiquette  

    @property
    def nom(self) -> str:
        """Nom de la colonne (lecture seule)."""
        return self._nom

    @property
    def etiquette(self) -> str:
        """Texte affiché dans l'interface (lecture seule)."""
        return self._etiquette

    @abstractmethod
    def valider(self, saisie: str):
        """Vérifie la saisie et renvoie la valeur convertie.
        DonneeInvalideError si la saisie n'est pas valide.
        """
        pass

    def __str__(self) -> str:
        return self._etiquette


class VariableNumerique(Variable):
    """Caractéristique numérique, avec un intervalle de valeurs permises."""

    def __init__(self, nom: str, etiquette: str, minimum: float, maximum: float, entier: bool):
        super().__init__(nom, etiquette)
        self._minimum = minimum
        self._maximum = maximum
        self._entier = entier

    def valider(self, saisie: str) -> float:
        """Vérifie que la saisie est un nombre (entier si demandé) dans l'intervalle.
        Reçoit le texte tapé par l'utilisateur.
        Renvoie le nombre converti.
        DonneeInvalideError si la saisie est vide, non numérique ou hors intervalle.
        """
        if self._entier:
            return valider_entier(saisie, self._etiquette, self._minimum, self._maximum)
        return valider_decimal(saisie, self._etiquette, self._minimum, self._maximum)

    def __repr__(self) -> str:
        return f"VariableNumerique({self._nom}, {self._minimum}, {self._maximum})"


class VariableCategorielle(Variable):
    """Caractéristique catégorielle, avec une liste de choix permis."""

    def __init__(self, nom: str, etiquette: str, choix: list):
        super().__init__(nom, etiquette)
        self._choix = choix

    @property
    def choix(self) -> list:
        """Copie de la liste des choix permis (l'original reste protégé)."""
        return list(self._choix)

    def valider(self, saisie: str) -> str:
        """Vérifie que la saisie fait partie des choix permis.
        Reçoit le choix de l'utilisateur.
        Renvoie ce même choix.
        DonneeInvalideError si le choix n'est pas dans la liste.
        """
        return valider_categorie(saisie, self._etiquette, self._choix)

    def __repr__(self) -> str:
        return f"VariableCategorielle({self._nom}, {len(self._choix)} choix)"