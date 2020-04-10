from Middleware.ConnectionSystem.ConnectionSystem import ConnectionSystem
from Middleware.GroupAdmin.GroupAdmin import GroupAdmin
from Middleware.CommunicationManager.CommunicationManager import CommunicationManager


def sendMessage():
    connectionSystem = ConnectionSystem(11111111)
    connectionSystem.callMessageSender(555,"message sent through system")
    #communicationManager = CommunicationManager(connectionSystem,11111111)
    #communicationManager.sendMessage(555,"message sent through system")
    connectionSystem.ReceiveMessages()

sendMessage()
