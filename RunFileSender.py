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
    connectionSystem = ConnectionSystem()
    groupAdmin = GroupAdmin(connectionSystem)
    # join group by supplying Group id and member id
    groupAdmin.joinGroup(555,11111111)

JoinGroup()
