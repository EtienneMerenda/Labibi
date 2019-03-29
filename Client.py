# Définition d'un client réseau rudimentaire
# Ce client dialogue avec un serveur ad hoc

import socket
import threading
from Tools import UnblockingInput
import sys
import time
import select
from Data import manager, runInput
from GUI import ClientGUI

def launchClient(host='localhost', port=12800):

    host = host
    port = port

    class ThreadReception(threading.Thread):
        """Reception object manager. works with timed reception."""

        def __init__(self, com):
            threading.Thread.__init__(self)
            self._com = com

        def run(self):
            oldMsg = ""
            while manager["exchange"]:
                try:
                    self._com.settimeout(5)
                    manager["incomMsg"] = self._com.recv(1024).decode()
                    self._com.settimeout(None)
                except socket.error:
                    pass
                if manager["incomMsg"] != oldMsg:
                    print(manager["incomMsg"])
                oldMsg = manager["incomMsg"]
                if not manager["incomMsg"] or manager["incomMsg"] == "END":
                    print("Reception de la commande d'arret du client de la part"
                          " du serveur")
                    manager["exchange"] = False

            self._com.close()
            exit()

    class ThreadSending(threading.Thread):
        """Sending object manager. Works with input hand-made by Bibi (use msvcrt)"""

        def __init__(self, com, comMove):

            threading.Thread.__init__(self)
            self._com = com
            self._comMove = comMove
            self.send = True
            self.break_ = False

        def run(self):

            import time

            while manager["exchange"]:
                while runInput[0]:
                    # Start input with delay, free
                    self.sendingMsg = UnblockingInput("Message à envoyer: ")
                    self.sendingMsg.start()
                    # While user don't hit 'return' or 'escp', thread stay alive.
                    while self.sendingMsg.isAlive():
                        time.sleep(0.1)
                        if manager["incomMsg"] is "Q":
                            print("Le client va se fermer sur demande de"
                                  "l'utilisateur.")
                            manager["exchange"] = False

                            self._com.send("Q".encode())

                    msg = self.sendingMsg.getInput()
                    self._com.send(msg.encode())


        def interupt(self):
            """Function called when user close the windows"""
            self._com.send("Q".encode())
            sys.exit(0)

        def is_Alive(self):
            return self.sendingMsg.isAlive()

    comTchat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    comGame = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        comTchat.connect((host, port))
        comGame.connect((host, port))

    except socket.error:
        print("La connexion a échoué.")
        sys.exit()



    # Thread are assigned and launched
    th_E = ThreadSending(comTchat, comGame)
    th_R = ThreadReception(comTchat)
    th_R.start()
    time.sleep(0.5)
    th_E.start()

    while 1:
        if manager["exchange"] is False:
            sys.exit(0)

        try:
            rlist, wlist, xlist = select.select([comGame], [], [], 0.05)
        except select.error:
            pass
        try:
            msg = rlist[0].recv(1024).decode("utf-8")
            runInput[0] = False
            print(msg)
            while th_E.is_Alive():
                print(time.time())
            r = input("> oui ? :")
            rlist[0].send(r.encode("utf-8"))
            runInput[0] = True
        except IndexError:
            pass

        msg = comGame.recv(1024).decode("utf-8")
        print(msg)
