# coding: utf-8

from Data import infoClient, msgList, playerDict
from Server import Server, SharedInfo
from MapSelect import MapSelect
from Turn import TurnAndTurn
from Player import Player
import socket

# Acceptation des clients.
# Si un Serveur est déjà en ligne, lance un client.


try:
    server = Server()
    server.onLine()

    # Selectoin de la map.

    map = MapSelect()
    map.mapListPrinter()
    mapUsed = map.mapListSelecter()

    print(f"Vous avez choisie la carte: {map._mapTitleProper[mapUsed[2]]}\n\n{map._mapChoiced}")

    print("Serveur en attente d'acceptation.")

    while server.searchBool is True:
        # Début de l'acceptation de client
        try:
            chatCom = server.newClient(1)
            gameCom = server.newClient(0.5)
            update = SharedInfo(chatCom[0])
            update.start()
            id = update.getName()

            playerObject = Player(len(playerDict) + 1)
            playerObject.idThread = id
            playerObject.chatCom = chatCom[0]
            playerObject.gameCom = gameCom[0]

            infoClient[id] = chatCom[0]

            playerDict[f"player{len(playerDict) + 1}"] = playerObject

            playerDict[f"player{len(playerDict)}"]\
                .chatCom.send("Connexion établie".encode("utf-8"))
            print(playerDict)
            # Envoi aux autre clients quand un message est reçu
            for player in playerDict.values():
                if player.idThread != id:
                    player.chatCom.send(f"le joueur {len(playerDict)} "
                                        "s'est connecté".encode("utf-8"))

        except socket.timeout:
            if msgList[-1].upper() == "C":
                server.searchBool = False

except OSError:
    import Client
    Client.launchClient()

# Une fois l'acceptation des clients terminé, trie des infos pour une utilitée
# simplifiée


game = TurnAndTurn()
game.map_refresh(mapUsed)
game.mapWithoutX()
print(game._mapOriginal)
game.cleanMap()
print(game._mapUsed)


for i, player in enumerate(playerDict):
    bot = game.pastePlayer()[1]
    playerDict[f"player{i + 1}"].bot = bot
    playerDict[f"player{i + 1}"].gameCom.send(f"Vous jouez le bot: {bot} et "
                                              f"êtes le joueur {i + 1}."
                                              "".encode("utf-8"))


while 1:
    for player in playerDict.values():
        game.inputChoice(player.bot, player.gameCom)
        game.move(player.bot)
