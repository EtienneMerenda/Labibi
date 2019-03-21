# Définition d'un client réseau rudimentaire
# Ce client dialogue avec un serveur ad hoc

import socket
import threading
from Tools import UnblockingInput
import sys
import time


def launchClient(host='localhost', port=12800):

    host = host
    port = port

    class ThreadReception(threading.Thread):
        """Reception object manager. works with timed reception."""

        def __init__(self, com):
            threading.Thread.__init__(self)
            self._com = com

        def getMsg(self):
            return self.incomMsg

        def run(self):
            oldMsg = ""
            while sharedInfo["exchange"]["receive"] is True:
                try:
                    self._com.settimeout(5)
                    self.incomMsg = self._com.recv(1024).decode()
                    self._com.settimeout(None)
                except socket.error:
                    pass
                if self.incomMsg != oldMsg:
                    print(self.incomMsg)
                oldMsg = self.incomMsg
                if not self.incomMsg or self.incomMsg == "END":
                    print("Reception de la commande d'arret du client de la part"
                          " du serveur")
                    sharedInfo["exchange"]["receive"] = False
                    sharedInfo["exchange"]["sending"] = False

            self._com.close()
            exit()

    class ThreadSending(threading.Thread):
        """Sending object manager. Works with input hand-made by Bibi (use msvcrt)"""

        def __init__(self, com):

            threading.Thread.__init__(self)
            self._com = com
            self.send = True

        def run(self):

            import time

            while sharedInfo["exchange"]["sending"] is True:
                # Start input with delay, free
                sendingMsg = UnblockingInput("Message à envoyer: ")
                sendingMsg.start()
                # While user don't hit 'return' or 'escp', thread stay alive.
                while sendingMsg.isAlive() is True and sendingMsg.closeInput\
                        is False and sharedInfo["exchange"]["sending"] is True:
                    time.sleep(0.1)
                    if sendingMsg.closeClient is True:
                        print("Le client va se fermer sur demande de"
                              "l'utilisateur.")
                        sharedInfo["exchange"]["sending"] = False
                        sharedInfo["exchange"]["receive"] = False
                        self._com.send("Q".encode())
                if sharedInfo["exchange"]["sending"] is True:
                    msg = sendingMsg.getInput()
                    self._com.send(msg.encode())

    def interupt(self):
        """Function called when user close the windows"""
        comm.send("Q".encode())
        sys.exit(0)

    def getMsg(self):
        return th_R.getMsg()

    sharedInfo = {"exchange": {"sending": True, "receive": True}}

    comm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        comm.connect((host, port))
    except socket.error:
        print("La connexion a échoué.")
        sys.exit()


    # Thread are assigned and launched
    th_E = ThreadSending(comm)
    th_R = ThreadReception(comm)
    th_R.start()
    time.sleep(0.5)
    th_E.start()

    while 1:
        if sharedInfo["exchange"]["receive"] is False and\
           sharedInfo["exchange"]["sending"] is False:
            sys.exit(0)
