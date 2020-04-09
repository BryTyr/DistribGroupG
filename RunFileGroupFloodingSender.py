from Middleware.ConnectionSystem.ConnectionSystem import ConnectionSystem
from Middleware.GroupAdmin.GroupAdmin import GroupAdmin
from Middleware.MessageParsing.MessageParsing import MessageParsing
from Middleware.MessageHandler.MessageHandler import MessageHandler
from Middleware.FaultHandling.FaultHandling import FaultHandling




# run system
# runMessageReceiving()


def SendGroupUpdateMessage():
    connectionSystem = ConnectionSystem(11111112)
    faultHandling = FaultHandling(connectionSystem,11111112)
    faultHandling.sendUpdateGroupActivity(555,11111112)
    connectionSystem.ReceiveMessages()



SendGroupUpdateMessage()
