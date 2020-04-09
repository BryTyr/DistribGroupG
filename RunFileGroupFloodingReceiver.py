from Middleware.ConnectionSystem.ConnectionSystem import ConnectionSystem
from Middleware.GroupAdmin.GroupAdmin import GroupAdmin
from Middleware.MessageParsing.MessageParsing import MessageParsing
from Middleware.MessageHandler.MessageHandler import MessageHandler
from Middleware.FaultHandling.FaultHandling import FaultHandling




# run system
# runMessageReceiving()


def ReceiveGroupFlooding():
    connectionSystem = ConnectionSystem(12345)
    connectionSystem.ReceiveMessages()


ReceiveGroupFlooding()
