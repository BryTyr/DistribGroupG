from Middleware.ConnectionSystem.ConnectionSystem import ConnectionSystem
from Middleware.GroupAdmin.GroupAdmin import GroupAdmin
from Middleware.MessageParsing.MessageParsing import MessageParsing
from Middleware.MessageHandler.MessageHandler import MessageHandler


def runMessageSending():
    connectionSystem = ConnectionSystem()
    connectionSystem.CreateMessage("hello World!")

def runMessageReceiving():
    connectionSystem = ConnectionSystem()
    connectionSystem.ReceiveMessages()



# run system
# runMessageReceiving()


def AddToGroup():
    connectionSystem = ConnectionSystem(12345)
    connectionSystem.ReceiveMessages()


    # print('Receives message: '+Message)
    # GroupID,MemberID = messageParsing.parseMessages(Message)
    #
    # groupAdmin.addToGroup(GroupID,MemberID)

AddToGroup()
