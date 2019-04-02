# -*- coding: utf-8 -*-


class Player:
    """Classe gérant les infos des joueurs"""

    def __init__(self, number):
        self.number = number
        self.idThread = None
        self.chatCom = None
        self.gameCom = None
        self.bot = None
        self.move = ""

    def send(self, msg):
        self.chatCom.send(msg.encode("utf-8"))

    def __repr__(self):
        info = (f"Numéro: {self.number}, id: {self.idThread} chatCom: "
                f"{self.chatCom}, gameCom: {self.gameCom} bot: {self.bot}")
        return info
