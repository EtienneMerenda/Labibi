# -*- coding: utf-8 -*-


class Player:
    """Classe gérant les infos des joueurs"""

    def __init__(self, number, address):
        self.number = number
        self.address = address
        self.bot = None

    def send(self, msg):
        self.address.send(msg.encode("utf-8"))

    def __repr__(self):
        info = f"Numéro: {self.number}, address: {self.address}, bot: {self.bot}"
        return info
