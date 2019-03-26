# -*- coding: utf-8 -*-

from tkinter import *

class ServerGUI():

    def __init__(self):
        self.win = Tk()
        self.label = Label(self.win, text="Serveur RobCo")
        self.label.pack()
        self.win.mainloop()

    def display(self, txt):
        self.label["text"] = txt

test = ServerGUI()
r = input(">")
test.display(r)
