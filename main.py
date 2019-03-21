# coding: utf-8

from Data import infoClient, msgList
from Server import Server, SharedInfo
from MapSelect import MapSelect
from Turn import TurnAndTurn
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
            info = server.newClient(0.5)
            update = SharedInfo(info[0])
            update.start()
            id = update.getName()
            name = f"Player {len(infoClient) + 1}"
            infoClient[(id, name)] = info[0]
            info[0].send("Connexion établie".encode("utf-8"))
            # send to others clients when client join.
            for player in infoClient.values():
                if player != id:
                    player.send(f"le {name} s'est connecté".encode("utf-8"))
            print(infoClient)
        except socket.timeout:
            if msgList[-1].upper() == "C":
                server.searchBool = False
except OSError:
    import Client
    Client.launchClient()

game = TurnAndTurn()
game.map_refresh(mapUsed)
game.mapWithoutX()
print(game._mapOriginal)
game.cleanMap()
print(game._mapUsed)

for player, socket in infoClient.items():
    game.pastePlayer()
    socket.send("\n".join(game._mapUsed).encode())

while 1:
    game.inputChoice(game._playerIconUsed[0])
    game.move(game._playerIconUsed[0])
