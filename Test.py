#-*- coding: utf-8 -*-

from Tools import *
from Turn import *
import unittest
import os

class TestToolsAndMap(unittest.TestCase):

    def testFileListMaker(self):

        try:
            with self.assertRaises(FileNotFoundError):
                self.assertEqual(fileListMaker("./maps"), os.listdir("./maps"))
            print("Les dossier Maps n'existe pas.")
        except AssertionError:
            print("Le dossier Maps est présent")

        self.assertNotEqual(len(fileListMaker("./maps")), 0, "Le dossier Maps ne contient pas de cartes.")

        self.assertEqual(fileListMaker("./maps"), os.listdir("./maps"))

    def testMapListPrinter(self):

        for items in extensionRemover(fileListMaker("./maps"), ".txt"):
            self.assertNotRegex(items , ".txt", "Les extensions sont encore présentes.")

    def testInputWithNumberConstraint(self):
        i = 0
        while i < 5:
            Num = i
            self.assertGreaterEqual(inputWithNumberConstraint(5, 0, cmd="test", testNumber=Num), 0)
            self.assertEqual(inputWithNumberConstraint(5, 0, cmd="test", testNumber=Num), i)
            self.assertLessEqual(inputWithNumberConstraint(5, 0, cmd="test", testNumber=Num), 5)
            i += 1

    def testInputWithCaraterConstraint(self):
        import string
        alphabet = list(string.ascii_letters)
        for items in alphabet:
            self.assertIn(inputWithCaraterConstraint("", alphabet, "test", items), alphabet)

    def testCaraterListChecker(self):
        testList = ["000000000010000000000","000000000000","000000000100"]
        self.assertEqual(len(caracterListChecker(testList, "1")), 2)
        self.assertEqual(caracterListChecker(testList, "1"), ([0, 2], ["000000000010000000000", "000000000100"]))

    def testCaracterStringChecker(self):
        stringTest = "000000000010000000000"
        self.assertEqual(caracterStringChecker(stringTest, "1"), 10)

    def testDictIndexGetter(self):
        testDict = {"a": 0, "b": 1, "c": 2, "d": 3}
        self.assertEqual(dictIndexGetter(testDict, 2), ["c"])

    print("Fichier Tools.py fonctionnel.")

class TestTurn(unittest.TestCase):

    def testMapWithoutX(self):
        self.assertNotIn("X", ["1867sqdegfsXetgqdsgh46564"])

    def testPasteMe(self):
        # Test de la méthode newPlayer de PasteMe
        test = TurnAndTurn()
        test._mapUsed = ["OOOOOOOOOO", "O O    O O", "O . OO   O",
                         "O O O    O", "O OOOO O.O", "O O O    U",
                         "O OOOOOO.O", "O O      O", "O O OOOOOO",
                         "O . O    O", "OOOOOOOOOO"]
        print()
        i = 0
        bool = False
        j = len(test._playerIcon)
        while j > 0:
            test.pastePlayer()
            for item in test._mapUsed:
                if test._playerIconUsed[i] in item:
                    self.assertIn(test._playerIconUsed[i], item)
                    bool = True
            j -= 1
            i += 1
        self.assertIs(bool, True)

    # -------------------------------------------------------------------
    # Test de la fonction paste et cut

        test.pastePlayer(bot="X", cmd="cut")
        self.assertIs(caracterListChecker(test._mapUsed, "X"), False)
        test.pastePlayer(bot="X", cmd="paste")
        self.assertIsNot(caracterListChecker(test._mapUsed, "X"), False)

    # -------------------------------------------------------------------
    # Test de la méthode perçage
        test._mapUsed = ["OOOOOOOOOO", "O O    O O", "O . OO   O",
                         "O O O    O", "O OOOO O.O", "O O O    U",
                         "O OOOOOO.O", "O O     XO", "O O OOOOOO",
                         "O . O    O", "OOOOOOOOOO"]
        test._playersInfos["X"]["positionY"] = 7
        test._playersInfos["X"]["positionX"] = 8
        test._playersInfos["X"]["moveChoice"] = ["PS"]
        test.move(bot="X")
        self.assertIs(test._mapUsed[8][8], ".")

    # Test de la méthode murage

        test._playersInfos["X"]["moveChoice"] = ["MS"]
        test.move(bot="X")
        self.assertIs(test._mapUsed[8][8], "O")

    def testSurroundingChecker(self):
        test = TurnAndTurn()
        test._mapUsed = ["OOOOOOOOOO", "O O    O O", "O . OO   O",
                         "O O O    O", "O OOOO O.O", "O O O    U",
                         "O OOOOOO.O", "O O     XO", "O O OOOOOO",
                         "O . O    O", "OOOOOOOOOO"]
        test._playersInfos["X"] = {"positionY": 7, "positionX": 8}
        self.assertIs(len(test.surroundingsChecker("X")), 4)
        self.assertEqual(test.surroundingsChecker("X"), {"N": ".", "S": "O",
                                                      "E": "O", "O": " "})

    def testCardianlFullWord(self):
        test = TurnAndTurn()
        listTest = ["N", "S", "E", "O"]
        self.assertEqual(test.cardinalFullWord(listTest), ["au Nord", "au Sud",
                                                           "à l'Est", "à l'Ouest"])





if __name__ == '__main__':
    unittest.main()
