# -*- coding: utf-8 -*-

from Tools import *
from MapSelect import *
from Data import playerIcon, playerIconUsed
import pickle
import time


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

    def getMap(self):
        return self._mapUsed

    def getLastMove(self, bot):
        return self._playersInfos[bot]["moveChoice"][-1]

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
            if oldCase == ".":
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
            if cmd == "door":
                self._playersInfos[bot]["turnNumber"][0] += 1
                chaine = self._mapUsed[self._playersInfos[bot]["drilling"][0]]
                deb = chaine[0:(self._playersInfos[bot]["drilling"][1])]
                fin = chaine[self._playersInfos[bot]["drilling"][1] + 1:]
                refreshChain = deb+"."+fin
                self._mapUsed[self._playersInfos[bot]["drilling"][0]] = refreshChain

                return self._mapUsed

            elif cmd == "wall":
                self._playersInfos[bot]["turnNumber"][0] += 1
                chaine = self._mapUsed[self._playersInfos[bot]["walling"][0]]
                deb = chaine[0:(self._playersInfos[bot]["walling"][1])]
                fin = chaine[self._playersInfos[bot]["walling"][1] + 1:]
                refreshChain = deb+"O"+fin
                self._mapUsed[self._playersInfos[bot]["walling"][0]] = refreshChain

                return self._mapUsed

        if cmd == "newPlayer":
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

        elif cmd == "cut":
            self._mapUsed = cutMe(bot)

        elif cmd == "paste":
            self._mapUsed = pasteMe(bot)

        elif cmd == "wall" or cmd is "door":
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

        if direction == "N":
            i = 1
            while case != "O" and i <= self._playersInfos[bot]["positionY"]:
                case = self._mapUsed[self._playersInfos[bot]["positionY"] - i][self._playersInfos[bot]["positionX"]]
                probedCaseList.append(case)
                if case != "O":
                    i += 1
        elif direction == "S":
            i = 1
            while case != "O" and i < len(self._mapUsed) - self._playersInfos[bot]["positionY"]:
                case = self._mapUsed[self._playersInfos[bot]["positionY"] + i][self._playersInfos[bot]["positionX"]]
                probedCaseList.append(case)
                if case != "O":
                    i += 1
        elif direction == "E":
            i = 1
            print(len(self._mapUsed[self._playersInfos[bot]["positionY"]]))
            print(self._playersInfos[bot]["positionX"])
            print((len(self._mapUsed[self._playersInfos[bot]["positionY"]]) - self._playersInfos[bot]["positionX"])-1)
            while case != "O" and i <= (len(self._mapUsed[self._playersInfos[bot]["positionY"]]) - self._playersInfos[bot]["positionX"]) - 1:
                case = self._mapUsed[self._playersInfos[bot]["positionY"]][self._playersInfos[bot]["positionX"] + i]
                probedCaseList.append(case)
                if case != "O":
                    i += 1
        elif direction == "O":
            i = 1
            while case != "O" and i <= self._playersInfos[bot]["positionX"]:
                case = self._mapUsed[self._playersInfos[bot]["positionY"]][self._playersInfos[bot]["positionX"] - i]
                probedCaseList.append(case)
                if case != "O":
                    i += 1

        elif direction == "all":
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
            if value == "N":
                fullWordList.append("au Nord")
            elif value == "S":
                fullWordList.append("au Sud")
            elif value == "E":
                fullWordList.append("à l'Est")
            elif value == "O":
                fullWordList.append("à l'Ouest")

        if len(fullWordList) > 0:
            return fullWordList
        else:
            return None

    def inputChoice(self, bot, sock):
        """Récupère le déplacement voulu par le joueur"""

        # Au premier tour, donne les indications sur la méthode pour entrer
        # les mouvements
        if self._playersInfos[bot]["turnNumber"][0] == 1:
            data = pickle.dumps(("info", "Vous pouvez \
choisir une direction à l'aide des commandes: 'N','S','O','E' suivie du nb de pas, percer avec 'P'"
", murer avec 'M'."))
            sock.send(data)
            time.sleep(5)

        else:
            data = pickle.dumps(("info", "Vous pouvez jouer."))
            sock.send(data)
            time.sleep(0.5)

        # On récupère la commande du joueur en vérifiant qu'il la rentre
        # correctement.

        moveInput = [""]
        boléen0 = False
        boléen1 = False
        avalaibleMove = []

        # Récupération des cases adjacentes au robot

        souroundingsDict = self.surroundingsChecker(bot)
        for key, value in souroundingsDict.items():
            if value == " " or value == "." or value == "U":
                avalaibleMove.append(key)
            if value == "." and avalaibleMove.count("M") == 0:
                avalaibleMove.append("M")
            if value == "O" and avalaibleMove.count("P") == 0:
                avalaibleMove.append("P")
        avalaibleMove.append("Q")

        avalaibleMoveTxt = ""
        for lettre in avalaibleMove:
            avalaibleMoveTxt += f" '{lettre}' "

        sourrounding = self.surroundingsChecker(bot, "all")
        indexListWall = dictIndexGetter(sourrounding, "O")
        indexListDoor = dictIndexGetter(sourrounding, ".")
        print('indexListDoor', indexListDoor, "indexListWall", indexListWall)

        while boléen0 is False and moveInput[0] != "Q":
            try:
                data = pickle.dumps(("map", "\n".join(self._mapUsed)))
                sock.send(data)
                data = pickle.dumps(("info", f"Choisissez votre action:\n{avalaibleMoveTxt}"))
                sock.send(data)
                move = sock.recv(1024).decode("utf-8").upper()

                if move[0] in avalaibleMove and len(move) == 1:
                    boléen0 = True
                    moveInput[0] = move
                    if move[0] == "Q":
                        return "Q"

                # Utilisateur entre une direction et un nombre de pas.
                elif move[0] in avalaibleMove and\
                     move[0] not in ["P", "M"] and\
                     len(move) > 1 and move[0] != "Q":
                    try:
                        step = int(move[1:])
                        caseListProbed, NbStep = self.surroundingsChecker(bot, move[0])

                        if step > NbStep - 1 or step < 1:
                            data = pickle.dumps(("info", "Vous n'avez pas rentré"
                                                 " un nb de pas correct. Vous "
                                                 f"pouvez faire {NbStep - 1} pas."))
                            sock.send(data)
                        else:
                            boléen0 = True
                            boléen1 = True
                            self._playersInfos[bot]["moveChoice"].append([move[0], step])

                    except ValueError:
                        data = pickle.dumps(("info", "Vous n'avez pas rentré un nb de pas correct."))
                        sock.send(data)
                        time.sleep(2)

                # Utilisateur entre une action et une direction.
                elif len(move) == 2 and move[0] in ["P", "M"]:
                    if move[0] == "P":
                        if len(indexListWall) == 0:
                            data = pickle.dumps(("info", "Vous ne pouvez pas percer. Aucun mur à proximité."))
                            sock.send(data)
                            time.sleep(2)
                        elif move[1] not in indexListWall:
                            data = pickle.dumps(("info", "Vous ne pouvez pas percer dans cette direction."))
                            sock.send(data)
                            time.sleep(2)
                            if len(indexListWall) > 0:
                                data = pickle.dumps(("info", "Vous pouvez percer"))
                        else:
                            self._playersInfos[bot]["moveChoice"].append(move)
                            boléen0 = True
                            boléen1 = True
                    else:
                        if len(indexListWall) == 0:
                            data = pickle.dumps(("info", "Vous ne pouvez pas murer. Aucune porte à proximité."))
                            sock.send(data)
                            time.sleep(2)
                        elif move[1] not in indexListDoor:
                            data = pickle.dumps(("info", "Vous ne pouvez pas murer dans cette direction."))
                            sock.send(data)
                            time.sleep(2)
                        else:
                            self._playersInfos[bot]["moveChoice"].append(move)
                            boléen0 = True
                            boléen1 = True

                else:
                    data = pickle.dumps(("info", "Votre commande n'est pas bonne."))
                    sock.send(data)
                    time.sleep(2)
            except IndexError:
                data = pickle.dumps(("info", "Votre commande n'est pas bonne."))
                sock.send(data)
                time.sleep(2)

        if len(move) == 1:

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
                                data = pickle.dumps(("info", f"Vous partez vers {direction}."
                                                     f" vous pouvez faire {NbStep - 1} pas."
                                                     " Combien souhaitez vous en faire ?"))
                                sock.send(data)
                                nbStep = sock.recv(1024).decode("utf-8")
                                nbStep = int(nbStep)

                                if nbStep > 0 and nbStep <= NbStep:
                                    moveInput.append(nbStep)
                                    boléen1 = True
                                    self._playersInfos[bot]["moveChoice"].append(moveInput)
                                    self._playersInfos[bot]["turnNumber"][1] = moveInput
                                else:
                                    data = pickle.dumps(("info", "Votre nombre est incorrect."))
                                    sock.send(data)
                                    time.sleep(2)
                            except ValueError:
                                data = pickle.dumps(("info", "Vous n'avez pas saisie un nombre."))
                                sock.send(data)
                                time.sleep(2)
                    else:
                        data = pickle.dumps(("info", "Vous ne pouvez pas aller dans cette direction."))
                        sock.send(data)
                        time.sleep(2)

                elif move[0] == "M":

                    doors = self.surroundingsChecker(bot, "all")
                    indexList = dictIndexGetter(doors, ".")

                    if len(indexList) == 0:
                        data = pickle.dumps(("info", "Vous ne pouvez murer aucune porte à proximité."))
                        sock.send(data)
                    else:
                        direction = self.cardinalFullWord(indexList)
                        avalaibleDirectionTemp = ""

                        for value in direction:
                            avalaibleDirectionTemp += value+", "

                        avalaibleDirection = avalaibleDirectionTemp[:-2]
                        while boléen1 is False:
                            data = pickle.dumps(("info", f"Vous avez choisi de murer."
                                                 f" Vous pouvez le faire {avalaibleDirection}."))
                            sock.send(data)
                            wallDir = sock.recv(1024).decode("utf-8").upper()
                            if wallDir in indexList:
                                moveInput.append(wallDir)
                                self._playersInfos[bot]["moveChoice"].append(moveInput)
                                self._playersInfos[bot]["turnNumber"][1] = moveInput
                                boléen1 = True

                elif move[0] == "P":

                    wall = self.surroundingsChecker(bot, "all")
                    indexList = dictIndexGetter(wall, "O")
                    if len(indexList) is 0:
                        data = pickle.dumps(("info", "Vous ne pouvez percer aucun mur à proximité."))
                        sock.send(data)
                        time.sleep(2)
                    else:
                        direction = self.cardinalFullWord(indexList)
                        avalaibleDirectionTemp = ""

                        for value in direction:
                            avalaibleDirectionTemp += value+", "

                        avalaibleDirection = avalaibleDirectionTemp[:-2]

                        while boléen1 is False:
                            data = pickle.dumps(("info", "Vous avez choisi de percer. Vous "
    f"pouvez le faire {avalaibleDirection}."))
                            sock.send(data)
                            drillDir = sock.recv(1024).decode("utf-8").upper()
                            if drillDir in indexList:
                                moveInput.append(drillDir)
                                self._playersInfos[bot]["moveChoice"].append(moveInput)
                                self._playersInfos[bot]["turnNumber"][1] = moveInput
                                boléen1 = True

    def passOrChoice(self, bot, sock):
        try:
            changeBool = True
            while changeBool is True:
                print(self._playersInfos[bot]["moveChoice"][-1][-1])
                lastMove = self._playersInfos[bot]["moveChoice"][-1]
                if self._playersInfos[bot]["moveChoice"][-1][-1] > 0:
                    data = pickle.dumps(("info", f"Votre dernier coup {lastMove}.\nVoulez vous changer de direction ? O/N"))
                    sock.send(data)
                    change = sock.recv(1024).decode("utf-8").upper()
                    if change == "O":
                        print("Je souhaite changer de déplacement")
                        self.inputChoice(bot)
                        changeBool = False
                    elif change == "N":
                        print("je ne change pas de direction")
                        pass
                        changeBool = False
                else:
                    print("je lance l'input car le nb de pas = 0")
                    self.inputChoice(bot, sock)
                    changeBool = False
        except (IndexError, TypeError):
            print("IndexError, je lance l'input")
            self.inputChoice(bot, sock)

    def move(self, bot, sock):
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
            data = pickle.dumps(("info", "Le crochetage de la porte vous a fait perdre un tour."))
            sock.send(data)
            time.sleep(2)
        else:

            self.passOrChoice(bot, sock)

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
        return self.win

        print("\n".join(self._mapUsed))
