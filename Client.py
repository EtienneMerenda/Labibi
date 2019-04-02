# -*- coding: utf-8 -*-

import pickle
import socket
import threading
import sys
import time
import select
from Data import manager, runInput

from tkinter import Tk, StringVar, Label, Entry
from Data import GUIDict


class ThreadReception(threading.Thread):
    """Reception object manager. works with timed reception."""

    def __init__(self, com):
        threading.Thread.__init__(self)
        self._com = com

    def run(self):
        while manager["exchange"]:
            time.sleep(0.05)
            try:
                self._com.settimeout(5)
                manager["incomMsg"] = self._com.recv(1024).decode()
                self._com.settimeout(None)

                if not manager["incomMsg"] or manager["incomMsg"] == "END":
                    GUIDict["labiRcv"] = ("Reception de la commande "
                                          "d'arret du client de la "
                                          "part du serveur")
                    manager["exchange"] = False

                else:
                    GUIDict["chatRcv"] = manager["incomMsg"]
                    GUIDict["flagChatRcv"] = True


            except socket.error:
                pass

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

        while manager["exchange"]:
            time.sleep(0.05)
            if GUIDict["flagChatSd"] is True:
                self._com.send(GUIDict["chatSd"].encode("utf-8"))
                GUIDict["flagChatSd"] = False
                if manager["incomMsg"] == "Q":
                    GUIDict["labiRcv"] = ("Le client va se fermer sur "
                                          "demande de l'utilisateur.")
                    manager["exchange"] = False
                    self._com.send("Q".encode())
            elif GUIDict["flagLabiSd"] is True:
                self._comMove.send(GUIDict["labiSd"].encode("utf-8"))
                print("envoyé")
                GUIDict["flagLabiSd"] = False

class ClientGUI():

    def __init__(self):

        self.win = Tk()
        self.win.geometry("960x600")
        self.win.grid()
        self.win.title("Seveur RobCo")

        self.userEntry = StringVar()
        self.userEntryLabibi = StringVar()
        self.chatRcv = StringVar()
        self.labibiRcv = StringVar()

        GUIDict["chatRcv"] = ""
        GUIDict["labiRcv"] = ""
        GUIDict["flagChatRcv"] = ""
        GUIDict["oldLabiRcv"] = ""
        GUIDict["chatSd"] = ""
        GUIDict["flagChatSd"] = ""
        GUIDict["labiSd"] = ""
        GUIDict["flagLabiSd"] = ""
        GUIDict["labiGrid"] = ""
        GUIDict["oldLabiGrid"] = ""

        self.createWidget()

    def createWidget(self):

        self.labiGrid = Label(self.win, font="Consolas", text="", width=52, height=25)
        self.labiGrid.grid(column=0, row=0, sticky="nsew")

        self.labiText = Label(self.win, text="Entrez 'C' pour lancer la partie.",
                              wraplength=350, font="Consolas")
        self.labiText.grid(column=0, row=1)

        self.inputLabibi = Entry(self.win, textvariable=self.userEntryLabibi, font="Consolas")
        self.inputLabibi.grid(column=0, row=2, sticky="ew")

        self.bothMsgRcv = Label(self.win, text="Vous êtes sur le chat de RobCop.",
                                font="Consolas")
        self.bothMsgRcv.grid(column=1, row=1)

        self.msgRecever = Label(self.win,
                                text="", justify="left", wraplength=350,
                                width=52, height=25, anchor="sw", font="Consolas")
        self.msgRecever.grid(column=1, row=0, sticky="sw")

        self.input_ = Entry(self.win, textvariable=self.userEntry, font="Consolas")
        self.input_.grid(column=1, row=2, sticky="ew")

        self.win.bind("<Return>", self.getInput)

    def getInput(self, event):
        focus = self.win.focus_get()

        if focus is self.input_:
            tmp = self.userEntry.get()
            self.userEntry.set("")
            GUIDict["chatSd"] = tmp
            GUIDict["flagChatSd"] = True

        elif focus is self.inputLabibi:

            tmp = self.userEntryLabibi.get()
            self.userEntryLabibi.set("")
            GUIDict["labiSd"] = tmp
            GUIDict["flagLabiSd"] = True
            if tmp in ["C", "c"]:
                self.labiText["text"] = ""

    def refreshChat(self):
        if GUIDict["flagChatRcv"] is True:
            self.msgRecever["text"] += f"\n{GUIDict['chatRcv']}"
            GUIDict["flagChatRcv"] = False

    def refreshLabi(self):
        if GUIDict["labiRcv"] != GUIDict["oldLabiRcv"]:
            self.labiText["text"] = GUIDict["labiRcv"]
            GUIDict["oldLabiRcv"] = GUIDict["labiRcv"]

    def refreshLabiGrid(self):
        if GUIDict["labiGrid"] != GUIDict["oldLabiGrid"]:
            self.labiGrid["text"] = GUIDict["labiGrid"]

    def start_(self, comGame):

        while True:
            if manager["exchange"] is False:
                sys.exit(0)
            try:
                rlist, wlist, xlist = select.select([comGame], [], [], 0.05)
            except select.error:
                pass
            try:
                tmp = rlist[0].recv(1024)
                print(tmp)
                data = pickle.loads(tmp)
                print(data)
                if data[0] == "map":
                    GUIDict["labiGrid"] = data[1]
                elif data[0] == "info":
                    print("texte changé")
                    GUIDict["labiRcv"] = data[1]
                elif data[0] == "infoP":
                    self.bothMsgRcv["text"] = data[1]
            except IndexError:
                pass

            self.win.update_idletasks()
            self.win.update()
            self.refreshChat()
            self.refreshLabi()
            self.refreshLabiGrid()


def link():

    host = "localhost"
    port = 12800

    comTchat = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    comGame = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        comTchat.connect((host, port))
        comGame.connect((host, port))

    except socket.error:
        root = Tk()
        error = Label(root, text=("La connexion a échouée. Lancez le serveur."))
        error.grid()
        root.update()
        time.sleep(3)
        sys.exit()

    # Thread are assigned and launched
    th_E = ThreadSending(comTchat, comGame)
    th_R = ThreadReception(comTchat)
    th_R.start()
    time.sleep(0.5)
    th_E.start()

    return comTchat, comGame
