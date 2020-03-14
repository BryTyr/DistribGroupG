from Middleware.ConnectionSystem.ConnectionSystem import ConnectionSystem


def runMessageSending():
    connectionSystem = ConnectionSystem()
    connectionSystem.CreateMessage("hello World!")

def runMessageReceiving():
    connectionSystem = ConnectionSystem()
    connectionSystem.ReceiveMessages()



# run system
runMessageReceiving()
