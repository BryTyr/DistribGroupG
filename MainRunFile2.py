from Middleware.ConnectionSystem.ConnectionSystem import ConnectionSystem
from Client.GUI import GUI


import tkinter as tk
import threading

class App(threading.Thread):
    gui=""
    connectionSystem=""
    UserID=""

    def __init__(self,ConnectionSystem,UserID):
        self.connectionSystem = ConnectionSystem
        self.UserID=UserID
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        print("Callback")

    def run(self):
        print(type(self.connectionSystem))
        self.gui = GUI(self.connectionSystem,self.UserID)
        self.passGUIToBackEnd()
        self.gui.setUp_Window()

    def passGUIToBackEnd(self):
        self.connectionSystem.passGUI(self.gui)




#11111111
#11111112
connectionSystem = ConnectionSystem(11111112)
app = App(connectionSystem,11111112)
print('Now we can continue running code while mainloop runs!')
# default backend behaviour
connectionSystem.ReceiveMessages()
