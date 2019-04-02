# coding: utf-8

import pickle
from Data import infoClient, playerDict
from Server import Server, SharedInfo
from MapSelect import MapSelect
from Turn import TurnAndTurn
from Player import Player
from Client import ClientGUI, link
import select
import socket
import time

# Booléen

gameBool = True

# Acceptation des clients.
# Si un Serveur est déjà en ligne, lance un client.

try:
    server = Server()
    server.onLine()
    # Selection de la map.

    map = MapSelect()
    map.mapListPrinter()
    mapUsed = map.mapListSelecter()
    mapData = ("map", map._mapChoiced)
    data = pickle.dumps(mapData)
    print(map._mapChoiced)

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
            # print(playerDict)
            playerDict[f"player{len(playerDict)}"]\
                .chatCom.send("Connexion établie".encode("utf-8"))
            playerDict[f"player{len(playerDict)}"]\
                .gameCom.send(data)
            # Envoi aux autre clients quand un message est reçu
            for player in playerDict.values():
                if player.idThread != id:
                    player.chatCom.send(f"le joueur {len(playerDict)} "
                                        "s'est connecté".encode("utf-8"))

        except socket.timeout:
            for client in playerDict.values():
                try:
                    rlist, wlist, xlist = select.select([client.gameCom], [], [], 0.05)
                except select.error:
                    pass
                try:
                    tmp = rlist[0].recv(1024).decode("utf-8")
                    if tmp in ["c", "C"]:
                        server.searchBool = False
                except IndexError:
                    pass

except OSError:
    infoCom = link()
    client = ClientGUI()
    client.start_(infoCom[1])


# Une fois l'acceptation des clients terminé, trie des infos pour une utilitée
# simplifiée

game = TurnAndTurn()
game.map_refresh(mapUsed)
game.mapWithoutX()
print(game._mapOriginal)
game.cleanMap()
print(game._mapUsed)

# Collage des bots et attribution des objets players.

for i, player in enumerate(playerDict):
    (map, bot) = game.pastePlayer()
    playerDict[f"player{i + 1}"].bot = bot
    data = pickle.dumps(("info", f"Vous jouez le bot: {bot} et "
                         f"êtes le joueur {i + 1}."))
    playerDict[f"player{i + 1}"].gameCom.send(data)

# envoi de la carte

data = pickle.dumps(("map", "\n".join(game.getMap())))
time.sleep(0.2)

for i, player in enumerate(playerDict):
    playerDict[f"player{i + 1}"].gameCom.send(data)
time.sleep(3)

# début des tours de jeu.

while gameBool:
    for player in playerDict.values():
        winBool = game.move(player.bot, player.gameCom)
        data = pickle.dumps(("info", "votre tour est terminé."))
        player.gameCom.send(data)
        # actualisation des cartes pour les clients
        time.sleep(0.5)
        data = pickle.dumps(("map", "\n".join(game.getMap())))
        print(winBool)
        for player in playerDict.values():
            player.gameCom.send(data)

        if winBool is True:
            gameBool = False
            data = pickle.dumps(("info",f"Le joueur {player.number} a gagné !!"))
            for player in playerDict.values():
                player.gameCom.send(data)
            time.sleep(1)
            data = pickle.dumps(("info", "END"))
            for player in playerDict.values():
                player.gameCom.send(data)
            break

print("Fin du jeu")
