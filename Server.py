# -*- coding: utf-8 -*-

"""Script établissant un server gérant plusieurs client avec échange de
 messages."""

import threading
import socket
from Data import infoClient, msgList


class Server():

    def __init__(self):

        self.searchBool = True

    def onLine(self):
        """Classe mettant en ligne le server"""

        # création de la connection serveur.
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.bind(('localhost', 12800))
        print("Serveur en ligne.")

    def newClient(self, time=None):
        """Accepte les client
        Retourne client_socket, (ip, port)"""
        self._server.settimeout(time)
        self._server.listen(5)
        client_socket, (ip, port) = self._server.accept()
        self._server.settimeout(None)

        return client_socket, (ip, port)

    def stopAcces(self):
        self._com.send("END".encode())


class SharedInfo(threading.Thread):

    def __init__(self, com):
        threading.Thread.__init__(self)
        self._com = com
        self._comEnd = False

    def run(self):
        # Get the identifier of the thread to use it to avoid sending a message to itself.
        id = self.getName()
        while self._comEnd is False:
            msgClient = self._com.recv(1024).decode()
            if not msgClient or msgClient.upper() == "Q":
                self._comEnd = True
                self._com.send("END".encode())
            else:
                msg = "{0}> {1}".format(id, msgClient)
                print(msg)
                for cle in infoClient:
                    if cle != id:
                        infoClient[cle].send(msg.encode())
            msgList.append(msgClient)

        self._com.close()
        del infoClient[id]
        print("Client {} déconnecté.".format(id))
