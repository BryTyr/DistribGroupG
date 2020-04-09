from Middleware.ConnectionSystem.ConnectionSystem import ConnectionSystem
from Middleware.GroupAdmin.GroupAdmin import GroupAdmin


def runMessageSending():
    connectionSystem = ConnectionSystem()
    connectionSystem.SendMessage("hello World!")

def runMessageReceiving():
    connectionSystem = ConnectionSystem()
    connectionSystem.ReceiveMessages()



# run system
#runMessageSending()

def JoinGroup():
    connectionSystem = ConnectionSystem(11111112)
    groupAdmin = GroupAdmin(connectionSystem,11111112)
    # join group by supplying Group id and member id
    groupAdmin.joinGroup(555,11111112)
    connectionSystem.ReceiveMessages()

JoinGroup()
