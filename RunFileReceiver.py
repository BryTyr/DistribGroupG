from Middleware.ConnectionSystem.ConnectionSystem import ConnectionSystem
from Middleware.GroupAdmin.GroupAdmin import GroupAdmin
from Middleware.MessageParsing.MessageParsing import MessageParsing


def runMessageSending():
    connectionSystem = ConnectionSystem()
    connectionSystem.CreateMessage("hello World!")

def runMessageReceiving():
    connectionSystem = ConnectionSystem()
    connectionSystem.ReceiveMessages()



# run system
# runMessageReceiving()


def AddToGroup():
    groupAdmin = GroupAdmin()
    messageParsing = MessageParsing()
    connectionSystem = ConnectionSystem()
    Message = connectionSystem.ReceiveMessages()
    print('Receives message: '+Message)
    GroupID,MemberID = messageParsing.parseMessages(Message)

    groupAdmin.addToGroup(GroupID,MemberID)

AddToGroup()
