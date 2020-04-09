from Middleware.ConnectionSystem.ConnectionSystem import ConnectionSystem
from Middleware.GroupAdmin.GroupAdmin import GroupAdmin
from Middleware.MessageParsing.MessageParsing import MessageParsing
from Middleware.MessageHandler.MessageHandler import MessageHandler
from Middleware.FaultHandling.ActiveNodeFlooding import ActiveNodeFlooding




# run system
# runMessageReceiving()


def SendGroupUpdateMessage():
    connectionSystem = ConnectionSystem(11111112)
    activeNodeFlooding = ActiveNodeFlooding(connectionSystem,11111112)
    activeNodeFlooding.sendUpdateGroupActivity(555,11111112)
    connectionSystem.ReceiveMessages()



SendGroupUpdateMessage()
