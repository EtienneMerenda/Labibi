#-*- coding: utf-8 -*-

from Tools import *
from MapSelect import *
from Data import playerIcon, playerIconUsed


class TurnAndTurn:

    def __init__(self):

        # Carte sans le X qui servira de planche où venir coller notre "X".
        self._mapOriginal = []
        # Carte utilisé pour tout le reste.
        self._mapUsed = []
        # Liste des robots utilisés pour la partie.
        self._playerIcon = playerIcon
        self._playerIconUsed = playerIconUsed
        # Dictionnaire des joueurs contenant le robot du joueur, sa position,
        # son nombre de tours
        self._playersInfos = {}

        # Compteur de tour
        self._nbMove = 0
        # Valeur sondé l'endroit où se déplace notre cher bot.
        self._probe = ""
        # Boléen qui conditionne si la partie doit s'arrêter ou pas.
        self.win = False

    def map_refresh(self, map):
        # Au premier tour, map contiendra 3 objets.
        # Si un partie est chargé, le constructeur passera par le else.

        if len(map) == 3:
            self._mapUsed = map[0].split("\n")
            # Nom de la carte joué.
            self._titleMap = map[1]
            # Numéro de la carte joué.
            self._mapChoiced = map[2]
        else:
            self._mapUsed = map[0].split("\n")
            self._mapChoiced = ""
            self._titleMap = ""

    def mapWithoutX(self):
        """Création d'une carte sans le "X" qui servira de base pour le collage
        de "X" lors de son déplacement."""
        for item in self._mapUsed:
            temp = ""
            for letter in item:
                if "X" in letter:
                    letter = " "
                temp += letter
            self._mapOriginal.append(temp)
        return self._mapOriginal

    def cleanMap(self):
        self._mapUsed = self._mapOriginal

    def pastePlayer(self, bot="", cmd="newPlayer"):
        """Mets un joueur sur la carte quand la méthode est appellé.
Retourne self._mapMultiplayer
Options disponibles:
-'newPlayer'
-'cut'
-'paste'
-'door'
-'wall'"""

        def pasteMe(bot):
            """Applique le robot choisi à la position souhaité. Se sert du bot
pour trouver dans le dictionniare la position voulue.
Ajoute la case sur laquelle appliqué le bot dans son dictionnaire."""

            self._playersInfos[bot]["turnNumber"][0] += 1
            chaine = self._mapUsed[self._playersInfos[bot]["positionY"]]
            oldCase = chaine[self._playersInfos[bot]["positionX"]]
            deb = chaine[0:(self._playersInfos[bot]["positionX"])]
            fin = chaine[self._playersInfos[bot]["positionX"] + 1:]
            refreshChain = deb+bot+fin
            self._mapUsed[self._playersInfos[bot]["positionY"]] = refreshChain

            # Attribution des infos pour la fonction cutMe()
            self._playersInfos[bot]["oldCase"] = oldCase
            if oldCase is ".":
                self._playersInfos[bot]["doorSlowDown"] = True
            else:
                self._playersInfos[bot]["doorSlowDown"] = False
            self._playersInfos[bot]["oldPositionY"] = self._playersInfos[bot]["positionY"]
            self._playersInfos[bot]["oldPositionX"] = self._playersInfos[bot]["positionX"]

            return self._mapUsed

        def cutMe(bot):
            chaine = self._mapUsed[self._playersInfos[bot]["oldPositionY"]]
            deb = chaine[0:(self._playersInfos[bot]["oldPositionX"])]
            fin = chaine[self._playersInfos[bot]["oldPositionX"] + 1:]
            refreshChain = deb+self._playersInfos[bot]["oldCase"]+fin
            self._mapUsed[self._playersInfos[bot]["oldPositionY"]] = refreshChain
            return self._mapUsed

        def setDoorOrWall(bot, cmd):
            if cmd is "door":
                self._playersInfos[bot]["turnNumber"][0] += 1
                chaine = self._mapUsed[self._playersInfos[bot]["drilling"][0]]
                deb = chaine[0:(self._playersInfos[bot]["drilling"][1])]
                fin = chaine[self._playersInfos[bot]["drilling"][1] + 1:]
                refreshChain = deb+"."+fin
                self._mapUsed[self._playersInfos[bot]["drilling"][0]] = refreshChain

                return self._mapUsed

            elif cmd is "wall":
                self._playersInfos[bot]["turnNumber"][0] += 1
                chaine = self._mapUsed[self._playersInfos[bot]["walling"][0]]
                deb = chaine[0:(self._playersInfos[bot]["walling"][1])]
                fin = chaine[self._playersInfos[bot]["walling"][1] + 1:]
                refreshChain = deb+"O"+fin
                self._mapUsed[self._playersInfos[bot]["walling"][0]] = refreshChain

                return self._mapUsed

        if cmd is "newPlayer":
            import random

            # Sélection du bot
            bot = self._playerIcon[random.randrange(0, len(self._playerIcon), 1)]
            self._playerIcon.remove(bot)
            self._playerIconUsed.append(bot)

            # Dépose du bot
            turnNumberAndLastChoice = [0, ""]
            positionY = 0
            positionX = 0
            while self._mapUsed[positionY][positionX] not in [" "]:
                positionY = random.randrange(0, len(self._mapUsed) - 1, 1)
                positionX = random.randrange(0, len(self._mapUsed[positionY]) - 1, 1)
            self._playersInfos[bot] = {"turnNumber": turnNumberAndLastChoice, "positionY": positionY, "positionX": positionX, "moveChoice": []}
            self._mapUsed = pasteMe(bot)

            return self._mapUsed, bot

        elif cmd is "cut":
            self._mapUsed = cutMe(bot)

        elif cmd is "paste":
            self._mapUsed = pasteMe(bot)

        elif cmd is "wall" or cmd is "door":
            self._mapUsed = setDoorOrWall(bot, cmd)

            return self._mapUsed

    def intitPos(self, loading):
        """réattribut les positions de la sauvegarde précédente"""

        # Si une partie est chargé, les données sont réattribuées.

        self._position = loading[0]
        self._moveChoice = loading[1]
        self._nbMove = loading[2]
        self._mapChoiced = loading[3]

    def surroundingsChecker(self, bot, direction="all"):

        probedCaseList = []
        case = ""

        if direction is "N":
            i = 1
            while case != "O" and i <= self._playersInfos[bot]["positionY"]:
                case = self._mapUsed[self._playersInfos[bot]["positionY"] - i][self._playersInfos[bot]["positionX"]]
                probedCaseList.append(case)
                if case != "O":
                    i += 1
        elif direction is "S":
            i = 1
            while case != "O" and i < len(self._mapUsed) - self._playersInfos[bot]["positionY"]:
                case = self._mapUsed[self._playersInfos[bot]["positionY"] + i][self._playersInfos[bot]["positionX"]]
                probedCaseList.append(case)
                if case != "O":
                    i += 1
        elif direction is "E":
            i = 1
            print(len(self._mapUsed[self._playersInfos[bot]["positionY"]]))
            print(self._playersInfos[bot]["positionX"])
            print((len(self._mapUsed[self._playersInfos[bot]["positionY"]]) - self._playersInfos[bot]["positionX"])-1)
            while case != "O" and i <= (len(self._mapUsed[self._playersInfos[bot]["positionY"]]) - self._playersInfos[bot]["positionX"]) - 1:
                case = self._mapUsed[self._playersInfos[bot]["positionY"]][self._playersInfos[bot]["positionX"] + i]
                probedCaseList.append(case)
                if case != "O":
                    i += 1
        elif direction is "O":
            i = 1
            while case != "O" and i <= self._playersInfos[bot]["positionX"]:
                case = self._mapUsed[self._playersInfos[bot]["positionY"]][self._playersInfos[bot]["positionX"] - i]
                probedCaseList.append(case)
                if case != "O":
                    i += 1

        elif direction is "all":
            probedCaseDict = {}
            i = 1
            try:
                probedCaseDict["N"] = self._mapUsed[self._playersInfos[bot]["positionY"] - i][self._playersInfos[bot]["positionX"]]
            except IndexError:
                pass
            try:
                probedCaseDict["S"] = self._mapUsed[self._playersInfos[bot]["positionY"] + i][self._playersInfos[bot]["positionX"]]
            except IndexError:
                pass

            try:
                probedCaseDict["E"] = self._mapUsed[self._playersInfos[bot]["positionY"]][self._playersInfos[bot]["positionX"] + i]
            except IndexError:
                pass

            try:
                probedCaseDict["O"] = self._mapUsed[self._playersInfos[bot]["positionY"]][self._playersInfos[bot]["positionX"] - i]
            except IndexError:
                pass

            return probedCaseDict
        return probedCaseList, i

    def cardinalFullWord(self, list):
        """Transforme l'entrée utilisateur en point cardinaux ecrit en toute
 lettre"""
        fullWordList = []
        for value in list:
            if value is "N":
                fullWordList.append("au Nord")
            elif value is "S":
                fullWordList.append("au Sud")
            elif value is "E":
                fullWordList.append("à l'Est")
            elif value is "O":
                fullWordList.append("à l'Ouest")

        if len(fullWordList) > 0:
            return fullWordList
        else:
            return None

    def inputChoice(self, bot):
        """Récupère le déplacement voulu par le joueur"""

        import time

        # Au premier tour, donne les indications sur la méthode pour entrer
        # les mouvements
        if self._playersInfos[bot]["turnNumber"][0] == 1:
            ("\nVous avez choisi le niveau: {0}\n\n{1}\n\nVous pouvez \
déplacer le robot à l'aide des commande:\
\n  -N: pour aller vers le nord.\n  -S: pour aller vers le Sud.\n  -O: pour aller \
vers l'Ouest.\n  -E: pour aller vers l'Est.\nVous entrerez ensuite le nombre \
de cases que vous voulez faire parcourir au robot.\n\nVous avez la possiblité de \
murer une porte avec la commande M suivi de la direction.\nOu de percer un mur \
avec la commande P et la direction.\n\nVous pouvez quittez le\
 jeu en tapant 'Q' lors du choix de la direction".format(self._titleMap, "\n".join(self._mapUsed)))
            #input("\nLa partie va commencer dans 5 secondes.")
            #time.sleep(5)

        # On récupère la commande du joueur en vérifiant qu'il la rentre
        # correctement.

        moveInput = [""]
        boléen0 = False
        boléen1 = False
        avalaibleMove = []

        souroundingsDict = self.surroundingsChecker(bot)
        print(souroundingsDict)
        for key, value in souroundingsDict.items():
            if value is " " or value is "." or value is "U":
                avalaibleMove.append(key)
            if value is "." and avalaibleMove.count("M") == 0:
                avalaibleMove.append("M")
            if value is "O" and avalaibleMove.count("P") == 0:
                avalaibleMove.append("P")
        avalaibleMove.append("Q")
        print(avalaibleMove)
        avalaibleMoveTxt = ""
        if "N" in avalaibleMove:
                avalaibleMoveTxt += " -Aller au Nord\n"
        if "S" in avalaibleMove:
            avalaibleMoveTxt += " -Aller au Sud\n"
        if "E" in avalaibleMove:
            avalaibleMoveTxt += " -Aller à l'Est\n"
        if "O" in avalaibleMove:
            avalaibleMoveTxt += " -Aller à l'Ouest\n"
        if "M" in avalaibleMove:
            avalaibleMoveTxt += " -Murer\n"
        if "P" in avalaibleMove:
            avalaibleMoveTxt += " -Percer\n"
        while boléen0 is False and moveInput[0] != "Q":
            try:
                print("\n" + "\n".join(self._mapUsed))
                move = input("\nChoisissez votre action:\n{}".format(avalaibleMoveTxt)).upper()
                if move[0] in avalaibleMove and len(move) == 1:
                    boléen0 = True
                    moveInput[0] = move
                    if move[0] == "Q":
                        return "Q"
                else:
                    print("Votre commande n'est pas bonne.\n")
            except IndexError:
                print("Votre commande n'est pas bonne.\n")

        while boléen1 is False:
            if move[0] in ["E", "O", "N", "S"]:
                if move[0] == "N":
                    direction = "le Nord"
                elif move[0] == "S":
                    direction = "le Sud"
                elif move[0] == "E":
                    direction = "l'Est"
                elif move[0] == "O":
                    direction = "l'Ouest"
                caseListProbed, NbStep = self.surroundingsChecker(bot, move[0])
                if NbStep > 1:
                    while boléen1 is False and moveInput[0] != "Q":
                        try:
                            nbStep = input("Vous partez vers {0}. vous pouvez \
faire {1} pas. Combien souhaitez vous en faire: ".format(direction, NbStep - 1))
                            nbStep = int(nbStep)

                            if nbStep > 0 and nbStep <= NbStep:
                                moveInput.append(nbStep)
                                boléen1 = True
                                self._playersInfos[bot]["moveChoice"].append(moveInput)
                                self._playersInfos[bot]["turnNumber"][1] = moveInput
                            else:
                                print("Votre saisie est invalide.\n")
                        except ValueError:
                                print("Vous n'avez pas saisie un nombre.\n")
                else:
                    print("Vous ne pouvez pas aller dans cette direction.\n")

            elif move[0] == "M":

                doors = self.surroundingsChecker(bot, "all")
                indexList = dictIndexGetter(doors, ".")

                if len(indexList) is 0:
                    print("Vous ne pouvez murer aucune porte à proximité.\n")
                else:
                    direction = self.cardinalFullWord(indexList)
                    avalaibleDirectionTemp = ""

                    for value in direction:
                        avalaibleDirectionTemp += value+", "

                    avalaibleDirection = avalaibleDirectionTemp[:-2]
                    while boléen1 is False:
                        wallDir = input("Vous avez choisi de murer. Vous pouvez le faire {}. Dans quelle\
 direction souhaitez vous le faire: ".format(avalaibleDirection)).upper()
                        if wallDir in indexList:
                            moveInput.append(wallDir)
                            self._playersInfos[bot]["moveChoice"].append(moveInput)
                            self._playersInfos[bot]["turnNumber"][1] = moveInput
                            boléen1 = True

            elif move[0] == "P":

                wall = self.surroundingsChecker(bot, "all")
                indexList = dictIndexGetter(wall, "O")
                if len(indexList) is 0:
                    print("Vous ne pouvez percer aucun mur à proximité.\n")

                else:
                    direction = self.cardinalFullWord(indexList)
                    avalaibleDirectionTemp = ""

                    for value in direction:
                        avalaibleDirectionTemp += value+", "

                    avalaibleDirection = avalaibleDirectionTemp[:-2]

                    while boléen1 is False:
                        drillDir = input("Vous avez choisi de percer. Vous \
pouvez le faire {}. Dans quelle direction souhaitez vous le faire: \
".format(avalaibleDirection)).upper()
                        if drillDir in indexList:
                            moveInput.append(drillDir)
                            self._playersInfos[bot]["moveChoice"].append(moveInput)
                            self._playersInfos[bot]["turnNumber"][1] = moveInput
                            boléen1 = True

    def passOrChoice(self, bot):
        try:
            print(self._playersInfos[bot]["moveChoice"][-1][-1])
            if self._playersInfos[bot]["moveChoice"][-1][-1] > 0:
                optionalCaracter = ["O", "o", "N", "n"]
                change = inputWithCaraterConstraint("Voulez vous changer de direction ? O/N", optionalCaracter).upper()
                print(change, type(change))
                if change == "O":
                    print("Je souhaite changer de déplacement")
                    self.inputChoice(bot)
                elif change is "N":
                    pass
            else:
                self.inputChoice(bot)
        except IndexError:
            self.inputChoice(bot)

    def move(self, bot):
        """Va chercher le type de case vers lequel se déplace le joueur, check
si c'est possible d'y aller et déplace le joueur"""

        # Relève l'environnement autour du robot en fonction du choix du joueur
        # et le met dans un dictionnaire

        # Si toi aussi tu penses qu'il y a trop de liste, bienvenu au club.
        # À ce stade, mon cerveau coule par mon nez.

        print(self._playersInfos[bot])

        # Si le bot est passé par une porte, retarde d'un tour
        if self._playersInfos[bot]["doorSlowDown"] is True:
            self._playersInfos[bot]["doorSlowDown"] = False
            print("Le crochetage de la porte vous a fait perdre un tour.\n")

        else:
            print(self._playersInfos[bot]["moveChoice"][-1][0])
            if self._playersInfos[bot]["moveChoice"][-1][0] in ["N", "S", "O", "E"]:

                self.pastePlayer(bot, "cut")
                if "N" in self._playersInfos[bot]["moveChoice"][-1]:
                    self._playersInfos[bot]["positionY"] -= 1
                    if self._playersInfos[bot]["moveChoice"][-1][-1] > 0:
                        self._playersInfos[bot]["moveChoice"][-1][-1] -= 1
                elif "S" in self._playersInfos[bot]["moveChoice"][-1]:
                    self._playersInfos[bot]["positionY"] += 1
                    if self._playersInfos[bot]["moveChoice"][-1][-1] > 0:
                        self._playersInfos[bot]["moveChoice"][-1][-1] -= 1
                elif "O" in self._playersInfos[bot]["moveChoice"][-1]:
                    self._playersInfos[bot]["positionX"] -= 1
                    if self._playersInfos[bot]["moveChoice"][-1][-1] > 0:
                        self._playersInfos[bot]["moveChoice"][-1][-1] -= 1
                elif "E" in self._playersInfos[bot]["moveChoice"][-1]:
                    self._playersInfos[bot]["positionX"] += 1
                    if self._playersInfos[bot]["moveChoice"][-1][-1] > 0:
                        self._playersInfos[bot]["moveChoice"][-1][-1] -= 1
                if self._mapUsed[self._playersInfos[bot]["positionY"]][self._playersInfos[bot]["positionX"]] is "U":
                    self.win = True
                self.pastePlayer(bot, "paste")

            elif self._playersInfos[bot]["moveChoice"][-1][0] == "P":

                if self._playersInfos[bot]["moveChoice"][-1][1] == "N":
                    self._playersInfos[bot]["drilling"] = (self._playersInfos[bot]["positionY"] -1, self._playersInfos[bot]["positionX"])
                if self._playersInfos[bot]["moveChoice"][-1][1] == "S":
                    self._playersInfos[bot]["drilling"] = (self._playersInfos[bot]["positionY"] +1, self._playersInfos[bot]["positionX"])
                if self._playersInfos[bot]["moveChoice"][-1][1] == "E":
                    self._playersInfos[bot]["drilling"] = (self._playersInfos[bot]["positionY"], self._playersInfos[bot]["positionX"] + 1)
                if self._playersInfos[bot]["moveChoice"][-1][1] == "O":
                    self._playersInfos[bot]["drilling"] = (self._playersInfos[bot]["positionY"], self._playersInfos[bot]["positionX"] - 1)
                print(self._playersInfos[bot]["drilling"])
                self.pastePlayer(bot, "door")

            elif self._playersInfos[bot]["moveChoice"][-1][0] == "M":

                if self._playersInfos[bot]["moveChoice"][-1][1] == "N":
                    self._playersInfos[bot]["walling"] = (self._playersInfos[bot]["positionY"] -1, self._playersInfos[bot]["positionX"])
                if self._playersInfos[bot]["moveChoice"][-1][1] == "S":
                    self._playersInfos[bot]["walling"] = (self._playersInfos[bot]["positionY"] +1, self._playersInfos[bot]["positionX"])
                if self._playersInfos[bot]["moveChoice"][-1][1] == "E":
                    self._playersInfos[bot]["walling"] = (self._playersInfos[bot]["positionY"], self._playersInfos[bot]["positionX"] + 1)
                if self._playersInfos[bot]["moveChoice"][-1][1] == "O":
                    self._playersInfos[bot]["walling"] = (self._playersInfos[bot]["positionY"], self._playersInfos[bot]["positionX"] - 1)

                self.pastePlayer(bot, "wall")


        print("\n".join(self._mapUsed))

#map = MapSelect()
#map.mapListPrinter()
#mapUsed = map.mapListSelecter()
#game = TurnAndTurn()
#game.map_refresh(mapUsed)
#game.mapWithoutX()
#print(game._mapOriginal)
#game.cleanMap()
#game.pastePlayer()
#print(game._mapUsed)
#print("\n".join(game._mapUsed))
#print(game._playersInfos, game._playerIconUsed[0])
#while 1:
#    game.inputChoice(game._playerIconUsed[0])
#    game.move(game._playerIconUsed[0])
