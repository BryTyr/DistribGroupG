from Middleware.ConnectionSystem.ConnectionSystem import ConnectionSystem
from Middleware.CommunicationManager.CommunicationManager import CommunicationManager
from Middleware.GroupAdmin.GroupAdmin import GroupAdmin
from Middleware.MessageParsing.MessageParsing import MessageParsing
from Middleware.MessageHandler.MessageHandler import MessageHandler




def displayMessage():
    connectionSystem = ConnectionSystem(12345)
    connectionSystem.ReceiveMessages()
    #communicationManager.displayMessages(555)


displayMessage()
