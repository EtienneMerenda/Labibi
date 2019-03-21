#-*- coding: utf-8 -*-

from Tools import folderCleanerByExtKeeper, fileListMaker, extensionRemover,\
 inputWithNumberConstraint

class MapSelect():
    """Classe permettant de gérer la selection des cartes"""

    def __init__(self):
        self._mapExisting = []
        self._mapTitleProper = []
        self._mapChoiced = 0

    def getMap(self):
        return self._mapChoiced

    def mapListPrinter(self):
        """Récupère la liste des cartes et l'affiche sur la console"""

        # Je supprime les documents non .txt avant listage des cartes.
        folderCleanerByExtKeeper("./maps/", ".txt")

        # Je récupère ma liste de carte
        self._mapExisting = fileListMaker("./maps/")

        # Création d'une liste contenant les cartes entières divisées en liste.
        maps = []
        i = 0
        while i < len(self._mapExisting):
            with open("maps/" + self._mapExisting[i], "r") as map:
                maps.append((map.read().split("\n")))
            i += 1

        # Je supprime les extensions pour incrémenter de 1 l'esthétisme.

        self._mapTitleProper = extensionRemover(self._mapExisting, ".txt")

        # Affichage des cartes disponible suivi de leur numéro et nom.

        print("Les cartes disponibles sont:\n")
        i = 0
        while i < len(self._mapExisting):
            print(i + 1, "- {0} \n\n{1}\n".format(self._mapTitleProper[i], "\n".join(maps[i])))
            i += 1

    def mapListSelecter(self):
        """Méthode permettant la selection de la carte et son affichage.
        Retourne la carte sous forme de str."""

        # Condition et boucle permettant de demander de choisir une carte
        # tant que l'utilisateur n'a pas rentré de numéro correct

        number = self._mapChoiced = inputWithNumberConstraint(len(self._mapExisting), 1) - 1
        # Je récupère donc ladite carte et je retourne également le nom de la
        # carte pour l'affichage du jeu.

        with open("maps/" + self._mapExisting[number], "r") as map:
            self._mapChoiced = map.read()
            return self._mapChoiced, self._mapExisting[number - 1][:-4], number - 1

    def loadingMap(self, loading):
        """methode chargé de charger la map suivant la situation de l'ancienne partie."""

        import os

        # Je supprime les documents non .txt avant listage des cartes.
        intruders = os.listdir("./maps")
        for item in intruders:
            if not item.endswith(".txt"):
                os.remove("maps/" + item)

        # Je récupère ma liste de carte
        self._mapExisting = os.listdir("./maps")

        maps = []
        i = 0
        while i < len(self._mapExisting):
            with open("maps/" + self._mapExisting[i], "r") as map:
                maps.append((map.read().split("\n")))
            i += 1

        # Je supprime les extensions pour incrémenter de 1 l'esthétisme.
        mapListTemp = "".join(self._mapExisting)
        self._mapProper = mapListTemp.split(".txt")
        # ayant splitté par .txt, la dernière entrée est un champ vide que je
        # supprime.
        del self._mapProper[-1]

        with open("maps/" + self._mapExisting[loading], "r") as map:
            self._mapChoiced = map.read()
        return self._mapChoiced,
