#-*- coding: utf-8 -*-

from threading import Thread
import msvcrt
from Data import runInput


def fileListMaker(path="./"):
    """Fonction recupérant la liste des fichiers present dans le dossier voulu
 et la retournant.
path: Chemin d'accès terminant par '/'"""

    import os
    fileInDirectory = os.listdir(path)
    return fileInDirectory


def extensionRemover(fileList, extension):
    """Fonction permettant de supprimer les extensions de fichiers contenus
dans une liste. Prend en paramètre la liste ainsi que le type d'extension
(format '.ext')"""

    strFileList = "".join(fileList)
    fileListWithoutExt = strFileList.split(str(extension))
    # ayant splitté par .txt, la dernière entrée est un champ vide que je
    # supprime.
    del fileListWithoutExt[-1]

    return fileListWithoutExt


def folderCleanerByExtKeeper(path="./", extension=".py"):
    """!!!Risque sérieux de supression de fichiers!!!

Fonction permettant de supprimer les fichiers dont l'extension ne correspond
 pas à celle entrée dans ladite fonction.

path: Chemin d'accès finissant par '/'
extension: Extension des fichiers à garder format '.ext'"""

    import os

    intruders = os.listdir(path)
    for item in intruders:
        if not item.endswith(extension):
            os.remove(path + item)


def inputWithNumberConstraint(hiestNumber, lowestNumber=0,
                              answer="\nSaisissez le numéro de la carte que \
vous voulez jouer: ", cmd="", testNumber= ""):
    """Retourne le nombre choisi par l'utilisateur entrant dans des critères précis:
hiestNumber: Le nombre le plus haut
lowestNumber: Le nombre le plus bas."""

    condition = False
    while condition is False:
        try:
            if cmd is "":
                number = input(answer)
                number = int(number)

            elif cmd is "test":
                number = testNumber
                number = int(number)
            if number >= lowestNumber and number <= hiestNumber:
                condition = True
            else:
                print("\nVous n'avez pas rentré un numéro valide.")
        except ValueError:
            print("Vous n'avez pas rentré un nombre.\n")

    return number


def inputWithCaraterConstraint(msg, constraintList, cmd="", testChoice=""):
    """Retourne le nombre choisi par l'utilisateur entrant dans des critères précis:
Liste des caractères"""
    choice = ""
    booléen = False
    while booléen is False:
        if cmd == "test":
            choice = testChoice
        else:
            choice = input(msg)
        if choice in constraintList:
            booléen = True

    return choice


def caracterListChecker(list, sensingObject):
    """Retourne une liste des index des String contenant le caractère cherché.
    Ou False si il n'y en a pas."""
    i = 0
    indexlist = []
    stringList = []
    for string in list:
        if string.find(sensingObject) >= 0:
            indexlist.append(i)
            stringList.append(string)
        i += 1
    if len(indexlist) > 0:
        return indexlist, stringList
    else:
        return False


def caracterStringChecker(string, sensingObject):
    """Retourne l'index d'un caractère précis dans une chaine de caratère.
Utiliser une boucle for pour vérifier plusieurs chaines de caractère."""
    indexCaracter = string.find(sensingObject)
    return indexCaracter


def dictIndexGetter(dict, value):
    """Retourne les clefs du dictionnaire correspondant à la valeur rentrée."""
    indexList = []
    for keys, values in dict.items():
        if values == value:
            indexList.append(keys)

    return indexList

class UnblockingInput(Thread):
    """Fonction identique à input sans le blocage.

    Changer l'attribut self.closeInput en True pour couper l'input.

    """

    def __init__(self, txt=">"):
        Thread.__init__(self)
        self.txt = txt
        self.input = ""
        self.closeInput = False
        self.userInput = []

    def run(self):

        for char in self.txt:
            msvcrt.putwch(char)

        while runInput[0] is True and self.closeInput is False:
            if runInput[0] is True:
                if msvcrt.kbhit():
                    hitChar = msvcrt.getwch()
                    if hitChar == "\r":
                        self.closeInput = True
                        msvcrt.putwch("\n")
                    elif hitChar == '\x1b':
                        self.closeInput = True
                        self.closeClient = True
                    elif hitChar == "\x08":
                        if len(self.userInput) > 0:
                            msvcrt.putwch("\x08")
                            msvcrt.putwch(" ")
                            msvcrt.putwch("\x08")
                            del self.userInput[-1]
                        else:
                            pass
                    else:
                        self.userInput.append(hitChar)
                        msvcrt.putwch(hitChar)

            else:
                pass

        self.input = "".join(self.userInput)

    def getInput(self):

        return self.input
